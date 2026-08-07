# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，将结果以增量、分块的方式实时推送至客户端，而非等待整个响应完成后再一次性返回。这种方式显著降低端到端延迟，提升用户体验，尤其适用于对话交互、长文本生成、语音合成等对实时性敏感的场景。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台多个核心能力中统一支持，但协议格式、触发方式和适用范围略有差异：

- **Qwen 文本生成 API**（OpenAI/Anthropic/DashScope 协议）：  
  通过请求参数 `stream=true` 启用。DashScope 原生接口返回标准 SSE 格式（`event: message\ndata: {...}`），[OpenAI 兼容接口](openai-compatible-interface.md)返回纯 `data: {...}` 行；需客户端按行解析并拼接 `delta.content`。注意：工具调用开始时 `delta.content` 可能为空字符串，应忽略该片段。

- **Application Call（智能体/工作流调用）**：  
  仅同步调用（`background=false`）支持 `stream=true`；异步调用不支持流式。启用后，响应为 SSE 流，包含 `planning`、`tool_calling`、`generation` 等阶段事件，便于前端分阶段渲染（如思考中 → 调用工具 → 生成答案）。

- **Omni Realtime API 与 Realtime API**：  
  原生基于 WebSocket 或 AOQ/WebRTC 的事件驱动架构，天然支持流式。服务端持续推送 `response.text.delta`、`response.audio.delta` 等事件，无需显式设置 `stream` 参数；客户端需监听对应事件类型并实时消费。

- **Knowledge（知识问答）**：  
  `/api/v2/apps/knowledge/chat` 接口默认支持 SSE 流式响应，返回 `planning`（检索规划）、`tool_calling`（知识库调用）、`generation`（最终回答）三类事件，每类事件含 `delta` 字段，支持渐进式展示。

## 关键参数和配置

- **通用开关参数**：  
  `stream`: `boolean`，设为 `true` 启用流式输出（Qwen API、Application Call、Knowledge 问答均适用）；默认 `false`。

- **客户端处理要求**：  
  - 必须支持 Server-Sent Events（SSE）或 WebSocket 事件解析；  
  - 对 [OpenAI 兼容接口](openai-compatible-interface.md)，需按 `\n\n` 分割响应块，提取 `data:` 后内容并 JSON 解析；  
  - 对 DashScope 原生及 Knowledge 接口，需识别 `event:` 头部以区分阶段（如 `event: generation`）；  
  - 实时 API（Omni/Realtime）需监听具体事件名（如 `response.text.delta`），不可依赖通用 `data` 字段。

- **注意事项**：  
  - 流式响应中 `usage`（token 统计）仅在最后一条消息中完整返回，中间块不含或仅含部分统计；  
  - 工具调用场景下，`delta.tool_calls` 可能分多次到达，需累积解析；  
  - 若需保证语义完整性（如避免单词截断），建议在客户端做简单缓冲（如等待标点或空格后再渲染）。

## 面向开发者：简洁实用提示

- ✅ **首选 DashScope 原生协议**：流式字段最全（含 `event`、`id`、`usage` 分项），调试友好；  
- ✅ **前端务必实现增量渲染**：不要等待 `done` 事件才显示内容，优先展示 `delta.content`；  
- ⚠️ **注意空 content 边界**：[OpenAI 兼容接口](openai-compatible-interface.md)中 `delta.content === ""` 表示工具调用开始，非错误；  
- ⚠️ **异步调用 ≠ 流式**：`application call` 的 `background=true` 模式不支持 `stream`，勿混用；  
- 🚀 **Realtime 场景直接用 SDK**：AOQ/WebSocket 客户端已内置流式事件监听与音频 buffer 管理，无需手动解析 SSE。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [knowledge](../api/knowledge.md)


