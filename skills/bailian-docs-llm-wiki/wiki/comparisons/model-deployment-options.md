# 模型部署方案对比：高并发推理、生产部署与压缩优化

为帮助开发者在不同业务阶段（如流量洪峰应对、长期服务上线、成本敏感型部署）科学选型，本文系统对比百炼平台三大核心模型部署能力：**高并发推理（TPM 预留 & 快速模式）**、**生产级模型部署（[model production](../api/model-production.md)）** 和 **模型压缩（[model compression](../guides/model-compression.md)）**。三者定位互补——高并发推理聚焦 *运行时性能保障*，生产部署解决 *定制化模型落地闭环*，压缩优化则面向 *推理成本与资源效率平衡*。理解其差异是构建稳定、高效、可演进 AI 服务的关键前提。

## 关键维度对比

| 维度 | 高并发推理（TPM 预留 + 快速模式） | 生产部署（[model production](../api/model-production.md)） | 压缩优化（[model compression](../guides/model-compression.md)） |
|------|----------------------------------|------------------------------|------------------------------|
| **核心目标** | 保障高吞吐稳定性（TPM 预留）或极致首 token/流式延迟（快速模式） | 实现私有化微调模型的端到端上线与服务化 | 降低已训练模型的推理资源消耗与部署成本 |
| **输入格式** | 标准 OpenAI 兼容请求体（`messages`, `stream`, `temperature` 等）；快速模式需额外适配 `reasoning_content` 字段解析 | 微调：JSONL 训练数据集 URL；部署：`model_id` / `fine_tuned_model_id` + 实例规格等配置参数 | 微调成功且状态为 `SUCCEEDED` 的自定义模型 ID；可选校准数据集（最多 5 个已发布数据集） |
| **输出格式** | 标准 OpenAI 流式/非流式响应；快速模式返回含 `delta.reasoning_content` 和 `delta.content` 的双通道结构 | 微调任务输出 `fine_tuned_model_id`；部署后返回 `endpoint_url`（兼容 `/v1/chat/completions`） | 生成新模型 ID（源模型名 + 后缀），如 `my-qwen-ft-w8a8`，存于模型中心，可直接用于部署 |
| **支持模型** | **TPM 预留**：Qwen、GLM、DeepSeek、Kimi 等十余个主流基础模型（如 `qwen3.7-max-2026-05-20`, `deepseek-v4-pro`）；<br>**快速模式**：仅 `glm-5.2-fast-preview`（Preview 阶段，严格限定） | 支持基于 Qwen 系列等基础模型的全参微调（`full`）与 LoRA 微调（`lora`）；部署对象为微调产出模型或 `import_model` 导入的第三方模型 | **仅限百炼平台内微调产出的自定义模型**（如 `qwen3.5-flash-2026-02-23-finetuned-xxx`）；不支持基础模型、OSS 模型、第三方模型 |
| **API 端点** | **TPM 预留**：复用标准 MaaS 域名（如 `https://{workspace_id}.maas.aliyuncs.com/v1`），但 `model` 参数需替换为专属 TPM code（如 `tpm-qwen37max-xxx`）；<br>**快速模式**：必须使用专属地域域名（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），`model="glm-5.2-fast-preview"` | 微调：`POST /api/v1/fine_tuning_jobs`；部署：`POST /api/v1/deployments`；服务调用：`POST {endpoint_url}/v1/chat/completions` | 控制台操作为主（路径：模型 > 模型训练 > 模型压缩）；无公开 REST API，任务通过控制台提交与管理 |
| **计费方式** | **TPM 预留**：按预留容量（kTPM）预付费，超额部分自动降级为按量计费；缩容按 1.5 倍系数结算；<br>**快速模式**：Preview 阶段暂未明确独立计费规则，实际按底层资源消耗计费（建议监控） | 微调：按 GPU 小时计费；部署：按所选实例规格（如 `ecs.gn7i-c16g1.4xlarge`）的 MU 小时计费；版本管理不额外收费 | 压缩任务本身限时免费；压缩后模型的部署费用按 MU 规格单独计费（因规格降低而节省成本） |
| **典型场景** | - 大促期间客服机器人流量峰值保障（TPM 预留）<br>- 编程助手要求 <200ms 首 token 延迟（快速模式）<br>- Agent 多步推理中对 token 流速敏感的链路 | - 金融领域定制化报告生成模型上线<br>- 电商客服知识库问答模型迭代与灰度发布<br>- 将开源模型微调后封装为内部 SaaS 服务 | - 已验证效果的微调模型需降低 30%+ 推理成本<br>- 边缘侧或轻量级容器环境部署受限于显存/内存<br>- 快速验证不同量化精度（W4A4/W8A8）对业务指标的影响 |

## 适用场景建议

- **选择高并发推理（TPM 预留）当**：  
  你的模型已在生产环境稳定运行，但面临周期性流量高峰（如每日晚 8 点用户咨询激增），且 SLA 要求“99.9% 请求在 1s 内完成”，无法容忍公共资源池的随机限流。此时，TPM 预留是保障容量确定性的最优解，尤其适用于成熟业务线的稳态扩容。

- **选择快速模式（Fast mode）当**：  
  你的应用对交互实时性极度敏感（如 IDE 内嵌代码补全、语音转文字后的即时意图分析），且能接受 Preview 阶段的技术不确定性。注意：仅 `glm-5.2-fast-preview` 可用，客户端需改造解析逻辑，**严禁用于支付、风控等强 SLA 场景**。

- **选择生产部署（[model production](../api/model-production.md)）当**：  
  你需要将自有业务数据训练出的专属模型（如医疗问诊微调模型）长期、可靠、可回滚地上线。它提供完整的生命周期管理（训练→部署→版本→监控），是构建企业级 AI 应用的基石能力，适合从 PoC 迈向规模化落地的团队。

- **选择压缩优化（[model compression](../guides/model-compression.md)）当**：  
  你的微调模型已通过业务验证，但部署成本过高（如需 2×A10 GPU），或目标环境资源受限（如单卡 24GB 显存）。通过 PTQ 量化可显著降低 MU 规格（如从 `gn7i-c16g1.4xlarge` 降至 `gn7i-c8g1.2xlarge`），在精度损失可控前提下实现成本优化，**必须在部署前执行，且不可逆**。

## 技术选型参考（面向开发者）

| 你的关键诉求 | 推荐方案 | 关键动作提醒 |
|--------------|----------|--------------|
| “我的模型流量忽高忽低，怕高峰期被限流崩掉” | ✅ TPM 预留 | 计算真实 kTPM 需求（考虑长文本阶梯系数），使用专属 model code，监控“超额降级统计”避免隐性成本 |
| “用户抱怨补全太慢，首 token 要 1.2 秒，体验差” | ⚠️ 快速模式（仅限 GLM-5.2） | 确认业务能接受 Preview 风险；切换域名；解析 `reasoning_content`；压测排队延迟容忍度 |
| “我要用自己标注的 5000 条合同数据训练一个法律问答模型并上线” | ✅ 生产部署 | 优先选用 LoRA 微调（成本低、速度快）；规划 `endpoint_name`；部署后立即做 A/B 测试验证效果 |
| “这个微调好的模型效果不错，但部署要两台 A10，太贵了，能压小点吗？” | ✅ 压缩优化 | 在华北2地域操作；选 W8A8 模板作为起点；用历史测试集校准；部署后对比 accuracy & latency |
| “我想把 HuggingFace 上下载的 Llama3-8B-GGUF 模型直接部署” | ❌ 三者均不支持 | 百炼当前不支持直接导入 GGUF/AWQ 等外部量化格式；需先转换为百炼兼容格式或通过 `import_model` 流程验证 |
| “我需要同时跑 10 个不同版本的客服模型做灰度” | ✅ 生产部署（+ 版本管理） | 提工单申请提升部署实例配额（默认 5 个）；利用 `version_id` 精确路由流量 |
| “模型压缩后还能不能继续微调？” | ❌ 不可以 | 压缩不可逆！务必保留原始 `SUCCEEDED` 微调模型，所有后续迭代均从此开始 |

> **重要提醒**：三类能力并非互斥，而是可组合使用——例如：对生产部署的 `qwen3.5-flash-finetuned-xxx` 模型执行压缩得到 `qwen3.5-flash-finetuned-xxx-w8a8`，再为其预留 TPM 并启用快速模式（若该模型未来支持）。但请注意：**快速模式当前仅对 `glm-5.2-fast-preview` 开放，不支持其他模型（含压缩后模型）**。技术演进请持续关注官方文档更新。

## 被对比主题页

- [model high speed inference](../guides/model-high-speed-inference.md)
- [model production](../api/model-production.md)
- [model compression](../guides/model-compression.md)


