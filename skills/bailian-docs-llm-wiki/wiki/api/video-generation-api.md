# video generation api

百炼平台的 Video Generation API 提供多种文生视频、图生视频、参考生视频及视频编辑能力，支持 HappyHorse、万相（WanX）、爱诗（PixVerse）、Vidu、可灵（Kling）等主流模型。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果，任务有效期为 24 小时。开发者须确保模型、Endpoint URL 与 API Key 严格同地域，跨地域调用将失败。

## 支持的模型/功能

当前支持四大类视频生成范式，对应不同模型家族：

- **文生视频（Text-to-Video）**：输入文本提示词生成视频，如 `wan2.7-t2v-2026-06-12`、`vidu/viduq3-turbo_text2video`、`kling/kling-v3-video-generation`、`happyhorse-1.1-t2v`。  
- **图生视频（Image-to-Video）**：基于单张首帧图像生成视频（如 `pixverse/pixverse-c1-it2v`、`vidu/viduq3-pro-fast_img2video`），或基于首尾帧图像生成平滑过渡视频（如 `pixverse/pixverse-c1-kf2v`、`vidu/viduq3-turbo_start-end2video`）。万相2.7还支持首帧+音频、视频续写等扩展能力 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。  
- **参考生视频（Reference-to-Video）**：传入多张人物/物体参考图，结合文本描述生成角色一致的视频，适用于广告、IP形象复现等场景，如 `happyhorse-1.1-r2v`、`wan2.7-r2v-2026-06-12`、`vidu/viduq3-ad_reference2video`。  
- **视频编辑与增强**：包括视频风格重绘（`video-style-transform`）、视频超清（`pixverse/pixverse-upscale`）、口型替换（`videoretalk`）、动作模仿（`pixverse/pixverse-motioncontrol`）、对口型（`pixverse/pixverse-lipsync`）等专项能力。  

> **注意**：万相系列存在新旧协议并存现象。`wan2.7` 模型统一使用 `/api/v1/services/aigc/video-generation/video-synthesis` 路径；而 `wan2.2-kf2v-fla` 等旧版模型仍使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径 [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)，调用时需严格区分。

## 关键参数

所有请求必须包含以下基础字段：

- `model`：模型标识符（如 `wan2.7-t2v-2026-06-12`），需与所选模型完全一致。  
- `input`：核心输入数据结构，根据任务类型变化：
  - 文生视频：`{"prompt": "..."}`  
  - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`  
  - 首尾帧：`{"media": [{"type": "first_frame", ...}, {"type": "last_frame", ...}], "prompt": "..."}`  
  - 参考生视频：`{"media": [{"type": "reference_image", "url": "..."}, ...], "prompt": "..."}`  
  - 视频编辑：`{"media": [{"type": "video", "url": "..."}], "prompt": "..."}`  
- `parameters`（可选）：控制输出质量与行为，常见字段包括：
  - `duration`: 视频时长（秒），通常支持 3–5 秒（部分模型支持最长 10 秒）  
  - `resolution` / `size`: 分辨率，如 `"720P"`、`"1280*720"`、`"1024*576"`  
  - `watermark`: 布尔值，控制是否添加水印（默认 `true`）  
  - `audio`: 布尔值，控制是否生成音频（仅部分模型支持）  
  - `style`: 风格索引（如 `video-style-transform` 中 `0` 表示日式漫画）  

必需请求头：
- `Authorization: Bearer $DASHSCOPE_API_KEY`  
- `Content-Type: application/json`  
- `X-DashScope-Async: enable`（**必须设置**，否则报错：“current user api does not support synchronous calls”）  

## 使用方式

1. **准备环境**：开通对应模型服务，获取同地域 API Key，并配置为环境变量 `DASHSCOPE_API_KEY`。  
2. **构造请求**：使用业务空间专属域名（推荐）或通用域名：
   - 专属域名（高性能）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`  
   - 通用域名（兼容性）：`https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（仅限北京地域）  
   > **注意**：`{WorkspaceId}` 需从百炼控制台【业务空间详情】页获取，不可省略 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。  
3. **提交任务**：`POST` 请求创建任务，响应中提取 `task_id`。  
4. **轮询结果**：使用 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（或专属域名对应路径）查询状态，直到 `status` 为 `"SUCCESS"`，`output.video_url` 字段返回可下载视频地址。  

## 限制和注意事项

- **地域强绑定**：模型、Endpoint、API Key 必须同属一个地域（如华北2北京），混用将直接失败。新加坡、美国、德国、日本等地域均有独立 Endpoint 和 WorkspaceId。  
- **任务时效性**：`task_id` 有效期为 24 小时，超时后无法查询结果，返回 `UNKNOWN` 状态。  
- **并发与限流**：多数模型任务下发 RPS 限制为 1，同时处理中任务数上限为 1（如 `videoretalk`、`emo-v1`），需避免高频重复提交。  
- **输入合规性**：数字人/肖像类模型（如 `emo-v1`、`liveportrait`、`animate-anyone`）要求先调用 `detect` 模型校验图片质量，否则生成失败。  
- **路径差异**：除主流 `/video-generation/video-synthesis` 外，部分旧模型（如 `wan2.2-kf2v-fla`）仍使用 `/image2video/video-synthesis` 路径，务必核对文档 [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)。  
- **多镜头支持**：仅 `wan2.7`、`kling-v3-omni` 等新版模型原生支持 [prompt](../guides/prompt.md) 内分镜描述（如“第1个镜头[0-3秒] 全景：...”），旧版 `wan2.6` 需显式设置 `"prompt_extend": true, "shot_type":"multi"`。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
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


