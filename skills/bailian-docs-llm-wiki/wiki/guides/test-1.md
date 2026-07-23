# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖新人免费额度、模型调用/训练/部署的计费规则、成本优化方案（节省计划与资源包）以及账单查询与成本管控机制。本文档整合官方最新策略，聚焦实时推理（按量调用）场景，明确免费额度适用边界、抵扣优先级及关键限制条件，帮助开发者快速建立成本意识并规避意外费用。

## 支持的模型/功能

- **支持免费额度的模型**：仅限华北2（北京）地域且服务部署范围为“中国内地”的模型（如 `qwen3.7-plus`、`qwen-max` 等），以及新加坡地域且服务部署范围为“国际”的模型；其他地域或部署范围（如美国、德国、日本）的同名模型**不享有免费额度** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **支持阶梯计费的模型**：千问Max、千问Plus等主流文本生成模型按单次请求输入Token总量分档计价（如 0–32K、32K–128K），所有Token均按所处最高阶梯单价结算 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **不支持免费额度抵扣的功能**：Batch调用、模型调优（训练）、模型部署、自定义模型（调优后或已部署模型）产生的费用，均**不可使用免费额度抵扣** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

> **注意**：文档5中列出的 `qwen3.7-max` 在华北2（北京）地域标注“免费额度100万Token”，而文档1明确说明免费额度仅适用于“中国内地”部署范围的模型。但文档5表格中部分行将“服务部署范围”列为“全球”或“欧盟”，却仍显示“免费额度”列——这与文档1“仅中国内地/国际地域享有免费额度”的核心规则矛盾。实际以文档1为准：**非中国内地/国际地域的模型无免费额度**。

## 关键参数

- **免费额度有效期**：90天，自开通百炼、模型发布或模型申请通过之日**三者中最晚者**起算；2025年9月8日11点前开通的用户，有效期可能不足90天 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **抵扣优先级顺序**：系统按固定顺序自动抵扣：**免费额度 > 资源包 > 其他模型节省计划 > AI通用型节省计划 > 按量付费**。该顺序在节省计划与资源包文档中被多次确认，是成本控制的核心逻辑 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **模型单元（MU）规格**：模型部署按“模型单元”计费时，不同规格（如 MU1 x 2、MU3 x 8）对应不同小时单价，最小计费单位为“分钟”；预付费则按“天”或“月”计费 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

## 使用方式

- **启用免费额度**：无需额外操作，开通百炼并同意协议后系统自动发放；调用时使用**通用API Key**（非Token Plan/Coding Plan专属Key），系统将自动优先抵扣 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **开启“免费额度用完即停”**：在控制台[免费额度页面](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)或[模型广场详情页](https://bailian.console.aliyun.com/?tab=model#/model-market/detail/group-qwen3-coder-plus?modelGroup=group-qwen3-coder-plus)手动开启开关，可防止额度耗尽后自动转为按量付费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **应用AI通用型节省计划**：购买后立即生效，覆盖阿里直供全部模型（A类），支持抵扣模型调用、工具调用、批量推理等费用，但**不支持抵扣模型训练与部署费用** [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 限制和注意事项

- **额度不共享、不转移**：不同模型（含不同快照版本，如 `qwen3.7-plus` 与 `qwen3.7-plus-2026-05-26`）的免费额度完全独立，不能合并或跨模型使用；主账号与RAM子账号共享同一模型的额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费导致服务中断**：账户可用额度 < 0（即欠费）时，**即使模型仍有剩余额度，所有按量付费相关服务（包括推理）将立即暂停**；Coding Plan/Token Plan等预付费套餐不受影响，但自动续费会失败 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **账单延迟与溯源**：模型推理账单通常在调用结束后2–10分钟出账（分钟级），而模型训练、知识库等为小时级；账单明细中“实例 ID（出账粒度）”字段（格式如 `ApiKeyID;业务空间ID;模型名称;...`）是定位费用归属的唯一可靠依据 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


