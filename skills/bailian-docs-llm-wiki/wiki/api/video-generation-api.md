# video generation api

百炼平台的 Video Generation API 提供多种视频生成能力，包括文生视频（T2V）、图生视频（I2V）、参考生视频（R2V）、视频编辑、风格重绘及数字人播报等。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果，任务 ID 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

API 支持多系列模型，按能力可分为以下几类：

- **文生视频（T2V）**：输入文本提示词生成视频，主流模型包括 `wan2.7-t2v-*`、`vidu/viduq3-*-text2video`、`kling/kling-v3-*-video-generation`、`pixverse/pixverse-*-t2v` 和 `happyhorse-1.1-t2v`。其中万相2.7支持自然语言分镜（如“第1个镜头[0-3秒] 全景…”），而可灵支持显式 `multi_shot` + `multi_prompt` 结构化分镜 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)。

- **图生视频（I2V）**：基于首帧图像生成视频，支持模型包括 `wan2.7-i2v-*`、`vidu/viduq3-*-img2video`、`pixverse/pixverse-*-it2v`、`happyhorse-1.1-i2v`；另有首尾帧生视频（KF2V）能力，由 `wan2.7-i2v-*`（新版）、`vidu/viduq3-*-start-end2video`、`pixverse/pixverse-*-kf2v` 及旧版 `wan2.2-kf2v-flash` 提供 [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)。

- **参考生视频（R2V）**：融合多张参考图（人物/场景/物体）生成角色一致的视频，模型包括 `wan2.7-r2v-*`、`vidu/viduq3-*-reference2video`（分广告/短剧场景）、`pixverse/pixverse-*-r2v`、`happyhorse-1.1-r2v`。注意万相2.6旧版 R2V 使用 `reference_urls` 字段，而2.7新版统一使用 `media` 数组 [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)。

- **视频编辑与重绘**：支持指令驱动编辑（如“转为黏土风格”）、局部替换、口型同步（VideoRetalk）、风格迁移（`video-style-transform`）及视频换人（`wan2.2-animate-mix`）。

- **数字人与表情包**：面向人像的轻量级生成，包括 `wan2.2-s2v`（说话/唱歌）、`emo-v1`（唱演）、`liveportrait`（播报）、`videoretalk`（口型替换）、`emoji`（表情包）和 `animate-anyone-gen2`（舞蹈）。

> **注意**：万相2.1–2.6 系列（如 `wan2.6-t2v`、`wan2.6-i2v-flash`）属旧版协议，其请求路径为 `/api/v1/services/aigc/video-generation/video-synthesis`，但部分旧版文档（如文档29）错误地指向 `/api/v1/services/aigc/image2video/video-synthesis`，实际应统一使用 `video-generation` 路径，以避免 404 错误。

## 关键参数

所有请求必须包含以下基础字段：

- `model`（必选）：模型标识符，如 `wan2.7-t2v-2026-06-12`、`vidu/viduq3-pro_text2video`。
- `input`（必选）：包含 `prompt`（文本提示）及媒体资源（`media` 或 `video_url`/`image_url` 等），格式因模型而异。
- `parameters`（可选）：控制输出质量与时长，常见参数包括：
  - `resolution`：如 `"720P"`、`"1080P"`（部分模型也支持 `"540P"`、`"480P"`）；
  - `duration`：视频时长（秒），通常范围为 3–8 秒；
  - `size`：分辨率宽高（如 `"1280*720"`），与 `resolution` 互斥，优先级依模型而定；
  - `watermark`：布尔值，启用/禁用水印（默认 `true`）；
  - `audio`：布尔值，是否生成音频（仅部分 T2V/I2V 模型支持）；
  - `prompt_extend`：旧版万相多镜头必需设为 `true`，新版万相2.7 已弃用该参数，改由 [prompt](../guides/prompt.md) 自然描述分镜。

请求头必须包含：
- `Content-Type: application/json`
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `X-DashScope-Async: enable`（缺失将报错：“current user api does not [support](../guides/support.md) synchronous calls”）

## 使用方式

所有视频生成任务均遵循两步异步流程：

1. **创建任务**：发送 `POST` 请求至对应 Endpoint，获取 `task_id`。Endpoint 因地域与模型类型略有差异：
   - 华北2（北京）推荐使用业务空间专属域名：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`；
   - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...`；
   - 美国/德国：`https://dashscope-us.aliyuncs.com/...` 或 `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/...`；
   - 通用兼容地址（仍可用）：`https://dashscope.aliyuncs.com/...`（北京）、`https://dashscope-intl.aliyuncs.com/...`（国际）。

2. **轮询结果**：使用 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态，直至 `status` 为 `"SUCCESS"`，响应中 `output.video_url` 即为生成视频地址。

> **注意**：`task_id` 有效期为 24 小时，超时后无法查询；请勿重复提交相同请求，否则可能触发限流或返回冗余任务。

## 限制和注意事项

- **地域强绑定**：模型开通地域、API Key 所属地域、Endpoint 地域三者必须完全一致。例如，使用北京地域 API Key 调用新加坡模型将鉴权失败 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。
- **媒体资源要求**：图片需为公网可访问 URL（HTTPS），且尺寸建议 ≥ 512×512；视频时长建议 ≤ 10 秒；音频需为清晰人声 MP3/WAV。
- **输入长度限制**：`prompt` 最长 5000 字符（Vidu），其他模型未明确说明但建议 ≤ 1000 字；过长内容将被自动截断。
- **并发与限流**：多数模型 QPS 限制为 1–5，同时处理中任务数上限为 1–100（详见各模型资费文档）。例如 `liveportrait` 和 `videoretalk` 同一时刻仅允许 1 个运行中任务。
- **废弃模型提醒**：万相2.1–2.6 系列（文档26–30）已标记为“旧版协议”，官方明确推荐迁移到万相2.7系列；爱诗（PixVerse）与可灵（Kling）为新上线主力模型，功能更全、性能更优。

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
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)


