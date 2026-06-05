# Token 计费与限流配额

Token 是百炼平台模型调用的最小计费与限流单位：账单按输入/输出 Token 量结算，调用频率与吞吐量则按账号-模型维度受 RPM（每分钟请求数）与 TPM（每分钟 Token 数）双限。开发者需同时关注**成本侧**（单价、阶梯、抵扣顺序）与**容量侧**（限流阈值、配额开关），才能让生产应用稳定运行且费用可控。

## 在百炼平台的使用场景

Token 计费与限流配额贯穿百炼的整个模型调用链路，不同子产品中的体现略有差异：

- **模型推理（按量计费）**：大语言模型按 Token 出账，输入/输出/缓存分别计价；图像、视频、语音模型分别按张、秒、字符或 Token 计量。Batch 调用享受 5 折单价，但与上下文缓存折扣互斥。
- **新人免费额度**：首次开通中国内地版百炼时各模型自动发放，有效期 30~90 天（2026-09-08 起统一为 90 天），仅抵扣**实时推理**，主账号与 RAM 子账号共享。可在控制台开启「免费额度用完即停」开关，耗尽后服务自动停止（返回 `AllocationQuota.FreeTierOnly` 403 错误）。
- **节省计划与资源包**：AI 通用型节省计划按月承诺金额换取最高 5.3 折，按月独立结算、未用完到月底清零；抵扣顺序固定为「免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费」。**节省计划不抵扣模型部署费用**。
- **Token Plan 团队版**：按 Credits 抵扣输入/缓存/输出 Token，无每 5 小时/每周限额，多租户隔离不排队，承诺数据不用于模型训练。配额由管理后台按席位分发（标准 25,000 / 高级 100,000 / 尊享 250,000 Credits/月）。
- **Coding Plan**：按模型**调用次数**而非 Token 计量，受每 5 小时、每周、每月调用次数限制；高峰期可能排队。
- **模型调优**：按训练 Token 计费，公式为「(训练数据 Token + 混合训练数据 Token) × 循环次数 × 训练单价」，最小粒度 1 Token，节省计划与免费额度均不抵扣。
- **模型监控与告警**：监控面板与 Prometheus 指标提供 Token 消耗、RPM、TPM、限流错误次数等数据，可针对成本与限流配置主动告警。
- **应用观测**：CHAIN / LLM 等节点会自动追踪每次调用的输入 Token、输出 Token、总 Token 与延时，支持按 Token 数值条件筛选 Span。

## 限流配额机制

- **聚合维度**：限流按**主账号**聚合（账号下所有 RAM 子账号、业务空间、API Key 共享额度），按**模型**独立计算。
- **双限制**：每个模型同时受 RPM 与 TPM 限制，**超出任一阈值即触发**。
- **典型报错与处理**：
  - `Requests rate limit exceeded` / `exceeded your current requests list` → RPM 超限，降低调用频率。
  - `Allocated quota exceeded` / `exceeded your current quota` → TPM 超限，缩短输入或限制输出长度。
  - `Request rate increased too quickly` → 短时请求爆发触发稳定性保护，采用匀速调度、指数退避、请求队列。

## 关键参数与配置

| 参数 / 配置项 | 位置 | 作用 |
| --- | --- | --- |
| `max_tokens` | 请求体 | 限制单次输出 Token 上限，直接影响 TPM 与单次成本 |
| `DASHSCOPE_API_KEY` | 环境变量 | 按账号识别配额归属，建议环境变量注入而非硬编码 |
| 「免费额度用完即停」 | 控制台 → 模型用量 → 免费额度 | 防止免费额度耗尽后产生意外按量费用 |
| 用量告警规则 | 模型监控 → 告警 | 对成本、失败率、限流次数设置主动告警（仅北京、新加坡地域支持） |
| Token Plan 席位 | 管理后台 | 决定每月可用 Credits 配额，可加购共享用量包（月度有效期到期清零） |
| `model_usage` / `model_call_count` | Prometheus HTTP API | 通过 Grafana 等工具按 `apikey_id` / `model` / `workspace_id` 维度查询 Token 用量 |

## 成本与容量优化建议

1. **控制输出长度**：合理设置 `max_tokens`，对推理模型限制思考长度，避免 Token 超额。
2. **按任务选模型**：简单任务优先用 `qwen-turbo` / `qwen-flash` 等轻量级模型，复杂推理才用 Max 系列。
3. **善用阶梯计费**：部分模型按单次请求输入 Token 总量划档，落入高档则全部 Token 按高单价结算，应控制单次请求规模避免跨档。
4. **优先使用 Batch 与上下文缓存**：Batch 享 50% 单价、上下文缓存对输入 Token 折扣，但二者**不能同时生效**。
5. **配置告警与「用完即停」**：及时发现成本异常与限流抖动，避免免费额度耗尽后产生计费。
6. **观察用量延迟**：控制台用量统计延迟约 1 小时、仅展示最近 30 天；更早数据需通过费用与成本页面查询。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [token plan guide](../guides/token-plan-guide.md)
- [model monitoring](../guides/model-monitoring.md)
- [test 1](../guides/test-1.md)
- [application monitoring](../guides/application-monitoring.md)


