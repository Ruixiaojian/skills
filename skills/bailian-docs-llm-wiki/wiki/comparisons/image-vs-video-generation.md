# 图像生成与视频生成对比

本文旨在帮助开发者清晰理解百炼平台中图像生成（Image Generation）与视频生成（Video Generation）两大视觉生成能力的核心差异，为技术选型、架构设计与成本规划提供客观、可落地的决策依据。随着AIGC应用从静态内容向动态表达演进，准确识别二者在协议设计、模型能力、工程约束及业务适配上的分野，已成为构建高质量[多模态](../concepts/multi-modal.md)应用的关键前提。

## 关键维度对比

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） |
|------|------------------------------|------------------------------|
| **输入格式** | 多样化：<br>• 文本提示（`input.messages` 或 `input.prompt`）<br>• 单图/多图 URL（`input.base_image_url`, `input.sketch_image_url` 等）<br>• 掩码图（`input.mask_image_url`）<br>• 涂鸦/草图（`input.sketch`）<br>• 结构化图文混排（如 `qwen-image-3.0-pro` 支持图文交错输入） | 严格结构化：<br>• 必须通过 `input.media` 数组声明媒体类型与URL<br>• 支持 `"image_url"`（首帧/参考图）、`"first_frame"`/`"last_frame"`（首尾帧）、`"video"`（原始视频）、`"audio"`（语音轨）、`"reference_image"`（风格参考）等类型<br>• 所有URL需公开可访问，且格式限于 JPEG/PNG/WebP（图片）或 MP4/MOV（视频） |
| **输出格式** | 单张或多张静态图像（PNG/JPEG），返回直接 `output.image_url`（同步）或 `output.images` 数组（异步）；URL 有效期通常为 24 小时 | 单个视频文件（MP4），返回 `output.video_url`；URL 有效期固定为 24 小时；不支持多版本并行输出（如不同分辨率同时生成） |
| **支持模型体系** | • **万相（WanX）系列**：`wan2.6-t2i`, `wan2.7-image-pro`, `wanx-x-painting` 等<br>• **千问（Qwen）系列**：`qwen-image-2.0-pro`, `qwen-image-3.0-pro`<br>• **垂直专用模型**：`kling/kling-v3-image-generation`, `vidu/vidu-image_reference2image`, `facechain-portrait-generation` 等<br>• 模型粒度细（含擦除、扩图、风格迁移等子功能） | • **通用视频模型**：`wan2.7-t2v`, `happyhorse-1.1-t2v`, `pixverse-c1-t2v` 等<br>• **人物驱动模型**：`emo-v1`, `liveportrait`, `videoretalk`, `animate-anyone-gen2`<br>• **增强专用模型**：`viduq3-turbo_text2video`, `pixverse-lipsync`, `pixverse-upscale`<br>• 模型按生成范式（T2V/I2V/R2V）和驱动方式（口型/动作/风格）强分类 |
| **API 端点** | • **同步调用**（主流）：<br>`POST /api/v1/services/aigc/multimodal-generation/generation`<br>• **异步调用**（部分旧/重载模型）：<br>`POST /api/v1/services/aigc/image-synthesis` 或 `/generation`（需 `X-DashScope-Async: enable`）<br>• Endpoint 域名统一为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com` | • **强制异步**：<br>`POST /api/v1/services/aigc/video-generation/video-synthesis`（新模型标准路径）<br>• 旧模型（如 `wan2.2-kf2v-fla`）使用 `/image2video/video-synthesis`（已逐步淘汰）<br>• Endpoint 域名同图像生成，但**路径与模型版本强绑定**，不可混用 |
| **调用模式** | **混合模式**：<br>• 多数新模型（`wan2.7-image-pro`, `qwen-image-3.0-pro`, `z-image-turbo`）支持**同步调用**（低延迟，适合交互场景）<br>• 部分编辑类模型（`wanx-x-painting`, `image-out-painting`）**仅支持异步**（需轮询） | **强制异步**：<br>所有视频模型均采用两阶段流程：<br>1. 创建任务 → 获取 `task_id`<br>2. 轮询 `GET /api/v1/tasks/{task_id}` 直至 `status === "SUCCESS"`<br>• 无同步接口，不支持实时响应 |
| **计费方式** | • 按**生成图片张数**计费（如 `wan2.6-t2i`：1 张 = 1 次调用）<br>• 免费额度：500 张/账号（主账号与 RAM 子账号共享）<br>• 部分模型（如 `wanx-x-painting`, `shoemodel-v1`）明确标注“免费体验期结束即停用，不支持付费” | • 按**视频时长（秒）** 计费（如 `wan2.7-t2v`：1 秒 = 1 计费单元）<br>• 免费额度按模型独立设置（如 `emo-v1`：1800 秒/月；`liveportrait`：并发数限制优先于额度）<br>• 无全局共享额度，各模型额度不互通 |
| **典型场景** | • 社媒配图、电商主图、海报设计、UI原型生成<br>• 图像局部编辑（擦除补全、背景替换、人像精修）<br>• 创意文字艺术、涂鸦转图、风格迁移<br>• 虚拟模特试穿、鞋靴3D展示、AI写真生成 | • 短视频广告、产品动态演示、数字人播报/唱演<br>• 图文转视频（PPT→视频、文章→解说视频）<br>• 口型同步（配音视频生成）、动作迁移（舞蹈/手势复现）<br>• 视频超分、风格重绘、首尾帧插值动画 |

## 适用场景建议

### ✅ 推荐选择图像生成当：
- 需要**毫秒级响应**的交互式应用（如设计工具中的实时预览、AI绘画App的即时出图）；
- 任务以**单帧质量、细节控制、文本渲染精度**为核心诉求（如UI还原、商品高清图、证件照生成）；
- 流程涉及**多步图像操作链**（如先扩图→再擦除→最后风格迁移），需灵活组合不同模型；
- 成本敏感且产出为静态资产（如批量生成1000张Banner图，总成本可控且可缓存）。

### ✅ 推荐选择视频生成当：
- 业务本质依赖**时间维度表达**（如营销短视频、教学动画、数字人直播）；
- 输入具备明确**时序结构**（如首尾帧定义运动轨迹、参考视频提供动作模板）；
- 需要**音画同步能力**（如语音驱动口型、音频节奏匹配画面变化）；
- 接受**10–60秒级处理延迟**，并已构建任务队列与状态管理机制（如后台批量视频合成系统）。

### ⚠️ 不建议混用或强行替代的情况：
- 用图像生成“逐帧生成再拼接”模拟视频 → **成本高、一致性差、无运动建模，且违反服务条款**；
- 用视频生成替代高质量单图输出 → **分辨率受限（多数模型上限为1080P）、细节丢失、成本倍增（1秒视频 ≈ 10–30张图成本）**；
- 在未校验输入合规性前提下调用人物驱动模型（如 `emo-v1`）→ **必须前置 `detect` 接口，否则必然失败**。

## 技术选型参考（面向开发者）

| 选型关注点 | 图像生成建议 | 视频生成建议 |
|------------|--------------|--------------|
| **集成复杂度** | 优先选用支持**同步调用**的新模型（如 `qwen-image-3.0-pro`），减少轮询逻辑；注意区分 `input.messages` 与 `input.prompt` 输入结构 | 必须实现**标准异步状态机**：创建任务 → 定时轮询（建议指数退避）→ 解析 `output.video_url` → 下载/转存；避免短间隔高频轮询触发限流 |
| **地域与认证** | 模型、Endpoint、API Key **三者同地域即可**；推荐使用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）提升稳定性 | 同图像生成，但**路径版本更敏感**：务必核对文档中模型对应的 API 路径（`/video-generation/` vs `/image2video/`），错误路径直接返回 404 |
| **错误防御** | 关注模型特有参数约束（如 `qwen-image-3.0-pro` 的像素范围、`kling` 的 `aspect_ratio` 格式）；异步模型需捕获 `X-DashScope-Async` 缺失错误 | 严格校验 `input.media` 类型与URL有效性；人物类模型必加 `detect` 预检；轮询时需处理 `task_status === "FAILED"` 并解析 `error_code`（常见如 `INVALID_MEDIA_URL`, `DETECT_FAILED`） |
| **性能与扩展** | 同步模型吞吐量高，适合高并发轻量请求；异步模型适合长耗时任务，但需自行维护任务生命周期 | 所有模型默认并发数为 1（尤其人物驱动类），如需提升吞吐，须申请配额扩容；视频存储与分发建议接入 OSS + CDN 加速 |
| **演进趋势** | 模型快速迭代（如 `wanx-v1` 已弃用，`wan2.7-image-pro` 成主力），建议通过 `model` 字段显式指定版本号，避免隐式降级 | 路径标准化加速（`/video-generation/` 全面替代 `/image2video/`），新模型均要求 `X-DashScope-Async: enable`；关注 `pixverse-upscale` 等后处理模型对成品质量的增强价值 |

> **最后提醒**：两类服务虽同属 AIGC 视觉生成范畴，但底层技术栈、资源调度策略与 SLA 保障机制完全不同。切勿基于“都是生成”做经验迁移——务必以官方最新模型文档为准，严格遵循输入/输出契约，方能保障生产环境稳定可用。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)


