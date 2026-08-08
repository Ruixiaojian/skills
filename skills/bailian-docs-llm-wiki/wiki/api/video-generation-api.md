# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，包括文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、数字人生成、动作迁移、口型替换等。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果，任务有效期为 24 小时。统一使用 `/api/v1/services/aigc/video-generation/video-synthesis` 端点（部分旧版模型例外），且严格要求模型、Endpoint URL 与 API Key 必须同地域。

## 支持的模型/功能

API 支持三大类模型能力：

- **通用视频生成**：  
  - `wan3.0-video`（万相3.0）：All-in-One 模型，统一支持文生、图生（首帧/首尾帧）、参考生视频，最长 30 秒，当前处于邀测阶段 [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)。  
  - `kling/kling-v3-video-generation` 等可灵系列：支持文生视频、图生视频（首帧/首尾帧）、参考生视频及视频编辑 [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)。  
  - `vidu/viduq3-*`、`pixverse/pixverse-*` 系列：提供文生、图生（首帧/首尾帧）、参考生视频等标准化能力。

- **专业视频编辑与迁移**：  
  - 视频编辑（`wan2.7-videoedit`, `pixverse/pixverse-lipsync`, `pixverse/pixverse-motioncontrol`）；  
  - 风格重绘（`video-style-transform`）；  
  - 超清增强（`pixverse/pixverse-upscale`）；  
  - 口型替换（`videoretalk`, `pixverse/pixverse-lipsync`）。

- **人物驱动类模型**：  
  - 数字人生成：`wan2.2-s2v`（单图+音频）、`emo-v1`（悦动人像）、`liveportrait`（灵动人像）、`animate-anyone-gen2`（舞动人像）；  
  - 角色替换：`wan2.2-animate-mix`（视频换人）、`wan2.2-animate-move`（图生动作）；  
  - 表情包生成：`emoji` 模型。

> **注意**：万相 2.1–2.6 系列（如 `wan2.6`）与 2.7+ 系列存在协议差异：前者部分模型使用 `/api/v1/services/aigc/image2video/video-synthesis`（如文档35），后者统一使用 `/api/v1/services/aigc/video-generation/video-synthesis`。开发者应优先选用 2.7+ 或 wan3.0 新版模型，旧版文档已明确标注“推荐优先选用”[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。

## 关键参数

所有请求必须包含以下基础字段：

- `model`: 模型标识符（如 `"wan2.7-videoedit"`, `"vidu/viduq3-pro-fast_img2video"`），需与所选模型精确匹配；
- `input`: 包含输入内容，结构因模型而异：
  - 文生视频：`{"prompt": "..."}`；
  - 图生视频：`{"media": [{"type": "image", "url": "..."}], "prompt": "..."}`；
  - 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "..."}`；
  - 参考生视频：`{"media": [{"type": "reference_image", "url": "..."}, ...], "prompt": "..."}`；
  - 数字人：`{"image_url": "...", "audio_url": "..."}`（`wan2.2-s2v`）或 `{"image_url": "...", "audio_url": "...", "style_level": "active"}`（`emo-v1`）；
- `parameters`: 控制生成效果，常见字段包括：
  - `duration`: 视频时长（秒），范围通常为 3–10 秒（部分模型如 wan3.0 支持至 30 秒）；
  - `resolution` / `size`: 分辨率（如 `"720P"`, `"1280*720"`, `"3840×2160"`）；
  - `aspect_ratio`: 宽高比（如 `"16:9"`, `"1:1"`）；
  - `watermark`: 布尔值，控制是否添加水印；
  - `audio`: 布尔值，控制是否生成音频（部分模型默认关闭）；
  - `style`: 风格类型（如 `video-style-transform` 的 `0`–`7`）。

请求头必需包含：
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `X-DashScope-Async: enable`
- `Content-Type: application/json`

## 使用方式

1. **准备环境**：确保模型、Endpoint URL 与 API Key 同地域；推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com` [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)。  
2. **创建任务**：`POST` 到对应地域的 `/api/v1/services/aigc/video-generation/video-synthesis`（或旧版 `/image2video/`），传入完整 JSON 请求体，获取 `task_id`。  
3. **轮询结果**：使用 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（或业务空间专属域名）查询状态，直至 `status` 为 `"SUCCESS"`，响应中 `output.video_url` 即为生成视频地址。  
4. **错误处理**：检查 `status` 字段（`"QUEUED"`/`"PROCESSING"`/`"SUCCESS"`/`"FAILED"`），失败时查看 `message` 字段定位原因（如 `invalid input`, `quota exceeded`）。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint、API Key 必须同地域，跨地域调用必然失败（所有文档均强调此前提）。  
- **异步时效性**：`task_id` 有效期为 24 小时，超时需重新提交任务；轮询间隔建议 ≥3 秒，避免触发限流。  
- **输入约束**：  
  - 图片/视频 URL 必须公网可访问、HTTPS 协议、文件大小符合模型要求（如万相系列建议 ≤10MB）；  
  - `prompt` 长度通常限制在 512 字符内，避免敏感/违规内容；  
  - 数字人类模型（如 `emo-v1`, `liveportrait`）需先调用 `detect` 模型校验图片合规性。  
- **计费与限流**：各模型独立计费（按秒/次），QPS/RPS 限制因模型而异（如 `videoretalk` 为 1 RPS），详见各模型资费文档。  
- **URL 差异**：注意区分新版统一端点 `/video-generation/` 与旧版 `/image2video/`（文档10、11、35），混用将导致 404 错误。

## 来源文档

- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)


