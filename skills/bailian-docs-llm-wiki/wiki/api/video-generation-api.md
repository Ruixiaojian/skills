# video generation api

百炼平台的视频生成 API 提供多种模态输入（文本、图像、视频、音频）驱动的视频生成与编辑能力，覆盖文生视频、图生视频、参考生视频、视频编辑、数字人、风格重绘等核心场景。所有接口均采用异步调用模式，任务创建后返回 `task_id`，需轮询获取结果，`task_id` 有效期为 24 小时。开发者必须确保模型、Endpoint URL 与 API Key 属于同一地域，跨地域调用将失败。

## 支持的模型/功能

视频生成 API 按能力维度分为以下几类：

- **文生视频（T2V）**：支持 `happyhorse-1.1-t2v`、`pixverse/pixverse-c1-t2v`、`wan2.7-t2v-2026-06-12`、`vidu/viduq3-turbo_text2video`、`kling/kling-v3-video-generation` 等模型，可生成单镜头或多镜头叙事视频。[万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md) 明确支持通过自然语言描述分镜（如“第1个镜头\[0-3秒\] 全景”），无需显式配置 `shot_type`。

- **图生视频（I2V）**：包括基于首帧（`happyhorse-1.1-i2v`、`pixverse/pixverse-c1-it2v`、`wan2.7-i2v-2`）、首尾帧（`pixverse/pixverse-c1-kf2v`、`vidu/viduq3-turbo_start-end2video`、`wan2.2-kf2v-flash`）及视频续写（仅 `wan2.7` 支持）三种模式。注意 `wan2.2-kf2v-flash` 使用旧版路径 `/api/v1/services/aigc/image2video/video-synthesis`，而 `wan2.7` 及主流模型统一使用 `/api/v1/services/aigc/video-generation/video-synthesis`。

- **参考生视频（R2V）**：支持多图、图文、图+视频混合输入，用于角色一致性生成，如 `pixverse/pixverse-c1-r2v`、`wan2.7-r2v-2026-06-12`、`vidu/viduq3-ad_reference2video`。[爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md) 强调通过 `media` 数组传入参考图像并控制分辨率与时长。

- **视频编辑与增强**：涵盖指令编辑（`wan2.7-videoedit`）、动作模仿（`pixverse/pixverse-motioncontrol`）、对口型（`pixverse/pixverse-lipsync`）、超清（`pixverse/pixverse-upscale`）、风格重绘（`video-style-transform`）等。其中 `video-style-transform` 支持 8 种预设艺术风格，且使用独立 endpoint `https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`，不依赖业务空间域名。

- **数字人与肖像动画**：包括 `wan2.2-s2v`（说话/唱歌）、`emo-v1`（唱演）、`liveportrait`（轻量播报）、`videoretalk`（口型替换）、`animate-anyone-gen2`（舞蹈）及 `emoji`（表情包）。此类模型普遍需先调用检测模型（如 `emo-detect-v1`）验证输入合规性，再提交生成任务。

> **注意**：文档中存在路径不一致问题。`wan2.2-kf2v-flash`（文档 31）和 `wan2.2-animate-move`（文档 15）、`wan2.2-animate-mix`（文档 16）均使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径；而所有 `wan2.7`、`HappyHorse`、`PixVerse`、`Vidu`、`Kling` 模型均使用 `/api/v1/services/aigc/video-generation/video-synthesis`。开发者应严格按模型版本选择对应 endpoint，混用将导致 404 错误。

## 关键参数

所有请求必须包含以下通用头字段：
- `Content-Type: application/json`
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `X-DashScope-Async: enable`（缺失将报错：“current user api does not support synchronous calls”）

核心请求体结构为 `{ "model": "...", "input": { ... }, "parameters": { ... } }`，其中：

- `model`：必填，精确匹配模型名称（如 `wan2.7-t2v-2026-06-12`），大小写敏感。
- `input`：根据任务类型变化：
  - 文生视频：仅 `prompt` 字符串；
  - 图生视频：`media` 数组，每项含 `type`（`image_url`/`first_frame`/`last_frame`）和 `url`；
  - 视频编辑/动作模仿：`media` 包含 `video_url` 与 `image_url`；
  - 数字人：`image_url` + `audio_url`；
  - 风格重绘：`video_url`（在 `input` 下，非 `parameters`）。
- `parameters`：可选，常见字段包括：
  - `duration`: 视频时长（秒），默认 5；
  - `resolution` / `size`: 分辨率，如 `"720P"`、`"1280*720"`、`"540P"`；
  - `watermark`: 布尔值，是否添加水印（默认 `true`）；
  - `audio`: 布尔值，是否生成音频（部分模型支持）；
  - `style`: 风格重绘专用，取值 0–7；
  - `prompt_extend`: 旧版多镜头必需（文档 29、30），新版已弃用。

## 使用方式

1. **准备环境**：开通对应模型服务，获取同地域 API Key，并配置为环境变量 `DASHSCOPE_API_KEY`；确认业务空间 ID（`{WorkspaceId}`）。
2. **构造请求**：
   - 使用地域专属域名（推荐）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（北京）或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...`（新加坡）；旧版或特定模型（如 `video-style-transform`）仍可使用 `https://dashscope.aliyuncs.com/...`。
   - 设置上述必填 headers 和 JSON body。
3. **提交任务**：`POST` 请求返回 JSON，含 `task_id`。
4. **轮询结果**：使用 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（通用）或 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`（业务空间域名）查询状态，直至 `output.video_url` 返回有效链接。

> **注意**：`wan2.2-s2v` 的示例代码（文档 17）使用了旧版通用域名 `https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis/`，而其 `task_id` 查询 URL 却要求替换为业务空间域名。实际开发中，**任务创建与结果查询应使用同一 base URL**，避免因域名不一致导致鉴权失败。

## 限制和注意事项

- **地域强绑定**：模型、API Key、Endpoint URL 必须同属一个地域（北京/新加坡/弗吉尼亚/法兰克福/东京），否则调用失败。[HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md) 明确强调此约束。
- **异步时效性**：`task_id` 仅 24 小时有效，过期后无法查询结果；任务状态轮询建议间隔 ≥3 秒，避免触发限流。
- **输入规范**：数字人系列（`EMO`、`LivePortrait`、`VideoRetalk`）必须先调用检测模型（如 `emo-detect-v1`）验证图片/音频质量，否则生成失败。
- **模型演进**：`wan2.7` 系列为当前主力，全面替代 `wan2.1`–`wan2.6` 旧版（文档 29–33 标注“推荐优先选用”）。旧版接口路径、参数（如 `shot_type`）已逐步废弃，新项目应直接集成 `wan2.7`。
- **资源隔离**：业务空间专属域名提供更高性能与稳定性，阿里云明确建议迁移；现有通用域名仍兼容，但非长期保障。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
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
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


