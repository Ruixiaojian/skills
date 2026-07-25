# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，将结果分块、实时、渐进式地返回给客户端，而非等待全部内容生成完毕后一次性返回。这种机制显著降低端到端延迟，支持实时渲染、语音合成逐字播报、交互式思考过程展示等关键体验。

## 在百炼平台的不同场景中如何使用

流式输出是百炼平台实现实时性与交互感的核心能力，在以下场景中被统一支持并差异化实现：

- **Realtime API（Omni/音频类实时模型）**：基于 WebSocket 或 AOQ 协议，服务端以事件流形式持续推送 `output.text.delta`（文本增量）、`output.audio.delta`（音频 PCM 片段）、`output.text.done` 等结构化事件。客户端可即时消费并渲染/播放，无需等待整句生成完成。适用于语音助手、实时字幕、低延迟对话等场景。

- **Qwen 文本生成 API（DashScope/OpenAI/Anthropic 兼容接口）**：通过设置 `stream: true` 参数，服务端返回 `text/event-stream`（OpenAI/Anthropic）或 JSON Lines（DashScope 原生），每行一个含 `delta` 字段的响应对象（如 `{"output": {"text": "你好"}}`）。适用于聊天界面逐字显示、代码补全预览等。

- **Managed Agents（托管智能体）**：通过 SSE（Server-Sent Events）连接 `/sessions/{session_id}/events/stream`，服务端按执行阶段推送结构化事件流，包括 `message`（模型回复片段）、`tool_call`（工具调用请求）、`tool_output`（工具执行结果）等。开发者可据此构建带中间状态反馈的智能工作流 UI。

- **Application Call（应用调用）**：同步调用时设置 `stream=true`，即可获得流式响应；但需注意：**工作流应用必须在流程编辑器中显式启用“流式输出”开关并重新发布**，否则该参数被忽略；异步调用（`background=true`）与流式互斥，不可同时启用。

- **多模态开发套件（multimodal-dialog）**：作为 Realtime API 的子集，同样支持 `["text"]` 或 `["text","audio"]` 模态的流式输出，音频以 24 kHz PCM 分片形式实时下发，文本以 delta 形式逐 token 推送。

## 关键参数和配置

| 场景 | 参数名 | 类型 | 说明 | 注意事项 |
|------|--------|------|------|----------|
| **所有 API（Qwen / Application / Realtime）** | `stream` | `boolean` | 启用流式响应的总开关 | 必须设为 `true` 才触发流式行为；默认为 `false` |
| **Realtime API（Omni / Audio）** | `modalities` | `array` | 指定输出模态，如 `["text"]` 或 `["text","audio"]` | 决定流式内容类型；`audio` 输出固定为 24 kHz PCM 分片 |
| **Qwen API（DashScope 原生）** | `output_format` | `string` | 可选 `"json"`（默认）或 `"text"`（仅限非流式） | 流式响应强制使用 JSON Lines 格式，无需设置 |
| **Application Call** | `stream` + 工作流配置 | — | 需在控制台工作流节点中开启“流式输出” | 未开启则 `stream=true` 无效；仅同步调用支持 |
| **Managed Agents** | — | — | 无显式参数，流式由 SSE 连接天然支持 | 调用 `/events/stream` 即启用，无需额外配置 |

> ⚠️ 重要限制：  
> - 异步调用（`background=true`）**不支持**流式输出；  
> - `qwen-omni-turbo-realtime` 系列模型的 `temperature`/`top_p`/`repetition_penalty` 等参数不可修改，流式行为不受影响；  
> - 流式响应中 `delta` 字段为增量内容（非全量），客户端需自行拼接；`done` 类事件（如 `output.text.done`）标志该字段结束。

## 面向开发者：简洁实用建议

- ✅ **首选 DashScope 原生接口**：流式格式最规范（JSON Lines），字段语义清晰（`delta`, `finish_reason`, `usage`），调试友好；  
- ✅ **Realtime 场景务必监听 `session.updated` 事件后再开启媒体流**：避免音频/文本错位；  
- ✅ **处理流式文本时，始终累积 `delta` 并检测 `finish_reason`**：不要依赖单次响应完整性；  
- ✅ **音频流需按顺序拼接 PCM 片段，并确保采样率匹配（输入16k → 输出24k）**；  
- ❌ **勿在流式响应中解析 `choices[0].message.content`（OpenAI 兼容）以外的字段**：部分字段（如 `usage`）仅在最终 `data: [DONE]` 前出现一次；  
- 🛠️ SDK 提示：DashScope Python/JS SDK 均提供 `.on('message', callback)` 或 `async for chunk in response` 等原生流式语法糖，优先使用。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [managed agents](../guides/managed-agents.md)
- [application call](../api/application-call.md)


