# [多模态](../concepts/multi-modal.md)生成 API 对比：图像、视频与3D生成

本文档面向百炼平台开发者，旨在系统性对比图像生成、视频生成与3D生成三类核心[多模态](../concepts/multi-modal.md)生成 API 的关键能力与工程特性，帮助技术团队在实际业务场景中快速完成模型选型、架构设计与集成落地。随着AIGC应用从静态内容向动态表达与空间交互演进，理解各模态API在输入输出、调用范式、资源约束及成本结构上的差异，已成为构建高质量生成服务的基础前提。

---

## 关键维度对比表

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D生成（3D Generation） |
|------|------------------------------|------------------------------|--------------------------|
| **核心输入格式** | 文本（`prompt`）、图像URL（`image_url`）、局部掩码（部分编辑模型）；支持多图参考（如 `vidu-image_reference2image`） | 文本（`prompt`）、单图/首帧图、首尾帧对、参考图像组（≤5张）、参考视频、音频（数字人场景）；严格结构化 `media` 数组 | 文本（`prompt`）、单图（`image`）、四视图（`images: [前,左,后,右]`，长度固定为4，空位需填 `{}`） |
| **核心输出格式** | PNG（主流）、JPG（`qwen-mt-image`等少数模型）；含预览图、蒙版、分割结果（按模型能力） | MP4（H.264编码）；含封面图（`output.cover_url`）、分段视频（部分模型）；无原始帧序列 | GLB（PBR材质模型，默认）、WebP预览图；可选无贴图 `base_model_url`（需 `pbr=false & texture=false`） |
| **支持模型（代表）** | `qwen-image-3.0-pro`, `wan2.6-t2i`, `wan2.7-image-pro`, `kling/kling-v3-image-generation`, `virtualmodel-v2` | `happyhorse-1.1-t2v`, `wan3.0-video`, `pixverse/pixverse-c1-kf2v`, `emo-v1`, `vidu/viduq3-ad_reference2video` | `Tripo/Tripo-H3.1`（高精度，≤200万面），`Tripo/Tripo-P1.0`（快速，≤2万面） |
| **API 调用模式** | **混合模式**：<br>• 同步：`qwen-image-3.0-pro`, `z-image-turbo` 等（秒级返回）<br>• 异步：`wanx-v1`, `image-out-painting` 等（需轮询 `task_id`） | **强制异步**：<br>全部模型均需 `X-DashScope-Async: enable`，创建任务 → 轮询 `task_id` → 获取 `output.video_url`；任务有效期 24 小时 | **强制异步**：<br>必须携带 `X-DashScope-Async: enable`；创建任务 → 轮询 `task_id` → 解析 `pbr_model_url`/`rendered_image_url`；任务有效期 24 小时 |
| **统一 Endpoint（推荐）** | `/api/v1/services/aigc/multimodal-generation/generation`（同步）<br>`/api/v1/services/aigc/image2image/image-synthesis`（部分异步） | `/api/v1/services/aigc/video-generation/video-synthesis`（全系列统一） | `/api/v1/services/aigc/video-generation/3d-generation`（注意：路径含 `video-generation`，属历史兼容命名） |
| **地域与域名要求** | 严格匹配：API Key、Workspace ID、Endpoint 地域三者一致；推荐使用 `https://{WorkspaceId}.{region}.maas.aliyuncs.com` | 同图像生成：跨地域调用直接失败；`task_id` 查询也需同地域域名 | **仅支持华北2（北京）**；Endpoint 必须为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`；其他地域不可用 |
| **计费方式** | • 免费额度：多数模型提供 500 张/90天<br>• 后付费：按**成功生成的图片张数**计费（如 `wanx-v1`: 0.16元/张）；失败/无效输入不计费 | • 免费额度有限（如 `emo-v1` 初始 10 分钟）<br>• 后付费：按**视频秒数**（如 `emo-v1`）、**任务次数**（如 `happyhorse-1.1-t2v`）或**分辨率×时长因子**计费；失败任务不计费 | • 按**任务次数**计费（单次 = 1 个3D模型）<br>• `Tripo-H3.1` 与 `Tripo-P1.0` 单价不同（H3.1 更高）<br>• 无免费额度，需预充值或开通后付费 |
| **典型场景** | 创意海报生成、电商主图/详情图、AI试衣、虚拟模特展示、图像修复与重绘、风格迁移、实例分割 | 短视频营销、数字人口播、产品动态演示、广告创意视频、动作模仿动画、口型同步、视频超分与风格化 | 工业设计原型、游戏资产建模、AR/VR内容生产、电商360°商品展示、建筑可视化、NFT 3D艺术品生成 |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「高吞吐、低延迟、强可控」的视觉内容生产  
- **首选场景**：需要批量生成高质量静态图的业务，如电商图文上新（千张级/日）、营销海报A/B测试、个性化头像生成、UI组件素材库建设。  
- **推荐组合**：`qwen-image-3.0-pro`（通用强鲁棒性） + `wan2.7-image-pro`（精细编辑） + `aitryon-plus`（服装垂类）。  
- **避坑提示**：避免在高并发场景下混用同步/异步模型；注意 `size` 参数在不同模型间的像素范围差异（如 `wan2.6-t2i` vs `qwen-image-3.0-pro`），务必查阅对应文档。

### ✅ 视频生成 —— 适合「强调时序表达、[多模态](../concepts/multi-modal.md)协同、角色驱动」的动态内容创作  
- **首选场景**：企业宣传短视频自动化、教育课程动画生成、直播数字人实时口播、电商商品动态展示、创意广告脚本转视频。  
- **推荐组合**：`wan3.0-video`（全能参考型，T2V/I2V/R2V统一接口） + `emo-v1`（高拟真唱演） + `pixverse/pixverse-upscale`（后处理增强）。  
- **避坑提示**：首尾帧模型（如 `pixverse-c1-kf2v`）对构图一致性要求极高；所有视频模型均**不支持同步调用**，前端需设计合理的加载态与重试机制；注意 `duration` 与 `resolution` 的组合限制（如 `720P` 最大支持 15 秒）。

### ✅ 3D生成 —— 适合「需空间建模、物理仿真、跨平台复用」的专业级三维内容构建  
- **首选场景**：制造业快速原型验证、游戏/元宇宙资产管线、AR商品试穿底层建模、建筑可视化初稿、3D打印前模型生成。  
- **推荐组合**：`Tripo/Tripo-H3.1`（高保真工业/艺术建模） + `Tripo/Tripo-P1.0`（草图→快速白模，用于内部评审）。  
- **避坑提示**：**仅限北京地域**，跨域调用必失败；四视图输入必须严格按 `[前,左,后,右]` 顺序且长度为4；无贴图模型需同时设置 `pbr: false` 和 `texture: false`，缺一不可；所有输出 URL 有效期仅 **2 小时**，务必及时下载并持久化存储。

---

## 技术选型参考指南（面向开发者）

| 选型维度 | 决策建议 |
|----------|----------|
| **开发效率优先** | 选图像生成：同步接口（如 `qwen-image-3.0-pro`）可直连返回 Base64 或 URL，调试链路最短；SDK 封装成熟，错误码语义清晰。视频与3D均需实现完整异步状态机（创建→轮询→下载），建议封装通用 Task Manager 模块复用。 |
| **生产稳定性优先** | 选图像生成（同步模型）+ 视频生成（`wan3.0-video`）：二者均采用新版统一协议（`/video-generation/` 路径已收敛），文档完备、错误反馈明确；避免使用已标记“旧版协议”的 `wan2.5-i2i-preview` 等模型。 |
| **成本敏感型项目** | 优先评估图像生成免费额度（500张/90天）是否覆盖冷启动期；视频/3D暂无普惠免费额度，建议用 `Tripo-P1.0` 替代 `H3.1` 降低建模成本，或用 `happyhorse-1.1-t2v`（3秒短片）替代长视频以控费。 |
| **多模态流水线集成** | 推荐采用「图像→视频→3D」分层架构：<br>• 图像生成输出作为视频首帧/参考图；<br>• 视频生成输出封面图可反哺图像模型做 [prompt](../guides/prompt.md) 优化；<br>• 3D模型导出 GLB 后，可用 `image-instance-segmentation` 提取部件掩码，用于后续纹理映射。注意三者地域隔离（3D仅北京），需在网关层做地域路由。 |
| **安全与合规要求高** | 所有 API 均需通过 Workspace 专属域名调用，天然隔离租户流量；敏感业务（如医疗/金融图像生成）应禁用 `watermark: false`，并启用 OSS 回源鉴权确保输入图 URL 安全；3D 输出需校验 GLB 文件完整性（SHA256），防范模型投毒。 |

> **最后提醒**：三类 API 均依赖统一的 DashScope 认证体系（`Authorization: Bearer $DASHSCOPE_API_KEY`），但**绝不共享限流配额**。图像 QPS、视频 RPS、3D 任务并发数各自独立限制，请在控制台分别监控配额使用率，避免因某类服务突发流量导致其他服务被限流。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


