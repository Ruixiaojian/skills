# model experience

`model experience` 是百炼平台面向开发者提供的统一模型能力体验层，涵盖文本、视觉、语音、音频、3D、视频等全模态模型的选型、调用与配置。其核心目标是通过标准化接口、一致的参数设计和跨模态协同能力（如 Function Calling、思考模式、结构化输出），降低多模型集成复杂度，支持从快速验证到生产部署的全生命周期。

## 支持的模型/功能

百炼提供覆盖主流 AI 场景的模型族系，按模态与能力分层组织：

- **文本生成**：以 `qwen3.7-plus` 为旗舰，支持 1M 上下文、Function Calling、内置工具（联网搜索/代码解释器）、结构化 JSON 输出及 `enable_thinking` 控制的混合推理模式；轻量场景可选用 `qwen3.7-flash` [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。
- **视觉理解**：`qwen3.7-plus` 和 `qwen3.7-flash` 同时支持图像、视频（最长 2 小时）、OCR 及多图输入，具备完整 Function Calling 与内置工具能力；专用 OCR 场景推荐 `qwen3.5-ocr` [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。
- **图片生成与编辑**：`wan2.7-image-pro` 支持文生图（4096×4096）、多图参考编辑及角色一致性；`qwen-image-3.0-pro`（邀测中）支持负向提示词与多语言字体渲染 [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。
- **3D 生成**：Tripo 系列（`Tripo/Tripo-P1.0` / `Tripo/Tripo-H3.1`）支持文生3D、单图生3D、多图生3D三种模式，需在华北2（北京）地域使用 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。
- **语音与音频**：
  - 语音识别（ASR）：`fun-asr`（支持说话人分离）、`qwen3.5-omni-plus`（Prompt 上下文注入）、`qwen3-asr-flash`（情感识别）；
  - 语音合成（TTS）：`qwen-audio-3.0-tts-plus`（标准+复刻）、`cosyvoice-v3.5-plus`（设计+复刻）；
  - 语音转语音（S2S）：`qwen-audio-3.0-realtime-plus`（低延迟对话）、`qwen3.5-livetranslate-flash-realtime`（60语种实时翻译）；
  - 音乐生成：`fun-music-v1`（支持歌词/提示词/纯音乐/性别控制，邀测中）。
- **全模态理解**：`qwen3.5-omni-plus` 支持文本、音频、图片、视频四模态输入，具备 Function Calling、联网搜索、思考模式（HTTP 模式）及声音复刻能力 [原文标题](../../raw/model-user-guide/model-experience/omni.md)。
- **向量与重排序**：`text-embedding-v4`（文本嵌入，维度可配）、`qwen3-vl-embedding`（图文融合）、`qwen3-rerank`（文本重排序，支持 100+ 语言）。

> **注意**：文档 1 与文档 2 均将 `qwen3.7-plus` 列为视觉理解首选，但文档 2 明确指出其支持“最长2小时视频”，而文档 1 未提及视频能力——该差异源于文档 1 聚焦文本生成主场景，视觉能力属延伸支持，实际调用需以 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md) 的视觉专项说明为准。

## 关键参数

各模态模型共享部分通用参数，同时具备模态特有配置：

- **通用参数**：
  - `model`：必填，指定模型 ID（如 `qwen3.7-plus`、`wan2.7-image-pro`）；
  - `input`：结构化输入对象，内容依模态而异（文本、图片 URL、音频 base64、[prompt](prompt.md) 字符串等）；
  - `parameters`：控制生成行为（如 `texture_quality` 控制 Tripo 贴图质量，`format` 控制 Fun-Music 输出格式）；
  - `enable_thinking` / `reasoning.effort`：启用逐步推理（仅 Qwen3 及以上文本/全模态模型支持）。

- **模态特有参数示例**：
  - 视觉：`max_images`（最大图片数）、`max_videos`（最大视频数）；
  - 视频生成：`video_duration`（时长）、`resolution`（分辨率）；
  - TTS：`gender`（`fun-music-v1`）、`voice_id`（音色 ID）、`instruction`（指令控制）；
  - ASR：`hotwords`（热词）、`speaker_diarization`（说话人分离）；
  - S2S：`translate_to`（目标语言）、`output_audio_format`（语音格式）；
  - Embedding：`dimension`（向量维度，`text-embedding-v4` 支持 64–2048）。

## 使用方式

- **API 接入**：所有模型均通过统一 RESTful API 调用，端点为 `{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/{service}/{action}`（如 `/services/aigc/video-generation/3d-generation`）。需配置 `Authorization: Bearer $DASHSCOPE_API_KEY` 及 `Content-Type: application/json`。
- **协议选择**：
  - 实时交互（语音助手、直播翻译）：使用 WebSocket（如 `qwen-audio-3.0-realtime-plus`）；
  - 批处理（文件转写、批量图片生成）：使用 HTTP（如 `fun-asr`、`wan2.7-image-pro`）；
  - 异步任务（3D/视频生成）：启用 `X-DashScope-Async: enable`，通过 `task_id` 轮询结果 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。
- **SDK 支持**：Python/Java SDK 全面覆盖，部分模型（如 Fun-ASR、CosyVoice）额外支持 Android/iOS SDK。
- **输入规范**：
  - 图片：JPEG/PNG，单图 ≤ 20MB，分辨率 ≤ 1600 万像素；
  - 视频：MP4/WebM，≤ 2GB，时长依模型而定（`qwen3.7-plus` 支持 2 小时）；
  - 音频：WAV/MP3/FLAC，采样率 ≥ 8kHz，时长上限见各模型文档；
  - 文本：UTF-8 编码，长度受模型上下文限制（如 `qwen3.7-plus` 为 1M tokens）。

## 限制和注意事项

- **地域限制**：Tripo 3D 模型、Fun-Music 仅限华北2（北京）地域；部分模型（如 `qwen3.8-max-preview`）需 [Token](../concepts/token.md) Plan 订阅方可使用 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。
- **能力冲突**：Qwen3.5-Omni 的联网搜索与 Function Calling 不可同时启用；思考模式下不支持语音输出（仅文本）。
- **版本兼容性**：快照版本（如 `qwen3.7-plus-2026-05-26`）用于稳定性保障，但旧版模型（如 `qwen2.5-omni-7b`、`paraformer` 系列）已停止更新，新项目应避免使用 [原文标题](../../raw/model-user-guide/model-experience/omni.md)。
- **资源约束**：
  - 视频生成：`happyhorse-1.1-*` 系列最大时长 15 秒，`wan2.7-*` 系列为 10–15 秒；
  - 重排序：`qwen3-rerank` 最多处理 500 个文档，`qwen3-vl-rerank` 单条输入上限 8,000 tokens；
  - 多图输入：视觉模型 `qwen3.7-plus` 最多支持 2048 张图片，Tripo 多图生3D 限定 2–4 张。
- **计费差异**：Qwen3-TTS 系列（如 `qwen3-tts-flash`）按 token 计费；Fun-Music、Tripo 等按请求或时长计费；具体计费规则需查阅对应模型的定价页。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)


