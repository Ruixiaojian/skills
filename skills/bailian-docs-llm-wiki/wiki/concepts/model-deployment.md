# 模型部署与推理优化

模型部署与推理优化是百炼平台将训练/微调完成的模型转化为稳定、高效、可监控的在线服务的核心能力集合，涵盖资源保障、性能加速、成本可控与弹性伸缩四大维度。它不是单一操作，而是面向生产环境的端到端技术栈，贯穿从部署选型、参数配置、流量调度到性能观测的全链路。

## 在百炼平台的不同场景中，这个概念如何使用

- **高确定性生产服务（如客服对话、金融风控）**：选用 **TPM 预留部署（`plan=ptu`, `service_tier=ptu_default`）**，锁定专属输入/输出吞吐（kTPM），规避公共资源池争抢，确保 P99 延迟稳定、429 错误率趋近于零。适用于千问3.8-Max、GLM-5.2、DeepSeek-v4-Pro 等 9 款主力模型。
  
- **低首 Token 延迟敏感场景（如编程助手、实时 Agent）**：组合使用 **TPM 预留 + 快速模式（Fast mode）** ——前者保障容量不被限流，后者通过解码调度优化将 TPS 提升至标准 API 的 1.5~2 倍（当前仅支持 `glm-5.2-fast-preview` 模型，需切换专属域名调用）。

- **轻量验证与快速迭代（如 A/B 测试、POC）**：采用 **Token 用量计费模式（`plan=lora`）**，按实际消耗付费，无需预估流量；仅限 LoRA 微调后的自定义模型，适合效果验证阶段。

- **独占资源与精细调优需求（如私有大模型、SLA 严苛的内部系统）**：选用 **模型单元（MU）部署**，通过 `deploy_spec`（如 `MU1`）、`rpm_limit`、`tpm_limit` 和 `max_context_length` 精确控制副本数、并发上限与上下文长度，支持 PD 分离计算降低首 Token 延迟。

- **长文本处理（如法律文档分析、代码库理解）**：优先选择支持 **1M token 输入** 的 PTU 部署（如 `qwen3.8-Max`、`glm-5.2`），并启用前缀缓存（自动生效，命中时响应头含 `cached_tokens`，额度按折扣系数折算）和阶梯容量系数（如 GLM-5.1 在 32K–200K 区间系数为 1.33），显著提升长输入性价比。

## 关键参数和配置

| 场景 | 必填/关键参数 | 说明 | 开发者提示 |
|------|----------------|------|-----------|
| **TPM 预留部署** | `plan="ptu"`<br>`service_tier="ptu_default"`<br>`ptu_capacity: {input_tpm, output_tpm, thinking_output_tpm}` | `input_tpm`/`output_tpm` 单位为 kTPM（千 Token/分钟），须为模型步长整数倍；`thinking_output_tpm` 仅深度思考模型支持 | ✅ 强烈建议显式指定 `service_tier="ptu_default"`（非 `"ptu_fast"`），否则不享受容量保障；扩缩容时三者必须同向调整（全增或全减） |
| **快速模式（Fast mode）** | 模型 ID=`glm-5.2-fast-preview`<br>专属域名=`https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1` | 无配额参数，按 token 计费；流式响应中需单独解析 `delta.reasoning_content` 字段 | ⚠️ 不可与 TPM 预留模型 code 混用；必须使用专属域名，标准域名调用无效 |
| **模型单元（MU）** | `plan="mu"`<br>`deploy_spec`（如 `"MU1"`）<br>`capacity`（副本数）<br>`max_context_length` | `deploy_spec` 决定单副本算力规格；`max_context_length` 超出模型原生上限将直接报错 | 🔒 MU 模式下 `service_tier` 不返回或为 `"default"`，不可用于 SLA 保障型场景 |
| **通用调用控制** | `overflow_strategy="enable"` 或 `"disable"` | `"enable"`：超 TPM 容量时自动转按量计费（响应头含 `x-dashscope-ptu-overflow:true`）；`"disable"`：直接返回 HTTP 429 | 🛑 生产环境推荐 `"disable"` + 监控告警联动，避免意外费用；变更需调用 `/updateOverflowStrategy` 接口 |

## 面向开发者，简洁实用

- **起步最快**：控制台 → 模型部署 → 选择模型 → 切换“预置吞吐（PTU）” → 使用内置「预置吞吐额度计算器」估算 kTPM 需求（输入 QPS × 平均输入/输出 token 数 × 60）→ 创建即用。
- **API 调用统一入口**：所有部署模式均通过 `POST /api/v1/deployments` 创建，仅 `plan` 和参数结构不同；部署成功后，调用方式与标准 DashScope API 完全一致（`model` 字段填生成的专属 model code，如 `qwen3-max-dedicated-abc123`）。
- **调试必查字段**：响应头中关注 `x-dashscope-ptu-overflow`（是否溢出）、`x-dashscope-cached-tokens`（缓存命中量）、`x-dashscope-first-token-latency-ms`（首 Token 延迟）——这些是推理优化效果的直接证据。
- **监控闭环**：部署后立即前往「模型监控」→「性能指标」页签，重点关注 `model_first_token_duration`（P95/P99）、`model_tps_per_request` 和 `model_call_duration_p99`；设置告警阈值（如首 Token > 300ms 或失败率 > 0.5%），实现问题主动发现。
- **避坑提醒**：
  - 部署创建后**计费模式不可更改**，切勿选错 `plan`；
  - TPM 预留模型 code **仅在创建区域有效**，跨区调用需重新部署；
  - `thinking_output_tpm` 配置后，深度思考阶段才受该额度约束，常规输出仍走 `output_tpm`；
  - 快速模式为 Preview 特性，接口行为可能调整，请订阅 [百炼更新日志](https://help.aliyun.com/zh/model-studio/release-notes)。

## 关联主题页

- [model production](../api/model-production.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model monitoring](../guides/model-monitoring.md)


