# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖新人免费额度、模型调用定价、节省计划、资源包及账单管理等关键能力。其设计目标是为开发者提供透明、可预测且灵活的成本控制机制，支持从免费试用到规模化生产的平滑演进。所有计费行为均基于实际用量（[Token](../concepts/token.md)、TPM、时长等）自动结算，且严格遵循地域隔离与模型独立性原则。

## 支持的模型/功能

- **模型类型**：覆盖文本生成（千问系列、DeepSeek、GLM）、多模态（千问VL）、图像生成（万相）、视频生成（万相）、语音合成与识别（CosyVoice、Qwen-TTS、Paraformer）等全栈大模型服务。
- **核心功能**：实时推理（按量计费）、Batch调用（部分模型支持50%折扣）、模型训练（按训练[Token](../concepts/token.md)计费）、[模型部署](../concepts/model-deployment.md)（按TPM或模型单元计费）、上下文缓存（显式/隐式缓存，单价独立）、联网搜索插件（独立计费，不纳入节省计划抵扣范围）[原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **地域支持**：华北2（北京）为默认主地域，享有完整免费额度与计费能力；美国（弗吉尼亚）、新加坡、德国（法兰克福）、日本（东京）等国际地域支持部分模型，但免费额度仅限华北2（北京）[原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。> **注意**：文档5中“德国（法兰克福）”章节存在矛盾——同一 `qwen3-max` 模型在“全球”和“欧盟”服务部署范围下给出了两套不同单价（如0<[Token](../concepts/token.md)≤32K输入单价分别为2.5元与8.993元），实际生效价格以控制台实时展示为准，建议以[模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)中“华北2（北京）”列为基准参考。

## 关键参数

- **免费额度**：每个模型（含带日期后缀的快照版本）独立发放100万Token，有效期90天（自开通/模型发布/申请通过日起算，以较晚者为准），仅抵扣实时推理费用，不支持Batch调用、模型训练或部署 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **计费粒度**：
  - 推理：输入/输出Token（百万Token为单位）、上下文缓存Token（单独计价）；
  - 部署：TPM（每10K/小时）、模型单元（MU规格×小时）、预置吞吐（按天）；
  - 训练：训练Token总量（千Token为单位），计算公式因模型类型而异（如文本模型=数据Token×循环次数，视频模型=∑视频时长×max_pixels/1024×n_epochs）[原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **抵扣优先级**：免费额度 > 资源包 > 其他模型节省计划 > AI通用型节省计划 > 按量付费，该顺序不可更改 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 使用方式

- **开通与查看**：首次开通百炼即自动发放华北2（北京）地域模型的免费额度；剩余额度可通过控制台[免费额度页面](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)或[模型广场详情页](https://bailian.console.aliyun.com/?tab=model#/model-market/detail/)实时查询（分钟级更新，需手动刷新）。
- **调用与抵扣**：使用通用API Key发起实时推理调用，系统自动按优先级抵扣额度；专属API Key（如Token Plan/Coding Plan）不消耗免费额度，需切换为通用Key才能启用 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **成本优化**：
  - 优先选用AI通用型节省计划（承诺月消费额，最高5.3折，覆盖全部阿里直供模型）；
  - 小规模或单一模型场景可选其他模型节省计划或资源包；
  - 开启“免费额度用完即停”功能防止意外扣费（需在免费额度页面或模型详情页手动开启）[原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **账单管理**：推理账单分钟级出账（2~10分钟），训练/批量任务小时级出账；关键字段“实例 ID（出账粒度）”以`;`分隔，格式为`ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`，用于精准溯源 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **地域限制**：免费额度、部分模型训练（如CosyVoice）及多数计费能力仅限华北2（北京）地域；国际地域模型价格普遍高于国内，且无免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **额度隔离**：不同模型（含快照版本）、主账号与RAM子账号间额度完全独立，不互通、不共享；额度过期后自动作废，不支持补发或延期 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费影响**：账户欠费时，即使免费额度或节省计划仍有余额，所有按量付费服务（含推理、部署）将暂停；Coding Plan/Token Plan等预付费套餐不受影响，但自动续费会失败 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **功能排除**：免费额度、节省计划、资源包均**不支持抵扣**模型训练、[模型部署](../concepts/model-deployment.md)、联网搜索插件、MCP广场、通义深度搜索、案例检索等费用；知识库规格费用（如RCU/小时）亦不在抵扣范围内 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


