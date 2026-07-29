# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在生成过程中持续、分块地向客户端推送结果，而非等待整个响应完成后再一次性返回。它显著降低端到端延迟，提升用户交互体验，并支持对生成过程的细粒度控制与可视化（如打字机效果、中间状态反馈）。

## 在百炼平台的不同场景中如何使用

流式输出已在多个核心能力中统一支持，但具体行为和协议略有差异：

- **知识问答（`/apps/knowledge/chat`）**：采用 Server-Sent Events（SSE）协议，响应按语义阶段分块推送，包括 `plan`（查询拆解）、`tool_call`（检索/工具调用）、`answer`（最终回答）三类事件，每条事件以 `data:` 行格式传输，需按 SSE 标准解析。

- **Qwen 文本生成（DashScope 原生 / [OpenAI 兼容接口](openai-compatible-api.md)）**：  
  - DashScope 原生接口返回 `output.text` 字段的增量片段；  
  - [OpenAI 兼容接口](openai-compatible-api.md)（`/chat/completions`）返回 `delta.content` 字段，遵循 OpenAI Streaming 格式；  
  - 注意：[OpenAI 兼容接口](openai-compatible-api.md)**不返回** `usage` 细粒度统计，完整 token 计数仅 DashScope 接口提供。

- **应用调用（`/apps/{app_id}/completion` 或 Responses API）**：  
  - 同步调用支持 `stream=true`，适用于智能体、工作流等应用；  
  - 工作流需在结束节点显式启用“流式开关”才生效；  
  - 异步调用（`background=true`）**不支持** `stream` 参数，设置将被忽略。

- **Realtime API（WebSocket / AOQ / WebRTC）**：  
  - 所有协议均原生支持流式，服务端通过结构化事件（如 `conversation.item.output.text.delta`）实时推送文本片段或音频 chunk；  
  - 音频流固定为 24 kHz PCM，文本流默认为增量式（即每次仅返回新生成 token，非全量重发）。

- **RAG 与插件集成场景**：  
  - 当 `stream=True` 且 `incremental_output=True` 时，启用**增量式流式输出**——每个响应块仅包含本次新增内容，避免重复传输已发送文本，大幅减少带宽消耗与前端处理开销。

## 关键参数和配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `stream` | boolean | `false`（多数接口）<br>`true`（`/knowledge/chat`） | 启用流式响应。必须设为 `true` 才能接收分块数据。 |
| `incremental_output` | boolean | `false` | **仅当 `stream=true` 时生效**。启用后，每帧响应仅含新增 token（如 `"你好"` → `"世界"`），而非全量重发（`"你好世界"`）。推荐生产环境开启。 |
| `modalities`（Realtime API） | array | `["text", "audio"]` | 控制输出模态组合；流式行为因模态而异：文本流为字符级增量，音频流为 PCM chunk 级推送。 |

> ⚠️ 注意事项：  
> - `stream` 参数在异步调用、部分旧版接口或未明确声明支持的 endpoint 中可能被忽略；请以各接口文档为准。  
> - OpenAI 兼容接口与 DashScope 原生接口的响应字段名不同（`delta.content` vs `output.text`），解析逻辑需区分。  
> - SSE 接口（如 [knowledge](../api/knowledge.md) `/chat`）需正确处理 `event:`、`data:`、`id:` 等字段，建议使用标准 SSE 客户端库（如 `EventSource`）。

## 面向开发者：简洁实用建议

- ✅ **必做**：检查目标接口是否支持流式（参见各 API 文档的「支持的模型/功能」章节），并显式传入 `"stream": true`。  
- ✅ **推荐**：始终搭配 `incremental_output=true` 使用，尤其在长文本生成或高并发场景下可显著降低网络与前端渲染压力。  
- ✅ **解析要点**：  
  - SSE：监听 `message` 事件，按行分割，提取 `data:` 后内容并 `JSON.parse()`；  
  - OpenAI 兼容：过滤 `choices[0].delta.content` 非空字符串；  
  - DashScope 原生：读取 `output.text` 字段；  
  - Realtime API：监听 `conversation.item.output.text.delta` 事件。  
- ❌ **避免**：在流式响应未结束前关闭连接；未设置超时或重连机制；在浏览器中直接 `console.log` 大量流式数据导致卡顿。  
- 🛠️ **调试提示**：使用 `curl -N` 或 Postman 的 SSE 支持模式验证流式行为；SDK 调用时优先选用最新版 `dashscope` Python SDK（v1.20.0+），其 `Application.call(..., stream=True)` 自动处理增量解析。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application support](../guides/application-support.md)


