# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与成本管理主题，涵盖模型调用、训练、部署等全链路的费用规则、优惠机制及实操指引。本文档整合官方最新策略，重点说明免费额度适用范围、多级抵扣逻辑（免费额度 > 资源包 > 节省计划 > 按量付费）、模型调用价格结构及关键限制条件，帮助开发者精准预估成本、规避意外扣费。

## 支持的模型/功能

- **支持免费额度的模型**：仅限华北2（北京）地域的实时推理调用，包括 `qwen-max`、`qwen3.7-plus-2026-05-26` 等主流千问系列，以及部分开源和第三方模型（如 DeepSeek、GLM 的阿里直供版本）。带日期后缀的快照版本（如 `qwen3.7-plus-2026-05-26`）与无后缀最新版（如 `qwen3.7-plus`）视为独立模型，各自享有 100 万 [Token](../concepts/token.md) 免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **不支持免费额度的场景**：Batch 调用、模型调优、模型部署、自定义模型（调优后或已部署模型）均不可使用免费额度抵扣 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **支持节省计划抵扣的模型**：AI 通用型节省计划覆盖 A 类（千问、向量、排序等）、B 类（图像/语音/视频）、C 类（qwen3.6-max-preview、DeepSeek 等阿里直供版），但 MiniMax、HappyHorse 等暂无阿里直供版本，不支持抵扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 关键参数

- **免费额度有效期**：90 天，自开通百炼、模型发布或申请通过之日三者中较晚者起算；**2025年9月8日11点前开通的用户，有效期可能不足90天** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **抵扣优先级顺序**：`免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费`。该顺序在多个文档中一致确认，是成本控制的核心逻辑 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **阶梯计费阈值**：部分模型（如 `qwen3-max`）按单次请求输入 [Token](../concepts/token.md) 数分档计价（例如 0–32K、32K–128K、128K–256K），所有 [Token](../concepts/token.md) 均按所处最高档单价结算，非累进计算 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。

## 使用方式

- **启用免费额度**：无需额外配置，使用通用 API Key（非 Token Plan/Coding Plan 专属 Key）调用华北2（北京）地域的实时推理接口，系统自动优先抵扣 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **开启“免费额度用完即停”**：在控制台[免费额度页面](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)或[模型广场详情页](https://bailian.console.aliyun.com/?tab=model#/model-market/detail/group-qwen3-coder-plus?modelGroup=group-qwen3-coder-plus)手动开启开关，可防止额度耗尽后自动转为按量付费产生意外费用。
- **购买节省计划**：推荐优先选用 [AI 通用型节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_GenAI_spn_cn)，支持跨模型、跨地域（华北2、新加坡、美国等）抵扣，购买后立即生效，无需绑定 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 限制和注意事项

> **注意**：文档 5 中 `qwen3.7-plus` 在华北2（北京）的“思考模式”输出单价标注为“原价8元 限时8折”，而文档 2 明确指出“AI 通用型节省计划对 A 类模型（含千问）提供阶梯折扣”，二者未冲突；但文档 5 中同一模型在“美国（弗吉尼亚）”地域的 `qwen3.7-plus-us` 输出单价为“原价11.991元 限时8折”，而文档 2 表明该地域属于 AI 通用型节省计划适用地域，此处存在潜在歧义——实际抵扣应以节省计划总览页查询结果为准，而非文档 5 的限时价直接套用。

- **地域限制严格**：免费额度仅华北2（北京）有效；模型部署计费中，PTU 和模型单元方案在不同地域（如北京 vs 新加坡）单价差异显著（例如 `qwen3.7-plus-2026-05-26` 北京后付费输入单价 ¥4.8/10K TPM/小时，新加坡为 ¥7.19），调用前务必确认地域配置 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **账户欠费影响全局服务**：即使某模型仍有剩余额度，只要账户整体欠费（可用额度 < 0），所有按量付费类服务（含免费额度、资源包、节省计划抵扣）将全部暂停，必须结清欠费方可恢复 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **账单延迟与溯源**：模型推理账单通常在调用结束 2–10 分钟后生成，而训练、批量推理等为小时级出账；账单中“实例 ID（出账粒度）”字段以分号 `;` 分隔，格式为 `ApiKeyID;业务空间ID;模型名称;...`，是定位费用归属的关键依据 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


