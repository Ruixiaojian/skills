# release notes

本页面汇总百炼平台的模型上下架动态与功能更新记录，帮助开发者快速了解平台最新变化。内容涵盖新模型发布、平台功能迭代、计费调整及重要公告通知。详细的时间线记录请参阅原始文档。

## 模型上下架动态

完整的模型上架与下线清单请参见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。以下为近期重点上线模型分类汇总：

### 推理模型（文生文/视觉理解）

| 时间 | 模型规格 | 说明 |
|------|----------|------|
| 2026-05-29 | vanchin/deepseek-v4-pro | 快手万擎直供 DeepSeek 推理服务 |
| 2026-05-25 | qwen3.7-max-preview | Qwen Max 系列，仅支持纯文本+思考模式 |
| 2026-05-21 | qwen3.7-max | Qwen Max 新一代旗舰，支持显式缓存 |
| 2026-05-19 | xiaomi/mimo-v2.5-pro | 小米直供，通用 Agent/复杂工程能力提升 |
| 2026-05-19 | ZHIPU/GLM-5.1、ZHIPU/GLM-5 | 智谱直供 |
| 2026-04-24 | deepseek-v4-pro、deepseek-v4-flash | DeepSeek-V4 系列（阿里直供） |
| 2026-04-23 | qwen3.6-27b | Qwen3.6 Dense 模型，Agentic coding 能力增强 |
| 2026-04-20 | qwen3.6-max-preview | Qwen3.6 最大闭源模型，仅文本输入 |
| 2026-04-16 | qwen3.6-flash | Qwen3.6 Flash，智能体编程/数学推理增强 |
| 2026-04-14 | glm-5.1 | 支持 200K 上下文，最大输出 128K Token |
| 2026-04-02 | qwen3.6-plus | 代码开发重点升级，多模态能力增强 |

### 视频生成（文生/图生/参考生/编辑）

平台已上线多个视频生成模型系列：

- **万相 2.7 系列**：文生视频（wan2.7-t2v）、图生视频（wan2.7-i2v）、参考生视频（wan2.7-r2v）、视频编辑（wan2.7-videoedit）
- **Vidu 系列**：viduq3-pro/turbo，支持文生、首帧生、首尾帧生、参考生视频
- **爱诗 PixVerse 系列**：v6/c1 版本，支持智能分镜与多风格
- **HappyHorse 系列**：支持有声视频生成，720P/1080P，3~15 秒
- **可灵 V3 系列**：支持文生视频、图生视频、参考生视频及视频编辑

### 全模态与语音

| 时间 | 模型规格 | 说明 |
|------|----------|------|
| 2026-05-19 | qwen3.5-livetranslate-flash-realtime | 实时音视频翻译，识别 60 种语言，翻译 29 种 |
| 2026-05-06 | fun-music-v1 | 百聆音乐生成，支持中英文歌曲 |
| 2026-04-16 | fun-asr | 实时语音识别，支持 30 语种，七大方言覆盖 |
| 2026-03-30 | qwen3.5-omni-plus/flash | 全模态，支持 3 小时音频及 1 小时视频输入 |
| 2026-03-30 | qwen3.5-omni-plus-realtime | 实时多模态，原生联网搜索，支持 113 种语种识别 |

### 图像生成与 3D

- **万相 2.7 图像**（wan2.7-image-pro/image）：支持文生图、图像编辑、4K 输出
- **千问图像**（qwen-image-2.0-pro）：图片生成与编辑融合，支持多语言图内文字
- **Tripo 3D**（Tripo-H3.1/P1.0）：文生3D/单图/多图生3D，最高 200 万面

## 平台功能更新

平台功能的完整时间线记录请参见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。以下按功能模块整理核心更新：

### 模型观测与监控

| 时间 | 功能点 |
|------|--------|
| 2025-01-21 | 新增模型观测能力（调用量/性能变化监控） |
| 2025-04-18 | 高级监控模式：分钟级刷新，4xx/5xx 分类统计 |
| 2025-06-05 | 告警与通知：指标异常自动通知 |
| 2025-11-06 | 支持查看模型推理日志（历史对话内容） |
| 2025-12-22 | 免费额度和用量统计看板 |

### 模型调优与部署

| 时间 | 功能点 |
|------|--------|
| 2025-08-14 | 通义千问2.5-VL-72B/32B/7B 支持调优和部署 |
| 2025-09-12 | Qwen3/Qwen2.5 系列支持 DPO 偏好训练 |
| 2025-10-21 | Qwen3-VL-8B-Instruct/Thinking 支持 SFT |
| 2025-10-24 | 新增模型单元部署方式（按时间计费，灵活调性能） |
| 2024-12-27 | qwen2.5-7b-instruct 支持 SFT 全参和高效调优 |
| 2024-12-27 | 模型部署支持按调用量计费 |

### 模型评测

| 时间 | 功能点 |
|------|--------|
| 2024-08-08 | 新增自动化评测 |
| 2025-12-15 | 排行榜功能：多模型多维度对比 |
| 2025-12-15 | 新增评估器：字符串匹配、文本相似度、模型打分等 |

### Context Cache（上下文缓存）

- 2024-12-24 上线，减少重复运算量，提升响应速度，降低使用成本
- deepseek-v4-pro 的 `cached_token` 单价调整为 1 元/百万 token

> **注意**：2024年12月上线时仅支持 qwen-plus 模型，当前已扩展至更多模型（含 deepseek-v4-pro 等），具体支持范围请参考最新计费文档。

### OpenAI 接口兼容

- **Batch 模式**（2024-08-23）：批量异步请求，24 小时内返回，费用为实时调用的 50%
- **Vision 模式**（2024-08-27）：调整 API-KEY/BASE_URL/model 即可对接视觉模型
- **Batch 任务通知**（2024-12-20）：支持 Callback 回调和 EventBridge 消息

### 数据处理

- 画布编排（2024-11）：灵活组合清洗/增强节点
- 毒性消除、敏感词过滤算子（2024-07）
- 数据增强（2024-06）

## 计费与定价调整

关键计费变动（详见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中的计费模块）：

| 时间 | 变动 |
|------|------|
| 2025-02-07 | qwen-max 输入降 88%，输出降 84% |
| 2025-02-08 | DeepSeek 系列由免费转计费 |
| 2025-01-22 | qwen2.5-14b/7b 降价 50%；qwen2.5-3b/qwen2-vl-72b 转计费 |
| 2024-12-31 | 通义千问 VL 系列降价最高 85% |
| 2024-09-19 | qwen-max/turbo/plus 降价 |
| 2024-09-20 | 支持预付费节省计划 |
| 2024-09-10 | 模型训练计费规则更新，混合训练开始计费 |

## 限制与注意事项

- **模型下线机制**：平台有明确的模型下线流程，已下线模型包括 qwen-max-longcontext（2024-10）、qwen-max-1201（2024-04）等。使用快照版本的开发者应关注下线通知并及时迁移。
- **免费额度**：新人免费额度有效期已从 30 天调整为 180 天；启用"用完即停"可避免超额费用（错误码 `AllocationQuota.FreeTierOnly`）。
- **限流扩容**：支持自定义申请，通过模型广场详情页提交。
- **部署范围**：中国内地部署时，推理计算资源限于中国内地，静态数据存储于所选地域（当前支持华北2-北京）。

> **注意**：部分模型（如 qwen3.7-max-preview、qwen3.6-max-preview）仅支持纯文本输入，不支持图像与视频输入，使用前请确认模型能力边界。

## 公告通知

- [阿里云百炼部分模型上下文缓存降价通知](https://www.aliyun.com/notice/117497)
- [Qwen3-Coder-Plus 限时优惠](https://help.aliyun.com/zh/model-studio/qwen3-coder-plus-price-drop)
- [2025年6月大语言模型推理资源包优惠活动](https://help.aliyun.com/zh/model-studio/june-2025-promotion-of-model-studio-inference-resource-plan)
- [模型下线机制说明](https://help.aliyun.com/zh/model-studio/model-depreciation)
- ["云工开物"高校计划](https://help.aliyun.com/zh/model-studio/introduction-to-yungongkaiwu)

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)

