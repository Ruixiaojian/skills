# video generation api

百炼平台提供多种视频生成能力，覆盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、数字人驱动、风格重绘等场景。所有 API 均采用异步调用模式，需通过“创建任务 → 轮询获取结果”两步完成，任务 ID 有效期为 24 小时。调用前必须确保模型、Endpoint URL 与 API Key 属于同一地域，跨地域调用将失败。

## 支持的模型/功能

视频生成 API 支持以下主流模型及对应能力：

- **文生视频（T2V）**：`wan2.7-text2video`、`vidu/viduq3-turbo_text2video`、`kling/kling-v3-video-generation`、`pixverse/pixverse-c1-t2v`、`happyhorse/text2video`  
- **图生视频（I2V）**：支持首帧（`wan2.7-i2v`、`vidu/viduq3-pro-fast_img2video`、`pixverse/pixverse-c1-it2v`）、首尾帧（`wan2.7-kf2v`、`vidu/viduq3-turbo_start-end2video`、`pixverse/pixverse-c1-kf2v`），以及视频续写（仅 `wan2.7` 支持）  
- **参考生视频（R2V）**：支持多图/多视频+文本融合（`wan2.7-r2v`、`pixverse/pixverse-v6-r2v-omni`、`vidu/viduq3-ad_reference2video`、`happyhorse/reference2video`）  
- **视频编辑**：指令编辑（如“转为水墨风”）、局部替换、风格迁移（`wan2.7-videoedit`、`happyhorse/video-edit`、`video-style-transform`）  
- **数字人与肖像动画**：基于单图+音频生成说话/唱歌视频（`wan2.2-s2v`、`emo-v1`、`liveportrait`），以及动作模仿（`pixverse/pixverse-motioncontrol`、`animate-anyone-gen2`）  
- **专用任务**：对口型（`pixverse/pixverse-lipsync`）、视频超清（`pixverse/pixverse-upscale`）、口型替换（`videoretalk`）、表情包生成（`emoji`）  

> **注意**：万相系列存在新旧协议并存现象。`wan2.7` 及以上模型统一使用 `/aigc/video-generation/video-synthesis` 路径；而 `wan2.6` 及更早版本（如文档31–34）部分仍沿用 `/aigc/image2video/video-synthesis` 路径（例如[万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)），开发者应优先选用 `wan2.7` 新协议以获得完整功能支持。

## 关键参数

所有请求均需包含以下基础字段：

- `model`：必填，指定模型标识符（如 `"wan2.7-text2video"`、`"vidu/viduq3-turbo_text2video"`）  
- `input`：必填，结构因任务类型而异：
  - 文生视频：`{"prompt": "描述文本"}`
  - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`
  - 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "..."}`
  - 参考生视频：`{"media": [{"type": "image_url", "url": "..."}, {"type": "video_url", "url": "..."}], "prompt": "..."}`
  - 数字人：`{"image_url": "...", "audio_url": "..."}`（见[万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)）
- `parameters`：可选，控制输出质量与时长：
  - `duration`：视频时长（秒），常见值 `5` 或 `10`（部分模型最大支持 `30` 秒，如万相3.0）
  - `resolution` / `size` / `aspect_ratio`：分辨率（如 `"720P"`、`"1280*720"`、`"16:9"`）
  - `watermark`：布尔值，是否添加水印（默认 `true`）
  - 其他模型特有参数（如 `style`、`mode`、`seed`）详见各模型文档

请求头必须包含：
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `Content-Type: application/json`
- `X-DashScope-Async: enable`

## 使用方式

1. **准备环境**：确认模型已开通，获取对应地域的 [API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，并配置为环境变量 `DASHSCOPE_API_KEY`；在控制台获取业务空间 ID（`WorkspaceId`）  
2. **构造请求 URL**：使用业务空间专属域名（推荐）：  
   `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`  
   （其他地域替换为对应区域标识，如 `ap-southeast-1`、`us-east-1` 等；旧版文档中出现的 `dashscope.aliyuncs.com` 已不推荐，详见[HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)）  
3. **提交[异步任务](../concepts/asynchronous-task.md)**：发送 `POST` 请求，获取 `task_id`  
4. **轮询结果**：使用 `task_id` 向 `GET https://.../api/v1/tasks/{task_id}` 查询状态，直到 `status == "success"`，响应中 `output.video_url` 即为生成视频地址  

> **注意**：部分模型（如 `animate-anyone`、`emo`、`liveportrait`）需前置图像检测步骤（调用 `*-detect` 模型），且流程为串行三步（检测 → 模板生成 → 视频合成），不可跳过；而 `pixverse-lipsync`、`video-style-transform` 等则为标准两步异步流程。详细流程请参考[爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)等具体文档。

## 限制和注意事项

- **地域强绑定**：模型、API Key、Endpoint URL 必须同属一个地域（如华北2北京），混用将导致鉴权失败或 404 错误  
- **任务并发限制**：多数模型同时处理中任务数上限为 1（如 `emo-v1`、`videoretalk`），高并发需排队；`wan2.7` 系列部分支持更高并发，但需查看具体模型限流说明  
- **输入约束**：  
  - 图片/视频 URL 必须公网可访问且 HTTPS 协议  
  - `prompt` 长度建议 ≤ 512 字符，避免敏感或违法内容  
  - 首帧/尾帧图像需构图清晰、主体居中、无遮挡  
- **计费与免费额度**：各模型单价差异显著（如 `liveportrait` 0.02元/秒，`wan2.2-s2v` 480P 0.5元/秒），免费额度按模型独立计算，详见各模型资费页  
- **路径一致性**：除少数遗留模型（如 `wan2.2` 首尾帧）外，**所有新模型统一使用 `/aigc/video-generation/video-synthesis` 路径**，而非 `/aigc/image2video/...` —— 开发者应以最新文档为准，避免因路径错误导致 404。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
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
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


