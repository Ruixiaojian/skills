# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署的全链路成本控制机制。其核心围绕免费额度自动抵扣、多层级付费方案（按量/预置/节省计划/资源包）及精细化账单溯源展开，所有费用均以 [Token](../concepts/token.md) 或时长为计量单位，严格区分地域、模型版本与调用场景。开发者需重点关注免费额度的地域限制、抵扣优先级及“免费额度用完即停”功能对服务连续性的影响。

## 支持的模型/功能

- **支持免费额度的模型**：仅限华北2（北京）地域的实时推理调用，包括 `qwen-max`、`qwen3.7-plus-2026-05-26` 等主流文本生成模型，以及部分 ASR 类模型（需在业务空间单独开通权限）[原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **不支持免费额度的场景**：Batch 调用、模型调优、模型部署、PAI-DSW、OSS 存储及自定义模型（如调优后模型、已部署模型）[原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **功能覆盖范围**：支持上下文缓存（显式/隐式）、Batch 调用（单价为实时推理的 50%）、思维链（Thinking）模式等高级能力，但缓存与 Batch 的折扣不可叠加 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。

## 关键参数

- **免费额度参数**：默认 100 万 [Token](../concepts/token.md)/模型，有效期 90 天（自开通/模型发布/申请通过日起算，以较晚者为准），输入与输出 [Token](../concepts/token.md) 共用总额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **阶梯计费参数**：部分模型（如 `qwen3-max`）按单次请求输入 Token 总量分档计价（如 0–32K、32K–128K），该请求全部 Token 均按对应档位单价结算 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。  
- **部署计费参数**：PTU（预置吞吐）按 `输入 TPM × 输入单价 + 输出 TPM × 输出单价` 计费；模型单元（MU）按 `使用时长 × 模型单元数量 × 单价` 计费，支持 PD 分离模式 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

## 使用方式

- **免费额度使用**：无需手动配置，系统自动优先抵扣；必须使用通用 API Key（非 Token Plan/Coding Plan 专属 Key），且调用需在华北2（北京）地域发起 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **付费方案选择**：  
  - 优先选用 **AI 通用型节省计划**（承诺月消费额，最高 5.3 折，覆盖全部阿里直供模型）；  
  - 小规模或模型专用场景可选 **其他模型节省计划**（如千问语音模型、万相模型）或 **资源包**（预购特定模型 Token 数量）；  
  - 抵扣顺序固定：`免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费` [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。  
- **账单查询**：模型推理账单分钟级出账（2–10 分钟），实例 ID 字段格式为 `ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`，用于精准溯源 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- > **注意**：文档 1 与文档 5 对 `qwen3.7-max` 的免费额度有效期描述存在潜在矛盾——文档 1 明确“2025年9月8日11点前开通用户有效期可能不足90天”，而文档 5 仅笼统标注“90天内（以较晚者为准）”。实际生效时间应以开通百炼时系统发放的额度详情页为准，开发者需在控制台免费额度页面核验具体到期日。  
- > **注意**：文档 2 中 `qwen3.7-plus-2026-05-26` 的部署价格（北京地域输入单价 ¥4.8/10K TPM/小时）与文档 5 中同名模型的调用价格（北京地域输入单价 ¥2元/百万Token）属不同计费维度，不可直接比较；前者针对 PTU 部署时长，后者针对实时推理 Token，二者适用场景分离。  
- 免费额度用完后，**全新未认证用户将返回错误码 `AllocationQuota.FreeTierOnly` 并停止服务**，必须完成实名认证并充值方可继续；已认证用户若未开启“免费额度用完即停”，则自动转为按量付费，可能导致意外扣费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- 账户**欠费时，即使模型仍有免费额度也无法调用**；模型部署状态为“运行中”即开始计费，与是否发生 API 调用无关，需主动下线部署以停止计费 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


