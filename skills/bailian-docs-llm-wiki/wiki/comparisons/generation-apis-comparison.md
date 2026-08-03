# 多模态生成 API 对比：图像、视频与3D生成

为帮助开发者快速理解百炼平台在多模态生成领域的能力边界与技术选型路径，本文系统对比图像生成、视频生成与3D生成三类核心API。对比聚焦实际工程落地关键维度——包括调用模式、输入/输出规范、模型生态、计费策略及典型适用场景，旨在提供清晰、可操作的技术决策依据。所有信息均基于当前（2024年Q3）百炼平台正式发布的API文档与控制台配置策略。

## 关键维度对比表

| 维度 | 图像生成（`api/image-generation.md`） | 视频生成（`api/video-generation-api.md`） | 3D生成（`api/3d-generation.md`） |
|------|----------------------------------------|-------------------------------------------|-----------------------------------|
| **核心能力** | 文生图（T2I）、图生图（I2I）、局部编辑、风格迁移、AI试衣等15+专业场景 | 文生视频（T2V）、图生视频（I2V）、首尾帧生视频（KF2V）、参考生视频（R2V）、数字人动画、视频编辑 | 文生3D、单图生3D、多图生3D（前/左/后/右四视角） |
| **输入格式** | • `prompt`（文本）或 `messages`（结构化提示）<br>• 支持图像URL数组（I2I/R2I）、草图base64、擦除mask等<br>• 局部重绘需指定`region_mask` | • `input.prompt`（T2V）<br>• `input.media` 数组（含`image_url`/`first_frame`/`last_frame`/`reference_image`等type）<br>• 数字人需`image_url`+`audio_url` | • 三者互斥：`input.prompt`（文本） 或 `input.image`（单图URL） 或 `input.images`（长度=4的数组，空位用`{}`占位） |
| **输出格式** | • 同步调用：HTTP 200 直接返回含`output.results[]`的JSON，含`url`字段指向图片<br>• 异步调用：返回`task_id`，轮询获取`result.url`<br>• 支持水印开关、多图批量生成（`n=1–9`） | • **强制异步**：返回`task_id`，轮询`/api/v1/tasks/{task_id}`获取`result.video_url`<br>• 输出为MP4（H.264编码），含`duration`、`resolution`、`aspect_ratio`元信息 | • **强制异步**：返回`task_id`，轮询获取`output.results`<br>• 输出含`pbr_model_url`（GLB/PBR材质）、`rendered_image_url`（预览图）、`base_model_url`（无材质基础网格） |
| **支持模型/服务** | • 主流通用模型：`wan2.6-t2i`、`qwen-image-3.0-pro`、`kling/kling-v3-image-generation`、`vidu/vidu-image_reference2image`<br>• 垂直工具模型：`virtualmodel-v2`、`shoemodel-v1`、`image-instance-segmentation`等（部分免费体验） | • 多厂商模型：`wan2.7-t2v-2026-06-12`、`vidu/viduq3-turbo_text2video`、`kling/kling-v3-video-generation`、`pixverse/pixverse-c1-t2v`、`happyhorse-r2v`<br>• 数字人专用：`liveportrait`、`emo-v1`、`animate-anyone-gen2` | • 仅Tripo模型：`Tripo/Tripo-P1.0`（2万面，快）与`Tripo/Tripo-H3.1`（200万面，高精）<br>• 依赖Tripo官方服务，无其他第三方模型接入 |
| **API端点（推荐）** | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/text-to-image`（及其他子路径如`image-to-image`） | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（统一入口） | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`（注意路径含`video-generation`但属3D服务） |
| **调用模式** | • **混合模式**：`wan2.6-t2i`、`z-image-turbo`等支持同步直出；`wanx-v1`、`wan2.5-i2i-preview`等强制异步<br>• 同步响应快（<5s），异步任务有效期24h | • **强制异步**：所有模型均需`X-DashScope-Async: enable`头<br>• 任务状态轮询，有效期24h<br>• 不支持同步直出 | • **强制异步**：必须携带`X-DashScope-Async: enable`<br>• 任务有效期24h，结果URL有效期2h<br>• 无同步选项 |
| **计费方式** | • 按[Token](../concepts/token.md)/请求/生成张数计费（因模型而异）<br>• 部分模型（如`wanx-x-painting`、`shoemodel-v1`）为**免费体验**，额度用尽即停用，不支持付费开通<br>• `qwen-image-3.0-pro`等主流模型按调用量计费 | • 按视频时长（秒）× 分辨率系数计费<br>• 所有模型均为**按量付费**，无免费体验额度<br>• 数字人模型（如`liveportrait`）单独计费，需先调用检测模型（免费） | • 按生成任务计费（与面数/精度相关）<br>• `Tripo-P1.0`与`Tripo-H3.1`单价不同（H3.1更贵）<br>• **无免费额度**，全部按任务计费 |
| **地域要求** | • 支持华北2（北京）、新加坡等多地域<br>• 推荐使用业务空间专属域名（`{WorkspaceId}.{region}.maas.aliyuncs.com`） | • **强地域绑定**：API Key、Endpoint、模型必须同地域（如北京Key只能调北京模型）<br>• 跨地域调用必然失败 | • **仅支持华北2（北京）地域**<br>• API Key必须在北京地域创建，Endpoint固定为`cn-beijing.maas.aliyuncs.com` |
| **典型场景** | • 电商商品图生成与背景替换<br>• 社媒海报/营销素材批量制作<br>• AI试衣、虚拟模特展示<br>• UI设计稿转效果图、局部修图 | • 短视频内容创作（广告/种草/剧情）<br>• 产品动态演示（首尾帧过渡）<br>• 数字人播报/虚拟偶像演唱<br>• 参考图驱动的品牌视频生成 | • 游戏资产快速建模（概念验证）<br>• 工业零件/家具3D原型生成<br>• AR/VR应用中的轻量化3D内容生产<br>• 电商平台商品3D展示 |

## 各方案适用场景建议

- **选择图像生成 API 当**：  
  ✅ 需要高频、低延迟产出静态视觉内容（如每日千张商品图）；  
  ✅ 场景高度垂直（如鞋类模特、海报生成），可利用`shoemodel-v1`或`wanx-poster-generation-v1`等免费工具模型；  
  ✅ 对输出分辨率有明确分级需求（`1K`/`2K`/`4K`），且需同步直出保障用户体验；  
  ❌ 不适合需要动态表达、时间序列建模或三维空间理解的任务。

- **选择视频生成 API 当**：  
  ✅ 核心目标是生成具备时间连续性的动态内容（如3–5秒短视频）；  
  ✅ 需要多模态输入协同（如首帧+尾帧+文本描述实现平滑转场）；  
  ✅ 业务涉及数字人交互（播报、口型同步、表情驱动）；  
  ✅ 可接受异步工作流与24小时任务生命周期；  
  ❌ 不适合对首帧到成片延迟敏感的实时交互场景（如直播即时生成）；  
  ❌ 避免跨地域混用Key与Endpoint，部署前须严格校验地域一致性。

- **选择3D生成 API 当**：  
  ✅ 明确需要可导入引擎（Unity/Unreal）或WebGL渲染的标准化3D资产（GLB格式）；  
  ✅ 输入条件满足：能提供高质量单图（正面清晰）或严格按序的四视角图；  
  ✅ 对几何精度有分级需求（P1.0用于快速原型，H3.1用于高保真工业建模）；  
  ✅ 已确认业务部署在北京地域，且能处理2小时结果链接时效性；  
  ❌ 不适用于需要纹理贴图精细控制、UV展开或拓扑编辑的后期流程；  
  ❌ 不支持非Tripo模型，无法切换底层渲染器或物理引擎。

## 技术选型参考（面向开发者）

1. **优先验证输入兼容性**：  
   - 图像API对输入格式最灵活（文本/图/草图/掩码），适合MVP快速验证；  
   - 视频API要求`media`结构严格，务必按`type`字段区分首帧、尾帧、参考图；  
   - 3D API的`images`数组长度与顺序为硬约束，开发时需前置校验并填充空位`{}`。

2. **关注调用链路稳定性**：  
   - **统一使用业务空间专属域名**（`{WorkspaceId}.{region}.maas.aliyuncs.com`），旧版`dashscope.aliyuncs.com`已逐步弃用，影响成功率与性能；  
   - 视频与3D API均强制异步，务必实现健壮的轮询逻辑（建议指数退避+超时熔断），避免阻塞主线程；  
   - 3D API结果URL仅2小时有效，下载逻辑需嵌入轮询成功后的立即执行流程。

3. **成本与合规性前置评估**：  
   - 免费模型（如`shoemodel-v1`）不可用于生产环境长期依赖，需规划替代付费模型路径；  
   - 视频与3D均为纯按量计费，建议在测试阶段开启配额告警，防止意外超支；  
   - 3D生成仅限北京地域，若业务已部署于新加坡，需评估数据跨境传输合规性或架构迁移成本。

4. **模型演进策略**：  
   - 图像领域：优先采用`wan2.7-image-pro`（4K/2K编辑）或`qwen-image-3.0-pro`（强几何推理），避免使用已标注“推荐升级”的`wanx-v1`；  
   - 视频领域：坚决选用`wan2.7`系列（支持多镜头叙事、视频续写），弃用仅支持单帧的`wan2.6`旧版；  
   - 3D领域：`Tripo-H3.1`精度更高但成本上升，建议A/B测试后按精度需求分级调用。

> **最后提醒**：所有API均需通过DashScope SDK或标准HTTP调用，SDK已封装地域路由、重试、鉴权等共性逻辑，**强烈建议优先集成最新版DashScope Python/Java SDK**，而非手写HTTP客户端。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


