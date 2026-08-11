# video generation api

百炼平台的视频生成 API 提供统一的异步调用接口，支持多种模型和输入模态（文本、图像、视频、音频），覆盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、数字人、口型替换、风格重绘等核心能力。所有任务均需通过“创建任务 → 轮询获取结果”两步完成，`task_id` 有效期为 24 小时。

## 支持的模型/功能

视频生成 API 并非单一模型，而是由多个专用模型组成的能力矩阵，按输入模态与任务类型组织：

- **文生视频（T2V）**：支持 `wan2.7-video`、`kling/kling-v3-video-generation`、`pixverse/pixverse-c1-t2v`、`vidu/viduq3-turbo_text2video` 等模型，可生成单镜头或多镜头叙事视频 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)。
- **图生视频（I2V）**：包括首帧生视频（如 `wan2.7-video`、`pixverse/pixverse-c1-it2v`、`vidu/viduq3-pro-fast_img2video`）、首尾帧生视频（如 `pixverse/pixverse-c1-kf2v`、`vidu/viduq3-turbo_start-end2video`）及视频续写（仅 `wan2.7` 支持）[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。
- **参考生视频（R2V）**：支持多图/[多模态](../concepts/multi-modal.md)参考（图像+视频+音频），用于角色一致性生成，如 `wan2.7-r2v-2026-06-12`、`pixverse/pixverse-c1-r2v`、`vidu/viduq3-ad_reference2video` [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)。
- **视频编辑与增强**：涵盖指令编辑（`wan2.7-videoedit`）、风格重绘（`video-style-transform`）、超清（`pixverse/pixverse-upscale`）、动作模仿（`pixverse/pixverse-motioncontrol`）、对口型（`pixverse/pixverse-lipsync`）等 [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)。
- **数字人与肖像动画**：包括 `wan2.2-s2v`（说话/唱歌）、`emo-v1`（唱演）、`liveportrait`（轻量播报）、`videoretalk`（口型替换）、`animate-anyone-gen2`（舞蹈）等，均需先调用检测模型（如 `emo-detect-v1`）验证输入合规性 [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)。

> **注意**：部分旧版模型（如 `wanx2.1`、`wan2.2`、`wan2.5`）仍可通过 `/api/v1/services/aigc/image2video/video-synthesis` 路径调用，但已明确标注为“推荐优先选用新版”，且其 Endpoint 路径与新版不一致（见文档34、35），开发者应避免混用。

## 关键参数

所有请求均需包含以下基础字段：

- `model`：必填，精确指定模型名称（如 `pixverse/pixverse-c1-t2v`），不同模型支持的 `input` 和 `parameters` 结构差异显著。
- `input`：必填，结构依模型而异：
  - 文生视频：`{"prompt": "..."}`；
  - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`；
  - 参考生视频：`{"media": [{"type": "image_url", "url": "..."}, ...], "prompt": "..."}`；
  - 数字人：`{"image_url": "...", "audio_url": "..."}`（需先过检）；
  - 视频编辑：`{"media": [{"type": "video_url", "url": "..."}], "prompt": "..."}`。
- `parameters`：可选，控制输出质量与时长，常见字段包括：
  - `duration`：视频时长（秒），范围通常为 2–10 秒，部分模型（如 `wan3.0-video`）支持最长 30 秒；
  - `resolution` / `size`：分辨率，如 `"480P"`、`"720P"`、`"1280*720"`；
  - `aspect_ratio` / `ratio`：宽高比，如 `"16:9"`、`"adaptive"`；
  - `watermark`：布尔值，控制是否添加水印（默认 `true`）；
  - `audio`：布尔值，控制是否生成音频（部分模型不支持）。

请求头必须包含：
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `Content-Type: application/json`
- `X-DashScope-Async: enable`

## 使用方式

1. **地域对齐**：模型、Endpoint URL 与 API Key 必须属于同一地域（如北京、新加坡、弗吉尼亚等），跨地域调用必然失败。业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）为首选，旧域名（`dashscope.aliyuncs.com`）虽兼容但性能与稳定性较低。
2. **异步流程**：
   - **步骤1（创建任务）**：`POST /api/v1/services/aigc/video-generation/video-synthesis`，获取 `task_id`；
   - **步骤2（轮询结果）**：`GET /api/v1/tasks/{task_id}`，直至 `status` 为 `"SUCCESS"`，响应中 `output.video_url` 即为成品视频地址。
3. **SDK 与工具**：推荐使用 DashScope SDK（需安装）简化调用；新手可直接使用 Postman 按示例调试 [Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

## 限制和注意事项

- **地域隔离严格**：华北2（北京）与新加坡地域的 API Key、Endpoint、模型实例完全独立，不可复用。文档7、12–15、17、18–29、30–35 均明确强调此约束。
- **模型路径差异**：多数新模型（`wan2.7+`、`kling`、`pixverse`、`vidu`）统一使用 `/api/v1/services/aigc/video-generation/video-synthesis`；但部分旧模型（如 `wan2.2-animate-move`、`wan2.2-animate-mix`、`wan2.2-s2v`）仍使用 `/api/v1/services/aigc/image2video/video-synthesis`，路径不兼容 [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)。
- **输入合规性**：数字人、肖像动画类模型（`emo`、`liveportrait`、`animate-anyone`）强制要求前置图像检测（`-detect` 模型），未通过检测的图片将导致任务失败。
- **资源限制**：免费额度、QPS/RPS 限流、并发任务数因模型而异（如 `liveportrait` 同时处理中任务数为 1，`emo-detect` 为 5），详见各模型资费文档。
- **URL 有效性**：`input.media.url` 或 `input.video_url` 等外部链接需确保公网可访问、无防盗链，且文件格式符合要求（常见支持 MP4、WEBP、PNG、JPEG）。

## 来源文档

- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


