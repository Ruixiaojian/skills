# model monitoring

阿里云百炼平台提供模型监控与用量管理能力，帮助开发者追踪模型调用的性能指标、Token 消耗及历史对话记录。通过监控与告警机制，开发者可以及时发现调用异常、控制成本，并将监控数据接入 Grafana 等第三方工具进行可视化分析。

## 功能概览

模型监控包含以下核心能力：

| 功能 | 说明 |
|------|------|
| **调用记录查看** | 查看每次模型调用的输入、输出及耗时 |
| **指标监控** | Token 延时、调用时长、RPM、TPM、失败率等 |
| **Token 消耗统计** | 按业务空间汇总或追踪单次调用的 Token 消耗 |
| **用量统计** | 查看各模型的调用量和免费额度使用情况 |
| **告警** | 对成本、失败率、响应延迟等指标设置主动告警 |
| **Grafana/自建应用接入** | 通过 Prometheus HTTP API 获取监控数据 |

## 支持的模型与地域

根据[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)文档，不同功能的模型支持范围如下：

- **普通监控**：支持[模型列表](https://help.aliyun.com/zh/model-studio/models)中的所有模型，包括调优后的自定义模型。
- **高级监控**：支持北京、新加坡、弗吉尼亚地域下的所有模型。
- **告警功能**：仅支持北京、新加坡地域。
- **日志功能**：仅支持北京地域和新加坡地域的部分模型（如 qwen3-max、qwen-max、qwen-plus、qwen-turbo、deepseek-v3 系列等）。

[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)功能则支持所有模型的用量查看。

## 用量统计

### 统计单位

不同类型模型的用量统计口径不同：

| 模型类型 | 统计单位 |
|----------|----------|
| 大语言模型（文本生成/深度思考/视觉理解） | Token |
| 图像生成 | 张 |
| 视频生成 | 秒 |
| 语音模型 | 秒、字符或 Token（视模型而定） |
| 全模态模型 | Token |
| 向量模型 | Token |

### 查看用量

- 在控制台的**用量统计**页面查看，数据按业务空间维度统计，延迟约 **1 小时**。
- **时间范围限制**：仅支持查看最近 **30 天**的数据。更早的用量需通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)页面查询。
- 仅「大语言模型」页签支持按推理类型（实时推理/批量推理）筛选。

### 免费额度管理

在控制台的**免费额度**页面可查看各模型的免费额度使用情况，并可开启**免费额度用完即停**开关。开启后，免费额度耗尽时服务自动停止（返回 403 错误 `AllocationQuota.FreeTierOnly`）。

> **注意**：免费额度出账周期为分钟级，但控制台显示的免费额度数据非实时，可能存在延迟。

## 监控指标与对话日志

### 四类监控指标

在模型监控列表中点击**监控**，可查看以下指标：

- **安全**：内容安全错误次数等
- **成本**：平均单次请求调用量等
- **性能**：调用时长、首 Token 延时、RPM、TPM 等
- **错误**：失败次数、失败率、限流错误次数等

支持按 API-KEY、推理类型和时间范围进行筛选。

### 查看历史对话（模型日志）

需先在模型监控配置中依次开通**审计日志**和**推理日志**，开通后系统记录每次模型调用的输入与输出，存在分钟级延迟。

> **注意**：日志功能目前仅适用于华北2（北京）和新加坡地域的部分模型。

## 告警配置

根据[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)文档，告警配置步骤如下：

1. **开启高级监控**：在模型监控配置中开启「性能和用量指标监控」。
2. **创建告警规则**：在模型告警页面选择要监控的模型和监控模板。

**通知方式**：短信、邮件、电话、钉钉群机器人、企业微信机器人、Webhook。

**告警等级与通知渠道**：

| 等级 | 通知渠道 |
|------|----------|
| 紧急（CRITICAL） | 电话、短信、邮件 |
| 错误（ERROR） | 短信、邮件 |
| 警告（WARNING） | 短信、邮件 |
| 普通（INFO） | 邮件 |

## 接入 Grafana 与自建应用

高级监控的数据存储在私有 Prometheus 实例中，支持标准 Prometheus HTTP API。

**关键监控指标（PromQL）**：

| 指标名称 | 描述 |
|----------|------|
| `model_call_count` | 调用次数总和 |
| `model_call_duration` | 调用时长均值 |
| `model_first_token_duration` | 首包时长均值 |
| `model_usage` | 模型用量总和 |

**请求示例**：

```
GET {HTTP_API}/api/v1/query_range?query=model_usage{workspace_id="llm-xxx",model="qwen-plus"}&start=2025-11-20T00:00:00Z&end=2025-11-20T23:59:59Z&step=60s
Authorization: Basic base64Encode(AccessKey:AccessKeySecret)
```

支持的过滤条件（LabelKey）包括：`user_id`、`apikey_id`、`workspace_id`、`model`、`protocol`、`status_code`、`error_code`、`usage_type` 等。

## 生产环境最佳实践

根据[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)文档的建议：

- **控制输出长度**：合理设置 `max_tokens` 参数和限制思考长度。
- **按任务选模型**：简单任务优先使用轻量级模型（如 `qwen-turbo`）。
- **监控与告警**：配置用量告警，及时发现异常。
- **优化 Prompt**：减少不必要的输入 Token 消耗。
- **使用批量推理**：非实时大批量任务使用批量推理，成本更低。

## 限制与注意事项

- 用量统计数据按**业务空间**维度统计，不支持按阿里云账号维度直接统计；如需账号级汇总，可导出账单查看。
- 普通监控数据延迟为**小时级**，高级监控为**分钟级**。
- 用量统计页面数据延迟约 **1 小时**，且仅保留最近 **30 天**数据。
- 日志功能和告警功能存在地域限制（详见上文支持范围）。
- 默认业务空间成员可查看所有空间数据；子业务空间成员仅能查看当前空间数据。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


