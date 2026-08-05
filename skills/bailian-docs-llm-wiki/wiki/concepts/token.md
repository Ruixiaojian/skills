# Token

Token 是百炼平台中用于计量模型输入与输出内容的基本单位，也是计费、限流和资源调度的核心粒度。一个 Token 通常对应一个子词（subword）或字符（如中文单字、英文单词/标点），其具体切分方式由底层模型的 tokenizer 决定；对开发者而言，Token 是可感知、可测量、可配置的最小计算资源单元。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费计量**：所有按量付费、Token Plan、TPM 预留、PTU/MU 部署等计费模式均以 Token 为基本单位。例如：
  - `input_tokens` 和 `output_tokens` 分别统计提示词（[prompt](../guides/prompt.md)）与模型生成内容的 Token 数；
  - Token Plan 按实际消耗的 Tokens 抵扣 Credits（非固定换算，受模型类型、思考模式、工具调用等影响）；
  - TPM（Tokens Per Minute）和 PTU（Prepaid Token Unit）直接以每分钟可处理的 Token 数定义吞吐能力。

- **限流控制**：平台通过 Token 级别参数实施速率限制：
  - `max_tokens` 控制单次请求最大输出长度（必须 ≤ 模型文档标注的上限）；
  - `tpm_limit`（部署服务级）、`input_tpm`/`output_tpm`（TPM 预留）限制每分钟允许处理的 Token 总量；
  - 动态限流（如 `qwen3.8-max`）按账号月消费档位分配 TPM 配额，超限返回 `429 Too Many Requests`。

- **性能与成本优化**：
  - 长文本输入触发阶梯系数（如 `glm-5.1` 在 32K–200K 区间输入 Token 按 1.33 倍计费）；
  - 缓存命中（如 GLM-5.2）可对重复输入 Token 按折扣（如 25%）计费；
  - 启用 `enable_thinking=true` 会增加推理 Token 消耗（因模型需生成中间思考链），并影响单价。

- **可观测性**：应用监控系统在 Trace 中精确上报每个 LLM 节点的 `input_tokens` 和 `output_tokens`，支持按 Token 量筛选异常请求、分析成本热点、评估 [prompt](../guides/prompt.md) 效率。

- **多模态适配**：图像、视频、语音等非文本输入经编码后同样转化为 Token 序列参与计费与限流（如 `qwen3-vl-plus` 的 `image_url` 会被 tokenizer 转为视觉 Token），纯文本模型则拒绝此类输入。

## 关键参数和配置

| 参数 | 说明 | 典型取值范围 | 使用位置 |
|------|------|--------------|----------|
| `max_tokens` | 单次响应最大输出 Token 数 | `1`–模型文档标注上限（如 `qwen3.8-max` 为 8192） | 所有 `/chat/completions` 请求体 |
| `input_tokens` / `output_tokens` | 响应体中返回的实际消耗 Token 数 | 自动计算，只读字段 | `completion.usage` 字段（OpenAI 兼容）或 `usage.total_tokens`（DashScope SDK） |
| `input_tpm` / `output_tpm` | TPM 预留购买的每分钟输入/输出 Token 容量 | 如 `10000` / `1000` | TPM 预留创建参数 |
| `tpm_limit` | 部署服务级每分钟 Token 总量上限 | `1000`–`1000000` | MU 模式部署参数 |
| `enable_thinking` | 是否启用思考模式（影响 Token 消耗与单价） | `true` / `false` | 请求体或部署参数（部分模型强制启用） |

> ⚠️ 注意：`max_tokens` 是硬性约束，超出将被截断并可能触发 `400 Bad Request`；而 `tpm_limit` 等容量参数是软性保障，溢出时按策略自动降级（如转按量付费）或返回 `429`。

## 面向开发者，简洁实用

- **估算 Token 数**：使用 DashScope SDK 的 `dashscope.Tokenizer` 或 OpenAI 的 `tiktoken`（注意：百炼 tokenizer 与 OpenAI 不完全一致，生产环境请以 API 返回的 `usage` 字段为准）。
- **降低 Token 成本**：
  - 精简 [prompt](../guides/prompt.md)，移除冗余描述；
  - 对长文档优先用 `qwen-long` + `chunking`，而非整篇输入；
  - 启用缓存（`cache_enabled: true`）复用历史输入；
  - 评估是否必需 `enable_thinking`——简单任务建议关闭。
- **调试技巧**：
  - 检查响应中的 `usage` 字段，确认实际 `input_tokens` 和 `output_tokens`；
  - 若 `max_tokens` 设置过小导致截断，观察 `finish_reason="length"`；
  - 在应用监控中按 `output_tokens > 1000` 过滤，快速定位高成本请求。
- **避坑提醒**：
  - 多模态模型的 `content` 数组中每个 `image_url` 会贡献数百至数千 Token，务必预估；
  - Token Plan 的 Credits 抵扣不等于 `input + output` 简单相加，含思考链、工具调用等附加消耗；
  - TPM 预留和快速模式的专属 model ID（如 `tpm-qwen38max-abc123` 或 `glm-5.2-fast-preview`）不可混用，否则鉴权失败或计费异常。

## 关联主题页

- [preparations](../api/preparations.md)
- [get started with models](../guides/get-started-with-models.md)
- [token plan guide](../guides/token-plan-guide.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [application monitoring](../guides/application-monitoring.md)


