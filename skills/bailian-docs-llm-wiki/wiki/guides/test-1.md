# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖新人免费额度、模型调用定价、训练与部署计费、成本优化方案（节省计划/资源包）及账单管理全流程。其设计目标是为开发者提供清晰、可预测、可管控的模型服务使用成本模型，所有计费行为均基于实际用量（[Token](../concepts/token.md)、TPM、时长等）自动结算，并严格遵循地域隔离与模型独立性原则。

## 支持的模型/功能

- **支持免费额度的模型**：仅限华北2（北京）地域的实时推理调用，包括 `qwen-max`、`qwen3.7-plus`、`qwen3.6-plus` 等主流千问系列模型及其快照版本（如 `qwen3.7-plus-2026-05-26`），不同模型及快照版本额度相互独立 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **支持阶梯计费的模型**：千问Max、千问Plus 等文本生成模型按单次请求输入 [Token](../concepts/token.md) 数量分档计价（如 0–32K、32K–128K），所有 [Token](../concepts/token.md) 均按所属最高档单价结算 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **支持 Batch 调用的模型**：部分模型（如 `qwen3.7-max`、`qwen-plus`）在启用 Batch 接口时，输入/输出 Token 单价按实时推理价格的 50% 计费，但该优惠与上下文缓存折扣不可叠加 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **不支持免费额度的场景**：Batch 调用、模型调优、模型部署、自定义模型（调优后或已部署模型）均不抵扣免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

> **注意**：文档 5 中 `qwen3.7-max` 在华北2（北京）的输入单价标注为“原价12元 限时5折”，而文档 2 中同模型在“模型部署计费”表格里后付费输入单价为 ¥28.8 / Per 10K TPM/小时。二者计量单位不同（Token vs TPM），无直接矛盾；但需注意：**免费额度仅适用于实时推理（Token 计费），不适用于模型部署（TPM 或模型单元计费）**，此逻辑在文档 1 和文档 2 中一致。

## 关键参数

- **免费额度有效期**：90 天，自开通百炼、模型发布或申请通过之日三者中最晚者起算；2025年9月8日11点前开通用户有效期可能不足90天 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **免费额度用完即停**：开启后额度耗尽返回错误码 `AllocationQuota.FreeTierOnly`，防止意外扣费；该功能默认关闭，可按模型或批量开启/关闭 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **抵扣优先级顺序**：免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费。此顺序在文档 3 的“抵扣逻辑”和文档 4 的“账单详情”说明中完全一致。
- **账单出账延迟**：模型推理账单为分钟级（通常 2–10 分钟），模型训练、批量推理、知识库为小时级；高峰期可能存在延迟 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 使用方式

- **获取免费额度**：访问华北2（北京）地域的[模型广场](https://bailian.console.aliyun.com/#/model-market)，阅读并同意协议后系统自动发放，无需额外操作。
- **查看剩余额度**：两种方式——① 控制台 [免费额度页面](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)；② 模型广场中进入具体模型详情页，在“免费额度”区域查看（如 `362,917/1,000,000`）。
- **成本优化选型**：
  - 首选 **AI 通用型节省计划**：承诺月消费金额，覆盖全部阿里直供模型，最高享 5.3 折，抵扣范围广（含批量推理、工具调用等）；
  - 次选 **资源包**：预购指定模型的 Token 数量，仅用于抵扣该模型超出免费额度后的实时推理费用；
  - 按需选用 **其他模型节省计划**（如千问语音、万相图像/视频）：针对特定模型系列，无折扣或低折扣，有效期固定。
- **账单查询**：登录控制台 → [账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail) → 产品名称选“大模型服务平台百炼”，通过“实例 ID（出账粒度）”字段（`;` 分隔）解析 `ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道` 等关键维度。

## 限制和注意事项

- **地域限制**：免费额度仅华北2（北京）有效；美国、新加坡等地域模型无免费额度，且单价存在差异（如新加坡 `qwen3.7-max` 输入单价为 18.736 元/百万 Token）。
- **额度不共享**：主账号与 RAM 子账号共享同一模型的免费额度；但不同模型（含快照版本）额度完全独立，`qwen-max` 与 `qwen-max-2026-05-17` 视为两个模型，各自拥有 100 万 Token 额度。
- **欠费影响**：账户可用额度 < 0 时，**即使模型仍有免费额度或节省计划剩余额度，所有按量付费类服务（含推理）将立即暂停**；Coding Plan/Token Plan 等预付费套餐不受影响，但自动续费会失败。
- **专属 API Key 限制**：`Token Plan/Coding Plan` 专属 API Key 不消耗免费额度，调用直接按量付费；如需使用免费额度，必须使用通用 API Key [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **模型部署持续计费**：模型部署状态为“运行中”即开始按时长计费，**与是否被 API 调用无关**；若不再使用，务必主动下线模型以停止计费。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


