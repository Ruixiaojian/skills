# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的实时多模态交互接口，支持语音、文本、图像输入与文本、语音输出的端到端流式交互。它采用事件驱动模型，通过客户端事件（如 `session.update`、`input_audio_buffer.append`）控制会话状态与数据流，服务端以结构化事件（如 `session.created`、`response.audio.delta`）实时反馈处理结果。该 API 专为低延迟、高保真语音交互场景设计，适用于智能客服、虚拟助手等实时对话系统。

## 支持的模型/功能

- **核心模型系列**：  
  - `qwen3.5-omni-realtime`（支持 `semantic_vad`、联网搜索、工具调用）  
  - `qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime`（支持 `idle_timeout_ms`、`smooth_output`）  
  - `qwen-omni-turbo-realtime`（仅支持基础 VAD 与音频 I/O，[不支持修改多数生成参数](../../raw/model-api-reference/omni-realtime-api/client-events.md)）  

- **多模态能力**：  
  - 输入：PCM 音频（16 kHz）、JPG/JPEG 图像（≤1080p，Base64 编码后 ≤256 KB）  
  - 输出：文本 + PCM 音频（24 kHz），可配置为仅文本（`["text"]`）或音文并行（`["text","audio"]`）  
  - 工具调用：仅 `qwen3.5-omni-realtime` 系列支持 `tools` 配置，用于自主触发外部函数（如天气查询）  
  - 联网搜索：仅 `qwen3.5-omni-realtime` 系列支持 `enable_search`，且与 `tools` 互斥  
  - 声音复刻：需先调用独立的 [声音复刻API](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md) 创建音色，再在 `session.update` 中通过 `voice` 字段传入  

> **注意**：文档中 `qwen3-Omni-Flash-Realtime`（带连字符）与 `qwen3.5-omni-flash-realtime`（点号）存在命名不一致。SDK 文档（[Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 和 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)）均使用 `qwen3.5-omni-flash-realtime`，应以此为准；`qwen3-Omni-Flash-Realtime` 为过时写法。

## 关键参数

所有参数均通过 `session.update` 客户端事件或 SDK 的 `update_session()` 方法配置：

- **基础配置**：  
  - `modalities`: 输出模态，`["text"]` 或 `["text","audio"]`（默认）  
  - `voice`: 音色名，不同模型默认值不同（如 `qwen-omni-turbo-realtime` 默认 `Chelsie`）  
  - `input_audio_format` / `output_audio_format`: 固定为 `"pcm"`，对应 16 kHz 输入 / 24 kHz 输出  

- **VAD 控制**（`turn_detection`）：  
  - `type`: `"server_vad"`（默认）或 `"semantic_vad"`（仅 `qwen3.5-omni-realtime` 支持）  
  - `threshold`: [-1.0, 1.0]，值越低越灵敏（嘈杂环境建议提高）  
  - `silence_duration_ms`: [200, 6000] ms，静音超时触发响应（默认 800）  
  - `idle_timeout_ms`: [5000, 30000] ms，仅 `qwen3.5-omni-plus-realtime`/`flash-realtime` + `server_vad` 有效，用于静默后主动引导  

- **生成控制**（部分参数 `qwen-omni-turbo-realtime` 不支持修改）：  
  - `temperature`: [0, 2)，控制多样性（默认 0.7~1.0）  
  - `top_p`: (0, 1.0]，核采样阈值（默认 0.01~1.0）  
  - `top_k`: ≥0，候选集大小（默认 20~50）  
  - `max_tokens`: 最大输出 token 数（截断，不影响生成过程）  
  - `repetition_penalty` / `presence_penalty`: 控制重复度（默认 1.0~1.05 / 0.0~1.5）  
  - `seed`: 整数，提升结果确定性（默认 -1）  

- **高级功能开关**：  
  - `enable_search`: `true` 启用联网搜索（仅 `qwen3.5-omni-realtime`）  
  - `search_options.enable_source`: `true` 返回搜索来源  
  - `tools`: 工具定义数组（仅 `qwen3.5-omni-realtime`，与 `enable_search` 互斥）  
  - `smooth_output`: `true`/`false`/`null`，仅 `qwen3-Omni-Flash-Realtime` 系列生效（见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）  

## 使用方式

1. **建立连接**：  
   - WebSocket URL 格式：`wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`（推荐业务空间专属域名，[详见 Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)）  
   - 连接后立即收到 `session.created` 事件，含默认配置  

2. **配置会话**：  
   - 发送 `session.update` 事件（或调用 SDK `update_session()`）设置 `modalities`、`voice`、`turn_detection` 等  

3. **输入数据**：  
   - **音频**：循环发送 `input_audio_buffer.append`（Base64 PCM），VAD 模式下由服务端自动提交；Manual 模式需显式发送 `input_audio_buffer.commit`  
   - **图像**：发送 `input_image_buffer.append`（Base64 JPG/JPEG），与音频缓冲区共用 `commit`  
   - **文本指令**：通过 `instructions` 字段在 `session.update` 中设定系统角色  

4. **触发响应**：  
   - VAD 模式：语音停止后服务端自动触发 `response.create`  
   - Manual 模式：客户端发送 `response.create` 显式请求  
   - 工具调用后：客户端回传 `conversation.item.create`（含 `call_id` 和 `output`），再发 `response.create`  

5. **接收输出**：  
   - 流式音频：`response.audio.delta`（Base64 PCM） → `response.audio.done`  
   - 流式文本：`response.text.delta` → `response.text.done`  
   - 转录结果：`conversation.item.input_audio_transcription.delta`（实时预览） → `.completed`（最终结果）  

## 限制和注意事项

- **音频限制**：输入必须为 16 kHz PCM 单声道；输出固定为 24 kHz PCM，不可自定义采样率  
- **图像限制**：仅 JPG/JPEG，分辨率建议 480p/720p（≤1080p），单图 Base64 编码后 ≤256 KB  
- **参数兼容性**：  
  - `tools` 与 `enable_search` 不可同时启用（[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 明确指出）  
  - `qwen-omni-turbo-realtime` 系列不支持修改 `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed`（所有相关文档均强调此限制）  
- **模式选择**：  
  - VAD 模式（`turn_detection.type = "server_vad"`）适用于持续音频流，支持语音打断  
  - Manual 模式（`turn_detection = null`）适用于按键录音等离散输入，需手动 `commit` 和 `response.create`  
- **错误处理**：服务端返回 `error` 事件（含 `type`、`code`、`message`、`param`），需监听并解析（如 `invalid_value` 错误提示 `modalities` 组合非法）  
- **域名迁移**：北京/新加坡地域已上线业务空间专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），[官方强烈推荐迁移](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)以获得更高性能与稳定性

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


