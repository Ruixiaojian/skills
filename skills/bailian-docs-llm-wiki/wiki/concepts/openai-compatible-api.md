# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 API 协议，其请求/响应格式、路径结构、认证方式与 OpenAI 官方 REST API 保持高度一致，使开发者能复用现有 OpenAI SDK（如 `openai` Python 包）、LangChain 集成、主流 AI 工具（Cursor、Dify、Claude Code 等）和已有代码逻辑，实现“零代码迁移”或“最小改造接入”。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移已有应用**：已基于 OpenAI SDK 开发的对话系统、Agent 或 RAG 应用，只需替换 `base_url` 和 `api_key`，即可直接调用百炼 Qwen、DeepSeek、Kimi、GLM 等数十种模型，无需重写业务逻辑。  
- **多模态统一接入**：通过 `/v1/chat/completions` 接口，可无缝调用 `qwen-vl-plus`、`qwen3-vl-plus`、`QVQ` 等视觉模型，输入含 `image_url` 或 Base64 图片的 `messages`，语义与字段完全兼容 OpenAI Vision 标准。  
- **增强智能体开发**：`/v1/responses` 是专为 Agent 设计的增强型兼容接口，内置联网搜索、代码解释器、网页提取等工具链，并支持 `previous_response_id` 自动维护多轮上下文，显著简化状态管理。  
- **向量与排序服务集成**：`/v1/embeddings` 和 `/v1/reranks` 接口分别支持文本/多模态嵌入与重排，与 LangChain 的 `OpenAIEmbeddings`、`CohereRerank` 等抽象层天然对齐，可直接注入 RAG 流水线。  
- **批量与[文件处理](file-processing.md)**：`/v1/files` 支持 `purpose=file-extract`（长文档解析）、`purpose=batch`（异步批量推理），配合 JSONL 输入，适用于 ETL、知识库构建等规模化场景。  
- **专用模型轻量接入**：`farui-plus`（法律）、`qwen-mt-plus`（翻译）、`qwen3.5-ocr`（OCR）等垂直模型均开放 OpenAI 兼容入口，仅需在 `model` 字段指定对应 ID，即可复用标准 chat 接口调用范式。

> ⚠️ 注意：`qwen-deep-research`、`qwen-audio`、`gte-rerank-v2`（即将下线）及部分多模态 embedding 模型（如 `qwen3-vl-embedding`）**不支持** OpenAI 兼容协议，必须使用 DashScope 原生接口。

## 关键参数和配置

| 参数 | 类型 | 说明 | 注意事项 |
|------|------|------|----------|
| `base_url` | string | 必填，服务端点地址 | **必须使用业务空间专属域名**，例如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；旧域名 `dashscope.aliyuncs.com` 已不推荐，性能与稳定性较低。 |
| `api_key` | string | 必填，认证密钥 | 使用 DashScope API Key（非 OpenAI Key），且需与计费方案匹配（[Token](token.md) Plan、Coding Plan 的 Key 不可混用）。 |
| `model` | string | 必填，模型标识符 | 不同接口支持模型不同：`/chat/completions` 支持 `qwen-max`、`deepseek-v4` 等；`/responses` 仅限 `qwen3.*` 及指定型号；`/embeddings` 仅限 `text-embedding-*` 系列。 |
| `messages` | array | 对话输入，格式为 `[{"role": "...", "content": "..."}]` | 支持 `system`/`user`/`assistant` 角色；多模态内容可内嵌 `image_url` 或 Base64；`system` message 中可嵌入领域指令（如 `"Response in INTENT_MODE."`）。 |
| `stream` / `stream_options` | boolean / object | 控制流式响应 | `stream_options={"include_usage": true}` 可在流式结束块返回 token 统计；`/responses` 接口默认不返回 `output_text`，需访问 `response.output_text`。 |
| `previous_response_id` | string | 上一轮响应 ID | 仅 `/responses` 接口有效，值为响应顶层 `id`（UUID），有效期 7 天，用于自动续聊。 |
| `dimensions` | integer | 向量维度 | 仅 `text-embedding-v3/v4`、`qwen3-vl-embedding` 等特定模型支持，取值见各模型文档。 |
| `top_n` | integer | 返回前 N 个结果 | 仅 `/reranks` 接口使用，位于请求体顶层（`qwen3-rerank`）或 `parameters` 内（`qwen3-vl-rerank`）。 |

## 面向开发者，简洁实用

- ✅ **起步最快**：复制粘贴以下 Python 示例，替换 `{WorkspaceId}` 和 `DASHSCOPE_API_KEY` 即可运行：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  response = client.chat.completions.create(
      model="qwen3.8-max",
      messages=[{"role": "user", "content": "你好，用中文简要介绍通义千问"}]
  )
  print(response.choices[0].message.content)
  ```

- ✅ **调试建议**：  
  - 优先使用 `curl` 验证基础连通性（避免 SDK 版本兼容问题）；  
  - 查看响应中的 `x-request-id` 头，用于排查失败请求；  
  - 流式响应务必按 OpenAI 标准解析 `data:` 行，不要依赖 `finish_reason` 或 `usage` 字段（这些在兼容接口中可能缺失或不完整）。

- ❌ **避坑提醒**：  
  - 不要将 `max_tokens` 误写为 `max_output_tokens`（后者是 DashScope 原生参数）；  
  - 不要在 `extra_body` 中传递 `enable_thinking` 等关键开关——它必须是 JSONL 请求体顶层字段；  
  - [Token](token.md) Plan/Coding Plan 的 Key **仅限 CLI 工具和 OpenClaw 类 Agent 使用**，Dify、Postman、cURL 等通用工具接入会触发风控。  

- 📚 **延伸参考**：  
  - [Qwen API 参考](../../raw/model-api-reference/qwen-api-reference.md) —— 模型能力与参数细节  
  - [Toolkits and Frameworks](../../raw/model-api-reference/toolkits-and-frameworks.md) —— SDK 与框架适配指南  
  - [Vector and Sort](../../raw/model-api-reference/vector-and-sort.md) —— 向量与排序兼容接口详解

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [vector and sort](../api/vector-and-sort.md)
- [more models](../api/more-models.md)


