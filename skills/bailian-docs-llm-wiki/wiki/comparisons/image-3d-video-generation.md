# [多模态](../concepts/multimodal.md)生成能力对比：图像、3D 与视频生成 API

本文档面向百炼平台开发者，系统对比图像生成、3D 生成与视频生成三类核心[多模态](../concepts/multimodal.md) API 的技术特性、使用约束与适用边界，旨在为实际业务场景下的模型选型、架构设计与成本规划提供客观、可落地的技术参考。随着 AIGC 应用从静态内容向动态、空间化演进，理解各模态生成能力的输入输出范式、异步/同步行为、地域依赖及计费逻辑，已成为高效集成与规模化部署的关键前提。

## 关键维度对比表

| 维度 | 图像生成（Image Generation） | 3D 生成（3D Generation） | 视频生成（Video Generation） |
|------|------------------------------|-----------------------------|-------------------------------|
| **核心能力** | 文生图（T2I）、图生图（I2I）、局部编辑、背景生成、风格迁移、图像翻译、实例分割等全栈图像创作与处理 | 文生3D、单图生3D、多图生3D；支持带 PBR 材质贴图与无贴图两种输出形式 | 文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、动作迁移、口型同步、风格重绘、超分等动态内容生成 |
| **输入格式** | - 文生图：`{"messages": [{"role":"user","content":[{"text":"prompt"}]}]}` 或 `{"prompt":"..."}`<br>- 图生图/编辑：`{"messages": [{"role":"user","content":[{"image":"url"},{"text":"instruction"}]}]}`<br>- 工具类（擦除/分割）：`{"image_url":"..."}` | 三者**互斥**：<br>- 文生3D：`{"input": {"prompt": "..."}}`（≤1024 字符）<br>- 单图生3D：`{"input": {"image": "url"}}`（JPEG/PNG，20–6000px，≤20MB）<br>- 多图生3D：`{"input": {"images": [{"url":"..."},{},{},{"url":"..."}]}}`（固定长度4，空位填 `{}`） | 结构化 `input` 对象：<br>- 文生视频：`{"input": {"prompt": "..."}}`<br>- 图生视频：`{"input": {"media": [{"type":"image_url","url":"..."}], "prompt":"..."}}`<br>- 首尾帧：`{"input": {"media": [{"type":"first_frame","url":"..."},{"type":"last_frame","url":"..."}]}}`<br>- 参考生视频：`{"input": {"media": [{"type":"image_url","url":"..."},{"type":"video_url","url":"..."}]}}`<br>- 视频编辑：`{"input": {"video_url": "..."}}` |
| **输出格式** | 同步返回：Base64 编码图片或 JSON 中含 `output.results[0].url`（有效期 24 小时）<br>异步返回：`task_id` → 轮询得 `output.results[].url`（WebP/JPEG/PNG，24 小时有效） | **纯异步**：`task_id` → 轮询得 `output.results`，含：<br>- `pbr_model_url`（GLB，含材质贴图，2 小时有效）<br>- `base_model_url`（GLB，无贴图，仅当 `texture=false && pbr=false` 时返回）<br>- `rendered_image_url`（WebP 预览图，2 小时有效） | **纯异步**：`task_id` → 轮询得 `output.video_url`（MP4/H.264，24 小时有效）；部分模型额外返回 `output.audio_url`、`output.thumbnail_url` 等 |
| **支持模型（代表）** | - 通用：`qwen-image-3.0-pro`（512×512–2048×2048 自由分辨率）、`wan2.7-image-pro`（支持 4K）<br>- 垂直：`virtualmodel-v2`（虚拟模特）、`shoemodel-v1`（鞋靴试穿）、`FaceChain`（人像写真）<br>- 工具：`wanx-x-painting`（局部重绘）、`image-erase-completion`（擦除补全）、`qwen-mt-image`（图像翻译） | - `Tripo/Tripo-H3.1`（高精度，≤200 万面，支持 `geometry_quality: "ultra"`）<br>- `Tripo/Tripo-P1.0`（快速生成，≤2 万面） | - 通用：`wan3.0-video`（最长 30 秒）、`wan2.7-*`、`pixverse/pixverse-c1-t2v`、`kling`<br>- 人像驱动：`emo-v1`（表情驱动）、`liveportrait`（灵动人像）、`videoretalk`（声动口型）<br>- 编辑增强：`video-style-transform`、`pixverse/pixverse-upscale`、`pixverse/pixverse-lipsync` |
| **API 端点（典型）** | - 同步：`/multimodal-generation/generation`（如 `qwen-image-3.0-pro`）<br>- 异步：`/image-synthesis` 或 `/generation`（如 `image-out-painting`）<br>📍 地域强绑定（北京/新加坡/弗吉尼亚等） | `/api/v1/services/aigc/video-generation/3d-generation`<br>✅ **仅支持华北2（北京）地域**，URL 必须匹配 WorkspaceId + `cn-beijing` | `/api/v1/services/aigc/video-generation/video-synthesis`（`wan2.7+`）<br>`/api/v1/services/aigc/image2video/video-synthesis`（旧版 `wan2.2-*`）<br>📍 支持多地域（北京/新加坡/弗吉尼亚/法兰克福/东京），但必须严格同地域 |
| **调用模式** | **混合模式**：<br>- 高性能模型（`qwen-image-3.0-pro`, `wan2.7-image-pro`）→ **同步响应**（毫秒级）<br>- 耗时工具类（`image-out-painting`, `wanx-v1`）→ **异步任务**（需轮询） | **强制异步**：<br>创建任务 → 轮询 `task_id` → 获取结果<br>✅ `task_id` 有效期 24 小时；建议轮询间隔 ≥15 秒 | **强制异步**：<br>创建任务 → 轮询 `task_id` → 获取结果<br>✅ `task_id` 有效期 24 小时；建议轮询间隔 ≥3 秒（部分模型限流敏感） |
| **计费方式** | - 按**成功生成的图片张数**计费（`n` 参数值）<br>- 免费额度模型（如 `wanx-virtualmodel`）额度用尽即停用，**不支持付费开通**<br>- 水印开关（`watermark`）不影响计费 | - 按**成功生成的 3D 模型任务次数**计费<br>- `pbr=true` 与 `pbr=false` 计费相同（无贴图模型仍计 1 次）<br>- `geometry_quality: "ultra"` 不额外加价 | - 按**成功生成的视频任务次数** + **视频时长（秒）** 双维度计费（如 `wan3.0-video` 按秒计费）<br>- 人像驱动类（`emo-v1`, `liveportrait`）按**任务次**计费，与长度无关<br>- 风格重绘/超分等编辑类按**输入视频时长**计费 |
| **典型场景** | - 电商：商品图生成、模特换装、背景替换、海报设计<br>- 设计：创意草图转高清、风格迁移、多尺寸适配<br>- 内容：社交媒体配图、AI 写真、多语种图文翻译 | - 工业：产品原型快速建模、零部件可视化<br>- 游戏/元宇宙：角色/道具 3D 资产生成、AR 商品预览<br>- 教育：教学模型三维重建、建筑结构可视化 | - 营销：短视频脚本转视频、广告片自动剪辑与风格化<br>- 社交：图文转短视频、表情包生成、数字人播报<br>- 影视：分镜预演、动作参考生成、老片修复与增强 |

## 各方案适用场景建议

### ✅ 图像生成 —— 优先选择当需求满足以下任一条件：
- **低延迟要求**：需毫秒级响应（如实时设计助手、电商详情页动态图生成），应选用 `qwen-image-3.0-pro` 或 `wan2.7-image-pro` 等同步模型；
- **精细控制需求强**：需局部重绘、精确擦除、实例分割、跨语言图文排版保留等，应选用专用工具模型（`wanx-x-painting`, `qwen-mt-image`, `image-instance-segmentation`）；
- **垂直业务闭环**：明确聚焦虚拟试衣、鞋靴展示、海报生成等场景，可直接调用 `aitryon-plus`, `shoemodel-v1`, `wanx-poster-generation-v1`（注意：部分免费模型已不支持付费扩容，新项目建议评估 `qwen-image-edit` 替代方案）；
- **成本敏感且批量小**：单次生成 1–4 张图为主，同步调用免去轮询开销，降低服务复杂度。

### ✅ 3D 生成 —— 优先选择当需求满足以下全部条件：
- **目标为三维资产交付**：最终产物需导入 Unity/Unreal/Blender 或用于 WebGL 渲染，且对几何精度（面数）、PBR 材质完整性有明确要求；
- **输入资源受限但可控**：能提供高质量单视角图（如白底产品图）或标准四视图（前/左/后/右），且可确保 URL 公网可达；
- **地域可锁定为华北2（北京）**：业务架构允许且已部署于北京地域，或可接受跨地域数据传输（因仅北京支持）；
- **接受中等延迟（1–5 分钟）与异步流程**：适用于后台批处理、用户提交后邮件通知等非实时交互场景。

### ✅ 视频生成 —— 优先选择当需求满足以下任一条件：
- **内容动态性为核心诉求**：需表达时间维度信息（运动、变化、对话、节奏），如营销短视频、数字人播报、教学动画；
- **[多模态](../concepts/multimodal.md)输入融合**：需同时利用文本意图 + 首帧图像 + 参考视频动作等组合输入，实现高保真动作迁移或风格复刻；
- **专业后期增强需求**：需对已有视频进行超分、风格转换、口型同步等增强操作，而非从零生成；
- **支持多地域部署**：业务面向全球用户，需在新加坡、弗吉尼亚等地就近调用，避免跨地域延迟与合规风险。

## 技术选型决策指南（致开发者）

| 选型问题 | 推荐动作 | 关键依据 |
|----------|-----------|-----------|
| **我的应用需要“所见即所得”的实时图像反馈（如设计插件）？** | ✅ 选用 `qwen-image-3.0-pro` 或 `wan2.7-image-pro` 同步接口<br>❌ 避免 `image-out-painting` 等异步模型 | 同步响应平均耗时 <800ms，无需维护轮询状态机；支持自由分辨率适配不同画布 |
| **我要为电商平台生成带材质的 3D 商品模型，但团队只有一张主图？** | ✅ 选用 `Tripo/Tripo-P1.0`（快速验证）→ 后续升级 `Tripo-H3.1`（高精度）<br>❌ 不要尝试用视频生成或图像生成“模拟”3D | 单图生3D 是唯一原生支持路径；`pbr=true` 直接输出带贴图 GLB，可直连 Three.js 渲染 |
| **我需要将公众号图文自动转为 60 秒短视频并配数字人口播？** | ✅ 组合调用：<br>1. `wan3.0-video`（文生视频，60 秒）→ 获取基础视频<br>2. `emo-v1` + `emo-detect-v1`（驱动数字人）→ 生成口型同步视频<br>3. `video-style-transform`（统一视觉风格） | 视频生成 API 原生支持“文本+数字人身份”联合输入；各模块解耦，便于灰度发布与效果迭代 |
| **我的服务部署在新加坡，但想调用 3D 生成？** | ⚠️ **不可行**。必须迁移至华北2（北京）地域，或改用客户端离线 3D 重建方案 | 3D 生成 API 明确限定仅 `cn-beijing` 地域可用，其他

## 被对比主题页

- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)


