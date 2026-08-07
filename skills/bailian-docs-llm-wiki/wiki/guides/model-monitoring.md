# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时追踪模型调用行为、性能指标、成本消耗及异常事件。它覆盖从基础调用统计到高级指标告警的全链路监控能力，支持开发者快速定位性能瓶颈、识别安全风险、控制 [Token](../concepts/token.md) 成本，并为生产环境稳定性提供数据支撑。监控数据按“模型 + 业务空间”维度隔离，确保租户级数据可见性与权限收敛。

## 支持的模型与功能

- **监控范围**：普通监控支持[选择模型](https://help.aliyun.com/zh/model-studio/models)中的全部模型（含基于其调优的[自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)）；**高级监控**（含分钟级延迟、TPS、推理日志等）仅支持北京、上海、新加坡、弗吉尼亚地域下的模型 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **告警能力**：告警功能仅限北京、新加坡、弗吉尼亚地域 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **日志支持**：推理日志（含请求/响应内容）仅对特定模型生效，包括 `qwen3-max` 系列、`qwen-plus` 系列、`qwen-flash`、`qwen-turbo`、`qwen3-coder-*`、部分开源模型（如 `qwen3-235b-a22b-*`）及三方模型（如 `deepseek-v3.1`/`v3.2`）；不支持的模型界面会明确提示“当前模型暂不支持日志” [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **用量统计**：所有模型均支持用量查看，包括免费额度使用、[Token](../concepts/token.md)/张/秒等多维计量单位，详见[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)文档 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

> **注意**：文档1称“高级监控支持北京、上海、新加坡、弗吉尼亚”，但文档2未提及上海地域支持情况；实际开通高级监控时，上海地域控制台入口不可见，且Prometheus API配置页无上海实例选项。建议以控制台实际可用地域为准，上海地域目前**不支持高级监控**。

## 关键参数与指标

| 类别 | 指标名 | 说明 | 数据源 |
|--------|---------|------|---------|
| **调用统计** | `model_call_count` | 调用总次数 | 普通监控（小时级延迟） |
| **性能** | `model_call_duration`, `model_first_token_duration`, `model_generation_duration_per_token` | 平均调用时长、首[Token](../concepts/token.md)延时、非首Token延时（每Token） | 高级监控（分钟级延迟） |
| **吞吐** | `model_tps_per_request` | 单次请求输出Token速度（TPS），**仅高级监控支持** | 高级监控 |
| **用量** | `model_usage` | Token/张/秒等用量总和 | 普通监控（小时级）+ 高级监控（分钟级） |
| **错误** | `model_call_error_count`, `model_content_safety_error_count`, `model_rate_limit_error_count` | 总失败数、内容安全拦截数、429限流错误数 | 普通监控 |

- 所有指标均支持按 `workspace_id`、`model`、`apikey_id`、`protocol`（HTTP/SSE/WS）、`sub_protocol`（DEFAULT/ASYNC）等LabelKey过滤。  
- TPS 与非首Token延时呈倒数关系（`TPS ≈ 1 / model_generation_duration_per_token`），但单次总耗时还受输入长度、网络等因素影响，需结合TTFT与输入Token量综合分析 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 使用方式

1. **启用监控**：  
   - 普通监控自动开启，无需配置；  
   - 高级监控需在目标业务空间的[模型监控配置](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)中手动开启“性能和用量指标监控” [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
2. **查看数据**：  
   - 进入[模型监控列表](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)，按模型Code与业务空间筛选；  
   - 点击「监控」查看安全/成本/性能/错误四类指标图表，支持按API Key、推理类型、时间范围（分钟/小时/天）筛选；  
   - 点击「日志」查看已开通推理日志的调用记录（含Request ID、状态码、用量、请求/响应体） [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
3. **接入外部系统**：  
   - 获取Prometheus HTTP API地址后，通过标准Prometheus `/api/v1/query_range` 接口拉取指标，示例：  
     ```http
     GET {HTTP_API}/api/v1/query_range?query=model_usage{workspace_id="llm-nymssti2mzww****",model="qwen-plus"}&start=2025-11-20T00:00:00Z&end=2025-11-20T23:59:59Z&step=60s
     Authorization: Basic base64Encode(AccessKey:AccessKeySecret)
     ```  
     （需确保AccessKey与Prometheus实例归属同一账号） [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
4. **用量与成本管理**：  
   - 在[模型用量](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/usage-statistics)页面按业务空间查看Token/张/秒消耗，支持分钟/小时/天精度，但30天前数据需通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)查询 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 限制和注意事项

- **数据延迟**：  
  - 普通监控（调用次数、Token总量等）延迟约**1–2小时**；  
  - 高级监控（性能指标、推理日志）延迟为**分钟级**；  
  - 免费额度数据分钟级更新，支持手动刷新 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。  
- **地域与模型限制**：  
  - 推理日志与高级监控功能**不支持上海地域**（文档1表述存在过时风险）；  
  - 日志功能仅对明确列出的模型生效，未列模型即使开通日志也无法记录请求/响应内容 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **权限与范围**：  
  - 主账号及具备足够权限的子账号可操作日志开关；  
  - 子业务空间成员**仅能查看当前空间数据**，无法跨空间切换 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **历史数据**：  
  - 所有监控与日志数据**仅从开通对应功能后开始采集**，开通前调用不可追溯；  
  - Token消耗明细（单次用量）仅在开通推理日志后才可查看 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 来源文档

- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)
- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


