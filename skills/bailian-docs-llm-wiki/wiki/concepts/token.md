# Token

Token 是百炼平台中用于计量模型输入、输出及内部计算资源消耗的最小语义单位，由模型 tokenizer 对原始文本、图像、语音等[多模态](multi-modal.md)内容进行分词/编码后生成。它是平台计费、配额控制、性能监控与资源调度的核心基础单元，所有模型调用（含推理、工具调用、[多模态](multi-modal.md)生成）均以 Token 用量为依据进行 Credits 扣减或资源占用核算。

## 在百炼平台的不同场景中，这个概念如何使用

- **Token Plan 订阅服务**：Token 是 Credits 消耗的基本粒度。实际扣费 = `input_tokens × 输入单价 + output_tokens × 输出单价 + 工具调用附加费用`；不同模型（如 `qwen3.8-max-preview` vs `wan2.7-image`）、不同模式（标准/思考/缓存命中）对应不同单价，且[多模态](multi-modal.md)模型（图像/视频/语音）需通过 Skill/Agent 独立接口调用，其 Token 计算逻辑与文本模型独立。
  
- **高吞吐推理（TPM 预留 / 快速模式）**：Token 直接决定容量单位（kTPM = 1000 tokens/分钟）。TPM 预留按输入/输出 Token 分别配额；快速模式虽无显式 TPM 配额，但受全局 TPM 排队约束，且返回结构中 `usage.completion_tokens_details.reasoning_tokens` 显式分离“思考 Token”，全部计入总输出 Token 计费。

- **模型部署（PTU / MU / LoRA）**：  
  - PTU 模式下，`ptu_capacity.input_tpm/output_tpm` 以 Token/分钟为单位定义专属吞吐；长输入（如 >32K）可能触发阶梯系数（如 ×1.33），影响实际 Token 消耗核算；  
  - MU 模式支持 `enable_thinking`，启用后模型内部推理过程产生的中间 Token（如思维链）同样计入 `output_tokens`；  
  - LoRA 微调模型仅支持按 Token 用量计费，不支持 PTU/MU 的性能配置能力。

- **监控与可观测性**：  
  - 模型监控中，`prompt_tokens`、`completion_tokens`、`cached_tokens` 等字段在单次请求日志中精确回传，是成本分析与性能归因的关键依据；  
  - 应用观测中，每个 `LLM` Span 的 `token_count` = `input_tokens + output_tokens`，支持按节点、按 Trace 维度聚合分析 Token 分布，辅助优化提示工程与 Agent 设计。

## 关键参数和配置

- **Token 计算来源**：严格依赖所调用模型自身的 tokenizer（如 Qwen 使用 `QwenTokenizer`，GLM 使用 `GLMTokenizer`），不同模型对同一输入的 Token 数可能差异显著。开发者应通过 `usage` 字段获取实际值，不可自行估算。

- **缓存相关字段**（若支持）：
  - `usage.prompt_tokens_details.cached_tokens`：命中前缀缓存的输入 Token 数，按折扣价计费（如 GLM-5.2 缓存命中部分按 25% 折算）；
  - `usage.completion_tokens_details.cached_tokens`：暂未开放，当前仅输入侧支持缓存计量。

- **思考 Token 显式暴露**（仅限支持思考模式的模型）：
  - `usage.completion_tokens_details.reasoning_tokens`：模型内部推理步骤产生的 Token，计入总 `completion_tokens`，不可减免；
  - `usage.completion_tokens_details.generated_tokens`：最终返回给用户的 Token 数，二者之和等于 `completion_tokens`。

- **长输入阶梯系数**（PTU/高并发场景）：当 `prompt_tokens` 超出基础区间（如 32K），平台按预设系数放大计费 Token 数（如 `32K–200K` 区间系数为 1.33），具体阈值与系数见各模型文档。

## 面向开发者，简洁实用

- ✅ **必查字段**：每次成功调用后，务必解析响应中的 `usage` 对象，提取 `prompt_tokens`、`completion_tokens` 及细分字段（如 `cached_tokens`、`reasoning_tokens`），用于成本核对与异常诊断。

- ✅ **避免估算**：不要基于字符数或单词数粗略换算 Token —— 使用 `dashscope.Tokenizer` SDK 或调用 `/v1/tokenize` 接口（支持主流模型）获取准确值。

- ✅ **监控对齐**：若发现控制台用量统计与 API 返回 `usage` 不一致，优先检查是否开通「推理日志」（模型监控）或「应用观测」（应用监控）—— 未开通时，控制台仅显示小时级聚合数据，存在 1–2 小时延迟。

- ⚠️ **地域约束牢记**：Token Plan 专属 API Key（`sk-sp-`）仅在华北2（北京）生效；TPM 预留与快速模式支持北京/新加坡双地域；而推理日志与高级监控能力仅在北京/新加坡/弗吉尼亚可用。

- ⚠️ **计费不可逆**：Token 消耗实时发生，无退款机制。高频调用前建议先用小样本验证 Token 用量，尤其注意多模态输入（如 Base64 图片）和思考模式带来的隐性开销。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)


