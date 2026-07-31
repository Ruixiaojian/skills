# 模型部署方式对比：托管服务、高并发推理与自定义部署

为帮助开发者在百炼平台上高效、可靠地将模型投入生产，本文系统对比三种主流部署路径：**托管服务（Model Production）**、**高并发推理（Model High Speed Inference）** 和 **自定义部署（Model Deployment 1）**。三者定位不同——托管服务聚焦“从微调到上线”的端到端闭环；高并发推理面向已上线模型的**性能保障与加速**；自定义部署则提供**资源隔离、精细调控与多计费模式**的生产级服务化能力。本对比旨在厘清能力边界、明确适用条件，辅助技术选型决策。

---

## 关键维度对比表

| 维度 | 托管服务（`model production`） | 高并发推理（`model high speed inference`） | 自定义部署（`model deployment 1`） |
|------|------------------------------|------------------------------------------|-----------------------------------|
| **核心定位** | 微调模型 → 生产部署的一体化流程（含训练、版本管理、灰度发布） | 对**已存在模型服务**进行吞吐保障（TPM预留）或解码加速（Fast Mode） | 将预置/导入模型部署为**独立、资源隔离的推理服务**，支持多种资源模型 |
| **输入格式** | 标准 OpenAI 兼容格式（`messages` 或 `prompt`/`completion`），仅支持 `.jsonl` 微调数据集 | 完全兼容标准 API 输入（`/v1/chat/completions` 等），无需格式变更 | 完全兼容标准 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/v1/chat/completions`, `/v1/embeddings` 等） |
| **输出格式** | 标准 OpenAI 兼容响应（含 `choices[0].message.content`）；不支持 Fast Mode 特有字段 | ✅ TPM 预留：同标准格式<br>✅ 快速模式：需解析 `delta.reasoning_content` + `delta.content`（流式专属结构） | 标准 OpenAI 兼容响应；MU 模式可选启用 `thinking` 流式分阶段输出 |
| **支持模型** | ✅ 平台内微调产出的模型（`model_id`）<br>❌ 不支持任意本地模型直传；仅限官方模型库或微调结果 | ✅ 主流预置模型（Qwen、GLM、DeepSeek、Kimi 等）的**标准版**<br>✅ 快速模式仅限 `glm-5.2-fast-preview`（北京/新加坡） | ✅ 全量预置模型（Qwen3/Qwen2.5/VL/Omni、GLM-4.7/5.x、DeepSeek-v3/v4、Kimi-K2.5）<br>✅ LoRA 微调后导入模型（OSS 导入）<br>❌ 全参微调模型暂不支持 |
| **API 端点** | `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/v1/chat/completions`（部署后返回专属 `endpoint`） | ✅ TPM 预留：复用标准域名，仅需替换 `model` 参数为专属 code<br>✅ 快速模式：**必须使用专属域名** `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/v1/chat/completions`（统一标准 endpoint，通过 `model_name` 路由） |
| **计费方式** | ✅ 按实例规格（`instance_type`）+ 运行时长计费（秒级）<br>✅ 副本数（`replicas`）决定并发能力与成本 | ✅ TPM 预留：按**预购输入/输出 TPM（kTPM/月）** 计费，溢出部分按量计费<br>✅ 快速模式：**按实际 token 消耗计费**（无额外加速费用，但 TPS 提升间接降低单位 token 成本） | ✅ PTU 模式：按预购 `input_tpm` / `output_tpm`（token/分钟）计费，支持缓存折扣与长输入阶梯系数<br>✅ MU 模式：按 **模型单元（MU）规格 × 副本数 × 运行时长** 计费<br>✅ LoRA 模式：按 token 按量计费（仅用于效果验证） |
| **弹性扩缩容** | ✅ 支持 `PATCH /deployments/{id}` 动态调整 `replicas`（需注意实例类型不可变） | ❌ TPM 预留：容量固定，缩容/退订产生违约金<br>❌ 快速模式：无扩缩容能力，依赖底层资源池 | ✅ PTU：额度固定，但请求自动溢出至按量（可配置）<br>✅ MU：支持动态增减 `capacity`（副本数），实时生效<br>✅ LoRA：无扩缩容概念（按量计费） |
| **灰度与版本控制** | ✅ 原生支持 `traffic_split`（如 `{ "v1": 80, "v2": 20 }`）<br>✅ 每个微调作业生成唯一 `model_id`，部署时指定 `model_version` | ❌ 不提供灰度能力<br>❌ 无版本管理（TPM/Fast Mode 作用于模型 code 层） | ✅ MU/PTU 模式支持多 `deployed_model` 实例并存，可手动路由流量<br>❌ 无内置灰度分流 API，需业务层实现 |
| **典型场景** | - 新模型快速验证上线<br>- 垂类任务（客服问答、合同解析）微调后一键部署<br>- 需要版本回滚与 A/B 测试的迭代场景 | - 高峰期保障核心模型不被限流（TPM 预留）<br>- AI 编程助手、Agent 多步推理等对首 token 延迟敏感场景（Fast Mode）<br>- 已上线模型的 SLA 提升需求 | - 长上下文（最高 256K）、前缀缓存等高级推理需求（PTU）<br>- 需 PD 分离、自定义 `max_context_length` 或 RPM/TPM 限流的定制化服务（MU）<br>- LoRA 微调效果快速验证（LoRA 模式） |

---

## 各方案适用场景建议

### ✅ 托管服务（`model production`）适合：
- **快速验证闭环**：从数据准备 → 微调 → 部署 → 灰度发布的全流程自动化需求；
- **垂类模型轻量上线**：如客服对话、知识库问答等 SFT 场景，且对长上下文、极致延迟无严苛要求；
- **需要强版本控制与回滚能力**：当模型迭代频繁、需保障线上服务稳定性时；
- **团队协作开发**：微调作业与部署实例绑定清晰，便于权限与生命周期管理。

> ⚠️ 注意：不适用于需独占算力、超长上下文（>32K）、或需对接已有运维体系（如 Prometheus 监控集成）的重载生产环境。

### ✅ 高并发推理（`model high speed inference`）适合：
- **存量服务性能加固**：已有基于百炼标准 API 的应用，需应对流量洪峰或降低首 token 延迟；
- **SLA 敏感型业务**：如实时对话机器人、低延迟 Agent，无法容忍 429 错误或 >100ms 首 token；
- **临时性加速需求**：快速模式处于 preview 阶段，适合技术预研与 PoC 验证；
- **成本可控的吞吐保障**：TPM 预留提供确定性容量，避免按量计费波动风险。

> ⚠️ 注意：非部署方案，**必须已有可用模型服务**；快速模式地域与模型限制严格，生产环境需密切关注控制台状态更新。

### ✅ 自定义部署（`model deployment 1`）适合：
- **生产级稳定服务**：要求资源隔离、独立监控、SLA 可承诺（如 99.9% 可用性）；
- **复杂推理策略**：需启用 Thinking 模式、自定义上下文长度、RPM/TPM 精细限流；
- **长文本与缓存优化场景**：文档解析、法律合同审查等需 64K–256K 上下文及前缀缓存；
- **混合计费策略**：如核心服务用 PTU 保底 + 非核心用 LoRA 按量验证；
- **企业级治理需求**：需对接内部审批流、配额管理、审计日志等。

> ⚠️ 注意：API 部署当前仅支持华北2（北京）地域；MU 模式需关注 `deploy_spec` 与模型显存匹配；LoRA 导入有严格 OSS 权限与参数约束。

---

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键理由 |
|----------|----------|----------|
| “我刚微调完一个 Qwen2.5 模型，想立刻上线测试效果，并支持灰度发布” | ✅ 托管服务 | 原生支持 `model_id` 直接部署 + `traffic_split`，5 分钟完成从微调到灰度 |
| “我们的客服机器人调用 Qwen3，高峰期常触发 429，但不想重构代码” | ✅ 高并发推理（TPM 预留） | 仅需替换 `model` 参数，零代码改造即可锁定专属吞吐，保障 SLA |
| “AI 编程助手要求首 token <80ms，且需多步 reasoning 输出” | ✅ 高并发推理（快速模式） + ✅ 自定义部署（MU 模式） | 快速模式专为低延迟设计；若需长期稳定，MU 模式可启用 `enable_thinking` 并定制硬件规格 |
| “要部署一个支持 200K 上下文的法律大模型，且需前缀缓存降低成本” | ✅ 自定义部署（PTU 模式） | PTU 明确支持 256K 上下文与缓存折扣，长输入阶梯系数可精准控本 |
| “我们有多个 LoRA 微调模型，需低成本验证效果，再择优上线” | ✅ 自定义部署（LoRA 模式） | 专为 LoRA 设计，按 token 计费，无资源预留成本，验证完毕可无缝迁至 PTU/MU |
| “需要将本地训练的全参微调模型（非 LoRA）部署上线” | ❌ 当前均不支持 | 百炼平台暂未开放全参微调模型导入能力，请关注后续 `model import` 功能演进 |

> 💡 **组合使用提示**：  
> - 托管服务部署的模型，可叠加高并发推理（如为 `qwen2.5-ft-xxx` 创建 TPM 预留）；  
> - 自定义部署的 PTU/MU 服务，可作为托管服务的上游模型源（通过 `model_id` 引用）；  
> - 快速模式与 TPM 预留**暂不兼容**（`glm-5.2-fast-preview` 尚未开放 TPM 预留入口），需权衡优先级。

---  
*最后更新：2024年10月 | 文档依据：百炼平台 v2.3 API 规范与用户指南*

## 被对比主题页

- [model production](../api/model-production.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model deployment 1](../guides/model-deployment-1.md)


