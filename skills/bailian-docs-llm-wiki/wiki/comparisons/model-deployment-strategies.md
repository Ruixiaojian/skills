# 模型部署策略对比：Model Production、Model Deployment 1 与 Model High Speed Inference

本文旨在帮助开发者清晰理解百炼平台当前提供的三类核心模型部署能力——`Model Production`（生产级模型管理）、`Model Deployment 1`（统一部署框架）与 `Model High Speed Inference`（高性能推理加速）——在定位、能力边界、技术约束及适用场景上的本质差异。三者并非简单版本迭代关系，而是面向不同架构目标与业务诉求设计的**正交能力层**：  
- `Model Production` 聚焦**高 SLA 生产环境的可编程容量保障与全生命周期治理**，是金融、政务等关键系统落地的合规性基座；  
- `Model Deployment 1` 提供**标准化、多计费模式融合的通用部署入口**，强调模型来源灵活性（预置/LoRA）、资源粒度可控性（PTU/MU/[Token](../concepts/token.md)）与跨场景适配能力；  
- `Model High Speed Inference` 则专精于**性能维度突破**，通过模型侧优化（Fast Mode）与基础设施预留（TPM Reservation）双路径，解决低延迟、高吞吐、强确定性的实时推理瓶颈。

以下从关键工程维度展开结构化对比，为技术选型提供客观依据。

## 关键维度对比表

| 维度 | Model Production | Model Deployment 1 | Model High Speed Inference |
|------|------------------|----------------------|----------------------------|
| **核心定位** | 面向高可用、高确定性生产环境的**端到端容量保障型部署体系**（含微调→部署→扩缩容→续费全链路） | 百炼平台统一的**通用模型部署入口**，支持多计费模式（PTU/MU/[Token](../concepts/token.md)）与多模型来源（预置/LoRA） | 专注**推理性能极致优化**的加速能力层，包含模型侧加速（Fast Mode）与资源侧保障（TPM Reservation）两类独立能力 |
| **输入格式** | 标准 OpenAI 兼容请求体（`messages`, `temperature`, `max_tokens` 等），支持 `thinking_output_tpm` 等扩展字段（仅思考模型） | 完全兼容 OpenAI 标准格式；MU 模式额外支持 `rpm_limit`, `tpm_limit`, `enable_thinking`, `max_context_length` 等自定义控制参数 | Fast Mode：需使用专属模型 ID（如 `glm-5.2-fast-preview`），流式响应返回分离的 `reasoning_content`/`content`；TPM Reservation：输入格式与标准 API 一致，仅 `model` 字段为控制台生成的专属 code |
| **输出格式** | 标准 OpenAI 兼容响应（含 `usage`, `choices[0].message.content`）；思考模型支持 `thinking_usage` 字段 | 同标准 OpenAI 格式；MU 模式支持更细粒度的 `usage` 统计（如按副本、按缓存命中率拆分） | Fast Mode：流式 delta 中新增 `reasoning_content` 字段，用于接收思考过程；TPM Reservation：输出格式与标准 API 完全一致 |
| **支持模型** | 严格限定 9 款模型（`qwen-max`, `qwen-plus`, `qwen-flash`, `glm-5.2`, `glm-5.1`, `deepseek-v4-flash`, `deepseek-v4-pro`, `kimi-k2.6` 及其带时间后缀版本）；`kimi-k2.6` 仅限华北2（北京） | **PTU 模式**：支持部分预置模型（如 `qwen3.8-max`, `deepseek-v4-flash`）及部分 LoRA 模型；<br>**MU 模式**：支持**全部预置模型 + 所有 LoRA 微调模型**；<br>**[Token](../concepts/token.md) 模式**：**仅支持 LoRA 模型**（不支持全参微调） | **Fast Mode**：仅 `glm-5.2-fast-preview`（Preview 阶段，北京/新加坡）；<br>**TPM Reservation**：支持 `Qwen3.8-Max`, `Qwen3.7-Plus-2026-05-26`, `GLM-5.2`, `DeepSeek-v4-Pro-0813`, `Kimi-K2.6` 等（以控制台实时列表为准） |
| **API 端点** | `https://dashscope.aliyuncs.com/api/v1/deployments`（主入口）<br>专属 workspace 域名亦支持 | `https://dashscope.aliyuncs.com/api/v1/deployments`（同一基础路径）<br>支持 OpenAI 兼容路径 `/compatible-mode/v1` | **Fast Mode**：必须使用 workspace 专属域名（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）；<br>**TPM Reservation**：使用标准 DashScope 域名，但 `model` 字段为控制台生成的专属 code |
| **计费方式** | **仅支持 PTU 预留模式**：<br>- `pre_paid`（预付费，按天/月结算）<br>- `post_paid`（后付费，按小时出账）<br>费用 = 预留 `input_tpm` + `output_tpm` + `thinking_output_tpm`（若启用）的容量单价 × 使用时长 | **三模式并存**：<br>- **PTU**：预付费/后付费，按预留 kTPM 计费<br>- **MU**：后付费，按购买的 MU 单元数 × 使用时长计费<br>- **Token**：按实际输入/输出 token 用量计费（仅 LoRA 模型） | **Fast Mode**：按实际 token 用量计费（单价独立，如北京输入 ¥56/百万 token）；<br>**TPM Reservation**：按预购的 kTPM 容量 × 自然日天数计费（如北京 `GLM-5.2` 输入 ¥36.29 / 10,000 TPM/天） |
| **典型场景** | 银行核心智能客服（要求 99.95% SLA、确定性吞吐、分钟级扩缩容）、政务热线（需合规审计、容量可追溯）、高价值内容审核（拒绝率敏感，不可溢出限流） | - **PTU**：中大型企业知识库问答（流量平稳，成本敏感）<br>- **MU**：医药研发分子模拟（需独占 GPU、自定义上下文长度与限流）<br>- **Token**：A/B 测试新 LoRA 模型效果（低并发、快速验证） | **Fast Mode**：实时音视频字幕生成、高频交互式代码补全（首 Token < 200ms，TPS > 80）<br>**TPM Reservation**：电商大促期间商品文案生成服务（峰值流量可预测，拒绝任何 429） |

## 各方案适用场景建议

### ✅ 推荐选择 `Model Production`
- 业务对**服务等级协议（SLA）有硬性要求**（如金融、医疗、政务行业），需明确承诺可用性、延迟 P99、吞吐下限；
- 需要**全生命周期自动化管理**：通过 OpenAPI 实现微调任务完成后的自动部署、基于监控指标的自动扩缩容、预付费订单到期前自动续订；
- 流量具备**强周期性或可预测性**，且能接受“预留即付费”的成本模型（避免突发流量导致的不可控按量费用）；
- 必须使用文档明确列出的 9 款高保障模型，且需启用 `thinking_output_tpm` 等深度思考专属能力。

### ✅ 推荐选择 `Model Deployment 1`
- 需要**灵活切换部署策略**：例如，先用 Token 模式验证 LoRA 模型效果，再升级为 PTU 模式投入生产，或为关键任务单独购买 MU 单元隔离资源；
- 模型来源**高度多样化**：既要部署官方预置模型，也要上线自研 LoRA 模型，甚至需支持视觉语言（VL）模型（需冻结 VIT）；
- 对**资源控制粒度有精细要求**：如需限制单实例 RPM、设置最大上下文长度、启用前缀缓存、或强制开启思考模式；
- 业务空间位于**华北2（北京）以外地域**（注意：该方案明确声明仅支持北京地域，其他地域调用可能失败）。

### ✅ 推荐选择 `Model High Speed Inference`
- **性能是第一优先级**：应用无法容忍首 Token 延迟波动（如实时语音转写、交互式游戏 NPC），或需要持续高 TPS 输出（如批量报告生成）；
- 已存在稳定流量基线，但**峰值流量存在确定性尖峰**（如每日早 9 点报表生成、每小时整点数据摘要），需避免公共池争抢导致的抖动；
- 愿意接受 Preview 阶段能力（Fast Mode）或接受专属模型 code 的运维复杂度（TPM Reservation）；
- **不追求通用部署能力**：无需微调联动、无需复杂生命周期管理，仅需一个高性能、低延迟、高吞吐的推理终端。

## 技术选型决策指南（面向开发者）

作为开发者，在启动模型部署前，请按以下逻辑链进行判断：

1. **第一步：确认模型来源与类型**  
   → 若使用 **LoRA 微调模型**，且需快速验证效果 → 选 `Model Deployment 1` 的 **Token 模式**（最低门槛，控制台一键部署）。  
   → 若使用 **LoRA 模型且需生产级稳定性**，或需 **全参微调模型** → `Model Production` 不支持全参模型，`Model Deployment 1` 的 MU 模式是唯一选择。  
   → 若使用 **官方预置模型（如 `qwen-max`, `glm-5.2`）且需最高保障** → 三者均支持，进入第二步。

2. **第二步：评估核心非功能需求**  
   → **是否要求确定性吞吐与 SLA 承诺？** 是 → `Model Production`（TPM 预留）是合规首选；否 → 进入第三步。  
   → **是否需要独占资源、自定义限流或超长上下文？** 是 → `Model Deployment 1` 的 **MU 模式**；否 → 进入第三步。  
   → **是否对首 Token 延迟或持续 TPS 有极致要求？** 是 → `Model High Speed Inference` 的 **Fast Mode**（若模型匹配）或 **TPM Reservation**（若需容量保障）。

3. **第三步：审视运维与成本模型**  
   → 接受预付费、按自然日结算、扩容需异步等待 → `Model Production` 或 `Model High Speed Inference`（TPM Reservation）。  
   → 需要按小时计费、随时释放、自助扩缩容 → `Model Deployment 1` 的 **PTU 或 MU 模式**。  
   → 需要最小化前期投入、按实际用量付费 → `Model Deployment 1` 的 **Token 模式**（LoRA 专用）或 `Model High Speed Inference` 的 **Fast Mode**（token 计费）。

> ⚠️ 重要提醒：  
> - **不要混用能力层**：`Model Production` 的 `ptu_default` 与 `Model Deployment 1` 的 `plan=ptu` 在底层共享 PTU v2 引擎，但前者强制绑定 `service_tier=ptu_default` 并提供续费/溢出策略等高级管理接口，后者更轻量；二者 API 路径相同，但参数语义与约束不同，务必依据文档选择对应参数组合。  
> - **地域是硬约束**：`Model Deployment 1` 明确仅支持华北2（北京）；`Model Production` 和 `Model High Speed Inference` 的部分模型（如 `kimi-k2.6`）在新加坡不可用。部署前请务必核对控制台实时地域支持列表。  
> - **始终以控制台为准**：模型列表、价格、参数选项均动态更新，文档可能存在滞后。创建部署前，请在百炼控制台对应页面确认最新支持范围。

## 被对比主题页

- [model production](../api/model-production.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


