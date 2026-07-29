# Token

Token 是百炼平台中用于计量大模型输入、输出及内部计算资源消耗的核心计费与性能单位。它代表模型处理的最小语义单元（如中文字符、英文子词或图像 patch），其数量直接决定调用成本、推理延时和资源配额使用。

## 在百炼平台的不同场景中，这个概念如何使用

- **Token Plan 订阅服务**：Token 是 Credits 消耗的基础单位。一次调用的总 Credits =（输入 Token 数 + 输出 Token 数）× 模型单价系数 + 思考模式/缓存/工具调用等附加因子。例如 `qwen3.6-plus` 的输入/输出 Token 均按固定单价折算，视觉理解或多模态生成中图片被编码为视觉 Token 后同样计入总量。

- **模型监控（Model Monitoring）**：Token 消耗是核心可观测指标之一。监控系统按分钟级或小时级聚合 `input_tokens` 和 `output_tokens`，支持按 API Key、模型、时间范围统计用量趋势，并可配置“Token 消耗突增”类告警。`max_tokens` 参数显式限制输出长度，直接影响 Token 成本与首 Token 延时。

- **应用监控（Application Monitoring）**：在智能体或工作流链路中，每个 `LLM` 节点的 Span 明确记录 `Token总量`（输入 + 输出之和），`EMBEDDING` 节点则以 Token 等效长度衡量文本向量化开销。该数据用于定位高 Token 消耗环节（如冗长 [prompt](../guides/prompt.md) 或过长响应），支撑成本优化与链路调优。

- **高性能推理（TPM / Fast Mode）**：Token 是容量与吞吐的标尺。TPM 预留以 **kTPM（千 Token/分钟）** 为单位购买专属算力；Fast Mode 则以 **TPS（Token/秒）** 衡量实际输出速率。缓存命中时，部分 Token 可享受折扣（如 `glm-5.2` 缓存部分按 25% 折算），进一步降低有效 Token 成本。

## 关键参数和配置

- `max_tokens`：强制限制模型输出最大 Token 数，推荐生产环境必设，防止意外长响应导致成本失控和超时。
- `temperature` / `top_p` 等采样参数：间接影响输出 Token 分布与长度稳定性，但不改变 Token 计数逻辑。
- 缓存相关：启用缓存后，重复输入的 Token 可按模型策略（如 25% 折扣）折算用量，需在控制台开通并确认模型支持。
- 多模态 Token：图像/视频/语音输入经编码器转换为视觉/音频 Token，统一纳入计费；具体换算规则由模型实现决定（如 `qwen-image-2.0-pro` 对 1024×1024 图片生成约 1280 视觉 Token）。

## 面向开发者，简洁实用

- ✅ **始终显式设置 `max_tokens`**：避免无上限输出，控制成本与延迟。
- ✅ **监控 `input_tokens` 和 `output_tokens` 分离值**：识别 [prompt](../guides/prompt.md) 过长或响应冗余问题（如 `output_tokens / input_tokens > 5` 可能提示低效生成）。
- ✅ **多模态调用前预估 Token**：使用 SDK 的 `count_tokens()` 工具或参考文档中的典型值（如单图 ≈ 1000–2000 Token），避免额度误判。
- ❌ **不要假设 Token 数 = 字符数**：中文、emoji、特殊符号、代码块均按子词（subword）或视觉 patch 计数，实际值需以 API 返回的 `usage` 字段为准。
- ⚠️ **Token Plan 与通用 API 的 Token 计费独立**：同一模型在不同接入方式（如 `token-plan.cn-beijing.maas.aliyuncs.com` vs `dashscope.aliyuncs.com`）下 Token 单价与配额互不影响。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


