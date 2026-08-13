# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖新人免费额度、模型调用/训练/部署定价、成本优化方案（节省计划与资源包）以及账单治理等全链路能力。本文档聚焦实时推理场景的使用基础，明确免费额度的适用边界、关键参数的计费逻辑、主流接入方式，并强调地域限制、模型快照独立性及额度耗尽后的服务行为等关键约束。所有信息均基于当前平台正式发布规则整理，不包含公测或邀测功能。

## 支持的模型/功能

- **支持免费额度的模型**：仅限华北2（北京）地域上架的模型，且需在控制台模型广场详情页中明确显示“免费额度”区域（如 `qwen-max`、`qwen3.7-plus-2026-05-26` 等）。ASR 类模型需在业务空间内单独开通权限后方可消耗额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **不支持免费额度的场景**：Batch 调用、模型调优、模型部署、自定义模型（含调优后模型、已部署模型）、PAI-DSW、OSS 存储及请求费用 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **模型快照独立性**：带日期后缀的快照版本（如 `qwen-max-2026-05-17`）与不带日期的最新版（如 `qwen-max`）视为两个独立模型，各自拥有 100 万 [Token](../concepts/token.md) 免费额度，额度不互通、不转移 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 关键参数

- **免费额度有效期**：90 天，自开通百炼、模型发布或模型申请通过之日三者中**最晚者**起算；2025年9月8日11点前开通的用户，有效期可能不足90天 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **[Token](../concepts/token.md) 计费粒度**：输入 [Token](../concepts/token.md) 与输出 Token 共用总额度，不单独区分；调用时产生的 Token 总量共同扣减该总额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **API Key 类型影响**：通用 API Key 可消耗免费额度；而 Token Plan/Coding Plan 专属 API Key **不消耗免费额度**，直接按量付费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **地域与部署范围**：免费额度仅适用于华北2（北京）地域模型；部分模型（如 `qwen3.8-max`）在全球/国际/欧盟等部署范围下无免费额度，其价格亦按对应地域标准执行 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。

> **注意**：文档 5 中 `qwen3.7-max` 在华北2（北京）标注为“当前能力等同于 `qwen3.7-max-2026-05-20`”，但文档 2 的部署计费表中未列出 `qwen3.7-max` 这一模型代码，仅列有 `qwen3.7-max-2026-05-20`。实际调用应以控制台模型广场展示的**确切 Model ID** 为准，避免因别名映射导致额度或计费异常。

## 使用方式

- **自动生效**：首次开通百炼后，系统自动发放免费额度，无需手动领取或实名认证；额度通常两小时内生效，控制台模型列表中以蓝色额度条标识 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **调用即抵扣**：使用通用 API Key 实时调用支持的模型时，系统按“免费额度 > 资源包 > 节省计划 > 按量付费”顺序自动抵扣，无需额外配置 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **查看剩余额度**：
  - 方式一：控制台[免费额度页面](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)，支持按模型类型筛选；
  - 方式二：模型广场详情页，在“模型Code”选择版本后，于“免费额度”区域直接查看（如 `362,917/1,000,000`）；
  - 方式三：[模型用量页面](https://bailian.console.aliyun.com/?tab=model#/model-usage)，查看各模型使用与剩余情况 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **成本优化选型**：长期稳定使用推荐 **AI 通用型节省计划**（覆盖全阿里直供模型，最高5.3折）；用量小或集中特定模型可选**资源包**；团队协作推荐**Token Plan** [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 限制和注意事项

- **额度用完即停（安心模式）**：开启后，免费额度耗尽时返回错误码 `AllocationQuota.FreeTierOnly`，服务停止；未认证用户默认强制开启且不可关闭；已认证用户可自行开关，但生产环境不建议开启，以免服务中断 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **账户欠费影响**：即使某模型仍有免费额度，只要账户整体欠费（可用额度 < 0），所有模型调用均会暂停 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **出账延迟**：模型推理账单为分钟级出账（通常2~10分钟），非实时扣款；批量推理、训练等为小时级出账。查询账单需等待对应延迟 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **地域强绑定**：免费额度、部分模型价格、节省计划抵扣均严格限定地域。例如，华北2（北京）的免费额度无法用于新加坡地域调用；AI 通用型节省计划虽支持多地域购买，但抵扣时需确保调用 Base URL 与购买地域一致 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


