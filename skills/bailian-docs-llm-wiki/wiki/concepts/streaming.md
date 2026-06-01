# 流式输出

流式输出（Streaming）是指模型在生成过程中将结果以增量片段（chunk/delta）逐步返回给客户端的输出方式，而非等待全部内容生成完毕后一次性返回。这种方式可显著降低首token延迟，提升用户的实时交互体验。

## 概述

在百炼平台中，流式输出广泛应用于文本生成、语音合成、实时翻译、应用调用等多种场景。根据底层协议的不同，流式输出主要通过两种机制实现：

| 协议 | 机制 | 典型场景 |
|------|------|----------|
| HTTP | Server-Sent Events (SSE) | 文本生成、离线翻译、应用调用 |
| WebSocket | 双向流式通信 | 实时语音合成、实时翻译、多模态实时交互 |

## 在不同场景中的使用

### 文本生成模型

通过 [OpenAI 兼容接口](openai-compatible-api.md)或 DashScope 接口调用 Qwen 系列模型时，设置 `stream=True` 即可启用流式输出。响应以 SSE 格式逐步返回增量文本内容。

### 应用调用

智能体应用和工作流应用均支持流式输出。在 DashScope API 和 OpenAI 兼容 Responses API 中，通过 `stream` 参数控制：

```python
# DashScope SDK
response = Application.call(
    app_id='YOUR_APP_ID',
    prompt='你好',
    stream=True  # 启用流式输出
)
for chunk in response:
    print(chunk.output.text, end='')
```

### 语音/音视频翻译

离线翻译接口（qwen3-livetranslate-flash）**必须**设置 `stream=True`，不支持非流式调用。流式响应包含三类 chunk：

- **文本 chunk**：`choices[0].delta.content` 包含增量翻译文本
- **音频 chunk**：`choices[0].delta.audio.data` 包含 Base64 编码的音频数据
- **[Token](token.md) 消耗 chunk**：`usage` 字段包含 token 统计信息

### 语音合成

实时语音合成（如 Qwen-TTS Realtime、CosyVoice）通过 WebSocket 实现双向流式通信——客户端可流式发送待合成文本，服务端流式返回音频数据。

### 实时多模态交互

Qwen-Omni-Realtime API 基于 WebSocket 协议实现全双工流式通信，服务端通过 delta 事件逐步推送结果：

| 事件 | 内容 |
|------|------|
| `response.text.delta` | 增量文本输出 |
| `response.audio.delta` | 增量音频输出 |
| `response.audio_transcript.delta` | 模型输出的转录文本 |
| `response.function_call_arguments.delta` | 工具调用参数增量 |

## 关键参数和配置

### HTTP 流式（SSE）

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `stream` | boolean | `false` | 设为 `true` 启用流式输出 |
| `stream_options` | object | — | 部分接口支持，如设置是否在最后一个 chunk 中返回 `usage` |

### WebSocket 流式

WebSocket 场景无需显式设置 `stream` 参数，连接建立后即为双向流式通信模式。服务端通过带 `delta` 后缀的事件推送增量数据，以 `done` 后缀的事件标识某项输出完成。

## 开发注意事项

1. **部分接口强制要求流式**：如离线翻译接口必须设置 `stream=True`，不支持同步返回完整结果。
2. **增量拼接**：客户端需自行拼接各 chunk 中的增量内容以获取完整输出。
3. **错误处理**：流式过程中如发生错误，服务端会通过 `error` 事件或特定格式的 chunk 通知客户端，需做好中断处理。
4. **工作流应用的流式输出**：工作流应用启用流式时，可能按节点逐步返回中间结果，具体行为取决于工作流编排结构。
5. **连接管理**：WebSocket 流式场景需关注连接保活和断线重连策略。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [application call](../api/application-call.md)

