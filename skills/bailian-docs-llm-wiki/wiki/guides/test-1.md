# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署及成本控制的全链路规则。本文档整合了免费额度、节省计划、资源包、模型定价及账单管理等关键机制，帮助开发者准确预估成本、合理配置资源并规避意外扣费。所有计费逻辑均以华北2（北京）地域为默认基准，其他地域模型价格与免费额度策略存在显著差异。

## 支持的模型/功能

- **支持免费额度的模型**：仅限华北2（北京）地域的实时推理调用，包括 `qwen-max`、`qwen3.7-plus`、`qwen3.6-plus` 等主流千问系列模型及其快照版本（如 `qwen3.7-plus-2026-05-26`），不同快照视为独立模型，额度不互通 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **支持 Batch 调用的模型**：部分模型（如 `qwen3.7-max`、`qwen3.7-plus`）在 Batch 接口下输入/输出 Token 单价按实时推理价格的 50% 计费，但该优惠与上下文缓存折扣不可同时生效 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **支持上下文缓存的模型**：`qwen3.7-max`、`qwen3.6-max-preview` 等模型支持显式/隐式缓存，缓存命中 Token 按标准输入单价的 10% 计费，创建显式缓存则按 125% 计费，此规则独立于主价格表 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **不支持免费额度的场景**：Batch 调用、模型调优、模型部署、自定义模型（调优后或已部署模型）均不可抵扣免费额度 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。

> **注意**：文档 5 中 `qwen-max` 在华北2（北京）的输入单价标为 `2.4元/百万Token`，而文档 1 明确其免费额度为 `100万Token`；但文档 5 同时注明“仅在华北2（北京）下有免费额度”，而文档 2 的 AI 通用型节省计划说明中将 `qwen-max` 归类为 A 类模型（可被抵扣），且未排除其免费额度适用性。三者逻辑一致，无实质性矛盾。

## 关键参数

- **免费额度有效期**：90 天，自开通百炼、模型发布或申请通过之日三者中最晚者起算；2025年9月8日前开通用户有效期可能不足90天 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **Token 计费粒度**：模型训练费用按训练 Token 总数计算，最小计费单位为 1 Token；模型推理费用按输入/输出 Token 分别计费，单价单位为“每百万 Token” [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)、[模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **阶梯计费阈值**：部分模型（如 `qwen3-max`）按单次请求输入 Token 数分档计价（如 0–32K、32K–128K），全部 Token 均按所属最高档单价结算 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **节省计划承诺周期**：“动态月”非自然月，从购买日次日 0 点起算，每月额度独立清零，不可累积 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 使用方式

- **免费额度启用**：无需额外操作，开通百炼后系统自动发放，调用时自动优先抵扣；需使用通用 API Key（非 Token Plan/Coding Plan 专属 Key），否则不生效 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **节省计划抵扣顺序**：严格遵循 `免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费` 顺序，若开启“免费额度用完即停”，额度耗尽后服务停止，节省计划无法触发抵扣 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **账单查询路径**：模型推理账单在 [账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail) 页面按“大模型服务平台百炼”筛选，关键字段 `实例 ID（出账粒度）` 以分号 `;` 分隔，格式为 `ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识` [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **成本分摊**：通过为业务空间绑定标签实现，需在 [标签管理](https://resourcemanager.console.aliyun.com/tags#/) 绑定业务空间 ID，并在 [费用标签](https://billing-cost.console.aliyun.com/finance/tags) 启用，T+1 生效 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **地域限制**：免费额度仅华北2（北京）有效；美国（弗吉尼亚）、新加坡等地域模型价格上浮（如 `qwen3.7-max-us` 输入单价达 `18.736元/百万Token`），且无免费额度 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **额度耗尽影响**：全新未认证用户额度用尽后返回错误码 `AllocationQuota.FreeTierOnly`，必须认证并充值；已认证用户若未开启“免费额度用完即停”，将直接按量扣费，可能导致账户欠费 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费全局阻断**：账户欠费时，即使免费额度、节省计划、资源包仍有余额，所有模型调用均被暂停 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **模型部署持续计费**：部署状态为“运行中”即开始按时长计费，与是否发起 API 调用无关；需主动下线模型或删除 API Key 才能停止费用产生 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


