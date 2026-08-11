# test 1

`test 1` 是阿里云百炼平台面向开发者的核心计费与资源管理主题，涵盖模型调用、训练、部署等全链路成本控制机制。其核心围绕**免费额度自动抵扣优先级**、**多层级付费方案（节省计划/资源包/按量）** 及**地域与模型粒度的计费隔离**展开。所有计费行为均以 [Token](../concepts/token.md) 或时长为计量单位，严格遵循“先免费、后预付、再按量”的抵扣顺序，开发者需特别注意地域限制（如免费额度仅限华北2）、模型快照独立性及额度耗尽后的服务状态切换逻辑。

## 支持的模型/功能

- **支持免费额度的模型**：仅限华北2（北京）地域的实时推理模型，包括 `qwen-max`、`qwen3.7-plus` 等主流千问系列，以及部分 ASR/TTS 模型（需在业务空间单独开通权限）[原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **不支持免费额度的场景**：Batch 调用、模型调优、模型部署、自定义模型（调优后或已部署）、PAI-DSW、OSS 存储等 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **模型快照独立性**：带日期后缀的快照（如 `qwen3.7-plus-2026-05-26`）与无后缀最新版（如 `qwen3.7-plus`）视为两个独立模型，各自拥有 100 万 [Token](../concepts/token.md) 免费额度，额度不互通 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **功能覆盖范围**：AI 通用型节省计划可抵扣全部阿里直供模型（含文本、向量、排序、工具调用、批量推理），但明确排除联网搜索[插件](../concepts/plugin.md)、MCP 广场、通义深度搜索等第三方服务费用 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

> **注意**：文档 5 中 `qwen3.7-plus` 在华北2（北京）的免费额度标注为“100万[Token](../concepts/token.md)”，而文档 1 明确说明“每个模型均有独立的免费额度（通常为 100 万 Token）”，二者一致；但文档 5 表格中 `qwen3.7-plus` 的输入单价存在“原价2元 限时8折”等促销标识，而文档 1 未提及时效性折扣，此处以文档 5 的实时价格表为准，文档 1 侧重额度规则而非价格浮动。

## 关键参数

- **免费额度有效期**：90 天，自开通百炼、模型发布或申请通过之日三者中最晚者起算；2025年9月8日11点前开通的用户有效期可能不足90天 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **Token 计费粒度**：模型调用按实际消耗的输入/输出 Token 总数计费，免费额度、资源包、节省计划均以 Token 为单位抵扣，不区分输入或输出 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **节省计划动态月**：非自然月，从购买/生效日起每满30天为一个周期；当月未用完的额度自动清零，不可结转至下月 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。  
- **模型部署计费参数**：PTU（预置吞吐）模式下，费用 = 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM)；模型单元（MU）模式下，费用 = 使用时长（小时）× 模型单元数量 × 小时单价 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

## 使用方式

- **免费额度启用**：首次实名认证并开通百炼后系统自动发放，无需手动领取；调用时自动优先抵扣，无需配置 API Key 类型（但需使用通用 API Key，Token Plan/Coding Plan 专属 Key 不消耗免费额度）[原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **节省计划抵扣顺序**：严格遵循 `免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费` 的层级，若开启“免费额度用完即停”，额度耗尽后服务将停止，节省计划无法触发抵扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。  
- **账单查询路径**：模型推理账单在[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面，筛选“大模型服务平台百炼”；关键字段 `实例 ID（出账粒度）` 以分号 `;` 分隔，格式为 `ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识` [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。  
- **API Key 作用域**：同一 API Key 可调用所有模型，但必须确保其所属业务空间已开通目标模型权限（如 ASR 模型需在业务空间单独授权）[原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 限制和注意事项

- **地域强约束**：免费额度仅华北2（北京）有效；模型部署与训练的计费价格因地域差异显著（如新加坡 qwen3.8-max 输入单价为 14.988 元/百万 Token，高于北京的 12 元）；跨地域调用不改变计费归属，但需确认 Base URL 地域匹配 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **额度耗尽影响**：全新未认证用户额度用尽后返回错误码 `AllocationQuota.FreeTierOnly`，需认证并充值；已认证用户若未开启“免费额度用完即停”，将直接按量扣费，可能导致账户欠费；**账户欠费时，即使其他模型仍有免费额度也无法调用** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **模型部署持续计费**：模型部署状态为“运行中”即开始按时长收费，与是否发生 API 调用无关；若不再使用，必须主动下线模型，否则费用持续产生 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。  
- **出账延迟**：模型推理账单通常 2~10 分钟出账，批量推理、训练、知识库等为小时级出账；控制台显示的剩余额度为分钟级更新且需手动刷新，实际额度可能已耗尽但页面未同步，导致意外扣费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


