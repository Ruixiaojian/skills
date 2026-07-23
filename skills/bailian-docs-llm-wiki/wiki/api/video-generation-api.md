# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，包括文生视频（T2V）、图生视频（I2V）、参考生视频（R2V）、视频编辑、口型替换、风格重绘等。所有接口均采用异步调用模式，任务创建后需轮询 `task_id` 获取结果，典型耗时为 1–5 分钟。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

API 覆盖三大类能力：

- **基础生成类**：支持纯文本输入生成视频（如 `happyhorse-1.1-t2v`、`wan2.7-t2v-2026-06-12`、`vidu/viduq3-turbo_text2video`、`pixverse/pixverse-c1-t2v`），部分模型支持智能分镜或多镜头叙事（如 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md) 中通过 [prompt](../guides/prompt.md) 描述时间戳实现）。
  
- **[多模态](../concepts/multi-modal.md)驱动类**：
  - 图生视频：支持首帧（`happyhorse-1.1-i2v`、`wan2.7-r2v-2026-06-12`）、首尾帧（`pixverse/pixverse-c1-kf2v`、`vidu/viduq3-turbo_start-end2video`）及视频续写；
  - 参考生视频：支持传入多张图像/视频/音频（如 [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md) 和 [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)）；
  - 视频编辑：支持指令式风格迁移（`wan2.7-videoedit`）、局部替换（`happyhorse-1.0-video-edit`）及超清增强（`pixverse/pixverse-upscale`）。

- **人像动画类**：聚焦数字人与表情驱动，包括：
  - 唱演/播报：`emo-v1`、`liveportrait`、`wan2.2-s2v`；
  - 动作迁移：`animate-anyone-gen2`、`pixverse/pixverse-motioncontrol`；
  - 口型替换：`videoretalk`、`pixverse/pixverse-lipsync`；
  - 换人/复刻：`wan2.2-animate-mix`、`wan2.2-animate-move`。

> **注意**：文档中存在协议版本冲突。例如，万相系列明确区分“旧版协议”（仅支持 wan2.6 及更早模型，如 [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)）与“新版协议”（仅支持 wan2.7 模型）。混用模型名与旧版 endpoint 将导致调用失败。

## 关键参数

所有请求必须包含以下通用参数：

- **HTTP 头部（Headers）**：
  - `Content-Type: application/json`（必选）；
  - `Authorization: Bearer $DASHSCOPE_API_KEY`（必选）；
  - `X-DashScope-Async: enable`（必选；同步调用不被支持）。

- **请求体（Body）**：
  - `model`：精确模型标识符（如 `"wan2.7-t2v-2026-06-12"`），不可省略；
  - `input`：根据任务类型结构化：
    - 文生视频：`{"prompt": "..."}`；
    - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`；
    - 首尾帧：`{"media": [{"type": "first_frame", ...}, {"type": "last_frame", ...}], "prompt": "..."}`；
    - 口型替换：`{"media": [{"type": "video_url", ...}, {"type": "audio_url", ...}]}`；
  - `parameters`：可选，常见字段包括：
    - `duration`（秒，默认 5）；
    - `resolution` 或 `size`（如 `"720P"`、`"1280*720"`）；
    - `watermark`（布尔值，默认 `true`）；
    - `aspect_ratio`（如 `"16:9"`，见 [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)）；
    - `style`（风格重绘专用，整数 0–7）。

## 使用方式

1. **准备环境**：
   - 在百炼控制台开通对应模型服务；
   - 获取目标地域的 [API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 并配置至环境变量 `DASHSCOPE_API_KEY`；
   - 获取业务空间 ID（WorkspaceId），用于构造专属 endpoint。

2. **发起异步任务**：
   - 向 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` 发送 `POST` 请求；
   - 所有模型共用该 endpoint（除少数遗留模型如 `wan2.2-kf2v-fla` 使用 `/image2video/` 路径，见 [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)）；
   - 成功响应返回 `{"task_id": "xxx"}`，有效期 24 小时。

3. **轮询结果**：
   - 使用 `GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态；
   - 当 `status` 为 `"SUCCESS"` 时，`output.video_url` 即为生成视频地址。

## 限制和注意事项

- **地域强一致性**：模型、API Key、Endpoint 必须同属一个地域（如华北2北京），否则鉴权失败或返回 `401 Unauthorized`。新加坡、美国、德国等地域 endpoint 格式不同，需严格匹配。
  
- **URL 构造规范**：业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）为推荐路径，旧域名（如 `https://dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低。

- **并发与限流**：
  - 多数模型对单账号 RPS/QPS 有限制（如 `liveportrait` 为 1 QPS，`emo-v1` 为 1 并发任务）；
  - 免费额度按模型独立计算（如 `emo-detect-v1` 免费 200 张，`emo-v1` 免费 1800 秒）；
  - 详细限流策略请查阅各模型资费文档。

- **输入约束**：
  - 图像/视频 URL 必须公网可访问且 HTTPS 协议；
  - 音频文件需为清晰人声（MP3/WAV），时长建议 ≤ 30 秒；
  - Prompt 长度通常 ≤ 512 字符，含敏感词将触发拦截。

- **错误处理**：常见错误码包括 `400 Bad Request`（参数缺失或格式错误）、`403 Forbidden`（地域不匹配或配额不足）、`429 Too Many Requests`（超出限流）。建议在轮询逻辑中加入指数退避重试。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)


