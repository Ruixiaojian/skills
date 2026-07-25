# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组遵循 OpenAI REST API 规范（如 `chat/completions`、`embeddings`、`vision` 等）的标准化模型调用入口，允许开发者复用现有 OpenAI SDK、LangChain 集成或工具链（如 Cursor、Dify、Postman），仅需替换 `base_url` 和 `model` 即可快速迁移，无需重写业务逻辑。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移已有项目**：当您已基于 OpenAI SDK（如 `openai==1.0+`）开发了应用，只需将 `client = OpenAI(api_key="...", base_url="https://api.openai.com/v1")` 中的 `base_url` 替换为百炼的兼容地址（如 `https://dashscope.aliyuncs.com/v1` 或地域专属域名），并把 `gpt-4o` 改为 `qwen-max` 等百炼模型名，即可直接运行。
- **多模态统一接入**：支持 Vision（图像理解）、Embedding（向量生成）、Completions（代码补全）、Files（文件管理）、Batch Chat（批量推理）等子接口，各功能复用同一套认证与流式机制，降低客户端适配复杂度。
- **智能体能力增强**：`OpenAI 兼容-Responses` 是专为轻量级智能体设计的增强型接口，内置联网搜索、网页抓取、代码解释器等工具链，自动维护对话上下文，适合构建无需自研调度逻辑的 AI 助手。
- **开发工具即插即用**：终端工具（Hermes Agent）、IDE 插件（Qoder、Cline）、低代码平台（Dify、OpenClaw）均原生支持该协议，配置 `Base URL + API Key + Model ID` 后即可调用百炼全部标准模型（如 `qwen3.8-max-preview`、`qwen-vl-plus`、`text-embedding-v3`）。
- **应用层集成**：通过 `application call` 的 OpenAI 兼容模式，可将已发布的智能体或工作流作为“黑盒模型”调用，输入格式与 `chat/completions` 完全一致（`messages` 数组），实现模型能力与业务流程的解耦。

> ⚠️ 注意：调优部署的私有模型、子业务空间内的专属模型**不支持 OpenAI 兼容接口**，必须使用 DashScope 原生接口调用。

## 关键参数和配置

| 参数 | 说明 | 示例值 | 注意事项 |
|------|------|--------|----------|
| `base_url` | 必填。服务端点地址，决定协议版本、计费归属与地域路由 | `https://dashscope.aliyuncs.com/v1`（通用）<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（推荐生产用） | 旧域名 `.../compatible-mode/v1` 已逐步淘汰；Batch Chat 固定使用 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1` |
| `model` | 必填。模型标识符，需与所选接口支持范围匹配 | `qwen-max`, `qwen3.7-plus`, `text-embedding-v3`, `qwen3-vl-plus` | 命名需带前缀（如 `qwen-`），`qwen-coder-turbo` 仅支持 `completions` 接口，`qwen3-vl-plus` 在 `chat/completions` 和 `vision` 接口中均可使用 |
| `stream` | 可选。启用流式响应 | `true` | 默认 `false`；Vision 接口的 `qvq` 模型**仅支持流式**；流式响应格式为 `text/event-stream` |
| `stream_options` | 可选。控制流式行为 | `{"include_usage": true}` | 设置后，最后一 chunk 将包含 `usage` 字段（含 `prompt_tokens`、`completion_tokens`） |
| `previous_response_id` | 仅 Responses API 必填（多轮对话） | `"resp_abc123"` | 必须传入上一轮响应的顶层 `id`（非 `output.message.id`），用于上下文自动注入 |
| `enable_thinking` | 可选。对支持思考模式的模型（如 `qwen3.8-max-preview`）显式启用 | `true` | OpenAI 兼容接口中需置于 `extra_body` 内；`qwen3.8-max-preview` 强制开启且不可关闭 |
| `dimensions` | 仅 Embedding 接口可选 | `256` | `text-embedding-v3`/`v4` 支持，指定输出向量维度；多模态 embedding（如 `qwen3-vl-embedding`）**不支持**该接口 |

## 面向开发者，简洁实用

- ✅ **认证方式统一**：使用阿里云 AccessKey（`AccessKeyId` + `AccessKeySecret`），通过 HTTP Header `Authorization: Bearer <DASHSCOPE_API_KEY>` 传递（注意：不是 OpenAI 的 `sk-xxx` 格式）。
- ✅ **错误处理一致**：返回标准 OpenAI 错误结构（`{ "error": { "message": "...", "type": "invalid_request_error", "code": "model_not_found" } }`），便于 SDK 自动解析。
- ✅ **流式兼容性好**：支持 `SSE`（Server-Sent Events），每条 `data:` 行为一个 JSON chunk，末尾含 `data: [DONE]`；可用 `openai` Python SDK 原生消费。
- ✅ **调试友好**：所有接口均在响应 `usage` 字段中返回精确 token 统计（`prompt_tokens`、`completion_tokens`），部分支持 `prompt_tokens_details`（需确认模型是否启用）。
- ❌ **不支持的功能**：`functions` / `tools` 参数（工具调用需用 Responses API 或 DashScope 原生 `tool_choice`）、跨请求 session 状态共享（需客户端自行维护 `messages` 数组）、私有调优模型调用。

> 💡 提示：生产环境请优先使用**地域专属域名**（如 `https://your-workspace-id.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），性能更稳定；调试时可用通用域名快速验证。所有 OpenAI 兼容接口均按百炼统一配额与计费规则执行，与模型实际调用量挂钩。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more about models](../api/more-about-models.md)
- [application call](../api/application-call.md)


