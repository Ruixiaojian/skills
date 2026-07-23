# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署的费用结构、成本优化工具（如免费额度、节省计划、资源包）以及账单治理机制。其核心逻辑是：**免费额度优先抵扣实时推理费用 → 其次按需使用资源包或节省计划 → 最终回退至按量付费**。所有计费行为均严格绑定地域、服务部署范围及模型快照版本，开发者需在调用前明确配置并监控额度状态。

## 支持的模型/功能

- **支持免费额度的模型**：仅限华北2（北京）地域且服务部署范围为“中国内地”的模型（如 `qwen3.7-plus-2026-05-26`、`qwen-max`），以及新加坡地域且服务部署范围为“国际”的模型；带日期后缀的快照版本（如 `qwen3.7-max-2026-06-08`）与不带日期的最新版（如 `qwen3.7-max`）视为独立模型，各自拥有独立的 100 万 [Token](../concepts/token.md) 免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **支持阶梯计费的模型**：千问 Max、Plus 等系列模型按单次请求输入 [Token](../concepts/token.md) 总量分档计价（如 `0<Token≤128K`、`128K<Token≤256K`），所有 [Token](../concepts/token.md) 均按所属区间的单价结算 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **支持多种计费模式的模型**：除按 Token 计费外，部分模型（如千问3.7-Max）同时支持「预置吞吐」（按 TPM/小时）和「模型单元」（按算力规格/小时）两种部署计费方式，适用于高并发或长时运行场景 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

## 关键参数

- **免费额度有效期**：90 天，自开通百炼、模型发布或模型申请通过之日三者中较晚者起算；但 **2025年9月8日11点前已开通的用户，有效期可能不足90天** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **抵扣优先级**：系统严格遵循 `免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费` 的顺序进行费用抵扣，该逻辑直接影响成本控制效果 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **账单出账延迟**：大模型推理账单为分钟级出账（通常 2~10 分钟），而批量推理、模型训练、知识库等为小时级出账，高峰期可能存在进一步延迟，查询账单时需预留缓冲时间 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

> **注意**：文档 5 中 `qwen3.7-max` 在华北2（北京）的输入单价标注为“原价12元 限时5折”，而文档 2 中同模型在“[模型部署](../concepts/model-deployment.md)计费”表格里未体现折扣，仅列出原价 ¥28.8/10K TPM。二者适用场景不同（文档 5 针对实时推理调用，文档 2 针对预置吞吐部署），但需警惕混淆——**部署计费不享受文档 5 所述的限时折扣**。

## 使用方式

- **启用免费额度**：无需额外操作，开通百炼后系统自动发放；调用时使用通用 API Key（非 Token Plan/Coding Plan 专属 Key），系统将自动优先抵扣 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **配置成本防护**：建议开启「免费额度用完即停」功能，避免额度耗尽后意外扣费；该功能可在[免费额度页面](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)或模型详情页单独/批量开启。
- **选购成本优化方案**：
  - 通用型场景：优先购买 [AI 通用型节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_GenAI_spn_cn)，承诺月消费金额换取最高 5.3 折，覆盖全部阿里直供模型；
  - 专项高频调用：针对特定模型（如语音、向量、万相）可选「其他模型节省计划」或「资源包」，但折扣力度和灵活性低于通用型；
  - 所有方案购买后立即生效，无需手动绑定模型或 API Key。

## 限制和注意事项

- **免费额度不覆盖场景**：明确不抵扣 Batch 调用、模型调优、[模型部署](../concepts/model-deployment.md)、自定义模型（调优后/已部署）产生的费用，且仅限实时推理 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **账户欠费影响全局服务**：即使某模型仍有剩余额度，只要账户整体欠费（可用额度 < 0），所有按量付费模型调用均会暂停，包括免费额度、节省计划、资源包的抵扣能力 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **地域与部署范围强约束**：免费额度、部分模型价格、节省计划适用地域均存在严格限制（如华北2仅支持中国内地部署范围），跨地域调用或错误配置部署范围将导致额度不可用、价格不匹配等问题。
- **模型单元部署的计费连续性**：[模型部署](../concepts/model-deployment.md)状态为「运行中」即开始计费，与是否发生 API 调用无关；若不再使用，必须主动下线部署，否则持续产生费用 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


