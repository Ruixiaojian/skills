# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时追踪模型调用行为、性能指标与资源消耗。它覆盖从基础用量统计到细粒度推理日志的全链路数据采集，支持开发者进行成本控制、故障排查与服务质量保障。该功能默认启用基础监控，高级监控（含分钟级延迟日志、Prometheus指标导出等）需手动开通。

## 支持的模型/功能

- **基础监控**：覆盖[模型列表](https://help.aliyun.com/zh/model-studio/models)中所有官方模型及基于其[调优后的自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)，适用于所有地域。
- **高级监控与告警**：仅支持北京、上海、新加坡、弗吉尼亚地域下的模型；告警功能当前限于北京、新加坡、弗吉尼亚地域（详见 [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。
- **推理日志（请求/响应内容）**：并非所有模型均支持，具体支持列表见 [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 中“支持请求和响应的模型”章节；该能力与模型是否为多模态无关，由模型底层实现决定。
- **[Token](../concepts/token.md) 消耗追踪**：所有支持监控的模型均可统计 [Token](../concepts/token.md) 用量，但单次调用级的 [Token](../concepts/token.md) 记录仅在开通推理日志后生效（参见 [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。

> **注意**：文档 1 中称“模型列表中的所有模型均支持查看用量”，而文档 2 明确指出推理日志和高级监控存在地域与模型型号限制。二者不矛盾——“用量”指汇总级指标（如总 Token 数），而“日志”和“高级指标”（如 TPS、首 Token 延时 p99）需额外开通且受地域约束。实际使用中应以 [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 的能力边界为准。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspace_id` | 业务空间 ID，监控数据按此维度隔离与聚合 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `model` | 模型 Code（如 `qwen-plus`），用于指标过滤与告警绑定 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `apikey_id` | API Key ID（非密钥字符串），用于按调用来源归因 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC），影响性能指标语义 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `max_tokens` | 控制输出长度的关键参数，直接影响 Token 消耗与费用（参见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)） | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |

## 使用方式

1. **基础监控查看**  
   进入 [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 页面，数据按“模型 + 业务空间”自动聚合。默认展示小时级延迟的调用总量、失败率、平均时长等卡片指标；点击模型右侧「监控」可查看安全、成本、性能、错误四类指标趋势。

2. **开启高级能力**  
   - 若需分钟级日志、TPS 指标或 Prometheus 导出，须在目标业务空间的「模型监控配置」中手动开启**高级监控**（含性能和用量指标监控、审计日志、推理日志）。
   - 开通后，日志与高级指标将从开通时刻起生效，历史调用不补录。

3. **告警配置**  
   在 [模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert) 页面创建规则，支持对 `model_call_count`、`model_usage`、`model_call_duration_p99` 等指标设置阈值。通知方式包括钉钉机器人、Webhook 等（详见 [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。

4. **Grafana / 自建系统集成**  
   获取 Prometheus 实例 HTTP API 地址后，通过标准 `/api/v1/query_range` 接口拉取指标，例如：  
   ```http
   GET {API}/api/v1/query_range?query=model_usage{workspace_id="xxx",model="qwen-plus"}&start=2025-11-20T00:00:00Z&end=2025-11-20T23:59:59Z&step=60s
   ```

## 限制和注意事项

- **数据延迟**：基础监控（调用次数、Token 总量）延迟约 1 小时；高级监控（推理日志、TPS）为分钟级延迟；账单级用量需通过 [费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance) 查询（文档 1 和文档 2 均明确此限制）。
- **时间范围限制**：模型监控页面仅支持查看最近 30 天数据；更早记录需导出账单（[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。
- **地域与模型兼容性**：高级监控、告警、推理日志功能**不支持杭州、深圳等非列名地域**；部分模型（如早期快照版本）不支持请求/响应内容记录（[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 明确列出支持清单）。
- **权限隔离**：子业务空间成员仅能查看本空间数据，无法跨空间筛选（[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。
- **免费额度联动**：监控本身不触发计费，但「免费额度用完即停」开关关闭后，超限调用将按实际用量扣费（[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）；建议结合监控告警及时干预。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


