# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，涵盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、口型同步、风格重绘等场景。所有接口均采用异步调用模式，通过“创建任务 → 轮询获取结果”两步完成，任务 ID 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

当前支持三大类模型家族，覆盖不同输入模态与生成目标：

- **文生视频（T2V）**：支持 `vidu/viduq3-turbo_text2video`、`wan2.7-t2v-2026-06-12`、`kling/kling-v3-video-generation`、`pixverse/pixverse-c1-t2v` 等模型，支持多镜头叙事（如时间戳分镜或自然语言描述），详见 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)。
- **图/参考生视频（I2V/R2V）**：包括基于单张首帧（`wan2.7-t2v`、`vidu/viduq3-pro-fast_img2video`）、首尾帧（`pixverse/pixverse-c1-kf2v`、`vidu/viduq3-turbo_start-end2video`）、多图参考（`happyhorse-1.1-t2v`、`wan2.7-r2v-2026-06-12`）等多种范式；其中万相2.7系列已统一支持首帧、首尾帧、视频续写三类任务，旧版 `wan2.6` 及更早模型仅支持单一模式，[万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md) 明确标注其能力局限。
- **专业视频处理**：包含数字人（`wan2.2-s2v`）、动作迁移（`wan2.2-animate-move`、`pixverse/pixverse-motioncontrol`）、口型替换（`videoretalk`、`pixverse/pixverse-lipsync`）、超清增强（`pixverse/pixverse-upscale`）、风格重绘（`video-style-transform`）等垂直能力，适用于播报、舞蹈复刻、影视后期等场景。

> **注意**：部分模型路径存在不一致。例如文档8和9中图生动作与视频换人使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径，而其余绝大多数模型（如文档1–7、17–27）均使用 `/api/v1/services/aigc/video-generation/video-synthesis`。该差异非笔误，而是历史演进导致的路径分离，开发者须按模型文档指定路径调用，不可混用。

## 关键参数

所有请求必须包含以下基础参数：

- **`model`（必填）**：模型标识符，格式为 `<vendor>/<model-name>`（如 `vidu/viduq3-turbo_text2video`），不同功能对应不同模型，不可通用。
- **`input`（必填）**：承载核心输入数据：
  - 文生视频：`{"prompt": "..."}`；
  - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`；
  - 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "..."}`；
  - 参考生视频：`{"media": [{"type": "image_url", "url": "..."}, ...], "prompt": "..."}`；
  - 视频编辑/口型同步：`{"media": [{"type": "video_url", "url": "..."}, {"type": "audio_url", "url": "..."}], "prompt": "..."}`。
- **`parameters`（可选）**：控制生成质量与输出规格：
  - 分辨率：`"resolution": "720P"` 或 `"size": "1280*720"`（依模型而异）；
  - 时长：`"duration": 5`（单位：秒，通常支持 2–10 秒）；
  - 水印：`"watermark": true/false`（默认开启）；
  - 其他：如 `video_fps`、`aspect_ratio`、`style`（风格重绘）等，详见各模型文档。

所有请求头（Headers）必须包含：
- `Content-Type: application/json`
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `X-DashScope-Async: enable`（强制启用异步，同步调用将报错）

## 使用方式

1. **准备环境**：在阿里云百炼控制台开通对应模型服务，获取所属地域的 API Key，并配置为环境变量 `DASHSCOPE_API_KEY`；确认业务空间 ID（WorkspaceId）。
2. **构造请求**：使用业务空间专属域名（推荐）或通用域名：
   - 推荐域名：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（北京）；
   - 兼容域名：`https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（仍可用，但性能与稳定性较低）。
3. **提交任务**：发送 `POST` 请求，获取 `task_id`。
4. **轮询结果**：使用 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（或对应地域专属地址）查询状态，直至 `status` 为 `SUCCESS`，响应体中 `output.video_url` 即为生成视频地址。

> **注意**：文档10中数字人 `wan2.2-s2v` 的轮询地址示例仍使用旧版通用域名 `https://dashscope.aliyuncs.com/api/v1/tasks/...`，而文档1–7、17–27均明确要求使用业务空间专属域名轮询。实际调用时应统一使用与创建任务相同的 base URL 域名，否则可能因鉴权失败返回 `UNKNOWN` 状态——请务必遵循 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md) 中强调的“同一地域”原则，包括轮询端点。

## 限制和注意事项

- **地域强绑定**：模型、API Key、Endpoint URL 必须同属一个地域（如华北2北京），跨地域调用必然失败，且错误信息不明确。
- **任务并发与配额**：多数模型对同时处理中任务数有限制（如 `emo-v1` 限 1 个、`liveportrait` 限 1 个），具体见各模型资费文档；免费额度与 QPS/RPS 限制需查阅控制台或 [计费与限流](https://help.aliyun.com/zh/model-studio/rate-limit) 文档。
- **输入规范**：图像需清晰、正面、单人；音频需人声清晰无背景噪音；视频时长建议 ≤30 秒；URL 必须可公开访问且 HTTPS 安全。
- **异步时效性**：任务平均耗时 1–5 分钟，超时任务（如 >30 分钟未完成）将被系统终止，`task_id` 失效。
- **模型演进**：万相、PixVerse、Vidu 等均推出 2.7/新版本，旧版（如 `wan2.6`、`wan2.2`）功能受限且不再更新，[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md) 明确提示“推荐优先选用”新版。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
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
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


