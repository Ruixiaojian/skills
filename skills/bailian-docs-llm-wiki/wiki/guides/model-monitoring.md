# model monitoring

模型监控（Model Monitoring）是百炼平台提供的核心可观测性能力，用于实时追踪模型调用行为、性能指标、成本消耗及异常事件。它覆盖从基础用量统计到高级性能告警的全链路监控场景，支持开发者快速定位问题、优化成本并保障服务稳定性。该功能与[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)形成互补：前者侧重细粒度运行时指标与日志，后者聚焦账单级用量汇总与免费额度管理。

## 支持的模型与功能

- **监控范围**：  
  - *普通监控*：支持所有[选择模型](https://help.aliyun.com/zh/model-studio/models)中的模型（含调优后的[自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)），数据延迟为小时级；  
  - *高级监控*：仅限北京、上海、新加坡、弗吉尼亚地域下的模型，提供分钟级延迟、TPS等深度指标及Prometheus API接入能力；  
  - *告警功能*：仅支持北京、新加坡、弗吉尼亚地域模型；  
  - *推理日志（请求/响应内容）*：仅限特定模型（如 `qwen3-plus`、`qwen3-flash`、`qwen-turbo` 等快照版本及部分开源/三方模型），详见[原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中“支持请求和响应的模型”列表。

- **核心功能**：  
  - 调用记录查询（含 Request ID、状态码、错误码）；  
  - 多维指标监控：RPM、TPM、调用时长、首 Token 延时（TTFT）、非首 Token 延时、失败率、限流错误次数、内容安全错误次数；  
  - Token 消耗追踪（单次调用级）与汇总（业务空间级）；  
  - 基于指标的主动告警（支持短信、邮件、钉钉、Webhook 等通知方式）；  
  - 推理日志回流至训练数据集；  
  - Grafana 及自建应用集成（通过私有 Prometheus HTTP API）。

> **注意**：文档 1 中称“模型用量页面数据延迟约为 1 小时”，而文档 2 明确区分了普通监控（小时级）与高级监控（分钟级）。二者不矛盾，但需注意：**用量统计（文档 1）与运行时监控（文档 2）使用不同数据通道**。若需分钟级洞察，请务必启用[高级监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 关键参数与指标

| 类别 | 指标名 | 说明 | 来源 |
|--------|---------|------|------|
| **调用统计** | `model_call_count` | 调用总次数 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| **性能** | `model_first_token_duration` | 首 Token 延时均值（TTFT） | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| **性能** | `model_generation_duration_per_token` | 非首 Token 延时均值（ITL） | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| **性能** | `model_tps_per_request` | 单次请求输出 Token 速度（TPS），**仅高级监控支持** | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| **用量** | `model_usage` | Token 总消耗量（按业务空间+模型聚合） | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| **错误** | `model_call_failure_rate` | 失败率（失败次数 / 总调用次数） | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

> **注意**：`model_tps_per_request` 是高级监控独有指标，其值 ≈ 1 ÷ `model_generation_duration_per_token`。排查响应慢问题时，须结合 TTFT、ITL、输入 Token 数综合分析，不可仅依赖 TPS。

## 使用方式

1. **访问入口**：  
   - 控制台路径：`百炼控制台 > 模型 > 模型监控`（[链接](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)）；  
   - 日志与告警页签位于模型详情页内，需先在列表点击目标模型的「监控」或「日志」按钮。

2. **启用高级能力**：  
   - 进入模型监控页面 → 右上角「模型监控配置」→ 开启「性能和用量指标监控」（高级监控）及「推理日志」（如需查看请求/响应内容）；  
   - **重要**：推理日志仅记录开通后的新调用，历史数据不可补录。

3. **创建告警规则**：  
   - 进入「模型告警」页签 → 「创建告警规则」→ 选择模型、监控模板（如“Token 消耗突增”、“失败率超阈值”）、阈值与通知方式；  
   - 告警等级（INFO/WARNING/ERROR/CRITICAL）决定通知渠道，不可自定义。

4. **API 集成（Grafana/自建系统）**：  
   - 获取 Prometheus HTTP API 地址（通过「模型监控配置」→「云监控 Prometheus 实例」→「查看详情」）；  
   - 使用标准 Prometheus Query API，例如：  
     ```http
     GET {API}/api/v1/query_range?query=model_usage{workspace_id="xxx",model="qwen-plus"}&start=2025-11-20T00:00:00Z&end=2025-11-20T23:59:59Z&step=60s
     Authorization: Basic base64Encode(AccessKey:AccessKeySecret)
     ```

## 限制和注意事项

- **地域限制**：高级监控、告警、推理日志功能仅在北京、新加坡、弗吉尼亚地域可用；上海地域仅支持普通监控。
- **模型兼容性**：并非所有模型支持推理日志，具体清单见[原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。不支持时界面提示“当前模型暂不支持日志”。
- **数据延迟**：  
  - 普通监控（用量汇总、失败率等）：小时级延迟，高峰期可达 1–2 小时；  
  - 高级监控（TPS、实时日志）：分钟级延迟；  
  - 免费额度数据：分钟级更新，支持手动刷新。
- **权限隔离**：子业务空间成员仅能查看本空间数据，无法跨空间筛选；主账号可查看全部空间。
- **用量查询范围**：模型用量页面（文档 1）**不支持查询 30 天以前的数据**；更早数据需通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)页面导出账单获取。
- **Token 计费口径差异**：不同模型类型（文本、视觉、语音、向量）的 Token 定义与计费单位不同，详见[模型用量统计单位说明](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


