# model monitoring

模型监控（Model Monitoring）是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标、成本消耗及异常事件。它面向生产环境提供细粒度的调用日志、多维指标监控与主动告警能力，帮助开发者快速定位问题、优化成本并保障服务稳定性。该功能覆盖模型生命周期中的推理阶段，不涉及训练或部署过程的监控。

## 支持的模型/功能

- **监控范围**：普通监控支持[所有在模型列表中可选的模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)，包括基于其调优的自定义模型；高级监控（含分钟级延迟、TPS、推理日志等）仅支持北京、上海、新加坡、弗吉尼亚地域下的模型。  
- **核心功能**：  
  - 调用记录追踪（含 Request ID、状态码、错误码）  
  - 多维指标监控：RPM、TPM、调用时长、首 [Token](../concepts/token.md) 延时（TTFT）、非首 [Token](../concepts/token.md) 延时、失败率、限流错误次数、内容安全错误次数  
  - [Token](../concepts/token.md) 消耗统计（按业务空间、API Key、时间维度汇总与单次调用粒度）  
  - 推理日志回溯（输入/输出内容，需手动开通）  
  - 主动告警（支持失败率突增、Token 异常消耗、延迟超标等场景）  
  - Prometheus 数据导出（支持 Grafana 可视化与自建系统集成）  

> **注意**：文档 1 中称“模型用量页面数据延迟约为 1 小时”，而文档 2 明确区分了普通监控（小时级）与高级监控（分钟级）的数据延迟。实际使用中，若需分钟级洞察，必须启用[高级监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)；否则默认为小时级汇总，二者不可混用。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识，用于隔离监控数据范围，不支持跨空间聚合 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `apikey_id` | API Key 的唯一 ID（非密钥本身），用于按调用来源归因；值为 `-1` 表示来自控制台调用 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `model` | 模型 Code（如 `qwen-plus`），区分大小写，需与模型列表中完全一致 | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC），影响延时与吞吐统计口径 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `max_tokens` | 控制输出长度的关键参数，直接影响 Token 消耗与费用，建议在生产调用中显式设置 | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |

## 使用方式

1. **启用监控**：  
   - 普通监控默认开启；高级监控需在目标业务空间的[模型监控配置](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中手动开启“性能和用量指标监控”。  
   - 推理日志（含请求/响应内容）需单独开通，仅对[明确支持的模型列表](../../raw/model-user-guide/model-monitoring/model-telemetry.md)生效，开通前调用无法补录。

2. **查看数据**：  
   - 模型级概览：访问[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)列表，按模型 Code 和业务空间筛选。  
   - 细粒度指标：点击模型操作列的「监控」，切换「调用统计」与「性能指标」页签，支持按 API Key、推理类型（实时/批量）、时间范围（最大 30 天）和精度（分钟/小时）筛选。  
   - 单次调用详情：点击「日志」页签，在表格中查看 `用量` 字段（Token 数）及 `请求和响应` 内容（需模型支持且日志已开通）。

3. **配置告警**：  
   - 进入[模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert)页面，创建规则时选择监控模板（如“Token 消耗突增”、“失败率超阈值”），指定通知渠道（钉钉/邮件/Webhook 等）与告警等级。  
   - 告警仅支持北京、新加坡、弗吉尼亚地域，上海地域暂未开放告警功能。

4. **对接自建系统**：  
   - 获取 Prometheus HTTP API 地址后，通过标准 `/api/v1/query_range` 接口拉取指标，例如：  
     ```http
     GET {API}/api/v1/query_range?query=model_usage{workspace_id="xxx",model="qwen-plus"}&start=...&end=...&step=60s
     ```

## 限制和注意事项

- **时间范围限制**：  
  - 监控界面最多查询最近 **30 天** 数据；更早历史用量需通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)页面导出账单获取。  
  - 分钟级精度仅支持 ≤1 天时间跨度；>7 天仅支持按天查看。

- **地域与模型限制**：  
  - 推理日志（含输入/输出内容）仅支持北京、新加坡、弗吉尼亚地域，且仅限[文档 2 明确列出的模型版本](../../raw/model-user-guide/model-monitoring/model-telemetry.md)，其他模型即使开通日志也无法记录内容。  
  - 上海地域当前仅支持普通监控，不支持高级监控与告警。

- **数据延迟与一致性**：  
  - 普通监控（用量汇总、失败率等）延迟为 **1–2 小时**；高级监控（推理日志、TPS 等）为 **分钟级**。  
  - 免费额度状态更新与用量统计存在异步刷新机制，控制台显示数值为准，账单数据可能存在分钟级偏差。

- **权限与范围**：  
  - 主账号可查看全部业务空间数据；子业务空间成员仅能访问本空间数据，无法跨空间切换。  
  - 开通高级监控与推理日志需主账号或具备 `AliyunBailianFullAccess` 权限的子账号操作。

- **成本提示**：  
  - 高级监控与推理日志为**收费功能**，启用后将按量计费；普通监控免费。  
  - Token 计费以模型实际输入/输出分词结果为准，中文平均 1.5–2 Token/字，英文单词约 1.3 Token/词，详见[模型用量统计单位说明](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


