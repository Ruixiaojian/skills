# 模型部署方案对比：Model Deployment vs Model Production

本文旨在帮助开发者清晰区分百炼平台中两类核心模型服务化能力——**Model Deployment（模型部署）** 与 **Model Production（模型生产）**，明确其定位、能力边界与适用阶段。随着大模型应用从实验验证走向规模化落地，选择恰当的服务化路径直接影响开发效率、资源成本与运维复杂度。本文基于当前平台能力（截至 2025 年 Q3），从技术实现、模型支持、计费逻辑与生命周期管理等维度进行客观对比，为工程化选型提供依据。

## 关键维度对比

| 维度 | Model Deployment | Model Production |
|------|------------------|------------------|
| **定位与目标** | 快速将**已有模型**（预置或 LoRA）转化为高可用推理服务，聚焦“即开即用”的服务化交付 | 支持从**训练/微调到上线**的端到端闭环，聚焦“定制化模型诞生→稳定服务”的全生命周期管理 |
| **输入格式** | • 预置模型 ID（如 `qwen3-8b`）<br>• LoRA 模型 ZIP 包（含 `adapter_model.safetensors` + `config.json`，需满足 rank 一致性与 VIT 冻结约束） | • 微调任务输出的完整模型 ID（如 `ft-qwen2-7b-20240510-123456`）<br>• 或已导入的完整模型快照（GGUF/Safetensors 格式，需含权重、tokenizer、config） |
| **输出格式** | 统一 RESTful API 接口（`/v1/chat/completions`），模型参数通过 `model=deployed_model_id` 指定；返回标准 OpenAI 兼容响应体 | 独立 HTTP endpoint URL（如 `https://dashscope.aliyuncs.com/v1/endpoint/ep-xxx/chat/completions`），需显式构造请求地址；响应结构与 Model Deployment 一致 |
| **支持模型类型** | • ✅ 预置大模型（Qwen、DeepSeek、GLM、Kimi、CosyVoice 等）<br>• ✅ LoRA 微调模型（仅限 LoRA，不支持 QLoRA/Adapter/全参微调）<br>• ❌ 不支持 GGUF、独立 Safetensors 完整模型 | • ✅ 全参微调（SFT）产出的完整模型快照<br>• ✅ 手动导入的 GGUF / Safetensors 完整模型<br>• ⚠️ LoRA 权重需先调用 `merge_lora=true` 合并为完整模型后方可部署（不支持纯 LoRA 推理） |
| **API 端点与调用方式** | • 创建：`POST /api/v1/deployments`（统一部署接口）<br>• 调用：复用 `/v1/chat/completions`，`model` 参数传入部署 ID<br>• SDK 支持：`Generation.call(model='deployed_id', ...)` | • 创建：`POST /v1/deployments`（需指定 `model_id` + `instance_type`）<br>• 调用：专用 endpoint URL 的 `/v1/chat/completions`（非共享路径）<br>• SDK 支持：需手动构造请求或使用 `EndpointClient` |
| **计费方式** | • **PTU 模式**：预付费吞吐额度（input/output TPM），超限可自动溢出计费<br>• **MU 模式**：按模型单元规格（如 MU1）+ 副本数预付费，支持 PD 分离与限流<br>• **Token 计费**：按实际 token 使用量计费（仅 LoRA 模型可用，API 中 `"plan": "lora"` 实为 `"plan": "token"` 别名） | • **按实例规格计费**：基于所选 ECS 实例类型（如 `ecs.gn7i-c16g1.4xlarge`）按秒/小时计费<br>• **无预置吞吐或模型单元概念**，费用 = 实例运行时长 × 单价<br>• 微调任务单独计费（GPU 小时） |
| **典型场景** | • 快速验证预置模型效果<br>• 为 LoRA 微调结果提供低成本、弹性推理服务<br>• 高并发稳态业务（PTU）、高性能隔离需求（MU）、A/B 测试（Token 计费） | • 需要全参微调以适配垂直领域任务（如金融问答、医疗报告生成）<br>• 要求模型完全可控、可审计、可回滚的生产环境<br>• 需灰度发布、多版本共存、细粒度实例资源控制 |
| **扩缩容能力** | • PTU/MU 模式：支持自动扩缩容（基于负载指标）<br>• Token 计费：天然弹性，无需预设容量 | • 手动扩缩容：通过更新 deployment 的 `instance_count` 或重建 deployment 实现<br>• 无自动扩缩容能力（需自行集成监控与调度逻辑） |
| **生命周期管理** | • 部署即服务，无版本概念；删除即释放全部资源<br>• PTU/MU 预付费资源需单独退订 | • 显式版本管理：`fine_tuning_job_id` → `model_id` → `endpoint_id`<br>• 支持灰度发布、版本回滚、多 endpoint 关联同一 model_id |

## 各方案的适用场景建议

### ✅ 优先选择 **Model Deployment** 当：
- 你使用的是百炼平台预置的主流大模型（如 Qwen3、GLM-5），且无需修改模型结构；
- 你已完成 LoRA 微调，并希望以最低门槛、最快速度上线推理服务（尤其适合 PoC、MVP 或轻量级业务）；
- 业务流量可预测（选 PTU）、需强性能隔离（选 MU），或需按调用量精确分摊成本（选 Token 计费）；
- 团队希望避免基础设施运维，专注业务逻辑与 [prompt](../guides/prompt.md) 工程。

### ✅ 优先选择 **Model Production** 当：
- 你需要对模型进行**全参监督微调（SFT）**，例如适配私有知识库、重构输出格式、提升特定任务指标；
- 你拥有自研或第三方训练好的完整模型（GGUF/Safetensors），要求 100% 模型自主权与可复现性；
- 生产环境要求严格合规：需审计模型来源、支持灰度发布、保留历史版本、实现故障快速回滚；
- 你具备一定的 DevOps 能力，愿意为更精细的资源控制（如 GPU 型号、内存配额、并发上限）承担额外配置成本。

### ⚠️ 注意规避的误用情形
- **不要用 Model Production 部署 LoRA**：其 API 要求 `model_id` 对应完整模型快照；若强行传入 LoRA ID，将报错 `Model not found`。LoRA 场景请坚定使用 Model Deployment 的 `"plan": "lora"`（即 Token 计费）模式。
- **不要用 Model Deployment 运行全参微调模型**：它不接受 `.bin`/`.safetensors` 完整权重包，仅支持预置模型 ID 或 LoRA ZIP 包。
- **高 SLA 要求场景慎用 Token 计费**：虽弹性好，但无容量保障，突发流量可能导致延迟升高；关键业务建议选用 PTU 或 MU 模式。

## 技术选型决策树（面向开发者）

```text
开始选型
│
├─ 你的模型是「预置模型」或「LoRA 微调结果」？ → 是 → 进入 Model Deployment
│   ├─ 需要极致低成本 & 流量波动大？ → 选 Token 计费（"plan": "lora"）
│   ├─ 流量稳定且需确定性性能？ → 选 PTU 模式（预置吞吐）
│   └─ 需要首 Token 低延迟、自定义上下文长度或硬性限流？ → 选 MU 模式
│
└─ 你的模型是「全参微调产出」或「自研完整模型」？ → 是 → 进入 Model Production
    ├─ 是否需要灰度发布/版本回滚/多 endpoint 管理？ → 是 → Model Production（必选）
    └─ 是否需指定 GPU 型号、精确控制并发数？ → 是 → Model Production（优势明显）
```

> 💡 **一句话总结**：  
> **Model Deployment 是“模型即服务”（Model-as-a-Service）的极简实现，追求开箱即用与弹性经济；**  
> **Model Production 是“模型工厂”（Model Factory）的生产流水线，追求定制自由与工程可控。**  
> 二者非替代关系，而是互补演进：LoRA 快速验证 → Model Production 全参精调 → Model Deployment 批量交付多个 LoRA 变体，构成高效迭代闭环。

---  
*最后更新：2025年7月28日*  
*文档状态：正式版（v2.3）*

## 被对比主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model production](../api/model-production.md)


