# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署的全链路成本控制机制。其核心围绕免费额度自动抵扣、多层级付费方案（按量、资源包、节省计划）及精细化账单溯源能力展开，适用于从新手试用到企业级规模化部署的各类场景。所有计费行为均严格遵循地域与服务部署范围约束，华北2（北京）为中国内地服务的默认且唯一支持免费额度的地域。

## 支持的模型/功能

- **实时推理**：支持千问（Qwen）、DeepSeek、GLM、Kimi、MiniMax 等主流文本生成模型，以及千问VL、万相（WanX）等多模态模型，覆盖非思考/思考模式、Batch调用（半价）、上下文缓存等特性 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **模型训练**：支持文本生成（千问）、图像生成（万相）、视频生成（万相）三类模型微调，按训练[Token](../concepts/token.md)总量计费，计算逻辑依赖 `max_steps`、`Lstep` 或 `视频计费时长 × max_pixels × n_epochs` 等超参 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **模型部署**：提供两种计费模式：  
  - *预置吞吐*：按输入/输出TPM（每分钟[Token](../concepts/token.md)数）与时长计费；  
  - *模型单元（MU）*：按算力规格（如 MU1 x 8）与使用时长（小时/月）计费，支持PD分离模式降低首[Token](../concepts/token.md)延迟 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **成本优化工具**：支持AI通用型节省计划（跨模型、阶梯折扣）、其他模型节省计划（单模型、无折扣）、资源包（指定模型Token量）三类预购方案，抵扣顺序为：免费额度 > 资源包 > 其他模型节省计划 > AI通用型节省计划 > 按量付费 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

> **注意**：文档 5 中 `qwen3.7-max` 在华北2（北京）标注“当前能力等同于 `qwen3.7-max-2026-05-20`”，但文档 2 的部署计费表中 `qwen3.7-max-2026-05-20` 被列为独立模型代码，且其部署单价（¥28.8/10K TPM/小时）与文档 5 中 `qwen3.7-max` 的输入单价（原价12元/百万Token）无直接换算关系。开发者需以控制台实际模型列表为准，避免因快照版本别名导致的配置错误。

## 关键参数

- **免费额度**：默认100万Token/模型，仅限华北2（北京）地域+中国内地部署范围，有效期90天（自2025年9月8日11点起新用户），不同模型（含带日期后缀的快照）额度完全独立 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **Token单价**：按地域与模型ID差异化定价，例如 `qwen3.7-plus` 在华北2（北京）非思考模式下，0–256K输入Token单价为¥2/百万Token；同一模型在新加坡地域单价升至¥2.936/百万Token [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **TPM阈值**：部署时需指定输入/输出TPM上限，超出后自动降级至按量付费模式，并在响应Header中返回 `x-dashscope-ptu-overflow:true` [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **节省计划承诺周期**：AI通用型节省计划以“动态月”为单位（非自然月），每月额度独立清零，不累积；例如3个月¥1000/月计划，每月仅可用¥1000，而非总计¥3000 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 使用方式

1. **启用免费额度**：开通百炼后自动发放，无需额外操作；调用时系统自动优先抵扣，无需切换API Key [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
2. **配置成本控制**：
   - 开启“免费额度用完即停”防止意外扣费（控制台 > 免费额度页面或模型详情页）；
   - 购买AI通用型节省计划（推荐）或资源包，购买后立即生效，自动按抵扣顺序结算 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
3. **调用与监控**：
   - 使用通用API Key（非Token Plan/Coding Plan专属Key）确保免费额度生效；
   - 通过[费用概览](https://bailian.console.aliyun.com/?tab=model#/costing-balance/overview)查看实时消费，通过[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)按 `ApiKeyID;业务空间ID;模型名称` 字段精准溯源费用 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **地域强约束**：免费额度、部分模型部署及节省计划仅支持华北2（北京）；美国、新加坡等地域虽可调用模型，但无免费额度，且价格显著上浮（如 `qwen3.7-plus` 新加坡输入单价¥2.936 vs 北京¥2）。
- **额度不互通**：同一账号下主账号与RAM子账号共享免费额度，但不同模型（如 `qwen-max` 与 `qwen-max-2026-05-17`）额度完全隔离，系统不会自动切换 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费影响全局**：账户欠费时，即使某模型仍有免费额度或节省计划余额，所有服务将暂停，必须结清欠费才能恢复 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **出账延迟**：模型推理账单分钟级生成（通常2–10分钟），批量推理、训练、知识库账单则为小时级，查询账单需预留缓冲时间 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


