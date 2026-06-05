# 流式输出

流式输出（Streaming）是指模型在生成过程中，将结果以增量片段的形式逐步返回给客户端，而非等待全部生成完成后一次性返回。这种方式可以显著降低用户感知的首次响应延迟，适用于对话交互、语音合成、实时语音识别等需要即时反馈的场景。

## 工作原理

在非流式（默认）模式下，客户端发送请求后需等待服务端完成全部生成，才能收到完整的响应。在流式模式下，服务端每生成一个片段（chunk/delta）就立即推送给客户端，客户端可边接收边处理、边渲染，从而实现"边生成边输出"的效果。

流式输出在百炼平台中通过两种协议实现：

| 协议 | 传输机制 | 典型场景 |
|------|---------|---------|
| HTTP（SSE） | 服务端发送事件（Server-Sent Events），客户端通过单向流接收增量数据 | 文本生成、应用调用 |
| WebSocket | 双向流式通信，客户端和服务端可同时收发数据 | 实时语音合成、实时语音识别、实时多模态交互 |

## 在不同场景中的使用

### 文本生成模型调用

通过 [OpenAI 兼容接口](openai-compatible-api.md)或 DashScope 接口调用 Qwen 系列模型时，设置 `stream=True` 即可启用流式输出。客户端会以 SSE 方式逐步接收生成的文本 token。

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

stream = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### 智能体与工作流应用调用

百炼应用（智能体和工作流）的两套调用接口——DashScope API 和 OpenAI 兼容 Responses API——均支持流式输出。

**DashScope API 示例：**

```python
from dashscope import Application

responses = Application.call(
    app_id='YOUR_APP_ID',
    prompt='介绍一下你自己',
    stream=True
)

for response in responses:
    print(response.output.text, end="\r", flush=True)
```

**Responses API 示例：**

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/"
)

stream = client.responses.create(
    input="介绍一下你自己",
    stream=True
)

for event in stream:
    print(event)
```

### 实时语音合成

Qwen-TTS Realtime 和 CosyVoice 等模型通过 WebSocket 实现双向流式通信：客户端可流式发送待合成文本，服务端则流式返回音频片段。这使得合成过程可以与文本生成过程并行进行，进一步降低端到端延迟。

### 实时语音识别

Qwen-ASR Realtime、Fun-ASR、Paraformer 等实时语音识别模型通过 WebSocket 接收流式音频输入，并以增量方式返回识别结果（中间结果和最终结果）。

### 实时多模态交互

Qwen-Omni-Realtime API 基于 WebSocket 实现音频、视频、文本的双向流式通信。服务端通过 delta 事件逐步推送生成内容：

| 事件 | 说明 |
|------|------|
| `response.text.delta` | 增量文本输出 |
| `response.audio.delta` | 增量音频输出 |
| `response.audio_transcript.delta` | 模型输出的转录文本（增量） |
| `response.function_call_arguments.delta` | 工具调用参数（增量） |

## 关键参数与配置

| 参数 | 类型 | 默认值 | 说明 | 适用接口 |
|------|------|--------|------|---------|
| `stream` | boolean | `false` | 是否启用流式输出 | HTTP 类接口（文本生成、应用调用） |
| `stream_options` | object | — | 流式输出的附加选项，如 `include_usage` 可在最后一个 chunk 中返回 token 用量 | [OpenAI 兼容接口](openai-compatible-api.md) |
| `incremental_output` | boolean | — | DashScope 接口中控制是否增量输出（每次只返回新增部分，而非累积全文） | DashScope 接口 |

## 注意事项

- **协议选择**：文本生成和应用调用场景通常使用 HTTP SSE 即可满足需求；实时语音、音视频交互等需要双向流式通信的场景应使用 WebSocket。
- **错误处理**：流式输出过程中如果发生错误，错误信息会通过流中的事件返回。客户端应妥善处理连接中断和错误事件，避免数据丢失。
- **工作流应用**：工作流类型的应用在流式模式下，可能会在中间节点处出现等待，输出节奏取决于工作流各节点的执行进度。
- **token 用量统计**：在流式模式下，token 用量信息通常在最后一个数据块中返回，而非每个 chunk 都包含。如需获取，可设置 `stream

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)

