# 图像生成与视频生成对比

为帮助开发者快速理解百炼平台中图像生成与视频生成两类能力的差异，明确技术选型边界与使用约束，本文从输入输出、模型支持、调用方式、计费策略等核心维度进行系统性对比。该对比基于当前（2024年Q3）平台正式发布的 API 能力与文档规范，适用于新项目接入、存量系统迁移及多模态方案架构设计。

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） |
|------|------------------------------|------------------------------|
| **输入格式** | • 文生图：`input.prompt` 或 `input.messages`（含 text）<br>• 图生图/编辑：`input.messages` 数组（含 `{"text": "..."}` 和 `{"image": "url"}`），部分旧模型仍用 `input.ref_image`<br>• 图片 URL 需公网可访问、无中文路径、支持 HTTPS | • 文生视频（T2V）：`input.prompt` + 可选 `parameters.multi_shot`/分镜描述<br>• 图生视频（I2V）：`input.media`（首帧图 URL）或 `input.video_url`（短片）<br>• 参考生视频（R2V）：`input.media` 数组（多张参考图）<br>• 所有媒体 URL 必须 HTTPS、≥512×512（图）、≤10秒（视频） |
| **输出格式** | • 同步调用：直接返回 JSON，含 `output.results` 数组（每项含 `url`、`width`、`height`）<br>• 异步调用：轮询 `GET /api/v1/tasks/{task_id}`，响应含 `output.results`（单图或多图） | • 全部异步：轮询 `GET /api/v1/tasks/{task_id}`，响应含 `output.video_url`（H.264 MP4）、`output.duration`（秒）、`output.resolution`（如 `"1080P"`）<br>• 不返回帧序列或中间产物，仅最终视频文件 |
| **支持模型（主力）** | • 文生图：`qwen-image-2.0-pro`、`wan2.7-image-pro`、`z-image-turbo`、`vidu`<br>• 图像编辑：`qwen-image-edit-*`、`wanx-x-painting`、`virtualmodel-v2`<br>• 创意工具：`image-out-painting`、`wanx-background-generation-v2`、`aitryon-plus` | • 文生视频：`wan2.7-t2v-*`、`vidu/viduq3-*-text2video`、`kling/kling-v3-*-video-generation`、`pixverse/pixverse-*-t2v`<br>• 图/参考生视频：`wan2.7-i2v-*`、`vidu/viduq3-*-img2video`、`wan2.7-r2v-*`<br>• 数字人：`liveportrait`、`videoretalk`、`emo-v1` |
| **API 端点** | • **统一主入口**：<br>`POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`（推荐）<br>• 历史路径（部分模型）：<br>`POST /api/v1/services/aigc/text2image/image-synthesis` 等 | • **全量异步专用入口**：<br>`POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`<br>• 通用兼容地址（不推荐）：<br>`https://dashscope.aliyuncs.com/...`（北京）或 `https://dashscope-intl.aliyuncs.com/...`（国际） |
| **调用模式** | • **同步 & 异步混合**：<br>– 快速模型（如 `qwen-image-2.0-pro`、`wan2.6-t2i`）支持同步（<10s），可流式返回（需 `X-DashScope-Sse: enable`）<br>– 长耗时模型（如 `wanx-x-painting`、`image-out-painting`）强制异步 | • **强制异步**：<br>所有模型均需两步流程：① 创建任务获取 `task_id`；② 轮询 `GET /api/v1/tasks/{task_id}` 获取结果<br>• `task_id` 有效期严格为 **24 小时** |
| **计费方式** | • 免费额度：**500 张/账号/90天**（主账号与 RAM 子账号共享）<br>• 计费模型：<br>– 按成功生成图片计费（如 `wanx-v1`: 0.16元/张）<br>– 部分模型免费额度用尽即停用（无单价），如 `wanx-x-painting`、`shoemodel-v1`、`image-instance-segmentation` | • 免费额度：**100 秒视频生成时长/账号/90天**（按实际生成视频秒数累加）<br>• 计费模型：<br>– 按生成视频时长计费（如 `wan2.7-t2v`: 0.8元/秒，`vidu`: 1.2元/秒）<br>– 数字人模型按任务计费（如 `liveportrait`: 0.5元/次）<br>• 所有模型均无“免费额度外不可用”例外，超限后自动转计费 |
| **典型场景** | • 静态内容生产：电商主图、营销海报、AI头像、文字艺术（WordArt）、背景生成、商品试穿（鞋靴/服装）<br>• 图像增强：局部重绘、擦除补全、实例分割、风格迁移<br>• 快速原型：A/B测试图稿、UI素材生成、设计草图扩展 | • 动态内容生产：短视频广告、产品演示动画、分镜脚本可视化、数字人播报、虚拟主播口型同步<br>• 视频创作辅助：图转视频（I2V）、多图角色一致性视频（R2V）、自然语言分镜生成（万相2.7）<br>• 垂直应用：表情包生成（`emoji`）、唱演视频（`emo-v1`）、舞蹈驱动（`animate-anyone-gen2`） |

## 各方案适用场景建议

### ✅ 推荐选择图像生成当：
- 业务需求聚焦于**静态视觉资产**，如电商平台的商品图、社交媒体封面、APP图标、个性化头像；
- 对**响应延迟敏感**（如实时交互式设计工具），且任务平均耗时 < 8 秒，可优先选用 `qwen-image-2.0-pro` 或 `wan2.7-image-pro` 同步接口；
- 需要**精细控制像素级输出**（如 4K 渲染、文字精准识别、局部编辑掩码），图像模型在空间保真度上显著优于视频模型首帧；
- 成本结构以**固定次数/张数**为主，且月用量稳定在数百张内，可充分复用免费额度。

### ✅ 推荐选择视频生成当：
- 核心目标是**动态表达与时间叙事**，如短视频营销、教学动画、数字人直播、AI分镜预演；
- 接受**异步工作流**（任务创建 → 轮询 → 下载），并能妥善管理 `task_id` 生命周期与失败重试逻辑；
- 需要**跨帧一致性能力**（人物/物体/风格在多帧中稳定呈现），R2V 与 I2V 模型专为此优化，图像模型无法替代；
- 业务具备**视频时长可预测性**（如统一生成 5 秒广告），便于成本建模；若需高频、短时（<3秒）视频，需注意部分模型最低时长限制（如 `kling` 最小 3 秒）。

### ⚠️ 需谨慎评估或组合使用的场景：
- **“动效化静态图”需求**（如将海报转为带缩放/平移的短视频）：  
  → 不建议直接调用视频生成，应先用图像生成产出高质量源图，再通过视频编辑模型（如 `video-style-transform` 或 `wan2.2-animate-mix`）添加运镜效果，兼顾质量与成本。
  
- **高并发实时图像/视频混合服务**（如用户上传图→生成图→生成对应视频）：  
  → 必须分离调用链路：图像生成走同步路径（低延迟），视频生成走异步路径（解耦阻塞）；同时注意地域强绑定——图像与视频模型若部署在不同地域（如图在北京、视频在新加坡），需分别配置 API Key 与 Endpoint。

- **需要帧级控制或导出中间帧**（如用于后期合成、AR叠加）：  
  → 当前两类 API 均**不提供帧序列下载**。若必须获取逐帧，需自行对生成视频做抽帧处理（注意版权与水印合规性），或联系平台申请定制化能力支持。

## 面向开发者的选型参考指南

1. **起步验证阶段**：  
   - 优先使用 `qwen-image-2.0-pro`（同步、北京/新加坡可用、免费额度覆盖）验证图像流程；  
   - 视频侧选用 `wan2.7-t2v-2026-06-12`（支持自然语言分镜、文档完善）+ `task_id` 轮询 SDK 封装，避免手动轮询。

2. **生产环境部署要点**：  
   - **域名与地域必须显式绑定**：禁用 `dashscope.aliyuncs.com` 通用域名，全部切换至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），提升稳定性与性能；  
   - **错误处理标准化**：图像 API 需捕获 `429`（限流）、`400`（参数错误）；视频 API 必须处理 `401`（地域不匹配）、`404`（旧版路径错误，如误用 `/image2video/`）；  
   - **水印策略统一**：生产环境所有请求显式设置 `"watermark": false`，避免默认水印影响交付。

3. **模型升级路径建议**：  
   - 图像侧：逐步淘汰 `wan2.5-i2i-preview` 等旧版，迁移到 `wan2.7-image-pro`（4K）或 `qwen-image-2.0-pro`（文字渲染）；  
   - 视频侧：**立即停用万相2.1–2.6系列**（文档标记为“旧版协议”），全面切换至 `wan2.7-*` 或 `vidu/kling` 新主力模型，享受分镜解析、多镜头、音频生成等增强能力。

4. **成本监控关键指标**：  
   - 图像：监控 `total_images_generated` 与 `free_quota_remaining`（Dashboard 可查）；  
   - 视频：监控 `total_video_seconds_generated` 及各模型 `avg_duration_per_task`，警惕因 `duration` 参数设置过高导致意外超支。

> **最后提醒**：两类能力虽同属 AIGC，但底层计算范式、资源调度与 SLA 保障机制完全不同。切勿将图像 API 的同步思维套用于视频，亦不可期望视频模型输出单帧图像——尊重各自技术边界，方能构建稳健、可扩展的多模态应用。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)


