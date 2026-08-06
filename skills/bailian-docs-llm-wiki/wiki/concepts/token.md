# Token

Token 是百炼平台中用于计量模型推理资源消耗的最小计费与调度单位，代表模型处理的一段文本、图像、语音或视频内容的基本语义单元。在 API 调用中，Token 既用于精确统计输入（[prompt](../guides/prompt.md)）与输出（completion）的计算量，也是配额控制、成本核算、性能监控和容量预留的核心度量基准。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与配额管理**：所有按量付费模型（包括 `test 1` 场景）以 Token 为基本计费单位，输入 Token 与输出 Token 分开统计、独立计价；免费额度、资源包、节省计划均以「万 Token」或「百万 Token」为单位发放与抵扣。
- **Token Plan 订阅服务**：虽统一以 Credits 计量，但 Credits 的实际扣减完全由 Token 消耗驱动——系统根据模型单价、输入/输出/缓存 Token 数、思考模式启用状态、Harness 工具调用次数等动态换算，无固定 Token/Credit 比例。
- **高吞吐部署（PTU / TPM 预留）**：Token 是容量保障的物理基础——`input_tpm` 和 `output_tpm` 单位均为「千 Token/分钟」（KTPM），长输入需经阶梯系数折算，前缀缓存命中则按折扣系数（如 0.2）折减实际 Token 消耗。
- **模型监控与可观测性**：`model_usage` 等核心 Prometheus 指标直接以 Token 总用量为数值，日志详情页明确展示每次调用的 `input_tokens`、`output_tokens` 及 `cached_tokens`，支撑精细化成本归因与性能分析。
- **API 调用约束**：`max_tokens` 参数严格限制输出长度上限（单位：Token），`messages` 内容经 tokenizer 编码后生成的实际 Token 数决定请求是否超限；[多模态](multimodal.md)输入（如 `image_url`）也会被模型内部转换为等效 Token 序列参与计数。
- **快速模式（Fast mode）与特殊能力**：即使采用 TPS 优化路径（如 `glm-5.2-fast-preview`），底层仍以 Token 为调度粒度，响应中 `reasoning_content` 等结构化字段的生成亦计入输出 Token 总量。

## 关键参数和配置

- `max_tokens`：必填整数，指定模型最多生成的 Token 数，取值范围为 `[1, 模型最大输出 Token 数]`，超出将返回 400 错误。
- `input_tokens` / `output_tokens`：API 响应体中返回的只读字段，分别表示本次请求实际消耗的输入与输出 Token 数（含系统提示词、工具描述等隐式内容）。
- `cached_tokens`：仅 PTU/TPM 场景返回，表示本次请求中被前缀缓存命中的 Token 数，按折扣系数折减额度消耗。
- `enable_thinking`：开启时强制流式响应，且所有 Token 消耗计入 `output_tokens`，不支持 `response_format="json_object"`。
- 缓存折扣系数：由模型决定（如 `glm-5.1` 为 0.2），影响 PTU 实际消耗，需在部署前确认。
- 阶梯系数：针对长输入（>32K），超出部分按模型档位加权折算 TPM 消耗（如 `glm-5.1` 超出部分系数为 1.33），非线性叠加。

## 面向开发者，简洁实用

- ✅ **始终校验响应中的 `usage` 字段**：`input_tokens` + `output_tokens` = 实际计费 Token 总量；`cached_tokens > 0` 表示缓存生效，成本已优化。
- ✅ **估算用量优先用控制台工具**：PTU 部署页的「预置吞吐额度计算器」、Token Plan 的「Credits 预估器」均基于真实 Token 换算逻辑，比人工估算更可靠。
- ✅ **调试时开启日志监控**：在「模型监控 → 日志」页查看原始请求/响应及 Token 统计，快速定位超额、缓存未命中或提示词膨胀问题。
- ❌ **勿假设 Token 数 = 字符数或单词数**：中文、emoji、[多模态](multimodal.md)内容、特殊符号均影响 tokenizer 结果；使用 `dashscope.Tokenizer.count_tokens()`（Python）或 CLI `bl token count` 进行本地预估。
- ❌ **勿混用 Key 与 Base URL**：Token Plan 专属 Key（`sk-sp-`）必须搭配其 Base URL 使用，否则 Token 将按通用计费规则扣除，导致额度误用。
- ⚠️ **注意地域与模型绑定**：免费额度仅在北京地域生效；同一模型不同快照版本（如 `qwen3.7-plus` 与 `qwen3.7-plus-2026-05-26`）Token 额度完全隔离，不可互通。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [test 1](../guides/test-1.md)
- [preparations](../api/preparations.md)
- [model monitoring](../guides/model-monitoring.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model deployment 1](../guides/model-deployment-1.md)


