# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标与资源消耗。它支持从基础用量统计到细粒度推理日志的全链路监控，并可基于关键指标（如失败率、首[Token](../concepts/token.md)延时、TPM）配置主动告警。该功能面向生产环境运维与成本治理场景，为开发者提供分钟级（高级监控）或小时级（普通监控）的数据洞察。

## 支持的模型/功能

- **监控覆盖范围**：  
  - 普通监控支持[所有在模型列表中可选的模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)，包括基于其调优的自定义模型；  
  - 高级监控（含推理日志、TPS、Grafana接入等）仅支持北京、上海、新加坡、弗吉尼亚地域下的模型；  
  - 告警功能当前仅支持北京、新加坡、弗吉尼亚地域的模型。  

- **核心功能能力**：  
  - 调用记录追踪（含 Request ID、状态码、错误码）；  
  - 多维指标监控：RPM、TPM、调用时长、首[Token](../concepts/token.md)延时（TTFT）、非首[Token](../concepts/token.md)延时、失败率、限流错误次数、内容安全错误次数；  
  - Token 消耗明细追踪（需开通推理日志）；  
  - 历史对话查看（输入/输出原文），但**仅限指定快照版本的千问系列及部分开源/三方模型**（详见 [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 中“支持请求和响应的模型”列表）；  
  - 告警规则创建与多通道通知（短信/邮件/钉钉/企业微信/Webhook）；  
  - Prometheus HTTP API 对接，支持 Grafana 可视化或自建系统集成。

> **注意**：文档1中提及“模型用量页面数据延迟约为1小时”，而文档2明确区分了普通监控（小时级）与高级监控（分钟级）的延迟差异。实际使用中，若需分钟级洞察（如故障排查），必须启用[高级监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)，否则无法满足低延迟需求。

## 关键参数

| 参数类别 | 参数名 | 说明 | 来源依据 |
|----------|--------|------|----------|
| **过滤维度** | `workspace_id` | 业务空间ID，监控数据按“模型 + 业务空间”聚合 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `model` | 模型Code（如 `qwen-plus`），区分大小写 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `apikey_id` | API Key ID（非密钥本身），值为 `-1` 表示控制台调用 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC） | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| **监控指标** | `model_usage` | Token 总消耗量（单位：Token） | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `model_call_duration_p99` | 调用时长P99分位值（毫秒） | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `model_first_token_duration` | 首Token延时均值（毫秒） | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `model_tps_per_request` | 单次请求输出TPS（仅高级监控支持） | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| **用量统计单位** | Token / 张 / 秒 / 字符 | 不同模型类型计费单位不同（如文本生成按Token，图像生成按张） | [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |

## 使用方式

1. **基础监控查看**：  
   - 进入 [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 页面，选择目标业务空间；  
   - 在“模型监控”表格中定位模型，点击 **监控** 查看调用统计与性能指标（支持按API Key、推理类型、时间范围筛选）；  
   - 点击 **日志** 查看已开通推理日志的调用记录（含用量、请求/响应原文）。

2. **开通高级能力**：  
   - 在模型监控页右上角点击 **模型监控配置** → 开启 **审计日志** 和 **推理日志**（仅北京/新加坡/弗吉尼亚地域支持）；  
   - 开通后，日志数据延迟约 **1–3 分钟**，历史调用不补录；  
   - 开启 **性能和用量指标监控** 后，方可使用 TPS 指标与 Prometheus API。

3. **配置告警**：  
   - 进入 [模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert) 页面；  
   - 点击 **创建告警规则**，选择模型、指标模板（如“失败率突增”、“Token消耗超阈值”）；  
   - 设置阈值、周期、通知方式与告警等级（CRITICAL/ERROR/WARNING/INFO）。

4. **对接自建系统**：  
   - 通过 Prometheus HTTP API 查询指标（如 `GET {prometheus_api}/api/v1/query_range?query=model_usage{model="qwen-plus"}&start=...&step=60s`）；  
   - 认证需使用 Base64 编码的 `AccessKey:AccessKeySecret`；  
   - 支持按 `workspace_id`、`apikey_id`、`protocol` 等 label 过滤，详见 [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 限制和注意事项

- **地域限制**：高级监控、推理日志、告警、Prometheus API 仅在北京、新加坡、弗吉尼亚地域可用；上海地域目前仅支持普通监控（小时级延迟）。  
- **模型兼容性**：并非所有模型支持推理日志（请求/响应内容），具体支持列表以 [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 中“支持请求和响应的模型”为准；不支持的模型在日志页签会显示“当前模型暂不支持日志”。  
- **数据时效性**：  
  - 普通监控（用量汇总、失败率等）延迟 **1–2 小时**；  
  - 高级监控（推理日志、TPS、实时指标）延迟 **1–3 分钟**；  
  - 模型用量页面（[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）同样存在约1小时延迟，且不支持查询30天以前数据。  
- **权限约束**：子业务空间成员只能查看本空间数据；主账号或具备 `AliyunBailianFullAccess` 权限的RAM用户才能开通日志与高级监控。  
- **免费额度联动**：“免费额度用完即停”开关仅影响计费行为，**不影响监控数据采集**——即使额度耗尽导致403错误，调用失败事件仍会被记录在监控与日志中。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


