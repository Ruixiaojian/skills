# 模型部署方式对比：Model Production vs Model Deployment 1

本文旨在帮助开发者清晰区分百炼平台中两种核心模型服务化能力——`Model Production`（模型生产）与 `Model Deployment 1`（模型部署 1），明确其定位、能力边界与适用阶段。二者虽均面向“将模型变为可用 API 服务”，但设计目标、抽象层级、资源模型与运维责任存在本质差异：  
- **Model Production** 是**模型生命周期编排层**，聚焦“从训练成果到可调用服务”的端到端自动化流程，强调微调与部署的强耦合、统一管控与快速验证；  
- **Model Deployment 1** 是**生产级推理服务交付层**，聚焦“已就绪模型在高负载、多 SLA 场景下的稳定、可控、可计量运行”，强调性能隔离、计费精细化与企业级运维保障。  
正确理解二者关系（非互斥，而是演进关系），是构建稳健 AI 应用的关键前提。

## 关键维度对比

| 维度 | Model Production | Model Deployment 1 |
|------|------------------|----------------------|
| **核心定位** | 模型生产流水线：统一管理微调任务 + 部署服务，实现“训完即用” | 生产级推理服务交付：为已就绪模型提供资源独占、SLA 可控、计费灵活的专属服务 |
| **输入格式** | • 微调：标注数据集 ID（`training_file_id`）+ 基座模型名（如 `qwen2-7b`）<br>• 部署：已完成微调/导入的模型 ID（`model_id`） | • 预置模型：标准模型名（如 `qwen-flash-2025-07-28`）<br>• 调优模型：SFT/LoRA 模型 ID（如 `qwen3-8b-ft-20251113...`）<br>• 导入模型：OSS 路径 + LoRA 模型约束校验通过的 `adapter_model.safetensors` 等文件 |
| **输出格式** | • 微调输出：`model_id`（唯一标识新模型版本）<br>• 部署输出：全局唯一 `endpoint_url`（如 `https://my-llm-v1.bailian.aliyuncs.com/v1/chat/completions`） | • 所有模式均输出标准 DashScope/OpenAI 兼容 API 端点（如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`），通过 `model_name`（部署服务名）路由请求 |
| **支持模型类型** | • 仅支持百炼平台内完成的 SFT 微调模型<br>• 支持通过 [模型导入](../../raw/model-api-reference/model-production/deployments-api.md) 上传的完整权重模型（但**不可用于微调**）<br>• 不支持 LoRA、多模态、RLHF 模型 | • **预置模型**：Qwen / DeepSeek / GLM / Qwen-VL 全系列（含 Flash/Plus/VL 等变体）<br>• **调优模型**：平台内 SFT/LoRA 微调产出的模型 ID<br>• **导入模型**：仅限符合约束的 LoRA 模型（rank ∈ {8,16,32,64}，VIT 冻结，chat_template 未修改） |
| **API 端点** | • 微调：`POST /v1/fine_tuning_jobs`<br>• 部署：`POST /v1/deployments`<br>• 推理：`POST {endpoint_url}/v1/chat/completions`（专属域名） | • 部署：DashScope API `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/deployments`<br>• 推理：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`（通用域名，按 `model_name` 路由） |
| **计费方式** | • **统一按实例规格 + 运行时长计费**：<br> - 微调任务：GPU 实例小时费 × 实际运行时长（≤72h）<br> - 部署服务：GPU 实例小时费 × 在线时长（自动扩缩容，min=1/max=5）<br>• 无 PTU/MU/[Token](../concepts/token.md) 等分层计费概念 | • **三类独立计费模式**：<br> - **PTU（预置吞吐）**：预购输入/输出 token 分钟额度，超限可选自动溢出或限流<br> - **MU（模型单元）**：按模型单元规格（如 MU1 x 8）后付费，支持 PD 分离、Thinking 模式、RPM/TPM 限流<br> - **[Token](../concepts/token.md) 计费（LoRA 专属）**：按实际请求 token 数量计费，仅限导入 LoRA 模型 |
| **资源调度与隔离** | • 自动扩缩容（默认 min=1, max=5），共享资源池<br>• 无物理/逻辑资源独占保障，适合开发测试与中小流量场景 | • **全模式资源独占**：<br> - PTU：逻辑吞吐隔离，共享底层 GPU，但配额硬保障<br> - MU：物理 GPU 卡级隔离（如 MU1 = 1×A10），完全独占<br> - [Token](../concepts/token.md)：共享资源池，但按 token 精确计量，无资源预留 |
| **典型场景** | • 快速验证微调效果（训完立刻部署试跑）<br>• 内部工具链集成（CI/CD 中自动触发微调→部署→测试）<br>• 小规模 PoC 或 MVP 应用，流量波动大、SLA 要求不高 | • 面向终端用户的高并发应用（如客服机器人、内容生成平台）<br>• 对首 Token 延迟、稳定性、上下文长度有严苛要求的业务（如实时对话、长文档摘要）<br>• 需要精细成本控制与预算规划的企业级部署（PTU 预算锁定 / MU 性能保障 / LoRA 效果验证） |

## 各方案适用场景建议

### ✅ 推荐使用 **Model Production** 当：
- 你正在**迭代优化模型**，需要频繁执行“微调 → 验证 → 调参 → 再微调”闭环；
- 你的工作流高度依赖**自动化编排**（例如 GitHub Actions 触发微调、成功后自动部署到测试环境）；
- 应用处于**早期验证阶段**，流量低且不稳定，无需承诺 SLA 或精确成本控制；
- 你使用的是**完整权重微调模型**，且不涉及 LoRA、视觉语言等复杂架构。

> ⚠️ 注意：若需长期稳定服务、高并发或定制化性能策略（如 PD 分离、Thinking 模式），不应止步于 Model Production，应将其产出的 `model_id` 作为输入，迁移到 Model Deployment 1。

### ✅ 推荐使用 **Model Deployment 1** 当：
- 模型已**完成调优并进入生产发布阶段**，需提供稳定、可计量、可运维的服务；
- 业务对**延迟（P99 < 500ms）、吞吐（≥1000 RPM）、上下文长度（≥128K）** 有明确 SLA 要求；
- 需要**精细化成本治理**：如用 PTU 锁定月度预算、用 MU 保障关键业务性能、用 Token 模式低成本验证多个 LoRA 方案；
- 部署模型为**LoRA 适配器**（尤其是 OSS 导入场景），或需利用前缀缓存、长输入优化等高级推理特性；
- 需要**企业级管控能力**：如 RPM/TPM 限流、自定义推理模式（Instruct/Thinking）、跨模型灰度发布。

> ⚠️ 注意：Model Deployment 1 **不提供微调能力**。若需微调，必须先通过 Model Production 完成训练，再将产出的 `model_id` 作为 `model_name` 输入 Model Deployment 1 进行部署。

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键理由 | 行动指引 |
|----------|-----------|-----------|-----------|
| “我刚微调完一个 Qwen2-7B 模型，想立刻让同事试用一下效果” | ✅ Model Production | 一键部署，5 分钟内获得专属 endpoint，无需配置计费与规格 | 调用 `POST /v1/deployments`，传入微调任务返回的 `model_id` |
| “我的客服系统日均 5000 请求，要求首 Token < 800ms，P95 延迟 < 2s” | ✅ Model Deployment 1（MU 模式） | MU 提供物理 GPU 隔离与 PD 分离计算，可精准控制延迟与并发 | 控制台选择 `MU2 x 4` 规格，启用 `enable_thinking: false`，设置 `rpm_limit: 100` |
| “我要上线一个内容生成 SaaS，需按客户用量精确计费，且支持突发流量” | ✅ Model Deployment 1（PTU 模式） | PTU 提供吞吐硬保障 + 自动溢出机制，兼顾成本确定性与弹性 | 预购 `input_tpm: 50000, output_tpm: 5000`，溢出策略设为 `auto_overflow` |
| “我有多个 LoRA 方案（不同 [prompt](../guides/prompt.md) 工程/领域适配），想低成本批量验证效果” | ✅ Model Deployment 1（Token 计费模式） | 仅对实际 token 收费，无资源预留成本，适合 A/B 测试与快速淘汰 | 使用 `plan: "lora"` 部署各 LoRA 模型 ID，监控 token 消耗与效果指标 |
| “我需要把本地训练的 LoRA 模型（rank=32）部署到百炼，且保持 VIT 冻结” | ✅ Model Deployment 1（LoRA 导入 + Token 计费） | 唯一支持 OSS LoRA 导入的路径，且严格校验 rank/VIT 约束 | 按 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md) 文档准备文件，部署时指定 `plan: "lora"` |
| “我需要在微调过程中实时查看 loss 曲线，并自动保存最佳 checkpoint” | ❌ 两者均不直接支持 | Model Production 仅提供日志与最终 model_id；Model Deployment 1 不涉及训练 | 需结合百炼 [训练作业日志](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) + 自定义 callback 或外部监控 |

> 💡 **最佳实践组合**：  
> **开发期** → 使用 `Model Production` 快速迭代微调与轻量部署；  
> **发布期** → 将验证通过的 `model_id` 输入 `Model Deployment 1`，按业务 SLA 选择 PTU/MU/Token 模式部署；  
> **运维期** → 通过 Model Deployment 1 的控制台/API 统一管理扩缩容、限流、计费账单，Model Production 仅用于后续版本迭代。

## 被对比主题页

- [model production](../api/model-production.md)
- [model deployment 1](../guides/model-deployment-1.md)


