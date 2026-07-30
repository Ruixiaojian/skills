# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与成本管理主题，涵盖模型调用、训练、部署的定价规则，以及免费额度、节省计划、资源包等成本优化机制。本文档聚焦于实时推理（模型调用）场景的通用计费逻辑，不涉及模型训练与部署的专用计费模型（详见[模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)），并明确区分了免费额度、按量付费及各类优惠方案的适用边界与抵扣顺序。

## 支持的模型/功能

- **支持模型**：覆盖千问（Qwen）全系列（Max、Plus、Flash、Coder、VL、Embedding、Rerank 等）、DeepSeek、GLM、Kimi、万相（WanX）、CosyVoice 等主流文本、[多模态](../concepts/multi-modal.md)、语音、图像、视频模型。
- **核心功能**：
  - 实时推理（同步/流式调用）
  - Batch 调用（文件输入，价格为实时推理的 50%）
  - 上下文缓存（显式/隐式，计费单价独立于标准输入，详见[上下文缓存文档](https://help.aliyun.com/zh/model-studio/context-cache)）
  - Function Calling、网页抓取等原生工具调用（费用可被 AI 通用型节省计划抵扣）

> **注意**：文档 5 中“千问Max”表格将 `qwen3.7-max` 标注为“当前能力等同于 `qwen3.7-max-2026-05-20`”，但文档 2 的部署计费表中仅列出 `qwen3.7-max-2026-05-20`，未提及其别名映射关系；实际调用应以控制台或 API 返回的 `model` 字段为准，避免依赖别名。该不一致需以[模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)中明确列出的 Model ID 为准。

## 关键参数

- **计费维度**：以 [Token](../concepts/token.md) 为基本单位，分 `input_token` 和 `output_token` 单独计费。
- **阶梯计费**：部分模型（如 `qwen3-max`、`qwen3.7-plus`）按单次请求的输入 [Token](../concepts/token.md) 总量分档定价，所有 [Token](../concepts/token.md) 均按所处最高档单价结算（例如输入 100K Token 落入 32K–128K 档，则全部 100K 按该档单价计费）。
- **地域差异**：同一模型在不同地域（华北2、美国、新加坡、德国、日本）价格不同，且**仅华北2（北京）地域模型享有新人免费额度**，其他地域无此权益 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **免费额度参数**：每个模型（含不同快照版本，如 `qwen-max` 与 `qwen-max-2026-05-17`）独立享有 100 万 Token 免费额度，有效期 90 天（自开通/模型发布/申请通过日起较晚者计算）。

## 使用方式

- **调用流程**：使用通用 API Key（非 Token Plan/Coding Plan 专属 Key）发起 HTTP 请求，系统自动按以下优先级抵扣费用：**免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费** [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **启用免费额度**：无需额外配置，首次开通百炼后，在华北2（北京）地域调用支持的模型即自动生效。专属 API Key 不消耗免费额度，须改用通用 Key [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **成本优化选型**：
  - 高频、跨模型调用：首选 [AI 通用型节省计划](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)，承诺月消费额换取最高 5.3 折。
  - 单一模型稳定用量：可选对应模型的“其他模型节省计划”或“资源包”。
  - 短期、不确定用量：直接按量付费，配合“免费额度用完即停”功能防意外扣费。

## 限制和注意事项

- **免费额度限制**：
  - 仅抵扣**实时推理**费用，**不支持** Batch 调用、模型调优、模型部署、自定义模型（调优后/已部署） [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
  - 主账号与 RAM 子账号共享额度，但不同模型额度完全独立，不会自动切换。
  - 免费额度耗尽后，全新未认证用户将返回错误码 `AllocationQuota.FreeTierOnly` 并停止服务；已认证用户若未开启“免费额度用完即停”，将直接按量扣费。

- **账户状态影响**：
  - **账户欠费时，即使模型仍有免费额度也无法调用**，必须结清欠费才能恢复服务 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
  - 模型部署（按时长计费）与 API 调用（按 Token 计费）是两个独立计费项：部署状态为“运行中”即开始计费，与是否发生 API 调用无关。

- **账单与监控**：
  - 推理账单分钟级出账（2–10 分钟），训练/批量/知识库账单小时级出账。
  - 账单中“实例 ID（出账粒度）”字段以分号 `;` 分隔，格式为 `ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`，是定位费用归属的关键依据 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


