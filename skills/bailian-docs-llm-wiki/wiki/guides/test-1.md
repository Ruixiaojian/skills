# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖新人免费额度、模型调用与训练部署的计费规则、成本优化方案（节省计划/资源包）以及账单管理全流程。所有计费行为均基于实际 [Token](../concepts/token.md) 消耗、使用时长或资源量，按地域（如华北2北京、新加坡等）独立结算。开发者需特别注意免费额度的地域限制、抵扣优先级及服务状态对计费的影响。

## 支持的模型/功能

- **支持免费额度的模型**：仅限华北2（北京）地域的实时推理调用，包括 `qwen-max`、`qwen3.7-plus-2026-05-26` 等主流千问系列模型，以及部分 ASR 类模型（需在业务空间中单独开通权限）[原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **不支持免费额度的场景**：Batch 调用、模型调优、模型部署、PAI-DSW、OSS 存储及自定义模型（如调优后模型、已部署模型）均不可抵扣免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **模型覆盖范围**：AI 通用型节省计划可抵扣全部阿里直供模型（A 类：千问、向量、排序；B 类：图像/语音/视频；C 类：DeepSeek、GLM 等直供版本），但第三方直供模型（如 MiniMax、HappyHorse）暂不支持 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

> **注意**：文档 5 中 `qwen3.7-max` 在华北2（北京）标注为“当前能力等同于 `qwen3.7-max-2026-05-20`”，而文档 2 的部署计费表中同时列出了 `qwen3.7-max-2026-05-20` 和 `qwen3.7-Max-2026-05-20`（大小写不一致）。实际调用应以控制台模型广场显示的 Model ID 为准，建议以 `qwen3.7-max-2026-05-20` 为标准写法，避免因大小写导致 404 错误。

## 关键参数

- **免费额度参数**：默认 100 万 [Token](../concepts/token.md)/模型，有效期 90 天（自开通百炼、模型发布或申请通过日起算，以较晚者为准）；主账号与 RAM 子账号共享额度，不同模型（含快照版本如 `qwen-max-2026-05-17`）额度独立 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **[Token](../concepts/token.md) 计费参数**：输入/输出 Token 单价按百万 Token 计，部分模型（如 `qwen3.6-max-preview`）实行阶梯计费（如 0–128K、128K–256K 区间单价不同），且 Batch 调用享 50% 折扣 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。  
- **部署计费参数**：PTU（预置吞吐）按 TPM（Tokens Per Minute）和使用时长计费；模型单元（MU）按规格（如 MU1×8）和小时/月计费；视频训练按 `计费时长 × (max_pixels/1024) × n_epochs` 计算 Token 总量 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

## 使用方式

- **免费额度启用**：首次实名认证并开通百炼后自动发放，无需手动领取；调用时系统自动优先抵扣，无需配置 API Key [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **节省计划生效**：购买 AI 通用型节省计划后立即生效，抵扣顺序为 `免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费`；若开启“免费额度用完即停”，需手动关闭该开关才能触发节省计划抵扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。  
- **账单查询路径**：模型推理账单在 `实例 ID（出账粒度）` 字段中以分号 `;` 分隔，格式为 `ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`，可用于精准溯源费用归属 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **地域限制**：免费额度仅华北2（北京）有效；模型部署与训练计费因地域（如北京、新加坡、美国）价格差异显著，需明确 Base URL 对应地域 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **额度耗尽影响**：全新未认证用户额度用尽后返回错误码 `AllocationQuota.FreeTierOnly`，必须认证+充值；已认证用户若未开启“免费额度用完即停”，将直接按量扣费，可能导致账户欠费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **欠费连锁反应**：账户欠费时，即使免费额度、节省计划或资源包仍有余额，所有按量付费服务（含模型推理）均暂停，需结清欠费后恢复 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。  
- **出账延迟**：模型推理账单分钟级出账（通常 2–10 分钟），训练/批量任务小时级出账；账单中“大模型文本消耗量”不直接显示模型名，须解析 `实例 ID` 字段第三位获取模型名称 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


