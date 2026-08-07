# [多模态](../concepts/multi-modal.md)生成 API 对比：图像、视频与 3D 生成

本文旨在为开发者提供百炼平台[多模态](../concepts/multi-modal.md)生成能力的横向技术对比，聚焦**图像生成、视频生成与 3D 生成**三大核心 API 能力。随着 AIGC 应用从静态内容向动态表达与空间建模演进，准确理解各模态在输入输出、调用机制、模型能力及工程约束上的差异，是构建高性能、可扩展、合规可控的 AI 应用的关键前提。本对比基于当前（2024 年 Q3）百炼平台正式发布的 API 文档与运行规范，覆盖模型选型、协议设计、地域策略、计费逻辑等关键决策维度。

## 关键维度对比表

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D 生成（3D Generation） |
|------|------------------------------|------------------------------|---------------------------|
| **核心能力范围** | 文生图（T2I）、图生图（I2I）、局部重绘、背景生成、风格迁移、AI 试衣、虚拟模特等 | 文生视频（T2V）、图生视频（I2V）、首尾帧生成（KF2V）、参考生视频（R2V）、数字人驱动、口型同步、视频编辑、风格重绘、超分 | 文生 3D、单图生 3D、四视角多图生 3D；输出 PBR 材质 GLB 模型、预览图、基础网格 |
| **主流支持模型** | `qwen-image-3.0-pro`、`wan2.6-t2i`、`z-image-turbo`、`wan2.7-image-pro`、`kling/kling-v3-omni-image-generation`、`outfitanyone` 等 | `wan2.7-t2v`、`vidu/viduq3-turbo_text2video`、`pixverse/pixverse-c1-t2v`、`kling/kling-v3-video-generation`、`wan2.2-s2v`、`emo-v1`、`liveportrait` 等 | `Tripo/Tripo-P1.0`（专业版，≤2 万面）、`Tripo/Tripo-H3.1`（高精度版，≤200 万面） |
| **输入格式** | • 文生图：`{"prompt": "..."}` 或 `{"messages": [...]}`<br>• 图生图/编辑：`image`（URL/base64）+ 可选 `mask_image_url`<br>• 垂直场景：`template_image_url` + `shoe_image_url` 等专用字段 | • 文生视频：`{"prompt": "..."}`<br>• 图生视频：`{"media": [{"type":"image_url","url":"..."}]}`<br>• 首尾帧：`{"media": [{"type":"first_frame",...}, {"type":"last_frame",...}]}`<br>• 数字人：`{"image_url": "...", "audio_url": "..."}` | • 文生 3D：`{"prompt": "..."}`<br>• 单图生 3D：`{"image": "https://..."}`<br>• 多图生 3D：`{"images": [{"file_token":"url1"}, ..., {"file_token":"url4"}]}`（长度严格为 4） |
| **输出格式** | • 同步调用：直接返回 `output.results` 数组（含 `url` 字段）<br>• 异步调用：返回 `task_id`，轮询后得 `output.results`（含 `url`、`size`、`seed` 等）<br>• 支持多张生成（`n=1–6`，部分模型达 9） | • 全异步：返回 `task_id` → 轮询 → `output.video_url`（HTTPS URL，有效期通常 2 小时）<br>• 输出含 `duration`、`resolution`、`aspect_ratio` 元信息<br>• 不支持批量生成（单任务单视频） | • 全异步：返回 `task_id` → 轮询 → `output.results` 包含：<br> ✓ `pbr_model_url`（GLB，带 PBR 材质）<br> ✓ `rendered_image_url`（PNG 预览图）<br> ✓ `base_model_url`（无贴图基础网格，需显式配置）<br>• 所有 URL 有效期仅 **2 小时** |
| **API 调用模式** | **混合模式**：<br>• 新模型（`wan2.6-t2i`、`qwen-image-3.0-pro`、`z-image-turbo`）支持 **同步调用**（低延迟，适合实时交互）<br>• 旧模型/复杂编辑（`wanx-x-painting`、`image-out-painting`、`virtualmodel-v2`）强制 **异步调用** | **全异步模式**：<br>所有模型均需两步：① 创建任务获取 `task_id`；② 轮询 `task_id` 查询结果<br>• `task_id` 有效期 **24 小时**<br>• 不支持同步响应 | **全异步模式**：<br>严格两步流程：<br>① POST 创建任务 → 返回 `task_id`<br>② GET 轮询 `task_id` → 获取模型下载链接<br>• `task_id` 有效期 **24 小时**<br>• 结果 URL（`pbr_model_url` 等）有效期仅 **2 小时**（必须及时下载） |
| **API 端点（推荐）** | `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`（同步）<br>或功能专属路径（如 `/background-generation/generation`） | `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（主路径）<br>⚠️ 注意：`wan2.2-kf2v` 等旧模型使用 `/api/v1/services/aigc/image2video/video-synthesis` | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`<br>（**仅限华北2北京地域**，路径固定） |
| **地域与认证约束** | • **强地域绑定**：API Key、Endpoint、模型开通地域必须一致（北京/新加坡/弗吉尼亚）<br>• 推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`） | • **强地域绑定**：同图像生成，跨地域调用直接鉴权失败<br>• Endpoint 与 API Key 必须同地域，且控制台开通模型需匹配该地域 | • **单地域锁定**：**仅支持华北2（北京）**<br>• API Key 必须为北京地域生成<br>• Endpoint 固定为北京专属域名，其他地域 URL 不可用 |
| **计费方式** | • 多数模型提供 **500 张免费额度**（90 天有效）<br>• 按生成张数计费（如 `wanx-style-repaint-v1`: 0.12 元/张；`image-out-painting`: 0.18 元/张）<br>• 部分模型（如 `wanx-x-painting`）限时免费，额度用尽即停用，**不支持付费续订** | • **按任务/秒独立计费**：<br> ✓ 文生/图生视频：按生成时长（秒）或任务次计费<br> ✓ 数字人/编辑：按任务次或音频时长计费<br>• 无统一免费额度，具体单价需查控制台定价页 | • **按任务次计费**：<br> ✓ `Tripo-P1.0`：基础价格较低，适合原型验证<br> ✓ `Tripo-H3.1`：价格显著更高，对应高面数与 `ultra` 几何质量<br>• 无公开免费额度，需开通后查看控制台实时报价 |
| **典型场景** | • 电商素材批量生成（商品图、场景图）<br>• UI/UX 设计稿渲染（`vidu` 分镜图）<br>• 社交媒体配图、营销海报<br>• AI 试衣、虚拟模特上身效果<br>• 工业设计草图转高清渲染（`qwen-image-edit-max`） | • 短视频内容创作（T2V/I2V）<br>• 产品演示动画（首尾帧生成）<br>• 数字人播报、虚拟主播（`liveportrait`, `emo-v1`）<br>• 广告片口型同步（`pixverse-lipsync`）<br>• 视频风格化与超分（`video-style-transform`, `pixverse-upscale`） | • 游戏资产快速建模（文生基础模型）<br>• 电商 3D 商品展示（单图生成带材质模型）<br>• AR/VR 场景搭建（四视角重建高精度模型）<br>• 工业零部件逆向建模（多图输入提升几何保真度） |

## 各方案适用场景建议

| 场景需求 | 推荐模态 | 关键理由 | 注意事项 |
|----------|----------|----------|----------|
| **需要毫秒级响应的前端交互**（如设计工具实时预览、聊天机器人即时配图） | ✅ 图像生成（新模型同步调用） | `wan2.6-t2i`、`qwen-image-3.0-pro` 等支持同步返回，端到端延迟 <3s，适合用户等待敏感型应用 | 避免选用 `wanx-v1`、`image-erase-completion` 等异步模型；确认地域与模型版本兼容性 |
| **生成动态叙事内容**（短视频、广告、数字人播报） | ✅ 视频生成 | 全链路覆盖 T2V/I2V/KF2V/R2V，且 `vidu`、`kling`、`pixverse` 在运动连贯性与语义一致性上表现突出；数字人模型生态成熟 | 必须采用异步轮询架构；预留 1–5 分钟任务耗时；注意 `task_id` 24 小时有效期管理 |
| **构建三维空间体验**（Web3D 展示、AR 商品、游戏资产管线） | ✅ 3D 生成 | Tripo 是百炼唯一原生 3D 生成方案，支持文/图/多图输入，PBR 输出开箱即用；`H3.1` 版本满足工业级精度需求 | **仅限北京地域**；务必在 2 小时内下载 `pbr_model_url`；多图输入需严格按「前左后右」顺序且长度为 4 |
| **轻量级创意实验或低成本试用** | ✅ 图像生成（免费额度） | 500 张免费额度覆盖大量测试与原型开发，`z-image-turbo` 等轻量模型成本极低 | 免费额度不跨地域、不跨模型共享；`wanx-x-painting` 等限时免费模型不可续费 |
| **高并发批量生产任务**（日均万张图/千条视频） | ⚠️ 需分模态评估 | 图像生成可通过同步调用 + 限流退避实现高吞吐；视频/3D 生成受限于异步队列与 RPS 限制（如视频轮询接口默认 20 RPS），需引入任务队列与回调机制 | 建议启用[异步回调](https://help.aliyun.com/zh/model-studio/async-task-api)替代高频轮询；对视频/3D 任务做优先级调度 |

## 技术选型参考（面向开发者）

- **第一步：明确输入源与输出目标**  
  若输入为纯文本且需静态图 → 优先评估 `qwen-image-3.0-pro`（语义强）或 `wan2.6-t2i`（电商优）；  
  若输入含图片且需动态延展 → 视频生成中 `wan2.7-i2v`（首帧）或 `pixverse-c1-kf2v`（首尾帧）更合适；  
  若目标为可交互 3D 模型 → 直接选用 `Tripo/Tripo-H3.1`，并确保前端具备 GLB 渲染能力（如 Three.js）。

- **第二步：校验地域与基础设施约束**  
  - 所有模态均要求 **API Key、Endpoint、模型开通地域三者一致**；  
  - 若业务已部署在北京，且需 3D 能力 → `Tripo` 是唯一选项；  
  - 若需全球部署 → 图像/视频生成可选新加坡或弗吉尼亚，但需分别申请对应地域密钥与开通模型。

- **第三步：设计调用架构**  
  - **同步优先**：图像生成新模型 → 直接 HTTP 请求，简化错误处理

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


