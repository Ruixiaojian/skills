# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能表现、成本消耗及安全合规状态。它覆盖从基础调用统计到分钟级延迟指标的全维度数据采集，并支持告警、日志回溯与外部系统集成。该功能面向生产环境运维与成本治理场景，为开发者提供可操作的诊断依据和自动化响应能力。

## 支持的模型/功能

- **监控范围**：普通监控支持[选择模型](https://help.aliyun.com/zh/model-studio/models)中的所有模型（含基于其调优的[自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)）；高级监控与告警功能仅限北京、上海、新加坡、弗吉尼亚地域下的模型（详见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。  
- **日志能力**：推理日志（含请求/响应内容）仅对特定模型开放，包括 `qwen3-max` 系列、`qwen-plus` 系列、`qwen-flash`、`qwen-turbo`、`qwen3-coder-*`、开源模型（如 `qwen3-235b-a22b-*`）及三方模型（如 `deepseek-v3.1` 等），具体支持列表见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **用量统计**：所有模型均支持用量查看，包括 Token、图像张数、视频秒数等不同计量单位，详细口径参见 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

> **注意**：文档1称“高级监控支持北京、上海、新加坡、弗吉尼亚地域”，而文档2未提上海地域；但文档1在“建立主动告警”章节明确说明“该功能目前适用于新加坡、北京和弗吉尼亚地域”，未包含上海。因此，**上海地域暂不支持告警与高级监控功能**，以文档1的告警章节为准。

## 关键参数

| 参数类型 | 参数名 | 说明 | 来源 |
|----------|--------|------|------|
| 过滤标签（LabelKey） | `workspace_id` | 业务空间ID，必需用于精确筛选 | [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `model` | 模型Code，如 `qwen-plus` | 同上 |
| | `apikey_id` | API Key ID（非密钥本身），值为 `-1` 表示来自控制台调用 | 同上 |
| | `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC） | 同上 |
| Prometheus指标 | `model_usage` | Token总用量（高级监控） | 同上 |
| | `model_call_duration_p99` | 调用时长P99分位值 | 同上 |
| | `model_first_token_duration` | 首Token延时均值 | 同上 |
| | `model_tps_per_request` | 单次请求输出TPS（仅高级监控） | 同上 |

## 使用方式

- **基础监控访问**：登录控制台 → 进入目标业务空间 → 访问 [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 页面，查看模型总量、失败率、平均调用时长等汇总卡片及表格。  
- **深度指标分析**：点击模型操作列的「监控」，切换至「调用统计」或「性能指标」页签，按 API Key、推理类型（实时/批量）、时间范围（支持分钟/小时/天精度）筛选；其中「调用统计」聚焦安全、成本、错误类指标，「性能指标」展示 RPM、TPM、首/非首Token延时等。  
- **Token消耗追踪**：在「调用统计」页签的「调用量」区域查看近30天Token汇总；单次调用明细需开通推理日志后，在「日志」页签的「用量」列中获取（仅限北京、新加坡、弗吉尼亚地域支持）。  
- **告警配置**：需先开启高级监控（模型监控配置 → 性能和用量指标监控），再进入 [模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert) 页面创建规则，支持短信、邮件、钉钉机器人等通知方式。  
- **Grafana/自建集成**：通过Prometheus HTTP API拉取指标，需使用同一阿里云账号的 AccessKey/Secret Base64编码认证，API地址在「模型监控配置 → 云监控Prometheus实例 → 查看详情」中获取。

## 限制和注意事项

- **数据延迟**：普通监控（调用次数、Token总量）延迟约1–2小时；推理日志（请求/响应内容）为分钟级延迟；费用类数据（如账单）延迟约1小时。  
- **地域与模型限制**：推理日志、高级监控、告警功能**仅在北京、新加坡、弗吉尼亚地域可用**；上海地域当前不支持告警（见上文注意项）；部分模型（如旧版 `qwen2.5` 或非列表内模型）不支持请求/响应记录，界面将提示“当前模型暂不支持日志”。  
- **日志开通要求**：推理日志仅记录开通**之后**的调用，历史调用无法补录；开通前需确保主账号或具备足够权限的子账号操作（参见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。  
- **用量统计边界**：模型用量按业务空间维度聚合，**不支持跨空间或按阿里云账号全局统计**；30天以外的数据需通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)页面查询。  
- **TPS指标说明**：`model_tps_per_request` 仅在高级监控中提供，其值 ≈ 1 ÷ `model_generation_duration_per_token`（非首Token延时均值），但单次总耗时还受输入长度、网络等因素影响，不可单独用于性能归因。

## 来源文档

- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)
- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


