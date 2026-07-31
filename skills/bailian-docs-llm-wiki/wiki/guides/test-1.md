# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署的费用结构，以及免费额度、节省计划、资源包等成本优化机制。本文档聚焦于华北2（北京）地域的通用规则，所有计费行为均以实际调用结束后的账单为准，且严格遵循“免费额度 > 资源包 > 节省计划 > 按量付费”的抵扣优先级。开发者需特别注意地域限制、额度有效期及服务状态对计费的影响。

## 支持的模型/功能

- **支持免费额度的模型**：仅限华北2（北京）地域的实时推理调用，包括 `qwen-max`、`qwen3.7-plus`、`qwen3.6-plus` 等主流千问系列模型（含快照版本），以及部分万相、CosyVoice模型。不同模型（含带日期后缀的快照版本）额度完全独立，不互通 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **不支持免费额度的场景**：Batch调用、模型调优、[模型部署](../concepts/model-deployment.md)、自定义模型（如调优后或已部署模型）均不可抵扣免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **支持阶梯计费的模型**：千问Max、千问Plus等文本生成模型按单次请求输入[Token](../concepts/token.md)总量分档计价（如0–32K、32K–128K），所有[Token](../concepts/token.md)统一按所在区间单价结算 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **地域差异**：同一模型在不同地域价格不同（如 `qwen3.7-plus` 在北京为2元/百万[Token](../concepts/token.md)输入，美国为2.998元），且仅北京和新加坡地域提供新人免费额度 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。

> **注意**：文档5中 `qwen3.7-max` 在北京的输入单价标注为“原价12元 限时5折”，而文档2中同[模型部署](../concepts/model-deployment.md)计费表未体现折扣；实际调用价格应以[模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)为准，部署计费表仅反映算力单元或TPM模式下的定价，二者适用场景不同，不构成矛盾。

## 关键参数

- **免费额度参数**：默认100万Token/模型，有效期90天（自开通/模型发布/申请通过日起较晚者计算），主账号与RAM子账号共享额度，但不同模型额度隔离 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **Token计费粒度**：模型调用按输入Token与输出Token分别计费，单位为“每百万Token”；模型训练按训练Token总量计费，单位为“每千Token”；[模型部署](../concepts/model-deployment.md)按TPM（Tokens Per Minute）或模型单元（MU）计费 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **抵扣顺序参数**：系统强制执行 `免费额度 > 资源包 > 其他模型节省计划 > AI通用型节省计划 > 按量付费` 的抵扣链，该逻辑直接影响费用归属与账单解析 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **账单延迟参数**：模型推理账单分钟级出账（通常2–10分钟），批量推理、训练、知识库账单小时级出账；账单字段中“实例ID（出账粒度）”以分号`;`分隔，格式为`ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识` [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 使用方式

- **启用免费额度**：开通百炼服务后自动发放，无需额外操作；调用时使用通用API Key（非Token Plan/Coding Plan专属Key），系统自动优先抵扣 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **配置成本优化**：
  - 优先选用[AI通用型节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_GenAI_spn_cn)，承诺月消费金额可享最高5.3折，覆盖全部阿里直供模型；
  - 针对特定模型高频调用场景，可选“其他模型节省计划”或“资源包”，但折扣力度与灵活性低于AI通用型；
  - 所有节省计划/资源包购买后立即生效，无需绑定或激活 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **查询与监控**：
  - 免费额度余量：控制台[免费额度页面](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)或模型广场详情页查看；
  - 实时用量与调用记录：[模型用量](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/usage-statistics)与[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面（数据按小时更新）；
  - 详细账单：[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面筛选“大模型服务平台百炼”，导出后按“实例ID”字段解析模型与调用渠道 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **地域强约束**：免费额度仅适用于华北2（北京）地域模型；模型训练服务（如CosyVoice）也限定在北京地域；跨地域调用将无法享受额度且价格不同 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **额度耗尽风险**：若开启“免费额度用完即停”，额度耗尽后返回错误码 `AllocationQuota.FreeTierOnly`，服务中断；未开启则自动转为按量付费，可能引发欠费——**账户欠费时，即使其他模型仍有剩余额度也无法调用** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **部署即计费**：模型部署状态为“运行中”即开始计费（按TPM或模型单元时长），与是否发生API调用无关；停止计费必须主动下线部署或删除API Key [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **账单归因复杂性**：同一模型一次调用会产生多行账单（输入Token、输出Token、缓存命中等），需依赖“实例ID”字段精确识别；联网搜索等插件费用独立计费，不纳入节省计划抵扣范围 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


