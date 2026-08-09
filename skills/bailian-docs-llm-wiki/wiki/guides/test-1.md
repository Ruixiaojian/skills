# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署及成本优化的全链路规则。本文档聚焦实时推理（即模型调用）场景，系统梳理免费额度、按量计费、节省计划与资源包等关键机制，帮助开发者准确预估成本、规避意外扣费，并高效配置资源。所有规则均以华北2（北京）地域为默认基准，其他地域存在显著差异，需特别注意。

## 支持的模型/功能

`test 1` 主要覆盖百炼平台上所有支持**实时推理调用**的模型，包括千问（Qwen）、DeepSeek、GLM、千问VL、万相（WanX）、CosyVoice 等系列。其中，文本生成模型（如 `qwen3.8-max`、`qwen-plus`）和[多模态](../concepts/multimodal.md)模型（如 `qwen3-vl-plus-2025-09-23`）是主力应用场景。ASR 类模型需在控制台业务空间中**逐一开通权限**后方可调用并消耗免费额度 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。需特别注意：**免费额度仅适用于实时推理调用**，明确不支持 Batch 调用、模型调优、模型部署、PAI-DSW、OSS 存储等场景 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。

> **注意**：文档 5 中列出的 `qwen3.7-max` 和 `qwen3.7-plus` 等模型，在“华北2（北京）”地域的价格表中均标注“当前能力等同于”某快照版本（如 `qwen3.7-max-2026-05-20`），而文档 2 的模型部署价格表中则直接列出快照版本（如 `qwen3.7-max-2026-05-20`）。这表明平台实际计费与调用均以具体快照版本为准，而非泛指的 `qwen3.7-max`。开发者应始终使用带日期后缀的精确模型 ID 进行调用和计费核对，避免因版本模糊导致预期偏差。

## 关键参数

- **[Token](../concepts/token.md) 计费粒度**：输入与输出 [Token](../concepts/token.md) 分别计费，单价单位为“每百万 [Token](../concepts/token.md)”。阶梯计费依据单次请求的**输入 Token 总量**确定档位，该请求所有 Token 均按对应档位单价结算 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **免费额度参数**：每个模型（含不同快照版本）拥有独立的 100 万 Token 免费额度，有效期为 90 天（自开通百炼、模型发布或申请通过日起算，以较晚者为准）[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **地域参数**：免费额度**仅限华北2（北京）地域**；模型调用价格因地域（如美国、新加坡、德国、日本）而异，同一模型在不同地域价格可能相差数倍 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **抵扣优先级**：费用抵扣严格遵循顺序：**免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费** [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 使用方式

1. **开通与初始化**：完成实名认证后，访问[华北2（北京）地域百炼控制台](https://bailian.console.aliyun.com/#/model-market)，阅读并同意协议，系统将自动发放免费额度，无需手动领取 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
2. **调用模型**：使用通用 API Key（非 Token Plan/Coding Plan 专属 Key）发起 HTTP 请求，系统自动优先使用免费额度抵扣 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。示例请求中需指定 `model` 参数为精确模型 ID（如 `qwen3.7-plus-2026-05-26`）。
3. **成本优化**：
   - 对于稳定用量，优先购买 **AI 通用型节省计划**，承诺月消费额可享最高 5.3 折，且覆盖全部阿里直供模型 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
   - 对于特定模型的确定性用量，可选购对应模型的**资源包**（预购 Token 数量）或**其他模型节省计划**。
4. **监控与告警**：通过控制台的[免费额度页面](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)或[模型用量页面](https://bailian.console.aliyun.com/?tab=model#/model-usage)实时查看剩余额度；在[费用概览](https://bailian.console.aliyun.com/?tab=model#/costing-balance)中设置月度消费限额与告警，防止欠费停服 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **免费额度限制**：全新未认证用户额度耗尽后将返回错误码 `AllocationQuota.FreeTierOnly` 并停止服务；已认证用户若未开启“免费额度用完即停”，则会自动转为按量付费，可能导致账户欠费 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。账户欠费时，**即使其他模型仍有免费额度也无法调用** [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **地域与模型绑定**：免费额度、部分模型（如 CosyVoice 调优）及价格均严格绑定地域。例如，CosyVoice 模型调优服务**仅支持华北2（北京）地域** [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **额度与功能隔离**：免费额度、资源包、节省计划三者互不兼容，不能叠加使用。例如，开启“免费额度用完即停”后，服务将停止，此时节省计划无法生效 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **账单延迟**：模型推理账单为分钟级出账（通常 2~10 分钟），批量推理、训练等为小时级出账。调用后立即查不到账单属正常现象 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


