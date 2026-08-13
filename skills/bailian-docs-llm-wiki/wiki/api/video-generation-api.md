# video generation api

百炼平台的 Video Generation API 提供统一的异步接口，支持多种视频生成与编辑范式，包括文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、动作迁移、口型同步等。所有任务均采用“创建任务 → 轮询获取结果”两阶段流程，典型耗时为 1–5 分钟（部分模型如 wanx2.1-vace-plus 达 5–10 分钟）。开发者需严格保证模型、Endpoint URL 与 API Key 同属一个地域，跨地域调用将失败。

## 支持的模型/功能

API 统一接入多个厂商与自研模型，按能力划分为以下几类：

- **通用视频生成**：万相系列（`wan3.0-video`、`wan2.7-*`）、HappyHorse、爱诗（PixVerse）、可灵（Kling）、Vidu，覆盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑等全场景。
- **人像驱动类**：数字人（`wan2.2-s2v`）、舞动人像（`animate-anyone-gen2`）、悦动人像（`emo-v1`）、灵动人像（`liveportrait`）、声动人像（`videoretalk`）、表情包（`emoji`），均需先调用检测模型（如 `emo-detect-v1`）校验输入合规性 [原文标题](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)。
- **专业编辑类**：视频风格重绘（`video-style-transform`）、视频超清（`pixverse/pixverse-upscale`）、视频动作模仿（`pixverse/pixverse-motioncontrol`）、视频对口型（`pixverse/pixverse-lipsync`）。
- **遗留模型**：`wan2.6` 及更早版本（如 `wanx2.1-vace-plus`、`wan2.2-animate-move`）仍可用，但官方明确推荐迁移到 `wan2.7` 或 `wan3.0` 新版协议 [原文标题](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。

> **注意**：万相系列中，`wan2.7` 及以上模型统一使用 `/api/v1/services/aigc/video-generation/video-synthesis` 路径；而 `wan2.2-animate-move`、`wan2.2-animate-mix` 等旧模型使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径，二者 endpoint 不互通 [原文标题](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)。

## 关键参数

所有请求必须包含以下基础字段：

- `model`：模型标识符（如 `"wan3.0-video"`、`"pixverse/pixverse-c1-t2v"`），需与所选模型市场中的名称完全一致。
- `input`：核心输入数据，结构因任务类型而异：
  - 文生视频：`{"prompt": "文本描述"}`
  - 图生视频（首帧）：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`
  - 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "..."}`
  - 参考生视频：`{"media": [{"type": "image_url", "url": "..."}, {"type": "video_url", "url": "..."}], "prompt": "..."}`
  - 视频编辑/风格重绘：`{"video_url": "..."}` 或 `{"media": [{"type": "video", "url": "..."}]}`。
- `parameters`：可选控制参数，常见字段包括：
  - `duration`：视频时长（秒），范围通常为 2–10 秒（`wan3.0-video` 最长支持 30 秒）。
  - `resolution` / `size` / `aspect_ratio`：输出分辨率（如 `"720P"`、`"1280*720"`、`"16:9"`）。
  - `watermark`：布尔值，控制是否添加水印（默认 `true`）。
  - `audio`：布尔值，控制是否生成音频（部分模型默认禁用）。
  - `style`：风格重绘模型专用（如 `0` 表示日式漫画）[原文标题](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)。

## 使用方式

1. **准备环境**：确保已开通对应模型服务，在百炼控制台获取该地域的 API Key，并配置至环境变量 `DASHSCOPE_API_KEY`。
2. **构造请求**：
   - Endpoint URL 必须匹配业务空间 ID 和地域，例如北京地域：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`。
   - 请求头必需包含：`Content-Type: application/json`、`Authorization: Bearer $DASHSCOPE_API_KEY`、`X-DashScope-Async: enable`。
3. **提交任务**：发送 `POST` 请求，获取 `task_id`（有效期 24 小时）。
4. **轮询结果**：使用 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（或对应地域的 workspace URL）查询状态，直到 `status == "SUCCESS"`，响应体中 `output.video_url` 即为生成视频地址。

> **注意**：部分模型（如 `wan2.2-s2v`）在文档中仍示例使用旧域名 `https://dashscope.aliyuncs.com`，但官方强烈建议迁移至业务空间专属域名以获得更高稳定性与性能 [原文标题](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)。

## 限制和注意事项

- **地域强绑定**：模型、API Key、Endpoint URL 必须同属华北2（北京）、新加坡、美国（弗吉尼亚）、德国（法兰克福）、日本（东京）等同一地域，混用将导致鉴权失败或 403 错误。
- **异步时效性**：`task_id` 仅在 24 小时内有效，超时需重新提交任务；轮询间隔建议 ≥3 秒，避免触发限流。
- **输入约束**：
  - 图片/视频 URL 必须公网可访问且 HTTPS 协议；
  - `prompt` 长度建议 ≤512 字符，避免截断；
  - [多模态](../concepts/multimodal.md)输入（如参考图+视频）需明确指定 `type` 字段（`"image_url"`、`"video_url"`、`"first_frame"` 等）。
- **计费与限流**：各模型独立计费（按秒/次），并发任务数受 RPS/QPS 限制（如 `emo-v1` 同时处理中任务上限为 1），详情见各模型资费文档。
- **模型弃用提示**：`wan2.6` 及更早模型（如文档31–35）已被标记为“推荐优先选用 wan2.7”，其功能覆盖有限且不支持新版多任务协议，新项目应避免依赖。

## 来源文档

- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
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
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
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


