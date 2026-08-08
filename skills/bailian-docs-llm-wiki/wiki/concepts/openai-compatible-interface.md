# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 REST API，严格遵循 OpenAI 的请求/响应协议（如 `/v1/chat/completions`），使开发者无需修改现有代码即可将应用从 OpenAI 迁移至百炼，或在多模型平台间快速切换。该接口并非简单协议映射，而是针对 Qwen 系列及第三方模型进行了能力适配与行为对齐，覆盖文本生成、视觉理解、嵌入向量、批量推理等核心场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移已有应用**：若您的项目已基于 OpenAI SDK（如 `openai>=1.0`）开发，只需替换 `base_url` 和 `api_key`，即可直接调用 `qwen-plus`、`qwen3.8-max`、`deepseek-v4-flash` 等模型，零代码改造完成接入。
  
- **轻量级智能体构建**：选用 **OpenAI 兼容 Responses API**（Endpoint: `/compatible-mode/v1/responses`），自动启用联网搜索、网页抓取、代码解释器等内置工具能力，并支持通过 `previous_response_id` 维护多轮对话状态，适合构建无需自研状态管理的助手类应用。

- **多模态与专业场景适配**：
  - 视觉任务：使用 **Vision 接口**（`/compatible-mode/v1/chat/completions` + `model=qwen-vl-plus`），支持图像输入与结构化输出，`QVQ` 模型仅支持流式响应；
  - 向量检索：调用 **Embedding 接口**（`/compatible-mode/v1/embeddings`），兼容 `text-embedding-v1` 至 `v4`，但多模态 Embedding 模型（如 `qwen3-vl-embedding`）不在此列；
  - 批处理：通过 **Batch 接口**（`https://batch.dashscope.aliyuncs.com/compatible-mode/v1/batches`）提交文件或文本列表，单次支持最高 256K tokens（部分模型如 `qwen3.8-max`），注意 endpoint 与 Chat 接口不同。

- **开发工具集成**：Cursor、Cherry Studio、Cline 等 IDE 工具原生支持 OpenAI 协议，配置 `Base URL = https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` 及对应 API Key 后，即可在编辑器内直接调用百炼模型，无需额外插件。

> ⚠️ 注意：OpenAI 兼容接口**不支持工具调用原生语义**（如 `tools` 参数触发函数执行），需依赖 Responses API 或 DashScope 原生接口实现；Qwen-Audio、图像/视频生成类模型（如 `wan2.6-t2i`）也不支持该协议，须使用专用异步 API。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `base_url` | string | 是 | 接口根地址，**必须匹配计费方案与地域**：<br>- [Token](token.md)/Coding Plan：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>- 按量计费（子空间）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://myworkspace.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `model` | string | 是 | 模型 ID，**严格区分大小写且需与接口类型匹配**：<br>- Chat Completions：`qwen3.8-max`, `qwen-vl-plus`, `glm-5.2`<br>- Vision：仅 `qwen-vl-plus`, `qwen-ocr`<br>- Embedding：仅 `text-embedding-v1`~`v4` | `"qwen3.8-max"` |
| `messages` | array | 是（多轮） | 对话消息数组，格式为 `[{"role":"user","content":"..."}]`；流式场景下**必须显式传入全量上下文**，不能依赖服务端自动维护历史 | `[{"role":"user","content":"你好"}]` |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；设为 `true` 时返回 SSE 流，支持 `stream_options={"include_usage": true}` 获取 token 统计 | `true` |
| `previous_response_id` | string | 否（仅 Responses API） | 上一轮响应的顶层 `id`（UUID 格式），用于自动关联对话上下文；**不可使用 `output` 中消息的 `id`** | `"resp_abc123..."` |
| `temperature` / `top_p` | number | 否 | 控制输出随机性（0.0–2.0），默认 `1.0`；`top_p` 默认 `1.0`，二者可共存，但 `top_k` 等细粒度参数仅 DashScope 原生接口支持 | `0.7` |

- **认证方式**：所有请求必须在 `Authorization` Header 中携带 `Bearer <api_key>`，API Key 与 `base_url` 方案严格绑定（[Token](token.md) Plan Key 不可用于按量计费环境）。
- **Endpoint 差异**：不同能力对应不同路径，例如：
  - Chat：`{base_url}/chat/completions`
  - Responses：`{base_url}/responses`
  - Embedding：`{base_url}/embeddings`
  - Batch：`https://batch.dashscope.aliyuncs.com/compatible-mode/v1/batches`

## 面向开发者，简洁实用

- ✅ **推荐做法**：优先使用 DashScope SDK（如 `dashscope==1.29.0+`），它自动处理 `base_url` 构造、重试、流式解析和错误码映射，比裸 HTTP 更稳定。
- ✅ **调试技巧**：开启 `stream=true` 时，务必检查响应头 `Content-Type: text/event-stream`；若返回 JSON 而非 SSE 流，大概率是 `base_url` 或 `model` 配置错误。
- ❌ **避坑提示**：
  - 不要混用 `compatible-mode/v1` 与 `/apps/anthropic` 路径；
  - `qwen-turbo` 在 OpenAI 兼容接口中最大上下文为 8192 tokens，超限返回 `400 Bad Request`；
  - Responses API 的联网能力（`enable_search`）默认开启，无需额外参数；
  - 子业务空间部署的模型**不支持 OpenAI 兼容接口**，仅限 DashScope 原生调用。

如需完整功能（如工具调用、异步任务、细粒度日志），请切换至 DashScope 原生接口；如需跨模型会话持久化，请结合百炼 Agent 编排服务或自行实现外部缓存。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more about models](../api/more-about-models.md)


