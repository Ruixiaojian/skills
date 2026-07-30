# Token

Token 是百炼平台中用于计量模型输入、输出及缓存内容的基本单位，是计费、限流、性能监控与资源调度的核心度量基准。一个 Token 通常对应文本中的一个子词（subword）或图像/语音等多模态数据经编码后的最小语义单元；其数量直接决定 API 调用的成本消耗、延迟表现与服务配额使用情况。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用（API/SDK/CLI）**：  
  `max_tokens` 参数明确限制模型单次响应的最大输出 Token 数；输入内容（如 [prompt](../guides/prompt.md)、system message、tool calls）和输出内容（response）均按实际编码后 Token 数计入用量。多模态输入（如图片 base64 编码、PDF 文本提取）也会被转换为 Token 并参与计费。

- **Token Plan 订阅服务**：  
  Credits 消耗以 Token 为基础动态计算，受模型类型（如 `qwen3.7-plus` vs `wan2.7-image`）、输入/输出长度、是否启用思考模式（`enable_thinking=true` 会额外增加推理 Token）、以及 Harness 工具调用（如 `web_search` 返回结果需编码为 Token）共同影响。个人版采用双窗口限额（5 小时 & 7 天），团队版按月度总 Token 预估 Credits 分配。

- **模型监控（Model Monitoring）**：  
  平台提供分钟级 Token 消耗明细（需开通高级监控），支持按 `model`、`workspace_id`、`apikey_id` 等维度聚合统计。关键指标包括：`input_tokens`、`output_tokens`、`cached_tokens`（前缀缓存节省量），可用于识别长上下文瓶颈或异常高 Token 请求。

- **应用监控（Application Monitoring）**：  
  在智能体/工作流链路中，每个 `LLM` 节点的 Token 用量统一定义为 `输入 Token 数 + 输出 Token 数`；`EMBEDDING` 节点仅统计向量化输入 Token；所有 Token 数据均支持按 Trace ID 关联、导出与评测集回流。

- **模型部署（Model Deployment）**：  
  - PTU 模式下，`input_tpm` / `output_tpm` 表示每分钟可处理的 Token 上限，支持前缀缓存折扣；  
  - MU 模式通过 `tpm_limit` 实施服务级 Token 吞吐限流；  
  - LoRA 模型按 Token 计费（`plan: "lora"`）时，费用 = 实际输入 Token × 输入单价 + 实际输出 Token × 输出单价。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `max_tokens` | 控制模型最大输出长度（Token 数） | 必须在模型文档指定范围内，超限将报错 `Range of max_tokens should be [1, xxx]` |
| `enable_thinking` | 启用思考模式（如 `qwen3-235b-a22b-thinking-2507`） | 开启后强制[流式输出](streaming-output.md)，且会显著增加中间推理 Token 消耗，不可与 `response_format={"type": "json_object"}` 共用 |
| `cache_prompt`（部分模型支持） | 启用前缀缓存，复用历史输入 Token | 仅 PTU 模式支持，可降低重复请求的 Token 成本与首 Token 延迟（TTFT） |
| `input_tokens` / `output_tokens`（监控字段） | 日志与监控中返回的实际 Token 数 | 推理日志需提前开通；未开通则无法获取单次明细，仅能查看小时级汇总 |

> ⚠️ 提示：Token 数量由百炼后端编码器精确计算，开发者无需自行估算。可通过开启[推理日志](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)在「日志」页签直接读取每次调用的 `input_tokens` 和 `output_tokens` 值，用于精准成本归因与性能调优。

## 面向开发者，简洁实用

- ✅ **调试建议**：首次集成时，务必开启推理日志并观察单次调用的 Token 明细，避免因 [prompt](../guides/prompt.md) 过长或工具返回冗余内容导致意外超支。  
- ✅ **成本优化**：对长文档处理任务，优先选用支持 256K 上下文的 PTU 模型，并启用 `cache_prompt`；对短对话场景，选择 `qwen3.6-flash` 等轻量模型可显著降低 Token 单价。  
- ✅ **限流应对**：若遇到 `429 Too Many Requests`，检查 `tpm_limit` 或 Token Plan 窗口限额是否触顶；可通过 `workspace_id` 隔离不同业务线用量。  
- ❌ **避免误区**：`max_tokens` 不控制输入长度，输入 Token 超限将直接报错（如 `qwen-long` 单文件 ≤ 150 MB / ≤ 1500 page）；Token Plan 的 `sk-sp-xxx` Key 不能用于普通 DashScope API（`sk-ws-xxx`），反之亦然。

## 关联主题页

- [preparations](../api/preparations.md)
- [token plan guide](../guides/token-plan-guide.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [model deployment 1](../guides/model-deployment-1.md)


