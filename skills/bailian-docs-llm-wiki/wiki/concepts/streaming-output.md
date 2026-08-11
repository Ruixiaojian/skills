# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在生成过程中持续分块返回结果，而非等待全部内容完成后再一次性返回。它显著降低端到端延迟，提升用户交互体验，尤其适用于长文本生成、实时对话、语音合成等对响应流畅性敏感的场景。

## 在百炼平台的不同场景中如何使用

流式输出在百炼多个核心能力层中统一支持，但启用方式、数据格式与适用约束因协议和场景而异：

- **模型 API（Qwen 系列）**：通过 `stream=true` 参数启用（DashScope 原生接口或 OpenAI/Anthropic 兼容接口均支持）。DashScope 返回 `output.text` 字段增量片段；[OpenAI 兼容接口](openai-compatible-api.md)返回 `delta.content`；Anthropic 兼容接口返回 `content` 数组中的逐条 `text` 或 `tool_use` 事件。
  
- **应用调用（Application Call）**：仅同步调用（`background=false`）支持流式输出，需设置 `stream=true`。工作流应用需在流程编辑器中为“结束节点”显式开启「流式输出」开关并重新发布；智能体应用默认支持，无需额外配置。

- **Realtime API（Omni / Audio 系列）**：原生基于 WebSocket 或 AOQ 的事件驱动架构，天然支持流式。文本输出以 `response.text.delta` 事件持续推送；音频输出为连续 PCM 数据流；VAD 触发后即开始流式响应，无需显式传参 `stream`。

- **高吞吐推理（Fast Mode）**：`glm-5.2-fast-preview` 等快速模式模型支持结构化流式字段，如 `delta.reasoning_content`（推理过程）与 `delta.content`（最终回答）分离输出，便于前端分阶段渲染。

- **应用增强能力（RAG/[插件](plugin.md)）**：启用 `stream=true` 后，RAG 检索结果融合、[插件](plugin.md)调用中间步骤（如代码执行日志）可随主回复一同流式返回；配合 `incremental_output=true` 可确保每次只返回新增内容，避免重复渲染。

> ⚠️ 注意：异步调用（`background=true`）、部分旧版工作流节点、以及非实时协议（如纯 HTTP 同步请求未启用流式）均不支持流式输出。

## 关键参数和配置

| 参数名 | 类型 | 说明 | 是否必需 | 备注 |
|--------|------|------|----------|------|
| `stream` | boolean | 启用流式响应（SSE 或 WebSocket 事件流） | 否（默认 `false`） | 所有支持流式的接口均通用此参数 |
| `incremental_output` | boolean | 仅当 `stream=true` 时生效；启用后每次返回增量内容（非全量重发） | 否（默认 `false`） | 推荐前端启用，避免重复解析/渲染 |
| `modalities` | string[] | Realtime API 中指定输出模态，如 `["text"]` 或 `["text","audio"]` | 是（Realtime 场景） | `["audio"]` 单独不合法，必须含 `"text"` |
| `turn_detection.type` | string | 控制 VAD 触发时机（`server_vad` / `semantic_vad`），影响流式起始点 | 否（默认 `server_vad`） | `semantic_vad` 更精准，减少静音截断 |

- **HTTP 协议要求**：启用流式时，客户端需支持 Server-Sent Events（SSE）或 WebSocket；HTTP 请求头应包含 `Accept: text/event-stream`（SSE）或升级为 WebSocket 连接。
- **SDK 使用提示**：DashScope SDK 提供 `Generation.stream_call()` 方法；OpenAI 兼容 SDK 需设置 `stream=True` 并迭代 `response` 对象；Realtime SDK 通过监听 `response.text.delta` 等事件处理流式数据。

## 面向开发者：简洁实用建议

- ✅ **必做**：始终检查 `stream` 参数是否已设为 `true`，并在客户端实现流式事件监听（不要依赖 `response.choices[0].message.content` 一次性读取）。
- ✅ **推荐**：启用 `incremental_output=true` 避免前端重复拼接；Realtime 场景优先选用 `semantic_vad` + 合理 `silence_duration_ms` 提升首字延迟与断句准确性。
- ⚠️ **避坑**：
  - [OpenAI 兼容接口](openai-compatible-api.md)与 DashScope 接口的流式字段命名不同（`delta.content` vs `output.text`），切勿硬编码字段路径；
  - 异步调用（`background=true`）**完全不支持流式**，需改用同步调用+超时重试策略；
  - 文件上传、[多模态](multi-modal.md)输入（如图像）不影响流式能力，但需确保模型本身支持（如 Qwen-VL 仅 DashScope 原生接口支持流式）。
- 🛠️ **调试技巧**：使用 `curl -N` 或 Postman 的 SSE 模式直接测试流式响应；Realtime 场景可通过 SDK 的 `debug: true` 查看完整事件日志。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application support](../guides/application-support.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


