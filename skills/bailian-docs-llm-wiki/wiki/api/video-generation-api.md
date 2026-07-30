# video generation api

百炼平台提供多种视频生成能力，覆盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、口型替换、风格重绘及数字人驱动等场景。所有 API 均采用异步调用模式，需通过“创建任务 → 轮询结果”两步完成，任务 ID 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

视频生成 API 按输入模态和任务类型分为以下几类：

- **文生视频（T2V）**：支持 `wan2.7-t2v`、`vidu/viduq3-turbo_text2video`、`pixverse/pixverse-c1-t2v`、`kling/kling-v3-video-generation` 等模型，可生成单镜头或多镜头叙事视频（如分镜描述、时间戳控制）[原文标题](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)。  
- **图生视频（I2V）**：包括基于首帧（`happyhorse-1.1-t2`、`wan2.7-i2v`、`vidu/viduq3-pro-fast_img2video`）、首尾帧（`pixverse/pixverse-c1-kf2v`、`vidu/viduq3-turbo_start-end2video`）及视频续写能力；万相2.7已统一为[多模态](../concepts/multi-modal.md)输入接口 [原文标题](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。  
- **参考生视频（R2V）**：支持传入多张图像（`happyhorse-reference-to-video`、`wan2.7-r2v`、`pixverse/pixverse-c1-r2v`、`vidu/viduq3-ad_reference2video`），融合角色生成场景化视频；部分模型支持图像+视频+音频混合参考。  
- **视频编辑与增强**：涵盖指令编辑（`wan2.7-videoedit`）、风格重绘（`video-style-transform`）、动作模仿（`pixverse/pixverse-motioncontrol`）、视频换人（`wan2.2-animate-mix`）、视频超清（`pixverse/pixverse-upscale`）等。  
- **人物驱动类**：面向肖像的专用模型，包括舞动人像（`animate-anyone-gen2`）、悦动人像（`emo-v1`）、灵动人像（`liveportrait`）、声动人像（`videoretalk`）、数字人（`wan2.2-s2v`）及表情包（`emoji`），均需前置图像检测（如 `emo-detect-v1`）[原文标题](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)。  

> **注意**：文档中存在新旧协议并存现象。万相系列明确区分 `wan2.7`（新版 `/api/v1/services/aigc/video-generation/video-synthesis`）与 `wan2.6` 及更早版本（旧版 `/api/v1/services/aigc/image2video/video-synthesis` 或 `video-generation/video-synthesis`，见文档30–34）。例如，`wan2.2-kf2v-fla`（文档33）使用 `image2video` 路径，而 `wan2.7-r2v`（文档13）统一使用 `video-generation` 路径。开发者应以模型命名（如含 `2.7`）和文档标题中的“新版协议”为准，避免路径误用。

## 关键参数

所有请求必须包含以下基础参数：

- **`model`**（必填）：模型标识符，格式如 `wan2.7-t2v-2026-06-12`、`vidu/viduq3-turbo_text2video`、`pixverse/pixverse-lipsync`。不同模型支持的参数集差异较大，需查阅对应文档。
- **`input`**（必填）：定义输入内容。常见结构：
  - 文生视频：`{"prompt": "..."}`；
  - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`；
  - 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "..."}`；
  - 视频编辑/对口型：`{"media": [{"type": "video_url", "url": "..."}, {"type": "audio_url", "url": "..."}]}`。
- **`parameters`**（可选）：控制生成质量与输出格式，常用字段：
  - `duration`: 视频时长（秒），通常为 2–5 秒；
  - `resolution` / `size`: 分辨率，如 `"720P"`、`"1280*720"`、`"1024*576"`；
  - `watermark`: 布尔值，是否添加水印（默认 `true`）；
  - `aspect_ratio`: 宽高比，如 `"16:9"`（Kling）；
  - `mode`: 模式选择，如 `"std"`（Kling）；
  - `style_level`: 动作风格强度（EMO 模型支持 `"active"`/`"normal"`/`"calm"`）。

请求头（Headers）必须包含：
- `Content-Type: application/json`
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `X-DashScope-Async: enable`（**必须**，同步调用不支持）

## 使用方式

1. **环境准备**：在阿里云百炼控制台开通对应模型服务，获取所属地域的 API Key，并配置为环境变量 `DASHSCOPE_API_KEY`；确认业务空间 ID（WorkspaceId）[原文标题](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。  
2. **构造请求**：使用地域专属 Endpoint（推荐 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），POST 到 `/api/v1/services/aigc/video-generation/video-synthesis`（万相2.7、HappyHorse、PixVerse、Vidu、Kling 等主流模型均统一此路径；仅部分 legacy 模型如 `wan2.2-kf2v` 使用 `image2video` 路径）。  
3. **轮询结果**：从响应中提取 `task_id`，通过 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（或带 WorkspaceId 的域名）轮询状态，直至 `status` 为 `"SUCCESS"`，返回 `output.video_url`。  
4. **错误处理**：关注 `task_status` 字段（如 `"FAILED"`）、`error_code`（如 `InvalidParameter`）及 `error_message`，常见错误包括地域不匹配、URL 不可达、提示词违规等。

## 限制和注意事项

- **地域强绑定**：模型、API Key、Endpoint URL 必须同属一个地域（如华北2北京、新加坡），混用将导致鉴权失败或 404 错误。  
- **异步时效性**：任务最长等待约 5–10 分钟（视频编辑类耗时更长），`task_id` 仅 24 小时有效，超时需重提任务。  
- **输入约束**：  
  - 图像 URL 需公网可访问、格式为 JPG/PNG/WebP，尺寸建议 ≥512×512；  
  - 视频 URL 需为 MP4/H.264 编码，时长 ≤30 秒；  
  - 音频需为 WAV/MP3，采样率 ≥16kHz，人声清晰无背景噪音。  
- **计费与限流**：各模型独立计费（按秒/张/次），QPS/RPS 限制严格（如 `emo-v1` 同时处理中任务数为 1），详见各模型资费文档；免费额度有限（如 `emo-detect-v1` 免费 200 张）。  
- **模型兼容性**：`wan2.7` 系列为当前主力，旧版 `wan2.6` 及更早模型（文档30–34）已标记为 Legacy，官方推荐迁移；HappyHorse、PixVerse、Vidu、Kling 等均为独立演进模型线，不互通。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


