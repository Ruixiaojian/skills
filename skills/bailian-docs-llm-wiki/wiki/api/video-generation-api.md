# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，涵盖文生视频（T2V）、图生视频（I2V）、参考生视频（R2V）、视频编辑、动作迁移、口型同步等场景。所有接口均采用异步调用模式，通过 `task_id` 轮询获取结果，任务有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格同地域部署，跨地域调用将失败。

## 支持的模型/功能

API 支持多系列模型，按能力划分如下：

- **文生视频（T2V）**：`happyhorse-1.1-t2v`、`wan2.7-t2v-2026-06-12`、`pixverse/pixverse-c1-t2v`、`kling/kling-v3-video-generation`、`vidu/viduq3-turbo_text2video`  
- **图生视频（I2V）**：  
  - 基于首帧：`happyhorse-1.1-i2v`、`wan2.7-i2v`（新版）、`wan2.6-i2v`（旧版，见 [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)）  
  - 基于首尾帧：`pixverse/pixverse-c1-kf2v`、`vidu/viduq3-turbo_start-end2video`、`wan2.2-kf2v-fla`（旧版，见 [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)）  
- **参考生视频（R2V）**：`happyhorse-1.1-r2v`、`wan2.7-r2v-2026-06-12`、`pixverse/pixverse-c1-r2v`、`vidu/viduq3-ad_reference2video`  
- **视频编辑类**：`happyhorse-1.0-video-edit`、`wan2.7-videoedit`、`pixverse/pixverse-lipsync`、`pixverse/pixverse-upscale`、`pixverse/pixverse-motioncontrol`  
- **人物动画类**（独立路径）：`wan2.2-s2v`（数字人）、`liveportrait`、`emo-v1`、`videoretalk`、`animate-anyone-gen2` 等，其 Endpoint 为 `/api/v1/services/aigc/image2video/video-synthesis` 或专用路径，与主 `video-synthesis` 接口分离。  

> **注意**：万相 2.7 系列（如 `wan2.7-i2v`）已统一支持首帧、首尾帧、视频续写三大任务，而旧版 `wan2.6` 及更早模型仅支持单一任务类型；新老协议共存，但推荐优先选用 2.7 新版 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。

## 关键参数

所有请求必须包含以下基础字段：

- `model`：模型标识符（如 `wan2.7-t2v-2026-06-12`），需与所选地域模型市场中开通的模型完全一致  
- `input.prompt`：文本提示词（T2V/R2V 必填；I2V/KF2V 建议提供以控制语义）  
- `input.media`：多模态输入数组，每项含 `type`（`image_url`/`first_frame`/`last_frame`/`video_url`/`audio_url`/`reference_image` 等）和 `url`（公网可访问 HTTPS 地址）  
- `parameters`（可选）：常见字段包括  
  - `resolution` / `size`：如 `"720P"`、`"1280*720"`、`"1024*576"`  
  - `duration`：视频时长（秒），通常取值 `2–5`  
  - `watermark`：布尔值，控制是否添加水印（默认 `true`）  
  - `aspect_ratio`（Kling）：如 `"16:9"`  
  - `style`（风格重绘）：整数索引（0–7）对应预设艺术风格  

请求头必需包含：  
- `Authorization: Bearer $DASHSCOPE_API_KEY`  
- `Content-Type: application/json`  
- `X-DashScope-Async: enable`（**必须显式设置**，否则返回“不支持同步调用”错误）

## 使用方式

1. **准备环境**：在百炼控制台开通目标模型 → 获取对应地域的 API Key → 配置为环境变量 `DASHSCOPE_API_KEY` → 获取业务空间 ID（`WorkspaceId`）  
2. **构造请求 URL**：使用业务空间专属域名（推荐）：  
   `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`  
   （其他地域替换 `cn-beijing` 为 `ap-southeast-1`/`eu-central-1` 等）  
3. **发起[异步任务](../concepts/asynchronous-task.md)**：`POST` 请求提交任务，获取 `task_id`  
4. **轮询结果**：使用 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态（旧版 SDK 可能需拼接 WorkspaceId，详见 [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)）  

> **注意**：部分模型（如 `wan2.2-s2v`、`liveportrait`、`emo-v1`）需先调用检测模型（`-detect`）验证输入合规性，再提交生成任务，流程为两步串联，不可跳过检测 [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)。

## 限制和注意事项

- **地域强绑定**：模型、API Key、Endpoint URL 必须同属一个地域（如华北2），混用将导致鉴权失败或 `401` 错误  
- **URL 规范**：所有 `media.url` 必须为公网可访问的 HTTPS 链接；本地文件需先上传至 OSS 或 CDN  
- **任务生命周期**：`task_id` 有效期为 24 小时，超时后无法查询结果；禁止重复提交相同任务  
- **并发限制**：多数模型 QPS 限流为 1–5（如 `videoretalk`、`emo-v1` 同时处理中任务数为 1），详见各模型资费文档  
- **路径差异**：  
  - 主视频生成接口路径为 `/api/v1/services/aigc/video-generation/video-synthesis`  
  - 部分人物动画模型（如 `wan2.2-animate-move`、`wan2.2-animate-mix`）使用 `/api/v1/services/aigc/image2video/video-synthesis`，路径不同，不可混用  
- **弃用警告**：`wan2.1`/`wan2.2`/`wan2.5`/`wan2.6` 等旧版模型仍可用，但功能受限且不再迭代；新项目应优先选用 `wan2.7`、`HappyHorse 1.1`、`Vidu` 或 `Kling` 等新版模型

## 来源文档

- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


