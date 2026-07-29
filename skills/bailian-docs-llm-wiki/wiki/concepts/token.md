# Token

Token 是百炼平台中用于计量大模型输入与输出文本长度的基本单位，也是计费、配额控制和性能监控的核心度量基准。一个 Token 通常对应一个子词（subword）或标点符号，在中文场景下平均约等于 1.5–2 个汉字，英文场景下约等于 1 个单词或常见标点；多模态任务中，图像、音频等非文本输入也会被编码为等效 Token 数参与统一计量。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与配额**：Token 是 Token Plan 订阅服务的底层计量单位，所有调用（含文本生成、视觉理解、图片/视频生成、语音合成）均按 `输入 Token 数 + 输出 Token 数` 抵扣 Credits；Harness 工具（如 `web_search`）虽按次计费，但其触发的模型推理仍计入 Token 消耗。  
- **模型监控**：`max_tokens` 是关键请求参数，显式限制输出长度，直接影响 Token 消耗与费用；监控系统以 `input_tokens` 和 `output_tokens` 字段统计每条请求的实际用量，支持按模型、API Key、时间范围聚合分析。  
- **应用监控**：在智能体/工作流调用链中，每个 `LLM` 节点的 Span 明细均展示 `input_tokens + output_tokens` 总量，Embedding 节点则按输入文本长度量化 Token 量，用于定位高消耗环节。  
- **模型评测**：被评测模型的每次推理产生 Token 消耗，计入推理费用；若使用大模型评估维度，裁判模型的评分过程同样产生独立 Token 费用，需在成本预算中一并考虑。  
- **高性能推理**：TPM 预留（Token Per Minute Reservation）直接以 kTPM（千 Token/分钟）为单位预购吞吐能力；快速模式（Fast Mode）的 TPS（Token Per Second）指标也基于 Token 流量定义，用于衡量响应实时性。

## 关键参数和配置

- `max_tokens`：必设推荐参数，用于硬性截断输出长度，避免意外长输出导致高额 Token 消耗。建议根据业务预期设置合理上限（如问答类设为 1024，摘要类设为 512）。  
- `input_tokens` / `output_tokens`：监控与日志中的只读字段，分别表示本次请求实际消耗的输入/输出 Token 数，可用于成本归因与优化分析。  
- TPM 预留配置：需按模型粒度分别设置 `input_tpm` 和 `output_tpm`（单位：kTPM），二者独立生效，且受输入长度阶梯系数影响（如长文本输入可能按 1.33 倍折算容量）。  
- 多模态 Token 计算：图像输入按分辨率和编码方式折算（如 `qwen3.7-plus` 视觉理解中，1024×1024 图片 ≈ 1280 Tokens），具体换算规则见各模型文档，无需开发者手动计算，平台自动完成。

## 面向开发者，简洁实用

- ✅ **务必设置 `max_tokens`**：防止失控输出，是控制成本最直接有效的手段。  
- ✅ **用监控查真实用量**：模型用量页（小时级延迟）和应用监控 Span 详情（分钟级）均可查看精确 Token 消耗，优先排查 `output_tokens` 异常偏高的请求。  
- ✅ **Token Plan 用户注意**：API Key 为 `sk-sp-xxxxx` 格式，Base URL 必须匹配地域（仅华北2可用），混用通用 Key 或错误域名将导致鉴权失败或按量扣费。  
- ⚠️ **避免隐式 Token 浪费**：流式响应中重复发送相同内容、Prompt 中冗余说明、未清理历史对话上下文，均会增加 `input_tokens`；启用 Harness 工具时，模型自动补全的搜索/执行步骤也计入 Token。  
- 📉 **优化建议**：对固定模板类任务，优先用规则评估替代大模型评估；批量推理前先用小样本验证 `max_tokens` 设置；视觉理解任务显式声明 `"modalities": {"input": ["text", "image"]}`，否则图片不参与 Token 计算但请求失败。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


