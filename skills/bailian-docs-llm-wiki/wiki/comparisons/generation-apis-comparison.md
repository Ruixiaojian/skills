# 多模态生成能力对比：图像、视频与3D生成

为帮助开发者快速理解百炼平台在多模态内容生成领域的技术布局与能力边界，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心能力。对比聚焦实际工程落地的关键维度——包括输入/输出规范、模型生态、调用机制、资源约束与成本模型等，旨在为产品设计、技术选型与架构决策提供客观、可执行的参考依据。

---

## 关键维度对比表

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D生成（3D Generation） |
|------|------------------------------|------------------------------|--------------------------|
| **输入格式** | • 文本提示（`prompt`）<br>• 图像 URL（支持 JPG/PNG/WEBP，≤10MB）<br>• 局部重绘需掩码图（`mask_image_url`）<br>• 支持图文混排（`messages` 数组） | • 文本提示（`input.prompt`）<br>• 首帧/首尾帧图像 URL（`media` 数组，`type: "image"`）<br>• 参考视频 URL（`type: "video"`）<br>• 多模态混合输入（图像+视频+文本） | • 文本提示（`input.prompt`）<br>• 单张图像 URL（`input.image`，JPEG/PNG，20–6000px，≤20MB）<br>• 四视角图像数组（`input.images`，顺序：前/左/后/右，空位用 `{}` 占位） |
| **输出格式** | • PNG（默认，含透明通道）<br>• JPG（部分模型如 `qwen-mt-image`）<br>• 输出为直传 URL（有效期 24 小时） | • MP4（H.264 编码，分辨率可配）<br>• 输出为直传 URL（有效期 24 小时） | • GLB（PBR 材质模型，含贴图，`pbr_model_url`）<br>• GLB（无贴图基础网格，仅当 `texture=false && pbr=false` 时返回 `base_model_url`）<br>• WebP 渲染预览图（`rendered_image_url`，2 小时有效） |
| **主流支持模型** | • 通用：`qwen-image-3.0-pro`、`wan2.6-t2i`、`z-image-turbo`、`kling/kling-v3-omni-image-generation`<br>• 垂直：`wanx-background-generation-v2`、`shoemodel-v1`、`outfitanyone`、`facechain-portrait-generation` | • 文生视频：`vidu/viduq3-turbo_text2video`、`kling/kling-v3-video-generation`、`wan3.0-video`<br>• 图生视频：`wan2.7-i2v`、`vidu/viduq3-pro-fast_img2video`<br>• 动作驱动：`emo-v1`、`animate-anyone-gen2`、`videoretalk`<br>• 后处理：`pixverse/pixverse-upscale`、`video-style-transform` | • `Tripo/Tripo-H3.1`（高精度，≤200 万面，支持 `geometry_quality: "ultra"`）<br>• `Tripo/Tripo-P1.0`（快速生成，≤2 万面） |
| **API 端点（推荐）** | `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation`<br>（同步/异步双模式） | `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`<br>（强制异步） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`<br>（强制异步，**仅华北2可用**） |
| **调用模式** | • **同步优先**：`qwen-image-3.0-pro`、`wan2.6-t2i`、`z-image-turbo` 等主流模型支持秒级响应<br>• **异步可选**：长耗时任务（如局部擦除、海报生成）需轮询 | • **强制异步**：所有模型均不支持同步返回<br>• 必须提交任务 → 获取 `task_id` → 轮询 `/tasks/{task_id}`<br>• 建议轮询间隔 ≥10 秒，超时容忍 ≥10 分钟 | • **强制异步**：所有请求必须携带 `X-DashScope-Async: enable`<br>• `task_id` 有效期严格为 **24 小时**<br>• 建议轮询间隔 ≥15 秒；高频查询建议启用[异步回调](https://help.aliyun.com/zh/model-studio/async-task-api) |
| **计费方式** | • 免费额度：主账号 + RAM 子账号共享 **500 张/90 天**<br>• 商业化模型（如 `wan2.6-t2i`）按张计费（例：0.02 元/张）<br>• 限时免费模型（如 `wanx-x-painting`）额度用尽即停用 | • 多数模型提供免费额度（如 `emo-v1`、`liveportrait`、`videoretalk`）<br>• 按任务计费（非按秒/帧），不同模型单价差异大<br>• 无统一“张/秒”单位，以单次 `video-synthesis` 请求为计费单元 | • 按任务计费，与生成精度强相关：<br> – `Tripo/Tripo-P1.0`：基础价格较低，适合原型验证与轻量应用<br> – `Tripo/Tripo-H3.1`（`ultra` 模式）：单价显著提升，适用于工业级建模需求<br>• 无公开免费额度，需开通服务后查看控制台实时报价 |
| **典型场景** | • 电商素材生成（商品图、背景替换、AI试衣）<br>• 设计辅助（海报扩图、风格迁移、文字艺术）<br>• 内容创作（插画生成、图文混排、中英文文本渲染）<br>• 人像增强（写真生成、局部重绘、虚拟模特） | • 短视频内容生产（文生口播视频、营销广告片）<br>• 数字人交互（播报、唱演、表情包、口型同步）<br>• 视频创意编辑（风格迁移、动作复刻、首尾帧动画）<br>• 教育/培训（动态演示、实验过程可视化） | • 电商 3D 商品展示（单图转 3D 模型）<br>• 游戏/AR 应用资产生成（文生低多边形模型）<br>• 工业设计初稿（多视角图→可编辑 3D 网格）<br>• 虚拟空间构建（PBR 材质模型导入 Unity/Unreal） |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 推荐用于「高频、轻量、强可控」场景  
- **适用**：需要快速迭代视觉素材、对输出分辨率/宽高比/风格有精细控制、集成至 CMS 或设计工具链、支持批量生成（`n=1–9`）。  
- **慎用**：对时序一致性无要求但需跨帧语义连贯性（如角色连续动作）；或需物理真实感材质与几何拓扑（如 CAD 级精度）。  
- **开发提示**：优先选用 `qwen-image-3.0-pro`（语义遵循强、中英文兼容好）；电商类任务直接调用垂直模型（如 `shoemodel-v1`）可省去后处理。

### ✅ 视频生成 —— 推荐用于「动态表达、人物驱动、跨模态融合」场景  
- **适用**：需生成带时间维度的内容（口播、舞蹈、产品演示）、已有图像/视频素材需赋予新动作或风格、需数字人播报/情感表达等交互能力。  
- **慎用**：对单帧图像质量要求极高（视频帧通常低于同级别图像模型单帧质量）；或需精确控制每一帧的像素级细节（如关键帧动画）。  
- **开发提示**：文生视频首选 `wan3.0-video`（最长 30 秒，稳定性优）；图生视频优先 `wan2.7-i2v`（兼容性好，首帧保真度高）；动作迁移类任务务必校验输入视频的帧率与姿态清晰度。

### ✅ 3D生成 —— 推荐用于「空间建模、资产复用、引擎集成」场景  
- **适用**：从文本/图片快速构建可导入 Unity/Unreal 的 GLB 模型、生成带 PBR 材质的电商商品 3D 展示页、基于多视角图重建基础工业零件。  
- **慎用**：需毫米级几何精度（如机械装配仿真）；或输入为模糊/遮挡严重/非正交视角的单图；或需实时生成（任务平均耗时 2–8 分钟）。  
- **开发提示**：务必使用华北2专属域名与 API Key；多图输入严格遵循 `[前, 左, 后, 右]` 顺序；如只需基础网格，请**同时设置 `parameters.texture=false` 和 `parameters.pbr=false`**，否则 `base_model_url` 不会返回。

---

## 面向开发者的选型决策指南

| 决策问题 | 推荐路径 | 技术验证建议 |
|----------|----------|--------------|
| **我的应用需要每秒生成 10+ 张高质量图？** | ✅ 选图像生成 + 同步调用<br>→ 使用 `qwen-image-3.0-pro` + `size="2048*2048"` + `n=4` | 测试 QPS 限流：构造并发请求，观察是否触发 `429 Too Many Requests`；确认地域 Endpoint 与 API Key 一致 |
| **我要为电商详情页自动生成 30 秒产品讲解视频？** | ✅ 选视频生成 + 图生视频<br>→ `wan2.7-i2v`（首帧） + `duration=30` + `resolution="1024*576"` | 验证首帧质量：确保输入图分辨率 ≥1024px、主体居中、光照均匀；避免复杂背景干扰模型理解 |
| **我有一组手机拍摄的家具四视角图，想生成可旋转 3D 模型上架？** | ✅ 选 3D生成 + 多图生3D<br>→ `Tripo/Tripo-H3.1` + `geometry_quality="standard"` + `texture=true` | 校验视角顺序：用示例图测试 `[front.jpg, left.jpg, back.jpg, right.jpg]`；检查 URL 是否公网可访问且无中文路径 |
| **我需要将用户上传的头像实时转为 3D 数字人并驱动说话？** | ⚠️ **组合方案更优**<br>→ 图像生成（`facechain-portrait-generation`）→ 3D生成（单图转模）→ 视频生成（`videoretalk` 口型同步） | 分阶段验证：先跑通单图→3D流程，再接入音频驱动；注意各环节地域必须统一（推荐全栈部署于华北2） |
| **我的预算有限，需最大化免费额度？** | ✅ 优先图像生成（500 张/90 天）<br>→ 混合使用 `qwen-image-3.0-pro`（免费额度内） + `z-image-turbo`（快且省） | 记录 `usage` 字段：所有响应中含 `output.usage.total_tokens` / `output.usage.image_count`，用于额度监控 |

> **重要提醒**：  
> - **地域一致性是硬性前提**：图像、视频、3D 三类服务虽共用 DashScope SDK，但模型部署、API Key、Endpoint 均按地域隔离。跨地域调用必然失败，切勿复用其他地域的密钥或域名。  
> - **异步任务需健壮轮询**：视频与3D任务必须实现带退避策略的轮询（如指数退避：1s → 3s → 10s → 30s），并设置全局超时（建议 15 分钟）。  
> - **错误应主动解析而非重试**：`InvalidParameter`、`BadRequest.InputDownloadFailed` 等错误需修正输入后重发；`UNKNOWN` 状态表示 `task_id` 过期，必须新建任务。  

---  
*本文档持续更新，最新模型支持列表与定价请以[百炼控制台模型市场](https://bailian.console.aliyun.com)为准。*

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


