# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标、成本消耗及异常事件。它覆盖从基础用量统计到细粒度推理日志的全链路数据采集，支持开发者快速定位性能瓶颈、成本异常和安全风险。该功能与[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)形成互补：前者侧重实时指标与告警，后者聚焦账单级用量汇总与免费额度管理。

## 支持的模型/功能

- **监控范围**：  
  - *普通监控*：支持所有在[模型列表](https://help.aliyun.com/zh/model-studio/models)中可选的模型（含基于其调优的[自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)）；  
  - *高级监控*（含分钟级延迟日志、TPS等指标）：仅限北京、上海、新加坡、弗吉尼亚地域下的模型；  
  - *告警功能*：仅支持北京、新加坡、弗吉尼亚地域模型。  

- **核心功能**：  
  - 调用记录追踪（含 Request ID、状态码、错误码）；  
  - 多维指标监控：RPM、TPM、调用时长、首 [Token](../concepts/token.md) 延时（TTFT）、非首 [Token](../concepts/token.md) 延时、失败率、内容安全错误次数、限流错误次数；  
  - [Token](../concepts/token.md) 消耗明细（单次调用级）与汇总（业务空间级）；  
  - 推理日志回流（支持将输入/输出日志导出为训练数据集）；  
  - 主动告警（支持短信、邮件、钉钉、Webhook 等通知方式）；  
  - Prometheus 数据源对接（支持 Grafana 可视化与自建应用集成）。  

> **注意**：文档 1 中称“模型用量页面数据延迟约为 1 小时”，而文档 2 明确区分了普通监控（小时级延迟）与高级监控（分钟级延迟）。实际使用中，若需分钟级洞察，请务必启用[高级监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)；否则默认普通监控无法满足实时性要求。

## 关键参数

| 参数类型 | 参数名 | 说明 | 来源 |
|----------|--------|------|------|
| **过滤标签（LabelKey）** | `workspace_id` | 业务空间 ID，用于按空间维度筛选数据 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `model` | 模型 Code（如 `qwen-plus`），必须与模型列表中一致 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `apikey_id` | API Key ID（非密钥本身），值为 `-1` 表示调用来自控制台 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC），影响延时与吞吐分析 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| **监控指标** | `model_usage` | Token 总消耗量（单位：Token） | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `model_call_duration_p99` | 调用时长 P99 分位值（毫秒） | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `model_first_token_duration` | 首 Token 延时均值（毫秒） | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | `model_tps_per_request` | 单次请求输出 Token 速度（TPS），**仅高级监控支持** | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

## 使用方式

1. **启用监控**：  
   - 进入目标业务空间的[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面；  
   - 点击右上角 **模型监控配置** → 开通 **审计日志** 和 **推理日志**（后者为查看请求/响应内容的必要前提）；  
   - 如需分钟级指标与告警，必须手动开启 **性能和用量指标监控**（即高级监控）。  

2. **查看数据**：  
   - 在模型监控列表中点击目标模型右侧的 **监控**，进入详情页查看调用统计与性能指标；  
   - 点击 **日志** 查看单次调用的输入、输出、用量及耗时（需已开通推理日志）；  
   - 在 **调用统计** 页签中，可通过 API Key、推理类型（实时/批量）、时间范围（支持分钟/小时精度）筛选。  

3. **配置告警**：  
   - 进入[模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert)页面；  
   - 点击 **创建告警规则**，选择模型、监控模板（如“失败率突增”或“Token 消耗超阈值”），设置阈值与通知方式；  
   - 告警等级（INFO/WARNING/ERROR/CRITICAL）决定通知渠道，不可自定义。  

4. **对接外部系统**：  
   - 获取 Prometheus HTTP API 地址（通过模型监控配置 → 云监控 Prometheus 实例 → 查看详情）；  
   - 使用 `GET /api/v1/query_range` 查询指标，例如：  
     ```http
     GET {API_URL}/api/v1/query_range?query=model_usage{workspace_id="llm-xxx",model="qwen-plus"}&start=2025-01-01T00:00:00Z&end=2025-01-01T23:59:59Z&step=60s
     Authorization: Basic base64Encode(AccessKey:AccessKeySecret)
     ```

## 限制和注意事项

- **地域限制**：高级监控、告警、推理日志（含请求/响应内容）仅在北京、新加坡、弗吉尼亚地域可用；上海地域仅支持普通监控（无分钟级日志与 TPS）。  
- **模型兼容性**：并非所有模型支持推理日志。支持列表见[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中“支持请求和响应的模型”章节；不支持时界面显示“当前模型暂不支持日志”。  
- **数据延迟**：  
  - 普通监控（用量汇总、失败率等）延迟约 1–2 小时；  
  - 高级监控（推理日志、TPS、分钟级趋势）延迟为分钟级；  
  - **历史数据补录不可行**：日志仅在开通后生效，开通前调用无记录。  
- **免费额度联动**：模型监控本身不控制免费额度开关，但可配合[免费额度用完即停](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)功能实现成本兜底——当监控发现 Token 消耗突增时，可人工关闭该开关避免超额计费。  
- **权限隔离**：子业务空间成员仅能查看本空间数据，无法跨空间切换；主账号可查看全部空间。  
- **批量推理支持**：模型监控目前**仅支持实时推理**的完整指标与日志；批量推理调用仅计入用量统计（见[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)），不提供单次调用级日志或性能指标。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


