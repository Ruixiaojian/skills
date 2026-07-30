# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署的全链路成本控制机制。其核心围绕免费额度发放、按量计费规则、节省计划与资源包抵扣逻辑、以及账单溯源能力展开，旨在帮助开发者在保障业务连续性的同时实现精细化成本治理。所有计费行为均严格遵循地域隔离原则，且免费额度、模型价格、抵扣优先级等关键策略存在明确约束条件。

## 支持的模型/功能

- **支持免费额度的模型**：仅限华北2（北京）地域的模型（如 `qwen3.7-plus-2026-05-26`、`qwen-max` 等），其他地域（如美国弗吉尼亚、新加坡、德国法兰克福、日本东京）虽提供服务，但**不享有新人免费额度** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **支持的计费模型类型**：覆盖文本生成（千问系列、DeepSeek、GLM、Kimi）、多模态（千问VL、万相图像/视频）、语音合成（CosyVoice、Qwen-TTS）、向量与排序（text-embedding-v4、qwen3-rerank）等全品类模型 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。  
- **关键功能支持**：  
  - 实时推理（支持 Batch 调用半价、上下文缓存折扣）；  
  - 模型训练（按 [Token](../concepts/token.md) 总量计费，含千问、万相、CosyVoice 等）；  
  - 模型部署（支持预置吞吐、模型单元两种计费模式）；  
  - 联网搜索插件、MCP 广场、通义深度搜索等**独立计费功能，不纳入 AI 通用型节省计划抵扣范围** [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

> **注意**：文档 5 中 `qwen3.7-max` 在华北2（北京）标注“当前能力等同于 `qwen3.7-max-2026-05-20`”，而文档 2 的部署计费表中列出 `qwen3.7-max-2026-05-20` 为独立模型代码，二者是否为同一模型快照需以控制台实际模型市场为准；若存在能力等同但代码不同，可能引发额度归属歧义，建议以模型 Code 为准进行额度管理。

## 关键参数

- **免费额度参数**：  
  - 额度总量：通常为 **100 万 [Token](../concepts/token.md)/模型**，不同模型（含带日期后缀的快照版本）额度独立、不互通；  
  - 有效期：**90 天**，自开通百炼、模型发布或申请通过之日三者中最晚者起算；2025年9月8日前开通用户有效期可能不足90天 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)；  
  - 抵扣范围：**仅实时推理调用**，明确排除 Batch 调用、模型调优、模型部署、自定义模型等场景。  

- **计费单价参数**：  
  - 输入/输出 [Token](../concepts/token.md) 单价：按地域、模型、输入 Token 区间（如 0–32K、32K–128K）阶梯定价，例如 `qwen3.6-plus` 在华北2（北京）非思考模式下，0–256K 输入单价为 ¥2/百万 Token [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)；  
  - 训练单价：按模型类型差异显著，如 `qwen3.7-plus-2026-05-26` 训练单价为 ¥0.35/千 Token，而 `qwen3-0.6b` 仅为 ¥0.003/千 Token [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)；  
  - 部署单价：分“预置吞吐”（TPM/小时）与“模型单元”（MU/小时）两类，如 `qwen3.7-plus-2026-05-26` 部署使用 MU2 x 8 规格时，小时单价为 ¥504 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

## 使用方式

- **免费额度使用**：无需额外配置，调用时系统自动按 **免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费** 顺序抵扣；使用通用 API Key 即可生效，**Token Plan/Coding Plan 专属 API Key 不消耗免费额度** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **节省计划与资源包开通**：  
  - AI 通用型节省计划：通过 [购买链接](https://common-buy.aliyun.com/?commodityCode=sfm_GenAI_spn_cn) 选择承诺周期与金额，支持跨模型抵扣；  
  - 资源包：按模型粒度购买，仅抵扣该模型超出免费额度后的实时推理用量 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)；  
- **账单查询与溯源**：  
  - 推理账单字段 `实例 ID（出账粒度）` 格式为 `ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`，可用于精准定位费用来源 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)；  
  - 训练账单字段以 `!` 分隔，格式为 `业务空间ID!地域!训练任务标识`，与推理账单结构不同，需区分解析。

## 限制和注意事项

- **地域限制**：免费额度、部分模型训练（如 CosyVoice）、模型部署计费项均严格限定在华北2（北京）地域，跨地域调用不享受对应权益 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **额度与服务状态联动**：  
  - 开启“免费额度用完即停”后，额度耗尽将返回错误码 `AllocationQuota.FreeTierOnly`，服务立即停止；关闭该功能后方可继续使用节省计划或按量付费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)；  
  - **账户欠费时，即使模型仍有免费额度或节省计划剩余额度，所有调用均被拒绝**，必须结清欠费才能恢复服务 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。  
- **抵扣逻辑硬约束**：  
  - 免费额度不支持补发、延期或重置，过期自动作废；  
  - 同一实名主体下 RAM 子账号与主账号共享免费额度，但不同模型额度完全隔离；  
  - AI 通用型节省计划**不抵扣模型调优、模型部署、联网搜索插件等费用**，需单独预算 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。  
- **出账延迟**：模型推理账单为分钟级出账（通常 2–10 分钟），批量推理、训练、[知识库](../concepts/knowledge-base.md)等为小时级出账，高峰期可能存在延迟，不可依赖实时账单做即时决策 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


