# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，涵盖文生视频（T2V）、图生视频（I2V）、参考生视频（R2V）、视频编辑、数字人驱动、口型同步等场景。所有模型均采用异步调用模式，通过 `task_id` 轮询获取结果，任务有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格同地域部署。

## 支持的模型/功能

Video Generation API 支持以下主流模型及对应能力：

- **万相系列（wan2.7）**：统一新版协议，支持首帧/首尾帧/视频续写三类图生视频、文生视频（含多镜头叙事）、参考生视频（图像+视频+音频多模态融合）、视频编辑（风格迁移、局部替换）[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。
- **HappyHorse 系列**：提供图生视频（基于首帧）、参考生视频（多图融合）、视频编辑（指令+参考图）三类能力，适用于物理真实感强的运动建模 [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)。
- **可灵（Kling）**：支持文生视频、图生视频（首帧/首尾帧）、参考生视频及视频编辑，强调高保真动态与构图控制 [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)。
- **爱诗（PixVerse）**：覆盖图生视频（首帧/首尾帧）、文生视频、参考生视频、视频对口型、动作模仿、视频超清、视频风格重绘等细分能力 [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)。
- **Vidu**：专注文生视频与图生视频（首帧/首尾帧），强调影视级画质与节奏控制。
- **数字人与肖像动画**：包括万相-s2v（音画同步）、LivePortrait（轻量播报）、EMO（唱演）、AnimateAnyone（舞蹈复刻）、VideoRetalk（口型替换）、Emoji（表情包）等专用模型，均需先调用 `detect` 模型校验输入合规性。
- **视频后处理**：如 Vidu/VideoStyleTransform（8种艺术风格重绘）、PixVerse-upscale（4K超分）等独立功能模型。

> **注意**：万相2.1–2.6 系列（如 `wan2.2-kf2v-fla`、`wanx2.1-vace-plus`）使用旧版协议，Endpoint 路径为 `/api/v1/services/aigc/image2video/video-synthesis`，而万相2.7 及所有新模型（HappyHorse、Kling、PixVerse、Vidu）统一使用 `/api/v1/services/aigc/video-generation/video-synthesis`。混用路径将导致 404 错误 [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)。

## 关键参数

所有请求必须包含以下基础参数：

- **`model`**（必填）：模型标识符，如 `"wan2.7-t2v-2026-06-12"`、`"pixverse/pixverse-c1-t2v"`、`"vidu/viduq3-turbo_text2video"`。不同模型支持的子能力由 model name 决定。
- **`input`**（必填）：结构化输入数据：
  - 文生视频：`{"prompt": "..."}`；
  - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`；
  - 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "..."}`；
  - 参考生视频：`{"media": [{"type": "reference_image", "url": "..."}, ...], "prompt": "..."}`；
  - 数字人：`{"image_url": "...", "audio_url": "..."}`（需先通过 detect）。
- **`parameters`**（可选）：控制输出质量与行为：
  - `resolution`（如 `"720P"`、`"540P"`、`"1280*720"`）；
  - `duration`（秒数，通常 3–5 秒）；
  - `watermark`（布尔值，默认 `true`）；
  - `aspect_ratio`（如 `"16:9"`）；
  - `style_level`（EMO 等模型特有）；
  - `seed`（固定随机性）。

- **请求头（Headers）**：
  - `Authorization`: `Bearer $DASHSCOPE_API_KEY`（必填）；
  - `Content-Type`: `application/json`（必填）；
  - `X-DashScope-Async`: `enable`（必填，异步强制开关）。

## 使用方式

1. **准备环境**：确认模型开通地域，获取对应地域的 [API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，配置为环境变量 `DASHSCOPE_API_KEY`；在控制台获取业务空间 ID（`WorkspaceId`）。
2. **构造请求**：使用业务空间专属域名（推荐）或通用域名：
   - 专属域名（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`
   - 通用域名（兼容旧模型）：`https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`
3. **提交任务**：发送 `POST` 请求，获取 `task_id`。
4. **轮询结果**：使用 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（或专属域名对应路径）查询状态，直到 `status` 为 `"SUCCESS"`，响应中 `output.video_url` 即为生成视频地址。

> **注意**：部分模型（如 EMO、LivePortrait、AnimateAnyone）要求严格两步流程：先调用 `detect` 模型验证输入图片合规性，再调用主模型生成视频。跳过检测将导致失败 [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)。

## 限制和注意事项

- **地域一致性**：模型、Endpoint、API Key 必须同属一个地域（如华北2北京），跨地域调用必然失败。
- **异步强制**：所有视频 API 均不支持同步调用，缺失 `X-DashScope-Async: enable` 头将返回错误 `"current user api does not support synchronous calls"`。
- **任务生命周期**：`task_id` 有效期为 24 小时，超时后无法查询结果。
- **并发与限流**：多数模型 QPS/RPS 限制为 1–5，同时处理中任务数上限为 1–100（依模型而异），详见各模型资费文档。
- **输入约束**：图像需清晰、正面、单人；视频时长建议 ≤30 秒；音频需人声清晰、无背景噪音；URL 必须可公开访问且 HTTPS。
- **废弃模型**：万相2.6 及更早版本（如 `wan2.2-s2v`、`wanx2.1-vace-plus`）已标记为 Legacy，新项目应优先选用 wan2.7 或其他新一代模型。

## 来源文档

- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
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
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


