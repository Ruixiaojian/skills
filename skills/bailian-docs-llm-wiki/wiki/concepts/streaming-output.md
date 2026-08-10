# 流式输出

流式输出（Streaming Output）是指大模型服务将生成结果以增量方式、分块逐次返回给客户端，而非等待完整响应生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户感知的响应实时性，是构建对话式、交互式 AI 应用（如聊天界面、语音助手、实时翻译）的关键能力。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台中并非统一机制，而是根据接入协议和业务场景采用不同实现形式与语义约定：

- **DashScope 原生接口**（`/api/v1/services/aigc/text-generation/generation`）：  
  设置 `stream=true` 后，服务以 Server-Sent Events（SSE）格式返回多个 `data:` 事件块，每个块包含 `output.text` 字段——该字段为**当前增量片段（非全量）**，客户端需累积拼接获得完整输出。

- **OpenAI 兼容 Chat Completions 接口**（`/v1/chat/completions`）：  
  同样通过 `stream=true` 启用，但响应格式遵循 OpenAI 标准：每个 chunk 的 `choices[0].delta.content` 字段携带新增 token 文本；首次 chunk 可能为空（含 `role`），后续 chunk 逐字/逐词追加内容。

- **Knowledge 知识问答 API**（`/api/v1/indices/knowledge/answer`）：  
  `stream=true`（默认启用）时，同样采用 SSE 协议，返回结构化事件流，包含 `planning`、`tool_calling`、`generation` 三阶段的增量结果，便于前端分阶段渲染（如先显示“正在检索知识…”再逐步输出答案）。

- **Realtime API（WebSocket/AOQ/WebRTC）**：  
  流式为默认行为，无需显式开关。文本输出通过 `text.delta` 事件实时推送；音频输出则以二进制 PCM 数据帧持续下发（如 `audio.delta`）。所有 Realtime 模型均原生支持低延迟流式，适用于语音对话、实时转录等强实时场景。

- **Application（智能体/RAG 应用）调用**：  
  SDK 或控制台调用时设置 `stream=True`，底层自动适配对应模型接口的流式协议；若启用 `incremental_output=True`（仅 DashScope 原生支持），可确保每次返回严格为新增内容，避免重复或重传。

> ⚠️ 注意：流式能力**不跨协议互通**。例如 [OpenAI 兼容接口](openai-compatible-interface.md)不支持 DashScope 特有的 `incremental_output`，Knowledge API 不支持 OpenAI 的 `delta` 结构；客户端必须按所选接口文档解析对应格式。

## 关键参数和配置

| 参数 | 类型 | 作用 | 支持接口 | 备注 |
|------|------|------|----------|------|
| `stream` | boolean | 启用/禁用流式响应 | 所有主流接口（DashScope、OpenAI 兼容、Knowledge、Application SDK） | 默认 `false`（除 Knowledge 问答接口默认 `true`） |
| `incremental_output` | boolean | 强制每次返回仅含新增文本（非全量重传） | 仅 DashScope 原生接口 | 需配合 `stream=true` 使用；提升前端处理效率，避免重复渲染 |
| `enable_search` / `tools` | object | 在流式过程中动态触发联网搜索或工具调用 | DashScope（Qwen-Max/Plus）、Omni-Realtime（qwen3.5 系列）、Knowledge | 工具调用结果也以流式事件返回，需监听 `tool_calls` 相关事件 |

- **连接与超时**：  
  - SSE 流式请求默认超时为 **60 秒**（Knowledge、DashScope），超时后连接关闭，需客户端主动重试；  
  - WebSocket/Realtime 连接由长连接维持，无固定单次超时，但空闲超时（如 `idle_timeout_ms`）需按模型文档配置。

- **错误处理**：  
  流式响应中若发生错误（如鉴权失败、模型不可用），服务会在最后发送一个含 `error` 字段的事件块（SSE）或 `error` 类型事件（WebSocket），**不会中断连接立即返回 HTTP 错误码**；客户端须监听并终止流处理。

## 面向开发者：简洁实用建议

- ✅ **必做**：始终检查 `stream` 参数是否生效，并按对应接口文档解析事件格式（勿混用 OpenAI 和 DashScope 的 delta 解析逻辑）；  
- ✅ **推荐**：前端使用 `TextEncoder` + `ReadableStream`（浏览器）或 `EventSource`（SSE）原生 API 处理流，避免手动拼接字符串引发编码问题；  
- ✅ **注意**：流式输出的 token 边界 ≠ 字符边界（尤其含 emoji、中文、标点时），`content` 字段可能截断在 UTF-8 多字节中间，需确保解码器支持流式 UTF-8；  
- ✅ **调试技巧**：开启 `stream=false` 对比全量响应，验证流式拼接结果是否一致；利用 `RequestId` 提交工单时务必附带完整流式事件日志；  
- ❌ **避免**：在流式过程中反复修改 `messages` 或重发请求——流式会话状态由服务端维护，客户端应保持单次请求生命周期。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [knowledge](../api/knowledge.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application support](../guides/application-support.md)


