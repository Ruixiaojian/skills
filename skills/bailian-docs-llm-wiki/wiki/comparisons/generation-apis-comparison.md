# 多模态生成 API 对比：Image Generation vs Video Generation vs 3D Generation

本文档面向百炼平台开发者，旨在系统性对比图像生成（Image Generation）、视频生成（Video Generation）与三维模型生成（3D Generation）三类核心多模态生成 API 的关键能力、技术约束与工程实践差异。随着AIGC应用场景从静态内容向动态表达与空间交互演进，准确理解各模态API在输入输出、调用范式、资源消耗及适用边界上的本质区别，是构建高性能、低成本、可扩展AI应用的前提。本对比基于百炼平台当前（2024–2026年）稳定发布的生产级API接口规范，覆盖模型支持、协议设计、计费逻辑与典型落地场景，为技术选型提供客观、可执行的决策依据。

| 维度 | Image Generation | Video Generation | 3D Generation |
|------|------------------|-------------------|----------------|
| **核心任务类型** | 文生图（T2I）、图生图（I2I）、局部重绘、背景生成、扩图、擦除补全、风格迁移、AI试穿等十余类 | 文生视频（T2V）、图生视频（I2V）、首尾帧生成、参考生视频（R2V）、视频编辑（指令/超清/风格/动作）、口型替换、数字人播报、唱演驱动等 | 文生3D、单图生3D、多图（前/左/后/右）生3D；支持PBR材质模型与无贴图基础网格 |
| **输入格式** | 灵活组合：<br>• 纯文本（`{"text": "prompt"}`）<br>• 图文混合（`{"messages": [...]}`，含 `text` + `image`）<br>• 基础图+掩码图（`base_image_url` + `mask_image_url`） | 结构化媒体数组：<br>• T2V：`{"prompt": "..."}`<br>• I2V/R2V：`{"media": [{"type": "image_url", "url": "..."}, ...]}`<br>• 首尾帧：`{"media": [{"type": "first_frame",...}, {"type": "last_frame",...}]}`<br>• 口型替换：`{"media": [{"type": "video_url",...}, {"type": "audio_url",...}]}` | 三选一互斥：<br>• 文本：`input.prompt`（≤1024字符）<br>• 单图：`input.image`（JPEG/PNG，20–6000px，≤20MB）<br>• 多图：`input.images`（长度为4的数组，顺序固定：前/左/后/右） |
| **输出格式** | • 原图URL（JPEG/PNG，分辨率可配）<br>• 可选返回推理过程（`thinking_mode: true`）<br>• 部分模型支持多张并行输出（`n=1–9`） | • 视频URL（MP4/H.264，时长2–30秒）<br>• 可选音频轨道（`parameters.audio: true`）<br>• 无中间帧流式返回，仅最终成品URL | • PBR材质模型URL（GLB，含纹理，`pbr_model_url`）<br>• 无贴图基础网格URL（GLB，需同时设 `texture: false` & `pbr: false`）<br>• 渲染预览图URL（WebP，`rendered_image_url`） |
| **支持模型（代表）** | • 通用：`qwen-image-3.0-pro`、`wan2.6-t2i`、`z-image-turbo`<br>• 垂直：`wanx-style-repaint-v1`、`shoemodel-v1`、`wanx-poster-generation-v1` | • T2V/I2V：`wan2.7-text2video`、`pixverse/pixverse-c1-t2v`、`kling/kling-v3-video-generation`<br>• R2V：`wan2.7-r2v-2026-06-12`、`vidu/viduq3-ad_reference2video`<br>• 人像驱动：`emo-v1`、`liveportrait`、`videoretalk` | • `Tripo/Tripo-H3.1`（高精度，≤200万面，支持 `geometry_quality: "ultra"`）<br>• `Tripo/Tripo-P1.0`（快速专业级，≤2万面） |
| **API 端点（推荐）** | 同步（新模型）：<br>`/api/v1/services/aigc/multimodal-generation/generation`<br><br>异步（主流）：<br>`/text2image/image-synthesis`（T2I）<br>`/image2image/image-synthesis`（I2I）<br>`/background-generation/generation`（背景） | 统一主路径（万相2.7+）：<br>`/api/v1/services/aigc/video-generation/video-synthesis`<br><br>部分旧模型独立路径：<br>`/api/v1/services/aigc/image2video/video-synthesis`（如 wan2.2） | 固定路径（北京地域限定）：<br>`/api/v1/services/aigc/video-generation/3d-generation`<br>⚠️ 注意：路径名含 `video-generation` 为历史兼容命名，实际为3D专属 |
| **调用模式** | • **混合模式**：`wan2.6-t2i`/`qwen-image-3.0-pro` 支持同步；多数模型（如 `kling`/`wanx`）强制异步<br>• 异步需轮询 `/api/v1/tasks/{task_id}` | • **强制异步**：所有模型均需两步调用（创建任务 → 轮询状态）<br>• 任务ID有效期24小时<br>• SDK已封装 `generate_video()` 封装异步流程 | • **强制异步**：无同步选项<br>• 必须携带 `X-DashScope-Async: enable`，否则直接报错<br>• 任务ID有效期24小时，轮询建议间隔 ≥15秒 |
| **计费方式** | • 按**成功生成的图片张数**计费（免费额度500张/90天）<br>• 商业化模型单价示例：`wanx-v1` 0.16元/张<br>• 免费模型（如 `wanx-x-painting`）额度用尽即停用，不支持付费续订 | • 按**成功生成的视频秒数**或**任务次数**计费（因模型而异）<br>• 人像类模型（如 `emo-v1`）按“处理时长秒数”计费（免费额度1800秒/月）<br>• T2V/I2V类通常按“单次任务”计费，与输出时长正相关 | • 按**单次成功任务**计费（无论文生/图生/多图生）<br>• 当前未开放免费额度，全部按量付费<br>• `Tripo-H3.1` 与 `Tripo-P1.0` 单价不同，高面数模型费用更高 |
| **地域与密钥约束** | • **强绑定**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域拥有独立API Key与Endpoint<br>• 跨地域调用必然失败（鉴权/路由错误） | • **强绑定**：同图像API，地域、Key、Endpoint必须严格一致<br>• 人像类模型并发限制更严（常限1个运行中任务） | • **唯一地域**：**仅支持华北2（北京）**<br>• API Key、WorkspaceId、Endpoint必须全部为北京地域配置<br>• 其他地域URL/Key调用直接返回404或InvalidApiKey |
| **典型场景** | • 电商海报批量生成（`wanx-poster-generation-v1`）<br>• AI设计稿辅助（`qwen-image-3.0-pro` 多轮编辑）<br>• 商品图智能换背景/擦除水印<br>• 个性化头像/壁纸生成 | • 短视频营销素材生成（`wan2.7-text2video` 多镜头叙事）<br>• 产品演示动画（`pixverse/pixverse-c1-it2v` 首帧驱动）<br>• 数字人直播/课程播报（`liveportrait` + `videoretalk`）<br>• 广告创意脚本可视化（`viduq3-ad_reference2video`） | • 工业设计原型快速建模（单图→3D）<br>• 游戏资产生成（文生低模+手动精修）<br>• AR/VR内容准备（PBR GLB直接导入引擎）<br>• 电商3D商品展示（多视角图→带材质3D模型） |

## 各方案适用场景建议

- **选择 Image Generation 当且仅当**：  
  ✅ 需求聚焦于**静态视觉内容**，如营销图、设计稿、头像、图标、海报；  
  ✅ 对生成速度敏感（部分模型支持毫秒级同步响应）；  
  ✅ 输入简单（纯文本或单张图），无需时间维度建模；  
  ❌ 不适用于需表达运动、时序逻辑、空间结构或交互反馈的场景。

- **选择 Video Generation 当且仅当**：  
  ✅ 核心诉求是**动态表达与时间叙事**，如短视频、教学动画、数字人播报、广告片；  
  ✅ 需要融合多模态输入（视频+音频、图像+动作指令、多帧参考）；  
  ✅ 接受10秒–数分钟的端到端延迟（[异步任务](../concepts/async-task.md)典型耗时）；  
  ❌ 不适用于对首帧精度要求极高但无需后续帧的场景（此时应优先用Image Generation生成关键帧）。

- **选择 3D Generation 当且仅当**：  
  ✅ 目标是生成**可交互、可渲染、可导入3D引擎**的空间模型（GLB格式）；  
  ✅ 输入具备明确几何线索（如正交多视角图）或强语义描述（如“带镂空雕花的青铜鼎”）；  
  ✅ 应用场景涉及AR/VR、游戏开发、工业仿真、3D电商等空间计算领域；  
  ❌ 不适用于2D平面设计、UI动效、GIF制作等非三维需求；❌ 不支持跨地域部署，北京地域为硬性前提。

## 面向开发者的选型决策指南

1. **先验判断模态本质**：  
   明确业务输出是否必须为**静态图**（→ Image）、**连续帧序列**（→ Video）、或**带拓扑与材质的三维网格**（→ 3D）。三者不可降级替代——用Video生成“伪3D旋转效果”无法替代真正可交互的GLB模型；用Image生成“多角度切片”无法满足Unity实时渲染需求。

2. **评估输入数据完备性**：  
   - 若仅有文本描述 → 三者均支持，但3D对[prompt](../guides/prompt.md)几何语义要求更高（推荐搭配Tripo官方Prompt Engineering指南）；  
   - 若有单张产品图 → Image（背景替换）或 3D（单图重建）可选，需权衡精度（3D需高质量正视图）与成本（3D单价显著高于单图生成）；  
   - 若有4张标准视角图 → **3D为唯一合理选择**；  
   - 若有视频片段+音频 → **Video为必选路径**（如口型同步、动作迁移）。

3. **校验基础设施约束**：  
   - 检查目标地域是否开通对应模型（尤其3D仅限北京）；  
   - 确认API Key已绑定正确地域，避免跨域调试失败；  
   - 高并发场景下，注意Video/3D的人像类模型常有**单任务串行限制**，需设计队列系统；Image Generation虽支持更高QPS，但需自行实现失败重试与结果去重。

4. **成本与体验平衡**：  
   - 免费额度策略差异大：Image有通用额度，Video按模型分额度，3D暂无免费层；  
   - 对延迟敏感应用（如实时设计工具），优先选用支持同步的Image模型（`qwen-image-3.0-pro`）；  
   - 对质量敏感应用（如工业设计），务必选用`Tripo-H3.1`而非`P1.0`，并启用`geometry_quality: "ultra"`。

5. **技术栈集成建议**：  
   - 统一使用 **DashScope SDK**（最新版）管理[异步任务](../concepts/async-task.md)生命周期（自动轮询、超时控制、回调注册），避免手写轮询逻辑；  
   - 所有API均需严格校验响应中的 `status` 字段（`SUCCEEDED`/`FAILED`/`UNKNOWN`），禁止依赖HTTP状态码判断业务成功；  
   - 输出URL均为临时链接（2–24小时有效期），务必在收到后立即下载或转存

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


