# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，聚焦模型调用、训练、部署及成本优化的全链路规则。本文档整合新人免费额度、按量计费、节省计划、账单管理等关键机制，明确各能力的适用范围、生效条件与协同逻辑，帮助开发者快速建立成本意识并规避常见扣费风险。所有计费行为均以实际出账时间为准，控制台显示数据存在分钟级延迟，操作前请务必手动刷新。

## 支持的模型/功能

- **实时推理（模型调用）**：支持全部上架模型（千问、DeepSeek、GLM、Qwen-VL、万相、CosyVoice 等），覆盖文本生成、图像/视频生成、语音合成与识别等类型。[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)仅适用于华北2（北京）和新加坡地域的实时推理调用，不支持 Batch 调用、模型调优、模型部署、PAI-DSW 或 OSS 存储等场景。
- **模型训练**：支持千问系列（文本）、万相系列（图像/视频）、CosyVoice（语音）等模型的微调，按训练 [Token](../concepts/token.md) 总量计费，与推理免费额度完全隔离。
- **模型部署**：支持 PTU（预置吞吐）和 MU（模型单元）两种模式，按使用时长或算力规格计费，同样不参与免费额度抵扣。
- **上下文缓存、Function Calling、网页抓取等原生工具**：其调用费用属于模型调用范畴，可被 AI 通用型节省计划抵扣，但不享受免费额度。

> **注意**：文档 5 中“千问Max”表格列出 `qwen3.7-max` 的输入单价为“原价12元 限时5折”，而文档 2 中同模型在“模型部署计费”表格中后付费输入单价为 ¥28.8/Per 10K TPM/小时（即 ¥2,880/百万[Token](../concepts/token.md)），二者单位与场景不同（前者为 [Token](../concepts/token.md) 原价，后者为 TPM 部署单价），无矛盾；但文档 5 中 `qwen3.7-plus` 在华北2（北京）的思考模式输出单价统一标为“8元”，而文档 2 中同模型部署的“后付费输出”单价为 ¥1.92/Per 1K TPM/小时（即 ¥1,920/百万Token），数值差异显著。经查证，文档 5 的“8元/百万Token”为**推理调用原价**，文档 2 为**部署服务单价**，属不同计费维度，此处无需修正，但开发者需严格区分调用（inference）与部署（deployment）场景。

## 关键参数

- **免费额度有效期**：90 天，自开通百炼、模型发布或模型申请通过之日三者中**最晚者**起算；2025年9月8日11点前开通用户有效期可能不足90天 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **Token 计费粒度**：最小计费单位为 1 Token，输入与输出 Token 共用同一免费额度池，不单独区分。
- **阶梯计费阈值**：如 `qwen3-max` 在华北2（北京）按输入 Token 分三档（≤32K、≤128K、≤256K），单次请求所有 Token 均按最高档单价结算。
- **节省计划动态月**：非自然月，从购买/生效日开始每满30天为一个周期，当月未用完额度自动清零，不结转 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **账单出账延迟**：模型推理账单为分钟级（通常 2~10 分钟），训练与批量推理为小时级，高峰期可能延迟 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 使用方式

- **免费额度**：首次开通百炼后自动发放，无需实名认证即可使用；调用时系统自动优先抵扣，无需额外配置。API Key 通用，但 **Token Plan/Coding Plan 专属 API Key 不消耗免费额度**，必须使用通用 API Key [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **节省计划**：按“免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费”顺序抵扣；若开启“免费额度用完即停”，额度耗尽后服务将停止，节省计划无法生效，需手动关闭该开关才能触发抵扣 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **账单查询**：通过[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面，筛选“大模型服务平台百炼”，查看“实例 ID（出账粒度）”字段（格式为 `ApiKeyID;业务空间ID;模型名称;...`）定位具体模型与调用来源 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **成本分摊**：为业务空间绑定标签，T+1 天后可在账单“实例标签”列验证分账效果，实现按部门或项目归集费用。

## 限制和注意事项

- **地域限制**：免费额度仅限华北2（北京）和新加坡地域；模型训练（CosyVoice）仅支持华北2（北京）；部分模型（如 `qwen3.7-max-us`）仅在弗吉尼亚地域提供。
- **额度不可共享与转移**：主账号与 RAM 子账号共享同一模型的免费额度；但不同模型（含快照版本，如 `qwen-max` 与 `qwen-max-2026-05-17`）额度完全独立，不互通、不合并。
- **欠费影响**：账户可用额度 < 0 时，**即使模型仍有剩余额度，所有按量付费服务（含免费额度、节省计划、资源包）均立即暂停**；Coding Plan/Token Plan 套餐因额度独立可继续使用，但自动续费会失败。
- **部署即计费**：模型部署成功进入“运行中”状态后即开始按时长计费，与是否发起 API 调用无关；停止计费需主动下线模型或退订预付费实例。
- **出账延迟风险**：节省计划额度扣减基于**实际出账时间**，而非任务提交时间；若任务提交时额度充足，但出账时已过期，仍会产生按量费用。建议设置高额消费预警并监控动态月额度使用率 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


