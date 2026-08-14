# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，包括文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、口型替换、风格重绘等。所有接口均采用异步调用模式，需先创建任务获取 `task_id`，再轮询查询结果。核心模型由 HappyHorse、万相（Wan）、爱诗（PixVerse）、可灵（Kling）、Vidu 等系列提供，覆盖从基础生成到专业级多模态编辑的全场景需求。

## 支持的模型/功能

API 统一通过 `/api/v1/services/aigc/video-generation/video-synthesis` 路径调用，具体能力由 `model` 参数指定：

- **文生视频（T2V）**：支持 `wan2.7-text2video`、`pixverse/pixverse-c1-t2v`、`kling/kling-v3-video-generation`、`vidu/viduq3-turbo_text2video` 等模型；万相2.7支持多镜头叙事（通过 [prompt](../guides/prompt.md) 描述分镜），而旧版 wan2.6 需显式设置 `"prompt_extend": true` [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)。
- **图生视频（I2V）**：含首帧（`wan2.7-i2v`、`pixverse/pixverse-c1-it2v`）、首尾帧（`pixverse/pixverse-c1-kf2v`、`vidu/viduq3-turbo_start-end2video`）、视频续写（仅 wan2.7）；注意万相2.2 首尾帧模型使用独立路径 `/api/v1/services/aigc/image2video/video-synthesis` [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)。
- **参考生视频（R2V）**：支持多图、图文混输（`wan2.7-r2v-2026-06-12`）、Omni 模式（`pixverse/pixverse-v6-r2v-omni`）、广告专用（`vidu/viduq3-ad_reference2video`）。
- **视频编辑类**：包括指令编辑（`wan2.7-videoedit`）、视频迁移、风格重绘（`video-style-transform`）、超清（`pixverse/pixverse-upscale`）、动作模仿（`pixverse/pixverse-motioncontrol`）等。
- **人像驱动类**：含数字人（`wan2.2-s2v`）、唱演视频（`emo-v1`）、播报视频（`liveportrait`）、口型替换（`videoretalk`、`pixverse/pixverse-lipsync`）、舞蹈生成（`animate-anyone-gen2`）等，此类模型通常需前置图像检测（如 `emo-detect-v1`）[图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)。

> **注意**：万相2.7 及以上版本已统一为 `video-generation` 路径，而部分早期模型（如 wan2.2-animate-move、wan2.2-animate-mix）仍使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径，调用时需严格匹配文档说明。

## 关键参数

- **必选请求头**：
  - `Authorization: Bearer $DASHSCOPE_API_KEY`
  - `X-DashScope-Async: enable`
  - `Content-Type: application/json`
- **核心请求体字段**：
  - `model`: 模型标识符（如 `wan2.7-text2video`, `pixverse/pixverse-c1-t2v`），必须与所选地域开通的模型一致。
  - `input`: 根据任务类型提供不同结构：
    - 文生视频：`{"prompt": "文本描述"}`
    - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`
    - 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "..."}`
    - 参考生视频：`{"media": [{"type": "reference_image", ...}, {"type": "video_url", ...}], "prompt": "..."}`
    - 口型替换：`{"media": [{"type": "video_url", ...}, {"type": "audio_url", ...}]}`  
  - `parameters`: 可选配置项，常见参数包括：
    - `duration`: 视频时长（秒），范围通常为 2–30 秒（万相3.0 最长支持 30 秒）
    - `resolution` / `size` / `aspect_ratio`: 分辨率（如 `"720P"`、`"1280*720"`、`"16:9"`）
    - `watermark`: 是否添加水印（布尔值）
    - `audio`: 是否生成音频（部分模型默认关闭）

## 使用方式

1. **地域对齐**：确保模型开通地域、Endpoint URL 和 API Key 三者完全一致。跨地域调用将失败。
2. **Endpoint 构建**：优先使用业务空间专属域名（推荐）：
   - 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`
   - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`
   - `{WorkspaceId}` 在控制台「业务空间详情」中获取；旧域名 `dashscope.aliyuncs.com` 仍可用但不推荐。
3. **异步流程**：
   - 步骤1：`POST` 创建任务，响应中提取 `task_id`（有效期 24 小时）。
   - 步骤2：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}` 轮询状态（建议间隔 ≥5 秒），直至 `status == "SUCCESS"`，返回 `output.video_url`。
4. **SDK 支持**：DashScope SDK 已封装[异步任务](../concepts/async-task.md)管理（如 `generate_video` 方法），推荐用于生产环境。

## 限制和注意事项

- **地域隔离**：华北2（北京）与新加坡地域的 API Key 和 Endpoint 不互通，混用将导致鉴权失败 [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)。
- **并发与配额**：多数人像类模型（如 `emo-v1`、`liveportrait`、`videoretalk`）限制「同时处理中任务数量」为 1，需排队执行；免费额度按模型单独计算（如 `emo-v1` 1800 秒/月）。
- **输入规范**：人像驱动类模型（EMO、LivePortrait、AnimateAnyone）必须先调用对应 detect 模型校验图片合规性，否则任务失败。
- **路径差异**：除主流 `video-generation` 路径外，部分功能使用独立路径：
  - 图生动作/换人：`/api/v1/services/aigc/image2video/video-synthesis`
  - 视频风格重绘：`/api/v1/services/aigc/video-generation/video-synthesis`（同主路径，但 model 为 `video-style-transform`）
- **模型演进**：万相2.7 已整合首帧、首尾帧、视频续写三大能力，旧版（2.1–2.6）文档明确标注为“推荐优先选用新版”，避免使用已标记为 legacy 的模型 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
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
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


