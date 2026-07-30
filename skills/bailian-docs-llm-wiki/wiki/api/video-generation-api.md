# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，包括文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、风格重绘、口型同步等。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果，任务 ID 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格同地域，跨地域调用将失败 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。

## 支持的模型/功能

API 支持多系列模型，按能力划分如下：

- **文生视频（T2V）**：`happyhorse-1.1-t2v`、`wan2.7-t2v-*`、`pixverse-c1-t2v`、`vidu/viduq3-turbo_text2video`、`kling/kling-v3-video-generation`  
- **图生视频（I2V）**：  
  - 首帧：`happyhorse-1.1-i2v`、`wan2.7-i2v`、`pixverse-c1-it2v`、`vidu/viduq3-pro-fast_img2video`  
  - 首尾帧：`pixverse-c1-kf2v`、`vidu/viduq3-turbo_start-end2video`、`wan2.2-kf2v-fla`（旧版）  
- **参考生视频（R2V）**：`happyhorse-r2v`、`wan2.7-r2v-*`、`pixverse-c1-r2v`、`vidu/viduq3-ad_reference2video`  
- **视频编辑**：`happyhorse-videoedit`、`wan2.7-videoedit`、`wanx2.1-vace-plus`（旧版）  
- **专用功能模型**：  
  - 对口型：`pixverse/pixverse-lipsync`  
  - 动作模仿：`pixverse/pixverse-motioncontrol`  
  - 视频超清：`pixverse/pixverse-upscale`  
  - 风格重绘：`video-style-transform`  
  - 数字人/播报：`wan2.2-s2v`、`liveportrait`、`emo-v1`、`videoretalk`  
  - 图生动作/换人：`wan2.2-animate-move`、`wan2.2-animate-mix`  

> **注意**：万相 2.7 系列（如 `wan2.7-i2v`、`wan2.7-t2v-*`）为当前推荐版本，支持首帧/首尾帧/视频续写三合一能力；而 `wan2.6` 及更早版本（如文档30–34所列）仅支持单一任务类型，且部分使用旧版 endpoint `/api/v1/services/aigc/image2video/`，已逐步淘汰 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。

## 关键参数

所有请求需包含以下必选字段：

- `model`：模型标识符（如 `"wan2.7-t2v-2026-06-12"`），必须与所选模型精确匹配  
- `input`：输入数据结构，依任务类型变化：  
  - 文生视频：`{"prompt": "..."}`  
  - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`  
  - 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "..."}`  
  - 参考生视频：`{"media": [{"type": "reference_image", "url": "..."}, ...], "prompt": "..."}`  
  - 视频编辑/对口型：`{"media": [{"type": "video", "url": "..."}, {"type": "audio", "url": "..."}]}`  
- `parameters`（可选）：控制输出质量与时长，常见字段：  
  - `duration`: 视频时长（秒），通常支持 3–5 秒（部分模型支持最长 10 秒）  
  - `resolution` / `size`: 分辨率，如 `"720P"`、`"1280*720"`、`"1024*576"`  
  - `watermark`: 布尔值，是否添加水印（默认 `true`）  
  - `aspect_ratio`: 宽高比（如 `"16:9"`，仅部分模型支持）  
  - `style`: 风格重绘中指定风格编号（0–7）  

请求头必须包含：  
- `Authorization: Bearer $DASHSCOPE_API_KEY`  
- `Content-Type: application/json`  
- `X-DashScope-Async: enable`（同步调用不支持，缺失将报错）  

## 使用方式

1. **准备环境**：  
   - 在百炼控制台开通对应模型服务  
   - 获取**同地域**的 API Key 并配置至环境变量 `DASHSCOPE_API_KEY`  
   - 获取业务空间 ID（WorkspaceId），用于构造专属 endpoint  

2. **构造请求 URL**（以北京地域为例）：  
   `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`  
   > **注意**：旧版文档（如文档33）仍使用 `/api/v1/services/aigc/image2video/` 路径，该路径仅适用于部分 legacy 模型（如 `wan2.2-kf2v-fla`），新模型统一使用 `/video-generation/` [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)  

3. **提交任务**：发送 POST 请求，获取 `task_id`  

4. **轮询结果**：使用 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态（或使用专属域名），直至 `status == "SUCCESS"`，响应中 `output.video_url` 为最终视频地址  

## 限制和注意事项

- **地域强绑定**：模型、API Key、Endpoint 必须同属一个地域（如北京、新加坡、美国弗吉尼亚等），混用将导致鉴权失败或 404 错误  
- **任务生命周期**：`task_id` 有效期为 24 小时，超时后无法查询结果  
- **并发与限流**：多数模型单账号 QPS 限制为 1–5，同时处理中任务数上限为 1–100（详见各模型资费文档），超出将返回 `429 Too Many Requests`  
- **输入要求**：  
  - 图像需为公网可访问 URL，格式为 JPG/PNG/WebP，尺寸建议 ≥ 512×512  
  - 视频时长建议 ≤ 10 秒，格式为 MP4/MOV  
  - Prompt 应简洁明确，避免冗长描述；多镜头需在 [prompt](../guides/prompt.md) 中显式说明（如“第1个镜头[0-3秒]...”），部分旧模型（如 wan2.6）需额外设置 `"prompt_extend": true`  
- **计费差异**：不同模型单价不同（如 `liveportrait` 0.02元/秒，`emo-v1` 0.08–0.16元/秒），且免费额度独立计算，调用前请确认模型计费策略

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)




