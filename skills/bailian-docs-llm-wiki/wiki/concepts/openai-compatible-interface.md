# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 API 协议实现，严格遵循 OpenAI REST API 的路径、请求/响应格式、参数命名与错误规范（如 `/v1/chat/completions`），使开发者能复用现有 OpenAI SDK（如 `openai>=1.0`）和代码逻辑，无需重写业务逻辑即可快速接入千问（Qwen）及第三方大模型。

## 在百炼平台的不同场景中如何使用

- **快速迁移已有项目**：只需将 `openai` SDK 的 `base_url` 指向百炼的兼容端点（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并替换 `model` 为百炼支持的模型 ID（如 `qwen3.7-plus`），即可零代码修改完成迁移。  
- **多模态任务**：通过 `chat/completions` 接口调用 `qwen3-vl-plus` 等视觉模型，支持 `image_url` 或 base64 图像输入，格式与 OpenAI Vision API 完全一致。  
- **向量检索**：使用 `/v1/embeddings` 接口调用 `text-embedding-v4` 等嵌入模型，支持批量文本、`dimensions` 调整与 `encoding_format="float"`，与 OpenAI Embedding API 行为一致。  
- **文件与批量处理**：通过 `/v1/files` 和 `/v1/batch` 接口上传文档、提交 JSONL 批量任务，适用于 RAG 文档解析、离线推理等非实时场景。  
- **会话状态管理**：结合 `/v1/conversations`（创建/查询会话）与 `/v1/responses`（自动维护上下文的增强版 chat/completions），实现跨设备、跨请求的对话延续，无需自行维护 `messages` 历史。  
- **轻量级工具增强**：`responses` 接口内置联网搜索、代码解释器、网页提取能力，仅需传入 `previous_response_id` 即可自动关联上下文，适合聊天机器人、Copilot 类应用。

> ⚠️ 注意：OpenAI 兼容接口**不支持** `qwen-audio`、`qwen-omni`、`qwen-vl`（部分旧版）、多模态 embedding（如 `qwen3-vl-embedding`）及 `gte-rerank` 等模型；工具调用需显式启用（见下文参数说明），且不支持流式工具调用响应解析。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例值 |
|------|------|------|------|--------|
| `base_url` | string | 是 | **必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名 `dashscope.aliyuncs.com` 已逐步停用 | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `model` | string | 是 | 模型 ID，**必须严格匹配控制台可用列表**；推荐使用带版本号的命名（如 `qwen3.7-plus`），避免 `qwen-plus` 等旧别名 | `"qwen3.7-plus"`, `"text-embedding-v4"`, `"qwen3-vl-plus"` |
| `messages` | array | 是（chat/completions） | 标准 OpenAI 消息数组，`role` 仅支持 `"user"`/`"assistant"`/`"system"`；`content` 支持字符串或 `{ "type": "image_url", "image_url": { "url": "..." } }`（Vision） | `[{"role":"user","content":"你好"}]` |
| `tools` / `tool_choice` | array / string | 否 | 启用工具调用：传 `tools` 定义工具列表，并设 `tool_choice="auto"` 或 `{"type":"function","function":{"name":"xxx"}}` | `[{ "type": "function", "function": { "name": "search_web", ... } }]` |
| `stream` | boolean | 否 | 启用流式响应（SSE），返回 `data: {...}` 分块；所有 chat/completions 接口均支持 | `true` |
| `previous_response_id` | string | 否（仅 `responses` 接口） | 用于自动上下文续写，**必须传上一轮响应的顶层 `id` 字段（UUID 格式）**，非 `choices[0].message.id` | `"resp_abc123-def456..."` |
| `dimensions` | integer | 否（embeddings） | 指定输出向量维度（仅部分 embedding 模型支持） | `1024` |

## 面向开发者：简洁实用提示

- ✅ **首选 SDK**：直接使用官方 `openai` Python/Node.js SDK，设置 `api_key` 和 `base_url` 即可，无需引入额外依赖。  
- ✅ **调试技巧**：开启 `logging` 或捕获 `APIResponse` 原始 body，检查 `x-request-id` 头用于问题追踪；错误码统一遵循 RFC 7807，优先解析 `error.code`（如 `invalid_model`、`rate_limit_exceeded`）。  
- ✅ **地域与计费隔离**：API Key、`base_url`、模型 ID 必须同属一个地域（如华北2）和计费方案（Token Plan / 按量），混用将返回 `401 Unauthorized` 或 `404 Not Found`。  
- ❌ **避坑提醒**：  
  - 不要硬编码 `model` 名称——从控制台「模型广场」或 [DashScope 文档](https://help.aliyun.com/zh/dashscope/developer-reference/quick-start) 获取实时支持列表；  
  - `qwen-turbo`、`qwen2.5` 系列模型在 OpenAI 兼容接口中**可能受限或不支持**，请以实际调用返回为准；  
  - 流式响应中 `delta.content` 可能为空（工具调用阶段），需监听 `delta.tool_calls` 字段解析[函数调用](function-calling.md)。  

> 📌 最小可行示例（Python）：
> ```python
> from openai import OpenAI
> client = OpenAI(
>     api_key=os.getenv("DASHSCOPE_API_KEY"),
>     base_url="https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
> )
> resp = client.chat.completions.create(
>     model="qwen3.7-plus",
>     messages=[{"role": "user", "content": "用 Python 写一个快速排序"}],
>     stream=True
> )
> for chunk in resp:
>     if chunk.choices[0].delta.content:
>         print(chunk.choices[0].delta.content, end="")
> ```

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [get started with models](../guides/get-started-with-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [vector and sort](../api/vector-and-sort.md)


