# 多模态生成 API 对比：图像、视频与3D生成

本文档面向百炼平台开发者，旨在系统性对比图像生成、视频生成与3D生成三类核心多模态生成 API 的能力边界、技术特性与工程实践差异。随着AIGC应用向高维内容（2D→3D→时序）纵深演进，准确理解各模态API在输入约束、输出形态、调用范式、计费逻辑及适用场景上的异同，是构建稳定、高效、可扩展的AI原生应用的关键前提。本对比基于当前（2026年Q2）百炼平台正式发布的生产级API能力，所有信息均来自官方文档与实际接口行为验证。

## 关键维度对比

| 维度 | 图像生成 API | 视频生成 API | 3D生成 API |
|------|--------------|----------------|--------------|
| **核心能力定位** | 文生图、图生图、局部编辑、风格迁移、背景/人物/商品等垂直场景生成 | 文生视频、图生视频（首帧/首尾帧/续写）、参考生视频、数字人播报、口型驱动、视频编辑与风格重绘 | 文生3D、单图生3D、多视角图生3D；输出带PBR材质或无贴图的GLB模型及渲染预览图 |
| **主流输入格式** | - 文本 [prompt](../guides/prompt.md)（中英文，≤512 token）<br>- 参考图 URL（最多14张，HTTPS公网可访问）<br>- `messages` 结构（支持图文混排） | - 文本 [prompt](../guides/prompt.md)<br>- 单图/首帧/首尾帧/参考图 URL（`media` 数组，类型明确标注）<br>- 音频 URL（数字人场景）<br>- 多媒体混合输入（如图+音频） | - 文本 [prompt](../guides/prompt.md)（≤1024字符）<br>- 单张图像 URL（JPEG/PNG，20–6000px，≤20MB）<br>- 四视角图像数组（固定顺序：前/左/后/右，长度必须为4，空位用 `{}` 占位） |
| **主流输出格式** | PNG/JPEG 图片 URL（同步直出）或 `output.results[].url`（异步）；支持水印开关 | MP4 视频 URL（`output.results[].url`）；部分模型额外返回关键帧图、音频轨道等；URL有效期24小时 | GLB 模型 URL（`pbr_model_url` 或 `base_model_url`） + 渲染预览图 URL（`rendered_image_url`）；所有URL有效期仅**2小时** |
| **支持模型（代表性）** | `qwen-image-3.0-pro`, `wan2.7-image-pro`, `kling/kling-v3-omni-image-generation`, `vidu/vidu-image_reference2image`, `facechain-portrait-generation`, `outfitanyone` | `wan2.7-t2v-*`, `pixverse/pixverse-c1-t2v`, `vidu/t2v`, `kling/kling-video`, `liveportrait`, `emo`, `video-style-transform`, `pixverse-upscale` | `Tripo/Tripo-H3.1`（高精度，≤200万面），`Tripo/Tripo-P1.0`（专业级，≤2万面） |
| **API 端点（典型）** | 同步：`POST /api/v1/services/aigc/multimodal-generation/generation`<br>异步：`POST /api/v1/services/aigc/xxx/generation` → `GET /api/v1/tasks/{task_id}` | 统一异步端点：<br>`POST /api/v1/services/aigc/video-generation/video-synthesis` → `GET /api/v1/tasks/{task_id}` | 强地域限定端点（仅华北2）：<br>`POST /api/v1/services/aigc/video-generation/3d-generation` → `GET /api/v1/tasks/{task_id}` |
| **调用模式** | **混合模式**：<br>- 同步直出（推荐）：`qwen-image-3.0-pro`, `wan2.7-image-pro`, `z-image-turbo` 等<br>- 异步轮询（兼容）：`kling`, `vidu`, `wanx` 系列旧模型 | **强制异步**：<br>所有模型均需 `X-DashScope-Async: enable`，任务创建后轮询；`task_id` 有效期24小时 | **强制异步**：<br>必须携带 `X-DashScope-Async: enable`；`task_id` 有效期24小时；**不支持同步调用** |
| **地域与密钥约束** | **严格隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）地域的 API Key 与 Workspace ID 完全独立，不可混用 | **严格隔离**：Key、Endpoint、Workspace ID 必须属同一地域；跨地域调用直接鉴权失败 | **强地域锁定**：**仅支持华北2（北京）地域**；其他地域 Key 或 URL 均无效 |
| **计费方式** | - 免费额度：多数模型提供 500 张/90天（主账号与RAM子账号共享）<br>- 计费粒度：按“生成张数”计费（如 `wanx-v1`: 0.16元/张）<br>- 限时免费模型（如 `wanx-x-painting`）额度耗尽即停用，不可续费 | - 免费额度：按“任务次数”或“视频秒数”提供（如 `wan2.7` 系列约 30 秒/90天）<br>- 计费粒度：按“任务成功执行次数”或“输出视频时长×分辨率系数”计费（如 `pixverse-upscale` 按4K超分帧数计费）<br>- 数字人模型常按“音频时长+图像分辨率”复合计费 | - 免费额度：开通 Tripo 服务后赠送初始额度（具体以控制台为准）<br>- 计费粒度：按“成功生成的3D模型任务次数”计费；`H3.1`（高面数）单价高于 `P1.0`（专业级）<br>- **无按面数/贴图质量细分计费，仅按任务成功与否结算** |
| **典型响应时效（平均）** | 同步：3–8 秒<br>异步：PENDING→SUCCEEDED 通常 10–60 秒（复杂提示/高分辨率可能达2分钟） | PENDING→SUCCEEDED 通常 60–300 秒（3–5秒视频）；超清/长时长/多动作模型可达5–10分钟 | PENDING→SUCCEEDED 通常 2–8 分钟（文生3D较慢，单图/多图相对快）；`H3.1-ultra` 模式可能超10分钟 |
| **关键限制与注意事项** | - 输入图必须公网HTTPS可访问，无中文路径<br>- `size`/`aspect_ratio` 参数因模型而异，需查对应文档<br>- 部分模型（如 `wanx` 系列）已停止维护，官方推荐迁移至 `qwen-image` 或 `wan2.7` | - 所有请求必须含 `X-DashScope-Async: enable`<br>- 数字人模型需先调用 `detect` 模型校验输入合规性<br>- 旧版 `wan2.1`–`wan2.6` endpoint 已废弃，新版统一使用 `/video-synthesis` | - `prompt`/`image`/`images` **三者严格互斥**，共存即报错<br>- 多图输入必须为长度4数组，顺序不可变<br>- 输出URL有效期仅**2小时**，必须及时下载保存<br>- 不支持任何同步调用尝试 |

## 各方案适用场景建议

| 场景类型 | 推荐方案 | 理由说明 |
|----------|-----------|-----------|
| **高频、轻量、实时反馈型应用**<br>（如电商详情页实时换背景、设计工具内嵌草图转图、社交App滤镜式生成） | ✅ **图像生成 API（同步直出模型）**<br>如 `qwen-image-3.0-pro`、`wan2.7-image-pro` | 同步模式毫秒级响应，低延迟体验佳；支持自由分辨率与批量生成（`n=1–9`），契合前端即时交互需求；免费额度充足，成本可控。 |
| **叙事性、时序性、动态表达型内容生产**<br>（如营销短视频自动生成、教育课件动画、游戏过场预演、数字人直播开场） | ✅ **视频生成 API（`wan2.7` 或 `pixverse` 系列）**<br>优先选用支持首尾帧/续写的模型 | `wan2.7` 提供最完整的图生视频控制能力（首帧启动、首尾帧约束、视频续写），保障叙事连贯性；`pixverse` 在对口型、动作模仿上表现突出；异步模式天然适配后台任务队列。 |
| **产品可视化、工业设计、虚拟空间构建**<br>（如电商3D商品展示、AR试穿底层建模、游戏资产快速原型、建筑可视化） | ✅ **3D生成 API（`Tripo/Tripo-P1.0` 或 `H3.1`）** | 唯一提供标准GLB输出的官方API，直接对接Unity/Unreal/WebGL渲染管线；`P1.0` 平衡速度与质量，适合批量生成；`H3.1-ultra` 满足高精度工业级需求；多视角输入显著提升几何准确性。 |
| **需要强语义控制与精细编辑的创意工作流** | ✅ **图像生成 API（垂直专用模型组合）**<br>如 `wanx-x-painting`（局部重绘） + `wanx-style-repaint-v1`（人像风格） + `image-out-painting`（扩展） | 垂直模型参数精简、效果确定性强；可通过链式调用（上一输出作为下一输入）构建非破坏性编辑流水线，远超通用模型的可控性。 |
| **数字人驱动与音视频融合场景** | ✅ **视频生成 API（人物驱动类）**<br>如 `liveportrait`（灵动人像）、`emo`（悦动人像）、`wan2.2-s2v`（数字人播报） | 专为肖像动画优化，内置人脸检测、关键点追踪、表情/唇动解耦模块；支持音频驱动，输出自然流畅；需配合 `detect` 模型前置校验，确保输入质量。 |
| **低成本快速验证与MVP开发** | ⚠️ **谨慎选择**：优先用图像API（免费额度高、调试快）<br>避免早期重度依赖视频/3D API | 视频与3D生成任务耗时长、失败率略高、URL有效期短，调试周期长；图像API可快速验证提示词工程、风格偏好与基础流程，是更高效的前期验证手段。 |

## 技术选型参考指南（致开发者）

1. **从调用范式开始决策**：  
   若业务要求**毫秒级响应**（如Web应用内联生成），图像API的同步直出是唯一选择；若可接受**秒级到分钟级延迟**（如后台任务、邮件通知式交付），则视频与3D API 的异步模式完全适用，且更利于资源调度与错误重试。

2. **地域与基础设施先行**：  
   务必在编码前确认目标地域——**3D API 锁死华北2**，视频/图像API虽多地可用，但Key、Workspace、Endpoint必须严格匹配。建议在CI/CD中注入地域变量，避免硬编码。

3. **输入准备是成败关键**：  
   - 图像/视频API：所有外部URL必须是**公网HTTPS、无中文路径、开启公共读**（OSS需设ACL为public-read）；本地文件请先上传至对象存储再传URL。  
   - 3D API：多图输入务必按「前/左/后/右」顺序填充4元素数组，缺失视角用 `{}`，不可省略或错位。

4. **输出持久化策略**：  
   - 图像/视频URL有效期24小时，**建议收到后立即下载并存入自有存储**；  
   - **3D模型URL仅2小时有效！** 必须在轮询到 `SUCCEEDED` 后**立刻并发下载** `pbr_model_url` 和 `rendered_image_url`，否则任务结果将不可恢复。

5. **错误处理标准化**：  
   所有API均返回 `request_id`，它是阿里云工单排查的唯一凭证；常见错误应主动捕获：  
   - `BadRequest.InputDownloadFailed` → 检查图片/视频URL可访问性；  
   - `InvalidParameter` → 核对输入字段互斥性（尤其3D的`prompt`/`image`/`images`）；  
   - `Forbidden.AccessDenied` → 确认地域Key与Endpoint匹配；  
   - `ServiceUnavailable.TooManyRequests` → 视频/3D轮询接口RPS限20，改用[异步回调](https://help.aliyun.com/zh

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


