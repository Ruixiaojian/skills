# Token

Token 是百炼平台中用于计量大模型调用资源消耗的核心单位，代表模型处理文本、图像、语音等输入输出内容时的最小语义单元（如子词、字节对或视觉 patch）。所有模型调用的计费、配额控制、性能监控与资源调度均以 Token 用量为统一基准。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与配额**：Token Plan 服务以 Credits 为账户单位，实际消耗按模型类型 × 输入 Token 数 × 输出 Token 数 × 动态系数（含思考模式、工具调用、缓存命中等）实时折算。个人版采用 5 小时/7 天双窗口限额，团队版采用月度总额度制，额度均以 Token 消耗量为底层依据。
  
- **可观测性监控**：
  - *模型监控* 中，`prompt_tokens`、`completion_tokens`、`total_tokens` 字段精确记录单次请求的 Token 用量，并支撑 TPM（Tokens Per Minute）、首 Token 延时（TTFT）、非首 Token 延时（ITL）等关键性能指标计算；
  - *应用监控* 中，LLM 节点自动统计 `input_tokens` 和 `output_tokens`，支持按 Token 量筛选异常 Span（如“输出 Token 突增”），并可导出用于成本归因与提示工程优化。

- **推理加速控制**：
  - TPM 预留能力以 kTPM（千 Token/分钟）为容量单位，直接绑定 Token 吞吐能力；
  - 快速模式虽不改变 Token 计数逻辑，但通过优化调度显著降低单位 Token 的响应延迟；其返回结构中 `usage.completion_tokens_details.reasoning_tokens` 显式分离思考 Token，确保计费透明。

- **[多模态](multi-modal.md)与工具调用**：
  - 图像生成（wan2.7-image）、视频生成（happyhorse-1.1-t2v）、语音合成（qwen-audio-3.0-tts-plus）等模型的 Token 用量由对应[多模态](multi-modal.md) tokenizer 统一计算，计入总 Credits 消耗；
  - Harness 工具（如 `web_search`、`code_interpreter`）调用按成功次数抵扣 Credits，但其触发的后续模型调用仍按实际 Token 用量二次计费。

## 关键参数和配置

| 参数 | 说明 | 开发者须知 |
|------|------|------------|
| `usage.prompt_tokens` | 输入 Token 数量（含系统提示、用户消息、历史对话等） | 所有模型均返回；长上下文输入可能触发阶梯系数（如 GLM-5.1 在 32K–200K 区间系数为 1.33） |
| `usage.completion_tokens` | 输出 Token 数量（含流式响应中所有 chunk） | 流式调用需累加各 chunk 的 `completion_tokens` 得到总量 |
| `usage.total_tokens` | `prompt_tokens + completion_tokens` | 计费主依据；部分模型（如快速模式 `glm-5.2-fast-preview`）额外返回 `reasoning_tokens` 字段 |
| `usage.prompt_tokens_details.cached_tokens` | 缓存命中 Token 数（如 GLM-5.2 缓存命中部分按 25% 折算） | 仅在支持缓存的模型/配置下返回，直接影响 Credits 扣减 |
| `model` 参数值 | 决定 Token 计算规则与单价（如 `qwen3.7-plus` vs `glm-5.2-fast-preview`） | 更换 model 即切换计费模型，需同步确认其 Token 定价与能力边界 |

> ⚠️ 注意：Token 统计始终基于模型原生 tokenizer（如 Qwen 使用 tiktoken-qwen，GLM 使用 glm-tokenizer），不接受自定义分词器；[多模态](multi-modal.md)模型的 Token 定义由平台封装，开发者无需手动 tokenize。

## 面向开发者，简洁实用

- **查用量**：在控制台「模型监控」→「调用记录」或「应用监控」→「Span 详情」中直接查看每次请求的 `usage` 对象；
- **控成本**：通过 `usage` 字段实时判断是否触发长输入阶梯、缓存优惠或工具调用溢出，结合告警规则（如“单次 total_tokens > 10000”）主动干预；
- **调性能**：将 `prompt_tokens` 与 TTFT 关联分析，识别提示长度对首 Token 延迟的影响；用 `completion_tokens` 与 ITL 对比，评估流式吞吐瓶颈；
- **避陷阱**：Token Plan 的 API Key（`sk-sp-xxx`）与 Base URL（`token-plan.cn-beijing.maas.aliyuncs.com`）必须配套使用，混用通用 Key 或地域错误会导致 401/404 错误；
- **验结果**：多模态生成不可直连 [OpenAI 兼容接口](openai-compatible-interface.md)，必须通过 Slash Command/Skill/Agent 封装调用——此时 Token 用量由封装层统一上报，而非原始模型 API 返回。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


