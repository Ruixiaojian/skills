# 流式输出

流式输出（Streaming Output）是指模型服务将生成结果分块、实时、逐段返回给客户端的通信模式，而非等待全部内容生成完毕后一次性返回。该模式显著降低端到端延迟，提升用户体验，并支持前端实时渲染、语音合成流式播放、长文本渐进式展示等典型场景。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼平台中并非全局默认行为，而是按接口类型和调用方式显式启用，主要应用于以下三类核心场景：

- **[OpenAI 兼容接口](openai-compatible-interface.md)（Chat Completions / Vision / Responses API）**：通过设置 `stream=true` 参数启用。适用于 `qwen-plus`、`qwen3-vl-plus`、`deepseek-v4-flash` 等主流文本与[多模态](multimodal.md)模型。响应为 Server-Sent Events（SSE）格式，每块含 `delta.content` 字段；末尾 chunk 可选包含 token 统计（需额外配置 `stream_options={"include_usage": true}`）。

- **智能体/工作流应用调用（Application Call）**：同步调用时支持 `stream=true`，但需满足前提条件——工作流应用必须在结束节点显式开启「流式输出」开关并重新发布；智能体应用默认支持。**异步调用（`background=true`）不支持流式输出**，此为硬性限制。

- **实时[多模态](multimodal.md)交互接口（Omni Realtime / Realtime API）**：底层基于 WebSocket 或 AOQ 的双向流式协议，天然支持流式。文本输出以 `conversation.item.output.text.delta` 事件实时推送；音频输出则以 PCM 数据帧持续下发（24 kHz），无需额外参数控制，流式为协议级默认行为。

> ⚠️ 注意：文件上传、批量推理（Batch Chat / Batch File）、Embeddings、异步任务查询等非交互式接口**不支持流式输出**。

## 关键参数和配置

| 参数 | 类型 | 说明 | 是否必需 | 备注 |
|------|------|------|----------|------|
| `stream` | boolean | 启用流式响应开关 | 否（默认 `false`） | 所有支持流式的接口均需显式设为 `true`；设为 `true` 后，HTTP 响应头 `Content-Type` 将为 `text/event-stream`。 |
| `stream_options` | object | 流式增强选项 | 否 | 目前仅 [OpenAI 兼容接口](openai-compatible-interface.md)支持；必须传 `{"include_usage": true}` 才能在最终 chunk 中返回 `usage` 字段（含 `prompt_tokens`/`completion_tokens`）。 |
| `modalities` | array | 输出模态声明（Realtime 场景） | 是（Realtime API） | 如 `["text"]` 或 `["text","audio"]`；决定服务端是否推送文本 delta 和/或音频帧流。 |

- **SDK 使用提示**：
  - Python（OpenAI SDK）：使用 `for chunk in client.chat.completions.create(..., stream=True): ...` 迭代处理；
  - DashScope SDK（Python/Java）：调用 `.stream()` 方法（如 `client.chat.completions.stream(...)`）；
  - Realtime API：无需设置 `stream`，直接监听 `conversation.item.output.text.delta` 或 `audio.delta` 事件即可。

## 面向开发者，简洁实用

- ✅ **推荐场景**：实时对话界面、语音助手前端、代码补全编辑器、长文档摘要预览。
- ❌ **禁止场景**：异步任务、批量处理、[Token](token.md) 统计强依赖的离线分析（流式统计需手动累加）。
- 🔧 **调试技巧**：用 `curl` 测试流式接口时，添加 `-N` 参数禁用缓冲（`curl -N -H "Authorization: Bearer ..." ...`）；浏览器开发者工具 Network 标签页可观察 SSE 流。
- 📉 **性能注意**：流式不降低总生成耗时，但大幅改善首字延迟（Time to First [Token](token.md)）；高并发下建议复用 HTTP 连接池（参见 [连接复用参数](../../raw/model-api-reference/more-about-models/more-about-models.md#连接复用参数)）。
- 🛑 **错误处理**：流式请求中断（如网络闪断）后，服务端不会自动重试；客户端需自行实现断点续传逻辑（如记录已接收 `id` 或 `index`）。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application call](../api/application-call.md)


