# 多模态生成 API 对比：图像生成 vs 视频生成 vs 3D 生成

本文旨在为开发者提供百炼平台三大核心多模态生成能力（图像、视频、3D）的系统性对比，帮助技术团队基于业务需求、技术约束与成本效益，快速完成 API 选型决策。随着 AIGC 应用从静态内容向动态表达与空间交互演进，理解各模态在输入范式、输出形态、调用机制及工程适配上的差异，已成为构建高质量生成服务的关键前提。

---

## 关键维度对比表

| 维度 | 图像生成 | 视频生成 | 3D 生成 |
|------|----------|----------|---------|
| **核心能力定位** | 静态视觉内容创建与编辑（文生图、图生图、局部重绘、风格迁移等） | 动态时序内容生成（文生视频、图生视频、参考生视频、动作迁移、口型同步等） | 空间结构建模（文本/单图/多图→可渲染 GLB 模型，支持 PBR 材质） |
| **输入格式** | • 文本提示（`messages` 或 `prompt`）<br>• 输入图像 URL（仅编辑类模型）<br>• 支持图文混排（`messages` 中含 `image` 元素） | • 纯文本（T2V）<br>• 单张/首帧图像 URL（I2V）<br>• 首尾帧图像 URL（KF2V）<br>• 多图/音视频混合参考（R2V）<br>• 原始视频 URL（编辑类） | • 纯文本（`prompt`）<br>• 单张图像 URL（`image`）<br>• 四视角图像数组（`images`，顺序：前/左/后/右，空位用 `{}` 占位）<br>（三者**互斥**，不可共存） |
| **输出格式** | • PNG/JPEG 图片 URL（HTTP 同步返回或异步任务结果中获取）<br>• 支持多张并行生成（`n=1–9`） | • MP4 视频 URL（异步返回，含水印/音频可选）<br>• 输出时长通常为 3–5 秒<br>• 部分模型支持预览图（`preview_url`） | • GLB 格式 3D 模型 URL（`pbr_model_url` 或 `base_model_url`）<br>• 渲染预览图 URL（`rendered_image_url`）<br>• 所有 URL **有效期仅 2 小时**，需及时下载 |
| **支持模型（代表性）** | • 万相系列：`wan2.6-t2i`（推荐 V2）、`wan2.5-i2i-preview`<br>• 千问系列：`qwen-image-3.0-pro`、`qwen-image-edit-max`<br>• 轻量专用：`z-image-turbo`、`kling/kling-v3-omni-image-generation`、`shoemodel-v1` | • 文生视频：`wan2.7-t2v-*`、`kling/kling-v3-*`、`pixverse/pixverse-*-t2v`、`vidu/viduq3-*-text2video`<br>• 图生视频：`happyhorse-1.1-i2v`、`wan2.7-*it2v`、`pixverse-*kf2v`<br>• 参考/编辑：`wan2.7-r2v-*`、`pixverse/pixverse-upscale`、`pixverse/pixverse-lipsync` | • `Tripo/Tripo-P1.0`（专业版，≤2 万面，速度快）<br>• `Tripo/Tripo-H3.1`（高精度版，≤200 万面，支持 `ultra` 几何质量） |
| **API 端点（典型）** | • 同步：`/api/v1/services/aigc/multimodal-generation/generation`（如 `wan2.6-t2i`）<br>• 异步：`/api/v1/services/aigc/image2image/image-synthesis`（如 `wan2.5-i2i-preview`） | • 主路径：`/api/v1/services/aigc/video-generation/video-synthesis`<br>• 特殊路径：`/api/v1/services/aigc/image2video/video-synthesis`（仅 `wan2.2-kf2v-fla`、`wan2.2-animate-move` 等旧模型） | • 统一路径：<br>`/api/v1/services/aigc/video-generation/3d-generation`<br>（注意：路径名含 `video-generation`，属历史命名，实际为 3D 专属） |
| **调用模式** | • **混合支持**：部分模型（`wan2.6-t2i`, `z-image-turbo`）支持 HTTP 同步调用；多数编辑类模型强制异步<br>• 同步响应快（毫秒级），异步需轮询（`GET /tasks/{task_id}`） | • **强制异步**：所有模型均需 `X-DashScope-Async: enable`，创建任务后轮询状态<br>• `task_id` 有效期 24 小时 | • **强制异步**：必须启用 `X-DashScope-Async: enable`，无同步选项<br>• `task_id` 有效期 24 小时，结果 URL 有效期仅 2 小时 |
| **计费方式** | • 按成功生成图片张数计费（失败不计费）<br>• 免费额度：多数模型提供 500 张/90 天（主账号与 RAM 子账号共享）<br>• QPS/RPS 限流：主账号与子账号共用（常见 2 QPS） | • 按成功生成视频条数计费（失败不计费）<br>• 免费额度较少或未开放（以控制台开通页为准）<br>• 各模型独立限流：如 `liveportrait` 同时处理中任务数上限为 1 | • 按成功生成 3D 模型个数计费（失败不计费）<br>• 当前暂无公开免费额度<br>• RPS 查询限流：轮询接口上限 20 RPS，建议搭配异步回调避免高频轮询 |
| **地域与域名约束** | • 严格绑定：API Key、Endpoint、Workspace ID 必须同地域（北京/新加坡/弗吉尼亚/法兰克福）<br>• 推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`） | • 同上，强地域一致性要求<br>• 跨地域调用必然鉴权失败或 404 | • **仅支持华北2（北京）地域**<br>• API Key、Endpoint、Workspace ID 必须为北京地域<br>• 其他地域 URL 不可用 |
| **典型场景** | • 电商商品图生成与背景替换<br>• 社媒内容快速配图与风格化<br>• AI 试衣、虚拟模特、人像写真<br>• 设计稿扩图与局部修改 | • 短视频创意脚本可视化（T2V）<br>• 产品展示动画（I2V + 超清）<br>• 数字人播报与口型驱动（S2V/LipSync）<br>• 舞蹈复刻、动作迁移、角色融合（R2V） | • 工业设计原型快速建模（文→3D）<br>• 电商商品 3D 展示（单图→GLB）<br>• AR/VR 内容资产生成（多视角图→PBR 模型）<br>• 游戏资产辅助创作 |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「高吞吐、低延迟、强可控」的视觉内容生产
- **推荐场景**：  
  - 需批量生成高质量静态图（如千张商品图、海报素材）且对首屏响应时间敏感 → 选用支持**同步调用**的 `wan2.6-t2i` 或 `z-image-turbo`。  
  - 需精准编辑已有图像（擦除补全、风格重绘、AI试衣）→ 优先选择 `qwen-image-edit-max` 或垂直专用模型（`shoemodel-v1`, `facechain`）。  
  - 快速验证或轻量应用 → 利用免费额度体验 `wanx-virtualmodel`、`image-erase-completion` 等工具。  
- **避坑提示**：避免混用跨地域 API Key；编辑类模型务必确保输入图公网可访问且 URL 无中文字符。

### ✅ 视频生成 —— 适合「叙事性、时序性、角色驱动」的动态内容构建
- **推荐场景**：  
  - 从文案自动生成分镜短视频 → 使用 `wan2.7-t2v-*`（天然支持多镜头描述）或 `kling/kling-v3-omni-video`（支持音频+多风格）。  
  - 将静态产品图转化为旋转展示视频 → 选用 `happyhorse-1.1-i2v` 或 `pixverse/*it2v`。  
  - 构建数字人播报系统 → 组合 `wan2.2-s2v`（语音驱动） + `videoretalk`（口型替换），注意需先调用 `detect` 模型校验输入合规性。  
- **避坑提示**：严格核对模型文档中的 API 路径（`video-generation` vs `image2video`）；人物类模型务必执行前置检测，否则任务直接失败。

### ✅ 3D 生成 —— 适合「空间建模、资产交付、跨平台复用」的专业级三维内容生产
- **推荐场景**：  
  - 快速将设计草图/实物照片转为可嵌入 Web/Unity/Unreal 的 GLB 模型 → 使用 `Tripo/Tripo-P1.0`（平衡速度与质量）。  
  - 高精度工业零件或游戏角色建模 → 选用 `Tripo/Tripo-H3.1` 并设置 `geometry_quality: ultra`。  
  - 需多角度一致建模 → 采集前/左/后/右四视角图（缺省视角用 `{}` 占位），调用多图生3D。  
- **避坑提示**：仅限北京地域；结果 URL 2 小时失效，务必在轮询成功后立即下载；输入 `prompt`/`image`/`images` 三者必须严格互斥。

---

## 开发者技术选型参考

| 选型维度 | 关键判断依据 | 推荐行动 |
|----------|--------------|----------|
| **调用实时性要求** | • 需 <1s 响应 → 选支持同步的图像模型（`wan2.6-t2i`）<br>• 可接受 5–60s 延迟 → 视频/3D 均适用 | 优先查阅各模型文档中 “调用方式” 章节，确认是否标注 “支持同步调用” |
| **输入数据形态** | • 纯文本 → 图像/视频/3D 均支持<br>• 单图 → 图像编辑、图生视频、单图生3D<br>• 多图/视频/音频 → 视频生成（R2V/I2V）为主，3D 仅支持四视角图 | 根据原始数据源选择最小改造路径：例如已有产品图 → 直接走 I2V 或 单图生3D，而非强行转文本再 T2V/T23D |
| **输出交付目标** | • 嵌入网页/APP 展示 → 图像（PNG/JPEG）、视频（MP4）、3D（GLB）均可<br>• 需后续渲染/编辑 → 3D（GLB 含材质）优势显著；视频需注意水印与分辨率适配 | 若需 Unity/Blender 进一步加工，3D 生成是唯一原生支持 PBR 材质导出的方案 |
| **成本与规模预期** | • 小规模试用 → 图像生成免费额度充足<br>• 中大规模商用 → 对比各模型单位成本（元/张/条/个），关注高并发限流阈值 | 在百炼控制台开通模型前，查看“资费与限流”章节，评估 QPS/RPS 是否满足峰值需求（如直播场景需高并发视频生成） |
| **工程集成复杂度** | • 同步调用：代码简洁，错误处理简单<br>• 异步调用：需实现任务创建 + 轮询/回调 + 结果持久化逻辑 | 新项目建议统一采用**异步回调**（Webhook）替代轮询，降低服务端资源消耗；百炼平台已提供标准异步回调配置入口 |

> **最后建议**：对于复合型应用（如“文生图 → 图生视频 → 视频抽帧 → 单图生3D”），建议分

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


