# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标、成本消耗及安全风险。它覆盖从基础调用统计到高级告警、日志审计和 Prometheus 对接的全链路监控场景，支持开发者快速定位异常、优化资源使用并保障服务稳定性。

## 支持的模型与功能

- **监控范围**：普通监控支持[选择模型](https://help.aliyun.com/zh/model-studio/models)中的全部模型（含基于其调优的[自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)）；**高级监控**（含分钟级延迟日志、TPS 指标、Prometheus 数据源）仅限北京、上海、新加坡、弗吉尼亚地域下的模型 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **告警能力**：告警功能仅支持北京、新加坡、弗吉尼亚地域 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)，且需先开启高级监控。  
- **日志能力**：推理日志（含请求/响应内容）仅对特定模型开放，包括 `qwen3-max` 系列、`qwen-plus` 系列、`qwen-flash`、`qwen-turbo`、`qwen3-coder-*`、部分开源及三方模型（如 `deepseek-v3.1`/`v3.2`）；不支持的模型界面将明确提示“当前模型暂不支持日志” [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **用量统计**：所有模型均支持用量查看（[Token](../concepts/token.md)/张/秒等），但免费额度管理、按 API Key 维度筛选等功能仅在[模型用量](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/usage-statistics)页面提供 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

> **注意**：文档 1 称“上海地域支持高级监控”，而文档 2 未提及上海；经交叉验证，[原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 中“支持北京、上海、新加坡、弗吉尼亚地域下的所有模型”为最新表述，上海地域确已纳入高级监控支持范围。

## 关键参数与指标

| 类别 | 指标名 | 说明 | 可用性 |
|--------|---------|------|--------|
| **调用统计** | `model_call_count` | 调用总次数 | 普通 & 高级监控 |
| **性能** | `model_call_duration`, `model_first_token_duration`, `model_generation_duration_per_token` | 平均调用时长、首 [Token](../concepts/token.md) 延时、非首 [Token](../concepts/token.md) 延时（每 Token） | 高级监控专属 |
| **吞吐** | `model_tps_per_request` | 单次请求输出 Token 速度（TPS），≈ 1 / `model_generation_duration_per_token` | 仅高级监控 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| **用量** | `model_usage` | Token 总消耗量（输入+输出） | 普通 & 高级监控 |
| **错误** | `model_call_error_count`, `model_content_safety_error_count`, `model_rate_limit_error_count` | 失败总数、内容安全拦截数、429 限流数 | 普通 & 高级监控 |

所有指标均支持按 `workspace_id`、`model`、`apikey_id`、`protocol`（HTTP/SSE/WS）、`sub_protocol`（DEFAULT/ASYNC）等 Label 过滤。`apikey_id = -1` 表示调用源自百炼控制台而非 API [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 使用方式

### 1. 基础监控（无需配置）
- 登录百炼控制台 → 进入[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) → 查看按“模型 + 业务空间”聚合的调用总量、失败率、平均时长等卡片与表格数据。
- 点击目标模型右侧「监控」可查看安全、成本、性能、错误四类指标趋势图；点击「日志」可查看已开通推理日志的调用记录（含 Request ID、状态码、用量、请求/响应）。

### 2. 高级监控与告警（需手动开通）
- 在模型监控页右上角点击「模型监控配置」→ 开启「性能和用量指标监控」（即高级监控）→ 后续方可使用分钟级日志、TPS 指标及 Grafana 接入 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- 开通后，进入[模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert) → 「创建告警规则」→ 选择模型、指标模板（如“失败率突增”、“Token 消耗超阈值”）→ 设置通知渠道（短信/邮件/钉钉/Webhook）及等级（INFO 至 CRITICAL）。

### 3. 自建系统对接
- 获取 Prometheus HTTP API 地址（通过「模型监控配置」→「云监控 Prometheus 实例」→「查看详情」）→ 使用标准 PromQL 查询，例如：
  ```http
  GET {API}/api/v1/query_range?query=model_usage{workspace_id="llm-nymssti2mzww****",model="qwen-plus"}&start=2025-11-20T00:00:00Z&end=2025-11-20T23:59:59Z&step=60s
  Authorization: Basic base64Encode(AccessKey:AccessKeySecret)
  ```
  > 注意：AccessKey 必须与 Prometheus 实例归属同一阿里云账号 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 限制和注意事项

- **数据延迟**：普通监控（调用次数、Token 总量）延迟约 **1–2 小时**；高级监控（推理日志、性能指标）延迟为 **分钟级**；免费额度数据更新也为分钟级 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。  
- **地域限制**：高级监控、告警、推理日志功能**不支持杭州、深圳等其他地域**，仅限北京、上海、新加坡、弗吉尼亚 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **历史数据**：所有日志与监控数据**仅在功能开通后开始采集**，开通前的调用无法补录；用量统计默认仅保留最近 **30 天**数据，更早数据需通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)页面查询 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。  
- **权限隔离**：子业务空间成员**仅能查看本空间数据**，无法切换或跨空间查询；主账号成员可查看全部业务空间 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **模型兼容性**：并非所有模型支持推理日志（请求/响应内容），具体支持列表以控制台实际展示为准；[多模态](../concepts/multi-modal.md)模型是否支持与模态无关，完全由模型自身能力决定 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 来源文档

- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)
- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


