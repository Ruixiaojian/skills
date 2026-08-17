# 模型部署方案对比：高并发推理、模型压缩与模型部署指南

本文旨在帮助开发者清晰区分百炼平台三大核心模型交付能力——**高并发推理（Fast Mode）**、**模型压缩（Quantization）** 与 **通用模型部署（Deployment）**，明确其定位、能力边界、技术约束及适用阶段。三者并非互斥替代关系，而是构成“训练 → 压缩 → 部署 → 加速推理”的完整生产链路中的不同环节：  
- **模型压缩** 是**模型优化阶段**的可选预处理动作，作用于微调后的自定义模型，目标是降本（降低 MU 规格）；  
- **模型部署** 是**服务化阶段**的必经步骤，为任意合规模型（基础模型、微调模型、压缩模型）提供稳定、可控、可计量的推理服务入口；  
- **高并发推理（Fast Mode）** 是**运行时加速能力**，仅对特定部署态模型（`glm-5.2-fast-preview`）生效，通过底层调度与流式协议优化，提升端到端吞吐与响应体验。  

正确理解三者层级关系，是避免误用（如对非 fast 模型设 `stream=true` 却期待 `reasoning_content`）、规避成本浪费（如为未压缩模型直接选用高规格 MU）、保障服务 SLA 的前提。

---

## 关键维度对比表

| 维度 | 高并发推理（Fast Mode） | 模型压缩（Quantization） | 通用模型部署（Deployment） |
|------|--------------------------|---------------------------|------------------------------|
| **本质定位** | 运行时推理加速能力（专用模式） | 模型离线优化技术（量化转换） | 模型服务化基础设施（资源编排 + API 网关） |
| **输入格式** | 标准 OpenAI 兼容请求体（含 `messages`, `model="glm-5.2-fast-preview"`） | 已完成微调且状态为 `SUCCEEDED` 的自定义模型 ID（仅限百炼内训产出） | 模型 ID（支持基础模型、微调模型、压缩模型、LoRA 导入模型） |
| **输出格式** | OpenAI 兼容格式，扩展字段：<br>• `delta.reasoning_content`（流式思考过程）<br>• `usage.completion_tokens_details.reasoning_tokens` | 生成全新模型 ID（源模型名 + 后缀，如 `qwen35-ft-awq8`），无标准 API 输出 | 部署成功后返回专属服务 ID（如 `dep-xxxxx`），推理调用返回标准 OpenAI 或百炼原生格式 |
| **支持模型** | 仅 `glm-5.2-fast-preview`（华北2/新加坡地域限定） | 仅百炼平台内微调成功的自定义模型（Qwen 系列为主，如 `qwen3.5-flash-2026-02-23` 微调产出） | 广泛支持：<br>• 预置大模型（qwen3.8-Max, glm-5.2, deepseek-v4-pro 等）<br>• 微调/压缩后模型<br>• LoRA 导入模型（需符合 rank/模板等校验） |
| **API 端点** | 专用域名：<br>`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（华北2）<br>`https://{workspace_id}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`（新加坡） | **无公开 API**：全部操作在控制台「模型 > 模型训练 > 模型压缩」完成，后台异步执行 | 标准部署管理 API：<br>`POST /api/v1/deployments`（创建）<br>`GET /api/v1/deployments/{id}`（查询）<br>推理调用使用 `Generation.call(model='dep-xxxxx', ...)` |
| **计费方式** | 按 token 计费（`prompt_tokens` + `completion_tokens`，含 `reasoning_tokens`），单价按地域浮动，与标准 API 逻辑一致但独立计费 | **压缩任务本身免费**（限时）；压缩后模型部署费用按所选 MU 规格计费（如 MU8×1 ¥47/小时） | 三类计费模式：<br>• **PTU**：预购吞吐量（KTPM/月），超量可自动转按量或限流<br>• **MU**：按模型单元规格 × 副本数 × 时长计费（如 MU1×2 ¥108/小时）<br>• **[Token](../concepts/token.md)用量（LoRA专属）**：按实际调用 token 数计费（¥/1K tokens） |
| **典型场景** | AI 编程助手实时补全、Agent 多步推理链中低延迟决策、高频率对话交互（需渐进式思考呈现） | 微调后模型上线前成本优化、边缘/轻量级业务场景对推理延迟容忍度较高、预算敏感型项目 | • PTU：流量稳定、SLA 要求严苛的 SaaS 服务<br>• MU：需独占资源、长上下文、多模态、Omni 推理等复杂任务<br>• [Token](../concepts/token.md)用量：低频、突发性、实验性 LoRA 应用（如 A/B 测试） |
| **地域支持** | 华北2（北京）、新加坡 | 仅华北2（北京） | PTU/MU：华北2（北京）<br>[Token](../concepts/token.md)用量：华北2（北京）<br>（注：部分预置模型在新加坡有定价，但 API 部署不支持跨地域） |
| **是否可逆/可变更** | 不可逆（模式由 model ID + endpoint 决定）；不可切换为标准模式 | **不可逆**：压缩后模型不支持继续微调、不支持二次压缩、不支持回滚至原模型 | 可动态调整：<br>• PTU：增减 `input_tpm`/`output_tpm`<br>• MU：PATCH 扩容 `capacity`（副本数）<br>• Token用量：不支持 API 扩容，需人工申请 |

---

## 各方案适用场景建议

### ✅ 推荐选择 **高并发推理（Fast Mode）** 当：
- 业务已部署 `glm-5.2-fast-preview` 模型，且对首 Token 延迟（TTFT）和每秒输出 Token 数（TPS）有强要求；
- 前端需实现“思考过程渐进渲染”（如显示 `reasoning_content` 后再输出最终答案）；
- 流量具备明显波峰波谷特征，能接受排队机制（而非硬限流 429），并已做好客户端超时与重试策略；
- **注意**：此方案不是通用加速开关，不能用于其他模型（包括 `glm-5.2` 标准版）。

### ✅ 推荐选择 **模型压缩（Quantization）** 当：
- 已完成 Qwen 系列模型的微调，且部署成本成为瓶颈（如当前使用 MU1×2，希望降至 MU8×1）；
- 对精度损失有可控预期（可通过业务测试集验证压缩后效果衰减 ≤3%）；
- 模型生命周期以“一次训练、长期服务”为主，无需后续迭代微调；
- **注意**：压缩是**前置动作**，必须在部署前完成；压缩后模型仍需走标准部署流程（PTU/MU/Token用量）才能对外提供服务。

### ✅ 推荐选择 **通用模型部署（Deployment）** 当：
- 需要将任意模型（基础模型、微调模型、压缩模型、LoRA 模型）转化为生产可用的 API 服务；
- 要求资源隔离、性能保障、扩缩容能力、访问权限管控、调用审计等企业级运维能力；
- 业务流量模型明确：稳定流量选 PTU，弹性需求选 MU，实验性 LoRA 选 Token用量；
- **注意**：这是所有模型上线的**必经环节**；Fast Mode 和压缩模型均需先完成部署，再启用对应能力。

---

## 技术选型参考（面向开发者）

| 你的需求 | 推荐路径 | 关键检查点 |
|----------|-----------|-------------|
| “我要把刚微调好的 `qwen3.5-flash` 模型上线，但成本太高” | **微调模型 → 模型压缩 → MU 部署** | ✔ 确认微调任务状态为 `SUCCEEDED`<br>✔ 在控制台「模型压缩」选择该模型 + 合适量化模板（如 MU8）<br>✔ 压缩成功后，在「模型部署」中选择新生成的压缩模型 ID，部署模式选 `MU`，规格填 `MU8` |
| “我的 Agent 应用需要毫秒级响应，且用户能看到思考过程” | **部署 `glm-5.2-fast-preview` → 使用 Fast Mode 专用 endpoint** | ✔ 确保业务空间开通于华北2或新加坡<br>✔ `base_url` 必须为专用域名（非标准 API 地址）<br>✔ 请求中 `model` 字段严格为 `glm-5.2-fast-preview`<br>✔ 客户端解析 `delta.reasoning_content` 和 `delta.content` 分别渲染 |
| “我有个 LoRA 微调的小模型，只做内部测试，不想买资源包” | **LoRA 模型导入 → Token用量部署** | ✔ 检查 LoRA 模型 `rank` 是否为 8/16/32/64<br>✔ 控制台「模型导入」上传，确认状态为 `READY`<br>✔ 部署时 `plan: "lora"`，`model_name` 填导入后的模型 ID<br>✔ 注意：`capacity` 字段无效，扩缩容需提工单 |
| “我需要支持 100K 上下文的千问3.8-Max，且要求 99.9% 请求 <2s” | **直接 PTU 部署 `qwen3.8-Max`** | ✔ 选择 PTU 模式，设置足够 `input_tpm`（如 500）和 `output_tpm`（如 200）<br>✔ 开启 `overflow_strategy: "ptu_only"` 防止超量转按量导致计费突增<br>✔ 利用前缀缓存折扣降低长文本成本（详见文档） |
| “我同时需要视觉理解（VL）和文本生成，且要低首 Token 延迟” | **MU 部署 `qwen3-vl-235b-a22b-thinking` + 启用 `enable_thinking`** | ✔ 部署参数中显式设置 `"enable_thinking": true`<br>✔ 选择支持 PD 分离的 MU 规格（如 MU4+）<br>✔ 验证 `max_context_length` 满足业务需求 |

> **重要提醒**：  
> - **无“一键加速”魔法**：Fast Mode 不是给任意模型加个 flag 就生效，它依赖专用模型、专用 endpoint、专用调度器；  
> - **压缩 ≠ 部署**：压缩产生的是新模型 ID，不是服务；必须再走一次部署流程，才能获得 endpoint；  
> - **部署是基石**：无论你用不用压缩、用不用 Fast Mode，只要模型要对外提供 API，就必须完成部署。  
>   
> 建议实践顺序：`模型选型 → （可选）微调 → （可选）压缩 → 必选部署 → （条件启用）Fast Mode`。

## 被对比主题页

- [model high speed inference](../guides/model-high-speed-inference.md)
- [model compression](../guides/model-compression.md)
- [model deployment 1](../guides/model-deployment-1.md)


