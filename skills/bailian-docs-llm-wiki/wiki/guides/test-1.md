# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与成本管理主题，涵盖模型调用、训练、部署的定价规则，以及免费额度、节省计划、资源包等成本优化工具。本文档整合了官方最新计费策略，重点说明华北2（北京）地域的通用规则，并明确各计费模式的适用边界与抵扣逻辑。开发者需特别注意免费额度的地域限制、模型快照版本的独立性，以及不同计费方式（如PTU、模型单元、按量）的并存关系。

## 支持的模型/功能

百炼平台支持文本生成（千问系列）、多模态（千问VL）、图像生成（万相）、视频生成（万相）及语音合成（CosyVoice）等模型的调用与训练。其中，**千问系列模型（如 `qwen3.7-plus-2026-05-26`、`qwen3-vl-8b-instruct`）和万相系列（如 `wan2.7-image-pro`、`wan2.7-i2v`）是当前主力支持模型**，覆盖从轻量级到超大规模的多种规格 [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。语音合成模型（CosyVoice）仅支持华北2（北京）地域 [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。所有模型均支持按量调用，部分模型（如 `qwen3.8-max`）支持 Batch 调用（单价为实时推理的 50%）和上下文缓存（显式/隐式缓存有独立计价） [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。

> **注意**：文档 1 中列出的 `Qwen3.7-Plus-2026-05-26` 在模型部署计费表中输入单价为 ¥4.8/10K TPM/小时，而文档 5 中同名模型在华北2（北京）的输入单价为 ¥2/百万 [Token](../concepts/token.md)（即 ¥0.002/10K [Token](../concepts/token.md)），二者单位与计费维度完全不同（TPM vs [Token](../concepts/token.md)），不构成矛盾，但开发者必须严格区分“部署”与“调用”两种场景——前者按吞吐量（TPM）或算力单元（MU）计费，后者按实际消耗 Token 计费。

## 关键参数

- **Token 计费**：模型调用按输入/输出 Token 数量计费，单价以“每百万 Token”为单位（如 `qwen-plus` 输入 ¥0.8/百万 Token） [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)；模型训练则按训练 Token 总量计费（如 `qwen3-vl-8b-instruct` ¥0.012/千 Token） [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **阶梯计费**：部分模型（如 `qwen3-max`）按单次请求输入 Token 总量分档定价，例如 0–32K、32K–128K、128K–256K 区间对应不同单价，**整个请求的所有 Token 均按所属最高档单价结算** [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **地域与部署范围**：免费额度、部分模型服务及价格仅限华北2（北京）地域；新加坡、美国（弗吉尼亚）等地域价格不同，且部分模型（如 `qwen3.7-plus-us`）为地域专属版本 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **免费额度有效期**：自开通百炼、模型发布或申请通过日起 90 天（以较晚者为准），到期自动作废，不支持延期或重置 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 使用方式

1. **调用计费**：使用通用 API Key 发起实时推理调用，系统自动按优先级抵扣：免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)；Batch 调用需显式指定 `batch` 接口，享受半价优惠 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
2. **成本优化**：
   - **AI 通用型节省计划**：承诺月消费金额（1000 元起），按周期（3/6/12/24 个月）购买，可跨模型抵扣 A/B/C 类模型调用费用，折扣最高达 5.3 折，是首选方案 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
   - **资源包**：预购特定模型（如 `qwen-plus`）的 Token 数量，仅用于抵扣该模型超出免费额度后的用量，无折扣 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
3. **账单查询**：调用结束后 2–10 分钟生成推理账单，字段 `实例 ID（出账粒度）` 以分号 `;` 分隔，格式为 `ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`，可用于精准溯源 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **免费额度限制**：仅适用于华北2（北京）地域的实时推理调用，**不支持抵扣模型调优、模型部署、Batch 调用及自定义模型（调优后/已部署模型）** [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)；同一实名主体下主账号与 RAM 子账号共享额度，但不同模型（含带日期后缀的快照版本）额度完全独立 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **地域锁定**：CosyVoice 模型调优仅支持华北2（北京）；万相视频生成模型（如 `wan2.7-i2v`）的计费时长上限为 10 秒/条（`wan2.2` 系列为 5 秒） [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **欠费影响**：账户欠费时，**即使模型仍有免费额度，所有按量付费服务（含推理、部署）将暂停**；已购 Coding Plan 或 Token Plan 套餐不受欠费影响，但自动续费会失败 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **部署即计费**：模型部署状态为“运行中”时即开始按时长计费，与是否发生 API 调用无关；停止计费需主动下线部署或删除 API Key [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


