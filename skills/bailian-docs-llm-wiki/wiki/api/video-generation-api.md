# video generation api

百炼平台提供多种视频生成能力，覆盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、动作迁移、口型同步等核心场景。所有 API 均采用异步调用模式，需通过 `task_id` 轮询获取结果，任务有效期为 24 小时。调用前必须确保模型、Endpoint URL 与 API Key 三者地域一致，否则将鉴权失败或返回错误。

## 支持的模型/功能

视频生成 API 按输入模态和任务类型分为以下几类：

- **文生视频（T2V）**：支持 `wan2.7-t2v-*`、`kling/kling-v3-*`、`pixverse/pixverse-*-t2v`、`vidu/viduq3-*-text2video` 等模型，支持多镜头叙事（如 `wan2.7` 通过 [prompt](../guides/prompt.md) 自然描述分镜，`pixverse-c1` 不支持 `shot_type` 参数）[万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)。
- **图生视频（I2V）**：包括基于首帧（`happyhorse-1.1-i2v`, `wan2.7-*it2v`, `pixverse-*it2v`, `vidu/*img2video`）、首尾帧（`pixverse-*kf2v`, `vidu/*start-end2video`, `wan2.2-kf2v-fla`）及视频续写（仅 `wan2.7` 支持）三种子类型；注意 `wan2.2-kf2v-fla` 使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径，与其他模型路径不同 [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)。
- **参考生视频（R2V）**：支持多图/图文/音视频混合输入，如 `happyhorse-1.1-r2v`、`wan2.7-r2v-*`、`pixverse/*r2v`、`vidu/viduq3-ad_reference2video`，适用于角色融合与多主体互动。
- **视频编辑与增强**：涵盖风格迁移（`video-style-transform`）、超清（`pixverse/pixverse-upscale`）、对口型（`pixverse/pixverse-lipsync`）、动作模仿（`pixverse/pixverse-motioncontrol`）、换人（`wan2.2-animate-mix`）、舞蹈复刻（`wan2.2-animate-move`）等专用模型。
- **数字人与播报**：`wan2.2-s2v`（语音驱动肖像）、`liveportrait`（轻量播报）、`emo-v1`（唱演）、`videoretalk`（口型替换）等均属人物视频生成范畴，需先调用对应 detect 模型校验输入合规性。

> **注意**：文档中存在路径不一致问题。`wan2.2-kf2v-fla`（文档33）和 `wan2.2-animate-move`（文档9）、`wan2.2-animate-mix`（文档10）均使用 `/api/v1/services/aigc/image2video/video-synthesis`，而其余所有视频生成模型（含 `wan2.7` 全系列、`happyhorse`、`kling`、`pixverse`、`vidu`）统一使用 `/api/v1/services/aigc/video-generation/video-synthesis`。开发者务必根据所选模型查阅对应文档路径，否则请求将返回 404。

## 关键参数

所有请求必须包含以下基础参数：

- **HTTP Header**：
  - `Authorization: Bearer $DASHSCOPE_API_KEY`（必选）
  - `Content-Type: application/json`（必选）
  - `X-DashScope-Async: enable`（必选，异步模式强制启用）

- **Request Body**：
  - `model`：精确模型名称（如 `wan2.7-t2v-2026-06-12`, `pixverse/pixverse-c1-t2v`），不可省略。
  - `input`：结构因任务类型而异：
    - T2V：`{"prompt": "文本描述"}`
    - I2V（首帧）：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`
    - R2V：`{"media": [{"type": "reference_image", "url": "..."}, ...], "prompt": "..."}`
    - 视频编辑：`{"media": [{"type": "video", "url": "..."}], "prompt": "..."}`
  - `parameters`：可选，常见字段包括：
    - `duration`: 视频时长（秒），通常为 3–5 秒
    - `resolution` / `size`: 分辨率（如 `"720P"`, `"1280*720"`, `"1024*576"`）
    - `watermark`: 布尔值，控制是否添加水印（默认 `true`）
    - `audio`: 布尔值，部分模型支持生成音频（如 `kling`）
    - `style` / `mode`: 风格或模式选择（如 `kling` 的 `"std"` 或 `"omni"`）

## 使用方式

1. **开通服务**：在百炼控制台模型市场搜索并开通对应模型（如 `kling`, `PixVerse`, `Vidu`），确认其所属地域。
2. **配置环境**：获取该地域的 API Key，并设置为环境变量 `DASHSCOPE_API_KEY`；获取业务空间 ID（WorkspaceId）。
3. **构造请求**：
   - 使用专属域名：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`（北京）或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`（新加坡），**强烈推荐迁移至此新域名**以获得更高性能与稳定性 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。
   - 发送 `POST` 请求至 `/api/v1/services/aigc/video-generation/video-synthesis`（或 `image2video/...`，见上文注意项）。
4. **轮询结果**：从响应中提取 `task_id`，使用 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（旧域名）或 `GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}`（新域名）轮询，直至 `status` 变为 `"SUCCESS"`，`output.video_url` 字段即为生成视频地址。

## 限制和注意事项

- **地域强一致性**：模型、Endpoint、API Key 必须同属一个地域（如北京、新加坡、弗吉尼亚、法兰克福），跨地域调用必然失败。
- **任务生命周期**：`task_id` 有效期为 24 小时，过期后无法查询结果，接口返回 `UNKNOWN` 状态。
- **并发与限流**：各模型有独立 QPS/RPS 和同时处理任务数限制（如 `liveportrait` 同时处理中任务数量为 1，`emo-v1` 为 1），详见各模型文档的“资费与限流”章节。
- **输入要求**：多数人物相关模型（`s2v`, `liveportrait`, `emo`, `animate-move`, `videoretalk`）需先调用 `detect` 模型验证图片/视频合规性，否则生成失败。
- **弃用提示**：`wan2.1`–`wan2.6` 系列模型（如文档30–34）为旧版协议，官方明确推荐优先选用 `wan2.7` 新版 API，其功能更全、协议统一且持续迭代。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
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
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
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
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


