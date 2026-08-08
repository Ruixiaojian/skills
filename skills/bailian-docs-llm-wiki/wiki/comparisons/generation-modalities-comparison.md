# 多模态生成能力对比：图像、视频与3D生成API

为帮助开发者快速理解百炼平台在多模态生成领域的技术能力边界与工程适配要点，本文系统对比图像生成、视频生成与3D生成三类核心API的能力特征。对比基于当前（2024年Q2）正式发布的稳定接口规范，聚焦实际开发中高频关注的技术维度——包括调用模式、输入/输出约束、模型生态、地域要求及计费逻辑等，旨在为产品选型、架构设计与成本预估提供可落地的决策依据。

---

## 关键维度对比表

| 维度 | 图像生成 API | 视频生成 API | 3D生成 API |
|------|--------------|----------------|--------------|
| **核心能力** | 文生图、图生图、局部编辑、风格迁移、背景生成、UI/图表渲染、虚拟模特试穿等 | 文生视频、图生视频（首帧/首尾帧）、参考生视频、数字人驱动、口型替换、动作迁移、视频超分与风格重绘 | 文生3D、单图生3D、多图（前/左/后/右）生3D，支持PBR材质与无贴图模型输出 |
| **输入格式** | • 文生图：`{"text": "prompt"}` 或 `{"prompt": "..."}`<br>• 图生图/编辑：含 `base_image_url` + `mask_image_url` 或 `messages` 数组（含 text/image）<br>• 支持多图融合、涂鸦、线稿等结构化输入 | • 文生：`{"prompt": "..."}`<br>• 图生：`{"media": [{"type": "image", "url": "..."}], "prompt": "..."}`<br>• 首尾帧：`{"media": [{"type": "first_frame", ...}, {"type": "last_frame", ...}], ...}`<br>• 数字人：`{"image_url": "...", "audio_url": "..."}` | • 三选一互斥：<br> – 文生：`{"prompt": "..."}`（≤1024字符）<br> – 单图：`{"image": "https://..."}`（JPEG/PNG，20–6000px，≤20MB）<br> – 多图：`{"images": [{}, {"url": "..."}, {}, {"url": "..."}]}`（长度固定为4，空视角用 `{}` 占位） |
| **输出格式** | • 同步返回：直接返回 `output.results[]`（含 `url`、`size`、`seed` 等）<br>• 异步返回：`output.result_url`（含图片URL数组）<br>• 支持4K/2K/1K及宽高比（如 `"16:9"`） | • 全部异步：返回 `output.video_url`（MP4格式，含音频可选）<br>• 附带 `rendered_image_url`（首帧预览图）<br>• 分辨率支持 `"720P"`、`"1280*720"`、`"3840×2160"` 等 | • 全部异步：返回 `output.pbr_model_url`（GLB格式，含PBR材质）<br>• 可选 `output.base_model_url`（无贴图基础网格）<br>• 同时返回 `output.rendered_image_url`（渲染预览图）<br>• 所有URL有效期均为 **2小时** |
| **支持模型（代表性）** | • 通用生成：`wan2.6-t2i`, `qwen-image-3.0-pro`, `z-image-turbo`, `kling/kling-v3-omni-image-generation`<br>• 编辑增强：`wan2.7-image-pro`, `qwen-image-edit-max`, `wanx2.1-imageedit`<br>• 垂直工具：`virtualmodel-v2`, `shoemodel-v1`, `facechain`, `wordart` | • 通用生成：`wan3.0-video`（邀测）、`kling/kling-v3-video-generation`, `vidu/viduq3-pro-fast_img2video`<br>• 编辑迁移：`wan2.7-videoedit`, `pixverse/pixverse-lipsync`, `videoretalk`<br>• 数字人：`emo-v1`, `liveportrait`, `animate-anyone-gen2` | • `Tripo/Tripo-H3.1`（高精度，≤200万面，支持 `geometry_quality: "ultra"`）<br>• `Tripo/Tripo-P1.0`（专业级，≤2万面，响应更快） |
| **API端点** | • 同步模型：`/api/v1/services/aigc/multimodal-generation/generation`<br>• 异步模型：同上（需 `X-DashScope-Async: enable`） | • 统一新版端点：`/api/v1/services/aigc/video-generation/video-synthesis`<br>• （旧版部分模型仍用 `/api/v1/services/aigc/image2video/video-synthesis`，已不推荐） | • 固定端点：`/api/v1/services/aigc/video-generation/3d-generation`<br>• ⚠️ 注意：路径含 `video-generation` 仅为历史命名，实际为3D专属路由 |
| **调用协议** | • **混合模式**：`wan2.6-t2i`/`z-image-turbo` 等支持同步；`wanx-v1`/`qwen-mt-image` 等强制异步<br>• 同步请求**禁止设置** `X-DashScope-Async` 头 | • **强制异步**：所有模型均需 `X-DashScope-Async: enable`<br>• 两步操作：`POST` 创建任务 → `GET /tasks/{task_id}` 轮询 | • **强制异步**：必须携带 `X-DashScope-Async: enable`<br>• 缺失该头将明确报错 `"current user api does not support synchronous calls"` |
| **地域支持** | • 北京、新加坡、美国（弗吉尼亚）、法兰克福、东京<br>• 模型、API Key、Endpoint 必须严格同地域 | • 北京、新加坡、美国（弗吉尼亚）<br>• 模型、API Key、Endpoint 必须严格同地域 | • **仅限华北2（北京）**<br>• 其他地域域名调用将失败，控制台开通与API Key获取均限定北京地域 |
| **计费方式** | • 免费额度：500张/90天（主账号与RAM子账号共享）<br>• 超出后按模型单价计费（例：`wanx-v1` 0.16元/张，`wanx-sketch-to-image-lite` 0.06元/张）<br>• 部分模型（如 `wanx-x-painting`）免费额度用尽后不可付费续订 | • 按模型独立计费：多数按“次”或“秒”计费（如 `videoretalk` 按音频时长计费）<br>• 免费额度未统一说明，需查阅各模型资费页<br>• QPS/RPS 限制因模型而异（例：`videoretalk` 限 1 RPS） | • 按模型+质量档计费：<br> – `Tripo/Tripo-P1.0`：基础档<br> – `Tripo/Tripo-H3.1` + `geometry_quality: "ultra"`：高阶档<br>• 无公开免费额度，需开通后按用量结算 |
| **典型场景** | • 营销素材批量生成（电商主图、广告Banner）<br>• UI设计稿自动渲染与改稿<br>• 人像写真风格化与虚拟试穿<br>• 文档插图、教育图表生成 | • 短视频内容创作（文生短视频、图文转视频）<br>• 数字人播报（新闻、客服、培训）<br>• 产品演示动画（首帧→动态效果）<br>• 影视分镜预演与AIGC短片制作 | • 工业设计原型快速建模（文生概念模型）<br>• 电商商品3D展示（单图生成可交互模型）<br>• 游戏资产辅助生成（多视角图→低多边形模型）<br>• AR/VR内容生产管线接入 |

---

## 适用场景建议

### ✅ 推荐选择图像生成 API 当：
- 需要**毫秒级响应**（如实时UI预览、设计协作工具中的即时生图）→ 选用 `z-image-turbo` 或 `wan2.6-t2i` 同步模型；
- 要求**强文本理解与排版能力**（如海报含多段文字、Logo与文案混排）→ 优先 `qwen-image-3.0-pro`；
- 进行**精细化图像编辑**（擦除水印、扩图、线稿上色、人物换装）→ 使用 `wanx2.1-imageedit` 或 `qwen-image-edit-max`；
- 构建**垂直行业应用**（鞋靴试穿、虚拟模特、手写字体生成）→ 直接调用 `shoemodel-v1`、`virtualmodel-v2`、`wordart` 等专用模型。

### ✅ 推荐选择视频生成 API 当：
- 业务需**自动化视频内容生产**（如每日资讯摘要视频、社交媒体种草短片）→ `wan3.0-video`（邀测中）或 `kling/kling-v3-video-generation`；
- 需集成**数字人播报能力**（企业知识库问答、智能客服视频回复）→ `emo-v1`（轻量活跃）或 `liveportrait`（高拟真）；
- 存在**已有视频素材需增强或改造**（提升分辨率、替换口型、迁移动作）→ `pixverse/pixverse-upscale`、`pixverse/pixverse-lipsync`；
- 要求**首尾帧控制的精准运镜**（产品旋转展示、机械结构分解动画）→ 使用 `vidu/viduq3-pro-img2video` 的首尾帧模式。

### ✅ 推荐选择3D生成 API 当：
- 目标是**快速构建3D可视化原型**（无需专业建模师）→ `Tripo/Tripo-P1.0`（平衡速度与质量）；
- 需要**高保真工业级模型输出**（用于3D打印、CAD导入、物理仿真）→ `Tripo/Tripo-H3.1` + `geometry_quality: "ultra"`；
- 具备**标准四视角产品图**（前/左/后/右），希望一键生成可交互3D模型 → 多图生3D模式；
- 集成至**WebGL/AR应用管线** → 直接使用返回的 GLB 文件，兼容 Three.js、Babylon.js 等主流引擎。

---

## 开发者技术选型参考

| 选型维度 | 关键建议 |
|----------|----------|
| **调用链路设计** | • 图像：评估延迟敏感度——高并发低延迟场景选同步模型；复杂编辑任务选异步并实现轮询兜底。<br>• 视频/3D：**必须设计异步状态机**，包含任务创建、状态轮询（建议指数退避）、结果下载、URL缓存（注意2小时过期）与失败重试策略。 |
| **地域与域名** | • 三类API均要求**模型、API Key、Endpoint 严格同地域**；跨地域调用必然鉴权失败。<br>• **强烈推荐使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），其稳定性、吞吐与错误率显著优于通用 `dashscope.aliyuncs.com`。 |
| **输入可靠性保障** | • 所有图像/视频/3D URL 必须为公网 HTTPS 地址，且服务可用；建议上传至 OSS 并设置公读权限。<br>• 视频/3D 对图片尺寸、格式、大小有明确限制（如3D单图 ≤20MB，视频首帧建议 ≤10MB），需前置校验与压缩。 |
| **错误处理与监控** | • 图像：关注 `status` 字段（同步）或 `task_status`（异步），区分 `INVALID_INPUT`、`QUOTA_EXCEEDED`、`MODEL_NOT_FOUND` 等码。<br>• 视频/3D：`task_id` 24小时过期后返回 `UNKNOWN`，不可重试；应记录任务生命周期日志，避免重复提交。 |
| **成本优化提示** | • 图像：免费额度共享于主账号下所有子账号，建议通过 RAM 精细分配；`z-image-turbo` 单价低、速度快，适合大批量简单生图。<br>• 视频：`duration` 和 `resolution` 直接影响计费，测试阶段建议先用 3秒+720P 挡位验证效果。<br>• 3D：

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


