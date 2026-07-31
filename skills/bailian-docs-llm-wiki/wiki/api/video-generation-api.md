# video generation api

百炼平台提供多种视频生成能力，覆盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、动作迁移、口型同步等核心场景。所有 API 均采用异步调用模式，通过“创建任务 → 轮询获取结果”两步完成，任务 ID 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格同地域，跨地域调用将失败。

## 支持的模型/功能

百炼视频生成 API 按输入模态和任务类型分为以下几类：

- **文生视频（T2V）**：支持 `happyhorse`、`wan2.7-t2v`、`pixverse-c1-t2v`、`vidu/viduq3-turbo_text2video` 等模型，可生成单镜头或多镜头叙事视频（如 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md) 所述，支持自然语言描述分镜）。
- **图生视频（I2V）**：包括基于首帧（`happyhorse-image-to-video`、`wan2.7-i2v`、`pixverse-c1-it2v`、`vidu/viduq3-pro-fast_img2video`）、首尾帧（`pixverse-c1-kf2v`、`vidu/viduq3-turbo_start-end2video`、`wan2.2-kf2v-fla`）两类；其中万相2.7已统一支持三大任务（首帧、首尾帧、视频续写），[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md) 明确推荐优先选用。
- **参考生视频（R2V）**：支持多图融合（`happyhorse-reference-to-video`、`wan2.7-r2v`、`pixverse-c1-r2v`、`vidu/viduq3-ad_reference2video`），部分模型支持图像+视频+音频多模态参考（如 [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)）。
- **视频编辑与增强**：涵盖风格迁移（`video-style-transform`）、超清（`pixverse/pixverse-upscale`）、动作模仿（`pixverse/pixverse-motioncontrol`）、对口型（`pixverse/pixverse-lipsync`）、换人（`wan2.2-animate-mix`）、舞蹈复刻（`wan2.2-animate-move`）等细分能力。
- **数字人与肖像动画**：包括 `wan2.2-s2v`（音画同步）、`emo-v1`（唱演）、`liveportrait`（轻量播报）、`animate-anyone-gen2`（舞蹈）等专用模型，均需前置图像检测（如 `emo-detect-v1`）。

> **注意**：文档中存在协议路径不一致问题。多数新模型（如 HappyHorse、万相2.7、PixVerse、Vidu）使用 `/api/v1/services/aigc/video-generation/video-synthesis`；但部分旧版模型（如 `wan2.2-kf2v-fla`、`wan2.2-animate-move`、`wan2.2-animate-mix`）仍使用 `/api/v1/services/aigc/image2video/video-synthesis`（见 [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)）。生产环境应优先选用新路径，旧路径可能逐步下线。

## 关键参数

所有请求必须包含以下基础参数：

- **`model`**（必填）：指定模型标识符，如 `"wan2.7-t2v-2026-06-12"` 或 `"pixverse/pixverse-c1-t2v"`；不同模型支持的 `input` 结构差异显著（如 `media` 数组 vs `prompt` 字符串）。
- **`input`**（必填）：根据任务类型结构化：
  - 文生视频：`{"prompt": "..."}`；
  - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`；
  - 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "..."}`；
  - 参考生视频：`{"media": [{"type": "reference_image", "url": "..."}], "prompt": "..."}`；
  - 对口型：`{"media": [{"type": "video_url", ...}, {"type": "audio_url", ...}]}`。
- **`parameters`**（可选）：控制输出质量，常见字段包括：
  - `resolution`（如 `"720P"`、`"540P"`）、`size`（如 `"1280*720"`）、`duration`（秒数，通常 2–5）；
  - `watermark`（布尔值，默认 `true`）；
  - `aspect_ratio`（如 `"16:9"`）、`video_fps`（如 `15`）；
  - 特定模型专属参数（如 `style` 用于风格重绘，`mode` 用于 Kling 分辨率模式）。

所有请求头必须包含：
- `Content-Type: application/json`
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `X-DashScope-Async: enable`（同步调用不支持，缺失将报错）

## 使用方式

1. **开通服务**：在百炼控制台模型市场搜索并开通对应模型（如 [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md) 要求先开通 Vidu 模型）。
2. **配置凭证**：获取同地域 API Key 并设为环境变量 `DASHSCOPE_API_KEY`。
3. **构造请求**：
   - Endpoint URL 格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（北京：`cn-beijing`；新加坡：`ap-southeast-1`；其他地域见文档）；
   - 替换 `{WorkspaceId}` 为控制台业务空间详情页获取的实际 ID；
   - 使用 `POST` 提交 JSON 请求体。
4. **轮询结果**：从响应中提取 `task_id`，向 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（或新域名对应路径）轮询，直至 `status` 为 `"SUCCESS"`，`output.video_url` 返回可下载视频地址。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint、API Key 必须同属一个地域（如华北2北京），混用将导致鉴权失败或 `401 Unauthorized`（所有文档均强调此约束）。
- **异步时效性**：`task_id` 仅在 24 小时内有效，超时后无法查询结果，接口返回 `UNKNOWN` 状态。
- **资源并发限制**：多数模型有 QPS/RPS 限制（如 `emo-v1` 为 1 QPS，`liveportrait` 为 1 并发任务），详见各模型资费文档。
- **输入规范**：数字人及肖像类模型（如 `emo-v1`、`liveportrait`）强制要求前置图像检测（`emo-detect-v1`、`liveportrait-detect`），未通过检测的图片将被拒绝。
- **URL 协议兼容性**：`media.url` 必须为 HTTPS 协议且可公开访问；部分模型（如 `wan2.2-s2v` 示例）仍使用旧版 `https://dashscope.aliyuncs.com` 域名，而新模型统一推荐业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性更优。

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
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)


