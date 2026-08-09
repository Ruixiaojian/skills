# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标、成本消耗及安全风险。它覆盖从基础调用统计到高级性能分析的全链路数据采集，并支持分钟级延迟的推理日志回溯与主动告警。该功能面向生产环境运维和成本治理场景，为开发者提供可操作的数据洞察。

## 支持的模型与功能

- **监控范围**：普通监控支持[选择模型](https://help.aliyun.com/zh/model-studio/models)中全部公开模型及基于其调优的[自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)；高级监控（含推理日志、TPS等指标）仅限北京、上海、新加坡、弗吉尼亚地域下的模型 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **日志支持**：并非所有模型均支持请求/响应内容记录。当前明确支持的包括 `qwen3-max` 系列、`qwen-plus` 系列、`qwen-flash`、`qwen-turbo`、`qwen3-coder-*`、开源模型（如 `qwen3-235b-a22b`）及三方模型（如 `deepseek-v3.1`）等；不支持时界面提示“当前模型暂不支持日志” [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **用量统计**：所有模型均支持用量查看，包括 [Token](../concepts/token.md)、图像张数、视频秒数等不同计量单位，具体口径详见[模型用量统计单位说明](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

> **注意**：文档1称“高级监控支持北京、上海、新加坡、弗吉尼亚地域”，而文档2未提及地域限制，但其“查看模型用量”章节明确指出数据延迟“约为1小时”，且仅支持最近30天数据——这与文档1中“高级监控为分钟级延迟”存在隐含矛盾。实际使用中，请以开通高级监控后控制台显示的延迟为准，上海地域需确认是否已纳入高级监控服务范围。

## 关键参数与指标

| 类别 | 指标名 | 说明 | 可用性 |
|--------|---------|------|---------|
| **调用统计** | `model_call_count` | 调用总次数 | 普通监控 |
| **性能** | `model_call_duration`, `model_first_token_duration`, `model_generation_duration_per_token` | 平均调用时长、首[Token](../concepts/token.md)延时、非首[Token](../concepts/token.md)延时（均值/p50/p99） | 高级监控 |
| **吞吐** | `model_tps_per_request` | 单次请求输出Token速度（TPS），仅高级监控支持 | 高级监控 |
| **用量** | `model_usage` | Token/张/秒等用量总和 | 普通与高级监控均支持 |
| **错误** | `model_call_error_count{error_type="rate_limit"}` / `{error_type="content_safety"}` | 限流错误、内容安全拦截次数 | 普通监控 |

所有指标均支持按 `workspace_id`、`model`、`apikey_id`、`protocol`（HTTP/SSE/WS）、`sub_protocol`（DEFAULT/ASYNC）等 label 过滤，详见 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 中“支持的过滤条件”章节。

## 使用方式

1. **启用监控**：  
   - 普通监控默认开启，数据延迟约1–2小时；  
   - 高级监控需手动开通：在目标业务空间的[模型监控配置](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)中开启“性能和用量指标监控”及“推理日志” [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  

2. **查看数据**：  
   - 控制台路径：`模型监控` → 选择模型 → `监控`页签（调用统计/性能指标）或`日志`页签（请求/响应详情）；  
   - Token消耗可在“调用统计”页签的“调用量”区域直接查看，或通过[模型用量](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/usage-statistics)页面按业务空间维度汇总分析 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。  

3. **接入外部系统**：  
   - 高级监控数据暴露标准 Prometheus HTTP API，支持 Grafana 可视化或自建应用集成；  
   - 请求示例：`GET {prometheus_api}/api/v1/query_range?query=model_usage{workspace_id="xxx",model="qwen-plus"}&start=...&step=60s`，需携带 Base64 编码的 AccessKey 认证头 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 限制和注意事项

- **数据延迟**：普通监控（调用次数、Token总量）延迟为小时级（高峰期达1–2小时）；高级监控（推理日志、TPS、p99指标）为分钟级延迟；免费额度数据分钟级更新，支持手动刷新 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **地域与模型限制**：告警功能仅支持北京、新加坡、弗吉尼亚地域；推理日志内容记录依赖模型本身能力，开通前的历史调用无法补录；上海地域高级监控支持状态需以控制台实际开通选项为准。  
- **权限隔离**：子业务空间成员仅能查看当前空间数据，无法跨空间切换；主账号或具备足够权限的子账号才可开通日志与告警 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **用量统计粒度**：模型用量按业务空间维度聚合，不支持按阿里云账号全局统计；超过30天的数据需通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)页面查询 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)
- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


