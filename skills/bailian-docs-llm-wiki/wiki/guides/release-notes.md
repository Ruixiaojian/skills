# release notes

百炼平台的 Release Notes 汇总了模型、功能、API 及基础设施层面的重要更新，涵盖新模型上架、能力升级、接口新增与计费策略调整等核心变更。所有变更均面向开发者设计，强调可集成性、稳定性与成本可控性。本文档按逻辑结构组织关键信息，便于快速定位适配点。

## 支持的模型/功能

- **新增模型**：2026年7月起，华北2（北京）地域陆续上线多模态与垂直领域模型，包括 `qwen3.7-flash`（原生VL Flash）、`qwen-image-3.0-pro`（高精度图生图）、`qwen-audio-3.0-realtime-plus/flash`（双工语音对话）、`pixverse/pixverse-motioncontrol`（动作迁移）、`vidu/viduq3-ad_reference2video`（广告专用视频生成）等。完整清单详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **模型能力扩展**：Qwen3.7系列全面支持视觉理解与Agent混合智能体能力；GLM-5.2新增Fast模式（[GLM-5.2 Fast mode 模式降价通知](../../raw/model-user-guide/release-notes/model-release-notes.md)）；Kimi K3支持100万token上下文与原生视觉理解。
- **平台级功能**：[知识库](../concepts/knowledge-base.md)RAG新增联合检索与混合排序（[知识检索服务上线](../../raw/model-user-guide/release-notes/model-release-notes.md)）；智能体托管运行时API正式发布（[智能体托管运行时上线](../../raw/model-user-guide/release-notes/model-release-notes.md)）；模型评测新增排行榜与BLEU_4等综合评估器。

> **注意**：文档1中“6月23日 [知识库](../concepts/knowledge-base.md)RAG 知识检索服务上线”与文档2未提及该服务API细节，实际调用需以 [知识检索服务上线](../../raw/model-user-guide/release-notes/model-release-notes.md) 文档为准；文档2中部分模型（如`qwen3.7-max-2026-06-08`）标注“增加视觉模态理解能力”，但文档1对应日期（6月9日）仅提及Skill能力包上线，未说明视觉能力同步落地，建议以模型文档ID为准验证能力可用性。

## 关键参数

- **上下文长度**：`kimi/kimi-k3`、`glm-5.2`、`deepseek-v4-pro` 等主流模型支持 1M token 超长上下文；`qwen-audio-3.0-asr-flash-streaming` 支持实时流式识别，`qwen3.5-ocr` 在卡证类业务场景中关键信息抽取准确率显著提升。
- **性能指标**：`glm-5.2-fast-preview` 输出TPS达标准版1.5～2倍；`kimi-k2.7-code-highspeed` 编程场景下输出速度约180 Token/s（中位数输入）；`qwen-audio-3.0-tts-plus` 在噪声混响环境下鲁棒性增强，音质与表现力优于Flash版。
- **部署单元**：模型部署支持按模型单元（MU）时长计费（[使用 API 部署新增预置模型与按模型单元时长计费](../../raw/model-user-guide/release-notes/model-release-notes.md)），适用于qwen-flash/qwen-plus等预置模型。

## 使用方式

- **API调用**：文本生成API已聚合OpenAI Responses与Anthropic Messages两类接口；Responses API支持`background=true`异步调用（[Responses API 新增异步调用](../../raw/model-user-guide/release-notes/model-release-notes.md)）；异步任务可通过事件总线EventBridge接收HTTP回调或RocketMQ推送，避免轮询。
- **SDK接入**：多模态交互开发套件提供Linux C++、Android/iOS Lite、RTOS C及Java SDK；Coding Plan支持Kilo CLI工具接入（[接入客户端开发工具新增 Kilo CLI](../../raw/model-user-guide/release-notes/model-release-notes.md)）。
- **模型导入与调优**：国际站支持从OSS导入LoRA微调模型（[模型导入功能国际站上线](../../raw/model-user-guide/release-notes/model-release-notes.md)）；模型调优支持SFT（全参/LoRA）、DPO偏好训练、强化学习（RL，邀约制）及0代码安全合规强化。

## 限制和注意事项

- **模型下线**：老旧模型分批下线，含“部分老旧模型”“部分老旧长尾模型”及`qwen-turbo`资源包退市（[部分老旧模型下线通知](../../raw/model-user-guide/release-notes/model-release-notes.md)、[qwen-turbo 资源包启动退市通知](../../raw/model-user-guide/release-notes/model-release-notes.md)）。具体清单与过渡期请严格参照 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-release-notes.md)。
- **免费额度**：新人免费额度启用“用完即停”策略，耗尽后返回错误码 `AllocationQuota.FreeTierOnly`（[新增免费额度用完即停功能](../../raw/model-user-guide/release-notes/model-release-notes.md)）；团队版新增共享Credits弹性用量包，但跨坐席抵扣需配置权限。
- **地域与兼容性**：美国、德国、日本地域于6月12日新增部署（[新增地域与部署范围](../../raw/model-user-guide/release-notes/model-release-notes.md)）；Spring AI Alibaba框架已支持调用百炼智能体应用（[Spring AI Alibaba 调用百炼应用文档上线](../../raw/model-user-guide/release-notes/model-release-notes.md)），但需确认SDK版本兼容性。

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)


