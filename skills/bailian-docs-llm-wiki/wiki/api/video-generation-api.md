# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，包括文生视频（T2V）、图生视频（I2V）、参考生视频（R2V）、视频编辑、动作迁移、口型同步等。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果，任务 ID 有效期为 24 小时。开发者必须确保模型、Endpoint URL 与 API Key 三者所属地域一致，跨地域调用将失败。

## 支持的模型/功能

API 支持多系列模型，按能力可分为以下几类：

- **基础生成类**：  
  - `happyhorse-1.1-t2v`（文生视频）、`happyhorse-1.1-i2v`（图生视频-首帧）、`happyhorse-1.0-video-edit`（视频编辑）[原文标题](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)  
  - `wan3.0-video`（全能参考视频生成，支持 T2V/I2V/R2V/文件生视频）[原文标题](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)  
  - `vidu/viduq3-turbo_text2video`、`kling/kling-v3-video-generation` 等厂商专属文生视频模型  

- **[多模态](../concepts/multi-modal.md)参考类**：  
  - `wan2.7-r2v-2026-06-12`（多图像+视频+音色参考）、`pixverse/pixverse-c1-kf2v`（首尾帧）、`vidu/viduq3-ad_reference2video`（广告级参考生视频）  
  - `pixverse/pixverse-motioncontrol`（动作模仿）、`wan2.2-animate-move`（图生动作）、`wan2.2-animate-mix`（视频换人）  

- **数字人与肖像动画类**：  
  - `wan2.2-s2v`（单图+音频生成说话视频）、`emo-v1`（悦动人像唱演）、`videoretalk`（口型替换）、`emoji`（表情包模板驱动）  

- **后处理与风格类**：  
  - `pixverse/pixverse-upscale`（视频超清）、`video-style-transform`（8种艺术风格重绘）  

> **注意**：文档中存在协议路径不一致问题。万相 2.2 及更早的首尾帧模型（如 `wan2.2-kf2v-flash`）使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径，而 2.7+ 及 HappyHorse、PixVerse、Vidu 等全部统一为 `/api/v1/services/aigc/video-generation/video-synthesis`。实际调用请以对应模型文档为准，避免路径错误导致 404 [原文标题](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)。

## 关键参数

所有请求必须包含以下通用参数：

- **必选 Header**：  
  `X-DashScope-Async: enable`（异步必需）、`Authorization: Bearer $DASHSCOPE_API_KEY`、`Content-Type: application/json`

- **核心 Body 字段**：  
  - `"model"`：精确模型名（区分大小写及版本号，如 `pixverse/pixverse-c1-t2v`）  
  - `"input"`：根据任务类型结构化输入  
    - 文生视频：`{"prompt": "..."}`  
    - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`  
    - 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "..."}`  
    - 参考生视频：`{"media": [{"type": "reference_image", "url": "..."}, ...], "prompt": "..."}`  
    - 视频编辑/动作迁移：`{"media": [{"type": "video", "url": "..."}, {"type": "image_url", "url": "..."}], "prompt": "..."}`  
  - `"parameters"`（可选）：常见字段包括  
    - `duration`: 视频时长（秒），范围通常为 3–30  
    - `resolution`: 如 `"720P"`、`"480P"`、`"540P"`（部分模型支持 `"adaptive"`）  
    - `watermark`: `true`/`false`（默认开启）  
    - `size`: 像素尺寸字符串（如 `"1280*720"`），与 `resolution` 互斥  
    - `aspect_ratio`: `"16:9"`、`"9:16"` 等（Kling 等模型特有）  

## 使用方式

1. **环境准备**：  
   - 在百炼控制台开通对应模型服务  
   - 获取目标地域的 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`  
   - 获取业务空间 ID（WorkspaceId），用于构造 Endpoint URL  

2. **Endpoint 构造**：  
   推荐使用业务空间专属域名（性能更优）：  
   `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`  
   其中 `{region}` 为 `cn-beijing`、`ap-southeast-1`、`us-east-1` 等（详见各模型文档）  

3. **异步调用流程**：  
   - **步骤1（创建任务）**：`POST` 请求提交任务，返回 JSON 中含 `"task_id"`  
   - **步骤2（轮询结果）**：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（或使用 Workspace 域名）  
     - 状态为 `"SUCCESS"` 时，响应中 `"output.video_url"` 为可下载视频地址  
     - 状态为 `"FAILED"` 时，检查 `"error.message"` 定位原因  

4. **调试建议**：  
   - 新手推荐使用 Postman 快速验证 [原文标题](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)  
   - 所有示例代码中的 `{WorkspaceId}` 必须替换为真实值，否则返回 404  

## 限制和注意事项

- **地域强一致性**：模型、API Key、Endpoint URL 必须同属一个地域（如北京、新加坡、弗吉尼亚等），混用将直接鉴权失败或返回 `UNKNOWN` 状态。  
- **任务生命周期**：`task_id` 仅在创建后 24 小时内有效，超时需重新提交任务。  
- **输入约束**：  
  - 图片/视频 URL 必须公网可访问且 HTTPS 协议；  
  - `prompt` 长度建议 ≤ 512 字符，避免截断；  
  - [多模态](../concepts/multi-modal.md)输入（如 R2V）中 `media` 数组长度通常 ≤ 5 项。  
- **计费与限流**：  
  - 后付费模型（如 EMO、VideoRetalk）按秒计费，免费额度有限；  
  - QPS/RPS 限制因模型而异（如 `emo-v1` 为 1 RPS），超出将返回 `429 Too Many Requests`。  
- **模型弃用提示**：万相 2.1–2.6 系列（如 `wan2.6-i2v`）已标记为“旧版协议”，官方明确推荐迁移到 `wan2.7` 或 `wan3.0` 新版协议。

## 来源文档

- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
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
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)


