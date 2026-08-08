# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署及成本优化的全链路规则。本文档整合官方最新政策，明确免费额度适用范围、按量计费基准、节省计划抵扣逻辑及关键使用约束，帮助开发者快速建立成本意识并规避意外扣费风险。所有规则均以华北2（北京）地域为默认基准，跨地域调用需额外关注价格与额度差异。

## 支持的模型/功能

- **实时推理**：支持千问（Qwen）、DeepSeek、GLM、千问VL、万相（WanX）、CosyVoice 等全系列模型的 API 调用，覆盖文本生成、多模态、语音合成与识别、图像/视频生成等场景。
- **模型训练**：支持文本生成（千问）、图像生成（万相）、视频生成（万相）、语音合成（CosyVoice）四类模型的微调服务，按训练 [Token](../concepts/token.md) 总量计费 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **[模型部署](../concepts/model-deployment.md)**：提供两种计费模式——预置吞吐（PTU，按 TPM 时长计费）和模型单元（MU，按算力规格与使用时长计费），支持华北2（北京）与新加坡双地域部署 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **成本优化工具**：支持 AI 通用型节省计划（跨模型、阶梯折扣）、其他模型节省计划（单模型专用）、资源包（指定模型 [Token](../concepts/token.md) 量）三类优惠方案，其中 AI 通用型节省计划可抵扣模型调用、工具调用、批量推理及上下文缓存费用 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

> **注意**：文档 5 中 `qwen3.7-max` 在华北2（北京）标注为“当前能力等同于 `qwen3.7-max-2026-05-20`”，但文档 2 的部署价格表中未列出该快照版本；实际调用时应以控制台模型广场显示的可用模型 ID 为准，避免因版本别名导致计费不一致。

## 关键参数

| 参数类别 | 说明 | 示例/范围 |
|----------|------|-----------|
| **免费额度** | 仅华北2（北京）地域模型享有，有效期90天（以开通/发布/申请通过三者最晚时间起算），额度为输入+输出 [Token](../concepts/token.md) 共用总额度，通常为 100 万 Token | `qwen-max`：100 万 Token；带日期后缀的快照（如 `qwen-max-2026-05-17`）视为独立模型，不共享额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md) |
| **Token 计价** | 按输入/输出 Token 分开计费，部分模型支持阶梯定价（如输入 ≤32K、32K–128K、>128K 对应不同单价），Batch 调用享 50% 折扣，上下文缓存有独立单价 | 华北2 `qwen3.6-plus`：输入 ≤256K 时 ¥2/百万 Token，输出 ¥12/百万 Token（非思考模式） |
| **部署规格** | PTU 模式按输入/输出 TPM 单价 × 使用时长计算；模型单元（MU）按规格（如 MU1×8）× 小时单价 × 时长计算 | `qwen3.6-plus` PTU 输入单价：¥4.8/10K TPM/小时；`qwen3.5-35b-a3b` MU1×2 小时单价：¥108 |
| **节省计划承诺周期** | AI 通用型节省计划以“动态月”为单位分配额度（非自然月），当月未用完额度自动清零，不累积至下月 | 订购 3 个月、月承诺 ¥10,000 的节省计划，每月独立获得 ¥10,000 额度 |

## 使用方式

1. **开通与初始化**：完成阿里云实名认证后，访问[华北2（北京）百炼控制台](https://bailian.console.aliyun.com/#/model-market)，同意协议即自动发放免费额度，无需手动领取 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
2. **API 调用**：使用通用 API Key（非 Token Plan/Coding Plan 专属 Key）发起请求，系统自动按优先级抵扣：免费额度 → 资源包 → 其他模型节省计划 → AI 通用型节省计划 → 按量付费。
3. **成本配置**：
   - 开启「免费额度用完即停」防止超额扣费（控制台 > 免费额度页面或模型详情页开关）；
   - 购买 AI 通用型节省计划（推荐）或资源包，按需绑定业务空间标签实现分账；
   - 设置[高额消费预警](https://billing-cost.console.aliyun.com/home/alarm-threshold)（阈值可设至 ¥0.01）。
4. **账单溯源**：调用结束后 2–10 分钟生成推理账单，通过[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页的 `实例 ID（出账粒度）` 字段（格式：`ApiKeyID;业务空间ID;模型名称;...`）精准定位费用归属。

## 限制和注意事项

- **地域限制**：免费额度、ASR 模型权限开通、CosyVoice 训练服务均**仅限华北2（北京）地域**；其他地域（如新加坡、美国）无免费额度，且部分模型价格上浮（如新加坡 `qwen3.8-max` 输入单价 ¥14.988/百万 Token，高于北京的 ¥12）。
- **额度不可转移**：主账号与 RAM 子账号共享同一模型的免费额度，但不同模型（含快照版本）额度完全独立，系统不会自动切换有余额的模型 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费影响全局**：账户欠费时，即使某模型仍有免费额度或节省计划余额，所有按量付费调用均会暂停，必须结清欠费才能恢复服务。
- **部署即计费**：[模型部署](../concepts/model-deployment.md)状态为“运行中”即开始按时长计费，与是否被 API 调用无关；停止计费需主动下线部署或删除 API Key。
- **不支持抵扣场景**：免费额度、节省计划、资源包均**不抵扣**模型训练、[模型部署](../concepts/model-deployment.md)、Batch 调用、联网搜索插件、知识库规格费用（仅向量/Rerank 调用可被 AI 通用型节省计划抵扣） [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


