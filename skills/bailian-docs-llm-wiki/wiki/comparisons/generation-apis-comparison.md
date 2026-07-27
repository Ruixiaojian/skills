# 多模态生成能力对比：图像、视频与3D生成API

本文旨在为开发者提供百炼平台多模态生成能力的横向技术对比，聚焦**图像生成（Image Generation）**、**视频生成（Video Generation）** 和 **3D生成（3D Generation）** 三类核心AIGC API。随着内容创作向高维化、沉浸式演进，准确理解各模态在输入约束、输出形态、调用范式、计费逻辑及适用边界上的差异，是构建稳定、高效、可扩展生成服务的关键前提。本对比基于当前（2024年Q3）百炼平台正式发布的API文档与生产实践规范整理，适用于技术选型、架构设计与成本预估。

## 关键维度对比表

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D生成（3D Generation） |
|------|------------------------------|------------------------------|--------------------------|
| **核心能力** | 文生图（T2I）、图生图（I2I）、局部编辑、风格迁移、垂直工具（虚拟模特、海报生成等） | 文生视频（T2V）、图生视频（I2V）、首尾帧生成（KF2V）、参考生视频（R2V）、动作/口型迁移、视频编辑 | 文生3D、单图生3D、多图生3D（前/左/后/右四视角），支持PBR材质与无贴图模型 |
| **输入格式** | • `prompt`（文本）或 `messages`（结构化对话）<br>• 可选：`image_url`（图生图）、`mask_image_url`（局部编辑）<br>• 支持多图输入（如Kling最多14张参考图） | • `input.prompt`（纯文本）<br>• `input.media`：支持 `image_url`（I2V）、`first_frame`+`last_frame`（KF2V）、`image_url`数组（R2V）、`video_url`+`audio_url`（对口型）<br>• 所有URL需HTTPS、公网可访问 | • 三者**互斥**：<br> ✓ `input.prompt`（≤1024字符）<br> ✓ `input.image`（单张JPEG/PNG，20–6000px，≤20MB）<br> ✓ `input.images`（长度为4的数组，顺序固定为【前、左、后、右】，空视角填 `{}`） |
| **输出格式** | • 直接返回Base64编码图片（同步）或带有效期（24h）的`image_url`（异步）<br>• 支持分辨率语义值（`"1K"`/`"4K"`）与像素格式（`"1024*1024"`） | • 异步返回带有效期（24h）的`output.video_url`（MP4/H.264）<br>• 同时返回`output.preview_image_url`（封面图） | • 异步返回：<br> ✓ `pbr_model_url`（GLB格式，含PBR材质，有效期2h）<br> ✓ `rendered_image_url`（预览图，有效期2h）<br> ✓ 或 `base_model_url`（无贴图基础网格，需显式设 `texture=false & pbr=false`） |
| **支持模型（代表性）** | • 通用：`qwen-image-3.0-pro`, `wan2.7-image-pro`, `vidu/vidu-image_reference2image`, `z-image-turbo`<br>• 垂直：`wanx-virtualmodel`, `shoemodel-v1`, `wanx-poster-generation-v1` | • T2V：`vidu/viduq3-turbo_text2video`, `kling/kling-v3-video-generation`, `wan2.7-t2v-2026-06-12`<br>• I2V/KF2V：`wan2.7-t2v`, `pixverse-c1-it2v`<br>• R2V/编辑：`pixverse-c1-r2v`, `wan2.7-videoedit`, `pixverse/pixverse-lipsync` | • `Tripo/Tripo-H3.1`（高精度，≤200万面，支持`geometry_quality: "ultra"`）<br>• `Tripo/Tripo-P1.0`（专业级，≤2万面，推理更快） |
| **API端点（推荐）** | • 同步：`POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`<br>• 异步：`POST /api/v1/services/aigc/text2image/image-synthesis`（旧模型） | • 统一异步端点：<br>`POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`<br>（万相2.7及新版模型均使用此路径） | • 异步专用端点：<br>`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`<br>（**仅华北2北京地域可用**） |
| **调用模式** | • **混合模式**：<br> ✓ `wan2.6`/`wan2.7-image-pro`/`qwen-image-3.0-pro` 等支持**同步调用**（即时返回）<br> ✓ `wanx-v1`/`wanx-x-painting` 等需**异步调用**（轮询`task_id`） | • **强制异步**：<br>所有模型均需 `X-DashScope-Async: enable` 头，创建任务后轮询 `GET /api/v1/tasks/{task_id}` | • **强制异步**：<br>必须携带 `X-DashScope-Async: enable`，轮询 `GET /api/v1/tasks/{task_id}`，**不支持同步** |
| **计费方式** | • 免费额度：多数工具模型（如`wanx-x-painting`）提供500张免费额度<br>• 按量计费：商业化模型（如`wan2.6-t2i`）按**成功生成图片张数**计费（0.02元/张起）<br>• 主账号统一扣费，RAM子账号不独立计量 | • 按**成功生成视频条数**计费<br>• 不同模型单价差异显著（如Vidu Turbo vs Kling V3）<br>• 任务失败（如输入错误、超时）不计费<br>• 部分模型（如`emo-v1`）存在并发任务数限制（通常为1） | • 按**成功生成3D模型个数**计费<br>• `Tripo-H3.1`（高面数）单价高于 `Tripo-P1.0`（低面数）<br>• 任务失败不扣费；成果URL过期未下载不额外计费 |
| **典型场景** | • 社媒配图批量生成<br>• 电商商品图AI换背景/换模特<br>• UI设计稿辅助出图<br>• 创意海报/营销素材一键生成<br>• 局部修图与风格迁移 | • 短视频创意脚本可视化（T2V）<br>• 产品动态展示（I2V/KF2V）<br>• 数字人直播/口型驱动（LipSync）<br>• 影视分镜预演与角色一致性视频生成（R2V）<br>• 视频风格化重绘（如转水墨风） | • 游戏/AR/VR资产快速建模（文生3D）<br>• 工业零件逆向建模（单图/多图生3D）<br>• 电商3D商品展示（多视角建模）<br>• 建筑/家居可视化方案生成 |

## 各方案适用场景建议

### ✅ 图像生成 —— 推荐用于「高频、轻量、确定性输出」场景  
- **适用**：需要毫秒级响应的前端交互（如设计工具实时预览）、批量图文生成（千张级/日）、对输出分辨率与风格一致性要求高但无需时序信息的任务。  
- **慎用**：当业务强依赖视频动态表达（如动作演示）、或需三维空间结构理解（如物体拓扑关系）时，图像生成无法替代视频或3D方案。  
- **提示**：优先选用支持同步调用的新模型（如 `wan2.7-image-pro`, `qwen-image-3.0-pro`）以降低延迟；对水印敏感场景，确认模型是否支持 `watermark=false`（如 `wan2.7-image-pro`）。

### ✅ 视频生成 —— 推荐用于「动态表达、跨帧一致性、人机交互」场景  
- **适用**：数字人播报、短视频营销、教育动画制作、产品功能演示、跨模态驱动（音频→口型→视频）。  
- **慎用**：对生成时长控制要求极严（如实时流媒体）、或需精确物理仿真（如流体/布料动力学）的工业级应用；此时建议结合专业引擎二次渲染。  
- **提示**：务必遵守**地域强一致性原则**（模型/Endpoint/API Key同地域）；对R2V等复杂任务，提前校验参考图质量（建议使用`*-detect`接口）；轮询时采用指数退避策略避免触发限流。

### ✅ 3D生成 —— 推荐用于「空间建模、可交互资产、下游工程集成」场景  
- **适用**：游戏开发原型、AR商品试穿、工业设计快速验证、建筑可视化、3D打印前模型生成。  
- **慎用**：需要实时渲染或物理碰撞模拟的场景（生成结果需导入Unity/Unreal等引擎进一步处理）；对纹理细节要求极高且需手工精修的影视级资产。  
- **提示**：**仅限华北2（北京）地域**，务必使用该地域专属API Key与Workspace域名；成果URL有效期仅2小时，务必在轮询成功后立即下载并持久化存储；多图输入严格遵循【前/左/后/右】顺序，缺失视角必须用 `{}` 占位。

## 面向开发者的选型参考指南

1. **从输入源头判断**  
   - 若输入仅为文本描述 → 优先评估图像生成（快、稳、便宜）；若需动态演绎 → 升级至视频生成；若需空间结构 → 选用3D生成。  
   - 若输入含单张图片 → 图像编辑（I2I）或视频首帧生成（I2V）均可；若需重建三维几何 → 必选3D生成。  
   - 若输入含多视角图片（≥2张）→ 3D生成是唯一原生支持方案。

2. **从输出需求判断**  
   - 输出需嵌入网页/APP直接展示 → 图像（静态）或视频（动态）更友好；  
   - 输出需导入3D引擎/进行CAD操作 → 3D生成（GLB格式）是标准选择；  
   - 输出需支持用户旋转/缩放交互 → 3D生成 + WebXR方案为最优解。

3. **从工程约束判断**  
   - **延迟敏感型应用**（如设计工具实时反馈）→ 优先图像同步API；  
   - **资源受限型部署**（如边缘设备）→ 图像生成对网络/算力要求最低；  
   - **合规与安全要求高** → 所有方案均支持业务空间专属域名（`{WorkspaceId}.region.maas.aliyuncs.com`），强烈推荐启用以规避通用域名风险。

4. **成本优化建议**  
   - 利用免费额度测试垂直工具模型（如`wanx-poster-generation-v1`做海报、`shoemodel-v1`做鞋靴展示）；  
   - 视频/3D任务耗时长、费用高，务必在提交前做输入校验（如图片URL可达性、分辨率合规性），避免无效扣费；  
   - 对3D生成结果，若仅需基础网格（无材质），显式设置 `texture=false & pbr=false` 可降低成本。

> **最后提醒**：所有多模态API均依赖DashScope统一认证框架，请始终使用业务空间专属域名，并定期更新API Key权限。模型迭代迅速（如万相V1已归档、V2/V2.7为当前主力），新项目请严格参照[模型市场](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)最新状态选型，避免依赖Legacy模型。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


