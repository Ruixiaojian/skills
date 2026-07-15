# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署的全链路成本控制机制。其核心围绕免费额度自动抵扣、多层级付费方案（按量、资源包、节省计划）及精细化账单溯源能力展开，旨在帮助开发者在保障业务连续性的同时实现成本可预测、可监控、可优化。所有计费行为均默认遵循“免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费”的严格抵扣顺序。

## 支持的模型/功能

- **支持免费额度的模型**：仅限华北2（北京）地域、服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)的模型，例如 `qwen3.7-plus`、`qwen-max` 等主流文本生成模型；快照版本（如 `qwen3.7-plus-2026-05-26`）与基础版本视为独立模型，各自享有独立额度 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **不支持免费额度的场景**：Batch调用、模型调优、模型部署、自定义模型（调优后或已部署模型）均不可使用免费额度抵扣 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **支持的计费模型类型**：覆盖文本生成（千问、DeepSeek、GLM）、多模态（千问VL）、图像生成（万相）、视频生成（万相）、语音模型（千问语音）、向量/排序模型（text-embedding-v4、qwen3-rerank）等全品类，详见各模型价格表 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **专属计费能力**：模型训练按训练Token计费（如千问VL、万相图生视频），模型部署支持两种模式——预置吞吐（按TPM时长）和模型单元（按算力规格小时）[模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

> **注意**：文档 5 中 `qwen3.7-plus` 在华北2（北京）的“思考模式”输出单价标注为 `8元/百万Token`，而文档 2 中同模型在“模型部署计费”表格里输出单价为 `¥1.92/Per 1K TPM/小时`（即 `1920元/百万TPM/小时`），二者计量单位与场景不同（Token vs TPM），不构成矛盾；但需注意文档 2 明确说明部署计费不支持免费额度抵扣，而文档 1 强调免费额度仅适用于实时推理，此边界必须严格区分。

## 关键参数

- **免费额度参数**：默认 100 万 Token/模型，有效期自开通或申请通过日起 90 天（2025年9月8日11点起新用户适用）；主账号与RAM子账号共享额度，不同模型间额度不互通 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **阶梯计费参数**：部分模型（如 `qwen3-max`）按单次请求输入Token总量分档计价（如 0–32K、32K–128K），该次请求全部Token均按对应档位单价结算 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **部署计费参数**：
  - 预置吞吐：`费用 = 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM)`；
  - 模型单元：`费用 = 使用时长（小时）× 模型单元数量 × 模型单元单价`，最小计费单位为分钟 [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **节省计划承诺参数**：AI 通用型节省计划以“动态月”为周期（非自然月），月承诺消费额从生效日起每满30天重置，当月未用完额度自动清零 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 使用方式

- **免费额度启用**：无需额外配置，开通百炼后系统自动发放，实时调用即自动优先抵扣；需确保使用通用 API Key（非 Token Plan/Coding Plan 专属 Key），否则不生效 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **节省计划购买与抵扣**：通过 [AI 通用型节省计划购买页](https://common-buy.aliyun.com/?commodityCode=sfm_GenAI_spn_cn)下单，支持全预付/零预付；购买后立即生效，自动按抵扣顺序参与结算，无需绑定模型或API Key [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **账单查询与归因**：通过[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面，依据 `实例 ID（出账粒度）` 字段（格式：`ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`）精准定位费用来源 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **成本防护配置**：在免费额度页面开启“免费额度用完即停”，可防止额度耗尽后意外扣费；同时建议设置[高额消费预警](https://usercenter2.aliyun.com/home/alarm-threshold)并绑定业务空间标签实现分账 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **地域与部署范围强约束**：免费额度仅限华北2（北京）+中国内地部署范围；其他地域（如美国、新加坡）或全球/国际部署范围的同名模型无免费额度，且价格存在显著差异（如 `qwen3.7-max` 在新加坡单价为 18.736 元/百万Token） [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **额度耗尽后行为差异**：全新未认证用户额度用完将直接返回错误码 `AllocationQuota.FreeTierOnly` 并停止服务；已认证用户若未开启“免费额度用完即停”，则自动切换至按量付费，可能导致账户欠费 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **抵扣顺序刚性**：免费额度、资源包、节省计划的抵扣顺序不可更改；若某模型开启了“免费额度用完即停”，则即使存在未到期的节省计划，服务也会暂停，无法触发后续抵扣 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **欠费影响全局**：账户整体欠费（可用额度 < 0）时，即使其他模型仍有免费额度或节省计划余额，所有服务均会暂停，必须结清欠费方可恢复 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **账单延迟与溯源**：模型推理账单通常在调用结束后 2–10 分钟生成，批量/训练类任务为小时级出账；账单中“计费项”统一显示为“大模型文本消耗量”，须依赖 `实例 ID` 字段中的模型名称进行准确归因 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


