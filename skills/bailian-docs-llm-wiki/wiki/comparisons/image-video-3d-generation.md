# 图像、视频与3D生成能力对比

为帮助开发者快速理解百炼平台在多模态生成领域的技术边界与工程适配要点，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大能力模块。对比聚焦实际开发中高频关注的**接入方式、模型生态、调用范式、资源约束与业务适配性**，旨在支撑技术选型决策——尤其适用于需构建AIGC内容生产流水线的产品、算法与全栈工程师。

---

## 关键维度对比表

| 维度 | 图像生成 | 视频生成 | 3D生成 |
|------|----------|----------|--------|
| **输入格式** | 文本（`prompt`/`messages`）、公网图片URL（支持单图/多图输入）、局部掩码坐标；部分模型支持图文混合输入（如 `qwen-image-3.0`） | 文本、单张首帧图、首尾帧图对、参考图组、参考视频、音频（数字人场景）、检测后结构化数据（如 `emo-detect-v1` 输出） | 文本（`input.prompt`）、单张图（`input.image`）、四视角图组（`input.images`，顺序：前/左/后/右，空位用 `{}` 占位）；三者**互斥**，不可混传 |
| **输出格式** | PNG/JPEG 图像（URL 或 base64），支持水印开关；扩图/擦除等任务返回带 Alpha 通道图像；部分模型输出多张（`n=1–9`） | MP4 视频（H.264 编码），含可选音频轨道；数字人/口型替换类输出带音画同步视频；所有结果均为公网可下载 URL（有效期 24 小时） | GLB 格式 3D 模型（PBR 材质版 `pbr_model_url` 或无贴图基础版 `base_model_url`），附带预览图 `rendered_image_url`（所有 URL 有效期 **2 小时**） |
| **支持模型（代表性）** | • 通用：`qwen-image-3.0-pro`, `wan2.7-image-pro`, `z-image-turbo`<br>• 垂直：`vidu/*`, `facechain`, `wordart`<br>• 工具：`wanx-x-painting`, `image-out-painting`, `shoemodel-v1` | • 通用：`wan3.0-video`, `vidu/viduq3-*`, `kling/kling-v3-*`<br>• 数字人：`wan2.2-s2v`, `emo`, `liveportrait`, `videoretalk`<br>• 编辑：`wan2.7-videoedit`, `pixverse/pixverse-upscale` | • `Tripo/Tripo-H3.1`（高精度，≤200万面，支持 `geometry_quality: "ultra"`）<br>• `Tripo/Tripo-P1.0`（快速，≤2万面）<br>**仅限 Tripo 系列，无第三方模型接入** |
| **API 端点（标准路径）** | `/api/v1/services/aigc/multimodal-generation/generation`（同步）<br>`/api/v1/services/aigc/{service}/image-synthesis`（异步，旧模型）<br>✅ **必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`） | `/api/v1/services/aigc/video-generation/video-synthesis`（新模型统一路径）<br>`/api/v1/services/aigc/image2video/video-synthesis`（万相旧版路径，已不推荐）<br>✅ 同样强依赖业务空间专属域名 | `/api/v1/services/aigc/video-generation/3d-generation`<br>⚠️ **路径命名存在历史遗留问题**（归入 `video-generation` 命名空间，但功能独立）<br>✅ 仅支持华北2（北京）地域专属域名 |
| **调用模式** | • 新模型（`qwen-image-3.0`, `wan2.7-image-pro`, `z-image-turbo`）：**同步调用**（一次请求返回结果）<br>• 老模型（`wanx-v1`, `wanx-x-painting`）：**异步调用**（创建任务 + 轮询）<br>• 所有请求需显式声明 `X-DashScope-Async: enable`（否则报错） | **全量异步调用**：<br>1. `POST` 创建任务 → 返回 `task_id`<br>2. `GET /api/v1/tasks/{task_id}` 轮询（间隔 ≥5s）<br>• `task_id` 有效期 24 小时 | **全量异步调用**：<br>1. `POST` 创建任务 → 返回 `task_id`<br>2. `GET /api/v1/tasks/{task_id}` 轮询（建议间隔 ≥15s，RPS ≤20）<br>• `task_id` 有效期 24 小时；结果 URL 有效期仅 **2 小时** |
| **计费方式** | • 按**生成张数**计费（如 `wan2.7-image-pro`：1024×1024 0.3 元/张）<br>• 免费额度：**500 张/账号**（主账号与 RAM 子账号共享，90 天有效）<br>• 部分轻量模型（`shoemodel-v1`, `wanx-x-painting`）为“免费体验”，额度用尽即停用 | • 按**视频秒数**计费（如 `wan2.2-s2v`：480P 0.5 元/秒）<br>• 部分模型按分辨率/质量档位阶梯计费（如 `pixverse-upscale`）<br>• **无统一免费额度**，邀测模型（如 `wan3.0-video`）需单独申请配额 | • 按**单次任务**计费（与输出面数/质量无关）<br>• 当前定价：`Tripo-H3.1` 15 元/次，`Tripo-P1.0` 5 元/次<br>• **无免费额度**，需预充值或开通后按量扣费 |
| **典型场景** | • 营销海报生成与批量改图<br>• UI 设计稿背景填充/局部重绘<br>• 电商商品图扩图与擦除补全<br>• 创意文字艺术（WordArt）、虚拟模特试穿 | • 短视频广告脚本可视化（文生视频）<br>• 产品演示动画（图生视频+风格迁移）<br>• 数字人播报/唱演/表情包生成<br>• 视频超分、换人、口型同步等后期增强 | • 工业设计概念建模（文生3D）<br>• 电商商品3D展示（单图转3D）<br>• AR/VR内容快速构建（四视角重建）<br>• 游戏资产原型生成 |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「高吞吐、低延迟、强可控」的内容生产
- **推荐场景**：需要快速产出大量静态视觉素材的业务，如电商详情页批量生成、营销活动海报A/B测试、UI组件自动化填充、AI绘画工具集成。
- **选型提示**：
  - 追求**响应速度与成本平衡** → 选用 `z-image-turbo` 或 `wan2.6-t2i`；
  - 要求**强文本遵循与复杂构图** → 优先 `qwen-image-3.0-pro`；
  - 需要**专业级画质与图文混排** → 选用 `wan2.7-image-pro`（支持4K+水印关闭）；
  - 做**垂直领域微调**（人脸/文字/鞋靴）→ 直接调用 `facechain`/`wordart`/`shoemodel-v1`。

### ✅ 视频生成 —— 适合「动态表达、人机交互、跨模态驱动」的应用
- **推荐场景**：短视频内容工厂、企业数字人客服、教育动画制作、游戏过场生成、营销视频自动化剪辑。
- **选型提示**：
  - 构建**端到端文生视频管线** → 使用 `wan3.0-video`（邀测中）或 `vidu/viduq3-turbo_text2video`；
  - 需要**首帧控制+运动连贯性** → `kling/kling-v3-*` 系列更优；
  - 实现**真人驱动型应用**（播报/唱演/舞蹈）→ 必须组合使用检测模型（如 `emo-detect-v1`）+生成模型（如 `emo`），不可跳过合规校验；
  - 做**视频质量增强** → `pixverse/pixverse-upscale`（超清）、`wan2.7-videoedit`（智能剪辑）。

### ✅ 3D生成 —— 适合「物理建模、空间交互、工业级精度」的高价值场景
- **推荐场景**：智能制造原型验证、电商3D商品库建设、元宇宙空间搭建、AR营销素材生成、教育三维教具开发。
- **选型提示**：
  - 要求**高面数与PBR材质**（用于渲染/仿真）→ 必选 `Tripo/Tripo-H3.1` + `geometry_quality: "ultra"`；
  - 追求**极速交付与轻量部署**（如WebGL预览）→ 选用 `Tripo/Tripo-P1.0`；
  - 输入为**实物多角度照片** → 严格按【前/左/后/右】顺序提供4张图，缺一不可；
  - 需要**无贴图基础网格**（供后续材质编辑）→ 同时设置 `"texture": false, "pbr": false`。

---

## 面向开发者的选型决策指南

| 决策问题 | 推荐动作 | 注意事项 |
|----------|----------|----------|
| **我的业务需要最快响应？** | 优先选择**图像生成**（新模型支持同步调用，平均耗时 <3s）；避免视频/3D的强制异步轮询链路 | 视频/3D任务平均耗时：30s–5min（依分辨率/时长/面数而异），需设计前端加载态与失败重试机制 |
| **我已有大量图片素材，想复用生成新内容？** | 图像生成（图生图/局部重绘）和视频生成（图生视频）均支持，但**3D生成仅支持单图或四图输入，不支持任意图生3D** | 图像URL必须公网可访问、HTTPS、无中文字符；视频/3D对图片尺寸/格式要求更严（如3D要求JPEG/PNG，宽高∈[20,6000]px） |
| **我需要跨地域部署？** | 图像/视频生成支持北京/新加坡/弗吉尼亚三地；**3D生成仅限华北2（北京）**，若业务部署在新加坡，需代理或架构调整 | 地域隔离严格：Key、Endpoint、模型列表完全独立，跨地域调用必报 `InvalidApiKey` 或 `404` |
| **我担心成本不可控？** | 图像生成有500张免费额度兜底；视频/3D无免费额度，**务必在控制台开通服务后，先用小规格参数（如3秒视频、P1.0模型）做成本探查** | 视频按秒计费，30秒4K视频成本可达文生图的10倍以上；3D任务无论输出大小均按次计费，但H3.1比P1.0贵3倍 |
| **我的团队缺乏AIGC调优经验？** | 从**标准化程度最高**的能力入手：图像生成参数最统一（`size`/`n`/`prompt`）；视频生成需区分输入类型（`media`结构复杂）；3D生成输入互斥规则严格（易因多传字段报错） | 建议使用 DashScope SDK（Python/Node.js），其自动处理异步轮询、错误重试与鉴权，大幅降低接入门槛 |

> 📌 **最后提醒**：所有能力均**强制要求业务空间专属域名**（`https://{WorkspaceId}.{region}.maas.aliyuncs.com`）。切勿继续使用旧域名 `dashscope.aliyuncs.com`，否则将面临性能下降、限流加剧及未来兼容性风险。迁移路径详见各模块文档中的「使用方式」章节。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


