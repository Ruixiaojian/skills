# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署及成本优化的全链路规则。本文档整合了免费额度、按量计费、节省计划、资源包及账单管理等关键机制，帮助开发者准确预估成本、规避意外扣费，并高效利用平台资源。所有计费行为均以实际调用结束后的出账为准，且严格遵循“免费额度 > 资源包 > 节省计划 > 按量付费”的抵扣优先级。

## 支持的模型/功能

- **实时推理（模型调用）**：支持千问（Qwen）、DeepSeek、GLM、Kimi、万相（WanX）、CosyVoice 等全系列模型，覆盖文本生成、[多模态](../concepts/multi-modal.md)、语音合成与识别、视频生成等场景。  
- **模型训练**：支持千问VL、万相图像/视频、CosyVoice 语音模型的微调，按训练[Token](../concepts/token.md)总量计费（详见[模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)）。  
- **模型部署**：提供两种计费模式——**预置吞吐**（按TPM时长）和**模型单元**（按算力规格小时），适用于高并发、低延迟或弹性伸缩场景。  
- **上下文缓存**：部分模型（如 `qwen3.7-max`、`qwen3.6-plus`）支持显式/隐式缓存，缓存命中[Token](../concepts/token.md)按折扣单价计费（输入[Token](../concepts/token.md)命中价为标准价10%，创建价为125%），但该折扣未包含在本文档所列基础价格中。  
- **Batch调用**：对支持OpenAI兼容接口的模型（如 `qwen3.7-max`、`qwen-plus`），Batch调用的输入/输出Token单价为实时推理价格的50%。  

> **注意**：文档 5 中 `qwen3.7-max` 在华北2（北京）地域标为“原价12元 限时5折”，而文档 2 中同模型部署计费表显示其后付费输入单价为 ¥28.8 / Per 10K TPM/小时——二者属不同计费维度（Token vs TPM），无矛盾；但需注意，文档 5 的“限时折扣”未说明有效期，而文档 1 明确指出“新人免费额度有效期为90天”，开发者应以控制台实时价格为准，避免依赖过期优惠信息。

## 关键参数

- **免费额度**：默认为 100 万 Token/模型，仅限华北2（北京）地域的实时推理调用，不支持 Batch、训练、部署或自定义模型（见[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)）。  
- **Token 计费粒度**：输入/输出 Token 均按百万为单位计费，阶梯计费以单次请求总输入 Token 数为依据（如输入 100K Token 落入 32K–128K 区间，则全部按该档单价结算）。  
- **TPM（Tokens Per Minute）**：部署计费核心指标，输入/输出 TPM 分开计算，溢出策略可选「自动溢出」（切至按量付费）或「仅使用 PTU 容量」（返回 429）。  
- **模型单元（MU）规格**：如 `MU2 x 8`、`MU9 x 1`，决定算力密度与时长单价，最小计费单位为分钟（后付费）或天（预付费）。  
- **节省计划承诺周期**：以“动态月”为单位（非自然月），每月额度独立发放、不可累积，到期自动清零（参见[节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)）。

## 使用方式

1. **开通与初始化**：访问[华北2（北京）地域控制台](https://bailian.console.aliyun.com/#/model-market)，同意协议后系统自动发放免费额度（见[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)）。  
2. **API 调用**：使用通用 API Key（非 Token Plan/Coding Plan 专属 Key），请求中指定 `model` 参数（如 `qwen3.7-plus-2026-05-26`），系统自动按优先级抵扣免费额度、资源包或节省计划。  
3. **成本优化配置**：  
   - 开启「免费额度用完即停」防止超额扣费（控制台免费额度页或模型详情页操作）；  
   - 购买 AI 通用型节省计划（推荐），承诺月消费额获取阶梯折扣，覆盖全部阿里直供模型；  
   - 针对特定模型高频调用，可选购其他模型节省计划或资源包（如万相图像生成、千问语音模型）。  
4. **账单监控**：通过[费用概览](https://bailian.console.aliyun.com/?tab=model#/costing-balance)查看当月总消费，结合[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)按 `ApiKeyID;业务空间ID;模型名称` 字段溯源（详见[账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)）。

## 限制和注意事项

- **地域限制**：免费额度、CosyVoice 训练、多数模型部署仅支持华北2（北京）；美国、新加坡等地域模型价格上浮（如 `qwen3.7-max-us` 输入单价 ¥18.736/百万Token），且无免费额度。  
- **额度隔离**：不同模型（含快照版本，如 `qwen3.7-plus` 与 `qwen3.7-plus-2026-05-26`）额度完全独立，不互通；主账号与 RAM 子账号共享同一模型额度。  
- **欠费影响**：账户可用额度 < 0 时，**所有服务（含仍有免费额度的模型）将立即暂停**，结清欠费后方可恢复（见[账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)）。  
- **出账延迟**：模型推理账单分钟级生成（通常 2–10 分钟），训练/批量任务小时级出账，高峰期可能延迟，查询账单前需等待对应周期。  
- **部署持续计费**：模型部署状态为「运行中」即开始计费，与是否被调用无关；停止计费需主动下线部署实例（而非仅停用 API Key）。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


