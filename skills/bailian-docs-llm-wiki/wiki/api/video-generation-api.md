# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，包括文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、口型同步、风格重绘等。所有接口均采用异步调用模式，通过 `task_id` 轮询获取结果，任务有效期为 24 小时。开发者需确保模型、Endpoint URL 和 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

API 支持多系列模型，按能力可分为以下几类：

- **文生视频（T2V）**：输入文本提示词生成视频，主流模型包括 `vidu/viduq3-turbo_text2video`、`kling/kling-v3-video-generation`、`wan2.7-t2v-2026-06-12`、`pixverse/pixverse-c1-t2v` 等。[Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md) 和 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md) 均明确支持智能分镜（如时间戳描述或多镜头指令）。
  
- **图生视频（I2V）**：
  - *基于首帧*：以单张图像为起点生成视频，如 `wan2.7-i2v`、`vidu/viduq3-pro-fast_img2video`、`pixverse/pixverse-c1-it2v`；
  - *基于首尾帧*：输入首帧与尾帧图像生成平滑过渡视频，如 `wan2.2-kf2v-fla`（旧版）、`vidu/viduq3-turbo_start-end2video`、`pixverse/pixverse-c1-kf2v`；
  - *视频续写*：仅万相2.7新版支持，属图生视频子能力，详见 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。

- **参考生视频（R2V）**：支持[多模态](../concepts/multi-modal.md)参考（图像/视频/音频），融合角色形象与音色生成一致性视频，主流模型为 `wan2.7-r2v-2026-06-12`、`pixverse/pixverse-c1-r2v`、`vidu/viduq3-ad_reference2video`。

- **视频编辑类**：涵盖指令编辑（如风格迁移）、视频换人（`wan2.2-animate-mix`）、动作迁移（`pixverse/pixverse-motioncontrol`、`wan2.2-animate-move`）、口型替换（`videoretalk`、`pixverse/pixverse-lipsync`）、超清增强（`pixverse/pixverse-upscale`）、风格重绘（`video-style-transform`）等。

- **数字人与肖像动画**：面向人像驱动的专用模型，如 `wan2.2-s2v`（说话/唱歌）、`emo-v1`（唱演）、`liveportrait`（轻量播报）、`animate-anyone-gen2`（舞蹈复刻）、`emoji`（表情包）等，均需先调用对应 detect 模型校验输入合规性。

> **注意**：文档中存在协议路径不一致问题。多数新版模型（如 wan2.7、vidu、pixverse、kling）使用统一 Endpoint `/api/v1/services/aigc/video-generation/video-synthesis`；但部分旧版模型（如 `wan2.2-kf2v-fla`、`wan2.2-animate-mix`、`wan2.2-animate-move`）仍使用 `/api/v1/services/aigc/image2video/video-synthesis`。调用前请务必核对对应模型文档的请求路径，否则返回 404。

## 关键参数

- **必选请求头**：
  - `Authorization: Bearer $DASHSCOPE_API_KEY`
  - `X-DashScope-Async: enable`（必须为 `enable`，同步调用不支持）
  - `Content-Type: application/json`

- **核心请求体字段**：
  - `model`: 模型标识符（如 `"vidu/viduq3-turbo_text2video"`），不同模型支持的 `input` 结构差异显著；
  - `input`: 包含输入内容，常见结构：
    - 文生视频：`{"prompt": "..."}`；
    - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`；
    - 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "..."}`；
    - 参考生视频：`{"media": [{"type": "reference_image", "url": "..."}, ...], "prompt": "..."}`；
    - 视频编辑/口型替换：`{"media": [{"type": "video_url", "url": "..."}, {"type": "audio_url", "url": "..."}]}`。
  - `parameters`: 控制生成质量与行为，常用项包括：
    - `duration`: 视频时长（秒），通常为 3–5 秒；
    - `resolution` / `size`: 分辨率（如 `"720P"`、`"1280*720"`、`"1024*576"`）；
    - `watermark`: 是否添加水印（布尔值）；
    - `aspect_ratio`: 宽高比（如 `"16:9"`，仅 kling 支持）；
    - `style_level`（EMO）、`mode`（Kling）、`shot_type`（旧版 wan2.6）等模型特有参数。

## 使用方式

所有视频生成任务均遵循两步异步流程：

1. **创建任务**：发送 `POST` 请求至对应地域的 Endpoint（如北京地域：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`），获取 `task_id`；
2. **轮询结果**：使用 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（或业务空间专属域名）查询任务状态，直至 `status` 为 `"SUCCESS"`，响应中 `output.video_url` 即为生成视频地址。

> **注意**：`task_id` 有效期为 24 小时，过期后无法查询。文档中多次强调“请勿重复创建任务”，因重复提交相同请求可能导致计费异常或任务冲突。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint URL、API Key 必须同属一个地域（如华北2北京、新加坡、美国弗吉尼亚等）。跨地域调用必然失败，且不同地域的 API Key 不可复用。
- **业务空间专属域名推荐**：华北2（北京）和新加坡地域已启用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 等专属域名，性能与稳定性优于通用 `dashscope.aliyuncs.com`，[HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md) 明确建议迁移。
- **输入合规性前置检查**：数字人及肖像动画类模型（如 EMO、LivePortrait、AnimateAnyone、Emoji）必须先调用对应 `detect` 模型验证图像质量，否则生成失败。
- **旧版模型兼容性**：`wan2.1`–`wan2.6` 系列（如 `wanx2.1-vace-plus`、`wan2.2-kf2v-fla`）仍可调用，但官方明确推荐升级至 `wan2.7` 新版协议，因其支持更丰富的任务类型（如视频续写）和统一接口设计。
- **计费与限流**：各模型独立计费（按秒、按帧或按次），并发任务数与 QPS/RPS 受限（如 `emo-v1` 同时处理中任务数为 1），详情需查阅各模型资费文档。

## 来源文档

- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)


