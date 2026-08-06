# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，包括文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、数字人生成、动作迁移、口型替换等。所有接口均采用异步调用模式，需先创建任务获取 `task_id`，再轮询查询结果。核心服务由 HappyHorse、万相（WanX）、爱诗（PixVerse）、可灵（Kling）、Vidu 等模型提供，支持多地域部署与业务空间专属域名。

## 支持的模型/功能

API 覆盖以下主流视频生成范式：

- **文生视频（T2V）**：输入文本提示词生成视频，支持 HappyHorse、万相2.7/3.0、爱诗、可灵、Vidu 等模型 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)。
- **图生视频（I2V）**：基于单张首帧图像生成视频（如万相2.7、HappyHorse、爱诗、Vidu），或基于首尾帧图像生成平滑过渡视频（如爱诗、Vidu、万相2.2）。
- **参考生视频（R2V）**：传入多张参考图像（或图像+视频），结合文本描述融合生成角色一致的视频，支持万相2.7、HappyHorse、爱诗、Vidu 等模型 [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)。
- **视频编辑与增强**：包括风格迁移（如视频风格重绘）、超分（爱诗-视频超清）、动作模仿（爱诗-视频动作模仿）、口型同步（爱诗-视频对口型、声动人像VideoRetalk）、换人（万相-视频换人）、数字人生成（万相-数字人、悦动人像EMO、灵动人像LivePortrait）等。
- **专用动画生成**：图生动作（万相-图生动作）、舞动人像（AnimateAnyone）、表情包视频（Emoji）等垂直场景模型。

> **注意**：万相系列存在新旧协议并存现象。万相2.7 及以上模型使用 `/api/v1/services/aigc/video-generation/video-synthesis` 统一路径；而万相2.1–2.6 的部分旧版模型（如文档31–35）仍使用 `/api/v1/services/aigc/image2video/video-synthesis` 或不同参数结构，[万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md) 明确标注其为“仅支持首帧生视频”的旧版方案，开发者应优先选用万相2.7+ 新协议。

## 关键参数

所有请求需包含以下基础要素：

- **HTTP 方法与 Headers**：`POST` 请求，必需 `Content-Type: application/json` 和 `X-DashScope-Async: enable`，`Authorization: Bearer $DASHSCOPE_API_KEY` 用于鉴权。
- **模型标识（`model`）**：必须指定具体模型名，如 `"wan2.7-video"`、`"pixverse/pixverse-c1-t2v"`、`"vidu/viduq3-turbo_text2video"`。不同功能对应不同模型，不可混用。
- **输入数据（`input`）**：
  - 文生视频：`{"prompt": "..."}`；
  - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`；
  - 首尾帧：`{"media": [{"type": "first_frame", ...}, {"type": "last_frame", ...}], "prompt": "..."}`；
  - 参考生视频：`{"media": [{"type": "image_url", ...}, ...], "prompt": "..."}`；
  - 数字人：`{"image_url": "...", "audio_url": "..."}`（万相-数字人）；
  - 视频编辑：`{"media": [{"type": "video", "url": "..."}], "prompt": "..."}`。
- **参数配置（`parameters`）**：常见字段包括：
  - `duration`: 视频时长（秒），范围通常为 2–30 秒；
  - `resolution` / `size`: 分辨率（如 `"720P"`、`"1280*720"`）；
  - `aspect_ratio`: 宽高比（如 `"16:9"`）；
  - `watermark`: 是否添加水印（布尔值）；
  - `audio`: 是否生成音频（部分模型支持）；
  - `style`, `mode`, `seed` 等模型特有参数需查阅对应文档。

## 使用方式

1. **环境准备**：确保模型、Endpoint URL 与 API Key 属于同一地域；推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）替代旧版 `dashscope.aliyuncs.com`，以获得更高性能与稳定性。
2. **创建任务**：向对应地域的 Endpoint 发送 `POST /api/v1/services/aigc/video-generation/video-synthesis` 请求，携带完整 `model`、`input` 和 `parameters`。成功响应返回 `task_id`（有效期 24 小时）。
3. **轮询结果**：使用 `GET https://<base-url>/api/v1/tasks/{task_id}` 查询任务状态（`status: "SUCCESS"` 表示完成），响应中 `output.video_url` 为生成视频地址。
4. **错误处理**：关注 HTTP 状态码（如 401 鉴权失败、400 参数错误）及响应体中的 `code` 与 `message` 字段；避免重复提交相同任务。

## 限制和注意事项

- **地域强绑定**：模型、API Key、Endpoint URL 必须同属一个地域（如华北2北京、新加坡等），跨地域调用必然失败，且不同地域的 API Key 不可复用。
- **异步时效性**：任务处理耗时通常为 1–5 分钟（部分复杂任务如视频编辑可达 10 分钟），需实现健壮的轮询逻辑（建议间隔 ≥5 秒，最大重试次数 ≥12 次）。
- **资源约束**：各模型有独立的 QPS/RPS 限流与并发任务数限制（如万相-数字人同时处理中任务上限为 100 秒，VideoRetalk 为 1 个），超出将返回限流错误。
- **输入要求**：图像需清晰、正面、主体居中；视频需画面稳定、人声清晰；URL 必须可公开访问且 HTTPS 协议；文件大小受后端限制（通常 ≤200MB）。
- **模型兼容性**：新版协议（万相2.7+、HappyHorse、爱诗、Vidu、可灵）统一使用 `/video-synthesis` 路径；旧版万相2.1–2.6 模型部分使用 `/image2video/video-synthesis`，参数结构亦不兼容，迁移时需重构请求体。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


