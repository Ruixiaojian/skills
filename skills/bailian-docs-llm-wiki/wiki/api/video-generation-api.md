# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，包括文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、动作迁移、口型同步等。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果，任务有效期为 24 小时。开发者必须确保模型、Endpoint URL 与 API Key 三者所属地域一致，跨地域调用将失败 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。

## 支持的模型/功能

当前支持以下主流视频生成模型及对应能力：

- **文生视频（T2V）**：`happyhorse-1.1-t2v`、`wan2.7-t2v-2026-06-12`、`vidu/viduq3-turbo_text2video`、`pixverse/pixverse-c1-t2v`、`kling/kling-v3-video-generation`  
- **图生视频（I2V）**：  
  - 首帧：`happyhorse-1.1-i2v`、`wan2.7-i2v`、`pixverse/pixverse-c1-it2v`、`vidu/viduq3-pro-fast_img2video`  
  - 首尾帧：`pixverse/pixverse-c1-kf2v`、`vidu/viduq3-turbo_start-end2video`、`wan2.2-kf2v-fla`（旧版）  
- **参考生视频（R2V）**：`happyhorse-1.1-r2v`、`wan2.7-r2v-2026-06-12`、`pixverse/pixverse-c1-r2v`、`vidu/viduq3-ad_reference2video`  
- **视频编辑**：`happyhorse-1.1-videoedit`、`wan2.7-videoedit`、`wanx2.1-vace-plus`（旧版）  
- **专用能力模型**：  
  - 动作迁移：`wan2.2-animate-move`、`pixverse/pixverse-motioncontrol`  
  - 角色替换：`wan2.2-animate-mix`  
  - 数字人播报：`wan2.2-s2v`、`liveportrait`、`emo-v1`  
  - 口型同步：`videoretalk`、`pixverse/pixverse-lipsync`  
  - 风格重绘：`video-style-transform`  
  - 视频超分：`pixverse/pixverse-upscale`  

> **注意**：万相系列存在新旧两套协议。`wan2.7` 模型统一使用 `/api/v1/services/aigc/video-generation/video-synthesis` 路径；而 `wan2.2`/`wan2.5`/`wan2.6` 等旧版模型中，部分（如 `wan2.2-kf2v-fla`）仍使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径 [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)。混用路径将导致 404 错误。

## 关键参数

所有请求需包含以下必选 Header：
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `Content-Type: application/json`
- `X-DashScope-Async: enable`

核心请求体结构为：
```json
{
  "model": "model-name",
  "input": { ... },
  "parameters": { ... }
}
```

常用 `parameters` 字段：
- `duration`: 视频时长（秒），常见值 `5` 或 `8`
- `resolution` / `size`: 分辨率，如 `"720P"`、`"1280*720"`、`"1024*576"`
- `watermark`: 布尔值，控制是否添加水印（默认 `true`）
- `audio`: 布尔值，控制是否生成音频（部分模型默认禁用）
- `aspect_ratio`: 宽高比（如 `"16:9"`，仅 `kling` 支持）
- `mode`: 模式标识（如 `kling` 的 `"std"` 或 `"pro"`）

`input` 结构依任务类型而异：
- 文生视频：`{"prompt": "文本描述"}`
- 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`
- 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "..."}`
- 参考生视频：`{"media": [{"type": "image_url", "url": "..."}, ...], "prompt": "..."}`
- 视频编辑/动作迁移：`{"media": [{"type": "video_url", "url": "..."}, {"type": "image_url", "url": "..."}], "prompt": "..."}`
- 口型同步：`{"media": [{"type": "video_url", "url": "..."}, {"type": "audio_url", "url": "..."}]}`

> **注意**：`pixverse` 和 `wan2.7` 的多镜头能力实现方式不同——`pixverse` 依赖 `prompt` 自然语言描述（如“第1个镜头[0-3秒]...”），而旧版 `wan2.6` 需显式设置 `"prompt_extend": true` 和 `"shot_type": "multi"` [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)。新模型已弃用 `shot_type` 参数。

## 使用方式

1. **开通服务**：在百炼控制台模型市场搜索并开通对应模型（如 `HappyHorse`、`Vidu`、`PixVerse`）。
2. **配置环境**：获取对应地域的 API Key，并设为环境变量 `DASHSCOPE_API_KEY`。
3. **构造请求**：
   - Endpoint URL 格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（华北2为 `cn-beijing`，新加坡为 `ap-southeast-1`）；
   - `WorkspaceId` 在业务空间详情页获取；
   - 所有请求均为 `POST`，Body 为 JSON。
4. **轮询结果**：使用返回的 `task_id` 向 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（或对应地域专属域名）查询状态，直至 `output.video_url` 返回有效链接。

示例（Vidu 文生视频）：
```bash
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
  -H 'X-DashScope-Async: enable' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "vidu/viduq3-turbo_text2video",
    "input": {"prompt": "一只小猫在月光下奔跑"},
    "parameters": {"size": "1024*576", "duration": 5}
  }'
```

## 限制和注意事项

- **地域强绑定**：模型、Endpoint、API Key 必须同属一个地域（如华北2），否则鉴权失败或返回 `401`/`404`。
- **异步时效性**：`task_id` 有效期严格为 24 小时，超时后无法查询结果。
- **并发与限流**：多数模型单账号 RPS 限制为 1–5，同时处理中任务数通常为 1–100（详见各模型文档的“资费与限流”章节）。
- **输入要求**：
  - 图像 URL 需公网可访问、格式为 JPG/PNG/WebP，尺寸建议 ≥512×512；
  - 视频 URL 需为 MP4，时长 ≤30 秒，分辨率 ≥360P；
  - 音频需为 WAV/MP3，采样率 ≥16kHz，人声清晰。
- **路径差异**：除通用 `/video-synthesis` 外，`video-style-transform` 模型仍使用旧路径 `https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（不支持 WorkspaceId 域名）[视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)。
- **废弃模型**：`wan2.1`/`wan2.2`/`wan2.5`/`wan2.6` 系列已标记为“推荐优先选用 wan2.7”，旧版文档明确提示其功能覆盖有限且协议不兼容。

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
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
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
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


