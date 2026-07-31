# 图像、视频与3D生成能力对比

为帮助开发者快速理解百炼平台在多模态生成领域的技术布局与能力边界，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心能力。对比聚焦于**工程落地关键维度**，包括调用协议、模型生态、资源约束与成本模型，旨在为产品设计、技术选型及架构规划提供客观、可操作的决策依据。所有信息均基于百炼平台当前（2024年中至2026年初）正式发布的API文档与控制台能力。

## 能力维度对比表

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D生成（3D Generation） |
|------|------------------------------|------------------------------|--------------------------|
| **核心输入格式** | 文本（[prompt](../guides/prompt.md)）、图像URL（支持混合输入：text + image）、掩码图（mask）、模板图（template）等；支持多模态组合（如虚拟模特需 `template_image_url` + `shoe_image_url`） | 文本（[prompt](../guides/prompt.md)）、单图/首帧/首尾帧/参考图URL、视频URL、音频URL；`media` 字段为结构化数组，明确标注 `type`（如 `"first_frame"`、`"audio_url"`） | 文本（`prompt`）、单图URL（`image`）、或多图数组（`images`，**严格固定长度为4**，视角顺序为前/左/后/右，空位用 `{}` 占位）；三者**互斥**，不可混用 |
| **核心输出格式** | PNG/JPG 图像（Base64 或公网可访问 URL）；支持多张输出（`n=1–6`）；含预览图、扩图结果、擦除补全图等多样化产物 | MP4 视频（公网可访问 URL）；含渲染预览图（`rendered_image_url`）；部分模型支持分镜帧序列或中间帧导出（需查具体模型文档） | GLB 格式 3D 模型（PBR材质版 `pbr_model_url` 或基础网格版 `base_model_url`）、渲染预览图（`rendered_image_url`）；所有结果 URL **有效期仅2小时** |
| **支持模型（代表）** | `qwen-image-3.0-pro`（T2I+I2I）、`wan2.7-image-pro`（通用编辑）、`wanx-x-painting`（局部重绘）、`shoemodel-v1`（鞋靴试穿）、`image-out-painting`（扩图）等数十种垂直模型 | `wan2.7-t2v`（文生视频）、`wan2.7-i2v`（首帧生视频）、`pixverse-c1-kf2v`（首尾帧）、`vidu/viduq3-turbo_text2video`、`emo-v1`（唱演）、`liveportrait`（轻量播报）等 | `Tripo/Tripo-H3.1`（高精度，≤200万面）、`Tripo/Tripo-P1.0`（快速，≤2万面）；**仅Tripo系模型，无其他厂商替代选项** |
| **API 端点（典型）** | `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`（同步/异步共用路径，靠请求头区分） | `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（新路径，推荐）<br>⚠️ 部分旧模型仍用 `/api/v1/services/aigc/image2video/...`（将逐步下线） | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`（**仅华北2北京地域**，路径含 `video-generation` 但属3D服务，属历史命名遗留） |
| **调用模式** | **混合支持**：<br>• 同步：`wan2.6-t2i`、`qwen-image-3.0-pro`、`z-image-turbo` 等新版模型，直接返回结果<br>• 异步：`wanx-v1`、`wanx-x-painting`、`image-out-painting` 等，需轮询 `GET /api/v1/tasks/{task_id}` | **强制异步**：<br>所有模型均不支持同步调用；必须设置 `X-DashScope-Async: enable`；创建任务后轮询 `GET /api/v1/tasks/{task_id}`（通用域名或业务空间域名） | **强制异步**：<br>不支持同步；`X-DashScope-Async: enable` 为硬性要求；轮询地址与创建地址同属北京地域专属域名，`task_id` 有效期24小时 |
| **计费方式** | **按成功生成图片张数计费**（如 `wanx-v1`: 0.16元/张）；部分模型限时免费或体验额度制（如 `wanx-poster-generation-v1`）；无“失败不计费”兜底说明 | **按成功生成视频条数计费**；多数模型按 `task_id` 成功完成计1次（无论时长/分辨率）；数字人模型（如 `emo-v1`）有并发限制（1 QPS），超限请求可能被拒绝或排队；无失败退费机制 | **按成功生成任务计费**（1 task = 1次调用）；未明确单价，以控制台资费页为准；**失败任务（`FAILED`/`UNKNOWN`）是否计费未说明，建议按成功任务预估成本** |
| **地域支持** | **多地域支持**：华北2（北京）、新加坡、美国（弗吉尼亚）等；但**必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），禁用通用域名 `dashscope.aliyuncs.com` | **强地域绑定**：模型、Endpoint、API Key 必须同地域（如开通北京模型，必须用北京Endpoint + 北京API Key）；跨地域调用返回 `401 Unauthorized` | **单地域锁定**：**仅支持华北2（北京）地域**；其他地域域名不可用；API Key 必须为北京地域专属 |
| **典型场景** | • 创意海报/营销图批量生成<br>• 电商商品图智能换背景/擦除水印<br>• 虚拟模特穿搭展示、鞋靴AI试穿<br>• UI设计稿扩图、局部重绘迭代<br>• FaceChain写真、WordArt文字艺术 | • 短视频广告脚本→成片（T2V）<br>• 产品主图→动态展示视频（I2V）<br>• 多角度产品图→360°旋转视频（R2V）<br>• 主播口播音频→数字人口型同步视频（LipSync）<br>• 静态海报→舞蹈复刻/动作迁移短视频 | • 工业设计草图→高精度3D原型（`Tripo-H3.1` + `ultra`）<br>• 电商单品图→带材质3D模型用于AR试穿（`Tripo-P1.0`）<br>• 四视图产品图→标准GLB交付（`images` 输入）<br>• 游戏道具概念图→低面数可交互模型（`P1.0` + `texture: false`） |

## 各方案适用场景建议

### ✅ 图像生成 —— 推荐用于「高频、轻量、强可控」的视觉内容生产
- **适用**：需要快速产出大量静态图的场景，如A/B测试素材生成、电商详情页批量优化、UI组件库图标扩展、社交媒体配图。其同步调用能力显著降低前端等待延迟，`n` 参数支持一次请求多图，适合批处理。
- **慎用**：对时序一致性无要求的场景（如需连贯动画帧）；对物理精度、空间结构无要求的场景（如3D建模需求）。

### ✅ 视频生成 —— 推荐用于「叙事表达、动态呈现、人机交互」的中等复杂度多媒体应用
- **适用**：短视频内容创作（营销、教育、娱乐）、数字人播报系统、电商产品动态展示、AI驱动的创意视频工坊。首尾帧/参考生视频能力支持精准动作控制，LipSync与Animate-Anyone满足专业级口型/舞蹈复刻。
- **慎用**：超长视频（>5秒）生成（当前主流模型时长上限为2–5秒）；对帧率稳定性、逐帧编辑有严苛要求的影视级制作；无稳定公网图片/视频URL源的内网环境（所有输入必须HTTPS公网可访问）。

### ✅ 3D生成 —— 推荐用于「空间建模、工业设计、AR/VR内容供给」的结构化三维资产构建
- **适用**：制造业快速原型验证（草图→3D）、电商3D商品库建设（单图→带PBR材质GLB）、游戏/元宇宙资产生成（四视图→标准模型）、建筑可视化初稿。`Tripo-H3.1` 的200万面能力接近专业建模精度，`P1.0` 的2万面适合实时渲染场景。
- **慎用**：需要实时交互式生成（异步24小时等待不满足实时性）；非北京地域部署的系统（无跨地域替代方案）；输入非标准（如少于4张图、视角顺序错乱、URL不可达）导致高频失败的场景。

## 开发者技术选型参考

| 选型考量 | 推荐方案 | 关键依据 |
|----------|----------|----------|
| **追求开发效率与低延迟** | ▶ 图像生成（同步模型） | `qwen-image-3.0-pro` 等支持同步返回，无需轮询逻辑；SDK封装成熟，错误码体系清晰；调试周期短。 |
| **需构建端到端AI视频工作流** | ▶ 视频生成（优先 `wan2.7` 系列） | `wan2.7` 统一支持T2V/I2V/R2V三大范式，API结构一致，降低多模型集成复杂度；文档完备，控制台开通便捷。 |
| **必须生成高保真3D资产且接受异步流程** | ▶ 3D生成（`Tripo/Tripo-H3.1`） | 当前百炼唯一3D方案，`ultra` 模式面数领先；输出GLB原生兼容WebGL/Unity/Unreal，免格式转换。 |
| **预算敏感且需免费试用** | ▶ 图像生成（体验模型） | `wanx-poster-generation-v1`、`wanx-x-painting` 等明确标注“免费体验”，额度用尽前零成本验证。 |
| **系统已部署于非北京地域** | ▶ 图像生成 或 视频生成 | 3D生成强制北京地域，若基础设施无法迁移，应规避该能力，改用图像/视频方案模拟3D效果（如多角度图生成）。 |
| **需严格控制输出规格（分辨率/长宽比/帧率）** | ▶ 图像生成 & 视频生成 | 二者均提供细粒度参数：`size`/`aspect_ratio`（图像）、`resolution`/`duration`/`video_fps`（视频）；3D生成仅能控制面数与贴图质量，无分辨率概念。 |
| **输入源受限（仅有一张图/一段文字）** | ▶ 图像生成（T2I/I2I） 或 3D生成（单图模式） | 视频生成普遍要求更丰富输入（如I2V需首帧，R2V需参考图），而图像/3D对单模态输入支持更友好。 |

> **重要提醒**：所有能力均依赖**同地域 API Key 与业务空间专属域名**。跨地域混用是最高频报错原因（`401 Unauthorized` 或 `BadRequest.InputDownloadFailed`）。建议在初始化阶段强制校验地域一致性，并在错误处理中优先排查此配置项。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


