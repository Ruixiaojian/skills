# 模型部署方式对比：Model Deployment、Model Production 与 Fine-tuning

为帮助开发者在百炼平台上高效、合规地将大模型投入实际业务，本文系统对比三种核心能力：**Model Deployment（模型部署）**、**Model Production（模型生产）** 与 **Fine-tuning（微调）**。三者并非并列选项，而是构成「定制→发布→服务化」完整链路的关键环节：  
- **Fine-tuning** 聚焦**模型能力定制**（如何让模型更懂你的业务）；  
- **Model Production** 提供**端到端生命周期管理**（训练→验证→版本→部署的自动化流水线）；  
- **Model Deployment** 专注**生产级服务交付**（如何稳定、低成本、低延迟地对外提供推理能力）。  

理解其定位差异、能力边界与协同关系，是技术选型、架构设计与成本优化的前提。

---

## 关键维度对比

| 维度 | Model Deployment（模型部署） | Model Production（模型生产） | Fine-tuning（微调） |
|------|------------------------------|------------------------------|------------------------|
| **本质定位** | **在线推理服务交付层**：将已存在模型（预置/微调/导入）封装为高可用 API 服务 | **模型全生命周期管理层**：覆盖微调训练、版本控制、灰度发布与标准化部署的统一工作流 | **模型能力定制层**：基于自有数据对基座模型进行参数更新，提升领域适配性 |
| **输入格式** | - PTU/MU：模型 ID（如 `qwen3.7-plus-2026-05-26`）<br>- LoRA：LoRA 模型 ID（如 `qwen3-8b-ft-abc123`） | - 微调任务：`base_model` + `training_file_id`（JSONL）<br>- 部署任务：`model_version_id`（来自微调产出） | - 文本：ChatML 格式 JSONL（`{"messages": [...]}`）<br>- 视觉：ZIP 包（含 `data.jsonl` + 图片/视频）<br>- 语音：ZIP 包（WAV 音频 + 元数据） |
| **输出格式** | 统一 OpenAI 兼容 REST API 响应（`choices[0].message.content`），支持流式（`stream: true`） | - 微调产出：`model_version_id`（唯一版本标识）<br>- 部署产出：`endpoint_url` + `deployment_name`（服务标识） | - 训练产物：`finetuned_output`（模型路径/ID）<br>- 支持导出为 SafeTensors 或 Hugging Face 格式（部分场景需人工审核） |
| **支持模型** | - PTU：`glm-5.1`, `deepseek-v4-pro`, `qwen3.7-plus-2026-05-26`（长输入优化）<br>- MU：全量千问/GLM/DeepSeek/千问VL/CosyVoice 系列<br>- LoRA：仅限微调生成的 `*-ft-*` 模型 | - 微调：`qwen2-7b/57b`, `llama3-8b`, `qwen3-*` 等平台预置基座模型（**不支持自定义基座**）<br>- 部署：所有微调产出模型 + 通过 `import_model` 导入的 HF 格式模型 | - 文本：`qwen3-8b`, `qwen3.5-9b`, `qwen3-vl-8b-instruct` 等（SFT/CPT/DPO/RL）<br>- 视觉：`wan2.7-image-pro`, `wan2.7-i2v` 等<br>- 语音：`cosyvoice-v3-flash`（API 专属）<br>- RL：`qwen3.5-9b` 等 MoE/非 MoE 模型 |
| **API 端点** | `POST /api/v1/deployments`（`plan: "ptu"` / `"mu"` / `"lora"`） | - 微调：`POST /fine_tuning/jobs`<br>- 部署：`POST /deployments`（独立于 Model Deployment 的 API） | - 文件上传：`POST /files`（`purpose="fine-tune"`）<br>- 任务创建：`POST /api/v1/fine-tunes`（文本/视觉）或 `AgenticRL.run()`（RL） |
| **计费方式** | - PTU：预付费吞吐额度（KTPM/月），溢出可选自动转按量<br>- MU：按模型单元时长（MU·小时）计费<br>- LoRA：按 [Token](../concepts/token.md) 用量（输入+输出）计费 | - 微调：按训练消耗 [Token](../concepts/token.md) 数计费（文本/视觉）或 MTU 单元（RL）<br>- 部署：继承底层 Model Deployment 计费模式（即部署时需选择 PTU/MU/lora） | - SFT/CPT/DPO：按训练 [Token](../concepts/token.md) 总数 × epoch 数计费<br>- CosyVoice：0.2 元/千 Token（训练）+ MU 时长（部署）<br>- RL：强制使用 MTU 训练单元（预/后付费） |
| **典型场景** | - 高并发客服机器人（PTU）<br>- 私有化金融风控系统（MU，需思考模式+RPM限流）<br>- A/B 测试轻量模型（LoRA 按量调用） | - 快速迭代 FAQ 知识库（微调 → 版本 → 灰度发布）<br>- 多团队共享同一基座模型的不同业务分支（版本隔离）<br>- 自动化 CI/CD 流水线集成模型上线 | - 客服话术风格迁移（SFT）<br>- 行业术语理解增强（CPT）<br>- 图像生成品牌风格定制（SFT-LoRA）<br>- Agent 工具调用能力强化（RL） |

> ⚠️ **关键协同说明**：  
> - Fine-tuning 产出的模型（如 `qwen3-8b-ft-xxx`）**必须通过 Model Deployment 或 Model Production 的部署接口发布为服务**，不可直接调用；  
> - Model Production 的 `/deployments` 接口本质是 Model Deployment 能力的封装，但**不支持 PTU/MU 的精细化配置**（如前缀缓存、`enable_thinking`、`max_context_length`），若需这些能力，应直接使用 Model Deployment API；  
> - `qwen3.7-plus-2026-05-26` 等长上下文模型在 PTU 模式下享受阶梯系数优惠，但在 Model Production 部署流程中**无法启用该优化**，需优先选用 Model Deployment。

---

## 适用场景建议

### ✅ 选择 **Model Deployment** 当：
- 你已有**成熟模型**（平台预置模型、LoRA 微调产物、OSS 导入模型），需立即上线高 SLA 服务；  
- 业务对**延迟、吞吐、资源隔离**有强要求（如实时交易风控、高并发对话引擎）；  
- 需要**精细化性能调控**：启用思考模式、设置最大上下文长度、配置 RPM/TPM 限流、利用前缀缓存降低长输入成本；  
- 运维团队具备 API/命令行操作能力，追求部署灵活性与成本可控性。

### ✅ 选择 **Model Production** 当：
- 你处于**模型迭代期**，需频繁执行「微调 → 验证 → 发布」闭环，且重视**版本追溯与灰度能力**；  
- 团队采用 DevOps 实践，希望将模型上线纳入**标准化 CI/CD 流水线**（如 GitHub Actions 触发微调+部署）；  
- 业务方无需关心底层资源规格，只需关注 `model_version_id` 和 `deployment_name` 等语义化标识；  
- 使用场景**不涉及 PTU 缓存、MU 独占等高级特性**，接受通用 GPU 实例部署。

### ✅ 选择 **Fine-tuning** 当：
- 通用大模型在你的业务场景（如医疗问答、法律文书生成、品牌视觉风格）**效果未达预期**；  
- 你拥有**高质量、领域专属的标注数据**（≥1k 条高质量样本），且能保障数据安全与合规；  
- 需要**深度定制模型行为**：调整输出风格、注入专业知识、优化偏好对齐（DPO）、增强工具调用能力（RL）；  
- 接受训练耗时（数小时至数天）与迭代周期，以换取长期效果收益。

---

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键动作 | 注意事项 |
|----------|----------|----------|----------|
| **“我有个微调好的 LoRA 模型，想快速上线测试”** | Model Deployment（`plan: "lora"`） | 控制台选择模型 → 设 `plan=lora` → 提交 → 获取 `deployed_model` 名称调用 | • 仅支持 LoRA 模型<br>• 不支持扩缩容（需人工审核）<br>• 成本按 Token 实时结算 |
| **“我要部署一个千问 VL [多模态](../concepts/multi-modal.md)模型，要求最低 200ms P99 延迟，且需开启思考模式”** | Model Deployment（`plan: "mu"`） | API 提交 `{"plan":"mu", "deploy_spec":"MU2", "enable_thinking":true, "max_context_length":131072}` | • MU 是唯一支持 `enable_thinking` 的模式<br>• `max_context_length` 需模型本身支持<br>• 地域限制：仅华北2（北京） |
| **“我们每周更新一次客服知识库，需要自动微调+灰度发布”** | Model Production | 1. 上传新数据 → 2. `POST /fine_tuning/jobs` → 3. 监听 `succeeded` → 4. `POST /deployments`（指定新 `model_version_id`）→ 5. 切流量 | • 微调与部署使用不同 API 域名<br>• 部署后 `endpoint_url` 可直接用于业务调用<br>• 灰度需配合网关路由实现 |
| **“我想用公司财报 PDF 微调一个金融分析模型”** | Fine-tuning（SFT） | 1. 提取 PDF → 构建 ChatML JSONL（含 `system` + `user` + `assistant`）→ 2. ZIP 打包 → 3. 上传 → 4. 创建 `efficient_sft` 任务 | • 推荐 `lora_rank=16`, `n_epochs=3`<br>• 避免在 `messages` 中插入原始 PDF 内容（token 超限）<br>• 训练后务必在小样本上验证逻辑一致性 |
| **“我的应用需要 10K QPS，且输入平均 8K token，预算敏感”** | Model Deployment（PTU） | 1. 计算所需 `input_tpm`（例：10K QPS × 8K token × 60 ≈ 4.8M TPM → 选 5000 KTPM）→ 2. 开启「自动溢出」→ 3. 启用前缀缓存 | • PTU 是长输入场景唯一经济方案<br>• 必须显式配置 `ptu_capacity.input_tpm`<br>• 溢出策略影响服务稳定性，需监控 `x-dashscope-ptu-overflow` 响应头 |

> 💡 **终极建议**：  
> - **先微调，再部署**：Fine-tuning 是价值起点，Model Deployment 是效能终点；  
> - **生产环境首选 Model Deployment**：它提供最细粒度的性能、成本与稳定性控制；  
> - **避免混用 Model Production 部署 + PTU/MU 配置**：二者 API 能力不重叠，强行组合将丢失关键特性；  
> - **始终以控制台实时可选列表为准**：文档列举的模型 ID 可能滞后，创建前务必验证兼容性。

## 被对比主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model production](../api/model-production.md)
- [fine tuning](../guides/fine-tuning.md)


