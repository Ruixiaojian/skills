# video generation api

百炼平台的视频生成 API 提供多种模态输入（文本、图像、视频、音频）驱动的视频生成与编辑能力，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、口型替换、风格重绘等核心场景。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果，任务 ID 有效期为 24 小时。

## 支持的模型/功能

视频生成 API 涵盖三类主流能力模型：

- **通用生成模型**：  
  - `wan3.0-video`（[万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)）：All-in-One 模型，统一支持文生视频、图生视频（首帧/首尾帧）、参考生视频，最长生成 30 秒视频（邀测中）。  
  - `wan2.7-*` 系列（如 `wan2.7-video`、`wan2.7-r2v`、`wan2.7-videoedit`）：新版协议，支持多模态输入与高级语义理解（如多镜头叙事、首尾帧+续写），**推荐优先选用**。  
  - `kling/kling-v3-*`、`vidu/viduq3-*`、`pixverse/pixverse-*`：各厂商主力模型，覆盖文生/图生/参考生/超清/动作模仿等细分能力。

- **数字人与肖像动画模型**：  
  - `wan2.2-s2v`（数字人说话/唱歌）、`emo-v1`（悦动人像）、`liveportrait`（灵动人像）、`videoretalk`（口型替换）、`animate-anyone-gen2`（舞动人像）等，均需先调用对应 detect 模型校验输入合规性。

- **专用编辑与增强模型**：  
  - `video-style-transform`（8 种预设艺术风格重绘）、`pixverse/pixverse-upscale`（4K 超分）、`pixverse/pixverse-lipsync`（对口型）、`pixverse/pixverse-motioncontrol`（动作模仿）。

> **注意**：文档中存在 URL 路径不一致问题。多数模型（如 HappyHorse、万相2.7+、PixVerse、Vidu、Kling）使用 `/api/v1/services/aigc/video-generation/video-synthesis`；但部分旧版万相模型（如文档 33 中的 wan2.2 首尾帧）和 `wan2.2-animate-move`、`wan2.2-animate-mix` 使用 `/api/v1/services/aigc/image2video/video-synthesis`。开发者需严格按模型文档指定路径调用，不可混用。

## 关键参数

所有请求必须包含以下基础参数：

- **`model`**（必填）：模型标识符，如 `"wan2.7-video"`、`"pixverse/pixverse-c1-t2v"`、`"vidu/viduq3-turbo_text2video"`。不同模型支持的输入结构差异显著。
- **`input`**（必填）：根据模型类型结构化传入：
  - 文生视频：`{"prompt": "..."}`；
  - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`；
  - 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "..."}`；
  - 参考生视频：`{"media": [{"type": "image_url", "url": "..."}, ...], "prompt": "..."}`；
  - 视频编辑/口型替换：`{"media": [{"type": "video_url", "url": "..."}, {"type": "audio_url", "url": "..."}]}`。
- **`parameters`**（可选）：控制输出质量与格式：
  - `duration`: 视频时长（秒），常见值 5–10；
  - `resolution` / `size`: 分辨率，如 `"720P"`、`"1280*720"`、`"1024*576"`；
  - `aspect_ratio`: 宽高比，如 `"16:9"`（仅部分模型支持）；
  - `watermark`: 布尔值，是否添加水印（默认 `true`）；
  - `audio`: 布尔值，是否生成音频（部分模型默认 `false`）；
  - `style`: 风格重绘模型中指定风格编号（0–7）。

- **请求头**（必填）：
  - `Authorization: Bearer $DASHSCOPE_API_KEY`
  - `X-DashScope-Async: enable`
  - `Content-Type: application/json`

## 使用方式

所有视频生成任务均遵循标准异步流程：

1. **创建任务**：发送 `POST` 请求至对应地域的 Endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`），携带 `model`、`input` 和 `parameters`，返回 `task_id`。
2. **轮询结果**：使用 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（或新域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`）查询状态，直到 `status` 为 `"SUCCESS"`，响应体中 `output.video_url` 即为生成视频地址。

> **注意**：业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）已全面替代旧域名 `https://dashscope.aliyuncs.com`，且性能与稳定性更优。旧域名虽仍可用，但 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md) 明确建议迁移。务必确保 `WorkspaceId`、模型地域、API Key 三者严格一致，跨地域调用必然失败。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint URL、API Key 必须同属一个地域（如华北2北京、新加坡、美国弗吉尼亚等），否则鉴权失败或服务报错。业务空间 ID（`WorkspaceId`）是地域级概念，不可跨地域复用。
- **任务并发与配额**：多数模型有 RPS/QPS 限制（如 `emo-v1` 为 1 QPS，`liveportrait` 为 1 QPS），同时处理中任务数通常为 1–100 不等（详见各模型文档）。免费额度与计费单价因模型而异，需查阅 [模型列表与价格](https://help.aliyun.com/zh/model-studio/models)。
- **输入合规性**：数字人及肖像类模型（如 `emo-v1`、`liveportrait`、`animate-anyone`）**必须**先调用对应 `detect` 模型（如 `emo-detect-v1`）验证图片/视频质量，否则生成失败。
- **参数兼容性**：旧版模型（如 wan2.6 及早期）支持 `prompt_extend` 等特定参数，而 wan2.7+ 模型已移除该参数，改由自然语言描述分镜（如 “第1个镜头[0-3秒] 全景”）。直接复用旧参数将导致错误。
- **URL 格式规范**：所有 `media.url` 必须为公网可访问的 HTTPS 地址，且文件大小、格式（如 JPG/PNG/MP4/WAV）需符合各模型要求。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


