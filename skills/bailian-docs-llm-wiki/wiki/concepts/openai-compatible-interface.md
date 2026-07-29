# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 REST API，严格遵循 OpenAI 的请求/响应协议（如 `/v1/chat/completions`），使开发者能复用现有 OpenAI SDK、工具链和代码逻辑，零改造接入千问（Qwen）及第三方大模型。该接口不改变 OpenAI 的核心语义（如 `messages` 结构、`stream` 行为、错误码格式），但底层由百炼统一调度与计费。

## 在百炼平台的不同场景中如何使用

- **快速迁移已有应用**：若项目已使用 `openai` Python SDK 或 LangChain 的 OpenAI LLM 封装，只需替换 `base_url` 和 `api_key`，即可直接调用 `qwen3.7-plus`、`qwen-max` 等模型，无需重写业务逻辑。
- **构建智能助手（Responses API）**：选用 `/v1/responses` 路径的 OpenAI 兼容变体，可开箱启用联网搜索、代码解释器、网页提取等内置工具，自动维护对话状态，适合客服、Agent 类场景。
- **多模态与嵌入任务**：Vision 接口（`/v1/chat/completions` + `qwen3-vl-plus`）支持图像 URL/Base64 输入；Embedding 接口（`/v1/embeddings`）兼容 `text-embedding-v1`~`v4`，但多模态 Embedding（如 `qwen3-vl-embedding`）不支持此协议。
- **批量与异步处理**：通过 `/v1/batch`（同步 Batch Chat）或 `/v1/batch/jobs`（异步 JSONL 批量）复用 OpenAI Batch 代码，仅需切换 `base_url` 即可。
- **会话管理集成**：配合 `/v1/conversations` 接口，可创建、查询、追加消息，实现跨设备上下文持久化，与 Responses API 协同提升长周期交互体验。

> ⚠️ 注意：`qwen-vl`、`qwen-audio`、`qwen-ocr` 等多模态模型，以及 `qwen3-coder-next`（代码专用）等部分模型，**仅支持 DashScope 原生接口，不提供 OpenAI 兼容路径**。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `base_url` | string | 是 | **必须匹配地域与计费方案**：<br>• 生产推荐：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`（如北京：`https://abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）<br>• 兼容保留：`https://dashscope.aliyuncs.com/v1`（仅限试用/调试）<br>• [Token](token.md) Plan/Coding Plan 用户需使用专属域名（如 `token-plan.cn-beijing.maas.aliyuncs.com`） |
| `model` | string | 是 | 模型 ID，**严格区分大小写与版本后缀**：<br>• 文本生成：`qwen3.7-plus`、`qwen-max`、`deepseek-v4-pro`<br>• Vision：`qwen3-vl-plus`、`qwen-ocr`<br>• Embedding：`text-embedding-v4`<br>• 不支持：`qwen-audio`、`qwen-vl`（多模态原生模型）、`qwen-coder-turbo`（仅 Completions 接口） |
| `messages` | array | 是 | 标准 OpenAI 格式：`[{"role": "user", "content": "..." }, ...]`<br>• **不支持 `system` 角色**（会被忽略），请将系统提示合并到首条 `user` 消息中<br>• Vision 场景下 `content` 可为数组：`[{ "type": "text", "text": "..." }, { "type": "image_url", "image_url": { "url": "..." } }]` |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 SSE 流式响应，每帧含 `delta.content` 字段 |
| `stream_options` | object | 否 | 仅流式启用时有效：<br>`{"include_usage": true}` → 在流末尾返回 `usage` 统计（`prompt_tokens`, `completion_tokens`） |
| `temperature` / `top_p` | number | 否 | 控制输出随机性，取值范围 `0.0–1.0`；二者互斥使用效果更佳 |

## 面向开发者：简洁实用指南

✅ **推荐做法**  
- 使用 `openai` SDK（v1.0+）调用：  
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  response = client.chat.completions.create(
      model="qwen3.7-plus",
      messages=[{"role": "user", "content": "你好"}],
      stream=True
  )
  ```

✅ **避坑提醒**  
- ❌ 不要混用 Key 与 Base URL：[Token](token.md) Plan Key 只能配 [Token](token.md) Plan 域名；按量计费 Key 必须配 `{WorkspaceId}` 域名。  
- ❌ 不要传 `system` 消息——它会被静默丢弃，请改用 `user` + 提示词前置。  
- ❌ 不要对 `qwen-vl` 或 `qwen-audio` 使用 `/v1/chat/completions`——会返回 `404` 或 `400`。  
- ✅ 流式解析时，注意 OpenAI 兼容接口返回 `delta.content`（非 `output.text`），结尾帧含 `finish_reason`。  

✅ **调试技巧**  
- 查看响应头 `X-DashScope-Request-ID`，用于问题定位与工单提报；  
- 本地验证可用 `curl` + DashScope 域名（仅限试用 Key），生产务必切至 Workspace 域名；  
- 所有 OpenAI 兼容接口均按 `(input_tokens + output_tokens)` 计费，含工具调用返回内容。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [get started with models](../guides/get-started-with-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [model deployment 1](../guides/model-deployment-1.md)


