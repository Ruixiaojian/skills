# model monitoring

模型监控（Model Monitoring）是百炼平台提供的核心可观测性能力，用于实时追踪模型调用行为、性能指标、成本消耗及安全风险。它覆盖从基础用量统计到高级推理日志分析的全链路监控场景，支持开发者快速定位异常、优化成本并保障服务稳定性。该功能与[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)形成互补：前者侧重实时指标与告警，后者侧重账单级用量汇总与免费额度管理。

## 支持的模型/功能

- **监控范围**：  
  - 普通监控支持所有在[模型列表](https://help.aliyun.com/zh/model-studio/models)中可选的模型（含调优后的自定义模型）；  
  - 高级监控（含分钟级延迟日志、TPS、非首[Token](../concepts/token.md)延时等）仅支持北京、上海、新加坡、弗吉尼亚地域下的模型；  
  - 告警功能目前仅覆盖北京、新加坡、弗吉尼亚地域（见 [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。  

- **关键功能能力**：  
  - 调用记录追踪（含 Request ID、状态码、错误码）；  
  - 多维指标监控：RPM、TPM、调用时长、首[Token](../concepts/token.md)延时（TTFT）、非首[Token](../concepts/token.md)延时、失败率、限流错误次数、内容安全错误次数；  
  - Token 消耗细粒度追踪（单次调用级）与汇总；  
  - 推理日志回流（支持将输入/输出日志导出为训练数据集）；  
  - 主动告警（支持短信/邮件/钉钉/企业微信/Webhook）；  
  - Prometheus API 对接，支持 Grafana 可视化与自建系统集成。

> **注意**：文档1中称“模型用量页面数据延迟约为 1 小时”，而文档2明确区分普通监控（小时级延迟）与高级监控（分钟级延迟）。二者并非矛盾，而是分层设计：用量统计（如 `model_usage`）属账单聚合层，监控指标（如 `model_call_duration_p99`）属实时观测层。实际使用中应按需选择——成本审计用用量页面，故障排查用高级监控日志。

## 关键参数

| 参数类别 | 参数名 | 说明 | 来源 |
|----------|--------|------|------|
| **通用筛选** | `workspace_id` | 业务空间ID，监控数据按此维度隔离 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `apikey_id` | API Key ID（非密钥本身），值为 `-1` 表示控制台调用 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `model` | 模型 Code（如 `qwen-plus`），区分大小写 | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| **性能指标** | `model_first_token_duration_p99` | 首Token延时P99值（毫秒） | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `model_generation_duration_per_token` | 非首Token平均生成耗时（毫秒/Token） | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `model_tps_per_request` | 单次请求输出TPS（仅高级监控支持） | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| **成本指标** | `model_usage` | Token 总用量（单位：Token） | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| | `max_tokens` | API 请求中显式设置的输出长度上限，直接影响 Token 消耗 | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |

## 使用方式

1. **启用基础监控**：  
   - 登录控制台 → 进入 [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 页面 → 系统自动同步已调用模型（首次同步延迟约1小时）。

2. **开通高级监控与日志**（必需步骤，否则无法查看单次调用详情）：  
   - 在目标业务空间的模型监控页右上角点击 **模型监控配置** → 开通 **审计日志** 和 **推理日志**（仅北京/新加坡/弗吉尼亚地域支持）→ 开通后分钟级生效。

3. **查看指标与日志**：  
   - 在模型列表点击对应模型操作列的 **监控** → 查看安全/成本/性能/错误四类指标；  
   - 点击 **日志** → 查看含 `Request ID`、`用量`（Token数）、`请求`（输入）、`响应`（输出）的明细表（仅[支持的模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)可用）。

4. **创建告警规则**：  
   - 进入 [模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert) 页面 → 点击 **创建告警规则** → 选择模型、指标（如 `model_call_duration_p99 > 5000`）、阈值、通知方式。

5. **对接 Prometheus/Grafana**：  
   - 获取 Prometheus HTTP API 地址（通过模型监控配置页）→ 使用 `Authorization: Basic <base64(AK:SK)>` 调用 `/api/v1/query_range` → 示例查询：`model_usage{workspace_id="xxx",model="qwen-plus"}`（见 [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。

## 限制和注意事项

- **地域限制**：高级监控、推理日志、告警、Prometheus API 仅在北京、新加坡、弗吉尼亚地域可用；上海地域暂不支持高级监控（文档2提及“上海”但未说明能力，以控制台实际选项为准）；其他地域仅提供基础用量统计（见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

- **数据时效性**：  
  - 普通监控（用量汇总、失败率等）延迟约 1–2 小时；  
  - 高级监控（日志、TPS、P99等）延迟为分钟级；  
  - 免费额度状态在控制台分钟级更新，但账单数据以控制台显示为准（见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

- **日志覆盖范围**：  
  - 推理日志仅记录开通后的新调用，历史调用不可追溯；  
  - 并非所有模型支持请求/响应内容记录（如部分多模态模型或旧版快照），具体支持列表见 [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

- **免费额度联动**：  
  - “免费额度用完即停”开关开启后，服务将在额度耗尽时返回 `403 AllocationQuota.FreeTierOnly`；该机制独立于监控告警，需配合用量监控提前预警（见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

- **计费单位差异**：  
  - 大语言模型按 Token 计费；图像生成按张；视频生成按秒；语音模型按秒/字符/Token（依模型而定）；全模态模型按各模态对应 Token 数（见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


