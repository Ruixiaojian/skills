# model monitoring

模型监控（Model Monitoring）是百炼平台提供的核心可观测性能力，用于实时跟踪、分析和告警模型在生产环境中的调用行为、性能表现与资源消耗。它覆盖从基础用量统计到细粒度推理日志的全链路数据采集，支持开发者快速定位异常、优化成本并保障服务稳定性。该功能默认启用基础监控，高级监控（含分钟级延迟指标、推理日志、Prometheus API）需手动开通。

## 支持的模型/功能

- **基础监控（普通监控）**：覆盖[选择模型](https://help.aliyun.com/zh/model-studio/models)中所有官方模型及基于它们调优后的[自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)，数据延迟约 1 小时。  
- **高级监控**：仅限北京、上海、新加坡、弗吉尼亚地域下的模型，提供分钟级延迟的性能指标（如 RPM、TPM、首 [Token](../concepts/token.md) 延时）、完整推理日志（请求/响应内容）及 Prometheus 数据导出能力。  
- **告警功能**：支持北京、新加坡、弗吉尼亚地域下所有模型；上海地域暂不支持告警 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **日志回溯能力**：仅对开通推理日志后的调用生效，历史调用无法补录；日志内容支持回流为训练数据集 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **模型用量查看**：所有模型均支持用量统计，但免费额度管理、批量操作等功能仅在[免费额度](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)页面提供 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

> **注意**：文档 1 中称“模型列表中的所有模型均支持查看用量”，而文档 2 明确指出“高级监控”和“告警”存在地域限制（上海地域不支持告警），且推理日志功能仅对特定模型版本开放（如 `qwen3-plus-2025-12-01` 及之后快照）。二者范围不一致，实际能力以文档 2 的地域与模型版本约束为准。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspace_id` | 业务空间 ID，监控数据按此维度隔离与聚合 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `model` | 模型 Code（如 `qwen-plus`），用于指标过滤与告警绑定 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `apikey_id` | API Key ID（非密钥本身），用于按调用来源归因；值为 `-1` 表示控制台调用 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC），影响延时与吞吐统计口径 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `max_tokens` | 控制输出长度的关键参数，直接影响 [Token](../concepts/token.md) 消耗与费用，建议在 API 调用中显式设置 | [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |

## 使用方式

1. **基础用量查看**：进入[模型用量](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/usage-statistics)页面，按模型 Code、API Key、时间范围（最长 30 天）筛选，支持分钟/小时/天精度；[Token](../concepts/token.md) 消耗数据延迟约 1 小时 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。  
2. **实时性能监控**：访问[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面，点击目标模型右侧「监控」，查看安全、成本、性能、错误四类指标；支持按 API Key、推理类型（实时/批量）筛选。  
3. **推理日志查看**：需先在「模型监控配置」中开通审计日志与推理日志（仅北京/新加坡/弗吉尼亚地域支持），再点击「日志」页签，查看 Request ID、输入、输出、Token 用量等明细 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
4. **告警配置**：在[模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert)页面创建规则，支持失败率、TPM、调用时长等指标阈值告警，通知方式包括短信、邮件、钉钉机器人等。  
5. **Prometheus 集成**：开启高级监控后，通过私有 Prometheus 实例的 HTTP API 查询指标（如 `model_usage{model="qwen-plus", workspace_id="xxx"}`），支持 Grafana 可视化或自建应用对接 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 限制和注意事项

- **数据延迟**：普通监控（调用次数、Token 总量）延迟为小时级（高峰期可达 1–2 小时）；高级监控（推理日志、RPM/TPM）为分钟级延迟 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **地域限制**：高级监控、告警、推理日志功能仅在北京、新加坡、弗吉尼亚地域可用；上海地域暂不支持告警，且部分高级功能可能受限。  
- **模型兼容性**：并非所有模型均支持推理日志（请求/响应内容记录），具体支持列表见文档 2 的“支持请求和响应的模型”章节；不支持的模型在日志页签会明确提示“当前模型暂不支持日志”。  
- **免费额度联动**：免费额度用完即停功能仅作用于计费层面（返回 403），不影响监控数据采集；但若服务已停止，自然无新调用数据产生 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。  
- **批量推理监控**：模型用量页面仅在「大语言模型」页签支持按推理类型（实时/批量）筛选；而模型监控列表默认包含所有推理类型调用，但日志页签目前仅展示实时推理记录。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


