# 多模态生成能力对比：Image Generation vs Video Generation API vs 3D Generation

本页面旨在为开发者提供百炼平台三大核心多模态生成能力的系统性对比，涵盖图像生成（Image Generation）、视频生成（Video Generation API）与三维模型生成（3D Generation）在技术架构、使用方式、能力边界及工程实践层面的关键差异。随着AIGC应用场景从静态内容向动态表达与空间交互演进，准确理解各模态生成服务的定位、约束与协同潜力，是构建高质量AI原生应用（如电商可视化、数字人内容工厂、游戏资产管线、工业设计辅助等）的技术前提。

---

## 关键维度对比

| 维度 | Image Generation | Video Generation API | 3D Generation |
|------|------------------|----------------------|----------------|
| **核心任务类型** | 文生图（T2I）、图生图（I2I）、图像编辑（局部重绘/擦除/扩图/风格迁移等） | 文生视频（T2V）、图生视频（I2V）、首尾帧生成、参考生视频（R2V）、数字人驱动、口型同步、视频后处理（超分/风格重绘） | 文生3D、单图生3D、四视角多图生3D（前/左/后/右） |
| **输入格式** | • 文本提示（`prompt` 或 `messages[].content[].text`）<br>• 图像URL（支持最多14张参考图，含 `mask_image_url` 用于局部操作）<br>• 混合文本+图像输入（如 `vidu/vidu-image_reference2image`） | • 纯文本（`input.prompt`）<br>• 单图/多图URL（`media` 数组，支持 `first_frame`/`last_frame`/`reference_image` 等类型）<br>• 音频URL（数字人场景需 `audio_url` + `image_url`）<br>• 视频URL（部分编辑模型） | • 纯文本（`input.prompt`）<br>• 单图URL（`input.image`）<br>• 四元素数组（`input.images`，按「前-左-后-右」顺序，空视角用 `{}` 占位）<br>• **三者互斥，不可混用** |
| **输出格式** | • Base64 编码图像（同步调用）<br>• 公网可访问 URL（异步调用，有效期24小时）<br>• 支持 JPG/PNG/WEBP/BMP 格式 | • 视频 URL（MP4/H.264，有效期24小时）<br>• 预览图 URL（`output.preview_url`，WebP，部分模型）<br>• 元数据（时长、分辨率、帧率等） | • PBR材质模型 URL（GLB格式，含贴图，`pbr_model_url`，有效期2小时）<br>• 无贴图基础网格 URL（`base_model_url`，需显式配置）<br>• 渲染预览图 URL（WebP，`rendered_image_url`，有效期2小时） |
| **支持模型（典型代表）** | `wan2.6-t2i`, `qwen-image-3.0-pro`, `kling/kling-v3-image-generation`, `wanx-x-painting`, `shoemodel-v1` 等（共20+专用模型） | `wan2.7-t2v`, `pixverse/pixverse-c1-t2v`, `vidu/viduq3-turbo_text2video`, `emo`, `liveportrait`, `animateanyone` 等（覆盖生成+驱动+后处理） | `Tripo/Tripo-H3.1`（高精度，≤200万面），`Tripo/Tripo-P1.0`（快速，≤2万面） |
| **API 调用模式** | • **同步 & 异步双模支持**：<br> ✓ `wan2.6-t2i`/`qwen-image-3.0-pro` 等新协议模型支持同步返回<br> ✗ `wanx-sketch-to-image-lite`/`wanx-x-painting` 等强制异步 | • **强制异步**：<br> 所有模型均需 `X-DashScope-Async: enable`，两步流程（提交任务 → 轮询 `task_id`）<br> `task_id` 有效期24小时 | • **强制异步**：<br> 必须携带 `X-DashScope-Async: enable`<br> `task_id` 有效期24小时，结果资源（URL）仅保留2小时 |
| **地域支持** | • 华北2（北京）、新加坡、美国（弗吉尼亚）<br>• **地域隔离严格**：API Key、Endpoint、Workspace ID 必须同地域 | • 华北2（北京）、新加坡、美国（弗吉尼亚）<br>• **地域强绑定**：模型开通、API Key、Endpoint URL 必须完全一致，跨地域调用必失败 | • **仅限华北2（北京）**：<br> 控制台入口、API Key、Endpoint 均锁定北京地域<br> 其他地域调用直接报错，无降级或兼容路径 |
| **计费方式** | • 按生成图片张数计费（如 1 张 = 1 [Token](../concepts/token.md)）<br>• 多数模型提供 **500 张/90天免费额度**<br>• 部分垂直模型（如 `wanx-x-painting`）**额度用尽即停用，不支持付费续订** | • 按视频生成任务计费（1次成功任务 = 1 [Token](../concepts/token.md)）<br>• 按分辨率/时长/模型等级分级定价（如 `720P` vs `4K`，3s vs 5s）<br>• 免费额度较少（通常 10–50 次/月），**全部支持付费扩容** | • 按任务成功次数计费（1次 = 1 [Token](../concepts/token.md)）<br>• `H3.1`（高面数）单价高于 `P1.0`（快速版）<br>• **无公开免费额度**，需预充值或开通后按量扣费 |
| **典型场景** | • 电商商品图生成与背景替换<br>• 社媒配图/营销海报批量制作<br>• UI设计稿转真实效果图<br>• 人像精修与风格化（试穿/重绘）<br>• 涂鸦→成品图（Sketch-to-Image） | • 短视频内容自动化生产（广告/教程/资讯）<br>• 数字人播报/虚拟主播驱动<br>• 产品演示动画（图→3s动态展示）<br>• 口型同步配音（VideoRetalk）<br>• 动作复刻（AnimateAnyone） | • 工业/消费电子产品3D建模（文生/图生）<br>• 游戏资产快速原型（角色/道具）<br>• AR/VR内容管线接入（GLB直输引擎）<br>• 电商3D商品展示（替代传统摄影） |

---

## 各方案适用场景建议

### ✅ 选择 Image Generation 当：
- 需要**高吞吐、低延迟**交付静态视觉内容（如每日千张营销图）；
- 任务以**精细编辑**为核心（局部重绘、去水印、超分、风格迁移）；
- 输入源为**文本描述或单张参考图**，且无需时间维度表达；
- 对**成本敏感**，可充分利用免费额度（500张/90天）；
- 开发团队偏好**同步调用简化逻辑**（推荐 `qwen-image-3.0-pro` 或 `z-image-turbo`）。

### ✅ 选择 Video Generation API 当：
- 应用需**动态叙事能力**（如短视频脚本→成片、产品功能演示动画）；
- 涉及**人物驱动类需求**（数字人播报、唱演、口型同步、动作模仿）；
- 输入具备**多模态组合特征**（图+文+音，或首帧+末帧+提示词）；
- 接受**异步工作流**并已集成轮询/回调机制；
- 场景对**时长（3–5秒）与画质（720P–4K）有明确分级要求**，且预算支持按质付费。

### ✅ 选择 3D Generation 当：
- 目标是生成**可导入Unity/Unreal/Blender的标准化3D资产**（GLB with PBR）；
- 输入为**结构化视角图像**（四视图）或**精确文本描述**（如“不锈钢圆柱形保温杯，带硅胶防滑环”）；
- 业务链路需**与CAD/AR/电商平台深度集成**（如自动生成SKU 3D模型）；
- **仅在北京地域部署服务**，且能接受2小时资源有效期（需及时下载）；
- 对模型面数有明确分级需求：`P1.0`（快速验证） vs `H3.1`（生产级精度）。

---

## 技术选型参考（面向开发者）

| 选型关注点 | 推荐方案 | 关键依据 |
|------------|----------|----------|
| **开发效率优先** | Image Generation（同步模式） | 单次HTTP请求即得Base64，无轮询/状态管理开销；SDK封装成熟（DashScope Python/Java） |
| **跨地域部署需求** | Image Generation 或 Video Generation API | 二者均支持北京/新加坡/美东三地；3D Generation 仅限北京，若需全球服务需额外架构适配 |
| **输入灵活性最高** | Video Generation API | 支持文本+图像+音频+视频多模态混合输入，且 `media` 字段类型丰富（`first_frame`/`reference_image`/`audio_url`） |
| **输出可集成性最强** | 3D Generation | 原生输出标准GLB（含PBR材质），零改造对接主流渲染引擎与3D平台；Image/Video 输出需额外解码/转码 |
| **成本可控性最佳** | Image Generation | 免费额度覆盖中小规模应用；Video/3D均为纯按量计费，无缓冲期 |
| **长周期任务稳定性** | Video Generation API 或 3D Generation | 二者均强制异步，`task_id` 24小时有效，适合后台批处理；Image Generation 的[异步任务](../concepts/asynchronous-task.md)同样24小时，但同步模式无此保障 |
| **未来扩展性考量** | Video Generation API | 生态最活跃（持续新增数字人/动作模型），且与Image Generation存在天然协同（如“先图生图→再图生视频”流水线） |

> **重要提醒**：  
> - 所有服务均**强依赖地域一致性**——务必校验 API Key、Workspace ID、Endpoint 三者地域标签完全匹配；  
> - **[异步任务](../concepts/asynchronous-task.md)务必实现幂等轮询或启用回调通知**（[异步任务回调文档](https://help.aliyun.com/zh/model-studio/async-task-api)），避免因网络抖动丢失结果；  
> - 图像/视频/3D 的输入URL必须**公网可访问、HTTPS、无鉴权**；内网OSS链接需生成临时公链；  
> - 3D模型生成对输入图像质量敏感，**多图生3D强烈建议使用专业四视图拍摄**，非正交视角将显著降低重建精度。

---  
*最后更新：2024年6月 | 百炼平台技术文档中心*

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


