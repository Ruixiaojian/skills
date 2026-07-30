# 流式输出

流式输出（Streaming Output）是指模型响应以增量方式分块返回，而非等待整个生成过程完成后再一次性返回全部结果。它通过持续发送 token 或结构化数据片段，显著降低用户感知延迟，提升交互实时性，是构建低延迟 AI 应用（如对话助手、实时翻译、代码补全）的关键能力。

## 在百炼平台的不同场景中如何使用

- **应用调用（Application Call）**：在同步模式下（`background=false`），通过设置 `stream=true` 启用流式输出；异步调用（`background=true`）不支持流式，需轮询获取最终结果。
- **Qwen 模型直调（Qwen API）**：所有 DashScope 原生接口默认支持流式（`stream: true`），[OpenAI 兼容接口](openai-compatible-interface.md)也支持，但需注意其流式 chunk 中工具调用字段（如 `delta.tool_calls`）可能不完整，建议关键逻辑使用非流式验证。
- **Omni 实时 API**：作为 WebSocket 事件驱动接口，天然支持流式文本与音频同步输出（如 `response.text.delta`、`response.audio.delta`），无需额外参数，所有 `modalities` 组合均按事件流实时推送。
- **RAG/智能体增强场景**：流式输出可与知识检索、插件调用协同工作；若启用 `incremental_output=true`（需配合 `stream=true`），服务端将仅返回新增 token，避免重复传输已发送内容，进一步优化带宽与前端渲染效率。

## 关键参数和配置

| 参数名 | 类型 | 作用 | 适用场景 | 注意事项 |
|--------|------|------|----------|----------|
| `stream` | boolean | 启用流式响应机制 | 所有支持流式的 API（Application Call、Qwen 直调、Omni 实时） | 必须为 `true`；异步调用中设为 `true` 将被忽略 |
| `incremental_output` | boolean | 启用增量式流式（每次仅返回新 token，非全量重发） | Application Call、Qwen DashScope 接口 | 仅在 `stream=true` 时生效；前端需自行拼接 token 流 |
| `modalities` | array | 控制输出模态组合（如 `["text"]` 或 `["text","audio"]`） | Omni Realtime API | 决定流式事件类型（`response.text.delta` / `response.audio.delta`），不可动态变更 |

> ⚠️ 注意：  
> - 流式仅适用于同步请求路径；异步任务（`background=true`）必须等待任务完成后再获取完整结果。  
> - [OpenAI 兼容接口](openai-compatible-interface.md)的流式响应格式严格遵循 OpenAI SSE 标准（`data: {...}`），而 DashScope 原生接口使用自定义 JSON 行格式（每行一个 JSON 对象）。  
> - 前端解析流式响应时，需正确处理分块边界、空行、错误事件（如 `error` 字段），推荐使用百炼官方 SDK（如 `dashscope` Python SDK）自动管理连接与解析逻辑。

## 面向开发者提示

- ✅ **推荐实践**：对实时性敏感的 UI（如聊天输入框打字效果），务必启用 `stream=true` + `incremental_output=true`，并监听 `content` 或 `delta.content` 字段增量更新 DOM。  
- ❌ **避免踩坑**：不要在流式响应中依赖 `usage` 或 `finish_reason` 字段的中间值——它们仅在最后一个 chunk 中完整出现。  
- 🛠️ **调试建议**：使用控制台「API 调试」工具或 `curl -N` 命令直接观察原始 SSE 流；Python 开发者可结合 `requests.Response.iter_lines()` 或 `dashscope.Generation.stream()` 方法快速验证。  
- 📈 **性能考量**：流式本身不降低模型计算耗时，但可减少首字节时间（TTFB）；若发现流式延迟高，请优先检查网络链路、token 生成速率（受 `temperature`/`top_p` 影响）及客户端解析开销。

## 关联主题页

- [application call](../api/application-call.md)
- [application support](../guides/application-support.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)


