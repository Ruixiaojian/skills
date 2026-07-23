# [多模态](../concepts/multi-modal.md)生成能力对比：图像、视频与3D生成

为帮助开发者快速理解百炼平台在[多模态](../concepts/multi-modal.md)生成领域的技术布局与能力边界，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心能力。对比聚焦实际工程落地的关键维度——包括调用模式、模型生态、输入输出规范、计费逻辑与适用场景，旨在为技术选型提供客观、可操作的决策依据。所有信息均基于当前（2024年Q3）百炼平台正式发布的API文档与控制台配置。

## 关键能力维度对比

| 维度 | 图像生成（Image） | 视频生成（Video） | 3D生成（3D） |
|------|-------------------|-------------------|--------------|
| **核心输入格式** | 文本（[prompt](../guides/prompt.md)）、单图/多图（URL）、掩码图（mask_image_url）、草图（sketch）、风格参考图等；支持图文混排指令 | 文本（[prompt](../guides/prompt.md)）、首帧/首尾帧图像（image_url）、参考视频（video_url）、音频（audio_url）、[多模态](../concepts/multi-modal.md)组合（如图+音+[prompt](../guides/prompt.md)） | 文本（prompt）、单张图像（image）、四视角图像数组（images: [front, left, back, right]）；三者互斥 |
| **核心输出格式** | JPEG/PNG 图像（URL 或 base64），支持 512×512 至 4K 分辨率；含预览图、水印开关、扩展结果（如增强 prompt） | MP4 视频（URL），时长默认 5 秒（可设 2–10 秒），分辨率支持 480P–1080P；含封面帧、元数据（duration/frame_rate） | GLB 格式 PBR 材质模型（pbr_model_url）、无贴图基础网格（base_model_url）、渲染预览图（rendered_image_url）；支持面数分级（2万–200万面） |
| **主流支持模型** | `qwen-image-3.0-pro`, `wan2.7-image-pro`, `kling/kling-v3-image-generation`, `vidu/vidu-image_reference2image`, `z-image-turbo` | `wan2.7-t2v-2026-06-12`, `happyhorse-1.1-t2v`, `vidu/viduq3-turbo_text2video`, `emo-v1`, `liveportrait`, `pixverse/pixverse-c1-t2v` | `Tripo/Tripo-P1.0`（快模版，≤2万面），`Tripo/Tripo-H3.1`（高精版，≤200万面） |
| **API 端点（推荐）** | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`（同步/异步共用路径，行为由模型决定） | `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（全模型统一端点，强制异步） | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`（仅华北2可用，强制异步） |
| **调用模式** | **混合模式**：`wan2.6+` / `qwen-image-3.0-pro` / `z-image-turbo` 支持同步（直接返回结果）；`wanx-v1` / `wanx-x-painting` / `image-out-painting` 等仅支持异步（需轮询 task_id） | **强制异步**：全部模型必须使用 `X-DashScope-Async: enable`，创建任务后轮询 `GET /api/v1/tasks/{task_id}` 获取结果 | **强制异步**：必须启用 `X-DashScope-Async: enable`；轮询间隔建议 ≥15 秒；task_id 有效期 24 小时 |
| **计费方式** | 按生成张数计费（例：`wanx-v1` 0.16元/张，`image-out-painting` 0.18元/张）；主账号与子账号共享 500 张免费额度（90天有效期） | 按模型独立计费：文生视频按秒（如 `wan2.7-t2v` 0.35元/秒）、人像动画按时长（`emo-v1` 0.28元/秒）、口型替换按音频秒数；各模型有独立免费额度（如 `emo-detect-v1` 200次） | 按任务计费：`Tripo-P1.0` 0.8元/次，`Tripo-H3.1` 2.5元/次；暂无公开免费额度，需开通后查看控制台配额 |
| **典型响应耗时** | 同步调用：3–8 秒（T2I/I2I）；异步调用：10–60 秒（含排队） | 1–5 分钟（受分辨率、时长、模型复杂度影响显著；高精度或多镜头任务可达 8 分钟） | 2–10 分钟（`P1.0` 通常 ≤3 分钟；`H3.1` + `ultra` 模式常需 6–10 分钟） |
| **地域支持** | 华北2（北京）、新加坡、美国（弗吉尼亚）三地全域支持；密钥与 endpoint 必须严格匹配 | 华北2（北京）、新加坡、美国（弗吉尼亚）、德国（法兰克福）；跨地域调用将返回 `401 Unauthorized` | **仅华北2（北京）**；其他地域 endpoint 不可用，调用必失败 |
| **关键限制** | • 输入图需公网可访问 HTTPS URL<br>• `wan2.5` 及以下版本不支持同步调用<br>• 局部重绘/背景生成等高级功能限北京地域专属域名 | • 所有模型强制异步，无同步选项<br>• 音频输入需清晰人声、≤30 秒<br>• Prompt ≤512 字符，含敏感词触发拦截<br>• `liveportrait` 等模型 QPS 限 1 | • 仅支持 JPEG/PNG；单图 ≤20MB；多图需严格四视角顺序<br>• `pbr=true` 时 `texture=false` 无效；唯一无贴图路径：`"texture": false, "pbr": false`<br>• 输出 URL 有效期仅 2 小时 |

## 各方案适用场景建议

### ✅ 图像生成（Image）——适合「高并发、低延迟、强交互」场景  
- **推荐场景**：电商海报批量生成、AIGC设计助手（实时预览）、社交内容配图、UI组件自动化出图、AI修图SaaS集成。  
- **选型提示**：若需毫秒级响应（如用户拖拽即实时重绘），优先选用 `z-image-turbo` 或 `qwen-image-3.0-pro`（同步调用）；若需4K精细输出或复杂编辑（如虚拟模特试穿），选用 `wan2.7-image-pro` 并注意其仅支持异步流程。

### ✅ 视频生成（Video）——适合「叙事表达、数字人驱动、轻量内容生产」场景  
- **推荐场景**：短视频营销素材生成、AI主播播报、产品演示动画、教育口型同步课件、游戏NPC动作迁移。  
- **选型提示**：纯文本生成短片（≤5秒）选 `viduq3-turbo_text2video`；需精准动作控制选 `animate-anyone-gen2`；强调口型自然度选 `pixverse-lipsync`；对并发要求高（如批量生成）需提前申请 QPS 提升，并配置异步回调避免轮询压力。

### ✅ 3D生成（3D）——适合「工业可视化、电商3D展示、AR/VR内容基建」场景  
- **推荐场景**：电商商品3D建模（文生/图生）、工业零件快速原型、建筑概念可视化、元宇宙空间资产生成、教育三维教具制作。  
- **选型提示**：快速验证创意或轻量应用 → `Tripo-P1.0`；需导入CAD/渲染管线或对接Unity/Unreal → `Tripo-H3.1` + `geometry_quality: "ultra"`；务必使用北京地域密钥与专属域名，且提前下载 `pbr_model_url`（2小时过期）。

## 技术选型参考指南（面向开发者）

1. **优先确认调用模式约束**  
   - 若业务无法容忍异步延迟（如实时聊天机器人附带图片生成），**排除视频与3D方案**，仅考虑图像生成中的同步模型（`wan2.6-t2i` 及以上、`qwen-image-3.0-pro`）。  
   - 若已构建成熟异步任务队列（如 Celery/RabbitMQ），视频与3D的强制异步特性反而是优势，可统一调度。

2. **严格校验地域一致性**  
   - 图像生成支持多地，但**视频与3D对地域敏感度极高**：3D仅限北京；视频若在新加坡部署服务，却误用北京密钥，将直接鉴权失败。建议在初始化 SDK 时硬编码 `region` 参数，并做启动校验。

3. **输入准备成本是隐性瓶颈**  
   - 图像：只需文本或单图，接入成本最低；  
   - 视频：需准备高质量音频/多帧图像，且 URL 必须公网可直连（OSS需设 public-read）；  
   - 3D：多图生3D要求严格视角顺序与光照一致性，实测中“前左后右”四图质量不均将导致模型崩坏。建议优先尝试文生3D降低门槛。

4. **计费颗粒度决定架构设计**  
   - 图像按张计费 → 适合按需调用，可缓存结果复用；  
   - 视频按秒计费 → 需精确控制 `duration` 参数，避免默认5秒造成浪费；  
   - 3D按次计费 → 建议对同一prompt/image做结果缓存（MD5哈希索引），避免重复生成。

5. **错误处理策略差异化**  
   - 图像：关注 `400 Bad Request`（参数错）、`403 Forbidden`（额度超）；  
   - 视频：高频出现 `429 Too Many Requests`，需实现指数退避轮询；  
   - 3D：`task_status: "UNKNOWN"` 表示 task_id 过期，必须重新提交任务——不可重试旧ID。

> **最后提醒**：所有多模态能力均依赖 DashScope SDK 最新版（≥4.20.0）及百炼控制台「业务空间」配置。请勿混用旧版文档（如 `wanx-v1` 协议）与新版模型（如 `wan2.7-*`），模型名与 endpoint 的严格匹配是调用成功的前提。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


