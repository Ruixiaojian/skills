# 流式输出（SSE 与 WebSocket）

流式输出指模型在生成结果的同时，将片段逐步推送给客户端，从而显著降低首字时延、提升交互感。在百炼平台上主要通过两种协议实现：基于 HTTP 长连接的 **SSE（Server-Sent Events）** 用于单向逐块推送，**WebSocket** 则用于客户端与服务端双向流式收发音频、图像或文本。

## 在百炼平台的典型场景

百炼平台对流式输出的使用大致可以分为三类。

### 1. SSE：单向流式响应（HTTP）

适合"客户端发请求 → 服务端持续推送结果"的场景，无需双向通道：

- **音乐生成（Fun-Music）**：在 `POST /api/v1/services/audio/music/generation` 上加请求头 `X-DashScope-SSE: enable` 即可启用 SSE。中间消息通过 `output.audio.data` 不断推送 Base64 音频片段（`finish_reason` 为字符串 `"null"`），最终消息以 `finish_reason: stop` 结束，并在 `output.audio.url` 给出完整音频的 OSS 下载链接。
- **OpenAI 兼容 Chat Completions（含语音/音视频翻译）**：`qwen3-livetranslate-flash` 等模型走 `${base_url}/chat/completions`，请求必须设置 `stream: true`，由 HTTP SSE 流式返回翻译文本（可选语音）。建议同时设置 `stream_options.include_usage: true`，以便在最后一个 chunk 拿到 Token 用量。

SSE 通道是单向的：客户端一次性提交请求体，之后只接收服务端逐步推送的 `data:` 帧，直到流终止。

### 2. WebSocket：双向流式音视频/对话

适合需要持续推流、低时延、可被中断的交互场景。典型代表是 Realtime 家族：

- **Qwen-Omni-Realtime（多模态对话）**：通过 `wss://dashscope.aliyuncs.com/api-ws/v1/realtime` 建立双向通道，客户端逐帧发送 Base64 PCM 音频与 JPG/JPEG 图像，服务端实时返回音频、文本与转录。
- **Qwen-TTS-Realtime 与 CosyVoice / Sambert 实时合成**：在 `wss://dashscope.aliyuncs.com/api-ws/v1/inference` 上由客户端发送 `session.update`、`input_text.append` 等事件，服务端以 `response.audio.delta`、`response.done` 等事件持续吐出音频片段。
- **Paraformer / Fun-ASR / Qwen-ASR-Realtime 实时语音识别**：客户端持续上送 PCM/Opus 音频，服务端流式回吐识别结果（含部分识别、最终识别、说话人切换等事件）。
- **Qwen-LiveTranslate 实时音视频翻译**：在 Realtime WebSocket 之上，客户端推送麦克风/摄像头流，服务端逐句返回翻译文本与可选语音。

WebSocket 形态采用统一的"客户端事件 / 服务端事件"协议：消息以 JSON 帧承载（音频/图像为 Base64 字段），由 `session.*`、`input_audio_buffer.*`、`input_image_buffer.*`、`conversation.item.*`、`response.*` 等事件类型驱动。

### 3. WebSocket 的两种触发模式

针对实时多模态/语音场景，WebSocket 协议通过 `session.turn_detection` 字段切换两种工作模式：

| 维度 | VAD 模式（默认） | Manual 模式 |
| --- | --- | --- |
| `turn_detection` | `"server_vad"` 或 `"semantic_vad"` | `null` |
| 适用场景 | 持续推流、自由对话、语音打断 | 按下即说、本地音视频文件回放 |
| 响应触发 | 服务端检测到静音超阈值后自动生成响应 | 客户端显式发送 `input_audio_buffer.commit` + `response.create` |
| 工具调用回传 | 服务端自动基于工具结果继续生成 | 需再次发送 `response.create` 触发最终响应 |

`server_vad` 通过 `threshold`（默认 0.5）与 `silence_duration_ms`（默认 800）控制灵敏度；`semantic_vad` 仅 `qwen3.5-omni-realtime` 系列支持，可过滤回应语与背景音。

## 接入端点与地域

流式输出沿用百炼的标准端点，注意北京和新加坡两地的 API Key 不通用：

- **SSE / HTTP（非实时）**
  - 中国内地（北京）：`https://dashscope.aliyuncs.com`
  - 国际（新加坡）新版：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
- **WebSocket 推理类（TTS / ASR）**
  - 北京：`wss://dashscope.aliyuncs.com/api-ws/v1/inference`
  - 新加坡新版：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference`
- **WebSocket Realtime（Omni / Qwen-TTS-Realtime / Qwen-ASR-Realtime / LiveTranslate）**
  - 北京：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`
  - 新加坡新版：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`
- 新加坡旧版域名 `dashscope-intl.aliyuncs.com` 即将下线，国际地域请尽快迁移到带 `WorkspaceId` 的新版域名。

鉴权统一通过 `Authorization: Bearer <API_KEY>` 请求头传递；对部分 ASR 等异步接口，提交任务还需要 `X-DashScope-Async: enable` 请求头。

## 关键参数与配置

启用与控制流式输出时常用的字段：

- **HTTP / SSE 启用**：
  - `X-DashScope-SSE: enable`（DashScope 原生协议，如 Fun-Music）。
  - `stream: true`（OpenAI 兼容 Chat Completions，如 LiveTranslate）。
  - `stream_options.include_usage: true`：在最后一个 chunk 中携带 Token 用量统计。
- **WebSocket 连接参数**：
  - URL 查询参数 `model=<model_name>`（Qwen-ASR-Realtime）或在 `session.update` 中指定。
  - `Authorization: Bearer <API_KEY>` 请求头。
- **会话与轮次控制**：
  - `session.update`：建立连接后更新会话配置，参数非法时返回 `error`。
  - `session.turn_detection`：`"server_vad"` / `"semantic_vad"` / `null`，决定 VAD 还是 Manual 模式。
  - `response.create` / `response.cancel`：手动触发或取消响应（Manual 模式与工具回传后必用）。
- **音视频缓冲**：
  - `input_audio_buffer.append` / `commit` / `clear`：追加、提交、清空音频缓冲（VAD 模式下提交由服务端自动完成）。
  - `input_image_buffer.append`：写入 Base64 JPG/JPEG 图像，随下一次音频 commit 一并提交。
- **模态与采样**：
  - `modalities`：`["text"]` 或 `["text", "audio"]`。
  - `temperature` / `top_p` / `top_k` / `max_tokens` 等采样参数（`qwen-omni-turbo-realtime` 系列固定，不可修改）。
- **流式音乐生成限制**：
  - `lyrics` 流式上限：中文 300~350 字、英文 200~250 词。
  - `prompt` 流式上限：5~1000 个中文汉字或英文单词。

## 流式消息的常见解析模式

不论 SSE 还是 WebSocket，处理流式输出时建议遵循统一模式：

1. **识别"中间帧"与"终止帧"**：中间帧通常仅携带增量片段（如 `output.audio.data` 是 Base64 片段、`response.audio.delta`、`response.text.delta`），终止帧给出完整结果（如 `output.audio.url`、`response.done`、`finish_reason: stop`）。
2. **拼接增量结果**：对文本类 `*.delta` 直接拼接；对音频类 `audio.delta` / `audio.data` 解码后追加到本地音频缓冲再播放/落盘。
3. **处理错误事件**：服务端会通过 `error` 事件或 SSE 的 `error` 帧返回异常，应及时关闭连接或重试。
4. **WebSocket 工具调用闭环**：在 `response.function_call_arguments.done` 后由客户端执行函数，再通过 `conversation.item.create` 回传 `function_call_output`；Manual 模式下还需再次 `response.create` 才会触发最终响应。

合理选择 SSE 还是 WebSocket：单向、一次性的长任务（如音乐生成、翻译已录制文件）用 SSE 最简单；麦克风/摄像头实时输入、可打断对话则必须使用 WebSocket Realtime 协议。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [music generation references](../api/music-generation-references.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)


