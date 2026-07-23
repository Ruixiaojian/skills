# 流式输出

流式输出（Streaming Output）是指模型在生成响应过程中，将结果以增量方式分块（chunk）实时返回给客户端，而非等待全部内容生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户体验，尤其适用于对话交互、长文本生成、语音合成等对实时性敏感的场景。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台中并非统一接口能力，而是按调用协议和应用类型差异化支持，需结合具体 API 显式启用：

- **模型 API（Qwen 系列）**：  
  DashScope 原生接口与 OpenAI 兼容的 `chat/completions` 接口均支持流式响应，通过 `stream=true` 参数开启。返回格式为 Server-Sent Events（SSE），每 chunk 包含 `delta.content` 字段（可能为空字符串，需忽略并持续拼接），最终 chunk 含 `finish_reason`。

- **应用调用（Application Call）**：  
  调用已发布的智能体或工作流时，可通过 `stream=true` 启用流式输出。**注意**：工作流应用需在结束节点显式开启“流式开关”，否则即使请求设 `stream=true` 也不会流式返回。

- **Omni Realtime API（WebSocket）**：  
  作为原生实时协议，流式是默认行为。服务端通过 `response.text.delta`、`response.audio.delta` 等事件持续推送文本/音频片段，无需额外参数；`modalities` 配置决定输出模态组合（如 `["text", "audio"]`）。

- **Realtime API（AOQ/WebRTC/WebSocket）**：  
  所有协议均默认支持流式文本与音频输出。客户端需监听 `response.text.delta` 或 `response.audio.delta` 事件，并按顺序拼接；音频流需按采样率（输入 16 kHz / 输出 24 kHz）解码播放。

- **应用支持层（RAG/插件类应用）**：  
  若需实现增量式流式（即仅返回本次新增内容，而非累计全文），必须**同时设置 `stream=True` 和 `incremental_output=True`**。该模式适用于前端逐字高亮、带思考过程的工具调用反馈等精细化控制场景。

## 关键参数和配置

| 参数名 | 类型 | 说明 | 生效范围 |
|--------|------|------|----------|
| `stream` | boolean | 启用基础流式响应（逐 token 分块返回） | 所有支持流式的 API（模型、应用、Realtime） |
| `incremental_output` | boolean | 启用增量式流式（每 chunk 仅含本次新增内容，非累计） | 仅 `application call` 及部分 RAG 应用支持；必须与 `stream=true` 共用 |
| `modalities` | array | 指定流式输出模态（如 `["text"]`, `["text","audio"]`） | Omni Realtime / Realtime API |
| `voice` | string | 配合音频流式时指定音色，影响 `response.audio.delta` 的合成效果 | Omni Realtime / Realtime API |

> ⚠️ 注意事项：
> - 流式响应中 `delta.content` 可能为空字符串（表示中间 token 分片），客户端应跳过空 content 并持续累积；
> - [OpenAI 兼容接口](openai-compatible-api.md)不支持 `response_format: { "type": "json_object" }` 等结构化流式，JSON 模式需使用 DashScope 原生接口；
> - 工作流应用未开启节点级流式开关时，`stream=true` 将被静默忽略；
> - `incremental_output=true` 仅在应用侧启用对应能力后生效，需在百炼控制台配置或通过 SDK 显式声明。

## 面向开发者：简洁实用建议

- ✅ **首选 DashScope SDK**：Python SDK（v1.20.0+）自动处理 SSE 解析与 chunk 迭代，调用时传入 `stream=True` 即可：
  ```python
  from dashscope import Generation
  response = Generation.call(
      model='qwen-max',
      messages=[{'role': 'user', 'content': '写一首五言绝句'}],
      stream=True
  )
  for chunk in response:
      if chunk.output and chunk.output.text:
          print(chunk.output.text, end='', flush=True)  # 实时打印
  ```

- ✅ **前端流式渲染**：监听 `event: message`，解析 `data:` 字段，用 `textContent` 追加而非 `innerHTML`（防 XSS），并做好空 content 过滤。

- ✅ **音频流处理**：Realtime/Omni 场景下，`response.audio.delta` 返回 Base64 编码 PCM 数据，需按 `output_audio_format`（固定为 `pcm`，24 kHz）解码后喂入 Web Audio API 或原生播放器。

- ❌ **避免混用模式**：`stream=true` 与 `background=true` 互斥，不可同时设置；流式调用不支持异步轮询。

- 🚨 **生产环境必做**：流式连接需设置超时重连机制（推荐 30s 连接超时 + 5s 重试间隔），并在 `error` 事件中捕获断连、鉴权失败等异常。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application support](../guides/application-support.md)


