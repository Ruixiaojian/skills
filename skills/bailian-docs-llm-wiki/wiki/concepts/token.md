# Token

Token 是百炼平台中用于计量模型输入、输出及中间计算过程的基本单位，是计费、配额、性能监控与资源调度的核心度量基准。它由模型 tokenizer 对原始文本、图像、音频等[多模态](multi-modal.md)内容进行分词（tokenization）后生成的离散单元构成，其数量直接反映模型处理的数据规模和计算负载。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与用量管理**：所有按量调用（包括 Token Plan、模型部署中的 LoRA 按 Token 计费、TPM 预留/快速模式的缓存折算）均以 Token 为最小计费单元。实际消耗 = `prompt_tokens` + `completion_tokens`（含 `reasoning_tokens` 等细分项），并受长输入阶梯系数、缓存命中折扣（如 GLM-5.2 缓存命中按 25% 折算）等规则影响。
  
- **资源配额控制**：Token Plan 的限额（个人版双窗口制、团队版月度制）、TPM 预留（kTPM = 1000 tokens/分钟）、PTU 部署（`input_tpm`/`output_tpm`）均以 Token 为容量单位；并发能力（如 Agent 数量）和 RPM/TPM 限流也间接依赖 Token 吞吐量约束。

- **性能监控与可观测性**：模型监控（`model_usage` 指标）、应用观测（LLM Span 中的 `input_tokens`/`output_tokens`）均实时上报 Token 用量，并支持按 Token 维度分析成本、延时（如首 Token 耗时）、失败率等关键 SLA 指标。

- **[多模态](multi-modal.md)与工具调用**：图像/视频/语音生成模型、Harness 工具（`web_search`、`code_interpreter` 等）虽不直接暴露 Token 接口，但其调用仍按成功次数或等效 Token 量折算 Credits；视觉理解能力是否原生支持，亦取决于模型对图像 token 的编码能力。

- **协议兼容性**：OpenAI/Anthropic 兼容接口返回的 `usage` 字段（`prompt_tokens`, `completion_tokens`, `total_tokens`）与百炼内部统计严格一致，开发者可直接复用标准 SDK 解析。

## 关键参数和配置

- **`usage` 响应字段**（必读）：
  - `prompt_tokens`：输入 [prompt](../guides/prompt.md) 的 token 数（含 system/user/assistant message 及工具描述）
  - `completion_tokens`：模型生成的输出 token 数
  - `total_tokens`：`prompt_tokens + completion_tokens`
  - `completion_tokens_details.reasoning_tokens`（仅快速模式）：思考阶段 token，计入总输出计费
  - `prompt_tokens_details.cached_tokens`（TPM/PTU/快速模式）：缓存命中 token 数，按折扣系数折算用量

- **长输入阶梯系数**（PTU/TPM 场景）：当 `prompt_tokens` 超过基础阈值（如 GLM-5.1 在 32K–200K 区间），输入 token 按系数（如 1.33）放大计费，需在创建实例时确认支持范围。

- **地域约束**：Token Plan 仅限华北2（北京）；高级监控（含精确 Token 日志）仅支持北京、新加坡、弗吉尼亚；模型部署 API 仅支持北京。

- **API Key 隔离**：Token Plan 使用 `sk-sp-` 开头的专属 Key，与通用 `sk-` Key 完全隔离，不可混用。

## 面向开发者，简洁实用

- ✅ **计费验证**：始终检查响应 `usage` 字段，而非自行估算；控制台用量明细为准，尤其注意缓存、阶梯、工具调用等折算逻辑。  
- ✅ **性能优化**：减少冗余 [prompt](../guides/prompt.md)、启用前缀缓存（PTU）、选择 `fast-preview` 模型可降低首 Token 延时与单位 Token 成本。  
- ✅ **监控定位**：在应用观测中筛选 `Token 总量 > 10000` 或 `首 Token 耗时 > 2000ms`，快速识别低效调用链路。  
- ⚠️ **避免陷阱**：  
  - 不要假设 `model` 名称隐含 Token 规则（如 `qwen3.7-plus` 无默认阶梯，`glm-5.2-fast-preview` 不支持 TPM）；  
  - 不要跨地域复用 Token Plan Key 或监控配置；  
  - LoRA 模型部署后无法切换为 PTU/MU，需重部署。  
- 📌 **调试建议**：开启推理日志（模型监控）或应用观测，直接查看原始 `prompt_tokens`/`completion_tokens`，比估算更可靠。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)


