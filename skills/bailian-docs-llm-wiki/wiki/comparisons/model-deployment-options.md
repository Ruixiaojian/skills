# 模型部署方式对比：Model Production vs Model Deployment

本文旨在帮助开发者清晰区分百炼平台中两类核心模型服务化路径——**Model Production（模型生产）** 与 **Model Deployment（模型部署）**，明确其定位差异、能力边界与适用阶段。二者虽均以“发布可调用模型服务”为目标，但在设计目标、技术路径、生命周期管理粒度及面向场景上存在本质区别：  
- **Model Production** 是端到端的 *模型定制与交付流水线*，聚焦“从零构建专属模型”，强调训练+部署一体化、版本可追溯、私有化适配；  
- **Model Deployment** 是即开即用的 *推理服务编排体系*，聚焦“将已有模型快速上线为稳定服务”，强调弹性、计费灵活、高并发保障与细粒度资源控制。  
正确理解二者差异，是避免重复建设、规避权限/格式错误、实现成本与性能最优平衡的关键前提。

## 关键维度对比

| 维度 | Model Production | Model Deployment |
|------|------------------|------------------|
| **核心定位** | 模型定制化生产流水线（训练 + 部署一体化） | 已有模型的推理服务化编排（仅部署，不训练） |
| **输入格式** | - 微调：JSONL 格式指令数据集（OSS 路径）<br>- 部署：`fine_tuned_model_id` 或符合 ONNX/Triton 规范的第三方模型包（ZIP/OSS 路径） | - PTU/MU：预置模型 ID 或已成功导入的 LoRA 模型 ID<br>- [Token](../concepts/token.md) 计费：仅支持已通过校验的 LoRA 模型 ID（`qwen3-8b-ft-*` 等）<br>（注：不接受原始 Hugging Face 模型或自定义训练权重直接上传） |
| **输出格式** | 统一 `/v1/chat/completions` 推理接口（兼容 OpenAI 标准），返回 `choices[].message.content` 等标准字段 | 统一 `/v1/chat/completions` 推理接口（兼容 OpenAI 标准），但不同部署方式在响应头、流式行为、长文本处理逻辑上存在差异（如 PTU 返回 `x-dashscope-ptu-overflow`） |
| **支持模型类型** | - 基础模型：仅限平台白名单（如 `qwen2-7b-chat`）<br>- 微调方式：监督微调（SFT），支持 LoRA（API 显式支持 `lora_target_modules`）<br>- 导入模型：ONNX / Triton 格式，需平台兼容性验证 | - PTU：主流预置模型（如 `qwen3.8-max`, `deepseek-v4-flash`） + 所有 LoRA 模型<br>- MU：全部预置模型 + 所有 LoRA 模型（含千问/GLM/DeepSeek/Kimi/CosyVoice）<br>- [Token](../concepts/token.md) 计费：**仅 LoRA 模型**（且必须完成 OSS 导入与状态校验）<br>（⚠️ 全参微调模型、未验证 Hugging Face 模型、视觉语言模型 VIT 未冻结者均不支持） |
| **API 端点** | - 微调：`POST /v1/fine_tuning/jobs`<br>- 部署：`POST /v1/deployments`<br>- 调用：`POST {endpoint_url}/v1/chat/completions` | - 统一创建接口：`POST /api/v1/deployments`（仅华北2北京可用）<br>- 调用：`POST {endpoint_url}/v1/chat/completions`（各部署方式 endpoint 独立） |
| **计费方式** | - 微调阶段：按 GPU 小时计费（任务运行时长 × 实例规格单价）<br>- 部署阶段：按实例规格（CPU/GPU）+ 副本数 + 运行时长计费（类似云服务器）<br>- **无按 [Token](../concepts/token.md) 或吞吐量计费选项** | - **PTU**：预购吞吐容量（Input/Output TPM），固定月费，溢出部分按量计费<br>- **MU**：按部署规格（如 `MU1`）+ 副本数 + 运行时长计费（资源独占）<br>- **Token 计费**：按实际请求 token 数（input + output）实时计费（仅 LoRA 模型） |
| **扩缩容能力** | 支持配置 `replicas`，但**不支持暂停（scale to zero）**；最小副本数为 1 | - PTU：吞吐固定，无副本概念，自动负载均衡<br>- MU：支持动态调整 `capacity`（副本数），支持 PD 分离模式扩展<br>- Token 计费：`capacity` 参数无效，扩缩容需人工申请，无自动扩缩容 |
| **典型场景** | - 需对基础模型进行领域适配（如金融问答、医疗术语微调）<br>- 需私有化部署、数据不出域<br>- 需完整模型版本管理（训练版本 ↔ 部署版本强绑定）<br>- 需高性能推理（GPU 实例直通） | - PTU：高并发、低延迟、长文本（≤1M token）稳定服务（如客服对话引擎）<br>- MU：需要精细调优推理参数（`temperature`, `max_context_length`, `rpm_limit`）、启用思考模式、或需 PD 分离架构的复杂业务<br>- Token 计费：A/B 测试、效果验证、POC 快速验证、低频调用（如内部工具） |

## 各方案适用场景建议

| 场景描述 | 推荐方案 | 关键原因 |
|----------|----------|----------|
| **需要基于自有数据训练一个全新领域模型（如法律合同解析专用模型），且要求模型完全私有、可版本回滚、支持 GPU 加速推理** | ✅ Model Production | 唯一支持 SFT 训练 + 自定义 GPU 实例部署 + 完整版本链路（`job_id` → `fine_tuned_model_id` → `deployment_id`） |
| **已有 LoRA 微调成果（`adapter_model.safetensors`），希望快速上线为高可用服务，并支持长上下文（512K tokens）与前缀缓存优化** | ✅ Model Deployment（PTU） | PTU 原生支持 LoRA 模型 + 1M token 输入 + 缓存加速，吞吐保障优于手动部署的 Model Production 实例 |
| **需对同一模型同时提供“思考模式”（CoT）和“非思考模式”两种推理路径，并严格限制每分钟请求数（RPM）与每分钟 Token 数（TPM）** | ✅ Model Deployment（MU） | MU 支持 `enable_thinking` 开关与 `rpm_limit`/`tpm_limit` 精细限流，Model Production 不提供此类运行时策略控制 |
| **正在验证多个 LoRA 方案效果，每天调用量仅数百次，无需长期占用资源，追求最低试错成本** | ✅ Model Deployment（Token 计费） | 按实际 token 支付，无闲置成本；Model Production 的最小部署实例（1 副本）会产生持续计费，不经济 |
| **需部署一个未经百炼验证的自定义 PyTorch 模型（非 LoRA，非 ONNX/Triton），且必须使用 CPU 推理** | ⚠️ Model Production（有限支持） | Model Production 支持导入 ONNX/Triton 模型，若您的模型可转换为 ONNX 并通过兼容性验证，则可行；否则两种方案均不支持。建议优先转换格式。 |
| **希望将 Hugging Face 上的 `Llama-3.1-70B-Instruct` 直接部署为 API 服务** | ❌ 两者均不推荐 | Model Production 要求基础模型在白名单内（Llama 系列未开放）；Model Deployment 仅支持百炼预置模型或已校验 LoRA，不支持任意 HF 模型直接部署。需联系商务定制支持。 |

## 技术选型参考（面向开发者）

- **第一步：确认你的“模型资产”来源**  
  → 若模型尚未存在（需从头训练）→ 选 **Model Production**；  
  → 若模型已存在（预置模型 ID / LoRA 模型 ID / ONNX 包）→ 进入第二步。

- **第二步：评估服务 SLA 与成本模型**  
  → 高并发、稳态流量、长文本 → 优先 **PTU**；  
  → 需要动态调参、限流、PD 分离 → 选 **MU**；  
  → 低频、验证性、预算敏感 → 选 **Token 计费**；  
  → 需要 GPU 加速、私有化、训练闭环 → 回退至 **Model Production**（即使已有模型，也可用其部署 ONNX/Triton 包）。

- **第三步：检查约束条件**  
  ✅ 验证模型是否在 [预置模型列表](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md) 或 [LoRA 导入规范](../../raw/model-user-guide/model-deployment-1/model-import.md) 内；  
  ✅ 确认地域（API 部署仅支持华北2北京）；  
  ✅ 检查权限（Workspace 是否拥有目标模型部署权限）；  
  ✅ 若用 Model Production，确认数据集 ≤100 MB 且单样本 ≤8192 token。

- **最后提醒**：  
  - **计费方式不可变**：Model Deployment 创建后无法切换 PTU/MU/Token 计费，务必一次选对；  
  - **模型不可混用**：全参微调模型（来自 Model Production）**不能**直接用于 Model Deployment（MU/Token 计费），反之亦然；  
  - **调试建议**：新模型首次上线，推荐先用 Token 计费快速验证功能，再根据压测结果升级至 PTU 或 MU。

## 被对比主题页

- [model production](../api/model-production.md)
- [model deployment 1](../guides/model-deployment-1.md)


