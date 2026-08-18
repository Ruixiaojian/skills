# model experience

`model experience` 是百炼平台面向开发者提供的模型能力总览与选型指南，覆盖文本、视觉、语音、音视频、音乐、向量等全模态模型。本文档聚焦核心能力、关键参数与使用约束，帮助开发者快速匹配业务场景与最优模型，避免通用性描述与营销话术。

## 支持的模型/功能

百炼提供覆盖多模态的模型矩阵，按能力层级与场景细分：

- **文本生成**：以 `qwen3.8-max`（高能力）、`qwen3.7-plus`（平衡）、`qwen3.7-flash`（轻量）为核心，支持 1M 上下文、Function Calling、内置工具（联网搜索/代码执行）及结构化 JSON 输出 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。办公场景推荐 `qwen3.7-plus`；超长文档处理需 `qwen-long`（10M 上下文）；AI 编程优先 `qwen3.7-plus` 或 `qwen3.8-max`。
  
- **视觉理解**：`qwen3.7-plus` 和 `qwen3.7-flash` 支持图像（最高 1600 万像素）、视频（最长 2 小时/2GB）、OCR（专用 `qwen3.5-ocr`）及结构化输出 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。Function Calling 与内置工具在 `qwen3.7-plus`、`qwen3.6-plus` 及后续版本中全面支持。

- **图片生成与编辑**：`qwen-image-3.0-pro` 适用于复杂版面与小字渲染；`wan2.7-image-pro` 支持品牌色控制与 4096×4096 分辨率；`z-image-turbo` 侧重速度与成本，但不支持编辑功能 [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。

- **视频生成与编辑**：`happyhorse-1.1-t2v` 用于文生视频（1080P，3–15 秒）；`wan2.7-i2v-2026-04-25` 支持首尾帧续写；`wan2.2-animate-move` 实现动作迁移 [原文标题](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)。

- **语音相关**：
  - 合成（TTS）：`qwen-audio-3.0-tts-plus` 支持声音复刻与指令控制；`cosyvoice-v3.5-plus` 支持 SSML 与 LaTeX 公式朗读 [原文标题](../../raw/model-user-guide/model-experience/tts-model.md)。
  - 识别（ASR）：实时场景用 `qwen-audio-3.0-asr-flash-streaming`；非实时文件转写用 `qwen-audio-3.0-asr-flash-filetrans`（支持说话人分离）[原文标题](../../raw/model-user-guide/model-experience/asr-model.md)。
  - 语音转语音（S2S）：`qwen-audio-3.0-realtime-plus` 用于低延迟对话；`qwen3.5-omni-flash` 支持 Function Calling 与联网搜索 [原文标题](../../raw/model-user-guide/model-experience/s2s-model.md)。

- **全模态与翻译**：`qwen3.5-omni-plus` 是旗舰全模态模型，支持文本/音频/图片/视频输入，具备联网搜索、Function Calling 及深度推理能力；`qwen3.5-livetranslate-flash-realtime` 支持 60 种语言实时语音翻译 [原文标题](../../raw/model-user-guide/model-experience/omni.md)。

- **向量与重排序**：`text-embedding-v4` 为文本 Embedding 默认推荐；跨模态检索用 `qwen3-vl-embedding`（融合向量）或 `tongyi-embedding-vision-plus`（独立向量）；RAG 精排推荐 `qwen3-rerank`（纯文本）或 `qwen3-vl-rerank`（多模态）[原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

- **3D 与音乐**：Tripo 模型（`Tripo/Tripo-P1.0` / `Tripo/Tripo-H3.1`）仅限华北2（北京）地域调用，需异步轮询获取 GLB 结果 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)；Fun-Music（`fun-music-v1`）处于邀测阶段，仅支持北京地域，需申请开通 [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。

> **注意**：文档 1 和文档 2 中对 `qwen3.7-plus` 是否支持“思考模式”的描述存在矛盾——文档 1 未提及该能力，而文档 2 明确其支持。依据文档 2 的“推荐模型”表格及“思考模式”章节，`qwen3.7-plus` 及更高版本均支持 `enable_thinking` 参数，此为权威表述。

## 关键参数

- **上下文窗口**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.7-flash` 等主流文本模型统一为 1M Token；`qwen-long` 达 10M；旧版 `qwen3.5-397b-a17b` 等仅 256k。
- **输入限制**：
  - 图像：单图最高 1600 万像素，Token 数 = `h × w / (32 × 32) + 2`；
  - 视频：`qwen3.7-plus` 支持最长 2 小时/2GB；`qwen3-vl-plus` 限 1 小时/2GB；
  - 音频：ASR `qwen-audio-3.0-asr-flash-filetrans` 支持最大 12 小时/2GB；TTS 输入文本长度依模型而定，Qwen-Audio-TTS 系列无硬性上限。
- **输出控制**：
  - TTS：通过 `qwen-audio-3.0-tts-plus` 的自然语言指令（如“温柔语气，语速稍慢”）动态调节表达；
  - S2S：`qwen3.5-omni-flash` 在 HTTP 模式下支持思考模式，但**思考模式下不支持生成语音**；
  - Tripo：`parameters.texture_quality` 控制贴图（`standard`/`detailed`），`parameters.geometry_quality`（仅 H3.1）控制面数（`standard`/`ultra`）。
- **多模态输入**：`qwen3.5-omni-plus` 支持文本+音频+图片+视频混合输入；`qwen3.7-plus` 仅支持文本+图像+视频（不含音频）。

## 使用方式

- **API 调用**：所有模型均通过 DashScope API 接入，需配置 `DASHSCOPE_API_KEY` 环境变量。HTTP 请求需设置 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`。
- **协议选择**：
  - 实时交互（语音助手、直播字幕）：优先 WebSocket（如 `qwen-audio-3.0-asr-flash-streaming`、`qwen-audio-3.0-realtime-plus`）；
  - 批量/离线任务（视频分析、播客翻译）：使用 HTTP（如 `qwen3.5-omni-flash`、`qwen3-livetranslate-flash`）；
  - 异步长耗时任务（3D 生成、音乐生成）：必须轮询 `task_id`，有效期 24 小时。
- **SDK 支持**：Qwen-Audio、Fun-ASR、Qwen-Audio-Realtime 等系列支持 DashScope Python/Java SDK；CosyVoice 还支持 Android/iOS SDK；Tripo 和 Fun-Music 仅提供 RESTful API。
- **地域限制**：Tripo 模型和 Fun-Music **仅支持华北2（北京）地域**，调用 endpoint 必须为 `cn-beijing.maas.aliyuncs.com`；其他模型默认支持多地域，但部分快照版本（如 `qwen3.7-plus-2026-05-26`）可能有地域部署差异。

## 限制和注意事项

- **功能互斥性**：S2S 模型中，`qwen3.5-omni-flash` 的联网搜索与 Function Calling **不可同时开启**；思考模式仅在 HTTP 模式下可用，且禁用语音输出。
- **模型弃用**：`qwen-omni-turbo`、`qwen-vl-max`、`qwen2.5-omni-7b` 等旧版模型已停止更新，新项目应使用 `qwen3.5-omni-plus` 或 `qwen3.5-ocr` 等对应新版 [原文标题](../../raw/model-user-guide/model-experience/omni.md)。
- **音频格式与语言**：TTS `cosyvoice-v3.5-plus` 不支持系统音色，仅通过声音复刻/设计生成；ASR `qwen-audio-3.0-asr-flash` 支持超百种方言口音，但 `fun-asr-flash-8k-realtime` 仅支持中文。
- **成本与性能权衡**：`qwen3.7-flash` 在效果接近 `qwen3.7-plus` 的前提下显著降低成本，但图片数上限为 256（`qwen3.7-plus` 为 2048）；`z-image-turbo` 生成速度快 10 倍、价格约 1/5，但不支持编辑功能。
- **安全与合规**：Tripo 和 Fun-Music 均需单独申请开通权限；所有模型调用需遵守阿里云《AI 服务内容安全规范》，禁止生成违法、侵权或歧视性内容。

## 来源文档

- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)


