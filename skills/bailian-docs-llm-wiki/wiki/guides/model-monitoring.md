# model monitoring

模型监控（Model Monitoring）是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标、成本消耗及异常事件。它覆盖从基础用量统计到高级推理日志分析的全链路监控场景，支持开发者快速定位性能瓶颈、成本异常与服务稳定性问题。该功能默认启用基础监控，高级监控（含分钟级延迟日志、Prometheus指标导出等）需手动开通。

## 支持的模型/功能

- **基础监控**：覆盖[模型列表](https://help.aliyun.com/zh/model-studio/models)中所有官方模型及基于其[调优后的自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)，适用于所有地域。
- **高级监控与告警**：仅支持北京（华北2）、上海（华东2）、新加坡、弗吉尼亚地域下的模型；告警功能当前仅限北京、新加坡、弗吉尼亚地域 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **推理日志（请求/响应内容）**：并非所有模型均支持，具体支持列表详见[模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 中“支持请求和响应的模型”章节。不支持的模型在日志页签会明确提示“当前模型暂不支持日志”。

> **注意**：文档 1 中称“模型列表中的所有模型均支持查看用量”，而文档 2 明确限定高级监控与日志功能的地域与模型范围。二者不矛盾——**用量统计（文档1）是基础能力，全域可用；而细粒度日志、分钟级指标、Prometheus导出等高级能力（文档2）存在地域与模型限制**。实际使用时应以文档 2 的约束为准。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspace_id` | 业务空间 ID，监控数据按此维度隔离与聚合 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `model` | 模型 Code（如 `qwen-plus`），用于指标过滤与告警绑定 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `apikey_id` | API Key ID（非密钥本身），用于按调用来源归因 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC），影响延时与吞吐表现 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `max_tokens` | 控制输出长度的关键参数，直接影响 [Token](../concepts/token.md) 消耗与费用 | [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |

## 使用方式

1. **访问入口**  
   - 基础监控与用量概览：进入百炼控制台 → [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 页面。  
   - 免费额度与用量详情：进入 [免费额度](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota) 和 [模型用量](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/usage-statistics) 页面 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

2. **启用高级能力**  
   - 开通推理日志与审计日志：在目标业务空间的模型监控页面 → 右上角「模型监控配置」→ 启用「推理日志」与「审计日志」。  
   - 开通 Prometheus 指标：同路径下启用「性能和用量指标监控」，获取 HTTP API 地址后可对接 Grafana 或自建系统 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

3. **查看与分析**  
   - **用量趋势**：在「模型用量」页面按时间范围、API Key、模型 Code 筛选，支持分钟/小时/天精度（超 7 天仅支持按天） [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。  
   - **单次调用详情**：开启推理日志后，在「日志」页签查看 Request ID、输入/输出、[Token](../concepts/token.md) 用量、状态码及错误码。  
   - **告警配置**：在 [模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert) 页面创建规则，支持失败率、TPM、首 [Token](../concepts/token.md) 延时等阈值告警，通知方式含钉钉、企业微信、Webhook 等。

## 限制和注意事项

- **数据延迟**：  
  - 基础用量统计（调用次数、Token 总量）延迟约 **1 小时**，高峰期可达 1–2 小时；  
  - 高级监控（推理日志、性能指标）为 **分钟级延迟**，但仅限已开通日志的模型与地域 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
  - 免费额度数据分钟级更新，支持手动刷新同步。

- **时间范围限制**：  
  - 模型用量页面仅支持查询 **最近 30 天** 数据；更早数据需通过 [费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance) 页面导出账单获取 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

- **地域与权限约束**：  
  - 子业务空间成员**仅能查看本空间数据**，无法跨空间筛选；  
  - 高级监控、告警、Prometheus 接入等功能**仅限主账号或具备足够权限的子账号操作**；  
  - 日志回流、Grafana 接入等功能依赖高级监控开通状态，未开通时对应入口不可见。

- **模型兼容性**：  
  - 推理日志（含输入/输出内容）**仅对明确列出的支持模型生效**，且仅记录开通日志后的调用；历史调用无法补录；  
  - `free-tier-only`（免费额度用完即停）功能开启后，若需关闭，**必须等待免费额度完全消耗完毕**，否则控制台禁用关闭按钮 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


