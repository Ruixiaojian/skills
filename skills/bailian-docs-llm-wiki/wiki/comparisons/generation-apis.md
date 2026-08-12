# 多模态生成 API 对比：图像、视频与3D生成

为帮助开发者快速理解百炼平台在多模态生成领域的技术能力边界与工程适配要点，本文系统对比图像生成、视频生成与3D生成三类核心 API 的关键特性。对比基于当前（2024年Q2）正式上线的模型能力、调用协议、计费策略及运维约束，旨在支撑技术选型决策——尤其面向 AIGC 应用开发、内容工业化生产、数字人/虚拟空间构建等场景。

---

## 关键维度对比表

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D生成（3D Generation） |
|------|------------------------------|------------------------------|--------------------------|
| **核心输入格式** | 文本（[prompt](../guides/prompt.md)）、图像 URL（图生图/局部编辑）、涂鸦草图、多图融合；支持图文混排提示 | 文本、单图/首帧/首尾帧图像 URL、参考视频 URL、音频 URL（口型替换）、多模态组合（如图+[prompt](../guides/prompt.md)+audio） | 文本（[prompt](../guides/prompt.md)）、单张图像 URL（单图生3D）、4视角图像数组（前/左/后/右，空位用 `{}` 占位） |
| **输出格式** | Base64 编码图像（同步）、公网可访问 HTTPS URL（异步）；支持 PNG/JPEG；部分模型返回多图、带掩码或分割结果 | 公网可访问 HTTPS URL（MP4/H.264）；部分模型支持音频嵌入、多分辨率版本（如 720P/1080P）、风格化渲染帧 | GLB 格式 PBR 材质模型（`pbr_model_url`）、无贴图基础网格（`base_model_url`）、预览图（`rendered_image_url`）；均含 2 小时有效期 |
| **主流支持模型** | `qwen-image-3.0-pro`、`wan2.7-image-pro`、`z-image-turbo`（同步）；`wanx-sketch-to-image-lite`、`virtualmodel-v2`、`shoemodel-v1`（异步） | `wan3.0-video`、`wan2.7-video`、`pixverse/pixverse-c1-t2v`、`vidu/viduq3-turbo_text2video`、`emo-v1`、`liveportrait` | `Tripo/Tripo-H3.1`（高精度，≤200万面）、`Tripo/Tripo-P1.0`（快速，≤2万面） |
| **API 端点（推荐）** | `/api/v1/services/aigc/multimodal-generation/generation`（同步）<br>`/api/v1/services/aigc/multimodal-generation/generation` + `X-DashScope-Async: enable`（异步） | `/api/v1/services/aigc/video-generation/video-synthesis`（主流）<br>`/api/v1/services/aigc/image2video/video-synthesis`（部分旧版万相模型） | `/api/v1/services/aigc/video-generation/3d-generation`（注意路径中仍为 `video-generation`，属历史命名约定） |
| **调用模式** | **混合模式**：高质量通用模型（如 `wan2.7-image-pro`）支持同步；垂直工具链（如涂鸦、试穿）强制异步 | **强制异步**：所有模型均需 `task_id` 轮询；无同步接口 | **强制异步**：必须携带 `X-DashScope-Async: enable`；无同步能力 |
| **地域约束** | 支持北京、新加坡、弗吉尼亚等多地域；API Key、Workspace ID、Endpoint 必须同地域 | 强绑定地域：模型、API Key、Workspace ID、Endpoint 四者严格同地域（如新加坡模型不可用北京 Key） | **仅限华北2（北京）地域**：模型服务、API Key、Workspace ID、Endpoint 均必须为北京；其他地域调用失败 |
| **计费方式** | 免费额度：500 张 / 90 天（主账号与 RAM 子账号共享）；按次计费（如 `wanx-style-repaint-v1` 0.12 元/张）；限时免费模型额度用尽即停用 | 按模型独立计费：免费额度与单价差异大（如 `emo-v1` 与 `wan3.0-video` 不同）；需查阅[模型价格页](https://help.aliyun.com/zh/model-studio/models)；无统一基础额度 | 按任务计费：`Tripo-H3.1` 与 `Tripo-P1.0` 单价不同；无公开免费额度；需开通服务后查看控制台实时报价 |
| **典型响应延迟** | 同步：3–8 秒（`wan2.7-image-pro` @ 2K）；异步：10–60 秒（复杂编辑类） | 30–300 秒（5–30 秒视频）；数字人动画类（如 `liveportrait`）通常 60–120 秒 | 120–600 秒（文生3D约 3–5 分钟；单图生3D约 2–4 分钟；多图生3D约 5–10 分钟） |
| **并发限制（典型）** | QPS ≤2；同时处理任务数 ≤1（部分模型如 `image-out-painting` 支持 ≤5） | QPS 1–5（依模型而异，如 `emo-v1` 限 1 QPS）；同时任务数 1–100（详见各模型文档） | RPS ≤20（轮询查询）；单任务生成期间无额外并发限制，但 `task_id` 查询需错峰 |

---

## 适用场景建议

| 场景类型 | 推荐方案 | 理由说明 |
|----------|----------|----------|
| **高频轻量创意输出**（电商主图生成、营销海报、社媒配图） | ✅ 图像生成（同步模型） | `wan2.7-image-pro` 或 `qwen-image-3.0-pro` 支持毫秒级响应、多尺寸输出、水印开关，契合低延迟批量调用需求；SDK 集成成熟，错误处理完备。 |
| **动态内容工业化生产**（短视频脚本落地、产品演示动画、数字人直播素材） | ✅ 视频生成（`wan2.7-video` / `pixverse` 系列） | 支持首尾帧控制、多镜头分镜描述、风格重绘与超分增强；异步架构天然适配后台队列调度；`wan2.7+` 协议语义更清晰，降低 prompt 工程复杂度。 |
| **三维资产快速构建**（游戏原型建模、AR 商品展示、工业设计验证） | ✅ 3D生成（`Tripo/Tripo-H3.1`） | 高面数 PBR 输出直接兼容 Unity/Unreal；多视角输入显著提升几何准确性；北京地域专属服务保障模型稳定性与合规性，适合企业级资产管线集成。 |
| **跨模态协同工作流**（“文→图→视频→3D”链路） | ⚠️ 混合使用 + 统一异步调度层 | 图像生成可作为视频/3D的输入源（需确保 URL 公网可达、格式合规）；建议封装统一任务管理器，抽象 `task_id` 生命周期（创建→轮询→下载→清理），避免地域/协议碎片化。 |
| **实时交互应用**（Web端AI画板、AR试穿、虚拟主播） | ❌ 视频/3D生成不适用<br>✅ 图像生成（Turbo模型）优先 | 视频与3D生成延迟过高（分钟级），无法满足实时反馈；`z-image-turbo` 支持 1 秒内返回 1024×1024 图像，是唯一满足亚秒级交互要求的方案。 |

---

## 开发者技术选型参考

- **优先选择同步接口**：若业务对延迟敏感（<10 秒）、请求量稳定、无需复杂后处理，**图像生成中的 `wan2.7-image-pro` 或 `qwen-image-3.0-pro` 是最优起点**；避免为简单需求引入异步轮询复杂度。
  
- **务必校验地域一致性**：视频与3D生成对地域强绑定，**切勿复用跨地域 API Key 或 Workspace ID**；建议在初始化阶段增加地域自检逻辑（如通过 `/api/v1/status` 探测 Endpoint 可达性）。

- **输入 URL 是高频故障点**：三类 API 均要求输入资源为公网 HTTPS、无中文路径、大小合规（图像 ≤10 MB，视频 ≤500 MB，3D 图像 ≤20 MB）。**强烈建议封装预签名 OSS URL 生成器**，避免前端直传导致鉴权失败。

- **参数兼容性需逐模型验证**：`prompt_extend` 在图像 V2/V3 模型中行为不同；视频 `wan2.7+` 已弃用该参数；3D 生成中 `texture` 与 `pbr` 必须协同设置。**严禁跨模型复用请求体模板**，应以各模型官方 API 参考文档为准。

- **异步任务需健壮轮询策略**：视频与3D生成必须实现指数退避轮询（初始间隔 2s，上限 30s），并设置总超时（建议 ≤25 分钟）；任务失败时，应解析 `code` 字段（如 `InvalidParameter`、`InputDownloadFailed`）而非仅依赖 `message` 文本。

- **成本管控前置化**：图像生成有统一免费额度；视频与3D生成需按模型单独预算。**上线前务必在控制台启用用量告警**（阈值建议设为日均预估量的 120%），避免突发调用量导致费用激增。

--- 

> 本文档依据百炼平台 2024 年 6 月发布能力编写。模型能力、计费策略与接口细节可能随版本迭代更新，请以 [DashScope 官方文档中心](https://help.aliyun.com/zh/model-studio/) 及控制台实时信息为准。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


