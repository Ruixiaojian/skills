# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标、成本消耗及异常事件。它覆盖从基础用量统计到细粒度推理日志的全链路数据采集，支持开发者快速定位性能瓶颈、识别安全风险、控制成本并建立自动化告警。该功能与[模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)形成互补：前者侧重分钟级实时诊断与主动干预，后者侧重小时级账单对齐与资源规划。

## 支持的模型/功能

- **监控范围**：  
  - *普通监控*（免费）：支持所有在[模型列表](https://help.aliyun.com/zh/model-studio/models)中可选的模型，包括基于它们调优后的[自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)；  
  - *高级监控*（收费）：仅限北京、上海、新加坡、弗吉尼亚地域下的模型（注意：文档2明确列出上海地域支持，但文档1未提及，需以文档2为准）；  
  - *告警功能*：仅支持北京、新加坡、弗吉尼亚地域（**不支持上海**），详见[模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

- **核心功能**：  
  - 调用记录追踪（含 Request ID、状态码、错误码）；  
  - 多维指标监控：RPM、TPM、TPS（仅高级监控）、调用时长、首 [Token](../concepts/token.md) 延时（TTFT）、非首 [Token](../concepts/token.md) 延时；  
  - 成本维度：[Token](../concepts/token.md) 消耗汇总与单次调用用量明细；  
  - 安全维度：内容安全错误次数（涉黄/涉政/广告等拦截）；  
  - 日志回流：将推理日志导出为训练数据集；  
  - Grafana / 自建系统集成：通过私有 Prometheus HTTP API 接入。

> **注意**：文档1称“模型列表中的所有模型均支持查看用量”，而文档2明确限定高级监控和告警仅支持部分地域。二者无本质矛盾——文档1描述的是用量统计（基础能力），文档2描述的是实时监控与告警（增强能力）。但需注意：**上海地域模型不支持告警**，此限制在文档1中未体现，应以文档2为准。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspace_id` | 业务空间 ID，监控数据按此维度隔离与聚合 | [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `model` | 模型 Code（如 `qwen-plus`），用于精确筛选 | 同上 |
| `apikey_id` | API Key ID（非密钥本身），用于归因调用来源；值为 `-1` 表示来自控制台调用 | 同上 |
| `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC），影响延时与吞吐分析 | 同上 |
| `step` | Prometheus 查询步长（如 `60s`），影响时间序列分辨率 | 同上 |

## 使用方式

1. **启用监控**：  
   - 普通监控默认开启；  
   - 高级监控（含 TPS、分钟级日志、Prometheus API）需手动开通：进入目标业务空间的[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) → 右上角「模型监控配置」→ 开启「性能和用量指标监控」。

2. **查看数据**：  
   - **概览**：在[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)列表页查看模型总量、失败率、平均时长等卡片指标；  
   - **详情**：点击模型操作栏「监控」，切换「调用统计」与「性能指标」页签，支持按 API Key、推理类型、时间范围（≤30天）、时间精度（分钟/小时）筛选；  
   - **日志**：点击「日志」，查看请求/响应原文（仅限[支持的模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)#支持请求和响应的模型）及 Token 用量；  
   - **历史用量**：Token 消耗可在「调用统计」页签直接查看，或通过 Prometheus API 查询（见下文）。

3. **接入外部系统**：  
   - 获取 Prometheus HTTP API 地址（需已开通高级监控）；  
   - 使用 `Authorization: Basic base64Encode(AccessKey:AccessKeySecret)` 认证；  
   - 示例查询：`GET {API}/api/v1/query_range?query=model_usage{model="qwen-plus",workspace_id="llm-nymssti2mzww****"}&start=...&end=...&step=60s`。

## 限制和注意事项

- **数据延迟**：  
  - 普通监控（调用次数、Token 总量）：**小时级延迟**，高峰期可达 1–2 小时；  
  - 高级监控（推理日志、分钟级指标）：**分钟级延迟**，需等待日志同步完成后再查询；  
  - 免费额度数据：**分钟级更新**，支持手动刷新（见[模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

- **地域与模型限制**：  
  - 告警与高级监控**不支持上海地域**；  
  - 推理日志（请求/响应内容）**仅限部分模型**（如 qwen3-* 系列、deepseek-v3.* 等），不支持的模型界面提示“当前模型暂不支持日志”；  
  - 批量推理调用**不记录在模型监控日志中**（仅实时推理支持）。

- **权限与范围**：  
  - 主账号可查看全部业务空间数据；  
  - 子业务空间成员**仅能查看当前空间数据**，无法跨空间切换；  
  - 开通推理日志前的历史调用**无法补录**。

- **计费说明**：  
  - 普通监控免费；  
  - 高级监控、告警、Prometheus 实例存储与 API 调用按量计费；  
  - TPS 指标（`model_tps_per_request`）**仅在高级监控中提供**，且其物理意义为“单次请求输出 Token 速度”，与非首包时长呈倒数关系，不可直接等同于整体吞吐能力。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


