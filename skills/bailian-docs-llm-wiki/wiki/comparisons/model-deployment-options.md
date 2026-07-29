# 模型部署方案对比：Model Production、High-Speed Inference 与 Fine-tuning

本文旨在帮助开发者清晰区分百炼平台中三类核心模型服务能力——**Model Production（模型生产）**、**High-Speed Inference（高性能推理）** 与 **Fine-tuning（微调）**，明确其定位、能力边界、技术约束及适用阶段。三者并非互斥替代关系，而是构成「训练 → 优化 → 部署 → 加速」全链路的关键环节：  
- **Fine-tuning** 解决「模型好不好用」——通过业务数据定制模型能力；  
- **Model Production** 解决「模型能不能上线」——将训练成果封装为稳定、可扩缩的生产级服务；  
- **High-Speed Inference** 解决「上线后快不快、稳不稳」——在服务已就绪前提下，保障高并发下的确定性吞吐与低延迟体验。  
正确理解三者差异，是避免资源错配、计费异常与架构返工的技术选型前提。

## 关键维度对比表

| 维度 | Model Production | High-Speed Inference | Fine-tuning |
|------|------------------|------------------------|-------------|
| **核心目标** | 将训练完成/导入的模型发布为可管理、可扩缩的在线推理服务 | 在已有模型服务基础上，提升吞吐量（TPM/TPS）或降低端到端延迟 | 基于自有数据对基座模型进行参数级优化，提升领域适配性与任务表现 |
| **输入格式** | 已训练完成的模型 ID（如 `ft-xxx`）、部署配置（`instance_type`, `deployment_name` 等） | 标准 API 请求（含 `model` 参数），需匹配预留 model code 或快速模式专属域名 | 训练数据集（JSONL / ZIP 包）、超参配置（`learning_rate`, `n_epochs`, `lora_rank` 等）、基础模型标识 |
| **输出格式** | 部署成功后返回 `endpoint_url`，调用该地址返回标准 OpenAI 兼容响应（如 `/v1/chat/completions`） | 同标准 API 响应结构；快速模式额外返回 `delta.reasoning_content` 字段；TPM 预留无结构变化 | 训练完成后生成新模型 ID（如 `ft-qwen3-8b-20240520-abc123`），**不直接提供推理接口**，需经 Model Production 部署后方可调用 |
| **支持模型** | 所有已完成微调（Fine-tuning）或手动导入的模型（ID 以 `ft-` 或 `import-` 开头）；**不支持原生基座模型直连部署** | TPM 预留：千问、GLM、DeepSeek、Kimi 等主流基座模型（含 `glm-5.2`）；<br>快速模式：**仅 `glm-5.2-fast-preview`**（Preview 阶段） | 文本（Qwen3/3.5）、视觉（万相 Wan2.7）、语音（CosyVoice-v3-flash）、视频（Wan2.7-i2v）、强化学习（Qwen3.5-9B）等多模态模型，覆盖 SFT、DPO、CPT、RL 等范式 |
| **API 端点** | `POST /v1/deployments`（创建部署）<br>`GET /v1/deployments/{name}`（查询状态）<br>`DELETE /v1/deployments/{name}`（下线） | TPM 预留：复用标准 API 域名（如 `https://dashscope.aliyuncs.com/...`），仅需替换 `model` 参数为预留 code；<br>快速模式：**必须使用专属域名**（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`） | `POST /api/v1/fine-tunes`（提交任务）<br>`GET /api/v1/fine-tunes/{job_id}`（轮询状态）<br>`POST /api/v1/files`（上传数据） |
| **计费方式** | **按实例规格 + 运行时长计费**（GPU 实例小时单价 × 实际运行秒数），部署期间持续计费；<br>微调作业单独计费（按 MTU 或 GPU 小时） | TPM 预留：**预付费**，按天购买 kTPM 容量（输入/输出独立计价），超量部分自动溢出至按量计费；<br>快速模式：**纯按量计费**，按实际输入/输出 token 计费（缓存命中享折扣） | **按训练资源消耗计费**：<br>- SFT/DPO/CPT：按 GPU 小时或 MTU（Model Training Unit）计费；<br>- RL：**强制使用 MTU 计费**；<br>微调作业超时（72h）自动终止且不计费 |
| **典型场景** | - 微调完成后的模型正式上线<br>- 多版本 A/B 测试（如 `prod-qa-bot-v1` vs `v2`）<br>- 需要自动扩缩容与健康检查的长期服务 | - 高流量客服机器人（需保障 99.9% 请求 < 2s）<br>- AI 编程助手（依赖快速[流式输出](../concepts/streaming-output.md)）<br>- 大促期间临时扩容（TPM 预留防抖） | - 金融合同条款解析（定制法律语义）<br>- 电商商品图风格统一（万相微调）<br>- 企业专属语音播报（CosyVoice 音色克隆）<br>- 数学推理 Agent（RL 强化策略） |

## 各方案适用场景建议

### ✅ 推荐选择 **Fine-tuning** 当：
- 您拥有高质量、领域专属的标注数据（如客服对话、设计稿描述、医学报告）；
- 标准大模型在关键指标（准确率、风格一致性、专业术语召回）上未达业务要求；
- 您需要模型具备**不可迁移的知识或行为偏好**（如公司 SOP、品牌话术、IP 形象）；
- 您能接受 1~24 小时训练周期，并具备后续部署运维能力。

> ⚠️ 注意：Fine-tuning **不是**零样本/少样本推理替代方案。若仅需 [prompt](../guides/prompt.md) 工程优化，请优先使用 `inference` 模块。

### ✅ 推荐选择 **Model Production** 当：
- 您已完成 Fine-tuning 或已获得可部署模型（如第三方导出权重）；
- 您需要一个**生产就绪的服务实体**：具备唯一访问入口、自动扩缩容、健康探针、TLS 加密、权限隔离；
- 您需对多个模型版本进行生命周期管理（上线/下线/回滚）；
- 您希望规避手动维护 GPU 实例、负载均衡、监控告警等基础设施复杂度。

> ⚠️ 注意：Model Production **不提供训练能力**，也不支持 CPU 实例部署（当前仅 GPU 规格有效）。

### ✅ 推荐选择 **High-Speed Inference** 当：
- 您的模型服务**已通过 Model Production 上线并稳定运行**；
- 您面临明确的性能瓶颈：高并发下 TPS 不足、尾部延迟超标（P99 > 3s）、突发流量导致 429 错误频发；
- 您需要**SLA 保障**（TPM 预留）或**极致流式体验**（快速模式）；
- 您愿意为确定性容量或加速能力支付溢价（预付费或更高 token 单价）。

> ⚠️ 注意：High-Speed Inference 是**叠加在已部署服务之上的加速层**，无法独立存在；快速模式当前仅限 `glm-5.2-fast-preview`，不建议用于核心生产系统长期依赖。

## 技术选型参考（面向开发者）

| 您的问题 | 推荐方案 | 关键依据 |
|----------|-----------|-----------|
| “我有一批销售话术数据，想让 Qwen3 更懂我们行业术语” | ✅ Fine-tuning | 需修改模型参数以注入领域知识，属训练范畴 |
| “微调好的模型怎么让前端调用？需要自己搭服务器吗？” | ✅ Model Production | 提供开箱即用的 HTTPS endpoint，免运维部署 |
| “上线后用户一多就卡顿，P95 延迟从 800ms 涨到 4s” | ✅ High-Speed Inference（TPM 预留） | 容量争抢导致排队，需专属资源保障吞吐 |
| “Agent 调用时输出太慢，用户等待感强” | ✅ High-Speed Inference（快速模式） | 针对[流式输出](../concepts/streaming-output.md)速度优化，TPS 提升 1.5~2 倍 |
| “能否用 CPU 部署低成本测试模型？” | ❌ Model Production（不支持）<br>✅ 可考虑 `inference` 模块（非本文对比项） | 当前 Model Production 仅接受 GPU 实例类型 |
| “想同时用 TPM 预留 + 快速模式，是否可行？” | ✅ 支持组合使用 | 在 TPM 预留的 `glm-5.2` 实例上，将 `model` 设为 `glm-5.2-fast-preview` 即可 |
| “微调时发现 `qwen3.5-9b` 不支持 efficient_sft？” | ✅ 以控制台/API 实际选项为准 | 文档存在表述差异，但实操中 `efficient_sft` 是主流推荐方式，兼容性优于全参训练 |

> 💡 **最佳实践路径**：  
> `Fine-tuning` → `Model Production` → `High-Speed Inference`  
> 三者串联构成完整 MLOps 闭环。切勿跳过 Model Production 直接对微调模型做 TPM 预留（因预留对象必须是已部署的 `deployment_name` 或标准模型 ID）；也勿在未微调前过度投入 High-Speed Inference（基座模型能力不足时，加速无法解决根本效果问题）。

## 被对比主题页

- [model production](../api/model-production.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [fine tuning](../guides/fine-tuning.md)


