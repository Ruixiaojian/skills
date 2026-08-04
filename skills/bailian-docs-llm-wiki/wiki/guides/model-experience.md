# model experience

`model experience` 是百炼平台面向开发者提供的多模态模型能力总览，涵盖视觉理解、音视频生成与编辑、语音处理、3D建模、音乐生成及向量检索等核心场景。本文档结构化梳理各能力域的模型选型逻辑、关键参数与使用约束，帮助开发者快速匹配业务需求与最优模型，避免因版本混用或能力误判导致的集成问题。

## 支持的模型/功能

百炼提供覆盖文本、图像、视频、音频、3D和向量六大模态的模型能力，按场景分类如下：

- **视觉理解**：支持图像分析、OCR、视频理解及结构化输出。旗舰模型 `qwen3.7-plus` 支持1M上下文、2小时视频输入、Function Calling 和内置工具（联网搜索、代码执行）；`qwen3.5-ocr` 专为文档/手写体文字提取优化 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。
- **视频生成与编辑**：包括文生视频（`happyhorse-1.1-t2v`）、图生视频（`wan2.7-i2v-2026-04-25`）、参考生视频（`happyhorse-1.1-r2v`）及视频编辑（`wan2.7-videoedit`）。所有模型输出为 MP4，帧率 24–30 fps，单片段最长 15 秒 [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)。
- **图片生成与编辑**：`qwen-image-3.0-pro` 支持复杂版面与小字渲染；`wan2.7-image-pro` 支持 4096×4096 文生图及多图参考编辑；`z-image-turbo` 仅支持文生图，速度提升 10 倍，成本约为 1/5 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)。
- **3D模型生成**：Tripo 系列（`Tripo/Tripo-P1.0`、`Tripo/Tripo-H3.1`）支持文生3D、单图生3D、多图生3D三种模式，仅限华北2（北京）地域，需配置对应地域 API Key [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。
- **语音处理**：
  - **TTS**：`qwen-audio-3.0-tts-plus` 支持声音复刻与指令控制（如“温柔语速稍慢”）；`cosyvoice-v3.5-plus` 同时支持声音复刻与声音设计 [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)。
  - **ASR**：`qwen-audio-3.0-asr-flash-streaming` 用于实时识别（WebSocket），`qwen-audio-3.0-asr-flash-filetrans` 用于非实时文件转写（HTTP），均支持热词与 Prompt 上下文注入 [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)。
  - **S2S（语音转语音）**：`qwen-audio-3.0-realtime-plus` 支持端到端低延迟对话；`qwen3.5-livetranslate-flash-realtime` 支持 60 种语言实时翻译 [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)。
- **音乐生成**：`fun-music-v1` 支持 [prompt](prompt.md) 或 lyrics 输入生成带人声歌曲，`fun-music-preview` 仅支持 [prompt](prompt.md) 且不支持 `gender` 参数；两者均需申请邀测权限，仅限华北2（北京）地域 [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)。
- **向量与重排序**：`text-embedding-v4` 为通用文本 Embedding 默认推荐；`qwen3-vl-embedding` 适用于图文混合检索；`qwen3-rerank` 支持最多 500 条文本重排序 [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

> **注意**：文档 8 与文档 9 对 `qwen3.5-omni-flash` 的联网搜索支持描述存在矛盾——文档 8 明确标注其支持联网搜索，而文档 9 的表格中该能力为“支持”，但下方说明又指出“Qwen3-Omni-Flash 不支持此功能”。经交叉核对，以文档 8 为准：`qwen3.5-omni-flash`（HTTP/WebSocket）**支持联网搜索**；`qwen3-omni-flash`（HTTP）不支持。

## 关键参数

各模态模型的关键参数需按场景显式配置，常见参数如下：

- **视觉模型**：
  - 图像分辨率：[Token](../concepts/token.md) 消耗公式为 `h × w / (32 × 32) + 2`，单图最高 1600 万像素。
  - 视频限制：`qwen3.7-plus` 等主流模型支持最长 2 小时 / 2GB；`qwen3-vl-plus` 仅支持 1 小时 / 2GB。
  - 结构化输出：需在请求中声明 `response_format={"type": "json_object"}`，仅 Qwen3.5+ 及 Qwen3-VL 系列支持。

- **视频/图片生成**：
  - 输出分辨率与时长：`happyhorse-1.1-t2v` 支持 1080P/15 秒；`wan2.7-i2v-2026-04-25` 支持 1080P/15 秒；`qwen-image-3.0-pro` 最大输出 2048×2048，`wan2.7-image-pro` 文生图支持 4096×4096。
  - 多图输入：`wan2.7-image-pro` 编辑支持最多 9 张输入图；Tripo 多图生3D要求 2–4 张多角度 PNG/JPEG（≤20MB）。

- **语音模型**：
  - ASR 音频规格：`qwen-audio-3.0-asr-flash-filetrans` 支持最大 12 小时 / 2GB；`qwen-audio-3.0-asr-flash` 仅支持 5 分钟 / 2GB。
  - TTS 格式与控制：通过 `format=mp3/wav` 指定输出；指令控制需在 `input.text` 中嵌入自然语言描述（如“用激动的播报风格”）。

- **3D 与音乐**：
  - Tripo：`parameters.texture_quality` 控制贴图（`standard`/`detailed`），`parameters.geometry_quality`（仅 H3.1）控制面数（`standard`/`ultra`）。
  - Fun-Music：`is_instrumental=true` 生成纯音乐；`gender=female/male`（仅 v1）指定人声性别；`lyrics` 与 `prompt` 互斥，同时传入时 `lyrics` 优先。

- **向量模型**：
  - `text-embedding-v4` 维度可选 64–2048（默认 1024）；`qwen3-vl-embedding` 默认 2560 维，最大 [Token](../concepts/token.md) 数 32,000；重排序模型 `qwen3-rerank` 单次最多处理 500 条文本，每条上限 4,000 tokens。

## 使用方式

- **API 调用统一路径**：所有模型均通过 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/{service}/{endpoint}` 接入，其中 `service` 为 `aigc/video-generation`（视频）、`audio/music/generation`（音乐）等，`endpoint` 因模型而异（如 `/3d-generation`、`/generation`）。
- **认证方式**：必须配置 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 需在对应地域控制台获取并设为环境变量。
- **[异步任务](../concepts/asynchronous-task.md)**：Tripo 3D 生成、部分视频生成需先调用创建任务接口（含 `X-DashScope-Async: enable` header），再轮询 `GET /api/v1/tasks/{task_id}` 获取结果，有效期 24 小时。
- **协议选择**：
  - 实时交互（语音助手、直播翻译）：优先使用 WebSocket（如 `qwen-audio-3.0-realtime-plus`）。
  - 批处理（文件转写、视频分析）：使用 HTTP（如 `qwen-audio-3.0-asr-flash-filetrans`）。
  - [流式输出](../concepts/streaming-output.md)：TTS/ASR 的 HTTP 接口支持 `Transfer-Encoding: chunked` 流式响应。

## 限制和注意事项

- **地域限制**：Tripo 3D 生成、Fun-Music 仅支持华北2（北京）地域；部分 Wan 视频模型（如 `wan2.6-t2v-us`）明确标注适用于美国部署范围 [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。
- **输入互斥性**：Tripo 的 `prompt`/`image`/`images` 字段三选一；Fun-Music 的 `prompt` 与 `lyrics` 不能共存；Qwen3.5-Omni 的联网搜索与 Function Calling 不可同时启用。
- **旧版模型弃用**：Qwen3.5 以下系列（如 `qwen-vl-max`）、Paraformer ASR、`qwen-omni-turbo` 等已标注“不再更新”，新项目应选用 Qwen3.6+ 或对应 Omni/Livetranslate 系列 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。
- **资源约束**：
  - 视频生成：`happyhorse-1.1-*` 系列单请求最多 15 秒，`wan2.7-*` 系列最长 15 秒（t2v/i2v）或 10 秒（r2v/videoedit）。
  - 3D 输出：`pbr_model_url` 与 `rendered_image_url` 链接有效期仅 2 小时，需及时下载。
  - 重排序：`qwen3-rerank` 单次请求文档数上限 500，超限将报错。
- **功能兼容性**：Qwen-Audio Realtime 系列不支持联网搜索与思考模式；Qwen3-Omni-Flash 不支持联网搜索；`qwen3.5-omni-flash-realtime` 不支持思考模式（仅 HTTP 模式支持）[全模态](../../raw/model-user-guide/model-experience/omni.md)。

## 来源文档

- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)


