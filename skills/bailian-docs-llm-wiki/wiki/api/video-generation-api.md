# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，覆盖文生视频、图生视频、参考生视频、视频编辑、数字人播报、口型替换、风格重绘等核心场景。所有接口均采用异步调用模式（`X-DashScope-Async: enable`），任务创建后返回 `task_id`，需轮询获取结果，`task_id` 有效期为 24 小时。开发者必须确保模型、Endpoint URL 与 API Key 属于同一地域，跨地域调用将失败。

## 支持的模型/功能

API 支持多系列模型，按能力可分为以下几类：

- **通用生成类**：  
  - `wan2.7` 系列（推荐）：支持首帧/首尾帧/视频续写（[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)）、文生视频（[万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)）、参考生视频（[万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)）、视频编辑（[万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)）。  
  - `happyhorse` 系列：支持图生视频、文生视频、参考生视频、视频编辑（[HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md) 等）。  
  - `pixverse`（爱诗）系列：支持文生视频、图生视频（首帧/首尾帧）、参考生视频、对口型、动作模仿、超清等（[爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md) 等）。  
  - `vidu`、`kling`：提供高性能文生视频与图生视频能力（[Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)、[可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)）。

- **人物驱动类（数字人/肖像动画）**：  
  - `liveportrait`、`emo`、`videoretalk`、`animateanyone`、`emoji`：均需先调用检测模型（如 `liveportrait-detect`）验证输入合规性，再生成视频（[图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)、[图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md) 等）。  
  - `wan2.2-s2v`（数字人）：基于单图+音频生成说话/唱歌视频，流程为 `wan2.2-s2v-detect` → `wan2.2-s2v`（[万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)）。

- **专用增强类**：  
  - `video-style-transform`：8种预设艺术风格重绘（[视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)）。  
  - `pixverse/pixverse-upscale`：4K超分（[爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)）。  
  - `wan2.2-animate-move` / `wan2.2-animate-mix`：图生动作、视频换人（[万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)、[万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)）。

> **注意**：`wan2.1`–`wan2.6` 等旧版模型（如 [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)）已逐步被 `wan2.7` 新版协议替代；新版统一使用 `/api/v1/services/aigc/video-generation/video-synthesis` 路径，而旧版 `wan2.2-kf2v` 等部分模型仍使用 `/api/v1/services/aigc/image2video/video-synthesis`（见文档33），二者 endpoint 不兼容。

## 关键参数

所有请求需包含以下必选 Header：
- `Content-Type: application/json`
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `X-DashScope-Async: enable`

请求体（JSON）核心字段：
- `model`: 模型标识符（如 `"wan2.7-t2v-2026-06-12"`、`"pixverse/pixverse-c1-t2v"`），必须与所选模型精确匹配。
- `input`: 输入数据容器，结构因模型而异：
  - 文生视频：`{"prompt": "..."}`  
  - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`  
  - 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "..."}`  
  - 参考生视频：`{"media": [{"type": "reference_image", "url": "..."}, ...], "prompt": "..."}`  
  - 数字人：`{"image_url": "...", "audio_url": "..."}`（需先通过 detect 模型）  
- `parameters`: 可选配置项，常见参数包括：
  - `duration`: 视频时长（秒），通常为 3–5 秒（部分模型支持最长 10 秒）  
  - `resolution` / `size`: 分辨率（如 `"720P"`、`"1280*720"`、`"540P"`）  
  - `watermark`: 布尔值，控制是否添加水印（默认 `true`）  
  - `aspect_ratio`: 宽高比（如 `"16:9"`）  
  - `style_level`: 动作风格强度（`emo` 模型特有，如 `"active"`）  
  - `mode`: 生成模式（`kling` 模型特有，如 `"std"`）

## 使用方式

1. **环境准备**：  
   - 在百炼控制台开通对应模型服务（如 PixVerse、Vidu、Wan2.7）。  
   - 获取目标地域的 API Key，并配置为环境变量 `DASHSCOPE_API_KEY`。  
   - 获取业务空间 ID（WorkspaceId），用于构造专属域名（推荐）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。

2. **发起[异步任务](../concepts/asynchronous-task.md)**：  
   ```bash
   curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
     -H 'X-DashScope-Async: enable' \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H 'Content-Type: application/json' \
     -d '{
       "model": "wan2.7-t2v-2026-06-12",
       "input": {"prompt": "一只猫在花园里追逐蝴蝶"},
       "parameters": {"duration": 5, "resolution": "720P"}
     }'
   ```
   成功响应含 `task_id`（如 `"task-abc123"`）。

3. **轮询获取结果**：  
   使用 `task_id` 查询任务状态（示例 URL：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`），直至 `status` 为 `"SUCCESS"`，响应中 `output.video_url` 即为生成视频地址。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint、API Key 必须同属一个地域（北京/新加坡/美国等），混用将导致鉴权失败或 `401 Unauthorized`（所有文档均强调此点，如 [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)）。  
- **任务生命周期**：`task_id` 仅在创建后 24 小时内有效，超时需重新提交任务。  
- **并发与限流**：各模型有独立 QPS/RPS 与同时处理任务数限制（如 `liveportrait` 同时仅支持 1 个任务运行），详见各模型资费文档。  
- **输入合规性**：数字人/肖像类模型（`liveportrait`, `emo`, `animateanyone`）**必须前置调用 detect 模型**验证图片质量，否则生成失败（[图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md) 明确要求此流程）。  
- **路径差异**：`wan2.7` 及主流新模型统一使用 `/video-generation/video-synthesis`，但 `wan2.2-animate-move`、`wan2.2-animate-mix`、`wan2.2-s2v` 等旧模型仍使用 `/image2video/video-synthesis`（见文档9、10、11），不可混用。  
- **弃用提示**：`wan2.6` 及更早版本（文档30–34）已被明确标注为“旧版协议”，官方推荐迁移至 `wan2.7` 新版（[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)）。

## 来源文档

- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


