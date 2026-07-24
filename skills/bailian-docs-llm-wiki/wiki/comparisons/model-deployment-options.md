# 模型部署方式对比：Model Production、Model Deployment 1 与 High-Speed Inference

## 对比目的与背景

在百炼平台中，开发者面临多样化的模型服务化需求：从定制化训练后的端到端交付，到轻量级 LoRA 模型的快速上线；从稳定可预期的高吞吐保障，到极致低延迟的单请求响应优化。`Model Production`、`Model Deployment 1` 和 `High-Speed Inference` 是平台提供的三类核心部署能力，但其定位、技术路径、适用边界与运维范式存在本质差异。

本对比旨在为开发者提供清晰、客观、可落地的技术选型参考，避免因能力混淆导致架构误用（如用 Model Production 部署 LoRA、在 High-Speed Inference 中尝试微调）、计费偏差或 SLA 不达标。所有分析均基于当前（2024年Q2）正式可用功能，不包含灰度或 preview 中未开放能力。

---

## 关键维度对比表

| 维度 | Model Production | Model Deployment 1 | High-Speed Inference |
|------|------------------|----------------------|------------------------|
| **核心定位** | 全生命周期模型交付：支持**微调训练 + 在线部署一体化**，强调版本一致性与可追溯性 | **LoRA 模型专属部署通道**：聚焦已训练 LoRA 的高效、弹性、可观测上线，深度集成 OSS 导入与监控指标 | **推理性能增强机制**：非独立部署形态，而是对**已有标准 API 或预留服务的加速能力叠加**（TPM 预留 / 快速模式） |
| **输入格式** | - 微调阶段：JSONL 格式标注数据集（含 `messages` 或 `prompt`/`completion` 字段）<br>- 部署阶段：兼容 OpenAI `chat/completions` 格式（`model`, `messages`, `temperature` 等） | - 模型导入：OSS 子目录下 `adapter_model.safetensors` + `adapter_config.json`（LoRA 权重）<br>- 推理调用：OpenAI / Anthropic / DashScope 多协议兼容格式（含 `cached_tokens` 等扩展字段） | - TPM 预留：同标准 API 格式，仅需替换 `model` 参数为专属 code<br>- 快速模式：专用域名 + `glm-5.2-fast-preview` 模型 ID + 流式响应结构（含 `reasoning_content`） |
| **输出格式** | 标准 OpenAI `chat/completions` 响应（含 `id`, `choices[0].message.content`, `usage`） | 多协议兼容响应，额外返回 `usage.prompt_tokens_details.cached_tokens`、`usage.provisioned_tokens` 等精细化监控字段 | - TPM 预留：同标准 API 格式，`usage` 中体现预留额度消耗<br>- 快速模式：扩展字段 `reasoning_content`（思考过程流式推送）、`content`（最终答案），`usage` 含缓存详情 |
| **支持模型类型** | - 基础模型：Qwen 系列（如 `qwen2-7b-chat`）等百炼托管模型<br>- 部署模型：微调后模型 或 符合 ONNX / 百炼自定义格式的导入模型 | **仅限 LoRA 微调模型**，且须满足：<br>- rank ∈ {8,16,32,64}<br>- 基础模型限于 Qwen3/Qwen2.5 系列（含 VL）、GLM 等指定型号<br>- vocab/chat_template 未修改，VL 模型 VIT 冻结 | - TPM 预留：支持千问、GLM、DeepSeek、Kimi 等主流模型（北京/新加坡地域）<br>- 快速模式：**仅 `glm-5.2-fast-preview`（preview 阶段）** |
| **API 端点** | `POST /api/v1/fine_tuning_jobs`（训练）<br>`POST /api/v1/deployments`（部署）<br>推理调用：`POST {endpoint_url}/v1/chat/completions`（平台分配域名） | `POST /api/v1/deployments`（统一部署入口）<br>推理调用：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`（标准域名） | - TPM 预留：**同标准 API 域名**，仅 `model` 参数替换为预留 code（如 `qwen37max-20260520-tpm-abc123`）<br>- 快速模式：**专用接入域名** `https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1` |
| **计费方式** | - 微调训练：按 GPU 小时计费（实例规格 × 运行时长）<br>- 在线部署：按**实例运行时长 + 实际 token 消耗**（输入/输出分开计费） | - PTU 模式：按天预付 kTPM（输入/输出额度），超限可溢出至按量<br>- MU 模式：按**模型单元（MU）副本数 × 运行时长** + token 消耗（LoRA 必须使用 MU） | - TPM 预留：按天预付 kTPM（输入/输出分开计价），**刚性配额**<br>- 快速模式：**按实际 token 计费**（单价同标准 API），无预付，排队不额外计费 |
| **典型场景** | - 需要 SFT 定制指令遵循能力（如客服话术适配）<br>- 要求训练与部署版本强绑定、审计可追溯<br>- 交付私有化模型服务（如金融合规问答模型） | - 已有 LoRA 权重需快速上线 A/B 测试<br>- 长上下文（最高 256K）+ 前缀缓存高频命中场景（如文档摘要、法律条文检索）<br>- 需实时监控 `cached_tokens` 优化成本 | - 业务高峰期需**确定性吞吐保障**（如大促期间智能导购并发激增）<br>- Agent 多步推理链路中，**单次响应 TPS 敏感**（如编程助手代码生成）<br>- 对缓存折扣、阶梯容量系数有精细化成本管控需求 |

---

## 适用场景建议（面向开发者的技术选型指南）

| 你的需求 | 推荐方案 | 关键原因与避坑提示 |
|----------|-----------|----------------------|
| **需要从零开始训练一个领域专用模型（如医疗报告生成），并确保训练产出与线上服务版本完全一致** | ✅ Model Production | ✔️ 唯一支持“训练任务 ID → 部署引用”的闭环机制<br>⚠️ 注意：不支持 RLHF 和跨架构迁移；微调产出 90 天过期，需规划再训练周期 |
| **已有 LoRA 权重文件（rank=16），希望 10 分钟内上线测试，且需监控缓存命中率以优化成本** | ✅ Model Deployment 1（MU 模式） | ✔️ 专为 LoRA 设计，OSS 导入 + MU 部署最快 5 分钟就绪；`cached_tokens` 字段直出<br>⚠️ 切勿用 Model Production 部署 LoRA——不支持；`plan: "lora"` 已废弃，必须用 `plan: "mu"` |
| **业务流量波动大，要求高峰时段绝不返回 429，且能接受按天预付固定额度** | ✅ High-Speed Inference（TPM 预留） | ✔️ 提供刚性 kTPM 配额，SLA 可承诺；支持自动溢出降低风险<br>⚠️ 缩容/退订有违约金；专属 model code 退订即失效，需提前切换流量 |
| **正在开发 AI 编程助手，用户对单次代码生成延迟极其敏感（<800ms），且模型已确定为 GLM-5.2** | ✅ High-Speed Inference（快速模式） | ✔️ TPS 提升 1.5~2 倍，流式返回 `reasoning_content` 提升体验<br>⚠️ **仅 preview 模型**，不建议长期生产依赖；需改用专用域名，不可与 TPM 混用 |
| **需部署全参微调模型（非 LoRA），且要求自定义域名（如 api.yourcompany.com）** | ⚠️ Model Production（当前不支持）→ **暂无解** | ❌ Model Production 不支持自定义域名（Q3 上线）<br>❌ Model Deployment 1 仅支持 LoRA<br>✅ 可考虑反向代理 + 平台域名，或等待 Q3 功能发布 |
| **小规模 PoC 验证，无训练需求，仅需调用现成 Qwen3 模型并保障基础性能** | ✅ 直接使用标准 DashScope API（无需三者） | ✔️ 三者均为增强能力，非基础调用必需<br>⚠️ 若后续需提速/保量，再按需叠加 High-Speed Inference |

---

## 总结：一句话选型口诀

- **要训练 + 要版本锁死 → 选 `Model Production`**  
- **有 LoRA + 要快上线 + 要看缓存 → 选 `Model Deployment 1`**  
- **要稳吞吐（TPM）或要快响应（Fast）→ 选 `High-Speed Inference`**  
- **三者互斥，不可嵌套**：Model Production 部署的服务 *不能* 再叠加 TPM 预留；Model Deployment 1 的 MU 实例 *不等价于* TPM 预留实例；快速模式 *仅作用于特定 preview 模型*。

> 注：本文档所涉参数、限制与行为均基于百炼平台 2024 年 6 月最新正式版。功能迭代可能引入变更，请以控制台实时提示及 API 文档为准。

## 被对比主题页

- [model production](../api/model-production.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


