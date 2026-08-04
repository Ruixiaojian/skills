# video generation api

百炼平台提供多种视频生成能力，覆盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、视频动作迁移、数字人生成等场景。所有 API 均采用异步调用模式，需通过“创建任务 → 轮询结果”两步完成，任务 ID 有效期为 24 小时。统一使用 `POST /api/v1/services/aigc/video-generation/video-synthesis` 接口，但模型名、输入结构和参数因能力而异。

## 支持的模型/功能

视频生成 API 按输入模态与任务类型分为以下几类：

- **文生视频（T2V）**：纯文本提示词生成视频，支持多镜头叙事（如 `wan2.7-t2v-2026-06-12`、`vidu/viduq3-turbo_text2video`、`kling/kling-v3-video-generation`）。[万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md) 明确支持通过 [prompt](../guides/prompt.md) 描述分镜（如 “第1个镜头\[0-3秒\] 全景：雨夜的纽约街头”），无需显式配置 `shot_type`。
  
- **图生视频（I2V）**：基于单张图像生成视频，包括首帧生视频（如 `happyhorse-1.1-t2v`、`pixverse/pixverse-c1-it2v`、`vidu/viduq3-pro-fast_img2video`）和首尾帧生视频（如 `pixverse/pixverse-c1-kf2v`、`vidu/viduq3-turbo_start-end2video`）。[爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md) 和 [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md) 均要求 `media` 数组中按顺序传入 `"first_frame"` 和 `"last_frame"` 类型图像。

- **参考生视频（R2V）**：支持多张参考图像（或图像+视频+音频）融合生成视频，适用于角色一致性控制（如 `happyhorse-reference-to-video`、`wan2.7-r2v-2026-06-12`、`pixverse/pixverse-c1-r2v`、`vidu/viduq3-ad_reference2video`）。[HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md) 强调需通过 `prompt` 描述多主体交互逻辑。

- **视频编辑与增强**：包括视频风格重绘（`video-style-transform`）、超分辨率（`pixverse/pixverse-upscale`）、对口型（`pixverse/pixverse-lipsync`）、动作模仿（`pixverse/pixverse-motioncontrol`）、口型替换（`videoretalk`）等。

- **人物驱动类**：聚焦肖像动画，如数字人（`wan2.2-s2v`）、表情包（`emoji`）、播报视频（`liveportrait`）、唱演视频（`emo-v1`）、舞蹈视频（`animate-anyone-gen2`）及视频换人（`wan2.2-animate-mix`）。此类模型普遍要求前置图像检测（如 `emo-detect-v1`、`liveportrait-detect`），且多数仅限华北2（北京）地域。

> **注意**：文档 30–34 明确标注为“legacy”（旧版），对应 `wan2.1`–`wan2.6` 系列模型，其 endpoint path 为 `/api/v1/services/aigc/image2video/video-synthesis`（如文档 33），与新版 `/video-generation/` 路径不兼容。开发者应优先选用 `wan2.7` 及以上版本，避免混用路径。

## 关键参数

所有请求必须包含以下基础参数：

- `model`：模型标识符（如 `"wan2.7-t2v-2026-06-12"`），需与所选模型严格一致。
- `input`：核心输入数据，结构依模型而异：
  - 文生视频：`{"prompt": "..."}`；
  - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`；
  - 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "..."}`；
  - 参考生视频：`{"media": [{"type": "image_url", "url": "..."}, ...], "prompt": "..."}`；
  - 视频编辑：`{"media": [{"type": "video_url", "url": "..."}], "prompt": "..."}`。
- `parameters`：可选控制参数，常见字段包括：
  - `duration`：视频时长（秒），通常范围 3–5 秒；
  - `resolution` 或 `size`：输出分辨率（如 `"720P"`、`"1280*720"`）；
  - `watermark`：是否添加水印（布尔值，默认 `true`）；
  - `audio`：是否生成音频（布尔值，部分模型支持）；
  - `style`：风格重绘时指定风格 ID（0–7）。

请求头（Headers）必须包含：
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `Content-Type: application/json`
- `X-DashScope-Async: enable`

## 使用方式

1. **环境准备**：确保模型、Endpoint URL 与 API Key 属于同一地域（如华北2北京），并配置业务空间专属域名（推荐 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）。
2. **创建任务**：向 `POST https://{WorkspaceId}.<region>.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` 发送请求，获取 `task_id`。
3. **轮询结果**：使用 `task_id` 向 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（旧域名）或 `GET https://{WorkspaceId}.<region>.maas.aliyuncs.com/api/v1/tasks/{task_id}`（新域名）查询状态，直至返回 `"status": "SUCCESS"` 并含 `output.video_url`。
4. **错误处理**：检查 `task_id` 有效期（24 小时）、地域一致性及 `X-DashScope-Async` 头是否缺失（缺失将报错：“current user api does not support synchronous calls”）。

## 限制和注意事项

- **地域强约束**：所有模型、API Key 与 Endpoint 必须同地域，跨地域调用必然失败。新加坡、德国、日本等地域仅支持部分模型（如 HappyHorse、万相2.7），详见各文档适用范围说明。
- **异步强制性**：所有视频 API 仅支持异步，同步调用会报错；任务处理时间通常为 1–5 分钟（视频编辑类可达 10 分钟）。
- **资源限制**：多数后付费模型有 QPS/RPS 限制（如 `emo-v1` 为 1 QPS，`videoretalk` 为 1 RPS），并发任务数亦有限制（如 `animate-anyone-gen2` 同一时刻仅 1 个作业运行）。
- **输入合规性**：数字人、表情包等人物驱动类模型（如 `emo-v1`、`liveportrait`）必须先调用对应 `detect` 模型验证图像，否则生成失败。
- **路径差异**：新版模型统一使用 `/video-generation/` 路径，而 `wan2.2`–`wan2.6` 等旧版模型使用 `/image2video/` 路径（如文档 33），二者不可混用。

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
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


