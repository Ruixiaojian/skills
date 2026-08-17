# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署及成本控制的全链路规则。本文档聚焦实时推理（即模型调用）的计费体系，明确免费额度适用范围、付费模型的价格结构、成本优化工具（如节省计划）的使用逻辑，以及关键限制条件。所有信息均基于华北2（北京）地域的生产环境配置，其他地域模型不参与新人免费额度发放，且价格存在差异。

## 支持的模型/功能

- **支持免费额度的模型**：仅限华北2（北京）地域上架的模型，包括 `qwen-max`、`qwen3.6-plus`、`qwen3.7-plus` 等主流文本生成模型及其快照版本（如 `qwen3.7-plus-2026-05-26`），不同快照视为独立模型，各自拥有 100 万 [Token](../concepts/token.md) 免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **不支持免费额度的场景**：Batch 调用、模型调优、模型部署、PAI-DSW、OSS 存储及请求费用，均不可抵扣 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **[多模态](../concepts/multi-modal.md)与语音模型**：ASR 类模型需在业务空间中逐一开通权限后方可消耗免费额度；图像/视频生成模型（如 `wanx` 系列）不支持通过标准文本 Base URL 直接调用，必须经 Skill 或扩展机制接入 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 关键参数

- **[Token](../concepts/token.md) 计费粒度**：输入与输出 [Token](../concepts/token.md) 共用总额度，按实际消耗量扣减，不区分输入/输出单独计算 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **阶梯计费**：部分模型（如 `qwen3-max`）按单次请求输入 Token 总量分档定价，例如 `0 < Token ≤ 32K` 与 `32K < Token ≤ 128K` 对应不同单价，该请求所有 Token 均按所属档位结算 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **地域参数影响价格**：同一模型在不同地域价格不同，例如 `qwen3.8-max` 在华北2（北京）输入单价为 ¥12/百万 Token，而在新加坡为 ¥14.988/百万 Token [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。

## 使用方式

- **免费额度自动生效**：首次开通百炼后系统自动发放，无需实名认证即可使用；调用时系统按 `免费额度 > 资源包 > AI 通用型节省计划 > 按量付费` 顺序自动抵扣 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **启用节省计划**：AI 通用型节省计划覆盖全部阿里直供模型，购买后立即生效，可抵扣模型调用、Function Calling、上下文缓存、批量推理等费用，但**不支持抵扣联网搜索插件、MCP 广场、通义深度搜索等第三方工具费用** [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **API Key 选择**：通用 API Key 可消耗免费额度；Token Plan/Coding Plan 专属 API Key **不消耗免费额度**，调用将直接按量付费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 限制和注意事项

> **注意**：文档 5 中 `qwen3.7-max` 在华北2（北京）标注为“当前能力等同于 `qwen3.7-max-2026-05-20`”，但文档 3 的部署计费表中未列出 `qwen3.7-max`，仅列出 `qwen3.7-max-2026-05-20` 及 `qwen3.7-max-2026-05-20` 的部署规格与单价。开发者应以控制台实际展示的模型 ID 为准，避免使用别名调用导致计费异常或服务不可用。

- **免费额度用完即停（安心模式）**：未完成实名认证的用户默认强制开启，额度耗尽后返回错误码 `AllocationQuota.FreeTierOnly`；已认证用户可手动开关，但**开启后若额度耗尽，服务将停止，节省计划无法触发抵扣**，需关闭该功能才能继续使用节省计划 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **账户欠费影响全局服务**：即使某模型仍有免费额度或节省计划剩余额度，只要账户整体欠费（可用额度 < 0），所有模型调用均会暂停 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **出账延迟与账单溯源**：模型推理账单通常 2~10 分钟出账，但账单详情中的“实例 ID（出账粒度）”字段以分号 `;` 分隔，格式为 `ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`，是定位费用归属的唯一可靠依据 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


