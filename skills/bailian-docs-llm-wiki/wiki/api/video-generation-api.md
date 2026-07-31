# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，涵盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、口型同步、风格重绘等场景。所有接口均采用异步调用模式，通过 `task_id` 轮询获取结果，任务有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格同地域，跨地域调用将失败。

## 支持的模型/功能

当前支持三大类模型家族，覆盖不同生成范式与业务需求：

- **通用视频生成模型**：  
  - `wan2.7-t2v`（文生视频）、`wan2.7-i2v`（图生视频，支持首帧/首尾帧/视频续写）、`wan2.7-r2v`（参考生视频）、`wan2.7-videoedit`（视频编辑）——[万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)  
  - `happyhorse-1.1-t2v`（文生）、`happyhorse-1.1-i2v`（图生首帧）、`happyhorse-1.1-r2v`（参考生）、`happyhorse-1.1-videoedit`（编辑）——[HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)  
  - `pixverse-c1-t2v`/`it2v`/`kf2v`/`r2v` 等系列模型，支持多镜头、水印、分辨率定制等——[爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)

- **人物驱动类模型（Portrait Animation）**：  
  - `emo-v1`（唱演）、`liveportrait`（播报）、`videoretalk`（口型替换）、`animate-anyone-gen2`（舞蹈模仿）、`video-style-transform`（风格重绘）等，均需先调用对应 detect 模型校验输入合规性。

- **专用增强模型**：  
  - `viduq3-turbo_text2video`（Vidu 文生）、`kling-v3-video-generation`（可灵文生/图生/编辑）、`pixverse-lipsync`（对口型）、`pixverse-upscale`（超清）等。

> **注意**：文档中存在协议路径不一致问题。万相 2.2 及早期模型（如 `wan2.2-kf2v-fla`）使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径，而 2.6+ 及所有新模型统一使用 `/api/v1/services/aigc/video-generation/video-synthesis` ——[万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md) 与 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md) 存在明显路径差异，务必按模型版本选择正确 endpoint。

## 关键参数

所有请求必须包含以下基础参数：

- **必选 Header**：  
  `X-DashScope-Async: enable`（异步开关，缺失将报错）、  
  `Authorization: Bearer $DASHSCOPE_API_KEY`、  
  `Content-Type: application/json`

- **核心 Body 字段**：  
  - `"model"`：精确模型名（如 `"wan2.7-t2v-2026-06-12"`），不可省略或简写；  
  - `"input"`：根据任务类型结构化输入：  
    - 文生视频：`{"prompt": "..."}`；  
    - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`；  
    - 首尾帧：`{"media": [{"type": "first_frame", ...}, {"type": "last_frame", ...}], "prompt": "..."}`；  
    - 参考生视频：`{"media": [{"type": "reference_image", ...}, ...], "prompt": "..."}`；  
    - 视频编辑/口型替换：`{"media": [{"type": "video", ...}, {"type": "audio", ...}], "prompt": "..."}`；  
  - `"parameters"`（可选）：常见字段包括 `"resolution"`（如 `"720P"`）、`"duration"`（秒）、`"watermark"`（布尔）、`"aspect_ratio"`（如 `"16:9"`）、`"size"`（如 `"1280*720"`）等。

## 使用方式

标准异步流程分两步：

1. **创建任务**：  
   `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`  
   （北京：`cn-beijing`；新加坡：`ap-southeast-1`；美国弗吉尼亚：`dashscope-us.aliyuncs.com`；德国法兰克福/日本东京：使用 `{WorkspaceId}.{region}.maas.aliyuncs.com`）  
   成功响应返回 `{"task_id": "xxx"}`。

2. **轮询结果**：  
   `GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   响应含 `"status"`（`QUEUED`/`RUNNING`/`SUCCESS`/`FAILED`）及成功时的 `"output.video_url"`。

> **注意**：部分旧版文档（如 [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)）仍使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径，该路径仅适用于 `wan2.2-animate-move` 等特定旧模型，新模型必须使用 `/video-generation/` 路径，否则返回 404。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint、API Key 必须同地域（如北京地域模型只能配北京 Endpoint 和北京 API Key），混用导致鉴权失败或服务报错。
- **业务空间专属域名**：华北2（北京）和新加坡地域已启用 `https://{WorkspaceId}.{region}.maas.aliyuncs.com` 新域名，性能与稳定性更优，**强烈建议迁移**；旧域名 `dashscope.aliyuncs.com` 仍可用但非最优。
- **任务并发与限流**：  
  - 多数模型“同时处理中任务数量”为 1（如 `liveportrait`、`videoretalk`）；  
  - `emo-v1` 免费额度 1800 秒/月，`wan2.7-t2v` 按秒计费；  
  - 所有 `task_id` 有效期 24 小时，过期后查询返回 `UNKNOWN`。
- **输入规范**：人物驱动类模型（EMO/LivePortrait/AnimateAnyone）**必须先调用 detect 模型**验证图片合规性，否则生成失败；图生/参考生视频需确保图像 URL 可公开访问且格式有效（JPEG/PNG/WebP）。

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
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


