# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，包括文生视频（T2V）、图生视频（I2V）、参考生视频（R2V）、首尾帧生视频（KF2V）、视频编辑、风格重绘及数字人播报等。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果，任务有效期为 24 小时。

## 支持的模型/功能

API 支持以下主流视频生成模型及对应能力：

- **文生视频（T2V）**：`happyhorse-1.1-t2v`、`wan2.7-t2v-2026-06-12`、`pixverse/pixverse-c1-t2v`、`kling/kling-v3-video-generation`、`vidu/viduq3-turbo_text2video`  
- **图生视频（I2V）**：  
  - 基于首帧：`happyhorse-1.1-i2v`、`wan2.7-i2v-2026-04-25`、`pixverse/pixverse-c1-it2v`、`vidu/viduq3-pro-fast_img2video`  
  - 基于首尾帧：`pixverse/pixverse-c1-kf2v`、`vidu/viduq3-turbo_start-end2video`、`wan2.2-kf2v-flash`（[万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)）  
- **参考生视频（R2V）**：`happyhorse-1.1-r2v`、`wan2.7-r2v-2026-06-12`、`pixverse/pixverse-c1-r2v`、`vidu/viduq3-ad_reference2video`  
- **视频编辑**：`happyhorse-1.0-video-edit`、`wan2.7-videoedit`、`wanx2.1-vace-plus`（[万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)）  
- **数字人与肖像动画**：`wan2.2-s2v`（说话/唱歌）、`emo-v1`（悦动人像）、`liveportrait`（灵动人像）、`videoretalk`（口型替换）、`animate-anyone-gen2`（舞蹈复刻）  
- **专用功能**：`video-style-transform`（8种艺术风格重绘）、`emoji`（表情包模板驱动）、`wan2.2-animate-move`（图生动作）  

> **注意**：`wan2.6` 及更早版本（如 `wan2.2`、`wanx2.1`）属于旧版协议，其 endpoint 路径为 `/api/v1/services/aigc/image2video/video-synthesis`，而 `wan2.7+`、`HappyHorse`、`PixVerse`、`Kling`、`Vidu` 等新模型统一使用 `/api/v1/services/aigc/video-generation/video-synthesis`。混用路径将导致 404 错误。

## 关键参数

所有请求必须包含以下基础参数：

- **`model`**（必选）：模型名称，严格区分大小写和版本后缀（如 `wan2.7-i2v-2026-04-25`）。  
- **`input`**（必选）：  
  - 文生视频：`{"prompt": "..."}`  
  - 图/参考生视频：`{"media": [{"type": "...", "url": "..."}], "prompt": "..."}`；部分旧模型（如 `wan2.2-kf2v-flash`）仍使用 `first_frame_url`/`last_frame_url` 字段。  
- **`parameters`**（可选）：常见字段包括：  
  - `resolution`（如 `"720P"`、`"1080P"`）或 `size`（如 `"1280*720"`）  
  - `duration`（秒数，通常支持 3–8 秒）  
  - `watermark`: `true`/`false`（默认 `true`）  
  - `audio`: `true`/`false`（仅部分模型支持音频生成）  
  - 多镜头控制：`wan2.7` 系列通过 `prompt` 内时间戳描述分镜；`wan2.6` 需显式设置 `"shot_type": "multi"` 和 `"prompt_extend": true`（[万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)）  

请求头必须包含：  
- `X-DashScope-Async: enable`（强制异步）  
- `Authorization: Bearer $DASHSCOPE_API_KEY`  
- `Content-Type: application/json`

## 使用方式

1. **地域对齐**：模型、Endpoint URL 与 API Key 必须同属一个地域（如华北2北京、新加坡、美国弗吉尼亚等），跨地域调用必然失败。  
2. **Endpoint 选择**：  
   - 新业务空间推荐使用专属域名：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`（北京）或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`（新加坡），性能与稳定性更优；  
   - 兼容旧域名：`https://dashscope.aliyuncs.com`（北京）、`https://dashscope-us.aliyuncs.com`（美国）、`https://dashscope-intl.aliyuncs.com`（国际）。  
3. **异步流程**：  
   - **步骤1（创建任务）**：`POST /api/v1/services/aigc/.../video-synthesis`，获取 `task_id`；  
   - **步骤2（轮询结果）**：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（或对应地域专属域名），直到 `status` 为 `"SUCCESS"`，响应中 `output.video_url` 即为生成视频地址。  
4. **SDK 支持**：DashScope SDK 已封装异步轮询逻辑，推荐开发者优先使用（[安装DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)）。

## 限制和注意事项

- **地域隔离**：华北2（北京）与新加坡地域的 API Key、Endpoint、模型实例完全独立，不可混用；美国、德国等区域暂不支持业务空间专属域名。  
- **任务并发**：多数模型限流为 **1 个同时处理中任务**（如 `emo-v1`、`videoretalk`），排队任务需等待前序完成。  
- **输入规范**：  
  - 数字人类模型（`s2v`、`emo`、`liveportrait`）要求输入图片为正面清晰肖像，需先调用对应 `detect` 模型校验；  
  - 视频编辑/重绘类模型对输入视频分辨率、时长有隐式要求（如 `video-style-transform` 推荐 540P–720P，≤30秒）。  
- **过期模型**：`wan2.6` 及更早系列（如 `wan2.2`、`wanx2.1`）已标记为“推荐优先选用 wan2.7”，其文档明确提示为遗留接口（[万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)），新项目应避免接入。  
- **错误处理**：缺失 `X-DashScope-Async` 请求头将返回 `current user api does not support synchronous calls`；`task_id` 超过 24 小时有效期查询将返回 `UNKNOWN` 状态。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


