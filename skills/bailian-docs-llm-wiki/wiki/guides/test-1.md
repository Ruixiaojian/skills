# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署的计费规则，以及免费额度、节省计划、资源包等成本优化机制。本文档聚焦于华北2（北京）地域的通用文本生成模型（以千问系列为主），明确各计费项的适用范围、抵扣优先级及关键使用约束，帮助开发者合理规划资源、规避意外费用。

## 支持的模型/功能

- **支持模型**：主要覆盖千问（Qwen）系列文本生成模型，包括 `qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.5-plus`、`qwen-plus` 及其带日期后缀的快照版本（如 `qwen3.7-plus-2026-05-26`）。不同地域（如美国、新加坡、德国、日本）模型价格与免费额度策略存在差异，详见 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **核心功能支持**：
  - 实时推理（含思考模式与非思考模式）
  - Batch 调用（输入/输出 [Token](../concepts/token.md) 单价为实时推理的 50%）
  - 上下文缓存（显式/隐式缓存，按独立单价计费，不包含在本文所列基础单价中）
- **不支持免费额度的场景**：Batch 调用、模型调优、模型部署、自定义模型（调优后或已部署模型）均不可使用新人免费额度，具体参见 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。

> **注意**：文档 5 中 `qwen3.6-max-preview` 在华北2（北京）标注为“非思考和思考模式”，但在文档 2 的部署计费表中未列出该模型；同时，文档 2 明确指出 `qwen3.6-max-preview` 属于 C 类模型，不支持 AI 通用型节省计划抵扣，而文档 3 的 A 类模型列表中又将其排除。此矛盾需以控制台实时模型市场为准，建议开发者调用前通过 [模型广场](https://bailian.console.aliyun.com/?tab=model#/model-market/all) 确认模型当前状态与计费属性。

## 关键参数

- **[Token](../concepts/token.md) 计费粒度**：输入/输出 [Token](../concepts/token.md) 均按实际消耗量计费，单位为“每百万 Token”（即 ¥/M Token）。阶梯计费按单次请求总输入 Token 数划分区间，全部 Token 按对应区间单价结算。
- **免费额度参数**：新人默认获得 **100 万 Token** 免费额度，仅限华北2（北京）地域的实时推理调用，有效期为 **90 天**（自开通百炼、模型发布或申请通过日起算，以较晚者为准）[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **抵扣优先级**：系统严格按顺序抵扣：**免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费**。若开启“免费额度用完即停”，服务将直接中断，节省计划无法生效 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **地域与部署范围标识**：模型 ID 后缀（如 `-us`、`-2026-05-26`）及“服务部署范围”字段（全球/国际/美国/欧盟等）直接影响价格与免费额度可用性，调用时必须匹配目标地域 endpoint。

## 使用方式

- **API 调用**：使用通用 API Key（非 Token Plan/Coding Plan 专属 Key）发起 HTTP 请求，系统自动优先使用免费额度，无需额外配置。示例模型 ID：`qwen3.7-plus-2026-05-26`。
- **控制台操作**：
  - 查看剩余额度：访问 [免费额度页面](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota) 或模型详情页的“免费额度”区域。
  - 开启/关闭“免费额度用完即停”：在免费额度页面操作列或模型广场详情页开关控制，防止超额扣费 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **成本优化配置**：
  - 优先购买 [AI 通用型节省计划](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)，承诺月消费额可享最高 5.3 折，覆盖全部阿里直供模型。
  - 针对特定模型高频调用场景，可选购“其他模型节省计划”或“资源包”，但折扣力度通常低于通用型。
- **账单溯源**：通过 [账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail) 页面的“实例 ID（出账粒度）”字段（格式：`ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`）精准定位费用来源 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **地域限制**：免费额度**仅限华北2（北京）地域**，其他地域（含新加坡）模型无免费额度；部分模型（如 `qwen3.7-max-us`）仅在美国地域提供，价格与北京版不同。
- **额度隔离**：不同模型（含同一模型的不同快照版本，如 `qwen3.7-plus` 与 `qwen3.7-plus-2026-05-26`）的免费额度相互独立，不互通、不共享，额度耗尽后不会自动切换至其他有额度的模型。
- **欠费影响**：账户欠费时，**即使免费额度或节省计划仍有剩余，所有按量付费服务（含模型调用）将立即暂停**，必须结清欠费后方可恢复。
- **部署即计费**：模型部署（如按模型单元或预置吞吐方式）一旦状态为“运行中”，即开始按时长计费，与是否发生 API 调用无关，需主动下线以停止计费 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **专属 Key 限制**：Token Plan/Coding Plan 专属 API Key **不消耗免费额度**，调用将直接按量付费，如需使用免费额度，请确保使用通用 API Key。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


