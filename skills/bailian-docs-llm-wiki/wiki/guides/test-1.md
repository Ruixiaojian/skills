# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署的费用结构、免费额度机制、成本优化工具（如节省计划与资源包）及账单溯源方法。本文档聚焦于华北2（北京）地域中国内地服务部署范围下的主流文本生成模型（如 Qwen3 系列），其计费逻辑以 [Token](../concepts/token.md) 为基本单位，支持按量付费、预付费及多种抵扣策略组合。所有计费行为均受地域、服务部署范围、模型版本及调用方式（实时/批量/Batch）严格约束。

## 支持的模型/功能

- **主流文本生成模型**：包括 `qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.5-plus`、`qwen-plus` 等系列，均支持非思考与思考（思维链+回答）双模式；部分模型（如 `qwen3.7-max`）在华北2（北京）地域中国内地部署下享有新人免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **多模态与垂类模型**：千问VL（视觉语言）、万相（图像/视频生成）、千问语音（ASR/TTS）、向量/排序模型等，各自独立计费且适用不同节省计划 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **关键功能支持**：
  - Batch 调用：输入/输出 [Token](../concepts/token.md) 单价按实时推理价格的 50% 计费（若模型支持）；
  - 上下文缓存：显式缓存创建与命中 [Token](../concepts/token.md) 采用独立单价，不包含在本文档所列基础输入单价中 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)；
  - 模型部署：支持“预置吞吐”与“模型单元”两种计费模式，后者含 PD 分离部署以降低首 Token 延迟 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

> **注意**：文档 5 中 `qwen3.7-max` 在华北2（北京）的输入单价标注为“原价12元 限时5折”，而文档 2 中同模型部署计费表未体现折扣，仅列原价 ¥28.8/10K TPM（输入）。二者计费维度不同（Token vs TPM），但需注意：**实时推理按 Token 计费，模型部署按 TPM 或模型单元时长计费，不可混用价格表**。开发者应根据实际调用方式（API 直接调用 vs 已部署服务）选择对应文档参考。

## 关键参数

- **Token 计费粒度**：输入/输出 Token 均按百万（1M）为单位计价，阶梯计费依据单次请求总输入 Token 数（如 `0<Token≤32K`、`32K<Token≤128K`），该请求全部 Token 按所属最高阶梯单价结算。
- **免费额度参数**：默认 100 万 Token/模型，有效期 90 天（自开通/模型发布/申请通过日起算，以较晚者为准）；仅限华北2（北京）地域中国内地部署模型；不覆盖 Batch 调用、模型训练、模型部署等场景 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **部署规格参数**：
  - 预置吞吐：按 `输入 TPM` 和 `输出 TPM` 分别计费，单位为 `Per 10K TPM/小时`（后付费）或 `Per 10K TPM/天`（预付费）；
  - 模型单元（MU）：按 `模型单元数量 × 使用时长（小时）` 计费，不同规格（如 MU1×2、MU3×8）对应固定小时单价。
- **节省计划承诺参数**：AI 通用型节省计划需承诺月消费金额（≥1000 元）与周期（3/6/12/24 个月），折扣力度随金额与周期递增，最高达 5.3 折 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 使用方式

- **调用模型**：使用通用 API Key 发起 HTTP 请求，系统自动按 `免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费` 顺序抵扣费用；专属 API Key（如 Token Plan/Coding Plan）不消耗免费额度，需改用通用 Key [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **启用免费额度保护**：在控制台[免费额度页面](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)开启“免费额度用完即停”，避免超额扣费；该功能对已耗尽或过期额度的模型不可用。
- **购买成本优化工具**：
  - **AI 通用型节省计划**：覆盖全部阿里直供模型，推荐作为首选，购买后自动生效，无需绑定 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)；
  - **资源包**：针对特定模型（如 `qwen-plus`）预购 Token，购买后立即生效，按“先到期先抵扣”原则使用；
  - **其他模型节省计划**：适用于用量集中于单一模型系列（如千问语音、万相）的场景，无折扣或低折扣。
- **查询与监控**：
  - 免费额度余量：通过控制台[免费额度页面](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)或[模型广场详情页](https://bailian.console.aliyun.com/?tab=model#/model-market/detail/group-qwen3-coder-plus?modelGroup=group-qwen3-coder-plus)查看；
  - 实时账单：调用结束 2–10 分钟后生成，可在[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面按 `ApiKeyID`、`业务空间ID`、`模型名称` 等字段筛选分析 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **地域与部署范围强约束**：免费额度、部分模型价格及节省计划适用地域均严格限定。例如，仅华北2（北京）地域中国内地部署的模型享有免费额度；美国（弗吉尼亚）地域的 `qwen3.7-max-us` 模型单价显著高于北京同名模型 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **额度与服务隔离**：
  - 不同模型（含带日期后缀的快照版本，如 `qwen3.7-plus-2026-05-26`）额度完全独立，不互通；
  - 免费额度仅抵扣实时推理，明确排除 Batch 调用、模型训练、模型部署、自定义模型调用 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)；
  - 账户欠费时，即使模型仍有免费额度或节省计划余额，所有按量付费服务（含推理）将暂停。
- **出账与监控延迟**：
  - 模型推理账单分钟级出账（2–10 分钟），但模型调用记录需 1 小时后才在[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面可见；
  - 控制台免费额度显示为分钟级更新，需手动刷新页面获取最新余量，否则可能因缓存导致误判而产生费用 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **部署即计费**：模型部署状态为“运行中”时即开始按使用时长计费，与是否发生 API 调用无关；长期不用应主动下线部署以停止计费 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


