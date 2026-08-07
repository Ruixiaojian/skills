# video generation api

百炼平台提供多种视频生成能力，覆盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、口型同步、动作迁移等场景。所有 API 均采用异步调用模式，需通过“创建任务 → 轮询获取结果”两步完成，任务 ID 有效期为 24 小时。调用前必须确保模型、Endpoint URL 与 API Key 属于同一地域，跨地域调用将失败。

## 支持的模型/功能

视频生成 API 支持以下主流模型及对应能力：

- **文生视频（T2V）**：`wan2.7-t2v`、`vidu/viduq3-turbo_text2video`、`pixverse/pixverse-c1-t2v`、`kling/kling-v3-video-generation`、`happyhorse-1.1-t2v`  
- **图生视频（I2V）**：  
  - 首帧：`wan2.7-i2v`、`vidu/viduq3-pro-fast_img2video`、`pixverse/pixverse-c1-it2v`、`happyhorse-1.1-i2v`  
  - 首尾帧：`wan2.2-kf2v-fla`（旧版）、`pixverse/pixverse-c1-kf2v`、`vidu/viduq3-turbo_start-end2video`  
- **参考生视频（R2V）**：`wan2.7-r2v`、`pixverse/pixverse-c1-r2v`、`vidu/viduq3-ad_reference2video`、`happyhorse-1.1-r2v`  
- **视频编辑**：`wan2.7-videoedit`、`happyhorse-1.1-videoedit`、`pixverse/pixverse-motioncontrol`、`pixverse/pixverse-lipsync`  
- **数字人与肖像动画**：`wan2.2-s2v`（说话/唱歌）、`emo-v1`（唱演）、`liveportrait`（播报）、`videoretalk`（口型替换）、`animate-anyone-gen2`（舞蹈）  
- **风格与后处理**：`video-style-transform`（8种艺术风格重绘）、`pixverse/pixverse-upscale`（4K超清）  

> **注意**：万相系列存在新旧协议并存现象。[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md) 明确指出“推荐优先选用 wan2.7”，而 [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md) 被标注为“仅支持首帧生视频”，且其请求路径为 `/api/v1/services/aigc/video-generation/video-synthesis`，与新版一致；但 [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md) 的请求路径为 `/api/v1/services/aigc/image2video/video-synthesis`，与其他模型不统一，开发者需特别注意路径差异。

## 关键参数

所有视频生成请求共用以下核心参数结构：

- **`model`**（必填）：模型标识符，如 `"wan2.7-t2v"`、`"pixverse/pixverse-c1-it2v"`。不同功能需匹配对应模型。
- **`input`**（必填）：输入内容容器，结构因模型而异：
  - 文生视频：`{"prompt": "文本描述"}`
  - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "文本描述"}`
  - 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "文本描述"}`
  - 参考生视频：`{"media": [{"type": "image_url", "url": "..."}, ...], "prompt": "场景描述"}`
  - 数字人：`{"image_url": "...", "audio_url": "..."}`（如 [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md) 所示）
- **`parameters`**（可选）：控制生成质量与输出格式：
  - `duration`: 视频时长（秒），常见值 `5` 或 `10`
  - `resolution`: 分辨率，如 `"720P"`、`"480P"`、`"540P"`
  - `size`: 具体像素尺寸，如 `"1280*720"`（PixVerse）、`"1024*576"`（Vidu）
  - `watermark`: 是否添加水印（`true`/`false`）
  - `aspect_ratio`: 宽高比（如 `"16:9"`，Vidu/Kling）
  - `style`: 风格类型（如 `video-style-transform` 中 `0` 表示日式漫画）

所有请求必须携带以下 HTTP 头：
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `Content-Type: application/json`
- `X-DashScope-Async: enable`

## 使用方式

1. **准备环境**：确认模型开通地域，获取该地域的 [API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，并配置至环境变量 `DASHSCOPE_API_KEY`；在控制台获取业务空间 ID（`{WorkspaceId}`）。
2. **构造请求**：使用对应地域的 Endpoint URL（推荐业务空间专属域名，如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），按模型要求组织 `model`、`input` 和 `parameters`。
3. **提交任务**：发送 `POST` 请求至 `/api/v1/services/aigc/video-generation/video-synthesis`（少数旧模型如 wan2.2-kf2v 使用 `/api/v1/services/aigc/image2video/video-synthesis`），获取 `task_id`。
4. **轮询结果**：使用 `task_id` 向 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（或业务空间域名对应路径）轮询，直至 `status` 为 `"SUCCESS"`，响应中 `output.video_url` 即为生成视频地址。

> **注意**：[HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md) 强调“请勿重复创建任务”，因 `task_id` 24 小时内有效，重复提交将导致资源浪费与状态混乱。

## 限制和注意事项

- **地域强绑定**：模型、API Key、Endpoint URL 必须同属一个地域（如华北2北京、新加坡、美国弗吉尼亚等），混用将直接报错。
- **异步时效性**：任务平均耗时 1–5 分钟，部分复杂任务（如万相2.1视频编辑）可达 5–10 分钟；`task_id` 仅保留 24 小时。
- **输入规范**：数字人类模型（如 `wan2.2-s2v`、`emo-v1`）需先调用检测接口（如 `wan2.2-s2v-detect`）验证图片合规性，否则生成失败。
- **URL 格式**：所有媒体资源（图片、视频、音频）必须为公网可访问的 HTTPS URL；部分模型（如 PixVerse）明确要求 `url` 字段，不支持 base64 内联。
- **计费与限流**：各模型独立计费（按秒/次），并发任务数受 QPS/RPS 限制（如 `liveportrait` 同时处理中任务数为 1），详情参见各模型文档的“资费与限流”章节。

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
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


