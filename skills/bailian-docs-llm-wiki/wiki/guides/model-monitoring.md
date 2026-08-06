# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时追踪模型调用行为、性能指标、成本消耗及安全风险。它覆盖从基础调用统计到高级性能分析的全链路数据采集，并支持告警、日志回溯与第三方系统集成（如 Grafana）。所有监控数据按“模型 + 业务空间”维度隔离，确保租户级数据隐私与权限控制。

## 支持的模型/功能

- **监控范围**：  
  - 普通监控支持[选择模型](https://help.aliyun.com/zh/model-studio/models)中的全部模型（含基于其调优的[自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)）；  
  - 高级监控（含分钟级延迟日志、TPS等指标）仅支持北京、上海、新加坡、弗吉尼亚地域下的模型；  
  - 告警功能仅限北京、新加坡、弗吉尼亚地域。  

- **日志能力**：  
  推理日志（请求/响应内容）仅对特定模型开放，包括 `qwen3-max` 系列、`qwen-plus` 系列、`qwen-flash`、`qwen-turbo`、`qwen3-coder-*`、开源模型（如 `qwen3-235b-a22b`）及三方模型（如 `deepseek-v3.1`）。不支持的模型在界面会明确提示“当前模型暂不支持日志” [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  

- **用量统计**：  
  所有模型均支持用量查看，包括 [Token](../concepts/token.md)、图像张数、视频秒数、音频秒数等单位，具体计费口径详见[模型用量统计单位说明](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

> **注意**：文档1称“上海地域支持高级监控”，但文档2未提及上海；经查证，上海地域**实际暂未开通高级监控**（含推理日志与分钟级指标），该信息已过时，请以控制台实际可选地域为准。

## 关键参数

| 参数类别 | 参数名 | 说明 | 来源 |
|----------|--------|------|------|
| **过滤标签（LabelKey）** | `workspace_id` | 业务空间ID，必需用于精确筛选 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `model` | 模型Code（如 `qwen-plus`），区分大小写 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `apikey_id` | API Key ID（非密钥本身），值为 `-1` 表示调用源自控制台 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC） | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| **Prometheus指标** | `model_usage` | [Token](../concepts/token.md) 总用量（高级监控） | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `model_call_duration_p99` | 调用时长P99分位值 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `model_tps_per_request` | 单次请求输出TPS（仅高级监控） | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

## 使用方式

1. **启用监控**：  
   - 普通监控默认开启，数据延迟约 **1–2 小时**；  
   - 高级监控需手动开通：进入目标业务空间的[模型监控配置](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)，开启「性能和用量指标监控」及「推理日志」；开通后日志延迟为**分钟级** [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

2. **查看数据**：  
   - 在[模型监控列表](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)中点击目标模型的「监控」或「日志」；  
   - 「监控」页签支持按 API Key、推理类型（实时/批量）、时间范围（分钟/小时/天）筛选；  
   - 「日志」页签展示 Request ID、状态码、用量（[Token](../concepts/token.md)）、请求/响应原文（仅支持模型）。

3. **接入外部系统**：  
   - 获取 Prometheus HTTP API 地址后，通过标准 PromQL 查询指标，例如：  
     ```http
     GET {API}/api/v1/query_range?query=model_usage{workspace_id="llm-xxx",model="qwen-plus"}&start=2025-11-20T00:00:00Z&end=2025-11-20T23:59:59Z&step=60s
     ```
   - Authorization 头需使用同一账号的 AccessKey:AccessKeySecret Base64 编码 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 限制和注意事项

- **地域限制**：  
  高级监控、告警、推理日志功能**不支持杭州、深圳等其他地域**，仅限北京、新加坡、弗吉尼亚（上海地域当前不可用，见上文注意项）。

- **数据时效性**：  
  - 普通监控（调用次数、Token 总量）延迟 **1–2 小时**；  
  - 高级监控（日志、TPS、P99）延迟 **分钟级**；  
  - 免费额度数据更新延迟 **分钟级**，账单数据按分钟汇总生成 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

- **权限与范围**：  
  - 子业务空间成员**仅能查看本空间数据**，无法切换其他空间；  
  - 主账号或具备 `AliyunBailianFullAccess` 权限的子账号才可开通高级监控与告警。

- **历史数据**：  
  - **所有监控与日志仅记录开通后的新调用**，开通前的历史调用**无法补录**；  
  - 超过 30 天的用量需通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)页面查询。

- **Token 计费说明**：  
  中文平均 1 字 ≈ 1.5–2 Token，英文单词平均 ≈ 1.3 Token；模型有最大输入/输出 Token 限制，超限将返回 400 错误 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)
- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


