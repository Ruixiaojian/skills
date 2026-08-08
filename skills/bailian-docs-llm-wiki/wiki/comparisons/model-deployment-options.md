# [模型部署](../concepts/model-deployment.md)方式对比：Model Production、Model Deployment 1 与 Model High Speed Inference

## 对比目的与背景

在百炼平台中，模型从训练完成到线上服务落地存在多种技术路径。`Model Production`、`Model Deployment 1` 和 `Model High Speed Inference` 分别面向不同阶段、不同目标的工程需求：前者聚焦**端到端模型生命周期管理（含微调+部署）**，后者强调**生产级服务稳定性与资源可控性**，而第三者专为**极致吞吐或超低延迟场景提供加速能力**。本对比旨在帮助开发者清晰理解三者的定位差异、能力边界与适用约束，避免因选型不当导致开发返工、成本超支或 SLA 不达标等问题。

---

## 关键维度对比表

| 维度 | Model Production | Model Deployment 1 | Model High Speed Inference |
|------|------------------|----------------------|----------------------------|
| **核心定位** | 微调训练 + 在线部署一体化流程，支持自定义模型构建与版本化交付 | 生产就绪的专属推理服务，支持多计费模式与精细化资源调度 | 面向高吞吐/低延迟的**推理加速能力**（非独立部署方案，需依附于其他部署形态） |
| **输入格式** | 微调阶段：JSONL（`messages` 或 `prompt`/`completion` 字段）；部署后推理：OpenAI 兼容格式（`/v1/chat/completions`） | 全模式统一支持 OpenAI/Anthropic 兼容格式；PTU/MU 模式支持长上下文（最高 1M token）；[Token](../concepts/token.md) 计费仅限 LoRA 模型 | 同所依附的底层部署（如 `glm-5.2-fast-preview` 使用标准 OpenAI 格式，但流式响应新增 `delta.reasoning_content` 字段） |
| **输出格式** | OpenAI 兼容格式（含 `usage`、`choices[0].message.content` 等）；支持流式（`stream: true`） | 完全兼容 OpenAI/Anthropic 格式；MU 模式额外支持 `thinking` 模式输出结构；PTU 模式返回 `cached_tokens` 等额度明细字段 | 标准 OpenAI 格式基础上扩展流式字段（如 `delta.reasoning_content`）；TPM 预留不改变格式，仅提升容量保障 |
| **支持模型类型** | • 百炼托管基础模型（Qwen 系列等）的监督微调<br>• ONNX/Triton 格式第三方模型（通过 `import_model` 导入） | • 平台预置模型（Qwen3/Qwen2.5/GLM-4.7+/DeepSeek/Kimi/CosyVoice 等）<br>• **仅 LoRA 微调模型**（需满足 rank、vocab、chat_template 等约束）<br>• 不支持全参微调模型 | • TPM 预留：支持主流预置模型（Qwen、GLM、DeepSeek、Kimi）<br>• 快速模式：**仅 preview 阶段支持 `glm-5.2-fast-preview`**（不可泛化至其他模型） |
| **API 端点** | `POST /v1/fine_tuning_jobs` → `POST /v1/deployments` → `POST {endpoint_url}/v1/chat/completions` | `POST /api/v1/deployments`（指定 `plan: "ptu"`/`"mu"`/`"lora"`）→ 调用通用域名 `dashscope.aliyuncs.com`（PTU/MU）或专属域名（快速模式） | • TPM 预留：使用专属 `model` code（如 `qwen38max-tpm-abc123`），调用通用 DashScope 域名<br>• 快速模式：固定 model ID（`glm-5.2-fast-preview`）+ 地域专属域名（如 `{workspace_id}.cn-beijing.maas.aliyuncs.com`） |
| **计费方式** | • 微调阶段：按 GPU 小时计费（`instance_type` 决定单价）<br>• 部署阶段：按实例运行时长（小时）计费（GPU 规格 × 时间），**无请求量/[Token](../concepts/token.md) 关联计费** | • **PTU 模式**：预付费，按 kTPM × 天数（保底容量，溢出可自动转按量）<br>• **MU 模式**：后付费，按模型单元（MU）规格 × 运行时长<br>• **[Token](../concepts/token.md) 计费**：按实际输入/输出 token 计费（仅限 LoRA 模型） | • **TPM 预留**：预付费，按 kTPM × 自然日天数（当日 00:00–次日 00:00）<br>• **快速模式**：按 token 计费（输入/输出分别计价），单价高于标准 API（北京地域缓存命中单价 4 元） |
| **资源控制粒度** | • 实例级 GPU 规格（`instance_type`，如 `gpu-a10-2`）<br>• 批处理大小（`max_batch_size`）、并发请求数（`max_concurrent_requests`）创建时固定，**不支持运行时调整** | • PTU：以吞吐量（TPM）为单位，支持阶梯容量系数与缓存折扣<br>• MU：以模型单元（MU）为单位，支持 PD 分离、自定义推理模式、RPM/TPM 限流<br>• Token 计费：无资源预留，完全按需弹性 | • TPM 预留：锁定专属输入/输出 kTPM，保障高峰期不被公共资源限流<br>• 快速模式：优化 kernel 与调度，提升单请求 TPS（1.5~2×），**不提供资源独占保障** |
| **典型场景** | • 内部业务模型定制：基于私有数据微调 Qwen，并快速上线验证效果<br>• MLOps 流水线集成：自动化触发微调→评估→部署→灰度发布 | • SaaS 产品核心服务：需稳定 SLA 的对话引擎（PTU 保底+溢出）<br>• AI 编程助手：要求低首 Token 延迟与长上下文（MU + PD 分离）<br>• 效果验证期：低成本试用 LoRA 模型（Token 计费） | • 高并发客服系统：防止流量高峰时被公共资源限流（TPM 预留）<br>• Agent 多步推理链路：对输出速度敏感（快速模式提升 TPS）<br>• 关键链路兜底：TPM 预留 + 快速模式组合使用 |

---

## 各方案适用场景建议

### ✅ 推荐选择 `Model Production` 当：
- 你需要**从零开始构建定制化模型**（例如：用内部客服对话数据微调 Qwen2-7B）；
- 你重视**模型版本可追溯性与灰度发布能力**（`version_id` + `model_id` 统一管理）；
- 你希望**最小化运维复杂度**，接受按 GPU 实例小时计费，且对推理延迟/吞吐无严苛 SLA 要求；
- 你已有 ONNX/Triton 格式模型，需快速封装为 HTTP 服务。

> ⚠️ 注意：不适用于需要长上下文（>128K）、LoRA 增量更新、或按 token 精细计费的场景。

### ✅ 推荐选择 `Model Deployment 1` 当：
- 你已拥有**预置模型或 LoRA 微调成果**，需投入生产环境并承担明确 SLA；
- 你面临**多维度资源诉求**：既要保底吞吐（PTU）、又要低延迟（MU）、还要低成本验证（Token 计费）；
- 你需要**高级推理控制能力**：如 PD 分离降低首 Token 延迟、`enable_thinking` 模式、自定义 `max_context_length`；
- 你运营跨地域服务（北京 + 新加坡双地域支持）。

> ⚠️ 注意：全参微调模型无法直接部署；OSS 导入的 LoRA 模型不支持增量更新；API 部署当前仅限北京地域。

### ✅ 推荐选择 `Model High Speed Inference` 当：
- 你已在使用 `Model Deployment 1` 或其他方式部署模型，但**遭遇高峰期限流或响应速度瓶颈**；
- 你的业务对**确定性容量（TPM 预留）或单请求输出速率（快速模式）有硬性要求**；
- 你愿意为性能溢价付费，并能接受 preview 功能的演进风险（尤其快速模式）；
- 你计划组合使用：例如为 `glm-5.2-fast-preview` 创建 TPM 预留，兼顾容量保障与生成速度。

> ⚠️ 注意：TPM 预留是容量保障机制，**不是独立部署方案**；快速模式目前仅限单一模型，且不承诺生产级 SLA。

---

## 技术选型参考指南（面向开发者）

| 你的需求 | 推荐方案 | 关键理由 |
|----------|----------|----------|
| “我要用自己标注的数据训练一个专属客服模型，并一周内上线” | **Model Production** | 端到端支持微调+部署，控制台/API 全流程可视化，版本回滚便捷 |
| “我们 SaaS 产品已上线，现在要保障 99.9% 请求在 2s 内返回，且支持 100K 上下文” | **Model Deployment 1（MU 模式 + PD 分离）** | MU 提供资源独占、PD 分离优化首 Token 延迟、`max_context_length` 可配，SLA 可预期 |
| “营销活动期间流量激增 3 倍，现有部署频繁返回 429” | **Model High Speed Inference（TPM 预留）** | 锁定专属 kTPM，避免公共资源争抢；支持自动溢出，平滑承接突发流量 |
| “Agent 任务中，每步推理输出慢导致整体耗时超标” | **Model High Speed Inference（快速模式）** | `glm-5.2-fast-preview` TPS 提升 1.5~2×，显著缩短多步链路总延迟 |
| “刚训好一个 LoRA 模型，想先小流量验证效果再决定是否采购资源” | **Model Deployment 1（Token 计费模式）** | 零资源预留成本，按实际 token 付费，适合效果验证与 AB 测试 |
| “我们需要同时支持北京和新加坡用户，且两地模型配置需一致” | **Model Deployment 1（控制台双地域部署）** | 控制台原生支持北京/新加坡双地域，API 部署虽限北京，但可通过多 workspace 实现跨域管理 |

> 💡 **终极建议**：  
> - **起步阶段**：优先用 `Model Production` 快速验证模型效果；  
> - **规模化上线**：迁移到 `Model Deployment 1`，根据负载特征选择 PTU/MU/Token 模式；  
> - **性能攻坚期**：叠加 `Model High Speed Inference`（TPM 预留或快速模式）解决瓶颈；  
> - **禁止混用误区**：`Model Production` 部署的实例**不能**直接绑定 TPM 预留或启用快速模式——二者属于不同服务栈，需重新部署。

## 被对比主题页

- [model production](../api/model-production.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


