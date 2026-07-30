# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署及成本优化的全链路规则。本文档整合了免费额度、按量计费、节省计划、资源包及账单管理等关键机制，帮助开发者在华北2（北京）等支持地域高效、可控地使用大模型服务。所有计费逻辑均以 [Token](../concepts/token.md) 为基本计量单位，并严格遵循“免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费”的抵扣优先级。

## 支持的模型/功能

- **实时推理**：支持千问（Qwen）、DeepSeek、GLM、万相（WanX）、CosyVoice 等全系列文本、[多模态](../concepts/multi-modal.md)、语音、视频模型的 API 调用，是唯一可被新人免费额度抵扣的场景 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **不支持免费额度的场景**：Batch 调用、模型调优（训练）、模型部署、自定义模型（如调优后或已部署模型）均**不可**使用免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **地域限制明确**：仅华北2（北京）地域的模型享有新人免费额度；美国（弗吉尼亚）、新加坡、德国（法兰克福）、日本（东京）等地域模型虽可调用，但无免费额度，且部分模型（如 `qwen3.7-max-us`）存在专属定价 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- > **注意**：文档 5 中 `qwen3.6-max-preview` 在华北2（北京）标注为“非思考和思考模式”，但在文档 2 的部署计费表中未列出该模型，且其训练单价缺失——该模型可能已下线或不支持部署，实际使用前请以控制台最新模型列表为准。

## 关键参数

- **[Token](../concepts/token.md) 计量**：输入/输出 [Token](../concepts/token.md) 均按百万为单位计费，单价因模型、地域、输入长度区间（阶梯计费）及模式（非思考/思考）而异。例如 `qwen3.7-plus` 在华北2（北京）0–256K 输入区间，非思考模式输入单价为 ¥2/百万 Token，思考模式输出单价为 ¥8/百万 Token [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **免费额度参数**：每个模型（含不同快照版本，如 `qwen-max` 与 `qwen-max-2026-05-17`）独立享有 100 万 Token 免费额度，有效期为开通/发布/申请通过日起 90 天（以较晚者为准），且仅限华北2（北京）地域 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **部署计费参数**：模型部署支持两种模式：  
  - *预置吞吐*：按 TPM（Tokens Per Minute）购买，费用 = 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM)；  
  - *模型单元（MU）*：按算力规格（如 MU2×8）和小时/月计费，适用于对延迟和并发有确定性要求的场景 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

## 使用方式

- **调用即生效**：使用通用 API Key 发起实时推理请求，系统自动按“免费额度 → 资源包 → 节省计划 → 按量付费”顺序抵扣，无需额外配置 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **启用/关闭免费额度保护**：为防止意外扣费，可在控制台免费额度页面为单个或批量模型开启“免费额度用完即停”功能，额度耗尽后返回错误码 `AllocationQuota.FreeTierOnly` [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **成本优化选型**：  
  - 通用型用量推荐 **AI 通用型节省计划**（承诺月消费额，最高 5.3 折，覆盖全部阿里直供模型）；  
  - 高度聚焦单一模型可选 **其他模型节省计划** 或 **资源包**（预购 Token，仅抵扣指定模型）；  
  - 所有方案均需注意抵扣顺序，且“免费额度用完即停”开启时会阻断后续抵扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **账单溯源**：通过账单详情页的 `实例 ID（出账粒度）` 字段（格式为 `ApiKeyID;业务空间ID;模型名称;...`）可精确定位费用归属的模型、API Key 及调用渠道 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **额度不共享、不转移**：主账号与 RAM 子账号共享同一模型的免费额度，但不同模型间额度完全隔离；带日期后缀的快照版本视为独立模型，额度不可互通 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费影响全局**：账户欠费时，即使某模型仍有剩余额度或有效节省计划，所有按量付费类服务（包括实时推理）将暂停，必须结清欠费方可恢复 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **部署即计费**：模型部署状态为“运行中”即开始按时长计费，与是否发生 API 调用无关；务必及时下线闲置部署以避免持续扣费 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- > **注意**：文档 3 明确指出 AI 通用型节省计划**不支持抵扣模型调优、模型部署费用**，但文档 2 中模型训练与部署计费表未对此做交叉引用提示——开发者需主动区分“推理”与“训练/部署”两类费用，避免误判成本覆盖范围。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


