# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，包括文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、动作迁移、口型同步等。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果，任务有效期为 24 小时。调用前必须确保模型、Endpoint URL 与 API Key 属于同一地域，跨地域调用将失败。

## 支持的模型/功能

API 统一通过 `/api/v1/services/aigc/video-generation/video-synthesis` 端点提供服务，具体能力由 `model` 参数指定，主流模型按能力分类如下：

- **文生视频（T2V）**：`vidu/viduq3-turbo_text2video`、`pixverse/pixverse-c1-t2v`、`kling/kling-v3-video-generation`、`wan2.7-text2video`、`wan3.0-video`  
- **图生视频（I2V）**：支持首帧（`wan2.7-i2v`、`vidu/viduq3-pro-fast_img2video`）、首尾帧（`vidu/viduq3-turbo_start-end2video`、`pixverse/pixverse-c1-kf2v`）、视频续写（仅 wan2.7）  
- **参考生视频（R2V）**：支持多图/多视频+文本融合（`wan2.7-r2v-2026-06-12`、`pixverse/pixverse-v6-r2v-omni`、`vidu/viduq3-ad_reference2video`）  
- **视频编辑（Video Editing）**：风格迁移、局部替换、指令编辑（`wan2.7-videoedit`、`happyhorse-video-edit`）  
- **人物驱动类**：数字人播报（`wan2.2-s2v`）、唱演视频（`emo-v1`）、表情包（`emoji`）、舞蹈复刻（`animate-anyone-gen2`）、口型替换（`videoretalk`、`pixverse/pixverse-lipsync`）、动作模仿（`pixverse/pixverse-motioncontrol`）、视频换人（`wan2.2-animate-mix`）、图生动作（`wan2.2-animate-move`）  
- **后处理类**：视频超清（`pixverse/pixverse-upscale`）、风格重绘（`video-style-transform`）

> **注意**：部分旧版模型（如 `wan2.1`–`wan2.6` 系列）仍可通过 `/api/v1/services/aigc/image2video/video-synthesis` 或 `/api/v1/services/aigc/video-generation/video-synthesis` 调用，但协议与参数结构已迭代；[万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md) 明确指出“推荐优先选用”新版 wan2.7，旧版仅限兼容场景。

## 关键参数

所有请求必须包含以下基础参数：

- **`model`**（必填）：模型标识符，如 `pixverse/pixverse-c1-t2v`、`wan2.7-i2v`，详见各模型文档  
- **`input`**（必填）：输入内容容器  
  - 文生视频：`{"prompt": "..."}`  
  - 图生视频：`{"media": [{"type": "image", "url": "..."}], "prompt": "..."}`  
  - 参考生视频：`{"media": [{"type": "image", "url": "..."}, {"type": "video", "url": "..."}], "prompt": "..."}`  
  - 视频编辑/动作迁移等：`{"media": [...]}` 结构依任务类型而异（参见 [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)）  
- **`parameters`**（可选）：控制输出质量与时长  
  - `duration`: 视频秒数（通常 2–30 秒，`wan3.0-video` 最长支持 30 秒）  
  - `resolution`: 如 `"540P"`、`"720P"`、`"1024*576"`（注意不同模型取值范围不同）  
  - `watermark`: 布尔值，是否添加水印（默认 `true`）  
  - `aspect_ratio`: 宽高比（如 `"16:9"`），部分模型（如 `kling`）支持  
  - `style` / `style_level`: 风格强度（如 `emo-v1` 的 `"active"`）  

- **请求头**（必填）：  
  - `Authorization: Bearer $DASHSCOPE_API_KEY`  
  - `Content-Type: application/json`  
  - `X-DashScope-Async: enable`（异步必需，缺失将报错）

## 使用方式

1. **准备环境**：在阿里云百炼控制台开通对应模型服务，获取所属地域的 API Key，并配置为环境变量 `DASHSCOPE_API_KEY`；确认业务空间 ID（`{WorkspaceId}`）  
2. **构造请求**：使用业务空间专属域名（推荐）或通用域名  
   - 推荐域名（华北2/新加坡）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`  
   - 通用域名（兼容旧版）：`https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（[HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md) 强调新域名“提供卓越性能和更高稳定性”）  
3. **提交任务**：`POST` 请求创建任务，获取 `task_id`  
4. **轮询结果**：使用 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（或业务空间专属地址）查询状态，直至 `status == "SUCCESS"`，响应中 `output.video_url` 为成品视频地址  

## 限制和注意事项

- **地域一致性强制要求**：模型、Endpoint URL、API Key 必须同属一个地域（如华北2），否则鉴权失败或服务报错；新加坡、北京等地域拥有独立 API Key 与请求地址，不可混用（参见 [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)）  
- **任务生命周期**：`task_id` 有效期严格为 24 小时，超时需重新提交；禁止重复创建相同任务，应轮询获取结果  
- **输入格式差异**：  
  - `wan2.7` 系列统一使用 `media` 数组传入多模态素材（图像/视频/音频）  
  - `pixverse` 系列对首尾帧使用 `{"type": "first_frame"}` / `{"type": "last_frame"}`（[爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)）  
  - `happyhorse` 和 `vidu` 使用 `{"type": "image"}`  
- **异步强制性**：所有视频类 API 均不支持同步返回，必须实现轮询逻辑；超时时间建议设为 10 分钟以上（部分任务如视频超清耗时可达 5–10 分钟）  
- **免费额度与限流**：多数模型（如 `emo-v1`、`liveportrait`、`videoretalk`）提供免费额度（如 1800 秒/月），同时限制 QPS/RPS 及并发任务数（如 `emo-v1` 同时处理中任务数上限为 1）

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


