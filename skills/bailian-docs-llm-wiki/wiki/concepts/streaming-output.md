# 流式输出

流式输出（Streaming Output）是百炼平台中一种实时、增量式返回模型响应的通信机制，客户端无需等待整个响应生成完成即可逐段接收并处理结果，显著降低端到端延迟，提升交互实时性与用户体验。

## 在百炼平台的不同场景中如何使用

流式输出在以下三类核心能力中被统一支持，但协议形式与使用方式略有差异：

- **知识问答（`/api/v2/apps/knowledge/chat`）**：默认启用流式，采用 Server-Sent Events（SSE）协议。服务端按 `event: planning` / `event: tool_call` / `event: generation` 分阶段推送 JSON 数据块，每行以 `data: {...}` 格式发送，客户端需按事件类型解析并组装最终答案。

- **应用调用（Application Call）**：通过 `stream=true` 参数启用（仅同步调用有效），支持 DashScope API 和 Responses（OpenAI 兼容）接口。响应为 SSE 流，包含 `choices[0].delta.content` 字段的增量文本片段，适用于聊天机器人等实时对话场景。

- **Realtime API（Omni 及通用 Realtime）**：基于 WebSocket 或 AOQ 协议，采用事件驱动模型。服务端主动推送 `response.text.delta`、`response.audio.delta` 等细粒度事件，支持文本+音频混合流式输出，适用于语音助手、实时翻译等低延迟交互场景。

> ⚠️ 注意：异步调用（`background=true`）不支持流式输出；所有流式响应均无 `job_id` 或轮询机制，必须通过长连接持续接收。

## 关键参数和配置

| 参数 | 位置 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `stream` | 请求体（JSON）或 Query 参数 | `boolean` | `true`（知识问答）、`false`（应用调用） | 控制是否启用流式；设为 `false` 时返回完整 JSON 响应（非流式）。 |
| `event` 字段 | SSE 响应头 | `string` | 如 `planning`、`generation`、`text.delta` | 标识当前数据块语义阶段，客户端需据此做差异化处理。 |
| `data:` 前缀 | SSE 响应体 | `string` | 必须存在 | 每行以 `data: {...}` 开头，空行分隔事件；需严格按 SSE 规范解析。 |
| `modalities` | Realtime API 的 `session.update` | `string[]` | `["text","audio"]` | 决定流式输出模态组合，影响事件类型（如是否含 `response.audio.delta`）。 |

> ✅ 最佳实践：  
> - 客户端务必设置足够长的连接超时（建议 ≥ 300s），避免因网络波动中断流；  
> - 解析 SSE 时需忽略空行、跳过注释行（以 `:` 开头），并正确处理换行符 `\n` 或 `\r\n`；  
> - 对于 Realtime API，需监听 `response.done` 事件作为流结束信号，而非依赖连接关闭。

## 面向开发者提示

- 不要自行拼接 `data:` 行——使用标准 SSE 解析库（如 `EventSource` 浏览器原生 API、`sseclient` Python 库）；
- 流式响应中 `content` 字段可能为空字符串（如工具调用阶段），请判空处理；
- 所有流式接口均不透传 LLM 控制参数（如 `temperature`、`max_tokens`）至知识问答接口，该限制已在文档中明确；
- 若需调试，可临时禁用流式（`stream=false`）获取完整响应结构，再切换回流式实现渐进渲染。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application call](../api/application-call.md)


