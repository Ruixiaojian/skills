# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，聚焦模型实时推理的费用构成、抵扣机制及成本控制策略。其核心围绕新人免费额度、按量计费模型价格、节省计划与资源包等多层成本优化工具展开，所有计费行为均以 [Token](../concepts/token.md) 消耗为基本计量单位，并严格区分实时推理、批量调用、模型训练与部署等不同场景。开发者需特别注意地域限制（如免费额度仅限华北2）、额度优先级规则（免费额度 > 资源包 > 节省计划 > 按量付费）以及服务状态对计费的影响（如欠费将全局阻断调用）。

## 支持的模型/功能

- **支持实时推理的模型**：包括千问系列（Qwen3.x Max/Plus/Flash 等）、DeepSeek、GLM、万相（图像/视频生成）、CosyVoice（语音合成）等主流模型，覆盖文本、多模态、语音、视频等模态。具体模型列表及地域支持情况请参见 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **不支持免费额度的场景**：Batch 调用、模型调优、[模型部署](../concepts/model-deployment.md)、PAI-DSW、OSS 存储及请求费用等明确排除在免费额度适用范围之外，详见 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **地域限制**：新人免费额度**仅限华北2（北京）地域**模型享有；部分模型（如 CosyVoice 调优）也仅支持该地域，参见 [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

> **注意**：文档 5 中 `qwen3.7-max` 在华北2（北京）标注为“当前能力等同于 `qwen3.7-max-2026-05-20`”，而文档 2 的部署价格表中同时列出了 `qwen3.7-max-2026-05-20` 和 `qwen3.7-Max-2026-05-20`（大小写不一致），且后者在部署价格表中未见对应训练价格。实际使用应以控制台显示的 Model ID 为准，避免因命名差异导致调用失败或计费异常。

## 关键参数

- **[Token](../concepts/token.md) 计量**：输入与输出 [Token](../concepts/token.md) 共享同一免费额度总额度，不单独区分；调用产生的总 Token 数（含 [prompt](prompt.md) + response）共同扣减。
- **免费额度有效期**：90 天，自开通百炼、模型发布或模型申请通过之日三者中**最晚者**起算；2025年9月8日11点前开通用户有效期可能不足90天，详见 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **抵扣优先级**：系统严格按 `免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费` 顺序抵扣费用，此逻辑适用于所有计费项。
- **模型快照独立性**：带日期后缀的模型（如 `qwen-max-2026-05-17`）与无后缀版本（如 `qwen-max`）视为**完全独立模型**，各自拥有独立免费额度与计费规则，不可互通。

## 使用方式

- **自动启用免费额度**：首次完成实名认证并开通百炼后，系统自动发放额度，无需手动领取；仅需使用通用 API Key（非 Token Plan/Coding Plan 专属 Key）调用华北2（北京）地域的实时推理接口即可自动抵扣。
- **配置“免费额度用完即停”**：可在控制台 [免费额度页面](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota) 或 [模型广场详情页](https://bailian.console.aliyun.com/?tab=model#/model-market/detail/) 开启该功能，额度耗尽时返回错误码 `AllocationQuota.FreeTierOnly`，防止意外扣费。
- **购买节省计划**：推荐优先选用 [AI 通用型节省计划](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)，其可跨模型抵扣全部阿里直供模型的推理费用，折扣力度最高达 5.3 折；其他模型节省计划（如千问语音模型）仅限特定模型系列。
- **查询与分账**：通过 [账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail) 页面，依据 `实例 ID（出账粒度）` 字段（格式：`ApiKeyID;业务空间ID;模型名称;...`）精准定位费用归属；绑定业务空间标签可实现按部门/项目分账。

## 限制和注意事项

- **地域与模型绑定**：免费额度、部分模型训练能力（如 CosyVoice）、以及部分节省计划适用地域均存在严格限制。例如，[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md) 明确指出“仅华北2（北京）地域模型享有免费额度”，其他地域模型调用直接按量计费。
- **欠费全局阻断**：账户可用额度 < 0 时，**即使模型仍有剩余额度或有效节省计划，所有按量付费类服务（含推理）将立即暂停**，必须结清欠费方可恢复。
- **额度不可转移与重置**：免费额度到期自动作废，不支持补发、延期或重置；同一实名主体下重新注册账号无法再次领取；主账号与 RAM 子账号共享额度，但不同模型间额度完全隔离。
- **部署与推理分离计费**：[模型部署](../concepts/model-deployment.md)（PTU/模型单元）按使用时长计费，与实时推理的 Token 计费完全独立；部署状态为“运行中”即开始计费，与是否发生 API 调用无关，详见 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


