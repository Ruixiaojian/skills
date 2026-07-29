# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 REST API，严格遵循 OpenAI 官方 API 协议（如 `/v1/chat/completions`、`/v1/embeddings`、`/v1/images/generations` 等路径与请求/响应格式），使开发者无需修改客户端代码即可将现有基于 OpenAI 的应用无缝迁移到百炼平台，调用 Qwen 系列及其他支持模型。

## 在百炼平台的不同场景中，这个概念如何使用

OpenAI 兼容接口不是单一接口，而是一套覆盖多模态、多任务的协议族，在百炼中按能力维度统一部署于 `compatible-mode/v1` 路径下，适用于以下典型场景：

- **快速迁移已有应用**：使用标准 `openai` Python SDK、`curl` 或任何兼容 OpenAI 的 CLI/IDE 插件（如 Cursor、VS Code Copilot 扩展），只需替换 `base_url` 和 `API Key`，即可调用 `qwen-plus`、`qwen3.7-max`、`glm-5.2`、`deepseek-v4-pro` 等文本模型。
- **多模态理解**：通过 OpenAI Vision 协议（`messages` 中含 `image_url`）调用 `qwen3-vl-plus`、`qwen-vl-ocr`、`QVQ`，支持流式结构化输出；注意多模态 Embedding（如 `qwen3-vl-embedding`）**不兼容** OpenAI 接口，需专用 API。
- **向量嵌入服务**：调用 `/v1/embeddings` 接口使用 `text-embedding-v4`、`qwen3.7-text-embedding` 等模型，支持 `dimensions` 参数自定义向量维度；但 `qwen3-vl-embedding` 等多模态嵌入模型**不在此兼容范围内**。
- **文件驱动问答与分析**：结合 OpenAI 文件接口（`/v1/files` + `/v1/threads` + `/v1/runs`）上传 `.pdf`、`.docx`、图像等（单文件 ≤150 MB），再通过 `responses` 或 `chat/completions` 接口实现文档摘要、问答与数据提取。
- **批量异步处理**：使用 `/v1/batches`（文件批量）或 `/batch/chat/completions`（同步 Batch Chat）提交数千请求，费用为实时调用的 50%，适用于数据标注、批量评测等非实时场景。
- **对话状态管理**：通过 `conversations` 接口创建会话元数据，配合 `responses` 接口的 `previous_response_id` 自动注入历史上下文，实现跨设备、跨会话的上下文延续，无需手动拼接 `messages` 数组。

> ⚠️ 注意：`qwen-vl`、`qwen-audio`、`wanx`（文生图/视频）、`paraformer`（语音识别）等耗时型或多模态专用模型**均不支持 OpenAI 兼容接口**，必须使用 DashScope 原生 AIGC API。

## 关键参数和配置

| 参数 | 作用 | 必填 | 示例值 | 注意事项 |
|------|------|------|--------|----------|
| `base_url` | OpenAI 兼容接口根地址 | ✅ | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | **必须使用业务空间专属域名**（控制台获取 `{WorkspaceId}`），旧域名 `dashscope.aliyuncs.com` 即将停用；不同地域格式不同（如新加坡为 `ap-southeast-1`） |
| `model` | 模型标识符 | ✅ | `qwen3.7-plus`, `text-embedding-v4`, `qwen-coder-turbo` | 大小写敏感；`qwen-coder-turbo` 仅在 `/v1/completions` 有效；`qwen3.7-plus-2026-05-26` 等带时间戳变体需严格匹配 Responses API 文档列表 |
| `messages` | 对话历史（Chat 接口） | ✅（Chat） | `[{"role":"user","content":"你好"}]` | 不支持 `system` 角色（DashScope 原生支持）；`responses` 接口可省略此字段，由 `previous_response_id` 自动注入上下文 |
| `input` | 文本输入（Embedding/Completions） | ✅（Embedding/Completions） | `"hello"` 或 `["hello", "world"]` | Embedding 接口支持字符串、字符串数组、文件 URL（需 `X-DashScope-OssResourceResolve: enable`） |
| `temperature` / `top_p` | 输出多样性控制 | ❌ | `0.7`, `0.9` | 默认值同 OpenAI：`temperature=0.8`, `top_p=0.8`；思考模式（如 `qwen3.8-max-preview`）下 `temperature` 最低为 `0.6` |
| `max_tokens` | 输出长度上限 | ❌ | `2048` | OpenAI 兼容接口默认 `2048`（DashScope 原生默认 `1024`）；不返回细粒度 `prompt_tokens`/`completion_tokens` 统计 |
| `dimensions` | 向量维度（Embedding） | ❌ | `1024`, `2560` | 仅 `text-embedding-v4/v3`、`qwen3.7-text-embedding` 等支持；`v2` 及更早版本返回固定维度 |

## 面向开发者，简洁实用

- ✅ **即开即用**：安装 `openai==1.40.0+`，设置环境变量 `OPENAI_BASE_URL` 和 `OPENAI_API_KEY`，一行代码调用：
  ```python
  from openai import OpenAI
  client = OpenAI(base_url="https://your-workspace.cn-beijing.maas.aliyuncs.com/compatible-mode/v1", api_key="sk-xxx")
  response = client.chat.completions.create(model="qwen3.7-plus", messages=[{"role":"user","content":"你好"}])
  print(response.choices[0].message.content)
  ```

- ✅ **流式响应**：所有 Chat 接口支持 `stream=True`，解析 `delta.content` 字段（与 OpenAI 完全一致）；Vision 模型（如 QVQ）**强制流式**。

- ✅ **错误兼容**：HTTP 状态码（400/401/429/500）及错误结构（`error.message`, `error.code`）与 OpenAI 保持一致，便于统一错误处理。

- ❌ **不支持功能**：  
  - 工具调用（`tools`/`tool_choice`）需改用 DashScope 原生接口或客户端侧模拟；  
  - `logprobs`、`seed`、自定义 `stop` 字符串、`response_format`（JSON Schema）等高级参数仅 DashScope 原生支持；  
  - 多模态模型（VL/Audio）和异步任务（图像生成、长音频）**不可通过此协议调用**。

- 📌 **生产建议**：  
  - 优先使用业务空间专属 `base_url`，避免限流与延迟；  
  - 模型名务必查证 [Responses API 文档](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 中的精确列表；  
  - [Token](token.md) Plan/Coding Plan 用户**禁止**用于 Dify/n8n/Postman 生产调用，仅限按量计费 API Key 支持工作流平台。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more about models](../api/more-about-models.md)
- [vector and sort](../api/vector-and-sort.md)


