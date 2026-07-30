# 多模态生成 API 对比：图像、3D、视频生成

为帮助开发者快速理解百炼平台在多模态生成领域的能力边界与技术选型路径，本文系统对比图像生成、3D生成、视频生成三类核心 API 的关键特性。随着 AIGC 应用从静态内容向动态、空间化、沉浸式演进，准确识别各模态的技术成熟度、调用范式、资源约束与适用场景，已成为构建高质量生成服务的基础前提。本对比聚焦实际工程落地维度，覆盖输入/输出规范、模型生态、协议设计、计费逻辑与典型业务适配性，旨在提供可操作的技术决策依据。

## 关键维度对比表

| 维度 | 图像生成（`/image-generation`） | 3D生成（`/3d-generation`） | 视频生成（`/video-generation`） |
|------|-------------------------------|---------------------------|------------------------------|
| **核心能力** | 文生图、图生图、局部重绘、背景生成、扩图、擦除补全、风格迁移、超分、AI试衣、虚拟模特等全链路视觉创作 | 文生3D、单图生3D、四视角多图生3D（前/左/后/右） | 文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑（指令/动作/角色/口型/风格）、数字人驱动 |
| **支持模型体系** | • 万相（WanX）系列（`wan2.6-t2i`, `wanx-x-painting`, `wanx-virtualmodel` 等）<br>• 千问（Qwen）系列（`qwen-image-3.0-pro`, `qwen-image-edit`）<br>• 垂直场景模型（Vidu, Kling, FaceChain, WordArt 等） | • Tripo-P1.0（专业版，≤2万面，速度快）<br>• Tripo-H3.1（高精度版，≤200万面，支持 `ultra` 几何质量） | • HappyHorse（T2V/I2V/R2V 全栈）<br>• 万相 2.7（主力新版，统一路径 `/video-synthesis`）<br>• PixVerse（动作控制、口型同步、超分）<br>• Vidu/Kling（高性能文生视频）<br>• LivePortrait/Emo（数字人驱动） |
| **输入格式** | • 文生图：`input.messages[].content[]` 中含 `{"text": "prompt"}`<br>• 图生图/编辑：混合 `{"text": "指令"}` 与 `{"image": "url"}`（最多14张）<br>• 局部重绘：需 `base_image_url` + `mask_image_url` | • 三者互斥：<br> – 文生3D：`input.prompt`（≤1024字符）<br> – 单图生3D：`input.image`（JPEG/PNG，20–6000px，≤20MB）<br> – 多图生3D：`input.images`（长度严格为4的数组，空视角用 `{}` 占位） | • T2V：`input.prompt`<br>• I2V/R2V：`input.media` 数组（含 `image_url`）<br>• 视频编辑/口型同步：`input.media` 含 `video_url` + `audio_url`<br>• 所有输入 URL 需公网可访问、HTTP(S)、无中文路径 |
| **输出格式** | • PNG/JPEG 图像（URL 下载）<br>• 支持水印控制（`watermark: false`）<br>• 部分模型返回多张（`n=1–9`） | • GLB 文件（含 PBR 材质或基础网格）<br>• 附带预览图 `rendered_image_url`<br>• 可选 `pbr_model_url` / `base_model_url`（需显式设置 `pbr: false` & `texture: false`） | • MP4 视频（URL 下载）<br>• 支持分辨率（`720P`, `1280*720`）、时长（`duration: 3/5/8s`）、宽高比（`16:9`）控制<br>• 默认带水印（`watermark: true`） |
| **调用方式** | • **同步为主**：`wan2.6-t2i`, `qwen-image-2.0-pro` 等支持直接返回结果<br>• **异步为辅**：`wanx-x-painting`, `wanx-virtualmodel` 等需轮询 `task_id` | • **强制异步**：所有任务均需 `POST` 创建 + `GET` 轮询<br>• `X-DashScope-Async: enable` 为硬性 Header | • **强制异步**：全部接口仅支持异步<br>• `X-DashScope-Async: enable` 必须设置<br>• 平均耗时 1–5 分钟（部分数字人任务达 5–10 分钟） |
| **API 端点（北京地域示例）** | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation` | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` |
| **地域支持** | • 北京、新加坡、美国（弗吉尼亚）、德国（法兰克福）<br>• 各地域独立 API Key 与域名，**不可混用** | • **仅华北2（北京）**<br>• Tripo 服务需在控制台单独开通，API Key 必须在北京地域生成 | • 北京、新加坡、美国（弗吉尼亚）<br>• **部分模型强绑定北京**（如 `liveportrait`, `emo`, `videoretalk`）<br>• 模型、Key、Endpoint 必须同地域 |
| **计费方式** | • 按**成功生成的图片张数**计费（失败/超时/下载失败不扣额）<br>• 免费额度按自然月发放（90天有效期）<br>• 不同模型单价差异显著（如 `qwen-image-3.0-pro` > `wan2.5-i2i-preview`） | • 按**成功生成的 3D 模型任务数**计费<br>• Tripo-P1.0 与 H3.1 单价不同（H3.1 更高）<br>• 免费额度有限，且不支持续订 | • 按**成功生成的视频任务数**计费<br>• 不同模型、不同参数（如 `duration`, `resolution`）影响单价<br>• 数字人/口型同步类模型通常单价更高 |
| **典型场景** | • 电商商品图生成（虚拟模特、鞋靴模特）<br>• 营销海报/创意文案配图（结构化输入）<br>• UI 设计稿辅助（扩图、擦除、风格迁移）<br>• 社交媒体内容创作（文生图+局部重绘） | • 工业设计原型快速建模（单图转3D）<br>• 游戏/AR 场景资产生成（多视角重建）<br>• 电商 3D 商品展示（文生3D+渲染图）<br>• 教育可视化教具制作 | • 短视频内容批量生产（文生视频/T2V）<br>• 产品演示动画（图生视频/I2V）<br>• 虚拟主播播报（数字人+口型同步）<br>• 营销视频智能编辑（指令驱动剪辑/风格重绘） |

## 各方案适用场景建议

### ✅ 图像生成 —— 优先选择当需求满足以下任一条件：
- **高频、低延迟响应**：如实时设计辅助、A/B 测试图生成、前端组件占位图填充；
- **精细控制要求高**：需局部重绘、掩码编辑、文字渲染（千问-文生图支持段落级文本）、结构化海报生成；
- **垂直行业强适配**：电商（虚拟模特/鞋靴模特）、人像（FaceChain 写真）、创意营销（WordArt 锦书）；
- **成本敏感型批量任务**：利用 `n=4` 一次生成多图，或选用 `wan2.5-i2i-preview` 等轻量模型降本。

> ⚠️ 注意：免费体验模型（如 `wanx-x-painting`）额度用尽即停用，**生产环境务必迁移到 `qwen-image-edit` 或 `wanx-image-edit` 等正式商用模型**。

### ✅ 3D生成 —— 优先选择当需求满足以下条件：
- **需要可交付的 3D 资产**：目标为 GLB 导入 Unity/Unreal、WebGL 渲染、3D 打印或 CAD 二次编辑；
- **输入素材明确**：已有清晰单图（正视图）或已采集标准四视角照片（前/左/后/右）；
- **对几何精度有分级诉求**：P1.0 满足快速原型验证；H3.1 用于高保真工业/游戏资产；
- **接受异步工作流**：能容忍 30 秒–2 分钟生成延迟，并具备任务轮询与结果缓存能力。

> ⚠️ 注意：**多图输入必须严格遵循 4 元素数组格式**，任何索引错位或长度不符将直接报错；所有输出 URL 2 小时过期，需及时下载并持久化存储。

### ✅ 视频生成 —— 优先选择当需求满足以下条件：
- **内容动态化刚需**：需表达时间维度信息（动作、过渡、叙事），静态图无法替代；
- **已有视频/音频资产需增强**：如老视频超分、配音口型同步、营销视频风格重绘；
- **数字人交互场景**：虚拟客服、AI 讲师、品牌代言人等需人脸驱动与语音驱动耦合；
- **支持多模态输入协同**：例如“参考图 + 文本提示 + 音频”联合生成定制化播报视频。

> ⚠️ 注意：**万相 2.7 是当前唯一推荐版本**，旧版（2.1–2.6）已停止功能迭代，且不支持首尾帧续写等关键能力；调用前务必核对模型文档中的 Endpoint 路径是否匹配。

## 面向开发者的选型参考指南

| 选型考量点 | 推荐策略 |
|------------|----------|
| **首次集成，追求快速验证** | 从图像生成入手：使用 `qwen-image-2.0-pro` 同步接口 + `size="1024*1024"` + `watermark=false`，5 分钟内完成 Hello World；避免初期陷入异步轮询复杂度。 |
| **构建端到端生成流水线** | 采用「图像 → 3D → 视频」分层架构：<br>• 图像生成产出高质量参考图 →<br>• 3D生成构建可交互资产 →<br>• 视频生成驱动动画与播报；<br>注意各环节地域一致性（推荐统一部署于北京地域）。 |
| **控制成本与性能平衡** | • 图像：用 `qwen-image-2.0-pro` 替代 `wan2.6-t2i`（精度相当，单价更低）；<br>• 3D：P1.0 满足 80% 场景，H3.1 仅在材质/拓扑要求严苛时启用；<br>• 视频：`viduq3-turbo_text2video` 比 `happyhorse-1.1-t2v` 快 40%，适合大批量 T2V。 |
| **规避兼容性风险** | • 坚决弃用所有标注“仅限免费体验”的模型（如 `wanx-virtualmodel`）；<br>• 视频类务必检查模型文档中 `api_path` 是否为 `/video-synthesis`（万相 2.7）而非 `/image2video/`（旧版）；<br>• 所有图片/视频 URL 必须配置 CORS 允许 `dashscope.aliyuncs.com`，否则触发 `InputDownloadFailed`。 |
| **错误诊断优先路径** | 1. 检查 `Authorization` 和 `X-DashScope-Async` Header 是否存在且正确；<br>2. 核对地域是否一致（Key / Endpoint / 控制台开通地域）；<br>3. 验证输入格式（如 3D 的 `images` 长度、视频的 `media` 类型）；<br>4. 查阅对应模型文档末尾的「错误码说明」，而非通用错误页。 |

> 💡 **终极建议**：多模态生成不是“选一个

## 被对比主题页

- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)


