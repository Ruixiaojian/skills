# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署的费用结构、免费额度机制及成本优化工具。本文档整合了新人免费额度、模型调用价格、节省计划与资源包、账单查询及模型训练/部署计费五大维度，聚焦华北2（北京）地域的主流文本生成模型（如千问系列），明确各环节的适用范围、生效逻辑与关键约束。所有计费行为均以实际调用结束后的出账为准，开发者需结合免费额度、节省计划与资源包的抵扣优先级进行成本规划。

## 支持的模型/功能

- **支持免费额度的模型**：仅限华北2（北京）地域的实时推理调用，包括 `qwen-max`、`qwen3.7-plus`、`qwen3.6-plus` 等千问系列模型（含带日期后缀的快照版本，如 `qwen3.7-plus-2026-05-26`），以及部分万相、CosyVoice 模型。其他地域（如美国、新加坡、德国）模型**不享有免费额度**，详见[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **支持阶梯计费的模型**：千问Max、千问Plus 系列在华北2（北京）等地域按输入 [Token](../concepts/token.md) 区间分档定价（如 `0<Token≤128K`、`128K<Token≤256K`），单价随用量递增；Batch 调用可享实时推理价格 50% 折扣，但与上下文缓存折扣互斥 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **支持模型训练与部署的模型**：千问、千问VL、万相、CosyVoice、DeepSeek、GLM 等均支持训练与部署，但训练仅限华北2（北京）地域（CosyVoice 明确限定），部署则覆盖多地域 [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

> **注意**：文档 5 中 `qwen3.7-max` 在华北2（北京）标注“当前能力等同于 `qwen3.7-max-2026-05-20`”，而文档 2 的部署计费表中列出 `qwen3.7-max-2026-05-20`，但文档 5 的价格表未包含该精确 ID 的单价。开发者应以控制台实时展示或[模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)中最新快照版本为准，避免使用已归档的别名 ID。

## 关键参数

- **免费额度参数**：默认 100 万 [Token](../concepts/token.md)/模型，有效期 90 天（自开通/模型发布/申请通过日起算，以较晚者为准）；主账号与 RAM 子账号共享额度，不同模型（含快照版本）额度独立 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **[Token](../concepts/token.md) 计费参数**：输入/输出 Token 单价单位为“每百万 Token”，实际费用 = (输入 Token 数 / 1,000,000) × 输入单价 + (输出 Token 数 / 1,000,000) × 输出单价；Batch 调用单价为实时推理单价的 50% [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **部署计费参数**：预置吞吐模式按 TPM（Tokens Per Minute）计费，公式为 `费用 = 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM)`；模型单元模式按 `费用 = 使用时长（小时）× 模型单元数量 × 小时单价` 计算，最小计费单位为分钟 [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **节省计划参数**：AI 通用型节省计划按月承诺消费金额（1000 元起）和周期（3/6/12/24 个月）生效，抵扣顺序为免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 使用方式

- **启用免费额度**：开通百炼服务后自动发放，无需额外操作；调用时系统自动优先抵扣，使用通用 API Key（非 Token Plan/Coding Plan 专属 Key）即可生效 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **配置节省计划**：购买 AI 通用型节省计划后立即生效，自动抵扣模型调用、工具调用、批量推理等费用（不含模型训练、部署、联网搜索[插件](../concepts/plugin.md)）；若开启“免费额度用完即停”，需手动关闭该开关才能触发节省计划抵扣 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **查询与监控**：通过控制台[费用概览](https://bailian.console.aliyun.com/?tab=model#/costing-balance)查看当月总消费；账单明细需在[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)中筛选“大模型服务平台百炼”，解析 `实例 ID（出账粒度）` 字段（格式：`ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`）定位具体模型与调用渠道 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **停止计费**：删除 API Key 防止意外调用；下线已部署模型终止按时长计费；退订预付费实例需在[退订管理](https://usercenter2.aliyun.com/refund/refund)页面操作 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **免费额度限制**：仅抵扣实时推理费用，**不支持 Batch 调用、模型训练、模型部署、自定义模型（调优后/已部署）**；额度过期后自动作废，不可补发或重置；全新未认证用户额度耗尽后直接返回错误码 `AllocationQuota.FreeTierOnly`，需认证并充值方可继续 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **地域与模型绑定限制**：免费额度、CosyVoice 训练、部分模型部署仅限华北2（北京）；美国、新加坡等地域模型虽可调用，但无免费额度且单价不同（如 `qwen3.7-plus-us` 单价高于国内版） [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **抵扣逻辑冲突**：若同时开启“免费额度用完即停”与节省计划，免费额度耗尽后服务将停止，节省计划无法触发抵扣；必须关闭“免费额度用完即停”才能启用节省计划 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **欠费影响**：账户欠费时，**即使免费额度、节省计划、资源包仍有剩余，所有按量付费服务均暂停**；Coding Plan/Token Plan 套餐额度不受影响，但自动续费会失败 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


