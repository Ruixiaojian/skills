# [多模态](../concepts/multi-modal.md)生成能力对比：图像生成、3D生成、视频生成

本文旨在为开发者提供百炼平台三大核心[多模态](../concepts/multi-modal.md)生成能力（图像生成、3D生成、视频生成）的系统性技术对比，帮助在实际业务场景中快速识别能力边界、选型依据与集成要点。随着AIGC应用从二维内容向三维空间与动态叙事演进，理解各模态在输入灵活性、输出质量、调用范式、资源消耗及计费逻辑上的差异，是构建稳定、高效、可扩展AI工作流的关键前提。

---

## 关键维度对比表

| 维度 | 图像生成（Image Generation） | 3D生成（3D Generation） | 视频生成（Video Generation） |
|------|------------------------------|--------------------------|------------------------------|
| **输入格式** | • 文本提示词（`prompt` 或 `messages`）<br>• 输入图像URL（支持T2I/I2I/局部重绘等）<br>• [多模态](../concepts/multi-modal.md)混合输入（如text+image，千问/万相2.6+支持）<br>• 风格参考图、草图、分割掩码等专用输入 | • **三者互斥**：<br>  – 文本（`input.prompt`）<br>  – 单图（`input.image` URL）<br>  – 四视图数组（`input.images`，按[前,左,后,右]顺序）<br>• 所有图像URL需公网可访问、无中文路径、≤20 MB | • 文本（`prompt`）<br>• 图像URL（首帧/尾帧/参考图）<br>• 视频URL + 音频URL（口型同步/编辑）<br>• 多模态组合（如`media`数组含`image_url`/`video_url`/`audio_url`）<br>• 部分模型需前置`detect`校验（数字人类） |
| **输出格式** | • Base64编码图片（同步调用）<br>• 公网可访问URL（异步调用，有效期24小时）<br>• 支持多种分辨率（512×512 至 4K）、宽高比（如`16:9`）<br>• 可选水印、智能提示扩展 | • GLB格式PBR材质模型（`pbr_model_url`，含贴图与光照信息）<br>• 无贴图基础网格（`base_model_url`，需显式设`texture=false & pbr=false`）<br>• 渲染预览图（`rendered_image_url`，PNG/JPEG，有效期2小时）<br>• 面数可控（`Tripo-H3.1`: ≤200万面；`Tripo-P1.0`: ≤2万面） | • MP4视频URL（`output.video_url`，有效期24小时）<br>• 分辨率支持`720P`/`1024×576`/`1280×720`等<br>• 时长可控（通常3–5秒，部分模型支持更长）<br>• 可选水印、风格强度、宽高比（如Kling支持`16:9`） |
| **支持模型（代表性）** | • 通用：`qwen-image-3.0-pro`、`wan2.7-image-pro`、`z-image-turbo`、`kling/kling-v3-omni-image-generation`<br>• 工具：`wanx-x-painting`（局部重绘）、`wanx-background-generation-v2`（背景生成）、`shoemodel-v1`（鞋靴模特）<br>• 增强：`aitryon-plus`（AI试衣）、`FaceChain`（写真） | • `Tripo/Tripo-H3.1`（高精度，200万面）<br>• `Tripo/Tripo-P1.0`（快速，2万面）<br>• *注：当前仅Tripo系列，暂无其他厂商3D模型接入* | • 文生视频：`vidu/viduq3-turbo_text2video`、`kling/kling-v3-video-generation`、`wan2.7-t2v-2026-06-12`<br>• 图生视频：`wan2.7-i2v`、`vidu/viduq3-pro-fast_img2video`、`pixverse/pixverse-c1-it2v`<br>• 参考生视频：`wan2.7-r2v-2026-06-12`、`pixverse/pixverse-c1-r2v`<br>• 编辑类：`videoretalk`（口型）、`pixverse/pixverse-upscale`（超分）、`video-style-transform`（风格） |
| **API端点（典型）** | • 同步：`POST /api/v1/services/aigc/image-generation/image-synthesis`<br>• 异步：`POST /api/v1/services/aigc/image-generation/image-synthesis?async=true`<br>• 专属域名推荐：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` | • 异步专用：`POST /api/v1/services/aigc/video-generation/3d-generation`<br>• **强制北京地域**：仅支持`cn-beijing`专属域名<br>• 必须携带`X-DashScope-Async: enable` | • 主流新版：`POST /api/v1/services/aigc/video-generation/video-synthesis`<br>• 旧版兼容：`/api/v1/services/aigc/image2video/video-synthesis`（如wan2.2系列）<br>• 专属域名推荐：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` |
| **调用模式** | • **混合模式**：<br>  – 新模型（`qwen-image-3.0-pro`, `wan2.7-image-pro`等）支持**同步返回**（HTTP 200 + base64/URL）<br>  – 工具模型（`wanx-sketch-to-image-lite`, `image-erase-completion`等）强制**异步轮询** | • **强制异步**：<br>  – 创建任务 → 获取`task_id` → 轮询`GET /api/v1/tasks/{task_id}`<br>  – `task_id`有效期24小时，结果URL有效期2小时 | • **强制异步**：<br>  – 创建任务 → 获取`task_id` → 轮询`GET /api/v1/tasks/{task_id}`<br>  – `task_id`有效期24小时，视频URL有效期24小时 |
| **计费方式** | • 按**成功生成图片张数**计费（失败不扣费）<br>• 免费额度：多数模型提供500张/90天<br>• 单价示例：`wanx-v1` 0.16元/张，`image-out-painting` 0.18元/张<br>• 不同模型单价独立 | • 按**成功生成任务次数**计费<br>• 当前未公开单价，以控制台实际报价为准<br>• 免费额度未明确说明，建议开通后查看配额<br>• `Tripo-H3.1`因计算资源更高，预期单价高于`P1.0` | • 按**成功生成视频次数**或**时长/帧数**计费（依模型而异）<br>• 各模型独立计费（如Vidu、Kling、PixVerse单价不同）<br>• 免费额度未统一，部分模型（如早期wan2.2）已停供免费额度<br>• 数字人模型（EMO/LivePortrait）常按“分钟”或“次”计费 |
| **典型应用场景** | • 电商：AI试衣、虚拟模特、海报生成、商品图扩图<br>• 设计：创意构图、风格迁移、草图转高清、背景生成<br>• 内容：头像生成、插画创作、图文配图、局部编辑 | • 工业设计：产品原型快速建模（文生3D）<br>• 游戏开发：角色/道具资产生成（单图→3D）<br>• AR/VR：多视角实物扫描重建（四视图→3D）<br>• 教育：教学模型可视化（如分子结构、机械部件） | • 营销：短视频批量生成（文生视频）、广告片首尾帧合成<br>• 影视：分镜预演、风格化视频重绘、口型驱动数字人播报<br>• 社交：表情包生成（Emoji）、舞蹈复刻（AnimateAnyone）<br>• 教育：课件动画、实验过程可视化 |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 推荐用于「静态内容规模化生产」
- **首选场景**：需要高频、低延迟、多样化2D视觉输出的业务，如电商平台主图生成、营销海报批量制作、UI设计素材辅助、社交媒体配图。
- **优势匹配**：同步调用支持毫秒级响应；分辨率/风格/数量灵活可控；工具模型覆盖大量垂直需求（擦除、分割、试衣）；免费额度充足，试错成本低。
- **慎用场景**：对3D空间结构、物理运动、时间连续性有要求的任务（如动画、仿真、交互式3D展示）。

### ✅ 3D生成 —— 推荐用于「轻量级三维资产快速构建」
- **首选场景**：需将概念、草图或实物快速转化为可用3D模型的环节，如工业设计初稿验证、游戏美术资产预研、AR商品预览建模、教育可视化教具生成。
- **优势匹配**：Tripo模型在单图/四视图输入下生成质量稳定；GLB格式开箱即用，兼容WebGL/Unity/Unreal；`P1.0`模型兼顾速度与精度，适合原型迭代。
- **慎用场景**：高精度工程级建模（如CAD级公差）、复杂拓扑结构（如有机生物精细解剖）、实时渲染级PBR材质（需后处理优化）。

### ✅ 视频生成 —— 推荐用于「动态内容自动化创作」
- **首选场景**：需生成短时长、高表现力、语义连贯的视频内容，如企业宣传短视频、电商商品演示、数字人客服播报、社交平台创意视频。
- **优势匹配**：多模态输入（文本+图+音）支持复杂指令；首尾帧/参考视频机制保障动作一致性；口型同步、风格重绘等编辑能力完善；`wan2.7`/`Vidu`等新模型支持智能分镜。
- **慎用场景**：长视频生成（>10秒）、电影级运镜与光影控制、多角色复杂交互、实时视频流处理（非批处理任务）。

---

## 开发者技术选型参考指南

| 选型维度 | 关键判断依据 | 推荐行动 |
|----------|--------------|----------|
| **输入数据形态** | • 若仅有文本描述 → 优先评估图像/视频生成的T2I/T2V能力<br>• 若已有高质量单图 → 图像编辑 or 3D生成 or 图生视频均可候选<br>• 若有首尾帧/多视角图 → 直接锁定3D生成<br>• 若含音频/视频片段 → 必选视频生成（R2V/口型同步） | 使用最小可行输入验证各模型效果。例如：用同一张产品图分别调用`wan2.7-i2v`（视频）、`Tripo-P1.0`（3D）、`qwen-image-3.0-pro`（高清图），横向对比输出质量与耗时。 |
| **输出交付要求** | • 需嵌入网页/APP静态展示 → 图像生成（URL直链）<br>• 需WebGL/Unity加载 → 3D生成（GLB）<br>• 需自动播放/分享传播 → 视频生成（MP4）<br>• 需长期存储/二次编辑 → 优先选择支持下载原始文件的模型（如图像/3D提供URL，视频需及时下载） | 注意URL有效期差异：图像URL（24h）、3D渲染图（2h）、3D模型URL（2h）、视频URL（24h）。关键业务务必实现自动下载与CDN缓存。 |
| **性能与延迟敏感度** | • 实时交互场景（如设计工具[插件](../concepts/plugin.md)）→ 选用支持同步调用的图像模型（`qwen-image-3.0-pro`）<br>• 批处理后台任务（如每日千条视频生成）→ 视频/3D异步模式需设计任务队列与状态监控<br>• 高并发请求 → 确认RPS限制（3D轮询限20 RPS；视频创建无明确QPS限制但受地域配额约束） | 在生产环境部署前，务必压测峰值QPS，并配置熔断降级策略。异步任务建议使用消息队列（如RocketMQ）解耦轮询逻辑。 |
| **地域与基础设施** | • 所有服务均严格绑定地域，且API Key不可跨域

## 被对比主题页

- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)


