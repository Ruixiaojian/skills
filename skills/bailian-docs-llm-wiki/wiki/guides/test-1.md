# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，聚焦模型实时推理的费用结构、免费额度机制及成本优化策略。它不涵盖模型训练、部署或知识库等衍生服务的计费逻辑，仅针对标准 API 调用（即 `real-time inference`）场景。所有计费均以 [Token](../concepts/token.md) 为基本单位，输入与输出 [Token](../concepts/token.md) 分别计价，且免费额度、资源包与节省计划按固定优先级自动抵扣。

## 支持的模型/功能

- **适用模型**：仅限百炼平台上架的、支持 OpenAI 兼容 API 的文本生成模型（如 `qwen3.8-max`、`qwen3.7-plus-2026-05-26` 等），且必须为**阿里直供版本**；第三方直供模型（如部分 MiniMax、HappyHorse）暂不支持 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **地域限制**：免费额度**仅在华北2（北京）地域生效**，其他地域（如新加坡、美国弗吉尼亚）无免费额度，但可使用节省计划与资源包 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **功能覆盖**：支持 Batch 调用（单价为实时推理的 50%）、上下文缓存（显式/隐式命中有独立折扣），但**不支持**模型调优、模型部署、PAI-DSW、OSS 存储等场景 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。

> **注意**：文档 5 中列出的 `qwen3.7-max` 在“华北2（北京）”表格中标注“当前能力等同于 `qwen3.7-max-2026-05-20`”，而文档 2 的部署计费表中却将 `qwen3.7-max-2026-05-20` 列为独立模型并给出 PTU 单价。二者未明确说明是否为同一逻辑模型，开发者应以控制台实际模型 ID 和调用返回的 `model` 字段为准，避免因快照版本混淆导致额度误用或计费偏差。

## 关键参数

- **[Token](../concepts/token.md) 计量**：输入 Token 与输出 Token 分开统计，共同消耗免费额度总额（如 `qwen-max` 总额 100 万 Token，输入 + 输出累计扣减）[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **阶梯计费**：部分模型（如 `qwen3-max`、`qwen3.7-plus`）按单次请求输入 Token 总量分档定价，全部 Token 按最高档单价结算（例如输入 100K Token，落在 32K–128K 区间，则全部按该档单价计费）[模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **抵扣优先级**：系统严格按 `免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费` 顺序抵扣费用 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **免费额度用完即停**：开启后，额度耗尽时返回错误码 `AllocationQuota.FreeTierOnly`，服务立即中断；关闭此开关需等待额度完全耗尽且数据同步完成（约半小时延迟）[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 使用方式

1. **开通与生效**：完成实名认证后，系统自动发放华北2（北京）地域模型的免费额度，通常两小时内生效；无需手动领取 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
2. **调用接口**：使用通用 API Key（非 Token Plan/Coding Plan 专属 Key）发起标准 `/v1/chat/completions` 请求，系统自动优先使用免费额度 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
3. **成本优化**：
   - 高频稳定用量：购买 [AI 通用型节省计划](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)，承诺月消费额换取阶梯折扣；
   - 单一模型确定用量：购买对应模型的资源包（如 `qwen-plus` Token 包）；
   - 小额集中用量：选用“其他模型节省计划”（如千问语音模型节省计划）。
4. **监控与告警**：通过控制台 [费用概览](https://bailian.console.aliyun.com/?tab=model#/costing-balance) 查看实时消费，设置月度限额与短信/邮件告警，防止意外超支 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **免费额度限制**：仅抵扣实时推理费用；Batch 调用、模型调优、模型部署、自定义模型（调优后/已部署）均不支持抵扣 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **额度独立性**：不同模型（含带日期后缀的快照版本，如 `qwen3.7-plus-2026-05-26` 与 `qwen3.7-plus`）额度完全独立，不可互通；额度耗尽后不会自动切换至其他有余额的模型，需手动修改代码中的 `model` 参数 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **账户状态影响**：**账户欠费时，即使模型仍有免费额度也无法调用**；所有按量付费类服务（含免费额度、节省计划、资源包）均受账户可用额度约束 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **出账延迟**：模型推理账单为分钟级出账（通常 2–10 分钟），控制台显示的剩余额度亦为分钟级更新，调用前务必手动刷新页面，避免因数据延迟导致误判额度状态 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


