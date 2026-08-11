# 模型部署与生产化方案对比：Model Deployment 1 vs Model Production vs Model Monitoring

## 对比目的与背景

在百炼平台构建 AI 应用时，开发者需在模型“能跑起来”（部署）、“稳跑起来”（生产化）和“持续健康跑”（监控）三个关键阶段做出技术决策。  
- **Model Deployment 1** 是面向快速验证与轻量上线的**基础部署能力**，提供 PTU/MU/[Token](../concepts/token.md) 三种计费模式，强调易用性与灵活性；  
- **Model Production** 是面向企业级 SLA 要求的**全生命周期生产管理能力**，聚焦 TPM 预留、扩缩容、续订、策略配置等稳定性保障机制；  
- **Model Monitoring** 则是独立于部署形态的**可观测性基础设施**，不提供推理服务，但为所有部署形态（无论 PTU/MU/[Token](../concepts/token.md) 或是否来自微调）提供统一的用量、性能、成本与异常洞察。

本对比旨在帮助开发者厘清三者定位差异，避免将监控误认为部署方式、或将 MU 模式等同于生产就绪，从而在架构设计初期即选择匹配业务成熟度的技术路径。

---

## 关键维度对比表

| 维度 | Model Deployment 1 | Model Production | Model Monitoring |
|------|---------------------|-------------------|-------------------|
| **本质定位** | 基础模型服务开通接口（“启动服务”） | 生产级模型服务全生命周期管理（“运营服务”） | 模型调用可观测性平台（“看清服务”） |
| **输入格式** | `model_name` + `plan`（`ptu`/`mu`/`lora`）+ 模式专属参数（如 `ptu_capacity`、`deploy_spec`） | `model_name` + `plan="ptu"` + `service_tier="ptu_default"` + `ptu_capacity`（含 `thinking_output_tpm`） + `charge_type` | 无主动输入；自动采集所有已调用模型的请求/响应元数据（`workspace_id`, `model`, `apikey_id`, `protocol` 等） |
| **输出格式** | 返回 `deployment_id` 和 `deployed_model`（如 `qwen-max-ptu-abc123`），服务进入 `PENDING` → `RUNNING` 状态 | 同样返回 `deployed_model`，但额外支持 `scale`/`renew`/`updateOverflowStrategy` 等状态变更操作，返回异步任务 ID 及状态机流转 | 提供可视化仪表盘、API 查询结果（JSON）、Prometheus 指标（OpenMetrics 格式）、原始日志（JSON Lines）、告警通知（Webhook/钉钉/企微） |
| **支持模型** | • 预置模型：Qwen/DeepSeek/GLM/千问VL/Omni/CosyVoice 等（部分仅支持 [Token](../concepts/token.md) 计费）<br>• 自定义模型：**仅 LoRA 微调模型**（有 rank/词表/chat_template/ViT 冻结等硬约束） | • 9 款指定模型（如 `qwen-max`, `glm-5.2`, `deepseek-v4-pro`, `kimi-k2.6`）<br>• **必须为预置模型或经百炼微调训练生成的模型**（不支持直接导入 LoRA 文件）<br>• 新加坡地域不支持 `kimi-k2.6` | • 基础用量统计：**所有官方模型 + 所有调优后模型**（全域通用）<br>• 高级能力（日志/Prometheus/告警）：仅限北京/上海/新加坡/弗吉尼亚地域，且模型需显式支持（见文档列表） |
| **API 端点** | `POST /api/v1/deployments`（创建）<br>`GET /api/v1/deployments/{deployed_model}`（查询） | `POST /api/v1/deployments`（创建）<br>`PUT /api/v1/deployments/{deployed_model}/scale`（扩缩容）<br>`PUT /api/v1/deployments/{deployed_model}/renew`（续订）<br>`PUT /api/v1/deployments/{deployed_model}/updateOverflowStrategy`（溢出策略） | `GET /api/v1/telemetry/usage`（用量统计）<br>`GET /api/v1/telemetry/logs`（日志查询，需开通）<br>`GET /api/v1/telemetry/metrics`（Prometheus 指标端点，需开通）<br>控制台入口为主，API 为高级集成场景服务 |
| **计费方式** | • PTU：预付费/后付费，按购买 TPM 容量计费（超限可溢出）<br>• MU：按副本数计费（预付费包月/后付费按小时）<br>• Token：按实际 token 数计费（最小 1 token） | • **仅支持 PTU 模式**（TPM 预留）<br>• 必须指定 `charge_type=pre_paid` 或 `post_paid`<br>• 预付费支持 `auto_renewal`，续订逻辑严格（22:00 后提交顺延至 N+2 日） | **不产生推理费用**<br>• 基础监控：免费<br>• 高级监控（日志/Prometheus/告警）：按日志存储量、指标采集频率、告警次数等单独计费（详见计费页） |
| **典型场景** | • A/B 测试新 [prompt](../guides/prompt.md) 或小流量灰度<br>• PoC 快速验证 LoRA 微调效果<br>• 低并发内部工具（如客服知识库问答）<br>• 成本敏感型实验性项目 | • 核心业务 API（如电商商品推荐、金融风控问答）<br>• 需要 SLA 保障（如 99.9% 可用率、首 Token < 500ms）<br>• 流量存在明显波峰波谷（需自动化扩缩容）<br>• 长期稳定运行（需续订与容量规划） | • 定位高延迟请求根因（结合首 Token 延迟、缓存命中率）<br>• 分析 Token 消耗异常（如某 API Key 突增 300% 输出 tokens）<br>• 构建 SLO（如“失败率 < 0.1%”告警）<br>• 审计合规（保留输入/输出日志用于安全审查） |

---

## 适用场景建议

| 场景描述 | 推荐方案 | 理由说明 |
|----------|-----------|-----------|
| **刚完成 LoRA 微调，想快速验证效果，预算有限且无高可用要求** | ✅ Model Deployment 1（Token 计费） | 支持 LoRA 直接部署，按调用计费，零闲置成本；无需预购容量，适合短期验证。 |
| **已上线的客服机器人，日均调用量 50 万 tokens，要求首 Token 延迟 ≤ 800ms，且需应对促销期间 3 倍流量峰值** | ✅ Model Production（PTU 预留 + 自动扩缩容） | TPM 预留保障基线吞吐，`scale` API 支持分钟级扩容，`overflow_strategy=disable` 可避免突发流量冲击公共池导致抖动。 |
| **发现线上服务错误率从 0.02% 升至 0.5%，需快速定位是模型退化、输入脏数据还是网络问题** | ✅ Model Monitoring（开启推理日志 + 失败率告警） | 日志可查看具体失败请求的 input/output/error_code；结合 `protocol` 和 `sub_protocol` 字段区分 HTTP/SSE 异常；告警联动钉钉实现 5 分钟内响应。 |
| **同时使用 Qwen-Max（生产）和 CosyVoice（测试），需统一查看两个模型的月度 Token 消耗与成本分摊** | ✅ Model Monitoring（基础用量统计） | 全域模型用量聚合，支持按 `model` 和 `apikey_id` 多维筛选，30 天内数据实时可查，无需分别登录不同部署页面。 |
| **需要将百炼模型接入自建 Grafana 看板，展示 P95 延迟、TPM 使用率、缓存命中率趋势** | ✅ Model Monitoring（开通 Prometheus 指标） | 提供标准 OpenMetrics 接口，指标名语义清晰（如 `dashscope_model_latency_p95_seconds`, `dashscope_model_cache_hit_rate`），可无缝对接现有监控体系。 |

> ⚠️ **重要避坑提示**  
> - 不要将 **Model Monitoring 当作部署方案**：它不提供任何推理 endpoint，无法替代 `POST /api/v1/deployments`；  
> - 不要混用 **Model Deployment 1 的 MU 模式与 Model Production**：MU 是隔离资源单元，Production 仅支持 PTU；  
> - **LoRA 模型不能直接用于 Model Production**：Production 要求模型必须通过百炼微调训练作业生成，而非手动导入 LoRA 文件；  
> - **地域限制不可绕过**：Kimi-K2.6 仅北京可用、高级监控仅四地支持——选型时务必以实际地域为准，非文档“理论上支持”。

---

## 技术选型参考（面向开发者）

作为开发者，在技术栈设计阶段，请按以下流程决策：

1. **先确认模型来源**  
   → 若为 **LoRA 文件导入**：只能选 *Model Deployment 1*（Token 或 MU 模式）；  
   → 若为 **百炼微调训练产出** 或 **官方预置模型**：可进入下一步评估。

2. **再评估业务稳定性要求**  
   → 若 **无 SLA、无流量预测、无长期运维计划**：选 *Model Deployment 1*（PTU 快速起步，MU 保隔离）；  
   → 若 **要求可预测吞吐、支持自动扩缩容、需续订管理**：必须选 *Model Production*（它是 PTU 的增强生产版）；  
   → *Model Monitoring 是必选项，而非可选项*：无论选哪种部署，都应立即开通基础监控，并根据需要启用高级能力。

3. **最后检查地域与功能约束**  
   - 查阅 [模型支持列表](https://help.aliyun.com/zh/model-studio/models) 确认目标模型是否在所选地域支持；  
   - 若需日志审计，确认该模型是否在[支持列表](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中；  
   - 若用新加坡地域，避开 `kimi-k2.6`，并确认高级监控功能已开通。

✅ **最佳实践组合推荐**：  
`Model Production`（保障服务稳定性） + `Model Monitoring`（保障服务可视性） + `Model Deployment 1`（仅用于 LoRA 快速验证）  
——三者不是互斥选项，而是分层协作：Production 托管核心服务，Monitoring 提供洞察，Deployment 1 解决边缘需求。

> 💡 **一句话总结**：  
> **Deployment 1 是“怎么把模型跑起来”，Production 是“怎么让模型稳稳地跑下去”，Monitoring 是“怎么知道它跑得怎么样”。**  
> 三者共同构成百炼平台模型生产化的完整技术栈。

## 被对比主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model production](../api/model-production.md)
- [model monitoring](../guides/model-monitoring.md)


