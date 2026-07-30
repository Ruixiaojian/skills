# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，包括文生视频（T2V）、图生视频（I2V）、参考生视频（R2V）、视频编辑、口型同步、风格重绘等。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果，任务 ID 有效期为 24 小时。推荐使用业务空间专属域名以获得更高性能与稳定性 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。

## 支持的模型/功能

当前支持以下主流模型及对应能力：

- **文生视频（T2V）**：`happyhorse-1.1-t2v`、`wan2.7-t2v-2026-06-12`、`pixverse/pixverse-c1-t2v`、`kling/kling-v3-video-generation`、`vidu/viduq3-turbo_text2video`  
- **图生视频（I2V）**：  
  - 首帧：`happyhorse-1.1-i2v`、`wan2.7-i2v-2`、`pixverse/pixverse-c1-it2v`、`vidu/viduq3-pro-fast_img2video`  
  - 首尾帧：`pixverse/pixverse-c1-kf2v`、`vidu/viduq3-turbo_start-end2video`、`wan2.2-kf2v-flash`（旧版）[万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)  
- **参考生视频（R2V）**：`happyhorse-1.1-r2v`、`wan2.7-r2v-2026-06-12`、`pixverse/pixverse-c1-r2v`、`vidu/viduq3-ad_reference2video`  
- **视频编辑类**：  
  - 指令编辑：`happyhorse-1.0-video-edit`、`wan2.7-videoedit`  
  - 动作迁移：`wan2.2-animate-move`、`pixverse/pixverse-motioncontrol`  
  - 角色替换：`wan2.2-animate-mix`  
  - 口型同步：`pixverse/pixverse-lipsync`、`videoretalk`  
  - 风格重绘：`video-style-transform`  
  - 超分增强：`pixverse/pixverse-upscale`  
- **数字人/肖像驱动**：`wan2.2-s2v`、`liveportrait`、`emo-v1`、`video-retalk`  

> **注意**：万相系列存在新旧协议并存现象。`wan2.7` 模型统一使用 `/api/v1/services/aigc/video-generation/video-synthesis` 路径；而 `wan2.2`/`wan2.5`/`wan2.6` 等旧版模型中，部分（如 `wan2.2-kf2v-flash`）仍使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径 [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)，调用前务必核对文档路径与模型版本。

## 关键参数

所有请求需包含以下通用参数：

- **必选 Header**：
  - `Authorization: Bearer $DASHSCOPE_API_KEY`
  - `X-DashScope-Async: enable`
  - `Content-Type: application/json`

- **必选 Body 字段**：
  - `model`: 模型标识符（如 `"wan2.7-t2v-2026-06-12"`），必须与所选地域开通的模型一致
  - `input`: 根据任务类型提供不同结构：
    - T2V：`{"prompt": "文本描述"}`
    - I2V/R2V：`{"media": [{"type": "image_url", "url": "..."}, ...], "prompt": "..."}`
    - 视频编辑/口型同步：`{"media": [{"type": "video_url", "url": "..."}, {"type": "audio_url", "url": "..."}]}`  
  - `parameters`（可选但常用）：
    - `duration`: 视频时长（秒），常见值 `3`/`5`/`8`
    - `resolution` 或 `size`: 分辨率，如 `"720P"`、`"1280*720"`、`"540P"`
    - `watermark`: 布尔值，控制是否添加水印（默认 `true`）
    - `aspect_ratio`: 宽高比（如 `"16:9"`），部分模型支持
    - `prompt_extend`: 旧版万相多镜头需设为 `true`，新版 `wan2.7` 已弃用该参数，改由 `prompt` 自然语言描述分镜 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)

## 使用方式

1. **环境准备**：确保模型、Endpoint URL 与 API Key 属于同一地域；推荐迁移至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），其中 `{WorkspaceId}` 需从控制台获取。
2. **创建任务**：`POST /api/v1/services/aigc/video-generation/video-synthesis`，返回 `task_id`。
3. **轮询结果**：使用 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（或对应地域专属域名）查询状态，直至 `status == "SUCCESS"`，响应中 `output.video_url` 即为生成视频地址。
4. **错误处理**：若返回 `UNKNOWN` 状态，说明 `task_id` 已过期（24 小时）；若报错 `"current user api does not support synchronous calls"`，确认 `X-DashScope-Async` Header 已设置为 `enable`。

## 限制和注意事项

- **地域强绑定**：模型、API Key、Endpoint URL 必须同属一个地域（如华北2北京），跨地域调用必然失败，且部分模型（如 `liveportrait`、`videoretalk`、`emo`）仅支持华北2（北京）地域 [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)。
- **异步强制要求**：所有视频类 API 仅支持异步，同步调用将报错；任务平均耗时 1–5 分钟，超长任务（如 `wanx2.1-vace-plus`）可达 5–10 分钟。
- **输入规范**：多数肖像类模型（`s2v`、`liveportrait`、`emo`）需先调用 `*-detect` 接口校验图片合规性，否则生成失败。
- **模型演进提示**：万相 `2.7` 系列为当前主力版本，全面替代 `2.1–2.6` 旧版；旧版文档明确标注“推荐优先选用新版”，且部分旧模型（如 `wan2.6` 图生视频）已不支持首尾帧/视频续写等新能力 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
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
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


