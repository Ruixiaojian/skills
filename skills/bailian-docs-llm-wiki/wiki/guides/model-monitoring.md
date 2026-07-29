# model monitoring

模型监控（Model Monitoring）是百炼平台提供的核心可观测性能力，用于实时追踪模型调用行为、性能指标、成本消耗及异常事件。它面向生产环境提供细粒度的调用日志、多维指标监控与主动告警能力，帮助开发者及时发现服务降级、成本突增或内容安全风险。该功能覆盖所有已上线模型，但高级能力（如分钟级延迟日志、TPS指标、Grafana接入）受地域与配置状态限制。

## 支持的模型/功能

- **基础监控**：支持[选择模型](https://help.aliyun.com/zh/model-studio/models)中的全部模型（含调优后的自定义模型），覆盖所有地域；数据延迟为小时级（高峰期可达1–2小时）[原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **高级监控**：仅限北京、上海、新加坡、弗吉尼亚地域下的模型，提供分钟级日志、TPS（`model_tps_per_request`）等深度指标，并支持Prometheus API对接 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **告警能力**：仅在北京、新加坡、弗吉尼亚地域可用，支持对失败率、首[Token](../concepts/token.md)延时、[Token](../concepts/token.md)消耗等指标设置多级告警 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **日志回溯**：仅部分模型支持请求/响应内容记录（如 `qwen3-plus`、`qwen-flash` 等快照版本），且**仅在开通推理日志后生效**，历史调用无法补录；不支持的模型界面会明确提示“当前模型暂不支持日志”。

> **注意**：文档1中称“模型列表中的所有模型均支持查看用量”，而文档2明确指出日志与高级指标存在地域和模型版本限制。二者不矛盾——“用量统计”（文档1）指聚合计费数据，属基础能力；“模型监控”（文档2）指实时可观测性能力，需额外开通且有范围约束。实际使用中应以[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)文档为准判断功能可用性。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspace_id` | 业务空间ID，用于按空间维度隔离监控数据，必填过滤条件 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `model` | 模型Code（如 `qwen-plus`），用于精确筛选单个模型指标 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `apikey_id` | API Key ID（非密钥本身），用于归因调用来源；值为 `-1` 表示来自控制台调用 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC），影响延时与吞吐分析维度 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `max_tokens` | 调用API时显式设置，直接影响输出[Token](../concepts/token.md)数与费用，建议在生产中强制设限 | [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |

## 使用方式

1. **启用监控**  
   - 进入目标业务空间的[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面 → 点击右上角「模型监控配置」→ 开通**审计日志**与**推理日志**（高级监控必需）。
   - 高级监控开通后，方可使用分钟级日志、TPS指标及Prometheus API。

2. **查看指标**  
   - 在「模型监控」列表点击目标模型的「监控」，切换至「调用统计」或「性能指标」页签，支持按API Key、推理类型（实时/批量）、时间范围（最大30天）筛选。
   - Token消耗可在「调用量」区域直接查看；单次调用明细（含输入/输出）需进入「日志」页签（仅支持模型见文档2列表）。

3. **配置告警**  
   - 进入[模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert)页面 → 「创建告警规则」→ 选择模型、指标模板（如“Token消耗突增”）、阈值与通知渠道（短信/钉钉/Webhook等）。

4. **对接自建系统**  
   - 获取Prometheus HTTP API地址（通过「模型监控配置」→「云监控Prometheus实例」→「查看详情」）。
   - 使用标准PromQL查询，例如：  
     `GET {API}/api/v1/query_range?query=model_usage{workspace_id="xxx",model="qwen-plus"}&start=...&step=60s`

## 限制和注意事项

- **数据时效性**：普通监控（用量汇总）延迟约1小时；推理日志延迟为分钟级，但需等待日志开通后首次调用完成才开始采集。
- **地域限制**：高级监控、告警、日志回溯功能**仅限北京、新加坡、弗吉尼亚地域**；上海地域仅支持基础监控（无TPS、无分钟级日志）。
- **模型兼容性**：并非所有模型支持请求/响应内容记录，具体支持列表以[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)文档为准；不支持时界面明确提示。
- **免费额度联动**：监控本身不消耗免费额度，但用量统计与免费额度使用情况强关联；开启「免费额度用完即停」后，额度耗尽将返回403错误，此时监控仍可查看历史数据，但新调用被阻断 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
- **批量操作风险**：在「免费额度」页面进行批量开关操作时，若账号未绑定有效支付方式，操作将失败并提示绑定银行卡，需提前校验支付状态。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


