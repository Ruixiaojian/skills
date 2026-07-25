# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理能力集合，涵盖新人免费额度、按量调用、模型训练/部署、节省计划及成本管控等全链路机制。其设计目标是为不同规模和阶段的模型应用提供灵活、透明、可预测的成本模型，支持从快速验证到规模化生产的平滑演进。所有能力均以华北2（北京）地域为默认基准，跨地域使用需注意价格与额度差异。

## 支持的模型/功能

- **实时推理**：支持千问（Qwen）、GLM、DeepSeek、Kimi 等主流文本生成模型，以及千问VL、万相（WanX）等多模态模型，覆盖文本、图像、视频、语音全模态。具体模型列表及能力详见 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **模型训练**：支持文本生成（千问系列）、图像生成（万相）、视频生成（万相）三类模型的微调，按训练[Token](../concepts/token.md)总量计费，不支持免费额度抵扣 [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **[模型部署](../concepts/model-deployment.md)**：提供两种计费模式：**预置吞吐**（按TPM时长）和**模型单元**（按算力规格小时），均不支持免费额度抵扣 [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **上下文缓存**：部分模型（如 `qwen3.7-max`）支持显式/隐式缓存，缓存命中的[Token](../concepts/token.md)单价显著低于标准输入单价，但本文档价格表中未包含缓存专属单价 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。

> **注意**：文档 5 中 `qwen3.6-max-preview` 在“华北2（北京）”表格中标注为“非思考和思考模式”，但在“新加坡”表格中同一模型标注为“国际”部署范围且仅支持“非思考和思考模式”；而文档 2 的[模型部署](../concepts/model-deployment.md)计费表格中明确将 `qwen3.6-max-preview` 归入 C 类（不支持 AI 通用型节省计划抵扣）。这表明该模型在不同地域的服务能力和计费归属存在不一致，开发者应以控制台实时展示为准，并优先参考 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md) 中对应地域的最新说明。

## 关键参数

- **免费额度**：默认为 100 万 [Token](../concepts/token.md)/模型，仅限华北2（北京）地域的实时推理调用，有效期 90 天（自开通/模型发布/申请通过日起较晚者计算）[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **Token 计价粒度**：输入/输出 Token 均按百万（1M）为单位计费，部分模型（如 `qwen3.6-plus`）实行阶梯计费，单价取决于单次请求的总输入Token数。
- **地域参数**：价格、免费额度、节省计划适用地域均强绑定地域。例如，`qwen-max` 在华北2（北京）输入单价为 2.4 元/M，而在新加坡为 11.743 元/M；AI 通用型节省计划仅支持华北2（北京）、美国（弗吉尼亚）、新加坡等指定地域 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **抵扣优先级**：系统自动按固定顺序消耗资源：**免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费**。此顺序不可更改，是成本优化策略的基础 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 使用方式

- **调用模型**：使用通用 API Key 发起 HTTP 请求，系统自动优先消耗免费额度。专属 API Key（如 Token Plan/Coding Plan 专属）不参与免费额度抵扣，需改用通用 Key [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **启用节省计划**：购买 AI 通用型节省计划后，无需手动绑定，系统自动按抵扣顺序生效。若已开启“免费额度用完即停”，需手动关闭该开关才能触发后续抵扣 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **查询用量**：实时推理用量可在控制台「模型用量」页面查看（T+1 小时更新）；免费额度余量需在「免费额度」页面手动刷新，为分钟级延迟 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **账单溯源**：通过账单详情页的「实例 ID（出账粒度）」字段（格式：`ApiKeyID;业务空间ID;模型名称;...`）可精确追溯每笔费用对应的模型、API Key 和调用渠道 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **免费额度限制**：不覆盖 Batch 调用、模型训练、[模型部署](../concepts/model-deployment.md)、自定义模型（调优后/已部署）等场景。主账号与 RAM 子账号共享额度，但不同模型（含快照版本）额度完全独立 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费影响**：账户欠费时，**所有按量付费服务（包括仍有剩余额度的模型）将立即暂停**。Coding Plan/Token Plan 等预付费套餐不受影响，但自动续费会失败 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **模型部署持续计费**：只要部署状态为“运行中”，无论是否有 API 调用，均按时长计费。必须主动「下线」模型才能停止计费 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **价格时效性**：文档 5 中大量标有“限时5折”“限时8折”的价格，属于活动优惠，原价以控制台实时展示为准。所有价格均不含上下文缓存等附加功能的专项单价 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


