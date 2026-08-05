# 多模态生成 API 对比：Image Generation vs Video Generation API vs 3D Generation

为帮助开发者快速理解百炼平台多模态生成能力的定位差异与技术边界，本文系统对比 **图像生成（Image Generation）**、**视频生成（Video Generation API）** 和 **3D 模型生成（3D Generation）** 三大核心 API 能力。对比聚焦实际工程落地的关键维度——包括调用模式、输入/输出规范、模型生态、地域约束及计费逻辑等，旨在为产品设计、技术选型与资源规划提供清晰、可执行的决策依据。

---

## 关键维度对比表

| 维度 | Image Generation | Video Generation API | 3D Generation |
|------|------------------|------------------------|----------------|
| **核心能力定位** | 文生图、图生图、局部编辑、风格迁移、背景生成、擦除补全等二维视觉内容生成与精细化操控 | 文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、动作迁移、口型同步、数字人播报等时序动态内容生成 | 文生3D、单图生3D、多图生3D 等三维几何+材质模型生成，输出可渲染、可导入引擎的 PBR/GLB 文件 |
| **输入格式** | • 文生图：`{"prompt": "..."}` 或 `messages` 结构<br>• 图生图/编辑：`messages` 中混合 `text` + `image` URL<br>• 工具类（擦除/扩图）：`{"image_url": "...", "mask_url": "..."}` | • 文生视频：`{"prompt": "..."}`<br>• 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "..."}`<br>• 首尾帧：`{"media": [{"type": "first_frame",...}, {"type": "last_frame",...}], "prompt": "..."}`<br>• 视频编辑/口型同步：支持 `video_url` + `audio_url`/`image_url` 组合 | • 文生3D：`{"prompt": "..."}`<br>• 单图生3D：`{"image": "https://..."}`<br>• 多图生3D：`{"images": [{"file_token": "..."}, {}, {"file_token": "..."}, {}]}`（**严格4元素数组，空位用 `{}` 占位**） |
| **输出格式** | • 同步调用：HTTP 200 直接返回 `output.results[0].url`（图片 URL，有效期 ≥24 小时）<br>• 异步调用：轮询 `GET /tasks/{task_id}` 获取 `output.results[n].url` | • 全部异步：轮询 `GET /tasks/{task_id}`，成功后返回 `output.video_url`（MP4，有效期 24 小时）<br>• 部分模型支持 `output.audio_url`（如口型同步） | • 全部异步：轮询 `GET /tasks/{task_id}`，成功后返回：<br> ✓ `pbr_model_url`（GLB，含 PBR 材质与贴图，默认）<br> ✓ `base_model_url`（无贴图基础网格，需显式设置 `pbr: false & texture: false`）<br> ✓ `rendered_image_url`（预览图）<br>• 所有 URL 有效期 **2 小时**，需及时下载 |
| **支持模型（代表性）** | • 通用：`qwen-image-3.0-pro`、`wan2.6-t2i`、`z-image-turbo`<br>• 编辑：`wan2.7-image-pro`、`qwen-image-edit` 系列<br>• 垂直：`virtualmodel-v2`（虚拟模特）、`shoemodel-v1`（鞋靴试穿）、`wanx-poster-generation-v1`（海报） | • 文生视频：`happyhorse-1.1-t2v`、`vidu/viduq3-turbo_text2video`、`kling/kling-v3-video-generation`<br>• 图生视频：`pixverse/pixverse-c1-it2v`、`vidu/viduq3-pro-fast_img2video`<br>• 专用：`liveportrait`（数字人）、`videoretalk`（口型同步）、`pixverse/pixverse-upscale`（超分） | • `Tripo/Tripo-H3.1`（高精度，≤200 万面，支持 `geometry_quality: "ultra"`）<br>• `Tripo/Tripo-P1.0`（快速生成，≤2 万面） |
| **API 端点（典型）** | • 同步：`POST /api/v1/services/aigc/multimodal-generation/generation`<br>• 异步：`POST /api/v1/services/aigc/image2image/image-synthesis` 等（路径因模型而异） | `POST /api/v1/services/aigc/video-generation/video-synthesis`<br>（`wan2.7+` 新协议统一路径；旧版 `wan2.2/2.5` 使用 `/image2video/...`） | `POST /api/v1/services/aigc/video-generation/3d-generation`<br>（注意：路径含 `video-generation`，但属 3D 服务，为历史兼容命名） |
| **调用模式** | • **混合模式**：`qwen-image-3.0-pro`、`wan2.6-t2i` 等主流模型支持**同步调用**（低延迟，适合实时交互）；<br>• 局部重绘、虚拟模特、扩图等耗时任务强制**异步调用**（需轮询） | • **强制异步**：所有模型均需 `X-DashScope-Async: enable`，创建任务 → 轮询结果 → 下载视频<br>• 无同步接口 | • **强制异步**：必须携带 `X-DashScope-Async: enable`，否则报错 `"current user api does not support synchronous calls"` |
| **地域与域名约束** | • 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`<br>• 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`<br>• 弗吉尼亚/法兰克福：仅支持旧国际域名，且部分模型不可用 | • 严格绑定：API Key、Endpoint、模型开通地域三者必须一致<br>• 华北2（北京）：`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`<br>• 新加坡：`{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` | • **仅支持华北2（北京）地域**：<br> ✓ Endpoint 必须为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`<br> ✗ 其他地域域名直接返回 404 或鉴权失败 |
| **计费方式** | • 按**成功生成的图片张数**计费（失败/错误不扣费）<br>• 多数模型提供 **500 张/90 天免费额度**（如 `wan2.6-t2i`）<br>• 单价示例：`image-out-painting` 0.18 元/张 | • 按**成功生成的视频条数**计费<br>• 免费额度依具体模型而定（如 `HappyHorse` 提供 100 秒/月免费额度）<br>• 计费粒度细：部分模型按分辨率（720P/1080P）或时长（5s/8s）分级定价 | • 按**成功生成的 3D 模型个数**计费<br>• 当前无公开免费额度，需按量付费<br>• `Tripo-H3.1`（高面数）单价高于 `Tripo-P1.0`（快速版） |
| **典型场景** | • 电商商品图生成与换背景<br>• 社媒创意海报批量制作<br>• 设计师辅助：局部重绘、风格迁移、AI扩图<br>• 虚拟试穿（鞋靴/模特） | • 短视频平台：AI脚本→视频自动成片<br>• 教育/营销：图文内容动态化（PPT转视频、产品图转演示视频）<br>• 数字人播报：新闻/客服语音驱动口型与表情<br>• 游戏/动画：动作迁移、角色替换 | • 工业设计：产品概念快速建模（文生3D）<br>• 电商：多角度商品 3D 展示（多图生3D）<br>• AR/VR 应用：轻量化 3D 资产生成（P1.0 快速交付）<br>• 游戏美术：高精度资产原型（H3.1 超面数输出） |

---

## 各方案适用场景建议

### ✅ 选择 Image Generation 当：
- 需要**毫秒级响应**的轻量级视觉生成（如搜索页实时配图、聊天机器人即时插画）；
- 核心诉求是**二维平面内容的精准控制**（文字添加、物体擦除、背景替换、风格一致性）；
- 场景高度垂直（如海报生成、虚拟模特、鞋靴试穿），可直接复用预置专用模型；
- 开发团队希望最小化异步轮询复杂度，优先采用同步 API 简化客户端逻辑。

### ✅ 选择 Video Generation API 当：
- 业务本质依赖**时间维度表达**（故事叙述、产品演示、教学过程、情感传递）；
- 输入源为**静态图像或文本**，需自动赋予运动、节奏与镜头语言（如“将产品图生成 5 秒广告视频”）；
- 需深度集成**音视频工作流**（口型同步、音频驱动、视频超分、多镜头编排）；
- 接受 10–60 秒级任务延迟，并已构建健壮的异步任务状态管理机制（轮询/回调）。

### ✅ 选择 3D Generation 当：
- 终端目标为**可交互、可渲染、可导入引擎的三维资产**（非 GIF 或 MP4）；
- 输入具备明确**三维结构线索**（多视角照片）或需从零构建**几何拓扑+PBR材质**；
- 应用场景强依赖**空间属性**（AR 商品预览、工业仿真、游戏关卡原型、数字孪生）；
- 团队具备 GLB 解析、WebGL/Unity/Unreal 加载能力，且能处理 2 小时短时效 URL 下载逻辑。

> ⚠️ **关键避坑提示**：  
> - **勿混淆 3D 与 Video**：3D 输出是静态模型文件（`.glb`），非视频；若需“3D 动画视频”，需额外调用 Video Generation API 对 3D 渲染图序列进行图生视频。  
> - **地域锁死风险**：3D Generation 仅限北京地域，若业务已部署在新加坡集群，需单独申请北京 Workspace 并桥接数据流。  
> - **异步成本意识**：Video 与 3D 均强制异步，高频调用需主动配置 [异步任务回调](https://help.aliyun.com/zh/model-studio/async-task-api) 替代轮询，避免 QPS 浪费与延迟抖动。

---

## 技术选型参考（面向开发者）

| 选型考量点 | 推荐行动 |
|------------|----------|
| **延迟敏感型应用**（如实时设计工具、聊天机器人） | 优先评估 `qwen-image-3.0-pro` 等同步图像模型；避开 Video/3D（固有异步延迟）。 |
| **输入源为单张图，期望输出动态内容** | • 若需**简单运动生成**（如轻微晃动、平移）→ 选用 `pixverse/pixverse-c1-it2v`（图生视频）<br>• 若需**精确三维重建** → 选用 `Tripo/Tripo-P1.0`（单图生3D），再自行渲染动画。 |
| **预算有限，需最大化免费额度** | • 图像：善用 `wan2.6-t2i`（500 张/90 天）+ `wanx-poster-generation-v1`（免费海报）<br>• 视频：关注 `HappyHorse` 免费额度，避免高分辨率/长时长任务<br>• 3D：暂无免费额度，建议先用 `P1.0` 快速验证，再按需升级 `H3.1`。 |
| **跨地域架构部署** | • 图像/视频：按 Workspace 地域分别配置 API Key 与域名，避免混用<br>• 3D：必须在北京地域独立部署服务模块，通过内网或消息队列与主业务解耦。 |
| **错误处理与可观测性** | • 统一捕获 `code`/`message` 字段，关联 [错误码文档](

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


