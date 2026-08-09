# Token

Token 是百炼平台中用于计量模型输入与输出内容的基本单位，也是计费、限流、监控和资源调度的核心粒度。一个 Token 通常对应文本中的一个词元（如中文字符、英文子词或标点），在[多模态](multimodal.md)场景中则按统一规则折算为等效文本 Token 数（如图像、语音、视频的处理开销被映射为 Token 当量）。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费计量**：所有实时推理调用均按 `输入 Token 数 + 输出 Token 数` 分别计费，单价以“每百万 Token”为单位，阶梯价格由单次请求的输入 Token 总量决定；免费额度、资源包、节省计划均以 Token 为抵扣单位。
- **模型调用约束**：`max_tokens` 参数直接限制模型单次响应的最大输出 Token 数，必须 ≤ 模型文档声明的上限；超限将触发 `InvalidParameter` 错误。
- **监控与可观测性**：
  - **模型监控**：`model_usage` 指标统计各模型的 Token 消耗总量，支持按业务空间、API Key、协议等维度下钻分析；
  - **应用监控**：`LLM` 类节点明确上报 `input_tokens` 和 `output_tokens`，用于评估智能体/工作流中每个大模型调用的实际开销；`EMBEDDING` 节点仅统计输入 Token 数。
- **Token Plan 计量**：虽名义为“Token Plan”，但实际计费单位是 Credits —— 不同模型按其计算复杂度设定 Token-to-Credits 折算系数（如 `qwen3.7-max` 的 1000 Token 比 `qwen-plus` 消耗更多 Credits），Token 本身不直接交易，而是底层计量依据。
- **安全与限流**：内容安全策略、速率限制（Rate Limit）均基于 Token 级别触发（如 `error_type="rate_limit"` 指 Token 级配额超限），而非请求数。

## 关键参数和配置

- `max_tokens`：必填参数，指定模型最多生成的 Token 数，取值范围由具体模型决定（例如 `qwen3.8-max` 最高支持 8192），超出将报错。
- `input_tokens` / `output_tokens`：只读指标，由平台自动统计并暴露于监控日志与可观测链路中，开发者不可设置。
- Token 折算规则（[多模态](multimodal.md)）：
  - 图像：单张图片按分辨率和模型要求折算（如 `qwen-image-2.0` 默认按 1024×1024 基准折为约 1280 Token）；
  - 语音：ASR 输入音频按时长折算（如 `paraformer` 约 1 秒 ≈ 50 Token）；TTS 输出按文本长度计；
  - 视频：按帧率、时长及模型能力折算（如 `happyhorse-1.1-t2v` 每秒约 2000–5000 Token）；
  - 所有折算逻辑以[模型用量统计单位说明](https://help.aliyun.com/zh/model-studio/model-usage-statistics)为准，不透明但稳定。

## 面向开发者，简洁实用

- ✅ **务必校验 `max_tokens`**：调用前查阅目标模型文档的 `max_output_tokens` 上限，避免因超限导致失败。
- ✅ **监控 Token 消耗**：通过控制台「模型用量」或「应用观测」页面，按 `Request ID` 或 `Trace ID` 追踪单次调用的精确 `input_tokens`/`output_tokens`，快速定位高开销环节。
- ✅ **优化 Token 使用**：
  - 输入侧：精简 [prompt](../guides/prompt.md)，移除冗余上下文；对长文档优先用 `rerank` + `retriever` 缩减输入长度；
  - 输出侧：合理设置 `max_tokens`，避免盲目设高；结构化输出（如 JSON）通常比自由文本更紧凑。
- ❌ **不要假设 Token 数 = 字符数**：中文、标点、特殊符号、系统消息、工具调用参数均计入 Token，建议用 `dashscope.Tokenizer`（Python SDK）或在线 Token 计算器预估。
- ⚠️ **注意地域与模型快照绑定**：同一模型名（如 `qwen3.7-plus`）在不同地域或不同快照版本（如 `qwen3.7-plus-2026-05-26`）的 Token 折算和计费单价可能不同，务必使用精确模型 ID。

## 关联主题页

- [preparations](../api/preparations.md)
- [token plan guide](../guides/token-plan-guide.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [test 1](../guides/test-1.md)


