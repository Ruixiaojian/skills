# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，涵盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、数字人驱动及风格迁移等场景。所有接口均采用异步调用模式，任务创建后需轮询 `task_id` 获取结果，`task_id` 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

Video Generation API 按能力维度分为三类模型：

- **通用生成类**：支持[多模态](../concepts/multimodal.md)输入与灵活任务类型  
  - `wan3.0-video`（邀测）：All-in-One 模型，统一支持文生视频、图生视频（首帧/首尾帧）、参考生视频，最长生成 30 秒视频 [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)  
  - `wan2.7-*` 系列（推荐）：包括 `wan2.7-t2v`（文生视频）、`wan2.7-i2v`（图生视频）、`wan2.7-r2v`（参考生视频）、`wan2.7-videoedit`（视频编辑），全面替代旧版协议 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)  
  - `kling/kling-v3-*`：支持文生视频、图生视频（首帧/首尾帧）、参考生视频及视频编辑  

- **垂直场景类**：面向特定人像应用  
  - `liveportrait` / `emo` / `videoretalk` / `animate-anyone`：分别实现播报、唱演、口型替换、舞蹈复刻，均需先调用 `*-detect` 模型校验输入合规性  
  - `vidu/viduq3-*` 与 `pixverse/pixverse-*`：提供文生/图生/首尾帧生视频能力，部分支持广告级参考生视频（如 `vidu/viduq3-ad_reference2video`）  

- **工具增强类**：对已有视频进行后处理  
  - `video-style-transform`：8 种预设艺术风格重绘（日式漫画、国风水墨等）  
  - `pixverse/pixverse-upscale`：超分辨率处理至 4K  
  - `happyhorse-1.0-video-edit`：基于指令与参考图的局部编辑  

> **注意**：文档中存在协议路径不一致问题。`wan2.2-*` 系列（如 `wan2.2-kf2v-flash`）和 `wan2.2-s2v` 使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径，而其余所有模型（含 `wan2.7` 及全部第三方模型）均使用 `/api/v1/services/aigc/video-generation/video-synthesis`。开发者务必按模型版本选择正确 endpoint，否则返回 404。

## 关键参数

所有请求必须包含以下基础参数：

- **必选 Header**  
  `X-DashScope-Async: enable`（异步必需）  
  `Authorization: Bearer $DASHSCOPE_API_KEY`  
  `Content-Type: application/json`

- **核心 Body 字段**  
  `model`: 模型标识符（如 `"wan2.7-t2v-2026-06-12"`），需与开通地域匹配  
  `input`: 输入内容，结构因模型而异：  
  - 文生视频：`{"prompt": "..."}`  
  - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`  
  - 首尾帧：`{"media": [{"type": "first_frame", "url": "..."}, {"type": "last_frame", "url": "..."}], "prompt": "..."}`  
  - 视频编辑/动作迁移：`{"media": [...], "prompt": "..."}`  
  `parameters`: 可选控制项，常见字段：  
  - `duration`: 视频时长（秒），范围通常为 3–10 秒  
  - `resolution` / `size`: 分辨率（如 `"720P"`、`"1280*720"`）  
  - `watermark`: 布尔值，控制是否添加水印（默认 `true`）  
  - `prompt_extend`: 仅 `wan2.6` 及更早模型支持，启用多镜头叙事  

## 使用方式

1. **环境准备**  
   - 在百炼控制台开通对应模型，并获取**同地域**的 API Key  
   - 配置环境变量 `DASHSCOPE_API_KEY`  
   - 替换 Endpoint 中的 `{WorkspaceId}` 为业务空间 ID（控制台「业务空间详情」页获取）

2. **异步调用流程**  
   ```bash
   # 步骤1：创建任务（返回 task_id）
   curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
     -H 'X-DashScope-Async: enable' \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H 'Content-Type: application/json' \
     -d '{"model": "wan2.7-t2v-2026-06-12", "input": {"prompt": "一只猫在月光下奔跑"}}'

   # 步骤2：轮询结果（task_id 有效期 24 小时）
   curl -X GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY"
   ```
   - 任务状态为 `"SUCCESS"` 时，响应中 `output.video_url` 为可下载视频地址  
   - 状态为 `"FAILED"` 时，`output.error_code` 和 `output.error_message` 提供具体错误原因  

3. **地域与域名**  
   - 华北2（北京）与新加坡地域**强烈建议**使用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于公共域名 `dashscope.aliyuncs.com`  
   - 其他地域（如美国弗吉尼亚、德国法兰克福）仍需使用 `dashscope-us.aliyuncs.com` 等公共域名  

## 限制和注意事项

- **地域强绑定**：模型、API Key、Endpoint URL 必须同属一个地域（如北京地域的 Key 不能用于新加坡 Endpoint），否则鉴权失败或返回 `INVALID_REGION` 错误  
- **并发与限流**：  
  - 多数模型（如 `liveportrait`、`emo`、`videoretalk`）同时处理中任务数上限为 1  
  - `animate-anyone` 后付费模式下同时处理中任务数也为 1；独立部署模式支持更高并发（如 `animate-anyone-deployment` 支持 1 并发/算力单元）  
- **输入要求**：  
  - 数字人系列（`liveportrait`、`emo`、`s2v`）必须先调用 `*-detect` 模型验证图片合规性，否则生成失败  
  - `video-style-transform` 仅接受视频 URL（非文件上传），且源视频需可公开访问  
- **过时模型提示**：  
  > **注意**：`wan2.1`–`wan2.6` 系列（如 `wan2.2-kf2v-flash`、`wanx2.1-vace-plus`）为旧版协议，已明确标注“推荐优先选用 wan2.7” [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)。旧模型 endpoint 路径、参数支持（如 `shot_type`）与新模型不兼容，迁移前请仔细核对文档。

## 来源文档

- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)


