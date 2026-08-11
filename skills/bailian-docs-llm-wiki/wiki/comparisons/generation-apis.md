# [多模态](../concepts/multi-modal.md)生成能力对比：Image Generation vs 3D Generation vs Video Generation API

本页旨在为开发者提供百炼平台三大核心[多模态](../concepts/multi-modal.md)生成能力（图像、3D、视频）的系统性技术对比，帮助在实际业务场景中快速识别能力边界、选型依据与集成要点。随着AIGC应用从静态内容向空间化、时序化演进，理解三类API在输入约束、输出形态、调用范式及工程适配性上的差异，是构建高质量生成式应用的关键前提。

---

## 关键维度对比

| 维度 | Image Generation | 3D Generation | Video Generation |
|------|------------------|----------------|-------------------|
| **核心能力定位** | 静态二维视觉内容生成与编辑（文生图、图生图、局部重绘、风格迁移等） | 三维几何模型生成（文/图/多图→带材质或无贴图GLB模型） | 时序动态内容生成（文/图/视频/音频→2–30秒短视频，含数字人、编辑、风格化等） |
| **输入格式** | • 文本提示（`prompt`）<br>• 图像URL（PNG/JPEG/WEBP/BMP/AVIF，公网可访问）<br>• 局部掩码（部分编辑模型）<br>• 多图（如海报生成、AI试衣） | • **三者互斥**：<br> - 文本（`input.prompt`）<br> - 单图URL（`input.image`，JPEG/PNG）<br> - 四视角图数组（`input.images`，长度固定为4，缺失填`{}`） | • 模态组合灵活：<br> - 纯文本（T2V）<br> - 图像+文本（I2V）<br> - 多图/视频+音频+文本（R2V、数字人）<br> - 视频+指令（编辑类）<br>• 所有媒体URL需公网可访问、≤20MB |
| **输出格式** | • PNG/JPEG/WEBP 格式图像文件（同步返回或异步下载）<br>• 支持多张输出（`n=1~9`，依模型而定）<br>• 可选水印、分辨率/宽高比控制 | • GLB 格式3D模型（默认含PBR材质，`pbr_model_url`）<br>• 可选无贴图基础模型（`base_model_url`，需 `pbr=false & texture=false`）<br>• 同步返回预览渲染图（`rendered_image_url`） | • MP4 格式视频文件（`output.video_url`）<br>• 部分模型支持音频轨道（`parameters.audio=true`）<br>• 数字人任务额外返回口型/动作参数（如`output.lip_sync_result`） |
| **支持模型（代表性）** | • 通用：`qwen-image-3.0-pro`、`wan2.6-t2i`、`kling/kling-v3-image-generation`<br>• 编辑：`qwen-image-edit`、`wan2.7-image-pro`、`wanx-x-painting`<br>• 工具：`virtualmodel-v2`、`aitryon-plus`、`image-erase-completion` | • `Tripo/Tripo-P1.0`（专业版，≤2万面，低延迟）<br>• `Tripo/Tripo-H3.1`（高精度版，≤200万面，支持`ultra`几何质量） | • 文生视频：`wan2.7-video`、`kling/kling-v3-video-generation`、`pixverse/pixverse-c1-t2v`<br>• 图生视频：`pixverse/pixverse-c1-it2v`、`vidu/viduq3-pro-fast_img2video`<br>• 数字人：`emo-v1`、`liveportrait`、`animate-anyone-gen2`<br>• 编辑：`wan2.7-videoedit`、`video-style-transform`、`pixverse/pixverse-upscale` |
| **API 端点（典型）** | • 同步：`POST /api/v1/services/aigc/multimodal-generation/generation`（北京/新加坡）<br>• 异步：按功能路径区分，如 `/background-generation/generation`、`/image2image/image-synthesis` | • 异步专用：`POST /api/v1/services/aigc/video-generation/3d-generation`（**仅华北2/北京地域**） | • 统一入口（新模型）：`POST /api/v1/services/aigc/video-generation/video-synthesis`（多地域支持）<br>• 旧模型路径独立：`/api/v1/services/aigc/image2video/video-synthesis`（不兼容） |
| **调用模式** | • **混合模式**：<br> - 低延迟模型（如`wan2.6-t2i`）支持同步调用<br> - 高复杂度任务（局部重绘、虚拟模特）强制异步 | • **强制异步**：<br> - 必须设置 `X-DashScope-Async: enable`<br> - 无同步接口，创建任务后轮询 `GET /api/v1/tasks/{task_id}` | • **强制异步**：<br> - 全量任务均需两阶段流程<br> - 必须设置 `X-DashScope-Async: enable`<br> - 轮询间隔建议 ≥15 秒 |
| **地域约束** | • 支持多地域（北京、新加坡、弗吉尼亚）<br>• **API Key、Endpoint、Workspace ID 必须同地域**<br>• 推荐使用业务空间专属域名 | • **严格单地域**：仅支持华北2（北京）<br>• API Key、Endpoint、模型开通必须绑定北京地域<br>• 其他地域调用必然失败 | • 支持多地域（北京、新加坡、弗吉尼亚）<br>• **地域强绑定**：Key/Endpoint/模型实例不可跨域复用<br>• 新模型统一路径，旧模型路径隔离 |
| **计费方式** | • 免费额度：500 张/90天（主账号与RAM子账号共享）<br>• 超额按模型单价计费（如 `wanx-v1`: 0.16元/张，`image-out-painting`: 0.18元/张）<br>• **仅对成功生成的图片计费** | • 按任务计费（非按面数/分辨率）<br>• `Tripo-P1.0` 与 `Tripo-H3.1` 单价不同（H3.1更高）<br>• 免费额度未公开，需在控制台查看已开通服务的配额 | • 按模型+时长/分辨率阶梯计费<br> - 例如：`wan2.7-video`（5秒/720P）0.8元/次，`kling-v3-video-generation`（10秒/4K）3.2元/次<br>• 数字人任务按“检测+生成”双阶段计费（如 `emo-detect-v1` + `emo-v1`）<br>• 免费额度因模型而异，需查控制台 |
| **典型场景** | • 电商商品图生成与背景替换<br>• 社媒营销海报与创意文案配图<br>• 设计师辅助：局部修改、风格迁移、AI试衣<br>• 内容平台：头像生成、插画创作、文字转锦书 | • 游戏/AR/VR资产快速建模（概念验证、原型开发）<br>• 电商3D商品展示（单图生成可交互模型）<br>• 工业设计草图转三维结构（多视角输入）<br>• 教育/科普可视化（抽象概念具象化） | • 短视频平台：爆款脚本自动成片<br>• 企业宣传：图文稿→数字人播报视频<br>• 影视制作：分镜→动态预演、风格化重绘<br>• 教育培训：课件动画、虚拟讲师生成<br>• 直播电商：口型同步+形象驱动 |

---

## 适用场景建议

### ✅ 选择 Image Generation 当：
- 需要**快速产出高质量静态图**，且对实时性有要求（如运营素材秒级生成）；
- 任务聚焦于**语义编辑**（擦除对象、重绘局部、换背景、改风格）；
- 输入为**单一文本或单张图像**，无需空间或时间维度扩展；
- 成本敏感，需利用免费额度高频调用（如每日数百张海报生成）；
- 集成到Web端轻量应用，依赖同步响应简化前端逻辑。

### ✅ 选择 3D Generation 当：
- 目标产物是**可导入Unity/Unreal/Three.js的GLB模型**，用于交互式体验；
- 输入具备**明确空间线索**（单视角图可接受粗略建模，四视角图可提升拓扑准确性）；
- 对模型**面数与材质精度有分级需求**（P1.0满足快速原型，H3.1支撑生产级资产）；
- 业务部署在**华北2（北京）地域**，且能接受异步工作流（建模耗时通常1–5分钟）；
- 不需要动画、物理模拟或时序行为，纯静态三维表达即满足需求。

### ✅ 选择 Video Generation 当：
- 核心诉求是**动态叙事或行为表达**（人物说话、物体运动、镜头切换）；
- 输入模态**天然复合**（如“用这张产品图+这段配音生成带口型的导购视频”）；
- 需要**跨模态一致性控制**（参考图保角色、参考视频保运镜、参考音频保节奏）；
- 接受**分钟级等待**（典型生成耗时2–8分钟），并已设计轮询/回调机制；
- 场景涉及**专业视频处理能力**（超分、动作迁移、风格滤镜、数字人驱动）。

---

## 技术选型参考（面向开发者）

| 选型考量 | 推荐方案 | 关键依据 |
|----------|-----------|-----------|
| **首次集成，追求最小成本验证** | Image Generation（`qwen-image-3.0-pro`） | 同步调用简单、免费额度充足、文档成熟、SDK支持完善；适合快速验证AIGC可行性 |
| **需交付可交互3D资产，且已有北京云环境** | 3D Generation（`Tripo/Tripo-H3.1`） | 唯一原生支持高精度GLB输出的API；多视角输入显著提升重建鲁棒性；PBR材质开箱即用 |
| **构建短视频SaaS工具，支持用户上传图文生成视频** | Video Generation（`wan2.7-video` + `pixverse/pixverse-c1-it2v`） | `wan2.7`中文提示词理解强，`pixverse`首帧生成稳定性高；统一API路径降低维护复杂度 |
| **企业内训系统，需将PPT转为数字人讲解视频** | Video Generation（`liveportrait` + `emo-v1`） | `liveportrait`轻量高效（1秒内完成检测），`emo-v1`支持唱歌/说话双模式；需注意前置检测必调用 |
| **跨地域多活架构，避免单点依赖** | Image Generation 或 Video Generation | 二者均支持北京/新加坡/弗吉尼亚多地域部署；3D Generation 因强制北京地域，不适合作为多活核心能力 |
| **预算有限，需最大化免费资源** | Image Generation（优先用尽500张）→ Video Generation（选低价模型如 `wan2.7-video`）→ 3D Generation（按需付费） | 图像免费额度最高且通用性强；视频模型存在低价入门选项；3D暂无公开免费额度，成本最刚性 |

> **重要提醒**：  
> - 所有API均**强依赖地域对齐**，务必在控制台开通对应地域服务，并使用该地域专属 Workspace ID 和 API Key；  
> - 异步任务的 `task_id` 有效期统一为 **24 小时**，结果 URL（如 `video_url`、`pbr_model_url`）有效期仅 **2 小时**，务必及时下载并持久化存储；  
> - 参数命名与结构**不可跨模型复用**（如 `size` 在图像/视频/3D中含义完全不同），务必查阅各模型最新API参考文档；  
> - 生产环境请**禁用旧域名 `dashscope.aliyuncs.com`**，统一使用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），保障SLA与性能。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)


