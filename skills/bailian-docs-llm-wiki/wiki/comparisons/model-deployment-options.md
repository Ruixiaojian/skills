# 模型部署方式对比：Model Production vs Model Deployment 1

本文旨在帮助开发者清晰区分百炼平台中两种核心模型服务化路径——**Model Production**（模型生产）与**Model Deployment 1**（模型部署 1），避免因概念混淆导致选型偏差、计费异常或功能不可用。二者虽均以“部署”为最终目标，但在设计定位、能力边界、适用阶段及运维模型上存在本质差异：  
- **Model Production** 是面向**已托管基础模型的生产级治理能力**，聚焦微调后模型的**高可用、可计量、SLA 可保障**服务发布，强调容量预留、弹性扩缩与全生命周期治理；  
- **Model Deployment 1** 是面向**通用推理服务交付的轻量级部署通道**，支持预置模型、LoRA 微调模型及部分 SFT 模型的**快速实例化与资源独占式服务化**，强调易用性、多计费模式适配与控制台/API 一体化操作。  

下表从关键技术维度进行系统性对比，供开发者在架构设计与技术选型阶段参考。

| 维度 | Model Production | Model Deployment 1 |
|------|------------------|----------------------|
| **核心定位** | 模型全生命周期生产治理能力（微调 → 部署 → TPM 预留 → 扩缩容 → 续订） | 快速创建独立、资源专享的推理服务实例（支持预置/LoRA/SFT 模型） |
| **输入格式** | 仅支持百炼平台**托管的基础模型名**（如 `qwen-max`），不接受自定义模型文件或 OSS 路径；微调需通过 Fine-tuning Job 生成专属模型 ID 后再部署 | 支持：<br>• 预置模型名（如 `qwen3.8-max`）<br>• LoRA 模型（OSS 导入，需满足 rank/冻结/VIT 约束）<br>• 白名单 SFT 模型（如 `qwen3.5-27b`） |
| **输出格式** | 返回标准化 `deployed_model` ID（如 `qwen-max-ptu-a1b2c3d4`），由平台自动生成，**不可自定义后缀**；服务 endpoint 与基础模型 API 兼容（OpenAI/DashScope 格式） | 返回用户指定或平台生成的 `deployed_model` ID（如 `my_qwen_flash`），**支持自定义 `suffix`**（控制台可见，API 创建时可传）；endpoint 行为一致，但模型参数解析逻辑更灵活 |
| **支持模型类型** | 仅限百炼**官方托管且明确列入 TPM 预留清单的模型**（如 `qwen-max`, `glm-5.2`, `deepseek-v4-pro`, `kimi-k2.6` 等共 9 款），**不支持 LoRA 或自定义模型导入** | 支持范围更广：<br>• 全系列预置模型（Qwen/DeepSeek/GLM/QwenVL/QwenOmni/CosyVoice）<br>• 符合约束的 LoRA 模型（rank=8/16/32/64，VIT 冻结）<br>• 白名单 SFT 模型（[Token](../concepts/token.md) 用量计费） |
| **部署类型与计费模式** | 仅支持 **TPM 预留（`plan=ptu`）**，分 `pre_paid`（预付费）与 `post_paid`（后付费）；必须配置 `ptu_capacity`（含 `input_tpm`/`output_tpm`/`thinking_output_tpm`） | 支持三类独立计费模式：<br>• `ptu`：预置吞吐（类似 Model Production，但无 TPM 预留治理能力）<br>• `mu`：模型单元（按副本数 `capacity` + 规格 `MU1/MU2` 计费，资源严格隔离）<br>• `lora`：[Token](../concepts/token.md) 用量（按实际 token 消耗计费，仅限白名单模型） |
| **API 端点与调用方式** | 使用统一 `/api/v1/deployments` 接口；Endpoint 支持 DashScope 原生域名与 Workspace 专属域名；**必须指定 `service_tier=ptu_default`（TPM 预留）或 `ptu_fast`（通用部署）** | 同样使用 `/api/v1/deployments` 接口；Endpoint 与 Model Production 完全兼容；**通过 `plan` 字段区分计费类型（`ptu`/`mu`/`lora`）**，无需 `service_tier` 参数 |
| **扩缩容能力** | ✅ **支持动态扩缩容**（`PUT /scale`），`input_tpm`/`output_tpm`/`thinking_output_tpm` 必须同向调整；预付费扩缩容为异步状态机 | ❌ **不支持 API 动态扩缩容**：<br>• `ptu` 模式：仅能通过控制台重新部署变更容量<br>• `mu` 模式：`capacity`（副本数）为创建期静态参数，调整需人工审核，API 不开放修改接口 |
| **续订与生命周期管理** | ✅ 支持 `renew` 接口实现预付费自动续订；支持 `updateOverflowStrategy` 灵活配置溢出策略（启用/禁用） | ❌ **不支持续订接口**；预付费服务到期即停服，需手动重建；溢出策略仅在创建时配置，不可运行时修改 |
| **典型场景** | • SLA 敏感的核心业务（如客服对话引擎、金融风控推理）<br>• 需长期稳定 TPM 吞吐保障的 B2B 服务<br>• 微调后模型需纳入统一容量治理与成本分摊体系 | • 快速验证新模型效果（A/B 测试、POC）<br>• 中小规模业务线独立部署（如内部知识库问答）<br>• LoRA 微调成果需即时上线，且对首 [Token](../concepts/token.md) 延迟敏感（PD 分离计算） |

## 适用场景建议（面向开发者的技术选型指南）

| 你的需求 | 推荐方案 | 关键原因 |
|----------|-----------|-----------|
| **需要为微调后的模型提供 SLA 保障（如 ≥99.9% 可用性、≤500ms P95 延迟），并纳入企业级容量预算与成本审计体系** | ✅ Model Production | 唯一支持 TPM 预留、自动续订、溢出策略治理、跨周期扩缩容的生产级能力；所有操作符合 ITIL 运维规范。 |
| **你已有一个 LoRA 微调模型（OSS 存储），希望 5 分钟内完成部署并开始调用，且不关心长期容量规划** | ✅ Model Deployment 1（`plan=lora` 或 `plan=ptu`） | 直接支持 LoRA 导入与一键部署；`lora` 计费模式免容量预估，按实际 token 消耗付费；控制台流程极简。 |
| **你需要部署一个千问 VL 多模态模型，并要求首 Token 延迟 ≤300ms，同时限制每分钟最多 100 次请求** | ✅ Model Deployment 1（`plan=mu`） | `mu` 模式支持 PD 分离计算（优化首 Token）、`rpm_limit` 服务级限流、`max_context_length` 自定义上下文长度；Model Production 当前**不支持多模态模型部署**。 |
| **你正在构建一个高并发搜索推荐服务，需保证每分钟至少 50K output tokens 的稳定吞吐，且能随流量峰谷自动伸缩** | ✅ Model Production（`service_tier=ptu_default` + `post_paid`） | TPM 预留提供硬性吞吐下限保障；`post_paid` 支持按小时粒度扩缩容，完美匹配流量波动；`ptu_fast`（通用部署）虽弹性更强但无吞吐保障，不满足 SLA 要求。 |
| **你只是想临时测试 `qwen3.7-flash` 模型的效果，预计只用 2 小时，不想预付费用或配置复杂参数** | ✅ Model Deployment 1（`plan=ptu` + `post_paid`，最小容量） | 最小 `ptu_capacity`（1000 input/output TPM）即可启动；创建即用，删除即停计费；Model Production 强制要求 `ptu_capacity` 且无“最小规格”概念，门槛更高。 |

> **重要提醒**：  
> - **不要混用参数**：`service_tier`（Model Production）与 `plan`（Model Deployment 1）是互斥的部署标识符，同一请求中同时传入将导致 `InvalidParameter` 错误。  
> - **地域一致性**：两者当前均**仅支持华北2（北京）地域**；新加坡/东京/法兰克福区域仅 Model Production 支持 TPM 预留，Model Deployment 1 的 API 尚未开放。  
> - **计费刚性原则**：Model Deployment 1 创建后**不可变更 `plan` 类型**（如不能从 `ptu` 切换到 `mu`），Model Production 的 `plan` 固定为 `ptu`，无切换概念。若需变更，必须删除旧服务并新建。  
> - **模型时效性**：文档中出现的带未来日期模型（如 `qwen3.7-flash-2026-07-15`）**未在控制台开放部署入口，也不在 API 实际支持列表中**，请以控制台实时可选模型为准。  

选择即承诺。请根据你的**模型来源、SLA 要求、运维成熟度、成本模型偏好**综合决策——Model Production 是生产环境的“稳压器”，Model Deployment 1 是创新落地的“加速器”。

## 被对比主题页

- [model production](../api/model-production.md)
- [model deployment 1](../guides/model-deployment-1.md)


