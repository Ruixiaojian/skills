# Token（令牌计量）

Token 是大语言模型处理文本的基本计量单位，模型将输入和输出文本拆分为 Token 序列进行处理。在百炼平台中，Token 既是模型能力的度量尺度（如上下文窗口长度），也是计费和资源管控的核心单位。

## 什么是 Token

Token 并非直接等同于字符或单词。对于中文，1 个 Token 大约对应 1.5 个汉字；对于英文，1 个 Token 大约对应 4 个字符或 0.75 个单词。一次模型调用的 Token 消耗 = 输入 Token + 输出 Token（部分场景还包含思考 Token）。

## 在百炼平台中的使用场景

### 模型推理计费

百炼按量付费模式以 Token 为核心计量单位，按输入 Token 和输出 Token 分别定价。部分模型实行阶梯计费，单价取决于单次请求的输入 Token 总量：

| 阶梯示例（qwen3-max） | 输入单价 | 输出单价 |
|------------------------|----------|----------|
| 0 < Token ≤ 32K | 2.5 元/百万 Token | 10 元/百万 Token |
| 32K < Token ≤ 128K | 4 元/百万 Token | 16 元/百万 Token |
| 128K < Token ≤ 256K | 7 元/百万 Token | 28 元/百万 Token |

Token Plan 团队版则将 Token 消耗折算为 Credits 进行抵扣。

### 上下文窗口

上下文窗口以 Token 为单位衡量模型单次可处理的最大信息量：

| 上下文长度 | 代表模型 |
|-----------|---------|
| 1M Token（约 70 万汉字） | qwen3.7-max、qwen3.6-plus、qwen3.6-flash、deepseek-v4-pro |
| 256K Token | qwen3.6-max-preview、kimi-k2.6 |
| 128K~198K Token | glm-5.1（198K）、MiniMax-M2.5（192K） |

### 监控与用量统计

百炼模型监控以 Token 为核心统计口径（大语言模型场景），提供以下指标：

- **TPM**（Tokens Per Minute）：每分钟 Token 吞吐量
- **Token 总量**：按业务空间汇总的输入/输出 Token 消耗
- **平均单次请求 Token 量**：用于成本分析和异常检测

在应用观测中，可按 Token 总量、输入 Token、输出 Token 进行 Span 筛选和统计。

### 模型训练

模型调优按训练 Token 用量计费。训练数据中的 `max_length` 参数定义单条样本的最大 Token 长度，超长数据将被丢弃（推荐值 8192）。

### 向量模型

Embedding 模型对输入文本有单行最大 Token 限制：

| 模型版本 | 单行最大 Token |
|---------|--------------|
| text-embedding-v4 / v3 | 8,192 |
| text-embedding-v2 / v1 | 2,048 |

## 关键参数和配置

| 参数 | 作用 | 典型场景 |
|------|------|---------|
| `max_tokens` | 限制模型单次输出的最大 Token 数 | 控制输出长度和成本 |
| `enable_thinking` | 开启思考模式，消耗额外思考 Token | 复杂推理任务 |
| thinking budget | 思考模式下的最大思考 Token 预算（如 qwen3.7-max 为 256K） | 深度推理场景 |
| `max_length`（训练） | 训练样本的最大 Token 长度 | 模型调优 |

## 成本优化建议

- **合理设置 `max_tokens`**：避免不必要的输出 Token 消耗。
- **按任务选模型**：简单任务使用轻量模型（如 qwen3.6-flash），降低单价。
- **利用上下文缓存**：输入 Token 可享折扣（不与 Batch 调用同时生效）。
- **Batch 调用**：非实时场景使用批量推理，输入输出单价均为实时价格的 50%。
- **监控告警**：配置 Token 用量告警，及时发现异常调用。
- **免费额度用完即停**：开启后额度耗尽自动停止，避免意外扣费。

## 费用抵扣顺序

Token 消耗产生的费用按以下顺序抵扣：

1. 免费额度
2. 资源包
3. 其他模型节省计划
4. AI 通用型节省计划
5. 按量付费

## 注意事项

- 不同模型类型的用量统计口径不同：大语言模型按 Token，图像生成按张，视频生成按秒。
- 免费额度为分钟级出账，控制台显示存在延迟。
- Token Plan、Coding Plan 和百炼按量计费三者的计量体系互不相通。
- 账户欠费时，即使模型仍有免费 Token 额度也无法调用（Token Plan 和 Coding Plan 套餐额度除外）。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [model inference](../guides/model-inference.md)
- [model training](../api/model-training.md)
- [general text embedding](../api/general-text-embedding.md)

