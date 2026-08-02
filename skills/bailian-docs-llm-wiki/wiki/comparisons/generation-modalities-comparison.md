# 多模态生成能力对比：图像、视频与3D生成

为帮助开发者快速理解百炼平台在多模态生成领域的技术能力边界与工程适配要点，本文系统对比图像生成、视频生成与3D生成三大核心能力。对比聚焦于**实际落地所需的工程维度**——包括调用模式、地域约束、模型演进趋势、输入输出规范及计费逻辑等，避免泛泛而谈“能力强弱”，而是服务于真实场景下的技术选型决策。

---

## 关键维度对比表

| 维度 | 图像生成（Image） | 视频生成（Video） | 3D生成（3D） |
|------|-------------------|-------------------|--------------|
| **输入格式** | 支持文本（`prompt`/`messages`）、单图（`image_url`）、掩码图（`mask_image_url`）、草图（`sketch_image_url`）、多图参考（部分模型）；支持局部重绘、风格迁移等复合输入 | 文本（T2V）、单图/首帧（I2V）、首尾帧（Start-End2V）、多图参考（R2V）、原始视频+音频（口型同步/编辑）；所有输入均需公网可访问 HTTPS URL | 文本（T23D）、单图（`input.image`）、四视角图（`input.images`，前/左/后/右顺序）；三者互斥，不可混用 |
| **输出格式** | JPEG/PNG 图像（同步返回或异步 URL）；部分工具返回 JSON 结构化结果（如分割掩码、擦除补全坐标） | MP4 视频（H.264 编码，720P/1080P 可选）；附带预览图（`preview_url`）；数字人等场景可能返回多段视频或动作参数 | GLB 格式 PBR 材质模型（`pbr_model_url`）或无贴图基础网格（`base_model_url`）；同步返回渲染预览图（`rendered_image_url`） |
| **支持模型（代表性）** | `qwen-image-3.0-pro`（T2I+I2I）、`wan2.7-image-pro`（4K）、`kling/kling-v3-omni-image-generation`、`virtualmodel-v2`（电商模特）、`image-instance-segmentation`（工具类） | `vidu/viduq3-turbo_text2video`、`wan2.7-t2v-2026-06-12`（统一首帧/首尾帧/续写）、`pixverse/pixverse-c1-t2v`、`wan2.2-s2v`（数字人）、`pixverse/pixverse-lipsync`（口型） | `Tripo/Tripo-H3.1`（高精度，≤200万面）、`Tripo/Tripo-P1.0`（快速，≤2万面） |
| **API 端点（推荐）** | `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`（同步/异步共用） | `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（强制异步） | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`（仅北京，强制异步） |
| **调用模式** | **混合模式**：高频轻量模型（如 `wan2.6-t2i`、`z-image-turbo`）支持同步调用（<10s）；复杂编辑/长耗时模型（如 `kling`、`wanx-x-painting`）需异步轮询 | **强制异步**：全部模型均需创建任务 + 轮询（平均 1–5 分钟），无同步接口 | **强制异步**：全部模型均需创建任务 + 轮询（平均 2–10 分钟），`task_id` 有效期 24 小时，结果 URL 有效期 2 小时 |
| **地域支持** | 华北2（北京）、新加坡、美国（弗吉尼亚）——但**各模型支持不一致**（如 `qwen-image-3.0-pro` 不支持美东，`wan2.6-t2i` 支持美东） | 华北2（北京）、新加坡、美国（弗吉尼亚）——**严格要求模型、API Key、Endpoint 同地域**，跨地域鉴权失败 | **仅华北2（北京）**：Tripo 服务全域仅部署于北京地域，其他地域 Endpoint 不可用 |
| **计费方式** | 按**成功调用次数**计费（1次请求 = 1次计费），与生成图片张数（`n`）无关；免费额度按模型独立分配（如 `wanx-x-painting` 免费体验额度用尽即停） | 按**成功完成的任务数**计费（1个 `task_id` = 1次计费），与视频时长、分辨率、帧率无关；部分模型（如 `emo-v1`）有并发任务数硬限制（QPS/RPS） | 按**成功完成的任务数**计费（1个 `task_id` = 1次计费）；`Tripo-H3.1` 与 `Tripo-P1.0` 计费单价不同；无免费额度，需开通后按量付费 |
| **典型场景** | 电商主图生成、营销海报设计、AI试衣、人像写真、背景替换、UI图标生成、图像修复与扩展 | 短视频内容创作、数字人播报、产品演示动画、口型驱动短视频、影视分镜预演、舞蹈动作迁移 | 工业设计原型、游戏资产建模、AR/VR 内容开发、电商3D商品展示、建筑可视化初稿 |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「高频、低延迟、多样化编辑」需求  
- **推荐场景**：  
  - 实时交互类应用（如在线设计工具、AI绘画 App）→ 选用 `z-image-turbo` 或 `wan2.7-image-pro` 同步接口；  
  - 电商批量生成（千张商品图）→ 使用 `qwen-image-3.0-pro` 批量请求（`n=4`）+ 异步队列管理；  
  - 高精度人像处理（试衣/写真/风格重绘）→ 选用垂直模型（`aitryon-plus`、`FaceChain`），注意其异步特性与掩码精度要求。  
- **避坑提示**：避免跨地域混用 Key 与模型；`prompt` 格式需严格匹配模型要求（`messages` vs `prompt` 字段）；水印参数默认开启，生产环境务必设 `"watermark": false`。

### ✅ 视频生成 —— 适合「叙事性、时序性、多模态融合」需求  
- **推荐场景**：  
  - 品牌短视频自动化生产 → `vidu/viduq3-turbo_text2video`（快+稳）或 `wan2.7-t2v`（支持分镜描述）；  
  - 数字人播报系统 → `wan2.2-s2v`（头像驱动）+ `pixverse/pixverse-lipsync`（音频驱动）组合调用；  
  - 影视/广告后期增强 → `pixverse/pixverse-upscale`（超分）+ `video-style-transform`（油画/赛博朋克风格）。  
- **避坑提示**：必须使用业务空间专属域名发起和轮询；首尾帧输入需严格按 `{type: "first_frame"}` / `{type: "last_frame"}` 标注；音频输入须人声清晰、无背景噪音，否则口型同步失败率高。

### ✅ 3D生成 —— 适合「结构化、可交互、物理真实」需求  
- **推荐场景**：  
  - 快速构建 3D 商品库（如家具、饰品）→ `Tripo/Tripo-P1.0`（2万面，秒级生成，成本低）；  
  - 工业零件/概念设计验证 → `Tripo/Tripo-H3.1`（200万面，支持 `geometry_quality: ultra`，需预留更长轮询间隔）；  
  - AR 应用素材管线 → 使用 `pbr: true` + `texture: true` 输出标准 GLB，直接接入 Unity/Unreal。  
- **避坑提示**：仅限北京地域，勿尝试新加坡/美东 Endpoint；多图输入必须为长度 4 的数组，空视角填 `{}`；单图分辨率需 ≥20px 且 ≤6000px，否则直接报错 `InvalidParameter`。

---

## 面向开发者的选型参考指南

| 选型考量项 | 推荐策略 |
|------------|----------|
| **响应时效敏感型（<3s）** | 仅图像生成中部分模型（`z-image-turbo`, `wan2.6-t2i`）满足；视频与3D均为异步，不适用实时交互。优先评估是否可接受前端轮询+Loading状态。 |
| **跨地域部署需求** | 图像生成最灵活（三地域支持）；视频生成需按地域分别配置 Key 与 Endpoint；3D生成无选择余地，必须集中在北京。若业务已全球化，建议将3D任务调度至北京专属集群。 |
| **输入数据可控性** | 图像/视频对输入质量鲁棒性较强（模糊图仍可生成）；3D生成对单图角度、光照、遮挡极度敏感——**强烈建议优先采用多图输入（4视角）**，显著提升网格完整性与拓扑合理性。 |
| **成本优化路径** | 图像：复用免费额度模型（如 `wanx-poster-generation-v1`）做初稿；视频：选用 `turbo` 后缀模型（如 `viduq3-turbo`）降低单任务成本；3D：`Tripo-P1.0` 单任务成本约为 `H3.1` 的 1/5，精度足够时优先选用。 |
| **工程集成复杂度** | 图像：同步调用最简（HTTP POST → JSON Response）；视频/3D：必须实现任务生命周期管理（创建→轮询→超时处理→结果下载），建议封装为 SDK 中的 `wait_for_completion()` 工具方法。 |
| **未来演进确定性** | 图像：千问与万相双线并进，新模型（如 `qwen-image-3.0-pro`）已统一 `messages` 输入范式；视频：万相2.7为当前主力，旧版（2.2/2.6）已停止更新；3D：Tripo 为独家合作模型，版本迭代由 Tripo 官方主导，百炼侧保持 API 兼容性承诺。 |

> **最后提醒**：所有能力均需在[百炼控制台模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)确认当前地域下可用模型及最新文档链接。API 行为以控制台实时信息为准，文档可能存在滞后。建议将模型可用性检查纳入 CI/CD 流程，避免上线后因地域模型缺失导致服务降级。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


