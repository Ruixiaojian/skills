# video generation api

百炼平台的 Video Generation API 提供多种文生视频、图生视频、参考生视频及视频编辑能力，支持 HappyHorse、万相（Wan）、爱诗（PixVerse）、Vidu、可灵（Kling）等主流模型。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果，任务状态有效期为 24 小时。

## 支持的模型/功能

API 覆盖五大类视频生成能力，对应不同模型与输入范式：

- **文生视频（T2V）**：输入纯文本提示词，生成连贯视频。支持模型包括 `wan2.7-t2v-2026-06-12`、`vidu/viduq3-turbo_text2video`、`kling/kling-v3-video-generation`、`pixverse/pixverse-c1-t2v` 等。[万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md) 明确支持多镜头叙事（通过 [prompt](../guides/prompt.md) 描述分镜），而旧版 `wan2.6` 模型需显式设置 `"shot_type": "multi"` 才生效。

- **图生视频（I2V）**：基于单张首帧图像生成视频。除基础首帧外，还支持：
  - **首尾帧生视频（KF2V）**：输入首帧+尾帧+[prompt](../guides/prompt.md)，实现平滑过渡（如 `vidu/viduq3-turbo_start-end2video`、`pixverse/pixverse-c1-kf2v`）；
  - **视频续写**：仅万相2.7模型支持，[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md) 明确将其列为三大核心任务之一；
  - **图生动作/换人/对口型**：属垂直功能，如 `wan2.2-animate-move`（动作迁移）、`wan2.2-animate-mix`（角色替换）、`pixverse/pixverse-lipsync`（口型同步）。

- **参考生视频（R2V）**：传入多张参考图像（或图像+视频+音频），结合 [prompt](../guides/prompt.md) 控制角色与场景融合。HappyHorse、万相2.7、爱诗、Vidu 均提供对应模型（如 `happyhorse-r2v`、`wan2.7-r2v-2026-06-12`）。

- **视频编辑（Video Editing）**：支持风格迁移、局部替换、指令编辑等。万相2.7 和可灵均提供统一编辑接口，但参数结构不同；Vidu 和爱诗则聚焦于特定子任务（如 Vidu 的广告参考生视频）。

- **数字人与肖像动画**：面向播报、唱演、表情包等场景，包含 `liveportrait`、`emo-v1`、`animate-anyone-gen2`、`emoji` 等专用模型，均需先调用检测模型（如 `liveportrait-detect`）验证输入合规性。

> **注意**：文档中存在明确版本演进冲突。[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md) 明确指出“推荐优先选用”新版，并说明旧版（wan2.6及早期）仅支持首帧生视频；而 [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md) 被标记为“仅支持首帧生视频”，证实其功能已收敛。开发者应优先集成 wan2.7 系列模型。

## 关键参数

所有请求必须包含以下通用参数：

- **`model`**（必填）：模型标识符，格式为 `<vendor>/<model-name>`（如 `wan2.7-t2v-2026-06-12`、`vidu/viduq3-pro-fast_img2video`）。不同模型对 `input` 结构要求严格，不可混用。
- **`input`**（必填）：承载核心输入数据。结构因模型而异：
  - 文生视频：`{"prompt": "..."}`；
  - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`；
  - 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "..."}`；
  - 参考生视频：`{"media": [{"type": "reference_image", "url": "..."}, ...], "prompt": "..."}`；
  - 数字人：`{"image_url": "...", "audio_url": "..."}`（需先过检测）。
- **`parameters`**（可选）：控制输出质量与行为，常见字段：
  - `duration`: 视频时长（秒），通常为 3–5 秒；
  - `resolution` / `size`: 分辨率（如 `"720P"`、`"1280*720"`、`"1024*576"`）；
  - `watermark`: 布尔值，是否添加水印（默认 `true`）；
  - `aspect_ratio`: 宽高比（如 `"16:9"`）；
  - `style`: 风格重绘时指定预设风格 ID（如 `video-style-transform` 的 `0` 表示日式漫画）。

- **请求头（Headers）**：
  - `Authorization: Bearer $DASHSCOPE_API_KEY`（必填）；
  - `Content-Type: application/json`（必填）；
  - `X-DashScope-Async: enable`（必填，异步模式强制启用）。

## 使用方式

1. **环境准备**：确保模型、Endpoint URL 与 API Key 属于同一地域（如华北2北京），跨地域调用必然失败。强烈建议使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`，以获得更高性能与稳定性。

2. **创建任务**：向 `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` 发送请求，获取 `task_id`。注意：
   - 所有视频类 API（含数字人、风格重绘）均使用该统一 endpoint；
   - 例外：部分旧版模型（如 `wan2.2-kf2v-fla`）仍使用 `/api/v1/services/aigc/image2video/video-synthesis`，见 [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)。

3. **轮询结果**：使用 `task_id` 向 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态（旧版）或 `GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}`（新域名）。成功时返回 `result.video_url`。

4. **错误处理**：检查 `task_status` 字段（`QUEUED`/`PROCESSING`/`SUCCESS`/`FAILED`），失败时 `error_code` 和 `error_message` 提供具体原因（如 `INVALID_INPUT`、`QUOTA_EXHAUSTED`）。

## 限制和注意事项

- **地域强绑定**：模型、API Key、Endpoint URL 必须同地域。北京地域的 Key 无法调用新加坡模型，反之亦然。[HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md) 和 [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md) 均强调此约束。
- **任务幂等性**：`task_id` 24 小时内有效，**严禁重复提交相同请求**。重复创建将导致资源浪费且不保证结果一致性。
- **输入合规性**：数字人、肖像动画类模型（LivePortrait、EMO、AnimateAnyone、Emoji）必须前置调用 `*-detect` 模型验证图片质量，否则生成失败。
- **计费差异**：分辨率、时长、模型类型直接影响费用（如 EMO 3:4 画幅为 1:1 的 2 倍单价），详见各模型定价文档。
- **SDK 兼容性**：DashScope SDK 支持多数模型，但部分旧版（如 `wanx2.1-vace-plus`）或专用模型（如 `video-style-transform`）需直接 HTTP 调用。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
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


