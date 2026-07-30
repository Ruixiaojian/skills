# [多模态](../concepts/multi-modal.md)生成能力对比：图像生成、3D生成与视频生成

本文旨在为开发者提供百炼平台三大核心[多模态](../concepts/multi-modal.md)生成能力（图像生成、3D生成、视频生成）的系统性对比，帮助技术团队基于业务需求、性能约束、成本预算与工程落地复杂度，做出科学、可持续的技术选型决策。随着AIGC应用从静态内容向空间化、时序化演进，理解三类能力在输入表达力、输出可控性、调用链路与资源消耗上的本质差异，已成为构建高质量AI原生应用的关键前提。

---

## 关键维度对比表

| 维度 | 图像生成 | 3D生成 | 视频生成 |
|------|----------|--------|----------|
| **输入格式** | • 文本提示（`prompt`）<br>• 输入图像 URL（图生图/局部重绘等）<br>• 多图输入（如 `vidu-image_reference2image` 支持最多14张参考图）<br>• 支持文字渲染增强（`qwen-image-edit`） | • **三者互斥**：<br> ✓ 文本提示（`input.prompt`）<br> ✓ 单张图像 URL（`input.image`）<br> ✓ 四视角图像数组（`input.images`，固定顺序：前/左/后/右，空位填 `{}`） | • 文本提示（`input.prompt`）<br>• 首帧/首尾帧图像 URL 数组（`media` 中含 `first_frame`/`last_frame`）<br>• 参考图像/视频/音频 URL（`reference_image`, `video`, `audio`）<br>• 支持[多模态](../concepts/multi-modal.md)混合输入（如视频+音频对口型） |
| **输出格式** | • JPG/PNG/WebP 等标准图像文件（URL 下载）<br>• 部分模型支持 SVG（如 `wordart`）<br>• 输出分辨率灵活（512×512 至 2048×2048，部分支持 4K） | • GLB 格式 PBR 材质模型（`pbr_model_url`，含贴图与物理材质）<br>• 可选无贴图基础网格（`base_model_url`，需显式设 `"texture": false, "pbr": false`）<br>• 同步返回预览图（`rendered_image_url`，JPG） | • MP4 视频文件（`output.video_url`）<br>• 分辨率支持 `720P`/`1080P`/自定义尺寸（如 `"1280*720"`）<br>• 时长通常为 3–5 秒（部分模型支持最长 10 秒）<br>• 可选水印、宽高比（`aspect_ratio`）、风格编号（`style`） |
| **支持模型（主力推荐）** | • `qwen-image-3.0-pro`（文生图+图生图，多模态统一接口）<br>• `wan2.6-t2i`（万相V2文生图，同步低延迟）<br>• `wan2.7-image-pro`（4K图文混排与专业编辑）<br>• `z-image-turbo`（轻量级快速生图） | • `Tripo/Tripo-H3.1`（高精度，最高200万面，支持 `ultra` 几何质量）<br>• `Tripo/Tripo-P1.0`（专业级快速生成，最高2万面，生产首选） | • `wan2.7-t2v-*` / `wan2.7-i2v`（万相2.7系列，首帧/首尾帧/续写三合一）<br>• `happyhorse-1.1-t2v` / `happyhorse-1.1-i2v`（稳定高质通用模型）<br>• `pixverse-c1-*`（动作控制、口型同步、超分等专用能力）<br>• `vidu/viduq3-*`（高性能Turbo系列） |
| **API 端点（北京地域示例）** | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`<br>• 同步调用（`wan2.6-t2i`, `z-image-turbo`）<br>• 异步调用（其余模型，需轮询 `/api/v1/tasks/{task_id}`） | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`<br>• **强制异步**，必须带 `X-DashScope-Async: enable`<br>• 仅华北2（北京）地域可用 | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`<br>• **强制异步**，必须带 `X-DashScope-Async: enable`<br>• 支持多地域（北京/新加坡/弗吉尼亚），但模型、Key、Endpoint 必须同地域 |
| **计费方式** | • 按**成功生成的图片张数**计费（失败/无效输入不计费）<br>• 免费额度：多数模型提供 500 张/90天<br>• 单价示例：`wanx-v1` 0.16元/张；主力模型价格详见控制台资费页 | • 按**单次任务成功生成**计费（无论输出面数或分辨率）<br>• 免费额度：开通 Tripo 服务后赠送（具体额度见控制台）<br>• `H3.1` 与 `P1.0` 单价不同，`ultra` 模式不额外加价但耗时更长 | • 按**视频秒数 × 模型单价**计费（如 `liveportrait` 0.02元/秒，`emo-v1` 0.08–0.16元/秒）<br>• 免费额度按模型独立发放，不可跨模型共享<br>• 首帧/首尾帧/参考生视频等不同模式可能对应不同单价 |
| **典型场景** | • 电商商品图生成与背景替换<br>• 社媒配图、营销海报批量制作<br>• AI试衣、人像写真、局部重绘<br>• 创意文字设计（WordArt）、鞋靴模特生成 | • 工业设计快速原型验证（如家具、家电）<br>• 游戏/AR/VR 场景资产生成（需中低面数模型）<br>• 电商3D商品展示（配合WebGL/Three.js）<br>• 建筑可视化初稿建模 | • 短视频广告创意生成（文生视频）<br>• 产品演示动画（图生视频 + 风格重绘）<br>• 数字人播报、虚拟主播口型驱动<br>• 视频内容二次创作（编辑、超分、动作迁移） |

---

## 适用场景建议

### ✅ 图像生成 —— 适合「高吞吐、低延迟、强可控」的静态内容生产
- **推荐场景**：  
  - 需要每秒生成多张图的批量任务（如千张商品图生成）→ 选用 `z-image-turbo` 或 `wan2.6-t2i`（同步调用）；  
  - 要求语义精准+构图控制 → 优先 `qwen-image-3.0-pro`（支持 `messages` 多轮指令）；  
  - 专业级图像编辑（如换脸、风格迁移、多图参考）→ `wan2.7-image-pro` 或 `vidu/vidu-image_reference2image`；  
- **慎用场景**：  
  - 需要深度空间理解（如透视一致性、遮挡关系）的任务 → 图像生成无法替代3D建模；  
  - 动态过程表达（如物体运动轨迹、时间演变）→ 应转向视频生成。

### ✅ 3D生成 —— 适合「空间结构明确、需可交互资产」的三维内容构建
- **推荐场景**：  
  - 从单张产品照片快速生成可旋转查看的3D模型（电商展示）→ `Tripo-P1.0`（平衡速度与质量）；  
  - 设计师输入草图/多视角图，生成高保真工业模型 → `Tripo-H3.1` + `geometry_quality: "ultra"`；  
  - AR应用需轻量化模型 → 显式设置 `"texture": false, "pbr": false` 获取 `base_model_url`；  
- **慎用场景**：  
  - 输入仅为模糊文本描述（如“未来感城市”）→ 3D生成易失真，建议先用图像生成辅助构思；  
  - 需实时渲染或物理仿真 → 百炼3D输出为静态GLB，需下游引擎（Unity/Unreal）集成；  
  - 非北京地域项目 → 当前不支持，需评估架构迁移成本。

### ✅ 视频生成 —— 适合「时序表达、行为模拟、人机交互」的动态内容创作
- **推荐场景**：  
  - 企业数字人播报、客服视频生成 → `liveportrait`（低成本）或 `emo-v1`（高表现力）；  
  - 将静态产品图转为3–5秒展示动画 → `wan2.7-i2v`（首帧生视频，稳定性好）；  
  - 多镜头脚本驱动的短视频 → `happyhorse-1.1-t2v` + 结构化 [prompt](../guides/prompt.md)（分镜描述）；  
  - 视频内容增强（口型同步、画质超分、风格迁移）→ `pixverse/pixverse-lipsync` / `pixverse/pixverse-upscale`；  
- **慎用场景**：  
  - 超长视频（>10秒）或复杂运镜 → 当前模型普遍不支持，需分段生成+后期拼接；  
  - 高精度物理运动模拟（如流体、布料动力学）→ 属于专业仿真范畴，非AIGC视频模型能力边界；  
  - 对首帧到末帧运动逻辑有强因果约束（如机械臂精确路径）→ 建议结合传统动画工具或程序化生成。

---

## 技术选型参考指南（面向开发者）

| 选型维度 | 推荐策略 |
|----------|----------|
| **开发效率优先** | • 图像生成：首选 `qwen-image-3.0-pro`（统一 `messages` 接口，文档完备，SDK支持好）<br>• 3D生成：用 `Tripo-P1.0`（响应快、错误率低、无需调优）<br>• 视频生成：用 `wan2.7-i2v`（兼容性强，支持首帧/首尾帧/续写，减少接口切换） |
| **生产稳定性优先** | • 所有类型均**必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），禁用 `dashscope.aliyuncs.com` 公共域名<br>• API Key、模型、Endpoint **严格同地域绑定**，跨地域调用将直接失败（非降级，是硬性拦截）<br>• 异步任务务必实现幂等轮询（建议 ≥15 秒间隔）+ 异步回调（避免轮询风暴） |
| **成本优化建议** | • 图像：善用免费额度，高频调用优先选 `z-image-turbo`（单价更低）<br>• 3D：`P1.0` 满足80%场景，避免默认用 `H3.1` 增加等待成本<br>• 视频：按秒计费，明确 `duration` 参数；对口型/超分等附加功能单独调用，避免冗余处理 |
| **长期维护性** | • 避免使用标注“仅免费体验”或“推荐替代”的模型（如 `wanx-v1`, `shoemodel-v1`, `wan2.2-kf2v-fla`）<br>• 优先选用带版本号的主力模型（如 `wan2.7-*`, `qwen-image-3.0-pro`, `Tripo-P1.0`），其API契约稳定、文档持续更新<br>• 关注 [模型市场](https://bailian.console.aliyun.com) 中的“维护状态”标签，弃用模型将逐步关闭服务 |
| **工程集成提示** | • 图像/视频 URL 下载链接均有有效期（图像24h，3D模型2h，视频2h），**必须及时持久化存储**<br>• 输入图像/视频 URL 必须公网可访问、无中文路径、支持HTTP/HTTPS；OSS需设为 public-read<br>• 错误处理应基于 `code` 字段（非 `message` 文本），查阅[统一错误码文档](https://help.aliyun.com/zh/model-studio/error-code) |

> 💡 **一句话选型口诀**：  
> **“图快选图像，

## 被对比主题页

- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)


