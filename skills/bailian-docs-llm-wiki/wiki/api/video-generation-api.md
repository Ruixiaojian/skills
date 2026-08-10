# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，覆盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、口型同步、风格重绘等核心场景。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果，任务 ID 有效期为 24 小时。开发者必须确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

API 统一接入多个主流视频生成模型，按能力维度可分为以下几类：

- **文生视频（T2V）**：支持 `wan2.7-t2v`、`happyhorse-1.1-t2v`、`pixverse/pixverse-c1-t2v`、`vidu/viduq3-turbo_text2video`、`kling/kling-v3-video-generation` 等模型，输入文本提示词生成视频。万相2.7支持多镜头叙事（通过 [prompt](../guides/prompt.md) 描述分镜），而旧版 wan2.6 需显式设置 `"prompt_extend": true` 和 `"shot_type":"multi"` [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)。
  
- **图生视频（I2V）**：包括基于首帧（如 `wan2.7-i2v`、`vidu/viduq3-pro-fast_img2video`、`happyhorse-1.1-i2v`）和首尾帧（如 `vidu/viduq3-turbo_start-end2video`、`wan2.2-kf2v-fla`）两类。万相2.7已统一支持首帧、首尾帧及视频续写三大任务，[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md) 明确推荐优先选用，替代早期仅支持首帧的 [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)。

- **参考生视频（R2V）**：支持[多模态](../concepts/multi-modal.md)参考输入（图像、视频、音频、文件），如 `wan2.7-r2v`、`pixverse/pixverse-c1-r2v`、`vidu/viduq3-ad_reference2video`、`happyhorse-1.1-r2v`，适用于角色融合、广告生成等场景。

- **视频编辑与增强**：涵盖视频编辑（`wan2.7-videoedit`、`happyhorse-1.1-videoedit`）、视频动作模仿（`pixverse/pixverse-motioncontrol`）、视频对口型（`pixverse/pixverse-lipsync`、`videoretalk`）、视频超清（`pixverse/pixverse-upscale`）、视频风格重绘（`video-style-transform`）等专项能力。

- **数字人与肖像动画**：包括数字人说话（`wan2.2-s2v`）、图生唱演（`emo-v1`）、图生播报（`liveportrait`）、图生舞蹈（`animate-anyone-gen2`）、表情包生成（`emoji`）、视频换人（`wan2.2-animate-mix`）、图生动作（`wan2.2-animate-move`）等轻量级肖像驱动模型，均需前置图像检测（如 `emo-detect-v1`、`liveportrait-detect`）。

> **注意**：部分模型使用独立路径，例如 `wan2.2-animate-move` 和 `wan2.2-animate-mix` 的 Endpoint 为 `/api/v1/services/aigc/image2video/video-synthesis`，而绝大多数视频生成模型（包括万相2.7+、HappyHorse、PixVerse、Vidu、Kling）统一使用 `/api/v1/services/aigc/video-generation/video-synthesis`。该差异在 [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md) 和 [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md) 中明确体现，开发者需按模型文档严格匹配路径。

## 关键参数

所有请求必须包含以下通用头信息：
- `Content-Type: application/json`
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `X-DashScope-Async: enable`（**必选**，缺失将报错：“current user api does not support synchronous calls”）

请求体（JSON）结构统一为：
```json
{
  "model": "<model_name>",
  "input": { ... },
  "parameters": { ... }
}
```

- `model`：必需，精确指定模型名称（如 `wan2.7-t2v-2026-06-12`），不同模型支持的 `input` 结构差异显著：
  - 文生视频：`"input": {"prompt": "..."}`；
  - 图生视频：`"input": {"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`；
  - 参考生视频：`"input": {"media": [{"type": "image_url", "url": "..."}, ...], "prompt": "..."}`；
  - 视频编辑/动作模仿：`"input": {"media": [{"type": "video_url", "url": "..."}, {"type": "image_url", "url": "..."}]}`；
  - 数字人：`"input": {"image_url": "...", "audio_url": "..."}`（`wan2.2-s2v`）或 `{"image_url": "...", "audio_url": "...", "style": "speech"}`。

- `parameters`：可选，常见字段包括：
  - `duration`: 视频时长（秒），范围通常为 2–30 秒（万相3.0最长支持30秒）；
  - `resolution` / `size`: 分辨率（如 `"720P"`、`"1280*720"`、`"1024*576"`）；
  - `aspect_ratio`: 宽高比（如 `"16:9"`）；
  - `watermark`: 布尔值，控制是否添加水印；
  - `audio`: 布尔值，控制是否生成音频（部分模型默认不生成）；
  - `style`: 风格类型（如 `video-style-transform` 模型中 `style: 0` 表示日式漫画）。

## 使用方式

1. **环境准备**：确认模型、Endpoint URL 与 API Key 属于同一地域；获取业务空间 ID（WorkspaceId）；配置 `DASHSCOPE_API_KEY` 环境变量。
2. **选择 Endpoint**：优先使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`，以获得更高性能与稳定性 [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)。
3. **发起异步请求**：向对应地域的 `POST /api/v1/services/aigc/.../video-synthesis` 发送请求，获取 `task_id`。
4. **轮询结果**：使用 `GET https://<base_url>/api/v1/tasks/{task_id}` 查询状态，直至 `status` 为 `"SUCCESS"`，响应中 `output.video_url` 即为生成视频地址。

> **注意**：`task_id` 有效期为 24 小时，过期后无法查询；禁止重复创建相同任务，应复用 `task_id` 轮询。

## 限制和注意事项

- **地域强绑定**：模型、URL、API Key 必须同属一个地域（如华北2北京、新加坡、美国弗吉尼亚等），跨地域调用必然失败，且部分模型（如 `wan2.2-s2v`、`emo-v1`、`liveportrait`）明确限定仅支持“华北2（北京）”地域 [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)。
- **异步强制要求**：所有视频 API 仅支持异步调用，同步请求将被拒绝；`X-DashScope-Async: enable` 请求头不可省略。
- **输入合规性**：肖像类模型（如 `emo-v1`、`liveportrait`、`animate-anyone-gen2`）必须先调用对应 `detect` 模型验证图片，否则生成失败。
- **资源限制**：多数后付费模型有 QPS/RPS 限制（如 `emo-v1` 为 1 RPS，`videoretalk` 为 1 RPS），并发任务数亦有限制（如 `emo-v1` 同时处理中任务数为 1）。
- **路径差异**：除主流 `/video-generation/` 路径外，`wan2.2-animate-move`、`wan2.2-animate-mix`、`wan2.2-s2v` 等模型使用 `/image2video/` 路径，务必核对原始文档避免 404 错误。

## 来源文档

- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


