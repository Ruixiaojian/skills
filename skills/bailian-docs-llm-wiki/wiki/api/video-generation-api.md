# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，包括文生视频（T2V）、图生视频（I2V）、参考生视频（R2V）、视频编辑、动作迁移、口型同步等。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果，任务 ID 有效期为 24 小时。统一使用 `POST /api/v1/services/aigc/video-generation/video-synthesis` 端点（部分旧版模型例外），且**模型、Endpoint URL 与 API Key 必须属于同一地域**，跨地域调用将失败。

## 支持的模型/功能

当前支持三大类模型家族，覆盖不同生成范式与业务场景：

- **文生视频（Text-to-Video）**：输入纯文本提示词生成视频，主流模型包括 `vidu/viduq3-turbo_text2video`、`kling/kling-v3-video-generation`、`wan2.7-t2v-2026-06-12` 和 `happyhorse-1.1-t2v`。其中万相2.7支持多镜头叙事（通过 [prompt](../guides/prompt.md) 描述分镜），而 Vidu 和 Kling 提供分辨率、时长等精细化控制参数 [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)。

- **图生视频（Image-to-Video）**：基于单张首帧图像生成视频（I2V），或基于首尾帧图像生成平滑过渡视频（KF2V）。万相2.7统一支持首帧、首尾帧、视频续写三类任务；爱诗（PixVerse）和 Vidu 均提供独立的 `*-it2v` 和 `*-kf2v` 模型；HappyHorse 也支持首帧模式 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。

- **参考生视频与专业编辑**：  
  - 参考生视频（R2V）：传入多张角色/物体参考图（如 PixVerse `pixverse-c1-r2v`、Vidu `viduq3-ad_reference2video`、HappyHorse 多图像模式），结合 [prompt](../guides/prompt.md) 生成角色一致的新视频；  
  - 视频编辑：支持风格迁移（如 `wan2.7-videoedit`）、局部替换、指令编辑（如“转为黏土风”）；  
  - 动作/口型/形象迁移：包括图生动作（`wan2.2-animate-move`）、视频换人（`wan2.2-animate-mix`）、数字人（`wan2.2-s2v`）、对口型（`pixverse/pixverse-lipsync`）、声动人像（`videoretalk`）等垂直能力 [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)。

> **注意**：文档中存在新旧协议并存现象。万相2.7系列（如 `wan2.7-t2v`、`wan2.7-r2v`）使用新版 `/video-generation/video-synthesis` 接口；而万相2.2/2.5/2.6 等旧版模型（如 `wan2.2-kf2v-fla`、`wan2.6-r2v`）在部分文档中仍指向 `/image2video/video-synthesis` 路径（见文档33、32），但实际生产环境应优先采用新版统一路径，旧路径已逐步归档。

## 关键参数

所有请求必须包含以下核心字段：

- `model`：模型标识符（如 `"vidu/viduq3-turbo_text2video"`），需与所选地域模型市场中的名称完全一致；
- `input`：根据任务类型结构化输入：
  - 文生视频：`{"prompt": "..."}`；
  - 图生视频：`{"media": [{"type": "image", "url": "..."}], "prompt": "..."}`；
  - 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "..."}`；
  - 参考生视频：`{"media": [{"type": "image_url", "url": "..."}, ...], "prompt": "..."}`；
  - 对口型/动作模仿：`{"media": [{"type": "video_url", "url": "..."}, {"type": "audio_url"|"video_url", "url": "..."}]}`；
- `parameters`（可选）：控制输出质量，常见参数包括：
  - `duration`: 视频时长（秒），通常为 3–5 秒；
  - `resolution` / `size`: 分辨率（如 `"720P"`、`"1280*720"`、`"1024*576"`）；
  - `watermark`: 布尔值，是否添加水印（默认 `true`）；
  - `aspect_ratio`: 宽高比（如 `"16:9"`，Kling 特有）；
  - `audio`: 布尔值，是否生成音频（部分模型支持）；
  - `style`: 风格重绘时指定风格编号（如 `0` 表示日式漫画）。

## 使用方式

1. **前置准备**：  
   - 在百炼控制台开通对应模型服务；  
   - 获取目标地域的 API Key 并配置至环境变量 `DASHSCOPE_API_KEY`；  
   - 获取业务空间 ID（WorkspaceId），用于构造专属域名（推荐）；  

2. **发起异步任务**：  
   ```bash
   curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
     -H 'X-DashScope-Async: enable' \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H 'Content-Type: application/json' \
     -d '{...}'
   ```
   > **注意**：`X-DashScope-Async: enable` 为强制请求头，缺失将报错：“current user api does not [support](../guides/support.md) synchronous calls” [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)。

3. **轮询结果**：  
   使用返回的 `task_id` 向 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（或专属域名对应路径）轮询，直至 `status` 为 `"SUCCESS"`，响应体中 `output.video_url` 即为生成视频地址。

## 限制和注意事项

- **地域强一致性**：模型、Endpoint、API Key 必须同属一个地域（如华北2北京），混用将导致鉴权失败或 404 错误；
- **任务生命周期**：`task_id` 仅在创建后 24 小时内有效，超时需重新提交任务；
- **并发与限流**：多数模型（如 `emo-v1`、`liveportrait`、`videoretalk`）同时处理中任务数限制为 1，QPS/RPS 通常为 1–5，具体见各模型资费页；
- **输入规范**：数字人、表情包、LivePortrait 等模型要求先调用 `*-detect` 接口校验图片合规性，否则任务可能失败；
- **URL 协议**：所有 `media.url` 必须为 HTTPS 协议，且需公网可访问（OSS 或 CDN 地址推荐）；
- **弃用提醒**：万相2.1–2.6 系列（如 `wanx2.1-vace-plus`、`wan2.2-kf2v-fla`）已标记为 Legacy，官方明确推荐迁移到万相2.7统一接口 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


