# 模型部署方式对比：Model Deployment、High-Speed Inference 与 Model Production

为帮助开发者在百炼平台上高效、可靠地将模型投入实际业务，本文系统对比三种核心模型服务化能力：**Model Deployment（模型部署）**、**High-Speed Inference（高性能推理）** 和 **Model Production（模型生产）**。三者定位不同——Model Deployment 聚焦**生产级服务化交付**，High-Speed Inference 专注**性能维度的定向增强**，Model Production 则面向**训练-微调-上线的端到端自动化流水线**。本对比旨在厘清能力边界、适用条件与技术约束，辅助团队基于 SLA 要求、运维复杂度、成本模型及开发流程选择最优路径。

## 关键维度对比

| 维度 | Model Deployment | High-Speed Inference | Model Production |
|------|------------------|-----------------------|------------------|
| **本质定位** | 生产就绪的模型服务化平台（含资源隔离、SLA 保障、全生命周期管理） | 推理性能增强插件（非独立服务，需依附于基础 API 或已部署模型） | 端到端模型工程平台（覆盖微调、部署、作业管理的 API-first 流水线） |
| **输入格式** | 标准 OpenAI/DashScope 兼容请求体（`messages`, `prompt`, `max_tokens` 等）；PTU 模式支持超长输入（最高 1M token） | 同标准 API 格式；快速模式需额外解析 `delta.reasoning_content` 字段 | 百炼专属 RESTful 请求体（`model`, `name`, `scale_type`），调用时需显式指定 `endpoint` URL |
| **输出格式** | 完全兼容 OpenAI/DashScope 响应结构（含 `choices[0].message.content`, `usage`, `service_tier`, `x-dashscope-ptu-overflow` 等） | 同标准 API；快速模式响应中 `delta` 包含 `reasoning_content` 与 `content` 双流字段 | 百炼定制化 JSON（含 `id`, `endpoint`, `status`, `created_at`），推理调用需直连 `endpoint` 并遵循 `/v1/chat/completions` 协议 |
| **支持模型** | ✅ 预置模型（Qwen/DeepSeek/GLM/Kimi/CosyVoice/VL/Omni 全系列）<br>✅ LoRA 微调模型（OSS 导入，rank∈{8,16,32,64}，VIT 冻结等约束）<br>❌ 全参微调模型 | ✅ TPM 预留：主流预置模型（Qwen/GLM/DeepSeek/Kimi 等）<br>✅ 快速模式：仅 `glm-5.2-fast-preview`（Preview 阶段）<br>❌ 自定义模型（LoRA/FT）不支持 | ✅ 微调完成模型（`ft-xxx` ID）<br>✅ OSS 导入模型（通过 `/import_models` API）<br>❌ 预置模型（不可直接部署，需先微调或导入） |
| **API 端点** | 统一 DashScope 域名：<br>`https://dashscope.aliyuncs.com/api/v1/deployments`（创建）<br>`https://dashscope.aliyuncs.com/api/v1/chat/completions`（调用） | • TPM 预留：复用标准 DashScope 域名，仅 `model` 参数替换为专属 code<br>• 快速模式：专用 MaaS 域名：<br>`https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1` | 独立 MaaS 域名：<br>`https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/deployments`（创建）<br>调用使用返回的 `endpoint`（如 `https://xxx.maaS.aliyuncs.com/v1/chat/completions`） |
| **计费方式** | 三模式可选：<br>• **PTU**：预付费吞吐额度（TPM），含缓存折扣与长输入阶梯系数<br>• **MU**：包月模型单元（MU1/MU2…），支持 PD 分离与限流<br>• **按 [Token](../concepts/token.md)**：后付费，无资源预留 | • **TPM 预留**：预付费锁定吞吐（kTPM），溢出可选自动转按量<br>• **快速模式**：按标准 token 计费，**不享受缓存折扣**，无容量保障 | 按实际 GPU 实例运行时长计费（秒级），实例规格由模型自动匹配；微调作业单独计费（GPU 小时） |
| **资源隔离性** | ✅ 完全独占资源（PTU/MU 模式）<br>✅ 支持扩缩容、状态监控（`PENDING`/`RUNNING`/`DELETING`） | ❌ TPM 预留：逻辑隔离（专属吞吐配额），物理资源共享<br>❌ 快速模式：无资源隔离，共享调度队列 | ✅ 物理实例隔离（每个部署为独立容器）<br>⚠️ 最小实例数固定为 1（无法暂停），自动扩缩容上限受账号配额限制（最多 5 个活跃部署） |
| **典型场景** | • 高并发 SaaS 应用（需稳定低延迟）<br>• 企业级 AI 助手（需长上下文+前缀缓存）<br>• LoRA 微调后生产上线 | • 大促期间流量洪峰保障（TPM 预留）<br>• Agent 多步推理链路（快速模式提升 TPS）<br>• 对 P99 延迟敏感但无需长期独占资源的实验性服务 | • 私有数据微调 → 自动部署闭环（CI/CD 集成）<br>• 多版本模型 A/B 测试（快速创建/销毁部署）<br>• 无控制台权限的 DevOps 自动化流水线 |

## 各方案适用场景建议

### ✅ 优先选择 **Model Deployment** 当：
- 需要**长期稳定、可预期性能**的生产服务（如客服机器人、内容审核系统）；
- 使用**LoRA 微调模型**并要求资源独占与生命周期管理；
- 业务涉及**超长文本处理**（如法律合同分析、代码库理解），需 PTU 的前缀缓存与 1M token 支持；
- 团队具备控制台操作能力，或可通过 API 实现标准化部署（支持 PTU/MU/Lora 三模式灵活切换）。

### ✅ 优先选择 **High-Speed Inference** 当：
- 已有标准 API 调用链路，**仅需临时提升性能**（如大促、发布会期间）；
- 场景对**单次响应速度极度敏感**（如编程助手实时补全），且能接受 Preview 功能的演进风险；
- 需要**细粒度吞吐保障**（如承诺 500 RPM 不抖动），但不愿承担独占资源的固定成本；
- **组合使用**：为关键模型（如 `qwen3.8-max`）申请 TPM 预留，再叠加其 fast-preview 变体，兼顾稳定性与速度。

### ✅ 优先选择 **Model Production** 当：
- 工作流以**模型迭代为核心**（频繁微调 → 验证 → 上线），需 API 驱动的全自动流水线；
- 团队采用**GitOps/CI-CD 实践**，要求部署动作可版本化、可审计、可回滚；
- 无控制台访问权限（如安全合规限制），所有操作必须通过程序化 API 完成；
- 需要**统一管理微调作业与部署实例**（如批量终止失败任务、查询历史模型版本）。

## 技术选型参考指南（面向开发者）

| 选型关注点 | 推荐方案 | 关键依据 |
|------------|----------|----------|
| **是否需要控制台可视化操作？** | Model Deployment > Model Production > High-Speed Inference | Model Deployment 与 Model Production 均提供控制台入口（后者仅限 API 创建，无部署配置界面）；High-Speed Inference 仅支持控制台配置 TPM 预留，快速模式需手动构造域名。 |
| **是否需支持 LoRA 模型上线？** | **仅 Model Deployment** | Model Production 虽支持导入模型，但文档未明确 LoRA 兼容性；High-Speed Inference 明确不支持自定义模型。 |
| **能否接受 Preview 功能？** | High-Speed Inference（快速模式）需谨慎评估 | 快速模式为 Preview，模型 ID、性能、地域支持可能变更；Model Deployment 与 Model Production 均为 GA 级别能力。 |
| **是否要求最小实例数可设为 0（按需启停）？** | **均不支持** | Model Production 最小实例数固定为 1；Model Deployment 所有模式均持续计费；High-Speed Inference 无实例概念。建议搭配业务层开关或负载均衡路由实现逻辑“暂停”。 |
| **API 兼容性优先级** | Model Deployment ≈ High-Speed Inference > Model Production | 前两者完全兼容 OpenAI/DashScope SDK；Model Production 需适配百炼专属 endpoint 与认证方式，迁移成本较高。 |
| **成本优化潜力** | Model Deployment（PTU 缓存折扣） > High-Speed Inference（TPM 溢出可控） > Model Production（纯按量） | PTU 模式通过前缀缓存显著降低长文本 token 消耗；TPM 预留支持溢出策略避免服务中断；Model Production 无任何容量优化机制。 |

> **重要提醒**：  
> - **地域限制**：Model Deployment 的 API 部署仅支持华北2（北京），其他地域需使用控制台；High-Speed Inference 的 TPM 预留支持北京与新加坡；Model Production 全地域可用（以 API 文档为准）。  
> - **权限差异**：Model Deployment 要求模型部署权限（`Workspace xxx does not have deployment privilege`）；Model Production 依赖微调与部署双权限；High-Speed Inference 仅需基础调用权限。  
> - **演进趋势**：Model Production 正逐步集成 Model Deployment 的 MU 模式能力（如限流、Thinking 模式），未来可能收敛为统一 API 层。当前阶段请严格按文档边界设计架构。

## 被对比主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model production](../api/model-production.md)


