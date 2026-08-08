# release notes

百炼平台的 release notes 汇总了模型生命周期管理（上架、下线）、平台功能迭代及关键参数变更，旨在帮助开发者及时掌握服务可用性、兼容性与最佳实践。所有变更均遵循统一通知机制，并通过控制台、API 及文档同步更新。请务必关注模型下线时间窗口与替代方案，避免服务中断。

## 支持的模型/功能

- **新上线模型**：2026年7月起，平台陆续上架 `qwen3.8-max`（2.4万亿参数 MoE 架构）、`qwen3.7-flash`（多模态 Agent 强化版）、`qwen-audio-3.0-asr-flash-streaming`（支持30语种+方言+古诗词识别）、`kimi/kimi-k3`（2.8万亿参数，100万上下文）、`glm-5.2`（智谱旗舰，1M上下文）等核心模型；图像生成新增 `qwen-image-3.0` 与 `qwen-image-3.0-pro`；视频生成新增 `wan3.0-video`、`viduq3-drama_reference2video` 等专用模型。详情见 [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **下线模型**：按“主线模型提前3个月通知、快照模型提前30天通知”原则执行。2026年10月10日集中下线千问Max、VL、Coder、TTS、ASR等系列共百余个历史模型（如 `qwen-turbo`、`qwen-vl-max`、`qwen-tts`、`paraformer-v1`），以及第三方模型 `glm-4.5`、`deepseek-r1-distill-qwen-7b` 等；2026年5月30日已下线 `gte-rerank`，替代模型为 `qwen3-rerank`。完整清单与替代关系详见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。
- **平台功能更新**：2026年6月起，新增知识检索与问答服务、智能体托管运行时 API、Skill 能力包、数据连接模块（MySQL/语雀/OSS）、模型压缩模块；7月上线 Responses API 异步调用（`background=true`）、API Key 加密存储与业务空间专属域名；8月推出模型升级通知机制。详见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。

> **注意**：文档2中列出的 `qwen3.7-max-2026-06-08`（含视觉能力）与文档1中“2026年10月10日下线”的 `qwen3-max-preview` 存在命名重叠但语义冲突——前者为正式快照，后者属待下线主线预览版。实际以文档1的下线列表为准，`qwen3-max-preview` 已明确列入下线范围，不可用于新部署。

## 关键参数

- **上下文长度**：`qwen3.8-max`、`kimi/kimi-k3`、`glm-5.2`、`deepseek-v4-pro` 等主流模型支持 **100万 token** 上下文；`qwen3.7-flash`、`qwen-audio-3.0-asr-flash` 等 Flash 系列侧重低延迟，上下文通常为 32k–128k。
- **限流策略**：模型下线前进入限流期，QPM/TPM 逐步缩减至默认限流值（参见 [默认限流](https://help.aliyun.com/zh/model-studio/rate-limit)）；正式下线后 API 完全不可用。
- **部署计费单元**：自2026年1月起，[模型部署](../concepts/model-deployment.md)支持 **模型单元（MU）按时间计费**，替代传统实例规格，提升资源弹性与成本可预测性（见 [模型部署](../../raw/model-user-guide/release-notes/model-release-notes.md)）。
- **异步任务回调**：2026年4月起，异步任务支持 EventBridge HTTP 回调与 RocketMQ 主动推送，替代轮询模式，降低客户端复杂度。

## 使用方式

- **模型调用**：通过 DashScope SDK 或 REST API 调用，需指定 `model` 参数（如 `"qwen3.7-plus"`）。新版智能体应用 API（2026年5月首发）统一支持 OpenAI Responses / Anthropic Messages 兼容接口。
- **模型迁移**：下线模型用户应通过 [模型观测](https://bailian.console.aliyun.com/#/model-telemetry) 确认调用记录，测试替代模型（如 `qwen-turbo` → `qwen3.7-flash`）效果后切换。快照模型（含日期后缀）无自动升级，需显式更换 model ID。
- **功能启用**：新功能（如 Skill 能力包、知识检索服务）需在控制台对应模块开通或调用对应 API（如 `/v1/knowledge/retrieve`），部分能力（如强化学习训练）当前为邀约制。
- **安全合规**：模型调优支持 0 代码安全强化流程（2026年5月上线），适用于文本生成类模型；声音复刻、语音合成等敏感功能需遵守 [CosyVoice 声音复刻 API](../../raw/model-user-guide/release-notes/model-release-notes.md) 的身份核验要求。

## 限制和注意事项

- **下线模型不可恢复**：正式下线后，API 返回 `404` 或 `ModelNotAvailable` 错误，已部署的模型实例停止响应，**不支持回滚或续期**。
- **快照模型时效性**：快照模型（如 `qwen-max-2025-01-25`）仅保证在下线公告截止日前可用，期间不接受扩容申请，且不参与平台级性能优化。
- **地域与部署范围**：2026年6月新增美国、德国、日本地域，但部分新模型（如 `wan3.0-video`）初始仅在华北2（北京）可用，跨地域调用需确认[模型部署](../concepts/model-deployment.md)状态。
- **API 兼容性**：2026年5月起，文本生成 API 入口聚合 OpenAI/Anthropic 标准接口，旧版 `/v1/services/aigc/text-generation/generation` 接口仍可用但建议迁移；异步任务回调需配置 EventBridge 目标端点，否则事件丢失。
- **免费额度约束**：2026年7月起，[Token](../concepts/token.md) Plan 用户权益升级，但免费额度用完即停（2025年7月上线），且不覆盖已下线模型调用。

> **注意**：文档3中“7月10日 部分老旧模型下线通知”链接指向官网公告 `118434`，而文档1中同名表格亦引用该公告，但文档1所列下线模型数量远超公告原文覆盖范围。实际执行以文档1的结构化表格为准，公告仅为摘要入口。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


