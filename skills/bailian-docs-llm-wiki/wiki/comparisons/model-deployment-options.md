# 模型部署方式对比：Model Production、Model Deployment 1 与 Model High Speed Inference

## 对比目的与背景

在百炼平台中，模型从开发到上线存在多种技术路径，不同部署方式面向差异化的业务目标与工程约束。`Model Production` 聚焦**模型定制化生产闭环**（训练+部署一体化），`Model Deployment 1` 提供**标准化、多模式的推理服务托管能力**，而 `Model High Speed Inference` 则专为**高吞吐、低延迟场景提供性能增强层**（非独立部署方案，而是对已有部署的加速增强）。本对比旨在帮助开发者清晰理解三者的定位边界、能力边界与适用条件，避免因选型错配导致资源浪费、性能瓶颈或架构返工。

---

## 关键维度对比表

| 维度 | Model Production | Model Deployment 1 | Model High Speed Inference |
|------|------------------|----------------------|----------------------------|
| **核心定位** | 端到端模型定制流水线（微调训练 + 推理部署） | 生产级推理服务统一托管平台（支持多计费/调度模式） | 推理性能增强能力（TPM 预留保障容量确定性；Fast Mode 提升单请求输出速度） |
| **输入格式** | 微调阶段：JSONL 格式训练数据（需上传至百炼对象存储）<br>部署阶段：标准 OpenAI `/v1/chat/completions` 请求体 | 全量兼容 OpenAI / Anthropic / DashScope 协议的请求体（含 `messages`, `system`, `tools`, `stream` 等字段） | 完全复用对应基础模型的输入格式（如 `glm-5.2-fast-preview` 使用其专属协议） |
| **输出格式** | 部署后完全兼容 OpenAI 格式（含 `id`, `choices[0].message.content`, `usage` 等字段） | 同样兼容 OpenAI 格式；MU 模式支持 `thinking` 字段（当 `enable_thinking=true`）；[Token](../concepts/token.md) 用量模式返回 `lora_usage` 字段 | TPM 预留：输出格式与基础模型一致<br>Fast Mode：流式响应新增 `reasoning_content` 字段；非流式响应中 `reasoning_content` 与 `content` 并存 |
| **支持模型** | • 仅限百炼托管基础模型（如 `qwen2-7b-chat`）的监督微调（SFT）<br>• 支持导入 ONNX/Triton 格式第三方模型（需严格校验） | • PTU 模式：`glm-5.1`（64K）、`deepseek-v4-pro`、`qwen3.7-plus-2026-05-26` 等（长上下文优化模型）<br>• MU 模式：全量千问系列（Qwen3/VL/Omni）、DeepSeek、GLM、Kimi 等<br>• [Token](../concepts/token.md) 用量（LoRA）：仅限 LoRA 微调后的 `qwen3-8b`、`qwen3-vl-8b-instruct` 等指定模型 | • TPM 预留：支持十余个主流模型（含 `qwen3.7-max`、`deepseek-v4-pro`、`glm-5.2` 等），覆盖华北2（北京）与新加坡地域<br>• Fast Mode：**仅限 `glm-5.2-fast-preview`**（Preview 阶段，不支持其他模型变体） |
| **API 端点** | • 微调：`POST /v1/fine_tuning_jobs`<br>• 部署：`POST /v1/deployments`<br>• 推理：`POST {endpoint_url}/v1/chat/completions`（专属 endpoint） | `POST https://dashscope.aliyuncs.com/api/v1/deployments`（创建）<br>`GET /api/v1/deployments/{deployed_model}`（状态）<br>推理：`Generation.call(model='deployed_model_id', ...)` 或直接调用 `/v1/chat/completions`（使用 `model` 参数） | • TPM 预留：**复用标准 dashscope 域名**，仅替换 `model` ID（如 `qwen3.7-plus-2026-05-26-tpm-xxxxx`）<br>• Fast Mode：**必须使用专属域名**：<br>`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（北京）或新加坡对应域名 |
| **计费方式** | • 微调任务：按 GPU 小时计费（`gpu.2xlarge` 等实例规格 × 运行时长）<br>• 部署实例：按实例规格（`gpu.2xlarge`）和运行时长计费（秒级） | • PTU 模式：预购吞吐额度（kTPM），超限可选自动溢出（按量计费）或拒绝服务<br>• MU 模式：按模型单元（MU）规格 × 副本数 × 运行时长计费<br>• [Token](../concepts/token.md) 用量（LoRA）：按实际输入/输出 token 计费 | • TPM 预留：按预留的输入/输出 kTPM 月度订阅计费（支持缓存折扣）<br>• Fast Mode：按实际输出 token 计费（`glm-5.2-fast-preview` 单价为 4 元/百万 token，含缓存优惠） |
| **典型场景** | • 构建企业专属对话模型（基于内部知识微调 Qwen）<br>• 快速验证自研模型（ONNX/Triton）在线服务能力<br>• 需要完整生命周期管理（训练日志、部署状态、版本追溯）的 MLOps 流程 | • 高并发客服系统（PTU 模式保障 SLA）<br>• Agent 编排平台（MU 模式启用 Thinking 模式 + PD 分离）<br>• A/B 效果测试（Token 用量模式低成本试跑 LoRA 模型） | • 实时编程助手（Fast Mode 降低首 token 延迟至 <200ms）<br>• 大促期间流量洪峰（TPM 预留确保核心链路不被限流）<br>• 对响应抖动敏感的交互式应用（如语音合成前置推理） |

---

## 各方案适用场景建议

### ✅ 推荐选择 `Model Production` 当：
- 你需要**从零开始定制一个专属模型**（例如：用内部 FAQ 数据微调 Qwen2-7B Chat）；
- 你已拥有符合 ONNX/Triton 规范的自研模型，需快速验证其在线服务能力；
- 你要求**训练与部署状态可追踪、可审计、可回滚**（如微调失败自动终止部署）；
- 你接受较长的交付周期（微调耗时数小时至数天，部署分钟级）。

⚠️ 不推荐用于：
- 仅需调用现成大模型（无需训练）；
- 对首 token 延迟有严苛要求（如 <100ms）；
- 需要动态扩缩容或精细限流控制（无 RPM/TPM 配置项）。

---

### ✅ 推荐选择 `Model Deployment 1` 当：
- 你已选定成熟基础模型（如 `qwen3.7-plus`），只需**开箱即用的稳定推理服务**；
- 你的业务负载特征明确：高并发稳态（选 PTU）、需要独占资源调优（选 MU）、或低频效果验证（选 Token 用量）；
- 你需要**灵活的推理配置**（如开启 Thinking 模式、设置 `max_context_length=128K`、启用 PD 分离）；
- 你希望统一管理多个模型的部署生命周期（控制台一站式操作 + API 批量管理）。

⚠️ 不推荐用于：
- 需要修改模型权重（如全参微调）；
- 要求跨地域一键部署（API 当前仅支持华北2）；
- 期望部署后自动获得性能加速（它本身不提供 TPM 预留或 Fast Mode）。

---

### ✅ 推荐选择 `Model High Speed Inference` 当：
- 你已在使用 `Model Deployment 1` 或标准 API，但遭遇**高峰期限流（429）或首 token 延迟超标**；
- 你的业务 SLA 明确要求：**99% 请求首 token < 200ms**（选 Fast Mode）或 **99.9% 请求成功率 ≥ 99.99%**（选 TPM 预留）；
- 你愿意为确定性性能支付溢价（TPM 预留需预购；Fast Mode 当前仅限单一模型）；
- 你能接受 Preview 特性风险（Fast Mode 接口、模型、地域可能变更）。

⚠️ 不推荐用于：
- 作为独立部署入口（它必须依附于已有模型部署）；
- 需要 LoRA 微调模型的加速（当前 Fast Mode 不支持 LoRA 变体）；
- 成本极度敏感且流量波动小的后台批处理任务（标准部署更经济）。

---

## 技术选型参考指南（面向开发者）

| 你的需求 | 推荐方案 | 关键理由 | 行动建议 |
|----------|----------|----------|----------|
| “我要用销售合同训练一个法律问答模型，并上线为 API” | ✅ Model Production | 唯一支持 SFT 微调 + 自动部署闭环的路径；输出模型可复用于后续迭代 | 1. 准备 JSONL 训练集 → 2. 调用 `/v1/fine_tuning_jobs` → 3. 轮询成功后部署 → 4. 使用专属 endpoint |
| “我已选好 `qwen3.7-plus`，要支撑每日 500 万次调用，要求 P99 延迟 < 800ms” | ✅ Model Deployment 1 (PTU) + ✅ Model High Speed Inference (TPM 预留) | PTU 提供确定性吞吐基线，TPM 预留进一步锁定容量防突增；二者叠加可达成高 SLA | 1. 创建 PTU 部署 → 2. 为该部署申请对应 kTPM 预留 → 3. 在请求中使用预留 model ID |
| “我在做 AI 编程助手，用户输入后需 300ms 内返回首个代码 token” | ✅ Model High Speed Inference (Fast Mode) | 当前唯一能将首 token 延迟压至 200ms 级别的方案；`glm-5.2-fast-preview` 经实测满足该指标 | 1. 确认 workspace 已开通北京/新加坡地域权限 → 2. 使用 `maas.aliyuncs.com` 域名 + `glm-5.2-fast-preview` model ID → 3. 客户端适配 `reasoning_content` 解析 |
| “我有 10 个不同业务线的 LoRA 模型，需低成本验证效果” | ✅ Model Deployment 1 (Token 用量模式) | 按 token 计费，无闲置成本；支持批量 LoRA 导入与快速启停 | 1. 将 LoRA 权重上传 OSS → 2. 调用 `/api/v1/deployments` 指定 `plan: "lora"` → 3. 监控 `lora_usage` 字段优化 [prompt](../guides/prompt.md) |
| “我需要把本地 PyTorch 模型（非 Qwen/GLM）部署上线” | ✅ Model Production（导入 ONNX/Triton） | 唯一支持第三方模型格式导入的路径；需自行完成格式转换与校验 | 1. 将模型导出为 ONNX（含 dynamic axes）或 Triton Plan → 2. 上传至百炼对象存储 → 3. 调用 `/v1/deployments` 指定 `model_id` |

> 💡 **组合使用提示**：  
> - `Model Production` 输出的微调模型（如 `ft-qwen3-8b-abc123`），可作为 `Model Deployment 1` 的 `model_name` 输入，享受 MU/PTU 等高级调度能力；  
> - `Model Deployment 1` 创建的部署（如 `my_qwen_ptu`），可进一步绑定 `Model High Speed Inference` 的 TPM 预留，实现“基础服务 + 容量保险”双保障；  
> - `Model High Speed Inference` 的 Fast Mode **不可与任何微调模型（含 LoRA）叠加**，仅限官方发布的 `glm-5.2-fast-preview`。

---  
*最后更新：2026年6月*  
*本文档依据百炼平台 v2.4.0 文档体系整理，具体行为请以控制台与最新 API 文档为准。*

## 被对比主题页

- [model production](../api/model-production.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


