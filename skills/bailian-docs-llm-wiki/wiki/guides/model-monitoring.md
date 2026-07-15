# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标、成本消耗及异常事件。它面向生产环境提供细粒度的调用统计、多维指标监控、日志审计与主动告警能力，帮助开发者快速定位问题、优化成本并保障服务稳定性。该功能以业务空间为数据边界，默认按小时级聚合，高级监控支持分钟级洞察与 Prometheus 标准对接。

## 支持的模型与功能

- **监控覆盖范围**：普通监控支持[所有公开模型及调优后的自定义模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)，包括大语言模型（如 `qwen-plus`、`qwen3-max`）、视觉模型、语音模型、全模态模型和向量模型；高级监控与告警功能当前仅限北京、新加坡、弗吉尼亚地域的模型（详见 [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。
- **核心功能**：
  - **调用追踪**：记录请求/响应（限北京地域部分模型，见[支持请求和响应的模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）；
  - **指标监控**：RPM、TPM、调用时长、首[Token](../concepts/token.md)延时、失败率、限流错误次数（429）、内容安全错误次数等；
  - **[Token](../concepts/token.md) 消耗分析**：按业务空间维度汇总与单次调用级追踪（输入/输出/缓存/图像/音频/视频等细分用量类型）；
  - **主动告警**：支持对成本突增、失败率飙升、延迟超阈值等场景配置多级通知（短信/邮件/钉钉/企业微信/Webhook）；
  - **Grafana 与自建集成**：通过私有 Prometheus HTTP API 开放全部监控指标，支持标准 PromQL 查询（如 `model_usage{model="qwen-plus", workspace_id="..."}`）。

> **注意**：文档1中“模型用量”页面的数据延迟为“约1小时”，而文档2明确区分普通监控（小时级）与高级监控（分钟级）。二者不矛盾，但需注意：**普通监控无法满足实时诊断需求，分钟级洞察必须启用[高级监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)**。

## 关键参数与指标

| 类别 | 指标名（Prometheus） | 说明 | 过滤标签（LabelKey）示例 |
|--------|----------------------|------|---------------------------|
| 调用统计 | `model_call_count` | 调用总次数 | `apikey_id`, `status_code`, `error_code` |
| 性能 | `model_call_duration_p99` | 调用时长P99 | `workspace_id`, `model`, `protocol` |
| 首[Token](../concepts/token.md)延时 | `model_first_token_duration` | 首包平均耗时 | `sub_protocol`（DEFAULT/ASYNC） |
| 用量 | `model_usage` | Token/图像张数/视频秒数等总和 | `usage_type`（`input_tokens`, `image_count`, `video_seconds` 等） |

- `usage_type` 是关键过滤维度，取值包括 `total_tokens`、`input_tokens`、`output_tokens`、`cache_tokens`、`image_count`、`audio_count`、`video_count`、`duration`、`characters` 等，需结合模型类型选择（参见[模型用量统计单位说明](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。
- 所有指标均支持按 `workspace_id`、`model`、`apikey_id` 维度下钻，**不支持跨业务空间聚合或阿里云账号维度统计**（该限制在两篇文档中一致）。

## 使用方式

1. **基础监控查看**  
   进入控制台 [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 页面 → 选择业务空间 → 查看「监控数据看板」及「模型监控」表格 → 点击目标模型操作列的 **监控** 或 **日志**。

2. **启用高级能力（必选步骤）**  
   - 在模型监控页面右上角点击 **模型监控配置** → 开启 **性能和用量指标监控**（高级监控）；
   - 如需日志审计（输入/输出详情），需额外开通 **审计日志** 和 **推理日志**（仅北京地域生效，且仅限[指定模型列表](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。

3. **创建告警规则**  
   进入 [模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert) 页面 → 点击 **创建告警规则** → 选择模型、模板、阈值与通知渠道（注意：告警功能仅在北京、新加坡地域可用）。

4. **接入 Grafana / 自建系统**  
   - 获取 Prometheus HTTP API 地址（通过「模型监控配置」→「云监控Prometheus实例」→「查看详情」）；
   - 使用 `Authorization: Basic base64Encode(AccessKey:AccessKeySecret)` 认证；
   - 构造标准 PromQL 查询，例如：  
     `GET {API}/api/v1/query_range?query=model_usage{model="qwen-plus",usage_type="input_tokens"}&start=...&end=...&step=60s`

## 限制和注意事项

- **地域限制**：日志审计（请求/响应内容）、分钟级监控、告警功能仅支持 **华北2（北京）** 和 **新加坡** 地域；弗吉尼亚仅支持分钟级监控与 Prometheus 对接，**不支持告警与日志审计**。
- **数据时效性**：普通监控数据延迟约1小时；高级监控数据延迟为分钟级（通常 ≤5 分钟），但日志从调用发生到可查存在分钟级延迟，需手动刷新。
- **用量查询范围**：控制台内模型用量与监控页的 Token 消耗均**仅支持查询最近30天数据**；更早数据需通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)页面导出账单获取。
- **权限隔离**：子业务空间成员**仅能查看本空间数据**，无法切换或跨空间筛选；主账号可查看全部空间。
- **Token 计费口径差异**：不同模型类型计费单位不同（Token/张/秒/字符），务必参考[模型用量统计单位说明](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)匹配 `usage_type` 标签，避免误读指标。
- **免费额度联动**：“免费额度用完即停”开关仅影响计费行为，**不影响监控数据采集**；即使额度耗尽，监控仍持续记录调用与失败（如返回 403 错误），可用于故障归因。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


