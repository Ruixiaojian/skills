# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，将结果分块、增量地通过网络持续返回给客户端，而非等待全部内容生成完毕后一次性返回完整响应。这种方式显著降低端到端延迟，支持实时渲染、中断控制与弱网友好交互，是百炼平台面向语音助手、智能客服、RAG问答等低延迟场景的核心能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **知识问答（`/api/v2/apps/knowledge/chat`）**：启用 `stream=true` 后，服务端通过 Server-Sent Events（SSE）按阶段推送事件，包括 `planning`（查询规划）、`retrieving`（知识检索）、`generating`（答案生成），每阶段可含多个增量文本块，客户端可逐段渲染并支持中途取消请求。

- **Realtime API（Omni / Qwen-Audio 等）**：基于 WebSocket 或 AOQ 协议，以事件流形式推送 `response.text.delta`（文本增量）、`response.audio.delta`（PCM 音频增量），实现毫秒级语音合成与文本同步输出；VAD 触发、工具调用、联网搜索等过程均与流式生成无缝融合。

- **Qwen 文本生成（DashScope 原生接口）**：设置 `stream=true` 时，响应为 SSE 流，每个 `data:` 行包含一个 JSON 对象，字段为 `output.text`（当前增量文本）和 `usage`（已消耗 token 数），适用于长文本生成与前端渐进式展示。

- **应用调用（`/api/v1/apps/{APP_ID}/completion`）**：仅同步调用支持流式，需在工作流应用的结束节点显式开启“流式输出”开关并重新发布；启用后返回 SSE 流，内容结构与 DashScope 文本生成一致，但不支持异步调用模式下的流式。

- **[OpenAI 兼容接口](openai-compatible-interface.md)（Chat Completions）**：虽兼容 OpenAI 协议，但默认 `stream=false`；需显式传入 `"stream": true`，响应格式遵循 OpenAI 标准（`delta.content` 字段），解析逻辑需与 DashScope 原生流区分。

> ⚠️ 注意：所有流式接口均要求客户端正确处理连接中断、重连、事件解析与字符编码（UTF-8），且不可假设事件顺序或跳过中间块——例如知识问答中缺失 `retrieving` 事件可能导致答案缺乏依据。

## 关键参数和配置

| 参数 | 位置 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `stream` | 请求体（JSON）或 Query 参数 | `boolean` | 因接口而异：<br>• Knowledge API：`true`<br>• Qwen DashScope：`true`<br>• OpenAI 兼容：`false`<br>• Application Call：`false` | 全局开关，启用后服务端返回流式响应（SSE 或 WebSocket event stream） |
| `modalities` | `session.update` 事件（Realtime API） | `string[]` | `["text", "audio"]` | 控制输出模态组合；流式输出仅对启用的模态生效（如设为 `["text"]` 则无音频 delta） |
| `incremental_output` | Qwen DashScope `parameters` | `boolean` | `true`（当 `stream=true` 时自动生效） | 低层控制是否启用 token 级增量生成（通常无需手动设置） |
| `enable_search` / `tools` | Realtime 或 Qwen 接口的会话/请求参数 | `boolean` / `array` | 按模型支持而定 | 这些能力本身不改变流式机制，但会扩展流式事件类型（如 `response.tool_calls.delta`） |

- **协议适配要点**：
  - SSE 接口（Knowledge、Qwen DashScope、Application Call）：响应头含 `Content-Type: text/event-stream`，需按行解析 `event:`、`data:`、`id:` 字段；
  - WebSocket/AOQ 接口（Realtime API）：无固定 MIME 类型，所有消息为 JSON event object，需监听 `response.text.delta`、`response.audio.delta` 等指定 `type` 字段；
  - [OpenAI 兼容接口](openai-compatible-interface.md)：响应格式为 `data: {...}\n\n`，`delta.content` 为字符串增量，注意空 content 表示结束。

## 面向开发者，简洁实用

- ✅ **必做**：始终设置超时（建议 `timeout=60s`），监听 `close`/`error` 事件并实现重试（指数退避）；
- ✅ **推荐**：前端使用 `ReadableStream`（浏览器）或 `EventSource`（SSE）原生 API；服务端推荐 `aiohttp`（Python）或 `fetch-event-source`（Node.js）等成熟流式客户端库；
- ✅ **调试技巧**：用 `curl -N` 查看原始 SSE 流；Realtime API 可通过 `session.update` 设置 `debug: true` 获取内部 trace 事件；
- ❌ **避免**：将流式响应拼接后统一处理——应边收边渲染，利用 `response.text.delta` 实现打字机效果，`response.audio.delta` 直接喂入 Web Audio API；
- 📌 **计费提示**：流式不影响计费逻辑——仍按实际生成的 `output_tokens` 计费，与是否流式无关。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)


