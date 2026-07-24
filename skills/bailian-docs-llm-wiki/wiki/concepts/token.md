# Token

Token 是百炼平台中用于计量模型输入与输出内容的基本单位，代表模型处理的最小语义单元（如子词、标点、图像 patch 或音频帧等）。在计费、限流、性能监控与资源调度中，Token 是统一的量化基准——所有模态模型的用量均以 Token 为单位统计和结算。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用计费**：每次 API 调用的总 Token 消耗 = `输入 Token 数 + 输出 Token 数`。文本模型按字符/子词切分；视觉模型（如 `qwen3.7-plus`）将图像转为视觉 Token（单图最高约 1600 万像素 → 数万 Token）；语音/视频模型按时间分辨率与编码粒度映射为 Token。计费单价按模型维度独立设定（如 `qwen3.7-plus` 输入 0.0002 元/Token，输出 0.0004 元/Token）。

- **上下文长度约束**：模型能力明确标注最大支持 Token 数（如 `qwen3.7-plus` 支持 1000 万 Token 上下文），该值限制 [prompt](../guides/prompt.md) + history + 生成 output 的总长度。超出将触发截断或报错（HTTP 400，`context_length_exceeded`）。

- **性能监控指标**：  
  - `model_usage`（模型监控）：业务空间级 Token 总消耗量；  
  - `Token 总量`（应用观测）：单次 Span 中 LLM 节点的输入+输出 Token 数，用于成本归因与链路优化；  
  - `usage.prompt_tokens_details.cached_tokens`（高吞吐推理）：缓存命中 Token 数，参与 TPM 折扣计算（如 `glm-5.2` 缓存折扣率 0.25，即仅按 25% 计入预留容量）。

- **资源控制与限流**：  
  - TPM（Tokens Per Minute）预留机制以 kTPM 为单位锁定吞吐能力，保障高峰期容量；  
  - Coding Plan 等套餐虽不按 Token 计费，但内部仍以 Token 为调度单元实施请求级限流；  
  - 快速模式（Fast mode）通过提升 TPS（Tokens Per Second）优化首 Token 延迟，直接受 Token 处理效率影响。

- **思考模式预算控制**：在 OpenCode 配置中，`budgetTokens` 明确指定思考过程允许消耗的最大 Token 数（如 `1024`），超限则终止推理步骤。

## 关键参数和配置

| 参数名 | 所属场景 | 说明 | 示例值 |
|--------|----------|------|--------|
| `usage.input_tokens` / `usage.output_tokens` | API 响应体 | 每次调用实际消耗的输入/输出 Token 数，位于响应 `usage` 字段中 | `{"input_tokens": 128, "output_tokens": 42}` |
| `usage.prompt_tokens_details.cached_tokens` | 高吞吐推理 | 缓存命中 Token 数，仅当启用缓存且模型支持时返回 | `24` |
| `options.thinking.budgetTokens` | OpenCode 配置 | 思考模式 Token 预算上限，硬性截断阈值 | `1024` |
| `model_usage`（监控指标） | 模型监控 | Prometheus 指标名，标签含 `model`、`workspace_id`，单位：Token | `model_usage{model="qwen3.7-plus", workspace_id="ws-abc"} 125000` |
| `Token 总量`（Span 字段） | 应用观测 | 控制台可观测字段，等于 `input_tokens + output_tokens`，用于筛选与分析 | `168` |

> ⚠️ 注意：Token 统计严格区分模态——文本 Token 不与图像 Token 互换；同一请求中[多模态](multi-modal.md)输入（如图文混合）的 Token 分别计算并累加。缓存 Token 仅在支持缓存的模型（如 `glm-5.2`）和启用缓存的部署中生效，需通过监控验证实际命中率。

## 面向开发者，简洁实用

- **调试建议**：调用后必查响应 `usage` 字段，确认 Token 消耗是否符合预期（尤其长上下文或复杂[多模态](multi-modal.md)输入）；  
- **成本优化**：对重复性 [prompt](../guides/prompt.md)，优先启用缓存；对长输出，设置 `max_output_tokens` 避免无意义生成；  
- **限流规避**：TPM 预留需按峰值输入+输出 Token 速率预估 kTPM 值（例如：每秒 50 请求 × 平均 200 Token/请求 = 600kTPM）；  
- **监控告警**：在模型监控中配置 `model_usage` 告警规则，阈值建议设为日额度的 80%，避免突发流量超支；  
- **兼容性注意**：`*-fast-preview` 等加速变体 Token 计费逻辑与基线模型一致，但 `cached_tokens` 字段解析方式需参考对应文档。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [token plan guide](../guides/token-plan-guide.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


