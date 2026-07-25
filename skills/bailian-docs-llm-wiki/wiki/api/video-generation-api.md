# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，涵盖文生视频、图生视频、参考生视频、视频编辑、数字人驱动、风格重绘等核心场景。所有接口均采用异步调用模式（`X-DashScope-Async: enable`），需通过 `task_id` 轮询获取结果，任务有效期为 24 小时。统一使用 `/api/v1/services/aigc/video-generation/video-synthesis` 端点（部分旧版模型例外），且**模型、Endpoint URL 与 API Key 必须同地域**。

## 支持的模型/功能

当前支持三大类模型家族及对应能力：

- **万相（Wan）系列**：覆盖全模态生成能力。`wan2.7` 为最新主力版本，支持**首帧生视频、首尾帧生视频、视频续写**三大任务 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)；同时提供参考生视频（`wan2.7-r2v-*`）、文生视频（`wan2.7-t2v-*`）、视频编辑（`wan2.7-videoedit`）等专用模型。旧版 `wan2.6` 及更早模型（如 `wan2.2-kf2v-flash`、`wanx2.1-vace-plus`）仍可用，但功能受限且协议不同 [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)。

- **HappyHorse、PixVerse（爱诗）、Vidu、Kling（可灵）等第三方模型**：均提供文生视频与图生视频能力，部分支持首尾帧、参考生视频或视频超清。例如 HappyHorse 支持美式/日式漫画风格迁移，PixVerse 提供视频动作模仿与对口型，Vidu 支持广告级参考生视频 [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)。

- **数字人与口型驱动专用模型**：包括 `wan2.2-s2v`（单图+音频生成说话视频）、`emo-v1`（悦动人像EMO）、`liveportrait`（灵动人像）、`videoretalk`（视频口型替换）等，均需先调用检测模型（如 `emo-detect-v1`）预检输入合规性。

> **注意**：文档中存在 endpoint 路径不一致问题。万相 2.2 系列的首尾帧模型（文档32）和图生动作/换人模型（文档5、6）使用 `/api/v1/services/aigc/image2video/video-synthesis`，而其余所有新模型（wan2.7、HappyHorse、PixVerse、Vidu、Kling 等）均使用 `/api/v1/services/aigc/video-generation/video-synthesis`。开发者务必按模型版本选择正确路径。

## 关键参数

- **必选请求头**：`X-DashScope-Async: enable`（缺失将报错）、`Authorization: Bearer $DASHSCOPE_API_KEY`、`Content-Type: application/json`。
- **核心请求体字段**：
  - `model`: 模型名称（如 `"wan2.7-t2v-2026-06-12"`、`"pixverse/pixverse-c1-t2v"`），必须与所选模型精确匹配。
  - `input`: 包含任务所需输入。结构因模型而异：
    - 文生视频：`{"prompt": "文本描述"}`
    - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`
    - 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "..."}`
    - 参考生视频：`{"media": [{"type": "image_url", "url": "..."}, ...], "prompt": "..."}`
    - 数字人：`{"image_url": "...", "audio_url": "..."}`（`wan2.2-s2v`）或 `{"media": [{"type": "video_url", "url": "..."}, {"type": "audio_url", "url": "..."}]}`（`pixverse/pixverse-lipsync`）
  - `parameters`: 可选控制参数，常见项包括：
    - `duration`: 视频时长（秒），通常为 3–5 秒
    - `resolution` / `size`: 分辨率（如 `"720P"`、`"1280*720"`）
    - `watermark`: 是否添加水印（`true`/`false`）
    - `prompt_extend`: 是否启用提示词扩展（部分旧版模型需显式设置）

## 使用方式

1. **准备环境**：确保模型、Endpoint URL 和 API Key 同属一个地域（如华北2北京）。推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非通用 `dashscope.aliyuncs.com` [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。
2. **创建任务**：向对应地域的 `POST /api/v1/services/aigc/.../video-synthesis` 发送请求，携带 `model`、`input` 和 `parameters`，获取 `task_id`。
3. **轮询结果**：使用 `GET https://<base-url>/api/v1/tasks/{task_id}` 查询状态，直至 `status` 为 `"SUCCESS"`，响应中 `output.video_url` 即为生成视频地址。
4. **错误处理**：关注 `status` 字段（`"QUEUING"`/`"RUNNING"`/`"SUCCESS"`/`"FAILED"`）及 `error_code`/`error_message`。

## 限制和注意事项

- **地域强约束**：跨地域调用必然失败，必须严格保证模型开通地域、Endpoint 地域、API Key 所属地域三者一致。
- **异步时效性**：`task_id` 有效期仅 24 小时，超时后无法查询；任务排队或执行中状态需主动轮询，不可假设即时返回。
- **输入合规性**：数字人类模型（`emo-v1`、`liveportrait`、`wan2.2-s2v`）必须先调用对应检测模型（如 `emo-detect-v1`）验证图片质量，否则生成失败。
- **模型兼容性**：`wan2.7` 系列为新版协议，旧版 `wan2.6` 及更早模型（文档29–33）虽仍可用，但功能较弱（如仅支持单镜头）、参数配置不同（如依赖 `shot_type`），且部分 endpoint 路径不同，迁移前需仔细核对。
- **资源限制**：各模型有独立的 QPS/并发数限制（如 `emo-v1` 同时处理中任务数为 1），详见各模型资费文档。

## 来源文档

- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
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
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


