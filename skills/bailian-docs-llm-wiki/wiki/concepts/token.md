# Token

Token 是百炼平台中用于计量模型计算资源消耗的核心计费与性能观测单位，代表模型处理文本、图像、语音、视频等多模态内容时所消耗的基础计算粒度。在百炼体系中，Token 不仅是费用结算的最小单元，也是监控延迟、评估质量、优化成本的关键可观测指标。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与额度管理**：所有模型调用（含输入和输出）均按实际消耗的 Token 总量计费或抵扣。免费额度（100 万 Token）、Token Plan 的 Credits、节省计划与资源包，均以 Token 为统一计量基准；输入 Token 与输出 Token 合并计入总额度，不区分类型或方向。
  
- **模型监控**：在「模型监控」中，`TPM`（Tokens Per Minute）、`TTFT`（Time to First Token）、`ITL`（Inter-Token Latency）等核心指标均以 Token 为锚点；Token 消耗可按模型、业务空间、API Key 等维度聚合分析，用于识别高成本请求或异常调用模式。

- **应用监控**：在「应用监控」中，每个 `LLM` 节点自动上报 `input_tokens` 和 `output_tokens`，总和即为该次模型调用的 Token 用量；`EMBEDDING` 节点则上报向量化输入的 Token 数，支撑 RAG 链路的成本归因与性能诊断。

- **应用评测**：当使用 LLM 评估器（如 `qwen-plus`）进行自动评分时，评估过程本身会产生额外 Token 消耗，该部分费用独立计费，需在评测任务配置中明确评估模型并预留额度。

- **多模态与工具调用**：图像/视频/语音类模型的 Token 计算已内建适配（如 `qwen-image-2.0-pro` 按视觉 tokenization 规则折算），无需开发者手动转换；Harness 工具调用（联网搜索、代码解释器等）的 Token 消耗包含工具执行上下文开销，且**仅通过 Responses API 调用才纳入 Token Plan Credits 抵扣**。

## 关键参数和配置

- **`max_tokens`**：请求级关键参数，控制模型最大输出长度，直接影响 Token 消耗上限与响应成本。建议根据实际需求合理设置，避免过度预留导致浪费。
  
- **地域约束**：Token 相关计费与监控能力（如分钟级日志、高级监控）当前仅在北京、新加坡、弗吉尼亚地域完全可用；华北2（北京）是免费额度、Token Plan 及多数多模态模型的默认支持地域。

- **API Key 类型决定 Token 归属**：
  - 通用 `sk-xxx` Key：可消耗免费额度及按量付费；
  - Token Plan `sk-sp-xxx` Key：仅抵扣 Credits，**不触发免费额度**；
  - Coding Plan `sk-ws-xxx` Key：不兼容 Token Plan，误用将导致按量扣费。

- **Token 统计口径**：
  - 输入 Token：原始 [prompt](../guides/prompt.md) + system message + history + 多模态输入（如 base64 图片经视觉 tokenizer 编码后的 token 数）；
  - 输出 Token：模型实际生成的全部 tokens（含流式响应中的每个 chunk）；
  - 不计入：HTTP headers、metadata、非模型节点（如 `RETRIEVER`、`RERANKER`）的文本切片本身不产 Token，但其结果作为 LLM 输入后会参与计费。

## 面向开发者，简洁实用

- ✅ **查用量**：控制台 →「模型监控」→「调用统计」页签，筛选时间范围与 API Key，查看实时 Token 消耗趋势；分钟级数据延迟约 2–5 分钟。
  
- ✅ **省成本**：优先启用「免费额度用完即停」开关；对稳定流量使用 AI 通用型节省计划（最高 5.3 折）；高频调用单模型可购资源包；团队协作推荐 Token Plan（统一额度、免密钥管理）。

- ✅ **避踩坑**：
  - 多模态模型（图像/视频/语音）**不可直接用 Chat Completions 接口调用**，必须通过 Skill / Slash Command / Agent 扩展机制接入；
  - Harness 工具若未使用 Responses API，工具调用无效且按量计费；
  - 免费额度不覆盖 Batch 调用、模型训练、部署、ASR 权限未开通等场景。

- ✅ **调试建议**：开启「推理日志」后，可在模型监控 →「日志」页签查看每次调用的精确 input/output token 数（需模型支持），快速定位高 Token 请求原因（如过长 [prompt](../guides/prompt.md)、冗余 history、未设 `max_tokens`）。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)
- [test 1](../guides/test-1.md)
- [application evaluation](../guides/application-evaluation.md)


