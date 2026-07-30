# 模型部署与推理方案对比：高并发推理、模型部署、模型生产

本文旨在帮助开发者清晰区分百炼平台中三类核心模型服务能力——**高并发推理（Model High Speed Inference）**、**模型部署（Model Deployment 1）** 和 **模型生产（Model Production）**，明确其定位、能力边界与技术差异。随着大模型应用从实验走向规模化落地，选型不当易导致性能瓶颈、成本失控或运维复杂度激增。本对比聚焦实际工程落地维度，覆盖接入方式、资源模型、计费逻辑、扩展性及生命周期管理等关键要素，为技术决策提供结构化参考。

---

## 方案核心能力对比表

| 维度 | 高并发推理（TPM 预留 / 快速模式） | 模型部署（Model Deployment 1） | 模型生产（Model Production） |
|------|----------------------------------|--------------------------------|-----------------------------|
| **定位目标** | 保障已有模型服务的**确定性 SLA 与极致吞吐**（低延迟/高 TPS），面向已上线业务的流量护航 | 提供**资源独占、可定制的专属推理服务**，面向需稳定性能、灵活配置与长期运行的生产级模型服务 | 实现**端到端模型生命周期管理**（微调 → 部署 → 版本发布），面向需任务驱动、快速迭代的 AI 应用开发流程 |
| **输入格式** | 标准 OpenAI 兼容请求体（`messages`, `model`, `max_tokens` 等）；快速模式额外支持 `reasoning_content` 字段分离 | 同标准 OpenAI 请求体；MU 模式支持 `enable_thinking`、`max_context_length` 等扩展参数；PTU/Lora 模式参数受限 | 完全兼容 OpenAI `/v1/chat/completions` 协议；部署后调用方式与标准 API 一致 |
| **输出格式** | 标准响应（含 `choices[0].message.content`）；快速模式额外返回 `reasoning_content`（思考过程）与 `content`（最终结果）分离字段 | 标准响应；MU 模式启用 `enable_thinking` 时返回结构化 reasoning 流；所有模式均支持流式响应 | 标准 OpenAI 响应格式；支持流式（`stream: true`）；无专属字段扩展 |
| **支持模型** | • TPM 预留：`qwen3.7-max-2026-05-20`、`glm-5.2`、`deepseek-v4-pro` 等主流预置模型<br>• 快速模式：仅 `glm-5.2-fast-preview`（北京/新加坡地域） | • 预置模型：Qwen3/Qwen2.5/Qwen-VL/Qwen-Omni、DeepSeek v3/v4、GLM 5.x/4.7、Kimi-K2.5、CosyVoice 等<br>• 自定义模型：仅 LoRA 微调模型（严格校验 rank、chat_template、VIT 冻结） | • 微调：仅平台白名单基础模型（如 `qwen2-7b`）<br>• 部署：微调任务 ID（`ft-xxx`）或预置模型 ID；支持通过模型导入接入的自定义模型（需审核） |
| **API 端点** | • TPM 预留：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`（同标准 API，仅 `model` 替换为专属 code）<br>• 快速模式：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`（独立域名） | `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`（专属 endpoint，部署后生成唯一 `service_id`，需在请求头 `X-DashScope-Service-ID` 中传入） | `https://dashscope.aliyuncs.com/api/v1/deployments/{deployment_name}/chat/completions`（部署后分配专属 endpoint URL） |
| **计费方式** | • TPM 预留：按天预付费购买 kTPM（1kTPM = 1000 tokens/min），预留内调用免费；溢出部分按 token 计费；支持缓存折扣（如命中缓存按 25% 折算容量）<br>• 快速模式：纯按量计费（输入/输出 token），`glm-5.2-fast-preview` 缓存单价 4 元/百万 token | • PTU 模式：预付费购买输入/输出 kTPM，超限按量计费；支持长输入阶梯系数与缓存折扣<br>• MU 模式：预付费购买模型单元（MU）规格 + 副本数，按实例时长计费；支持 RPM/TPM 限流<br>• LoRA 模式：按 token 计费（仅限 LoRA 模型），月内不使用自动释放 | • 微调：按训练 token 总量计费（含数据加载、前向/反向计算）<br>• 部署：按部署实例时长计费（`gpu.2xlarge` 等规格），**不按 token 或 TPM 计费**；调用本身免费（但需注意底层资源占用） |
| **典型场景** | • 大促/秒杀期间保障核心对话服务 SLA（TPM 预留）<br>• 实时客服机器人、AI 助手交互链路提速（快速模式） | • 企业知识库问答服务（需长上下文 + 前缀缓存）<br>• 金融风控模型服务（需独占资源 + 低首 [Token](../concepts/token.md) 延迟）<br>• SaaS 厂商多租户模型隔离部署 | • 客服话术优化：基于历史对话微调 Qwen2-7b → 部署为 QA Bot<br>• 行业摘要模型：用领域文档微调 → 灰度发布新版本 → 回滚旧版<br>• 内部工具链集成：CI/CD 触发微调 + 自动部署流水线 |

---

## 适用场景建议（面向开发者的技术选型指南）

| 选型目标 | 推荐方案 | 关键理由 | 注意事项 |
|----------|-----------|-----------|-----------|
| **需要绝对确定性 SLA（如 P99 < 300ms）且流量可预测** | ✅ TPM 预留 | 刚性容量保障，避免排队抖动；支持缓存与长输入优化，适合高价值核心链路 | 需提前规划容量，缩容退订有违约金；专属 model code 不可复用至其他方案 |
| **追求极致响应速度（TPS > 80），但无法预估峰值或不愿预付费** | ✅ 快速模式 | 开箱即用，无需预留；排队式限流避免 429，适合突发流量缓冲 | 仅支持 `glm-5.2-fast-preview`；preview 阶段不承诺长期兼容；域名与标准 API 隔离 |
| **需长期稳定运行、自定义性能参数（如 max_context_length）、或部署 LoRA 微调模型** | ✅ 模型部署（Model Deployment 1） | 资源独占、支持 PD 分离降低首 [Token](../concepts/token.md) 延迟、MU 模式可配 RPM/TPM 限流；LoRA 模型可按 token 计费 | LoRA 导入校验严格（rank/词表/VIT）；PTU 模式不支持自定义参数；API 部署仅限北京地域 |
| **需从零开始构建领域专用模型（微调 + 部署 + 版本管理）** | ✅ 模型生产（Model Production） | 统一 API 管理微调任务与部署实例；支持灰度发布、回滚、自动清理训练数据；天然适配 DevOps 流程 | 微调仅限白名单模型；部署实例按规格计费（非 token）；不支持动态热更新权重（需重建部署） |
| **验证模型效果或小流量试用，无长期稳定性要求** | ⚠️ 优先选用标准 API（非本表任一方案） | 成本最低、接入最快；适用于原型验证、内部测试 | 无容量保障，高峰易限流；不支持长上下文优化、thinking 模式等高级特性 |

> **重要提醒**：  
> - **域名不可混用**：TPM 预留与快速模式使用不同域名（`dashscope.aliyuncs.com` vs `maas.aliyuncs.com`），错误调用将直接失败；  
> - **模型不可混用**：`glm-5.2`（TPM 支持） ≠ `glm-5.2-fast-preview`（快速模式专用），二者为独立模型实例；  
> - **权限需显式授权**：模型部署与模型生产均依赖业务空间（Workspace）对目标模型的部署权限，控制台或 API 调用前请确认授权状态；  
> - **地域限制**：模型部署（API 方式）仅支持华北2（北京）；快速模式当前开放北京/新加坡；模型生产无地域限制（以 dashscope 全局 endpoint 为准）。

--- 

*本文档持续更新，最新能力请以百炼控制台与官方 API 文档为准。*

## 被对比主题页

- [model high speed inference](../guides/model-high-speed-inference.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [model production](../api/model-production.md)


