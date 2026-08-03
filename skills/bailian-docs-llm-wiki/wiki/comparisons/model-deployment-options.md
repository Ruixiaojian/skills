# 模型部署方案对比：Model Production vs Model Deployment 1

本文旨在帮助开发者清晰区分百炼平台中两类关键模型服务化路径：**Model Production**（模型生产）与 **Model Deployment 1**（即以预置吞吐 PTU 为核心的模型部署方案）。二者虽均面向“将模型投入线上服务”，但定位、能力边界、适用阶段和运维范式存在本质差异。正确理解其差异，是避免部署失败、计费异常或资源浪费的前提，尤其在涉及自定义微调模型、长文本处理、成本敏感型业务等场景时尤为关键。

---

## 关键维度对比

| 维度 | Model Production | Model Deployment 1（PTU） |
|------|------------------|---------------------------|
| **核心定位** | **端到端模型工业化流程**：覆盖微调 → Checkpoint 提取 → 发布 → 部署 → 运维全生命周期，强调“从训练成果到可服务实例”的转化闭环 | **确定性算力保障型部署模式**：专为高并发、低延迟、流量可预估的生产环境设计，聚焦“已发布模型”的稳定、高效、可计量推理服务交付 |
| **输入格式** | 支持多模态输入（文本、图像、视频、语音），具体取决于所选微调模型类型（如 `wan2.5-i2v-preview` 接收图像+文本提示）；API 请求体结构由模型 schema 决定 | 仅支持**文本输入**（含长上下文）；严格遵循 OpenAI 兼容或 DashScope 标准格式（`messages` / `prompt` + `max_tokens` 等）；不支持图像/视频/语音原始数据直接传入 |
| **输出格式** | 多模态输出：文本生成、图像 URL、视频直链（含 `video_path`）、语音 WAV 下载地址等，由模型能力决定；响应结构高度异构 | **纯文本输出**（含流式响应）；返回标准 `choices[].message.content` 或 `output.text`；视频/图像类模型**不可通过 PTU 部署**，故无对应输出字段 |
| **支持模型来源** | ✅ 用户自定义微调模型（Custom Models）：<br>• 文本：`qwen3-14b`（SFT）、`qwen-plus-...`<br>• 图像：`wan2.7-image-pro`<br>• 视频：`wan2.5-i2v-preview`<br>• 语音：`cosyvoice-v3-flash`<br>❌ 不支持平台预置基础模型（需用其他部署方式） | ✅ 平台预置模型（Base Models）：<br>• `glm-5.1`、`deepseek-v4-pro`、`qwen3.7-plus-2026-05-26` 等<br>❌ **明确不支持任何 LoRA 或微调后模型**（包括通过 Model Production 发布的 custom model）；LoRA 模型仅支持 MU/CU 部署 |
| **API 端点与调用范式** | 分阶段多端点：<br>• `/api/v1/fine-tunes/{job_id}`（任务管理）<br>• `/api/v1/fine-tunes/{job_id}/checkpoints`（Checkpoint 列举）<br>• `/api/v1/deployments/models?model_source=custom`（查可部署模型）<br>• `/api/v1/deployments`（创建部署，`plan` 可选 `"mu"`/`"cu"`/`"lora"`/`"ptu"`） | 单一核心端点：<br>• `POST /api/v1/deployments`（仅当 `plan="ptu"` 时触发 PTU 部署）<br>• 必须携带 `ptu_capacity: {input_tpm, output_tpm}` 对象<br>• 部署成功后，推理调用仍使用统一 `/v1/services/{deployed_model}/chat/completions` 端点 |
| **计费方式** | 按**资源单元（MU/CU）或 LoRA 实例数**计费：<br>• MU：按 `capacity`（单位：base_capacity 的整数倍）× 时长计费<br>• CU：按 GPU 卡时计费<br>• LoRA：按共享实例数计费<br>• **无 TPM 预留费用** | 按**预置吞吐额度（KTPM）** 计费：<br>• 固定月费 = `input_tpm × 单价 + output_tpm × 单价`<br>• 超额部分自动溢出至按量计费（可选关闭）<br>• 实际消耗按阶梯系数 + 缓存折扣动态折算（`provisioned_tokens` 为计费依据） |
| **典型场景** | • 需要对私有数据微调专属模型（如金融问答、医疗报告生成）<br>• 多模态生成任务（图文生成、视频合成、语音克隆）<br>• 需精细化控制 Checkpoint 选择与验证（如筛选最优图像生成效果）<br>• 模型迭代频繁、需快速回滚至历史版本 | • 客服对话系统（高并发、低延迟、长上下文）<br>• 企业知识库检索与摘要（需 100K+ token 输入）<br>• SaaS 产品嵌入式 AI 功能（流量可预测，需 SLA 保障）<br>• 成本敏感型批量推理（利用前缀缓存降低长对话成本） |

---

## 适用场景建议

### ✅ 选择 **Model Production** 当：
- 你已完成模型微调（SFT/Efficient-SFT），并希望将 **Checkpoint 转化为线上服务**；
- 你需要部署 **图像生成、视频生成或语音合成类模型**；
- 你依赖 **Checkpoint 验证产物**（如预览图、首帧、视频链接）进行人工审核后再上线；
- 你要求 **灵活扩缩容**（如按请求峰值动态调整 MU 数量）或 **LoRA 多租户共享部署**；
- 你的模型来自私有训练，**非平台预置列表中的型号**。

### ✅ 选择 **Model Deployment 1（PTU）** 当：
- 你使用的是平台**预置大模型**（如 `glm-5.1`, `deepseek-v4-pro`），且**无需微调**；
- 你的业务对 **TPM 稳定性、P99 延迟、长文本处理（>32K）有硬性要求**；
- 你希望获得 **前缀缓存带来的成本优化**（如多轮客服对话、文档分析）；
- 你能预估月度流量，并愿意为确定性算力支付固定费用（性价比优于按量）；
- 你接受 **模型能力受限于 PTU 白名单**，且不涉及多模态输出需求。

### ⚠️ 明确不兼容场景：
- **不要尝试将 Model Production 发布的 custom model（如 `qwen3-14b-ft-xxx`）部署为 PTU** —— 系统会拒绝或返回 400 错误；
- **不要在 PTU 部署中期望获取视频/图像 URL 输出** —— PTU 仅支持文本模型；
- **不要在 Model Production 流程中跳过 Checkpoint 验证直接部署** —— 可能导致服务不可用（尤其视频/图像模型需验证产物有效性）。

---

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键依据 |
|----------|----------|----------|
| “我微调了一个 `qwen3-14b`，想上线提供 API” | **Model Production** | 自定义模型唯一入口；支持文本生成全流程；需通过 `list-checkpoints` 获取 `model_name` 后部署 |
| “我要部署 `glm-5.1` 做客服机器人，日均 500 万 tokens，要求首字延迟 <300ms” | **Model Deployment 1（PTU）** | PTU 提供确定性吞吐与前缀缓存；`glm-5.1` 在 PTU 白名单内；长输入支持达 200K |
| “我有一个 LoRA 适配器，想让 10 个客户共享同一个基座模型” | **Model Production（LoRA 部署）** | PTU 明确不支持 LoRA；Model Production 提供 `lora` 部署计划，支持多租户隔离 |
| “我需要上传一张图，生成描述 + 生成相似图” | **Model Production** | 多模态输入/输出仅 Model Production 支持；`wan2.7-image-pro` 等模型不在 PTU 白名单 |
| “我已有 `qwen3.7-plus-2026-05-26`，想低成本跑长文档摘要（80K tokens）” | **Model Deployment 1（PTU）** | 该模型支持 PTU；阶梯系数 + 缓存折扣可显著降低长输入成本；无需自行运维实例 |

> 💡 **最佳实践提示**：  
> - 若项目初期不确定是否需微调，**优先用 PTU 部署预置模型验证业务逻辑**；待 MVP 成熟后，再通过 Model Production 引入定制模型。  
> - 所有 Model Production 部署均需关注 `expire_time` 和 Region 限制（Checkpoint API 目前仅北京可用）；PTU 部署无此约束。  
> - PTU 的 `provisioned_tokens` 消耗可通过 `/v1/usage` 接口实时监控，而 Model Production 的 MU/CU 使用量需通过资源账单查看。  

---  
*最后更新：2025年4月 | 百炼平台技术文档组*

## 被对比主题页

- [model production](../api/model-production.md)
- [model deployment 1](../guides/model-deployment-1.md)


