# [多模态](../concepts/multimodal.md)生成能力对比：图像、视频与3D生成API

本文旨在为开发者提供百炼平台三大核心[多模态](../concepts/multimodal.md)生成能力（图像、视频、3D）的系统性对比分析，帮助技术团队基于业务需求、性能约束与工程成本，快速完成精准选型。随着AIGC应用场景从静态内容向动态表达与空间交互演进，理解各模态API在输入范式、输出形态、调用机制及部署约束上的差异，已成为构建高质量生成式应用的关键前提。

---

## 关键维度对比表

| 维度 | 图像生成 API | 视频生成 API | 3D生成 API |
|------|--------------|----------------|--------------|
| **核心能力** | 文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、背景生成、风格迁移、实例分割等全链路图像任务 | 文生视频（T2V）、图生视频（I2V）、首尾帧生成、参考生视频、视频编辑、数字人驱动（播报/唱演/口型/舞蹈）、风格重绘、超分 | 文生3D、单图生3D、多图（4视角）生3D；支持高精度几何重建与PBR材质渲染 |
| **输入格式** | • 文生图：`input.messages.content.text` 或 `input.prompt`<br>• 图生图/编辑：`content` 数组混合 `text` + `image` 对象（顺序敏感）<br>• 图像URL需公网可访问、无中文路径、格式为 PNG/JPG/WEBP | • 统一结构：`input.media` 数组（支持 `image_url`/`first_frame`/`last_frame`/`video_url` 等 type）+ `input.prompt`<br>• 数字人系列需前置调用 `*-detect` 模型校验输入合规性 | • 三者互斥：<br> – 文生3D：`input.prompt`（≤1024字符）<br> – 单图生3D：`input.image`（JPEG/PNG URL，20–6000px，≤20MB）<br> – 多图生3D：`input.images`（固定长度为4的数组，含空对象 `{}` 占位） |
| **输出格式** | • 同步调用：Base64 编码图像或直连 CDN URL<br>• 异步调用：`output.image_url`（有效期依模型而定，通常24h）<br>• 部分模型支持返回优化提示词（`prompt_extend`） | • 全异步：`output.video_url`（GLB/MP4格式，有效期24h）<br>• 数字人任务额外返回 `output.audio_url`、`output.animation_url` 等结构化产物 | • 全异步：`output.results` 包含<br> – `pbr_model_url`（GLB，含PBR材质，2h有效）<br> – `base_model_url`（无贴图基础网格，2h有效）<br> – `rendered_image_url`（WebP预览图，2h有效） |
| **支持模型（代表）** | • 通用：`qwen-image-3.0-pro`、`wan2.7-image-pro`、`z-image-turbo`、`vidu/vidu-image_reference2image`<br>• 垂直：`kling/kling-v3-*`（分镜）、`virtualmodel-v2`（虚拟模特）、`aitryon-plus`（AI试衣）<br>• 工具：`image-instance-segmentation`、`wanx-sketch-to-image-lite` | • 通用：`wan3.0-video`（邀测）、`wan2.7-t2v/i2v/r2v/videoedit`、`kling/kling-v3-*`<br>• 垂直：`liveportrait`（播报）、`emo`（唱演）、`animate-anyone`（舞蹈）<br>• 工具：`video-style-transform`、`pixverse-upscale` | • `Tripo/Tripo-H3.1`（高精度，最高200万面）<br>• `Tripo/Tripo-P1.0`（快速专业版，最高2万面） |
| **API端点（推荐）** | • 同步：`POST /api/v1/services/aigc/multimodal-generation/generation`<br>• 异步（按任务类型区分）：<br> – 图生图：`/api/v1/services/aigc/image2image/image-synthesis`<br> – 背景生成：`/api/v1/services/aigc/background-generation/generation` | • 统一端点（除旧版外）：<br>`POST /api/v1/services/aigc/video-generation/video-synthesis`<br>• 注意：`wan2.2-*` 系列仍使用 `/api/v1/services/aigc/image2video/video-synthesis` | • 统一端点：<br>`POST /api/v1/services/aigc/video-generation/3d-generation`<br>（命名沿用 `video-generation` 路径，属历史兼容设计） |
| **调用模式** | • **同步 & 异步并存**：<br> – 快速模型（如 `wan2.6-t2i`、`qwen-image-3.0-pro`）支持同步响应<br> – 耗时任务（虚拟模特、局部重绘）强制异步 | • **强制异步**：<br>所有模型均需两步调用（提交任务 → 轮询结果），`task_id` 有效期24小时 | • **强制异步**：<br>所有任务必须轮询 `task_id`，禁止同步调用；`task_id` 有效期24小时，结果URL有效期仅2小时 |
| **地域支持** | • 多地域：北京、新加坡、弗吉尼亚、法兰克福、东京（需Key/Endpoint/模型严格同地域）<br>• 部分模型限北京（如 `qwen-mt-image`、`wanx-poster-generation-v1`） | • 多地域：北京、新加坡（推荐专属域名）、弗吉尼亚、法兰克福（需用公共域名）<br>• 地域强绑定，跨域鉴权失败 | • **仅华北2（北京）地域**：<br>不支持其他地域调用，Key/Endpoint/模型必须为北京地域 |
| **计费方式** | • 按 [Token](../concepts/token.md)（文本）+ Image Unit（图像分辨率/张数）组合计费<br>• 免费额度模型（如 `image-erase-completion`）额度用尽后不可调用 | • 按 Video Unit 计费（与分辨率、时长、模型复杂度相关）<br>• 数字人系列按并发实例计费（如 `animate-anyone` 后付费模式=1并发/任务） | • 按 3D Unit 计费（与 `geometry_quality`/`texture_quality`/`pbr` 参数强相关）<br>• `Tripo-H3.1` + `ultra` + `pbr:true` 成本显著高于 `P1.0` + `standard` |
| **典型场景** | • 电商素材生成（商品图、模特图、海报）<br>• 社媒内容创作（配图、头像、表情包）<br>• 设计辅助（草图转高清、背景替换、风格迁移） | • 短视频营销（文/图→10s广告视频）<br>• 数字人应用（智能客服播报、虚拟主播、AI歌手）<br>• 影视预演（分镜生成、动作迁移、风格化剪辑） | • 游戏/AR/VR资产生产（角色、道具、场景建模）<br>• 工业设计验证（产品原型可视化）<br>• 电商3D展示（商品多角度交互模型） |

---

## 各方案适用场景建议

### ✅ 图像生成 API —— 适合「高频、轻量、多样化」视觉内容生产  
- **推荐场景**：  
  - 需要毫秒级响应的实时图像生成（如设计工具内嵌AI画布、聊天机器人配图）→ 选用 `z-image-turbo` 或 `wan2.6-t2i` 同步调用；  
  - 电商批量生成商品主图/场景图 → 使用 `virtualmodel-v2` + `aitryon-plus` 组合实现模特+试衣闭环；  
  - 创意营销活动（海报、节日Banner）→ `wanx-poster-generation-v1` 提供模板化生成能力；  
  - 图像质量要求高且需精细控制 → `qwen-image-3.0-pro` 支持双模态（T2I+I2I）与局部重绘。  
- **慎用场景**：  
  - 对输出一致性要求极高的系列化图像（如角色多姿态）→ 当前图像模型缺乏跨图ID锚定能力，建议转向视频/3D方案。

### ✅ 视频生成 API —— 适合「动态表达、人机交互、时间序列」内容构建  
- **推荐场景**：  
  - 企业级数字人应用（客服播报、培训讲师）→ `liveportrait` 或 `videoretalk`，需搭配 `*-detect` 校验确保输入合规；  
  - 快速制作短视频广告（图文→10s视频）→ `wan2.7-t2v` 或 `kling-v3-t2v`，平衡质量与生成速度；  
  - 专业影视工作流（分镜生成、镜头风格迁移）→ `kling/kling-v3-omni-image-generation`（分镜组图） + `video-style-transform`（统一艺术风格）；  
  - 用户UGC视频增强（老片修复、画质超分）→ `pixverse-upscale` + `happyhorse-1.0-video-edit`。  
- **慎用场景**：  
  - 需要精确控制每一帧运动轨迹 → 当前模型不支持关键帧编辑，建议结合后期合成工具；  
  - 超长视频（>30秒）生成 → 所有模型上限为30秒（`wan3.0-video`），需分段生成后拼接。

### ✅ 3D生成 API —— 适合「空间建模、物理仿真、沉浸体验」高价值资产创建  
- **推荐场景**：  
  - 游戏/元宇宙资产快速原型 → `Tripo-P1.0` 生成基础模型（2万面），用于快速迭代验证；  
  - 高精度工业/消费级产品建模 → `Tripo-H3.1` + `geometry_quality: "ultra"` + `pbr: true` 输出可直接导入Unity/Unreal的PBR GLB；  
  - 电商3D商品展示 → 单图生3D（用户上传实物照片）→ 自动生成可360°旋转的交互模型；  
  - AR应用内容生产 → 多图生3D（前/左/后/右视角）提升重建鲁棒性，适配移动端SLAM定位。  
- **慎用场景**：  
  - 实时3D渲染（如WebGL直播）→ 生成结果需下载后本地加载，不支持流式传输；  
  - 复杂拓扑结构（带内部腔体、镂空结构）→ Tripo对薄壁/穿透结构重建效果有限，建议人工修正。

---

## 技术选型参考指南（面向开发者）

| 选型维度 | 决策建议 |
|----------|----------|
| **响应时效性要求** | • <1s → 优先图像同步API（`wan2.6-t2i`, `qwen-image-3.0-pro`）<br>• 1–60s → 视频/3D异步API（需实现轮询+超时降级）<br>• 实时流式 → 当前三类API均不支持，需自建推理服务 |
| **输入数据形态** | • 纯文本 → 图像/视频/3D均可，按输出目标选择<br>• 单张图 → 图像编辑 or 视频首帧生成 or 3D单图重建（三者能力正交）<br>• 多视角图 → **唯一匹配3D多图生模**<br>• 视频文件 → **仅视频API支持**（`video-style-transform`, `pixverse-upscale`） |
| **输出产物用途** | • Web页面嵌入 → 图像URL/Base64、视频MP4、3D GLB（需前端Three.js/Babylon.js支持）<br>• 移动端App → 注意3D GLB体积（`H3.1-ultra`可达50MB+），建议启用CDN缓存与按需加载<br>• 渲染引擎集成 → 优先选择PBR材质输出（`pbr: true`），避免二次贴图烘焙 |
| **地域与运维约束** | • 多地域部署 → 图像/视频API更灵活；3D API必须集中在北京，需评估网络延迟与合规要求<br>• 域名稳定性 → **强烈推荐业务空间专属域名**（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），避免公共域名限流波动<br>• 错误排查 → 统一关注 `X-DashScope-

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


