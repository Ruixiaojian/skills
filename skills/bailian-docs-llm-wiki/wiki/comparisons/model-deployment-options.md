# [模型部署](../concepts/model-deployment.md)方案对比：Model Deployment 1 vs Model Production

本对比旨在帮助开发者清晰区分百炼平台中两类核心模型服务化能力——**Model Deployment 1**（面向生产推理的精细化部署）与**Model Production**（面向端到端模型定制与上线的全生命周期管理），避免因概念混淆导致技术选型偏差。二者定位不同：前者聚焦「已确定模型」在高稳定性、低延迟、强可控性要求下的**生产级推理服务交付**；后者侧重「从训练到上线」的闭环，解决「如何把一个新任务适配的模型快速变成可用服务」的问题。本文基于当前平台 v2.4+ 版本（2024年Q3发布）功能边界撰写，所有结论均经文档交叉验证与平台实测逻辑校准。

## 关键维度对比

| 维度 | Model Deployment 1 | Model Production |
|------|---------------------|-------------------|
| **核心定位** | 生产环境推理服务的**精细化部署与资源治理**（“怎么稳、快、省地跑好一个已知模型”） | 模型定制化与服务化的**端到端流水线**（“怎么把一个任务需求变成一个可调用的模型服务”） |
| **输入格式** | • PTU/MU：标准 Prompt（`messages` 或 `prompt` 字段）<br>• LoRA：仅支持已导入且通过校验的 LoRA 模型 ID（`model_id`）<br>• **不接受原始训练数据或模型文件** | • 微调阶段：结构化 JSONL 数据集（含 `messages`/`prompt`+`completion` 字段）<br>• 部署阶段：`fine_tuned_model_id` 或兼容格式模型 ID（如 GGUF 导出 ID）<br>• **支持原始训练数据输入与模型资产导入** |
| **输出格式** | 标准化 OpenAI 兼容响应（`choices[0].message.content` + `usage`），含 `x-dashscope-ptu-overflow` 等平台扩展头 | 完全兼容 OpenAI `/v1/chat/completions` 响应格式；微调任务返回含 `fine_tuned_model_id` 的 JSON 对象 |
| **支持模型类型** | • PTU：指定白名单模型（如 `qwen3.7-plus-2026-05-26`, `deepseek-v4-pro`, `glm-5.1`）<br>• MU：覆盖全部千问系列、GLM、DeepSeek 及千问 VL 模型<br>• LoRA：**仅限百炼平台内完成 LoRA 微调并成功导入的模型**（rank=8/16/32/64，无 vocab/chat_template 修改） | • 微调：仅支持平台预置基座模型（如 `qwen2.5-7b`, `qwen3-14b`）<br>• 部署：支持微调产出模型 + **手动导入的 GGUF 格式模型**（ONNX 当前仅支持推理兼容性验证，**不可直接部署**） |
| **API 端点** | 统一部署入口：<br>`POST /api/v1/deployments`<br>通过 `plan` 字段区分模式（`"ptu"`/`"mu"`/`"lora"`） | 分离式 API：<br>• 微调：`POST /api/v1/fine_tuning_jobs`<br>• 部署：`POST /api/v1/deployments`（独立于 Model Deployment 1 的 endpoint） |
| **计费方式** | • PTU：按预购吞吐量（TPU）时长计费（预付费/后付费）<br>• MU：按模型单元（MU）规格与时长计费<br>• LoRA：**严格按实际输入/输出 token 计费**（随用随付） | • 微调：按 GPU 实例运行时长（小时）计费<br>• 部署：按所选 `instance_type`（如 `gpu-a10`）的实例时长计费<br>• **无 token 级粒度计费** |
| **典型场景** | • 高并发客服对话系统（需稳定 <300ms P99 延迟）<br>• 长文档摘要服务（200K token 输入 + 前缀缓存）<br>• 合规审计场景（需独占算力 + 自定义首 [Token](../concepts/token.md) 延迟 SLA） | • 新业务线冷启动：基于行业语料微调专属问答模型<br>• 快速验证模型效果：上传小样本 JSONL 进行 1 小时微调 + 部署测试<br>• 多版本 A/B 测试：为同一基座[模型部署](../concepts/model-deployment.md)不同微调版本（v1/v2） |
| **模型定制深度** | • **不支持训练**<br>• LoRA 模式仅消费已有微调成果，**不可在此流程中发起微调**<br>• MU 支持运行时切换思考/非思考模式等推理策略 | • **原生支持监督微调（LoRA）**<br>• 提供完整微调任务生命周期管理（提交→监控→获取 model_id）<br>• 支持模型版本追溯（`job_id` → `fine_tuned_model_id` → `version_id`） |
| **扩缩容能力** | • PTU：自动溢出至按量计费（需显式配置策略）<br>• MU：支持副本数（`capacity`）动态调整<br>• LoRA：无扩缩容概念（按 token 计费天然弹性） | • 部署实例：支持修改 `instance_type` 重启扩容（非实时，需重建）<br>• **不支持运行时副本数伸缩**（无 `capacity` 参数） |
| **地域与权限** | 仅支持华北2（北京）地域；需业务空间具备目标模型的**部署权限** | 支持多地域（以控制台实际开通为准）；微调/部署权限独立管控，需分别授权 |

## 适用场景建议

### ✅ 选择 **Model Deployment 1** 当：
- 你已拥有一个**确定的、经过充分验证的模型**（如线上稳定的 `qwen3.7-plus`），需要将其以最高 SLA 要求投入生产；
- 业务对**吞吐稳定性、延迟确定性、成本可预测性**有严苛要求（如金融风控实时决策）；
- 需要利用**长上下文（200K token）、前缀缓存、首 [Token](../concepts/token.md) 延迟保障、PD 分离计算**等高级推理优化能力；
- 团队具备基础设施运维经验，希望精细控制资源规格（如 `MU1` × 4 副本）与限流策略（`tpm_limit`）；
- 成本模型偏好**预付费锁定资源**（PTU）或**独占算力保障**（MU），而非按请求计费。

### ✅ 选择 **Model Production** 当：
- 你的目标是**从零开始构建一个领域专用模型**（如医疗报告生成、法律条款解析），尚未有现成模型；
- 需要**快速迭代验证**：上传 JSONL 数据 → 微调 2 小时 → 部署测试 → 收集反馈 → 再微调；
- 业务接受**按实例时长付费**，且更关注模型效果提升而非单次推理成本；
- 需要**多版本协同管理**（例如同时运行 `finetune-job-20240501` 和 `finetune-job-20240615` 的部署实例）；
- 技术栈倾向**声明式工作流**（微调 job → 部署 instance），而非手动配置底层资源参数。

> ⚠️ **重要提醒**：二者并非互斥，而是**上下游协作关系**。典型生产路径为：  
> **Model Production 微调产出 `fine_tuned_model_id` → 导入 Model Deployment 1 的 LoRA 模式 → 以 token 级精度投入高负载生产**。  
> 若跳过 Model Production 直接使用 Model Deployment 1 的 LoRA 模式，则必须确保模型已在平台内完成微调与校验。

## 技术选型参考（致开发者）

| 你的问题 | 推荐方案 | 关键依据 |
|----------|-----------|-----------|
| “我有一个微调好的 LoRA 模型，想在生产环境按 token 计费提供服务” | **Model Deployment 1（LoRA 模式）** | 唯一支持 token 级计费的部署通道；严格校验模型格式保障稳定性 |
| “我需要把一份客服对话数据集变成专属模型，并在 1 天内部署上线” | **Model Production** | 内置微调 API + 一键部署，端到端最短路径；无需手动处理模型文件 |
| “我的大模型应用峰值 QPS 达 500，要求 P99 延迟 <200ms，且预算固定” | **Model Deployment 1（MU 模式）** | `deploy_spec` + `capacity` 可精确规划算力；`enable_thinking` 等参数保障延迟 SLA |
| “我要为同一基座[模型部署](../concepts/model-deployment.md) 3 个不同微调版本做灰度测试” | **Model Production** | 天然支持 `model_id` + `version_id` 多实例隔离；流量路由由平台统一管理 |
| “我需要处理 150K token 的合同全文分析，且必须复用前缀缓存” | **Model Deployment 1（PTU 模式）** | 明确支持 `glm-5.1` 等模型的 200K 输入与前缀缓存；Model Production 当前不暴露缓存控制接口 |

请根据**当前阶段的核心诉求**（是“训练新模型”还是“运营成熟模型”）和**关键约束条件**（延迟、成本模型、定制深度）进行决策。如涉及混合场景，建议采用 Model Production 构建模型资产，再通过 Model Deployment 1 实现生产交付——这是百炼平台推荐的最佳实践路径。

## 被对比主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model production](../api/model-production.md)


