# [模型部署](../concepts/model-deployment.md)方式对比：高并发推理、压缩、生产化部署

本文旨在帮助开发者在百炼平台上针对不同业务目标，科学选择[模型部署](../concepts/model-deployment.md)路径。随着大模型应用从实验走向规模化落地，单一“部署即上线”模式已无法满足多样化需求：  
- **高并发推理**关注吞吐确定性与响应实时性，适用于流量可预期或交互强敏感场景；  
- **模型压缩**聚焦资源效率与成本优化，是微调后模型轻量化落地的关键环节；  
- **生产化部署（Model Production）** 提供端到端的模型生命周期管理能力，是模型从训练成果转化为稳定在线服务的核心枢纽。  

三者定位不同、能力正交、可组合使用——例如：先通过 *[model production](../api/model-production.md)* 完成微调并部署基础服务，再对部署模型启用 *[model compression](../guides/model-compression.md)* 降低成本，最后为该压缩模型配置 *TPM 预留* 保障高并发稳定性。本文将从技术维度系统对比，辅助开发者完成精准选型。

## 关键维度对比表

| 维度 | 高并发推理（TPM 预留 / 快速模式） | 模型压缩（Model Compression） | 生产化部署（Model Production） |
|------|----------------------------------|------------------------------|------------------------------|
| **核心目标** | 保障吞吐稳定性（TPM）或提升单请求响应速度（Fast Mode） | 降低推理资源消耗（MU）与单位成本，支持轻量部署 | 实现模型从训练成果到可调用在线服务的工程化交付 |
| **输入格式** | 标准 OpenAI 兼容请求体（`messages`, `model`, `max_tokens` 等）；TPM 需专属 `model` code；Fast Mode 需专用域名 | 微调成功的自定义模型 ID（如 `ft-qwen35-20260223`） + 量化模板 + 可选校准数据集 | 模型 ID（`model_id`）或微调作业 ID（`fine_tuning_job_id`） + 部署名称（`deployment_name`） |
| **输出格式** | 同标准 API 响应结构；Fast Mode 额外返回 `reasoning_content` 字段（流式/非流式均含） | 新生成的压缩模型 ID（如 `my-qwen35-int4`），不可逆，不支持后续微调 | 部署服务唯一 endpoint URL（如 `https://.../deployments/{name}/chat/completions`）及服务元信息 |
| **支持模型** | **TPM 预留**：Qwen3.6-Flash、DeepSeek-v4-Pro、GLM 系列等主流基础/微调模型（北京/新加坡）<br>**快速模式**：仅 `glm-5.2-fast-preview`（北京/新加坡，Preview 阶段） | **仅限百炼平台内完成且状态为“成功”的微调模型**（如 `qwen3.5-flash-2026-02-23`）；不支持基础模型、第三方模型 | **所有百炼平台托管模型**：包括基础模型（`qwen2-7b-chat`）、微调产出模型（`ft-xxx`）、手动导入模型；支持 LoRA 微调作业管理 |
| **API 端点** | - TPM 预留：复用标准 dashscope 域名（`https://dashscope.aliyuncs.com/api/v1/services/...`）<br>- 快速模式：专用兼容模式域名（`https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`） | 控制台操作为主；API 接口暂未开放（当前为控制台驱动任务创建） | `/v1/fine_tuning_jobs`（启动/查询微调）<br>`/v1/deployments`（创建/管理部署服务）<br>均需显式指定 `region`（如 `cn-beijing`） |
| **计费方式** | - TPM 预留：按预留容量（kTPM/月）预付费，超限部分按量计费（自动溢出）或拒绝（仅预留）<br>- 快速模式：按实际 token 使用量计费，单价高于标准 API（因加速资源溢价） | 压缩任务本身限时免费；**压缩后模型的部署费用按 MU 规格单独计费**（如 MU8×1 vs MU1×2） | - 微调作业：按 GPU 小时计费<br>- 部署服务：按所选 MU 规格（如 MU4/MU8）及运行时长计费<br>- 调用流量：按 token 用量计费（同标准 API） |
| **典型场景** | - TPM：电商大促客服机器人、金融风控实时决策链路、SaaS 平台核心 AI 功能<br>- Fast Mode：编程助手实时补全、Agent 多步推理中单步低延迟要求环节 | 微调后的专属模型需长期稳定运行，但对成本敏感（如企业知识库问答、垂直领域 SaaS 插件）；边缘/轻量级容器环境部署需求 | - 快速验证微调效果<br>- 构建多版本 A/B 测试服务<br>- 将自有数据微调成果固化为生产服务<br>- 管理模型迭代生命周期（训练→部署→下线） |
| **地域支持** | TPM 预留 & 快速模式：华北2（北京）、新加坡（两地隔离，code 不通用） | 仅华北2（北京） | 全地域支持（调用时必须显式指定 `region` 参数） |
| **关键限制** | - TPM 与 Fast Mode 模型支持无交集<br>- Fast Mode 为 Preview 功能，接口/计费/可用性可能变更<br>- TPM 容量计算受输入长度阶梯系数、缓存命中率影响，需精确估算 | - 不可逆：压缩后模型禁止微调、禁止二次压缩<br>- 仅支持 PTQ（后训练量化），不支持剪枝/蒸馏<br>- 校准数据须提前发布，不支持 OSS 直接挂载 | - 单账号最多 5 个并发微调作业、3 个同[模型部署](../concepts/model-deployment.md)实例<br>- 微调输出模型默认保留 90 天<br>- 部署服务不支持热更新，需删旧建新 |

## 适用场景建议

| 业务需求 | 推荐方案 | 关键理由 | 组合提示 |
|----------|----------|----------|----------|
| **流量高峰可预测，且不可接受限流或抖动**（如双十一大促期间的智能导购） | ✅ TPM 预留 | 提供确定性吞吐保障（kTPM 锁定），支持自动溢出降级，兼顾稳定性与弹性 | 可与 `*-fast-preview` 模型组合：先为 `glm-5.2-fast-preview` 创建 TPM 预留，再用其专属 code 调用，实现“加速+保底”双重保障 |
| **用户交互强实时性要求，单次响应延迟敏感**（如代码 IDE 中的实时补全、Agent 的思考链首步） | ✅ 快速模式（谨慎评估） | TPS 提升 1.5~2 倍，内置排队缓冲，显著降低 P99 延迟 | ⚠️ 仅限非核心链路试用；务必监控 preview 风险；若需容量保障，必须搭配 TPM 预留使用 |
| **已微调出高性能模型，但推理成本过高或资源受限**（如微调后的法律模型需在低成本容器集群部署） | ✅ 模型压缩 | 在可控精度损失下大幅降低 MU 占用（例：MU1×2 → MU8×1），直接节省部署成本 | 建议利用免费期测试多个量化模板，用真实业务数据集验证效果后择优部署；压缩后模型仍可通过 *[model production](../api/model-production.md)* 部署为服务 |
| **需将微调成果快速上线验证，或构建多版本灰度/AB 测试** | ✅ 生产化部署 | 提供标准化 API 管理微调作业与部署服务，支持 `deployment_name` 隔离多实例，生命周期清晰可控 | 是其他两项的前提：TPM 预留/快速模式作用于已部署的模型；模型压缩对象必须是 *[model production](../api/model-production.md)* 产出的微调模型 |
| **需长期稳定运行、支持热更新与无缝迭代** | ✅ 生产化部署 + TPM 预留（组合） | *model production* 提供服务抽象层，TPM 预留保障底层资源，二者结合可实现“模型升级不停服”（新模型部署 → 切流 → 下线旧部署） | 不推荐直接对压缩模型启用快速模式（当前不支持）；TPM 预留可作用于压缩后的模型 ID |

## 技术选型参考（面向开发者）

- **第一步：确认模型来源与状态**  
  → 若模型来自百炼微调且状态为“成功”：可进入 *[model compression](../guides/model-compression.md)* 或 *model production* 流程；  
  → 若模型为基础模型或第三方导入：仅支持 *model production* 部署 和 *high speed inference*（TPM/Fast Mode）加速，**不可压缩**。

- **第二步：明确核心瓶颈**  
  → **卡在吞吐/延迟？** → 优先评估 TPM 预留（稳）或快速模式（快，Preview 风险自担）；  
  → **卡在成本/MU 资源？** → 对微调模型执行 *[model compression](../guides/model-compression.md)*，再部署；  
  → **卡在上线流程混乱、多版本难管理？** → 以 *model production* 为统一入口，规范训练→部署→调用链路。

- **第三步：组合策略推荐**  
  ```mermaid
  graph LR
    A[微调成功模型] --> B[模型压缩]
    A --> C[生产化部署]
    B --> D[压缩后模型部署]
    C --> E[TPM 预留保障]
    D --> E
    E --> F[高并发稳定服务]
  ```
  - **稳健路径**：微调 → 压缩 → 部署 → TPM 预留 → 上线  
  - **极致体验路径**：微调 → 部署 → 为 `glm-5.2-fast-preview` 创建 TPM 预留 → 用专属 code 调用（需严格评估 preview 风险）  
  - **快速验证路径**：微调 → 直接部署 → 调用测试 → 根据压测结果决定是否追加压缩或 TPM

- **避坑提醒**  
  - ❌ 不要直接用 `glm-5.2-fast-preview` 调用快速模式期望获得容量保障——必须先创建 TPM 预留并使用其生成的专属 model code；  
  - ❌ 不要在压缩后的模型上尝试微调或二次压缩——操作将失败，需回退至原始微调模型重试；  
  - ❌ 部署接口调用时遗漏 `region` 参数将返回 400 错误，此为隐含强制要求；  
  - ❌ TPM 预留退订后专属 code 立即失效，建议开启自动续费并设置用量告警。

> **总结**：三者非替代关系，而是分层协作的“能力栈”。*Model Production* 是地基，*Model Compression* 是减重优化器，*High Speed Inference* 是性能加速器。合理组合，方能兼顾稳定性、成本与体验。

## 被对比主题页

- [model high speed inference](../guides/model-high-speed-inference.md)
- [model compression](../guides/model-compression.md)
- [model production](../api/model-production.md)


