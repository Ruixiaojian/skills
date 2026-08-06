# 模型部署方式对比：Model Production vs Model Deployment 1

本文旨在帮助开发者清晰区分百炼平台中两种主流模型服务化路径——`Model Production`（模型生产）与 `Model Deployment 1`（预置吞吐型部署），明确其定位差异、能力边界与适用约束。二者并非替代关系，而是面向不同阶段、不同 SLA 要求和不同资源管理范式的互补方案：  
- **Model Production** 是“从训练到上线”的端到端生命周期管理能力，强调**模型定制化、版本演进与业务适配**；  
- **Model Deployment 1**（即 PTU 部署）是“已确定模型的高确定性服务交付”能力，强调**吞吐保障、成本可预测性与长上下文稳定性**。  
正确选型可避免资源浪费、部署失败或服务不可控等问题，尤其在微调后模型规模化上线、SaaS 产品级服务交付等关键场景中至关重要。

---

## 关键维度对比

| 维度 | Model Production | Model Deployment 1（PTU） |
|------|------------------|---------------------------|
| **核心定位** | 模型全生命周期管理：支持微调训练 + 部署发布 + 多版本灰度 | 确定性推理服务交付：基于预购吞吐（TPM）保障高并发、低延迟、可预测SLA |
| **输入格式** | 微调阶段：JSONL 格式监督数据（含 `messages` 或 `prompt`/`completion` 字段）<br>部署后推理：标准 OpenAI 兼容 JSON 请求（`messages` 或 `prompt`） | 推理阶段：标准 OpenAI 兼容 JSON 请求（`messages`），**支持超长输入（最高 256K token）并自动应用阶梯系数折算** |
| **输出格式** | 同标准大模型 API 响应（含 `choices[0].message.content`、`usage` 等），无额外字段 | 标准响应基础上扩展关键计费字段：<br>• `provisioned_tokens`: 折算后实际消耗的 KTPM<br>• `cached_tokens`: 命中的缓存 token 数<br>• `service_tier: "ptu-standard"`<br>• 响应头含 `x-dashscope-ptu-overflow: true/false` |
| **支持模型类型** | • 百炼托管基础模型（如 `qwen2-7b-chat-hf`）<br>• LoRA 微调产出模型（`ft-xxx`）<br>• 通过 [模型导入](../../raw/model-api-reference/model-production/import-models-api.md) 接入的第三方模型（需符合格式规范） | • **仅限平台预置模型**（如 `glm-5.1`、`deepseek-v4-pro`、`qwen3.7-plus-2026-05-26`）<br>• **不支持 LoRA 模型直接部署为 PTU 服务**<br>• 不支持自定义模型或非预置模型代码 |
| **API 端点** | `/v1/fine_tuning_jobs`（微调）<br>`/v1/deployments`（部署）<br>部署成功后返回 `endpoint_url`（形如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/<deployment_id>`） | `/api/v1/deployments`（统一部署入口，通过 `plan="ptu"` 区分）<br>部署成功后返回 `endpoint_url`（同 Model Production 格式，但底层路由与资源池隔离） |
| **计费方式** | • **按实例规格（GPU 类型 + 运行时长）计费**：部署后持续计费，无论是否调用<br>• 微调任务按 GPU 小时计费<br>• 无预购概念，弹性伸缩但成本不可精确预估 | • **预置吞吐（PTU）模式**：按购买的 `input_tpm` / `output_tpm`（单位：KTPM/分钟）固定月费<br>• 支持溢出策略：<br> ✓ `auto_overflow`：超额自动转按量计费（不中断服务）<br> ✗ `ptu_only`：超额直接返回 429（零额外费用）<br>• **不按实例计费，无空闲成本** |
| **典型场景** | • 垂直领域模型定制（如金融问答、医疗摘要微调）<br>• A/B 测试与灰度发布（多版本流量切分）<br>• 快速验证新模型效果并小规模上线<br>• 需频繁迭代模型版本的研发流程 | • SaaS 产品核心推理服务（高并发、稳延迟）<br>• 长文档分析、多轮对话等长上下文稳定需求场景<br>• 成本敏感且流量可预估的商业化服务（如企业知识库 API）<br>• 需前缀缓存降本的关键业务（如重复模板生成） |
| **版本与灰度** | ✅ 原生支持多版本管理（最多 5 个活跃版本）<br>✅ 支持按流量比例灰度发布（`traffic_split` 参数）<br>✅ 版本间完全隔离，可独立扩缩容 | ❌ **不支持多版本灰度**<br>❌ 单次部署仅对应一个模型版本与一套 PTU 配额<br>✅ 可通过创建多个独立部署实现逻辑灰度（但需分别购买配额） |
| **弹性与变更** | • 实例规格 `instance_type` **不可热变更**，升级需重建部署<br>• 并发数 `max_concurrency` 可动态调整（需在实例承载范围内） | • `input_tpm` / `output_tpm` **支持在线扩容/缩容**（秒级生效）<br>• 溢出策略可在部署后修改<br>• 无需重启或重建服务 |
| **长上下文支持** | 受基础模型原生长度限制（如 Qwen 系列默认 32K/128K），无特殊优化机制 | ✅ 原生支持超长输入（`glm-5.1`: 200K, `deepseek-v4-pro`: 256K）<br>✅ 自动应用阶梯系数折算 TPM 消耗<br>✅ 前缀缓存（Context Cache）显著降低重复内容成本（折扣系数低至 0.2） |

---

## 适用场景建议

### ✅ 优先选择 **Model Production** 当：
- 你需要对百炼基础模型进行 **LoRA 微调**，并希望将微调结果快速部署为服务；
- 业务处于探索期，需频繁更新模型（如每周迭代一个新版本），依赖 **灰度发布与版本回滚**；
- 模型来源多样（自有模型、开源模型、第三方模型），需通过 **模型导入** 统一纳管；
- 对成本敏感度中等，更关注研发效率与模型演进速度，能接受按 GPU 实例小时付费的弹性模式；
- 场景对长输入（>64K）无硬性要求，或可通过分块/摘要等工程手段规避。

### ✅ 优先选择 **Model Deployment 1（PTU）** 当：
- 你已确认使用 **平台预置模型**（如 `glm-5.1`），且该模型满足业务功能与性能要求；
- 服务需 **7×24 小时稳定运行**，对 P99 延迟、吞吐抖动有严格要求（如客服机器人、实时报告生成）；
- 日均请求量大且波动小，**可准确预估 RPM 与平均 token 长度**，追求成本可预测性；
- 核心场景涉及 **超长文档解析、多轮复杂对话、模板化批量生成**，需前缀缓存与长输入阶梯优化；
- 已上线模型进入成熟期，**无需频繁变更模型结构或参数**，重点在于服务稳定性与成本优化。

### ⚠️ 明确不适用情形：
- 若你的微调模型（`ft-xxx`）需以 PTU 方式部署 → **不可行**，必须改用 Model Production 或切换为「模型单元」/「按 [Token](../concepts/token.md) 计费」；
- 若需在华北2以外地域使用 PTU → **需确认该地域是否开放 PTU 模型与 endpoint**（当前部分地域仅支持基础部署）；
- 若业务流量峰谷差异极大（如日间 100 RPM、夜间 1 RPM）→ PTU 可能造成配额闲置，建议评估「按 [Token](../concepts/token.md) 计费」或 Model Production 的自动扩缩容能力。

---

## 技术选型参考（面向开发者）

| 决策问题 | Model Production | Model Deployment 1 |
|----------|------------------|----------------------|
| **我需要微调模型吗？** | ✅ 是 → 必选 | ❌ 否 → 不支持 LoRA 直接部署 |
| **我能否接受部署后按 GPU 实例持续计费？** | ✅ 可接受 → 灵活、免预购 | ❌ 必须按实际 token 消耗付费 → 选 PTU 或按 [Token](../concepts/token.md) 计费 |
| **我的服务是否要求 P99 < 500ms 且 99.9% 可用？** | ⚠️ 依赖实例规格与负载，存在排队风险 | ✅ PTU 提供确定性资源保障，更适合严苛 SLA |
| **我的输入经常 > 64K token？** | ⚠️ 可能触发截断或 OOM，需自行处理 | ✅ 原生支持 + 阶梯折算 + 缓存优化 |
| **我需要今天上线 v1、明天灰度 v2、后天回滚 v1？** | ✅ 多版本 + 流量切分开箱即用 | ❌ 需手动创建多个部署，运维成本高 |
| **我是否已有稳定的月度 token 预算，并希望刚性控制？** | ❌ 成本随调用量与实例时长浮动 | ✅ PTU 配额即预算，超额可控（auto_overflow）或零容忍（ptu_only） |

> 💡 **最佳实践提示**：  
> - **微调 → 上线闭环**：推荐采用 `Model Production` 完成微调与初版部署；待模型稳定、流量可测后，若需更高 SLA 与成本确定性，可将最终版本导出为标准模型，再通过 `Model Deployment 1` 以 PTU 方式重新部署。  
> - **混合计费策略**：在 PTU 部署中启用 `auto_overflow`，既能保障基线服务质量，又可应对突发流量，避免服务降级。结合监控 `x-dashscope-ptu-overflow` 响应头，可精准识别溢出场景并优化配额。  
> - **务必验证模型兼容性**：PTU 模型列表以控制台实时展示为准，勿依赖静态文档；Model Production 的 `instance_type` 必须匹配模型显存需求，部署前请查阅 [兼容性列表](../../raw/model-api-reference/model-production/deployments-api.md)。

## 被对比主题页

- [model production](../api/model-production.md)
- [model deployment 1](../guides/model-deployment-1.md)


