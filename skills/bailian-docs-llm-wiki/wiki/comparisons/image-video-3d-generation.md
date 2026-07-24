# 图像、视频与3D生成能力对比

为帮助开发者快速理解百炼平台在多模态生成领域的技术边界与工程适配特性，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心能力模块。对比聚焦于实际落地中的关键技术维度——包括输入/输出规范、模型生态、调用机制、资源约束与成本模型等，旨在为新项目选型、架构设计及性能优化提供客观、可操作的技术决策依据。

---

## 关键能力维度对比

| 维度 | 图像生成（Image） | 视频生成（Video） | 3D生成（3D） |
|------|-------------------|-------------------|--------------|
| **输入格式** | 支持纯文本（T2I）、单图/多图（I2I）、掩码图（局部重绘）、参考图+指令（风格迁移）；`input` 结构灵活（`prompt` / `messages` / `base_image_url` + `mask_image_url` 等） | 多模态混合输入：文本（`prompt`）、首帧/尾帧图像（`first_frame`/`last_frame`）、参考图（`reference_image`）、音频（`audio_url`）、视频（`video_url`）；统一通过 `input.media` 数组声明 | 三选一互斥输入：<br>• 文本（`input.prompt`，≤1024字符）<br>• 单图（`input.image`，JPEG/PNG，20–6000px，≤20MB）<br>• 四视角图（`input.images`，长度固定为4，顺序：前/左/后/右，空位填 `{}`） |
| **输出格式** | 主流为 PNG（含透明通道），部分模型支持 JPG（如 `qwen-mt-image`）；输出为图片 URL 数组（同步）或单 URL（异步） | 输出为 MP4 视频 URL（含水印）；部分编辑类模型额外返回预览图（`rendered_image_url`）；URL 有效期 24 小时 | 输出为 GLB 格式 3D 模型：<br>• `pbr_model_url`（PBR 材质，含贴图）<br>• `base_model_url`（无贴图基础网格）<br>• `rendered_image_url`（渲染预览图）<br>所有 URL 有效期仅 **2 小时** |
| **支持模型（代表）** | `qwen-image-3.0-pro`（T2I+I2I）、`wan2.7-image-pro`、`kling/kling-v3-image-generation`、`virtualmodel-v2`、`WordArt锦书` 等 10+ 专用模型 | `wan2.7-t2v`/`i2v`/`r2v`（统一架构）、`happyhorse-1.1-*`、`kling/kling-v3-video-generation`、`pixverse/*`、`vidu/*`；人物动画类独立路径（如 `/image2video/video-synthesis`） | 仅 `Tripo/Tripo-H3.1`（高精度，≤200万面）与 `Tripo/Tripo-P1.0`（快速，≤2万面）两档模型 |
| **API 端点** | 同步为主：`/api/v1/services/aigc/image-generation/image-generation`<br>异步为辅：`/api/v1/services/aigc/image-generation/image-generation-async` | **强制异步**：<br>`/api/v1/services/aigc/video-generation/video-synthesis`（主路径）<br>`/api/v1/services/aigc/image2video/video-synthesis`（数字人等专用路径） | **强制异步**：<br>`/api/v1/services/aigc/video-generation/3d-generation`（注意：路径含 `video-generation`，但属 3D 服务） |
| **调用模式** | **混合模式**：<br>• `wan2.6-t2i`、`z-image-turbo`、`qwen-image-3.0-pro` 等支持**同步调用**（直返结果）<br>• `wanx-x-painting`、`image-out-painting` 等需**异步轮询** | **全量异步**：<br>必须携带 `X-DashScope-Async: enable`，否则报错；任务创建后需轮询 `GET /api/v1/tasks/{task_id}` | **全量异步**：<br>必须携带 `X-DashScope-Async: enable`；轮询间隔建议 ≥15 秒；`task_id` 有效期 24 小时 |
| **地域支持** | 华北2（北京）、新加坡、美国（弗吉尼亚）三地全域支持；各地区 API Key 与 Endpoint **不可混用** | 同图像生成：华北2、新加坡、美国（弗吉尼亚）；**地域强绑定**（模型/Key/Endpoint 必须同域） | **仅限华北2（北京）**；其他地域 Endpoint 不可用；API Key 必须为北京地域生成 |
| **计费方式** | • 多数模型：500 张/90 天免费额度（主账号+RAM 子账号共享）<br>• 额度用尽后按**张数计费**（例：`wanx2.1-imageedit` 0.14 元/张）<br>• 部分工具模型（如 `shoemodel-v1`）**仅限免费体验，不支持付费** | • 按**任务成功次数计费**（非帧数/秒数）<br>• 免费额度较少（通常 10–50 次/90 天），具体依模型而定<br>• 高清/长时长/多视角任务单价更高（如 `kling-v3-video-generation` > `wan2.7-t2v`） | • 按**任务成功次数计费**<br>• `Tripo-H3.1`（高精度）单价显著高于 `Tripo-P1.0`（快速）<br>• 无公开免费额度，需开通服务后查看资费页 |
| **典型场景** | • 电商海报/营销图批量生成<br>• UI 设计稿辅助出图<br>• 虚拟模特换装/鞋靴试穿<br>• 创意文字艺术渲染（WordArt）<br>• 图像擦除补全、背景生成 | • 短视频广告创意生成（T2V）<br>• 产品展示动画（I2V/KF2V）<br>• 口型同步数字人播报（LipSync）<br>• 动作迁移/风格重绘（R2V）<br>• 视频超分与运镜控制 | • 工业设计原型快速建模（文生3D）<br>• 电商商品 3D 展示（单图转3D）<br>• AR/VR 内容资产生成（多视角重建）<br>• 游戏资产初稿制作 |

---

## 适用场景建议（面向开发者）

### ✅ 优先选择图像生成当：
- 需要**毫秒级响应**（如实时设计助手、AIGC画布交互）→ 选用 `z-image-turbo` 或 `qwen-image-3.0-pro` 同步接口；
- 业务对**输出格式与分辨率灵活性要求高**（如定制海报 `2K`/`4K`、多宽高比 `16:9`/`1:1`）→ `kling` 或 `qwen-image-3.0-pro` 是首选；
- 需集成**轻量级专业工具**（如文字变形、局部擦除、虚拟模特）→ 直接调用对应工具模型，无需复杂 pipeline；
- 成本敏感且调用量大 → 充分利用 500 张免费额度，并优先选用 `wan2.6-t2i` 等性价比模型。

### ✅ 优先选择视频生成当：
- 核心需求是**动态内容表达**（广告、教学、社交传播）→ 视频是不可替代的载体；
- 已有高质量首帧/首尾帧图像 → `wan2.7-i2v` 或 `pixverse-c1-kf2v` 可高效生成连贯视频；
- 需要**人物驱动能力**（数字人播报、口型同步、表情迁移）→ 选用 `liveportrait`、`pixverse-lipsync` 或 `emo-v1`，注意其使用独立 Endpoint；
- 接受**异步工作流** → 构建任务队列 + Webhook 回调机制，避免阻塞主业务线。

### ✅ 优先选择3D生成当：
- 目标是**构建可交互三维资产**（WebGL/Unity/AR 应用）→ GLB 输出天然兼容主流引擎；
- 输入资源具备**结构化视角信息**（如工业零件四视图照片）→ 多图生3D重建精度远超单图；
- 对模型质量有分级需求 → `Tripo-P1.0` 用于快速原型验证，`Tripo-H3.1` 用于生产级交付；
- **仅在北京地域部署业务** → 否则需前置评估跨地域数据传输成本与合规风险。

---

## 技术选型决策提示

1. **不要忽略地域约束**：  
   图像/视频支持三地部署，但 3D **仅限北京**；若业务已全球化部署，3D 生成需额外规划 CDN 缓存或结果中转逻辑。

2. **异步是常态，同步是例外**：  
   视频与 3D 全量异步，图像虽支持同步，但复杂编辑任务（如局部重绘）仍需异步。建议统一采用「任务中心」架构，避免混合调用模式增加运维复杂度。

3. **URL 生效期差异巨大**：  
   图像 URL 通常长期有效（依赖 OSS 配置），视频 URL 有效期 24 小时，3D 模型 URL **仅 2 小时** —— 必须在轮询成功后立即下载并持久化存储。

4. **模型演进策略**：  
   - 图像：避开 `wanx-v1` 等标记为“推荐升级”的旧模型；  
   - 视频：优先选用 `wan2.7`/`HappyHorse 1.1`/`Kling` 新系列，旧版 `wan2.1–2.6` 功能受限且不再迭代；  
   - 3D：当前仅 Tripo 双模型，暂无替代方案，关注 `H3.1` 的 `ultra` 模式对硬件与存储的影响。

5. **错误处理差异化**：  
   - 图像常见错误：`BadRequest.InputDownloadFailed`（图片 URL 不可达）；  
   - 视频常见错误：`401 Unauthorized`（地域/Key 不匹配）或 `InvalidParameter`（`media` 数组格式错误）；  
   - 3D 常见错误：`InvalidParameter`（`images` 数组长度≠4）、`Forbidden`（非北京地域调用）。

> 选型不是功能罗列，而是权衡：**响应时效性、资源约束刚性、地域拓扑、以及长期维护成本**。建议新项目从最小可行模型起步（如 `z-image-turbo` → `wan2.7-t2v` → `Tripo-P1.0`），再按业务增长阶梯式升级。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


