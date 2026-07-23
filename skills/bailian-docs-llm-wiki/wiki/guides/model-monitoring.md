# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能表现、成本消耗及安全合规性。它支持从基础调用统计到高级指标告警的全链路监控，并提供推理日志回溯与 Prometheus 数据对接能力，适用于生产环境下的稳定性保障与精细化成本治理。

## 支持的模型与功能

- **监控覆盖范围**：  
  - 普通监控（免费）支持[选择模型](https://help.aliyun.com/zh/model-studio/models)中的所有模型，包括基于其调优的[自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)；  
  - 高级监控（收费）仅支持北京、上海、新加坡、弗吉尼亚地域下的模型；  
  - 告警功能仅支持北京、新加坡、弗吉尼亚地域（见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。  

- **关键功能模块**：  
  - 调用记录追踪（含 Request ID、状态码、错误码）；  
  - 四类核心指标监控：**安全**（如内容安全错误次数）、**成本**（如平均单次请求调用量）、**性能**（如调用时长、首[Token](../concepts/token.md)延时、TPS）、**错误**（如失败率、限流错误次数）；  
  - [Token](../concepts/token.md) 消耗细粒度统计（按业务空间、API Key、单次调用）；  
  - 推理日志（输入/输出内容）查看与回流为训练数据集；  
  - 主动告警（支持短信/邮件/钉钉/企业微信/Webhook）；  
  - Prometheus HTTP API 对接，支持 Grafana 可视化或自建系统集成。

> **注意**：文档 1 中称“高级监控支持北京、上海、新加坡、弗吉尼亚地域”，而文档 2 未提及上海地域支持情况；但文档 1 的告警说明明确限定为“北京、新加坡、弗吉尼亚”，且[模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中所有配置入口链接均未包含上海控制台路径。因此，**上海地域暂不支持告警与高级监控功能**，以文档 1 实际配置为准。

- **推理日志支持模型**（仅限开通后生效）：  
  包括 qwen3-max 系列、qwen-plus 系列、qwen-flash/turbo/coder 系列、部分开源模型（如 qwen3-235b-a22b）及三方模型（deepseek-v3.1/v3.2），详见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 中“支持请求和响应的模型”列表。不支持模型界面将提示“当前模型暂不支持日志”。

## 关键参数与指标

| 类别 | 指标名 | 说明 | 来源 |
|--------|---------|------|------|
| **调用统计** | `model_call_count` | 调用总次数 | [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| **性能** | `model_first_token_duration_p99` | 首[Token](../concepts/token.md)延时P99值 | [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| **性能** | `model_tps_per_request` | 单次请求输出TPS（每秒Token数），**仅高级监控支持** | [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| **用量** | `model_usage` | Token 总用量（输入+输出） | [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| **错误** | `model_call_failure_count` | 失败次数（含 429 限流、内容安全拦截等） | [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

> 所有指标均支持按 `workspace_id`、`model`、`apikey_id`、`protocol`（HTTP/SSE/WS）、`sub_protocol`（DEFAULT/ASYNC）等 Label 过滤，详见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 中“支持的过滤条件”。

## 使用方式

1. **启用监控**：  
   - 普通监控默认开启，数据延迟约 **1–2 小时**；  
   - 高级监控需手动开通：进入目标业务空间的[模型监控配置](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)，开启“性能和用量指标监控”；  
   - 推理日志需额外开通（审计日志 + 推理日志），开通后才记录请求/响应内容。

2. **查看数据**：  
   - 在[模型监控列表](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)中点击目标模型右侧「监控」进入详情页，分「调用统计」与「性能指标」页签；  
   - 点击「日志」可查看带 Token 用量、输入/输出内容的实时推理记录（仅支持模型且已开通日志）；  
   - Token 消耗可在「调用统计」页签的「调用量」区域直接查看，或通过[模型用量](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/usage-statistics)页面按业务空间聚合查询。

3. **配置告警**：  
   - 需先开启高级监控；  
   - 进入[模型告警页面](https://bailian.console.aliyun.com/?tab=model#/model-alert)，点击「创建告警规则」，选择模型、指标模板、阈值与通知方式；  
   - 告警等级（INFO/WARNING/ERROR/CRITICAL）决定可用通知渠道，不可自定义。

4. **对接外部系统**：  
   - 获取 Prometheus HTTP API 地址后，可通过标准 PromQL 查询指标，例如：  
     ```http
     GET {API}/api/v1/query_range?query=model_usage{workspace_id="llm-xxx",model="qwen-plus"}&start=2025-11-20T00:00:00Z&end=2025-11-20T23:59:59Z&step=60s
     ```
   - Authorization 使用 Base64 编码的 `AccessKey:AccessKeySecret`，且必须与 Prometheus 实例归属同一阿里云账号。

## 限制和注意事项

- **地域限制**：  
  - 高级监控、告警、推理日志功能**仅在北京、新加坡、弗吉尼亚地域可用**；上海地域目前不支持告警与高级监控（见上文注意项）；  
  - 推理日志查看功能在文档 1 中明确标注支持“华北2（北京）、新加坡、弗吉尼亚”，文档 2 未提及其地域约束，以文档 1 为准。

- **数据延迟**：  
  - 普通监控（调用次数、Token 总量）延迟 **1–2 小时**；  
  - 高级监控与推理日志延迟为**分钟级**；  
  - 免费额度数据更新为**分钟级**，账单费用数据按分钟汇总生成。

- **权限与可见性**：  
  - 默认业务空间成员可查看所有业务空间数据；子业务空间成员**仅能查看当前空间数据**，无法切换；  
  - 开通推理日志需主账号或具备 `AliyunBailianFullAccess` 权限的子账号。

- **历史数据限制**：  
  - 模型监控列表仅显示**最近 30 天**的 Token 消耗；更早数据需通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)页面查询；  
  - **未开通推理日志前的调用无请求/响应内容记录，且不可补录**。

- **模型兼容性**：  
  - 并非所有模型支持推理日志（如部分[多模态](../concepts/multi-modal.md)模型不支持），是否支持由模型本身决定，与是否为[多模态](../concepts/multi-modal.md)无关；  
  - TPS 指标（`model_tps_per_request`）**仅高级监控提供**，且其物理意义为“单次请求输出速度”，与 TPM（账号级限流）不同，排查慢响应需结合 TTFT、非首Token延时与输入长度综合分析。

## 来源文档

- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)
- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


