# Token 计量与管理

Token 计量与管理是百炼平台对大模型调用资源消耗进行标准化度量、实时追踪、精准计费与精细化治理的核心机制。它以 **Token** 为最小计量单元，覆盖输入、输出、缓存等全链路消耗，并统一映射到 Credits（Token Plan）或按量账单（Pay-as-you-go），支撑成本控制、用量分析与性能优化。

## 在百炼平台的不同场景中，这个概念如何使用

- **Token Plan 订阅服务**：以 Credits 为计费单位，按实际消耗的 `input_tokens`、`output_tokens` 和 `cache_tokens` 动态抵扣；模型白名单严格限定可计量范围，非白名单模型调用不计入 Credits，可能触发按量扣费。
- **模型监控（Model Monitoring）**：提供分钟级/小时级 `model_usage` 指标（含 `input_tokens`/`output_tokens`/`total_tokens` 等 `usage_type` 维度），支持按 `model`、`apikey_id`、`workspace_id` 等标签过滤，用于成本归因与异常排查（北京地域支持单次请求级 Token 查看）。
- **应用观测（Application Monitoring）**：在 Span 级别精确统计 `Input Tokens` 与 `Output Tokens`，关联至具体节点（如 `LLM`、`EMBEDDING`），支持按链路深度、节点类型、状态筛选，是智能体/工作流成本拆解与性能瓶颈定位的关键依据。
- **模型评测（Model Evaluation）**：评测任务执行时，被评测模型推理和裁判模型评分均产生 Token 消耗——前者计入被评测模型用量，后者计入裁判模型用量，二者独立计量、分别计费。
- **应用支持（Application Support）**：插件调用、RAG 检索、[流式输出](streaming-output.md)等能力本身不额外计 Token，但其触发的模型调用（如 LLM 生成响应、Embedding 向量化）仍遵循标准 Token 计量规则；`incremental_output=True` 不改变总 Token 数，仅影响传输方式。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `input_tokens` | 模型接收到的 Prompt、上下文、工具描述、图片 Base64 编码等输入内容所占 Token 数 | 图片按分辨率折算（如 `qwen-image-2.0` 使用固定 token 开销 + 可变视觉 token）；系统自动去除冗余空格与换行，但不压缩语义 |
| `output_tokens` | 模型实际生成的文本或结构化响应（含 function call 参数）所占 Token 数 | 流式响应中累计计数，`incremental_output` 不影响总量；截断（`max_tokens`）会限制此值上限 |
| `cache_tokens` | 模型缓存 Prompt 或历史对话产生的额外开销（如 KV Cache 预分配） | 当前仅部分模型（如 `qwen3.7-plus`）在启用缓存优化时显式计量，多数场景隐含在 `input_tokens` 中 |
| `total_tokens` | `input_tokens + output_tokens`（缓存通常不单独计入） | 计费与监控口径统一以此为准 |
| `usage_type` | Prometheus 指标 `model_usage` 的关键 label | 必须显式指定 `input_tokens`/`output_tokens`/`total_tokens` 才能正确聚合 |

> ⚠️ 重要约束：  
> - Token 计量基于模型实际 tokenizer 行为，**不接受客户端预估**；开发者不可自行计算并传入 `token_count` 参数。  
> - 所有计量均发生在服务端，调用返回的 `usage` 字段（如 OpenAI 兼容 API 中的 `"usage": {"prompt_tokens": ..., "completion_tokens": ...}`）为唯一可信来源。  
> - 图像生成（`multimodal-generation` API）与视觉理解（多模态输入）的 Token 计算逻辑与纯文本模型不同，需查阅对应模型文档确认细则。

## 面向开发者，简洁实用

- ✅ **必查返回值**：每次成功调用后，务必解析响应中的 `usage` 字段，用于本地日志记录、预算预警或用量上报。  
- ✅ **善用监控工具**：在北京地域部署关键应用时，开启模型监控的「高级监控」并配置告警，当 `model_usage{usage_type="total_tokens"}` 异常飙升时快速定位问题模型或恶意请求。  
- ✅ **成本优化实践**：  
  - 对长上下文场景，优先启用 `cache_tokens` 支持的模型（查看模型文档支持列表）；  
  - 评测任务中，用规则评估替代大模型评估可规避裁判模型 Token 费用；  
  - Token Plan 用户应定期检查控制台「用量分析」，识别高消耗模型/成员，及时调整分配策略。  
- ❌ **避免踩坑**：  
  - 不要复用通用 API Key（`sk-`）调用 Token Plan 模型——将导致 401 错误或意外按量扣费；  
  - 不要尝试通过修改 `max_tokens` 或 [prompt](../guides/prompt.md) 格式“欺骗”Token 计量——平台按真实 tokenizer 输出计费；  
  - 不要依赖前端渲染逻辑（如 Markdown 解析）估算 Token——实际消耗由模型侧 tokenizer 决定。  

Token 计量是百炼平台资源治理的基石。理解它，就是掌握成本、性能与合规的主动权。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)
- [application support](../guides/application-support.md)


