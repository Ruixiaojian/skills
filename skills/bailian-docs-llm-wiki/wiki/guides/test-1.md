# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署的费用结构、免费额度规则、成本优化工具（如节省计划与资源包）以及账单溯源方法。本文档聚焦于实际开发中高频涉及的计费逻辑、参数约束与操作边界，不包含营销性描述，所有信息均基于平台当前生效的运营策略与技术规范。

## 支持的模型/功能

`test 1` 覆盖百炼平台上全部主流模型类型及其关键能力：
- **文本生成模型**：以千问系列（Qwen3.x、Qwen2.5、Qwen-Max/Plus/Flash）为主，支持非思考模式、思考模式（思维链+回答）及 Batch 调用；部分模型（如 `qwen3.6-max-preview`）明确区分输入 [Token](../concepts/token.md) 阶梯计费区间 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **多模态模型**：千问VL系列（如 `qwen3-vl-8b-instruct`）、万相图像/视频生成模型，其训练计费依赖 `max_steps`、`max_pixels`、`n_epochs` 等超参 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **语音模型**：CosyVoice、Qwen-TTS/ASR 系列，仅华北2（北京）地域支持调优，且 ASR 类模型需在业务空间内单独开通权限方可消耗免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **向量与排序模型**：`text-embedding-v4`、`qwen2.5-vl-embedding` 等，其调用费用可被 AI 通用型节省计划抵扣，但知识库规格费用（如 0.03 元/知识库/小时）不在抵扣范围内。

> **注意**：文档 5 中 `qwen3.7-max` 在华北2（北京）标注为“当前能力等同于 `qwen3.7-max-2026-05-20`”，而文档 2 的部署价格表中 `qwen3.7-max-2026-05-20` 与 `qwen3.7-Max-2026-05-20`（大小写不一致）并存，且后者在部署价格表中未列出输入/输出单价。实际调用应以控制台模型广场展示的 `model_id` 为准，避免因命名差异导致计费误判。

## 关键参数

- **[Token](../concepts/token.md) 计费粒度**：所有按量计费模型以实际消耗的输入/输出 [Token](../concepts/token.md) 总数为单位，1 Token ≈ 1 个中文字符或 0.75 个英文单词；免费额度、节省计划、资源包均按此统一计量。
- **地域约束**：新人免费额度**仅限华北2（北京）地域**模型可用，其他地域（如新加坡、美国弗吉尼亚）无免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)；模型部署与训练的计费单价亦按地域分表（如华北2与新加坡价格差异显著）。
- **阶梯计费阈值**：部分模型（如 `qwen3-max`）按单次请求输入 Token 数划分阶梯（0–32K、32K–128K、128K–256K），**整个请求的所有 Token 均按最高区间单价结算**，非分段计价。
- **部署单元规格**：PTU（预置吞吐）按 TPM（每分钟 Token 数）购买，模型单元（MU）按算力规格（如 MU1 x 8）计费，二者计费公式与退订规则不同，需严格区分使用场景。

## 使用方式

1. **免费额度自动生效**：完成实名认证后，系统自动发放各模型独立的 100 万 Token 免费额度（仅华北2），无需手动领取；调用时系统按“免费额度 > 资源包 > 节省计划 > 按量付费”顺序自动抵扣 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
2. **节省计划配置**：AI 通用型节省计划需在[购买页面](https://common-buy.aliyun.com/?commodityCode=sfm_GenAI_spn_cn)选择承诺周期（3/6/12/24个月）与月消费额，生效后自动覆盖全模型调用费用，但**不支持抵扣模型训练、部署、联网搜索[插件](../concepts/plugin.md)费用**。
3. **账单溯源**：通过[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面，依据 `实例 ID（出账粒度）` 字段（格式：`ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`）精准定位费用来源，支持按 API Key 或业务空间筛选 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
4. **停止计费操作**：删除 API Key 可终止推理调用；下线已部署模型可停止按时长计费；退订预付费实例需在[退订管理](https://usercenter2.aliyun.com/refund/refund)页面操作，已使用部分按 1.5 倍系数结算。

## 限制和注意事项

- **免费额度不可共享与转移**：主账号与 RAM 子账号共享同一模型额度，但不同模型（含快照版本如 `qwen-max-2026-05-17` 与 `qwen-max`）额度完全独立，额度耗尽后**不会自动切换至其他有余额的模型**，必须手动修改代码中的 `model` 参数。
- **免费额度用完即停的风险**：开启该功能后，额度耗尽将返回错误码 `AllocationQuota.FreeTierOnly`，服务中断；生产环境**不建议开启**，以免意外停服；关闭后配置生效存在约半小时延迟 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **账户欠费影响全局服务**：即使某模型仍有剩余额度，只要账户可用额度 < 0（欠费），所有按量付费模型调用均会暂停，包括免费额度、节省计划、资源包的抵扣均失效。
- **出账延迟与预警滞后**：模型推理账单通常 2–10 分钟出账，但控制台免费额度显示为分钟级更新且需手动刷新；节省计划额度扣减基于**实际出账时间**，非任务提交时间，存在延迟风险，建议设置高额消费预警 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **专属 API Key 限制**：`Token Plan/Coding Plan` 专属 API Key **不消耗免费额度**，调用直接按量付费；如需使用免费额度，必须改用通用 API Key。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


