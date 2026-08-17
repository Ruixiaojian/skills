# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署的全链路成本结构。本文档聚焦实时推理（即模型调用）的计费逻辑、免费额度规则、成本优化工具（如节省计划与资源包）及账单溯源方法，不涉及模型能力、SDK 使用或业务集成细节。所有价格与策略均以华北2（北京）地域为默认基准，其他地域需单独确认适用性。

## 支持的模型/功能

- **支持免费额度的模型**：仅限华北2（北京）地域上架的模型，且必须明确标注“免费额度”区域（如 `qwen-max`、`qwen3.7-plus-2026-05-26` 等）。带日期后缀的快照版本（如 `qwen3.7-plus-2026-05-26`）与无后缀最新版（如 `qwen3.7-plus`）视为独立模型，各自拥有 100 万 [Token](../concepts/token.md) 免费额度，不互通 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **不支持免费额度的场景**：Batch 调用、模型调优、模型部署、自定义模型（调优后或已部署）、PAI-DSW、OSS 存储及请求费用 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **支持阶梯计费的模型**：千问 Max/Plus 系列等主流文本生成模型，单价按单次请求输入 [Token](../concepts/token.md) 总量所属区间统一结算（如输入 100K [Token](../concepts/token.md) 落在 32K–128K 区间，则全部按该档单价计费）[原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **不支持免费额度的模型类型**：ASR 类模型需在控制台业务空间逐一开通权限后方可消耗额度；部分模型（如 `qwen3.6-max-preview`）虽在列表中但未显示免费额度区域，即不参与发放 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 关键参数

- **免费额度有效期**：90 天，自开通百炼、模型发布或模型申请通过之日三者中**最晚者**起算；2025年9月8日11点前开通的用户有效期可能不足90天 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **Token 计费粒度**：输入/输出 Token 共用总额度，不区分计算；调用时产生的 Token 总量（输入+输出）共同扣减该额度。
- **抵扣优先级顺序**：免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **账单出账延迟**：模型推理账单为分钟级（通常 2–10 分钟），批量推理、训练、知识库为小时级；控制台显示的剩余额度为分钟级更新，需手动刷新 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

> **注意**：文档 5 中 `qwen3.7-plus` 在华北2（北京）的输入单价标为“原价2元 限时8折”，而文档 2 中同模型训练单价为 ¥0.3/千Token（即 ¥300/百万Token），二者属不同计费场景（推理 vs 训练），无矛盾；但文档 5 的“限时折扣”未注明截止时间，实际调用前应以控制台实时价格为准，避免依赖过期活动价。

## 使用方式

- **自动启用免费额度**：首次开通百炼后系统自动发放，无需实名认证即可使用；调用时系统自动优先抵扣，无需额外配置 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **API Key 选择**：通用 API Key 可消耗免费额度；Token Plan/Coding Plan 专属 API Key **不消耗免费额度**，需改用通用 Key [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **成本优化工具选型**：
  - 长期稳定使用 → 优先选 **AI 通用型节省计划**（覆盖全模型，最高 5.3 折）；
  - 用量小或集中单模型 → 选 **资源包** 或 **其他模型节省计划**；
  - 团队协作 → 选 **Token Plan**。
  详见[选型指南](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **账单查询路径**：
  - 实时费用概览：控制台「费用概览」页面；
  - 明细溯源：[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail) → 产品名称选「大模型服务平台百炼」→ 查看「实例 ID（出账粒度）」字段（格式：`ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`）[原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **地域限制**：免费额度仅华北2（北京）和新加坡地域模型享有，其他地域无 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **额度耗尽影响**：
  - 未认证用户：直接返回错误码 `AllocationQuota.FreeTierOnly`，需认证并充值后才能继续使用；
  - 已认证用户：若开启「免费额度用完即停」，服务停止；若未开启，则自动转为按量付费，可能产生欠费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费全局阻断**：账户可用额度 < 0 时，**即使免费额度、节省计划、资源包仍有剩余，所有模型调用均会暂停**，必须结清欠费后恢复 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **模型部署独立计费**：部署状态为「运行中」即开始按时长收费，与是否被 API 调用无关；需主动下线模型才能停止计费 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **免费额度用完即停开关**：未认证用户强制开启且不可关闭；已认证用户可自行开关，但关闭后存在约半小时生效延迟，期间调用可能因额度耗尽而计费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


