# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署的全链路成本控制机制。其核心围绕免费额度自动抵扣、多层级付费方案（按量/预置/模型单元）、以及精细化账单溯源能力展开，旨在帮助开发者在保障业务连续性的同时实现成本可预测、可监控、可优化。所有计费行为均严格遵循地域隔离原则，且免费额度与正式计费存在明确的适用边界。

## 支持的模型/功能

- **支持免费额度的模型**：仅限华北2（北京）地域的实时推理调用，包括 `qwen-max`、`qwen3.7-plus`、`qwen3.6-plus` 等主流千问系列模型（含带日期后缀的快照版本），以及部分万相、CosyVoice 模型；其他地域（如美国、新加坡、德国、日本）模型**不提供免费额度** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **支持阶梯计费的模型**：千问Max、千问Plus 系列在华北2（北京）等多地支持按单次请求输入 [Token](../concepts/token.md) 数量分档计价（如 0–32K、32K–128K、128K–256K），单价随 [Token](../concepts/token.md) 区间递增 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **支持 Batch 调用半价的模型**：`qwen3.7-max`、`qwen3.6-plus`、`qwen-plus` 等明确标注“[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价”的模型，其输入/输出 [Token](../concepts/token.md) 单价为实时推理价格的 50%；但该优惠与上下文缓存折扣**不能同时生效** [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **不支持免费额度的场景**：模型训练、模型部署、Batch 调用、自定义模型（调优后或已部署模型）均**不可使用免费额度抵扣** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

> **注意**：文档 5 中 `qwen3.7-max` 在华北2（北京）标有“限时5折”，而文档 2 中同模型在部署计费表中未体现该折扣；实际调用价格应以 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md) 的实时推理价格为准，部署计费属独立费用项，二者不冲突。

## 关键参数

- **免费额度有效期**：90 天，自开通百炼、模型发布或申请通过之日三者中最晚时间起算；2025年9月8日11点前开通用户有效期可能不足90天 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **Token 计费粒度**：最小计费单位为 1 Token；训练费用按 `训练Token总量 × 单价` 计算，其中 Token 总量依模型类型（文本/图像/视频/语音）有不同公式，例如万相图生视频为 `∑(视频计费时长) × (max_pixels / 1024) × n_epochs` [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **抵扣优先级顺序**：系统严格按 `免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费` 执行抵扣；同一类型多个计划时，优先消耗先到期者 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **账单出账延迟**：模型推理账单为分钟级（通常 2–10 分钟），批量推理、训练、知识库为小时级；高峰期可能存在进一步延迟 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 使用方式

- **启用免费额度**：无需额外配置，开通百炼后系统自动发放，调用时自动优先抵扣；需确保使用通用 API Key（非 Token Plan/Coding Plan 专属 Key），否则将跳过免费额度直接按量付费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **配置“免费额度用完即停”**：在控制台 [免费额度页面](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota) 或模型详情页开启开关，可防止额度耗尽后意外扣费；该功能默认关闭，开启后需手动关闭才能恢复按量付费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **购买节省计划**：AI 通用型节省计划支持跨模型抵扣，推荐作为首选；购买后立即生效，承诺周期内按“动态月”分配额度（每月独立额度，不可累积）；零预付需联系商务经理开通 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **查询账单与溯源**：通过 [账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail) 页面，按 `实例 ID（出账粒度）` 字段（格式为 `ApiKeyID;业务空间ID;模型名称;...`）精准定位费用归属；模型名称位于分号分隔后的第三字段 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **地域强约束**：免费额度仅华北2（北京）有效；模型训练服务（如 CosyVoice）也仅支持该地域；跨地域调用将无法享受对应优惠或服务 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **额度不互通**：不同模型（含同一模型不同快照版本，如 `qwen-max` 与 `qwen-max-2026-05-17`）的免费额度完全独立，不可合并或转移；额度耗尽后系统**不会自动切换**至其他有额度的模型，需手动修改代码中的 `model` 参数 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费影响全局**：账户欠费时，即使免费额度、节省计划、资源包仍有余额，所有按量付费类服务（含模型推理）将**全部暂停**；仅 Coding Plan/Token Plan 等预付费套餐不受影响 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **部署即计费**：模型部署状态为“运行中”时即开始按时长计费，**与是否发生 API 调用无关**；若不再使用，必须主动下线部署，否则持续产生费用 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


