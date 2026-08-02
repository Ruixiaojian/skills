# Token 计量与计费

Token 计量与计费是百炼平台统一的资源消耗度量与成本核算机制，以 **Token（含输入 Token 和输出 Token）为基本计量单位**，结合模型类型、调用方式、加速策略及服务等级，动态计算并抵扣 Credits 或按量费用。所有 AI 能力——无论是文本生成、多模态推理、Harness 工具调用，还是向量检索、重排序等应用节点——最终均归一化为 Token 消耗进行计费。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型推理调用（Chat Completions / Completions）**：  
  输入 Prompt + 上下文 + 图片 Base64 编码等计入 `input_tokens`；模型生成的文本、代码、JSON 等计入 `output_tokens`。二者分别计费，单价按模型和地域浮动（如 `qwen3.7-plus` 在华北2为 2.4 元/百万输入 Token）。长上下文、多图输入、工具调用返回内容均显著增加 Token 数。

- **Token Plan 订阅服务**：  
  所有调用（含模型推理、Harness 工具执行、多模态 Skill 调用）统一折算为 **Credits** 抵扣。Credits 消耗 = `f(model_type, input_tokens, output_tokens, thinking_mode, tool_calls)`，例如 `qwen3.8-max-preview` 启用联网搜索时，每次工具调用额外产生固定 Credits 成本。

- **应用监控（Application Monitoring）**：  
  在智能体/工作流链路中，每个 `LLM` 节点精确上报 `input_tokens` 和 `output_tokens`；`EMBEDDING` 节点仅上报输入 Token 量；`RETRIEVER`、`RERANKER` 等节点不产生 Token 计费，但其调用频次影响整体链路成本结构。Token 数据支持按 Trace ID 追溯到具体 Prompt 和响应片段。

- **模型监控（Model Monitoring）**：  
  提供小时级/分钟级 Token 消耗聚合视图，支持按 `API Key`、`model`、`workspace_id` 多维下钻。可定位高 Token 消耗请求（如 `max_tokens=8192` 且实际输出超长），辅助优化提示词与参数配置。

- **高性能推理（TPM 预留 / 快速模式）**：  
  TPM 预留按 **kTPM（千 Token/分钟）** 预购容量，其计费与 Token 实际消耗解耦，但超出预留部分仍按标准 Token 单价计费；快速模式（如 `glm-5.2-fast-preview`）采用独立单价（如缓存命中 4 元/百万 Token），Token 计量逻辑不变，仅费率不同。

## 关键参数和配置

- **`input_tokens` / `output_tokens`**：必填监控字段，由平台自动统计，开发者无需手动计算。建议在 API 请求中显式设置 `max_tokens` 以控制输出长度，避免意外高额消耗。
- **`model` 参数值**：决定基础单价与计费规则。同一模型不同版本（如 `qwen3.7-plus` vs `qwen3.7-plus-2026-05-26`）视为独立计费实体；TPM 预留模型 code（如 `tpm-qwen37max-abc123`）和快速模式模型（如 `glm-5.2-fast-preview`）均有专属费率。
- **`cache_control`（上下文缓存）**：启用后，缓存命中部分输入 Token 按折扣计费（如 10%~25%），显式创建缓存则按溢价（如 125%）计费。
- **`tool_choice` / `tools`（Harness 工具）**：工具调用本身不按 Token 计费，但工具返回结果作为后续 LLM 输入，会新增 `input_tokens`；部分工具（如联网搜索）在 Token Plan 中产生固定 Credits 成本。
- **免费额度与抵扣顺序**：免费额度（如 100 万 Token）仅适用于华北2（北京）通用 API Key 的实时推理调用，且严格按 `免费额度 > 资源包 > 节省计划 > 按量付费` 顺序抵扣；Token Plan 和 Coding Plan 的 Key 不参与此流程。

## 面向开发者，简洁实用

- ✅ **务必检查 `model` 和 `region`**：不同地域模型价格差异巨大（如弗吉尼亚 `qwen3.7-max-us` 输入单价达 18.7 元/百万 Token），且免费额度仅限华北2。
- ✅ **用好 `max_tokens` 和 `stop`**：防止模型无限制生成，这是最直接的 Token 成本控制手段。
- ✅ **监控优先看「Token 总量」趋势图**：在 [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 和 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe) 中，按小时/天筛选，快速识别异常增长。
- ✅ **调试阶段开启推理日志**：可查看真实 `prompt_tokens` 和 `completion_tokens`，验证是否因系统消息、工具描述等隐式内容导致 Token 溢出。
- ❌ **不要混用 Key**：Token Plan Key（`sk-sp-`）、通用 Key（`sk-`）、Coding Plan Key 完全隔离，混用将导致计费失败或额度不生效。
- ❌ **避免批量脚本调用 Token Plan**：个人版明确禁止自动化批量调用，违规将封禁 Key；生产环境请选用团队版或按量付费+TPM 预留组合方案。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [test 1](../guides/test-1.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


