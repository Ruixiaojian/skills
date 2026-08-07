# Token

Token 是百炼平台中用于计量模型输入与输出内容的基本单位，也是计费、配额、性能监控和资源调度的核心度量基准。一个 Token 通常对应文本中的一个词元（如中文字符、英文子词或标点），其具体切分方式由所调用模型的 tokenizer 决定；对于[多模态](multi-modal.md)模型，Token 还可扩展涵盖图像 patch、音频帧等结构化单元。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与额度管理**：所有实时推理调用均以 `输入 Token + 输出 Token` 为计费基础。免费额度（如 100 万 Token/模型）、资源包、节省计划及按量付费均按 Token 数量结算；Batch 调用单价为实时推理的 50%，但同样以总 Token 量计费。
- **模型调用控制**：`max_tokens` 参数限制单次响应的最大输出 Token 数；`budgetTokens`（如 OpenCode 思维链模式）用于硬性约束推理过程中的中间 Token 消耗，防止失控生成。
- **性能监控**：高级监控指标如 `model_generation_duration_per_token`（每 Token 生成耗时）、`model_tps_per_request`（每秒输出 Token 数）直接反映模型吞吐效率；应用观测中 `LLM` 节点的 Token 总量 = 输入 Token + 输出 Token，用于归因成本与延迟。
- **配额与限流**：Coding Plan 虽以“请求次数”为额度单位，但实际限流底层仍依赖 Token 级统计（如单次请求 Token 超限将触发 `429` 错误）；TPM（Tokens Per Minute）是部署级（PTU）和 API 级限流的关键阈值。
- **[多模态](multi-modal.md)扩展**：全模态模型（如 `qwen3.5-omni-plus`）对图像、视频等输入会自动编码为视觉 Token，并与文本 Token 统一参与计费与长度校验（如 `messages.content` 中 `image_url` 的解析开销计入输入 Token）。

## 关键参数和配置

- `max_tokens`：必需参数，指定最大输出 Token 数，不得超过模型能力上限（如 `qwen3.7-max` 为 8192）；设为 `0` 将导致调用失败。
- `budgetTokens`（仅限 Thinking 模式）：用于限制思维链推理过程中的中间 Token 总量，需显式设置且必须 ≤ 模型支持的最大思考长度。
- `stream` 与 `incremental_output`：启用流式响应时，Token 以增量方式返回；`incremental_output=True` 可避免重复传输历史内容，降低网络开销与客户端处理负担。
- 计费粒度：Token 计量精确到个位，输入/输出 Token 分别统计、共用免费额度；阶梯计费模型（如 `qwen3-max`）按单次请求**输入 Token 总量**分档，整次请求按最高档单价结算。

## 面向开发者，简洁实用

- ✅ **务必校验 Token 消耗**：使用 `bailian-cli` 或 SDK 的 `get_usage()` 方法获取实际消耗；调试阶段开启 `enable_thinking` 时，需预留额外 `budgetTokens`。
- ✅ **规避隐式超限**：[多模态](multi-modal.md)输入（如长图、高清视频）会显著增加 Token 数，建议先用 `text-embedding-v2` 或预处理工具估算输入规模。
- ✅ **监控与告警联动**：在模型监控中配置 `model_usage` 告警（如单日 Token 超 80% 免费额度），及时发现异常调用。
- ❌ **不要假设 Token 等价于字符数**：中文平均约 1 字 ≈ 1 Token，但含标点、空格、特殊符号或英文子词时差异显著；使用 `dashscope.Tokenizer` 或官方 tokenizer 工具精确测算。
- ❌ **不要混用 Key 类型**：Token Plan Key（`sk-sp-`）与 Coding Plan Key（同前缀但不同域名）不可互通，否则将因认证失败或计费错位导致 `401`/`403` 错误。

## 关联主题页

- [test 1](../guides/test-1.md)
- [token plan guide](../guides/token-plan-guide.md)
- [preparations](../api/preparations.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [application support](../guides/application-support.md)


