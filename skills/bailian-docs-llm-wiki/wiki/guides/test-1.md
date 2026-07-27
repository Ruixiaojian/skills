# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署及成本控制的全链路规则。本文档整合官方最新策略，明确免费额度适用范围、多层级抵扣逻辑（免费额度 > 资源包 > 节省计划 > 按量付费），并指出关键限制——例如免费额度仅限华北2（北京）地域实时推理，且不覆盖Batch调用、模型调优与部署等场景。所有计费行为均以[Token](../concepts/token.md)或TPM为计量单位，账单按分钟级（推理）或小时级（训练/批量）生成。

## 支持的模型/功能

- **支持免费额度的模型**：仅限华北2（北京）地域的实时推理调用，包括 `qwen-max`、`qwen3.7-plus`、`qwen3.6-plus` 等主流千问系列及部分第三方模型（如 DeepSeek、GLM），但**不包含** `qwen3.6-max-preview` 等预览版模型（其免费额度规则需单独确认）[原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **支持节省计划抵扣的模型**：AI 通用型节省计划覆盖 A 类（千问、向量、排序等）、B 类（图像/语音）、C 类（qwen3.6-max-preview、Kimi 等），但三方直供模型（如 MiniMax）暂不支持抵扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。  
- **支持按量计费的模型类型**：文本生成（千问、GLM、DeepSeek）、多模态（千问VL）、语音（Qwen-TTS、Paraformer）、图像/视频（万相）等，均按输入/输出 [Token](../concepts/token.md) 或其他单位（如图片张数、语音秒数）计费 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。  
- **不支持免费额度的场景**：Batch 调用、模型调优、模型部署、自定义模型（调优后或已部署模型）均不可使用免费额度抵扣 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

> **注意**：文档 5 中 `qwen3.6-max-preview` 在“华北2（北京）”价格表中标注“[上下文缓存]享有折扣”，但文档 1 明确指出“带日期后缀的快照版本（如 `qwen-max-2026-05-17`）与不带日期的最新版本视为两个独立模型，各自拥有独立额度”。而文档 5 未说明该预览版是否享有免费额度，存在信息缺口；实际使用中应以控制台显示为准，或参考 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md) 的独立额度原则。

## 关键参数

- **免费额度参数**：默认 100 万 [Token](../concepts/token.md)/模型，有效期 90 天（自开通/模型发布/申请通过日起算，以较晚者为准）；2025年9月8日前开通用户有效期可能不足90天 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **阶梯计费参数**：部分模型（如 `qwen3-max`）按单次请求输入 Token 总量分档计价（如 0–32K、32K–128K），所有 Token 均按所属最高档单价结算。  
- **部署计费参数**：  
  - *预置吞吐*：费用 = 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM)；  
  - *模型单元*：费用 = 使用时长（小时）× 模型单元数量 × 小时单价（如 `qwen3.7-plus` MU2 x 8 规格为 ¥504/小时）[原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。  
- **训练计费参数**：按训练 Token 总量计费，公式为 `训练Token总量 × 训练单价`；其中文本模型为 `(训练数据 Token 总数 + 混合训练数据 Token 总数) × 循环次数`，图像/视频模型则依赖 `max_steps`、`max_pixels`、`n_epochs` 等超参 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

## 使用方式

- **调用流程**：使用通用 API Key（非 Token Plan/Coding Plan 专属 Key）发起实时推理请求，系统自动按 `免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费` 顺序抵扣 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **开启/关闭“免费额度用完即停”**：在控制台 [免费额度页面](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota) 或 [模型广场详情页](https://bailian.console.aliyun.com/?tab=model#/model-market/detail/group-qwen3-coder-plus?modelGroup=group-qwen3-coder-plus) 操作开关；开启后额度耗尽返回错误码 `AllocationQuota.FreeTierOnly` [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **购买节省计划**：AI 通用型节省计划通过 [购买链接](https://common-buy.aliyun.com/?commodityCode=sfm_GenAI_spn_cn) 下单，支持全预付/零预付（后者需商务开通），承诺周期按“动态月”重置（非自然月）[原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。  
- **查询账单**：登录 [账单详情页](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)，选择产品为“大模型服务平台百炼”，通过 `实例 ID（出账粒度）` 字段（格式：`ApiKeyID;业务空间ID;模型名称;...`）精准定位费用归属 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **地域限制**：免费额度仅华北2（北京）有效；其他地域（如美国、新加坡）模型无免费额度，且价格不同（如新加坡 `qwen3.7-max` 输入单价为 ¥18.736/百万 Token）[原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。  
- **账户状态影响**：账户欠费时，即使模型仍有免费额度或节省计划余额，**所有按量付费服务均暂停**；Coding Plan/Token Plan 套餐因独立于账户余额，欠费期间仍可使用 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。  
- **额度互斥性**：不同模型（含不同快照版本）额度完全独立，不互通；主账号与 RAM 子账号共享同一模型额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **部署持续计费**：模型部署状态为“运行中”即开始计费，**与是否发生 API 调用无关**；需主动下线部署或删除 API Key 才能停止费用产生 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。  
- **出账延迟**：模型推理账单通常 2–10 分钟生成，批量推理、训练、知识库等为小时级出账；高峰期可能进一步延迟，查询账单需预留缓冲时间 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


