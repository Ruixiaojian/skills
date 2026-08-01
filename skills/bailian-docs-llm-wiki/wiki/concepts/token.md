# Token 计量与管理

Token 计量与管理是百炼平台统一的资源度量与配额控制机制，以 Token（或等效计量单位）为基本计费与用量单元，贯穿模型调用、训练、部署及应用执行全生命周期。它不仅决定服务调用的成本归属，更直接约束并发能力、速率限制与服务可用性。

## 在百炼平台的不同场景中，这个概念如何使用

- **实时推理（按量调用）**：输入 Token（[prompt](../guides/prompt.md)）与输出 Token（completion）分别计量，按百万 Token 精确计费；部分模型（如 `qwen3-max`）支持阶梯定价，单价随单次请求输入 Token 总量动态变化。
- **Token Plan 订阅服务**：统一以 Credits 为计量单位（1 Credit ≈ 1 Token），但实际消耗由模型类型、Token 用量、思考模式启用状态及 Harness 工具调用共同决定；个人版采用双窗口限额（5 小时 / 7 天），团队版采用月度总额度制。
- **模型训练与微调**：按训练阶段总 Token 数（文本）或复合指标（如视频生成中的“时长 × 像素数 × 轮次”）计量，不区分输入/输出，一次性结算。
- **模型部署**：预置吞吐模式（TPM × 时长）和模型单元模式（算力规格 × 小时）均独立于 Token 计量，但部署后的在线推理仍回归 Token 计量；训练后部署的自定义模型，其推理调用同样计入业务空间 Token 总用量。
- **向量与排序服务**：文本嵌入（`text-embedding-*`）按输入 Token 数计量；多模态嵌入（`qwen3-vl-embedding`）按融合/独立输入的语义单元折算为等效 Token；排序模型（`qwen3-rerank`）按查询 + 文档对总数计量。
- **应用观测与监控**：在智能体/工作流链路中，每个 `LLM` 节点精确上报输入 Token、输出 Token 及总量；`EMBEDDING` 节点上报量化后的输入长度（等效 Token）；所有 Token 数据支持分钟级聚合、告警触发（如“单日突增超 200%”）及导出分析。

## 关键参数和配置

- **计费粒度**：默认以 `1,000,000 Token` 为计费单位（即 1 百万 Token），控制台用量详情页显示精确到个位的 Token 消耗。
- **额度类型**：
  - 免费额度：100 万 Token/模型/90 天（仅华北2，仅限实时推理，不覆盖 Batch/训练/部署）；
  - Token Plan Credits：个人版双窗口限额（如 3,000/5h + 10,000/7d），团队版月度固定额度（如 25,000/坐席/月）；
  - 资源包：预购指定模型的 Token 量，优先抵扣；
  - 节省计划：AI 通用型或模型专属，按小时自动抵扣。
- **抵扣顺序**：严格遵循 `免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费`，不可手动调整。
- **监控指标**：
  - `model_usage`：业务空间级 Token 汇总（小时级延迟）；
  - `model_tps_per_request`：单请求输出 Token 速度（仅高级监控，分钟级）；
  - 应用观测中 `input_tokens` / `output_tokens` 字段：Span 级精确计量。
- **地域强绑定**：所有 Token 计量、额度发放与抵扣均按 API Key 所属地域隔离；跨地域调用不享受任何额度，全额计费。

## 面向开发者，简洁实用

- ✅ **查用量**：控制台 →「费用中心」→「用量明细」或「模型监控」→「用量统计」，支持按业务空间、模型、日期筛选；应用观测中可导出 JSONL 查看每 Span 的 Token 分解。
- ✅ **控成本**：开通「免费额度用完即停」；优先购买 AI 通用型节省计划（覆盖全部模型）；对高频调用模型单独购资源包。
- ✅ **避踩坑**：
  - Token Plan 的 `sk-sp-` Key 仅限指定工具（Cursor/Claude Code/Qwen Code 等）交互式使用，**禁止用于脚本批量调用**，否则可能封禁；
  - 多模态模型（如 `qwen-image-2.0`）必须通过 Slash Command/Skill/Agent 接入，**不可直调 Chat Completions 接口**，否则报错且不计 Token；
  - 启用 `enable_thinking=true` 时，必须同时设置 `stream=true` 和 `incremental_output=true`，否则请求失败且 Token 不扣除；
  - 免费额度不覆盖 `batch`、`training`、`deployment` 场景——这些操作直接走按量付费通道。
- ✅ **调试建议**：遇到“额度不足”错误，先检查账户是否欠费（欠费将暂停所有按量服务）；再确认 API Key 地域与模型开通地域一致；最后核对模型 ID 是否为控制台模型市场中展示的**正式 ID**（如 `qwen3-max`，非别名 `qwen3.7-max`）。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [preparations](../api/preparations.md)
- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [vector and sort](../api/vector-and-sort.md)


