# Token 计量与管理

Token 计量与管理是百炼平台对大模型调用资源进行精细化核算、配额控制与成本治理的核心横切能力。它以 Token（含输入、输出、缓存等维度）为统一计量单位，贯穿模型调用、监控、计费、订阅及评测全链路，为开发者提供可追溯、可配置、可优化的资源使用视图。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用与计费**：所有按量推理请求均按实际消耗的输入 Token、输出 Token 及缓存 Token 进行计量；阶梯计价（如 0–32K、32K–128K）以单次请求中最高 Token 区间为准；免费额度（100万 Token）、资源包、节省计划等均基于 Token 消耗自动抵扣，且严格遵循「免费额度 > 资源包 > 其他节省计划 > 按量付费」的优先级顺序。

- **Token Plan 订阅服务**：采用 Credits 作为上层计费单位，但底层仍以 Token 为核算基础——Credits 消耗量 = f(模型类型, 输入 Token, 输出 Token, 缓存 Token, Harness 工具调用次数)；个人版受「5 小时限额 + 7 天限额」双窗口约束，团队版按月度 Token 额度分配（如标准席位 25,000 Credits/月），额度到期不结转。

- **TPM 预留与快速模式**：TPM（Token Per Minute）预留直接以 kTPM（千 Token/分钟）为容量单位，支持输入/输出维度独立配置，并自动应用缓存折扣（如 glm-5.2 缓存部分按 25% 折算）；快速模式虽不显式暴露 TPM，但其 TPS 提升本质依赖底层 Token 级调度优化，且计费仍按实际 Token 数结算。

- **可观测性（监控与追踪）**：模型监控（Model Monitoring）在「调用详情」页精确展示每次请求的 `input_tokens`、`output_tokens`、`cached_tokens`；应用监控（Application Monitoring）在 `LLM` 节点中聚合统计 Token 消耗，并与延时、状态码联动分析；二者均支持按 API Key、业务空间、模型等维度下钻用量归属。

- **模型评测**：当评测任务选择「评测数据集」作为数据源时，被测模型的每次推理将产生真实 Token 消耗并计入账单；裁判模型（如 `qwen-max`）执行大模型评估时，其自身调用也按 Token 单独计费；复用「推理结果集」可完全规避二次 Token 消耗。

- **部署与训练**：Token 计量**不适用于**模型训练、模型部署、Batch 调用、自定义模型（调优后或已部署）等场景——这些环节按模型单元（MU）、GPU 小时、实例时长等其他单位计费，与 Token 无关。

## 关键参数和配置

| 参数 | 说明 | 开发者须知 |
|------|------|------------|
| `input_tokens` / `output_tokens` | 请求中实际发送的 Prompt Token 数与模型返回的 Completion Token 数 | 在模型监控日志、应用监控 LLM 节点中可精确查看；`max_tokens` 参数直接影响输出 Token 上限，建议合理设置避免浪费。 |
| `cached_tokens` | 缓存命中部分对应的 Token 数（如重复 Prompt 或 KV Cache 复用） | 仅部分模型（如 glm-5.2）支持缓存折扣，计费时按折扣率折算（如 0.25×cached_tokens）；非所有调用均触发缓存，需结合模型文档确认支持性。 |
| `model` 字段（含 TPM 预留专属 code） | 决定 Token 计量规则与计费策略的唯一标识 | 使用 TPM 预留时，必须替换为生成的专属 model code（如 `qwen37max-tpm-xxxx`），否则按标准计费；Token Plan 必须使用 `sk-sp-` 开头 Key + 对应 Base URL，混用通用 Key 将导致额度无法抵扣。 |
| `workspace_id` | 业务空间 ID，是 Token 用量归属、监控过滤、告警配置的基础维度 | 所有 Token 相关指标（监控、账单、评测）均默认按 workspace_id 维度聚合；跨空间调用需显式指定，否则可能归属错误。 |
| `apikey_id` | API Key 的唯一标识（非密钥字符串），用于用量溯源 | 在账单明细与监控日志中均为关键字段；主账号与 RAM 子账号共享同一模型额度，但 `apikey_id` 可区分具体调用来源，便于成本分摊。 |

## 面向开发者，简洁实用

- ✅ **必查项**：调用后立即在「模型监控 → 日志」中核对 `input_tokens`/`output_tokens`，确认是否符合预期（如长 Prompt 是否被截断、`max_tokens` 是否生效）；  
- ✅ **必配项**：开通 Token Plan 或启用 TPM 预留前，务必切换至正确地域（Token Plan 仅限华北2；TPM 预留需目标模型在对应地域可用）；  
- ✅ **必控项**：对成本敏感场景，开启「免费额度用完即停」开关（控制台 → 免费额度页面），避免额度耗尽后自动转为按量付费；  
- ⚠️ **避坑提示**：不同模型（含快照版本如 `qwen3.7-plus` 与 `qwen3.7-plus-2026-05-26`）的免费额度完全独立，不可合并；Token Plan 与 Coding Plan 的 Key、Base URL、额度三者严格隔离，禁止混用；  
- 📈 **优化建议**：优先复用推理结果集做评测、启用缓存支持模型、压缩 Prompt 冗余内容、设置合理 `max_tokens`，可显著降低 Token 消耗与成本。

## 关联主题页

- [test 1](../guides/test-1.md)
- [token plan guide](../guides/token-plan-guide.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)


