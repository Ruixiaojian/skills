# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，涵盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、数字人及风格迁移等场景。所有接口均采用异步调用模式，需通过“创建任务 → 轮询结果”两步完成，任务 ID 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

API 支持多系列模型，按能力分类如下：

- **通用视频生成**：  
  - `wan3.0-video`（万相3.0）：统一支持文生视频、图生视频（首帧/首尾帧）、参考生视频，最长生成 30 秒视频，当前处于邀测阶段 [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)。  
  - `vidu/viduq3-*` 系列（Vidu）：提供文生视频、首帧/首尾帧生视频、参考生视频等能力，强调物理真实与运动流畅性。  
  - `kling/kling-v3-*`（可灵）：支持文生视频、图生视频（首帧/首尾帧）、参考生视频及视频编辑 [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)。  

- **人物驱动类**：  
  - 数字人模型（如 `wan2.2-s2v`）：基于单图+音频生成说话/唱歌视频；  
  - 表情包模型（`emoji`）、播报模型（`liveportrait`）、唱演模型（`emo`）、舞蹈模型（`animate-anyone`）：均需先调用检测模型（如 `emo-detect-v1`）验证输入合规性 [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)；  
  - 口型替换（`videoretalk`）、动作模仿（`pixverse/pixverse-motioncontrol`）、对口型（`pixverse/pixverse-lipsync`）等专项能力。  

- **编辑与增强类**：  
  - 视频编辑（`wan2.7-videoedit`, `happyhorse-video-edit`）、视频换人（`wan2.2-animate-mix`）、视频超清（`pixverse/pixverse-upscale`）、风格重绘（`video-style-transform`）。  

> **注意**：文档中存在协议路径不一致问题。HappyHorse、Vidu、Kling 等新模型统一使用 `/api/v1/services/aigc/video-generation/video-synthesis`；而部分旧版万相模型（如 wan2.2/wanx2.1）仍使用 `/api/v1/services/aigc/image2video/video-synthesis`（见文档 20、35、34）。实际调用请以对应模型文档为准，避免路径错误导致 404。

## 关键参数

所有请求必须包含以下基础参数：

- **HTTP Headers**（必选）：  
  - `Authorization: Bearer $DASHSCOPE_API_KEY`  
  - `X-DashScope-Async: enable`（异步必需）  
  - `Content-Type: application/json`（除 multipart/form-data 场景外）  

- **Request Body 核心字段**：  
  - `model`: 模型标识符（如 `"vidu/viduq3-turbo_text2video"`、`"wan2.7-videoedit"`），需与开通模型完全一致；  
  - `input`: 输入内容结构，依模型类型不同：  
    - 文生视频：`{"prompt": "文本描述"}`；  
    - 图生视频：`{"media": [{"type": "image", "url": "..."}], "prompt": "..."}`；  
    - 首尾帧：`{"media": [{"type": "image", "url": "first.jpg"}, {"type": "image", "url": "last.jpg"}], ...}`；  
    - 参考生视频：`{"media": [{"type": "reference_image", "url": "..."}, ...], "prompt": "..."}`；  
    - 数字人/口型替换：`{"image_url": "...", "audio_url": "..."}` 或 `{"video_url": "...", "audio_url": "..."}`；  
  - `parameters`: 控制生成效果，常见字段包括：  
    - `duration`: 视频时长（秒），范围通常为 3–10（部分模型支持至 30）；  
    - `resolution` / `size` / `aspect_ratio`: 分辨率（如 `"540P"`、`"1024*576"`、`"16:9"`）；  
    - `watermark`: 是否添加水印（布尔值）；  
    - `audio`: 是否生成音频（部分模型默认 false）；  
    - `style` / `mode`: 风格或模式选择（如 `video-style-transform` 的 `style: 0` 对应日式漫画）。  

## 使用方式

1. **环境准备**：  
   - 在百炼控制台开通目标模型，并获取对应地域的 API Key；  
   - 配置环境变量 `DASHSCOPE_API_KEY`；  
   - 替换 Endpoint 中的 `{WorkspaceId}` 为业务空间 ID（可在控制台「业务空间详情」查看）；  
   - 推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于旧域名 `dashscope.aliyuncs.com`。  

2. **异步调用流程**：  
   - **步骤一（创建任务）**：发送 `POST` 请求至对应 Endpoint，携带完整请求体，成功返回 `{"task_id": "xxx"}`；  
   - **步骤二（轮询结果）**：使用 `GET https://<base-url>/api/v1/tasks/{task_id}` 定期查询（建议间隔 ≥5s），直至 `status` 为 `"SUCCESS"`，响应中 `output.video_url` 即为生成视频地址。  

3. **SDK 支持**：  
   - DashScope SDK 支持同步封装（内部自动轮询），推荐 Python/Node.js 开发者使用，详见各模型文档中的 SDK 示例。

## 限制和注意事项

- **地域强绑定**：模型、API Key、Endpoint URL 必须同属一个地域（如华北2北京、新加坡等），混用将直接报错；  
- **任务幂等性**：`task_id` 24 小时内有效，**禁止重复提交相同请求**，应复用已有 task_id 轮询；  
- **输入要求**：  
  - 图片/视频 URL 需公网可访问、HTTPS 协议、无防盗链；  
  - 数字人/表情包等模型必须先通过 `*-detect` 检测接口验证输入合规性；  
- **计费与限流**：  
  - 多数模型按秒计费（如 `wan2.2-s2v`：480P 0.5 元/秒）；  
  - QPS/RPS 限制因模型而异（如 `videoretalk` 同时处理中任务数上限为 1）；  
- **兼容性提示**：  
  > **注意**：万相 2.1–2.6 系列（文档 31–35）为旧版协议，已明确标注“推荐优先选用万相2.7”；其 `shot_type`、`prompt_extend` 等参数在 2.7+ 版本中已废弃，改由自然语言 [prompt](../guides/prompt.md) 控制分镜 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)


