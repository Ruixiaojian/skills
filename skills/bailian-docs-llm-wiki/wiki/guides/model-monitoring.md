# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标与资源消耗。它支持从基础用量统计到分钟级延迟分析的全栈监控，并可基于关键指标（如失败率、TPM、首[Token](../concepts/token.md)延时）配置主动告警。该功能面向生产环境设计，帮助开发者快速定位异常、优化成本并保障服务稳定性。

## 支持的模型/功能

- **监控覆盖范围**：  
  - 普通监控支持[所有在模型列表中可选的模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)，包括基于它们调优后的自定义模型；  
  - 高级监控（含分钟级日志、TPS、Prometheus指标导出等）仅支持北京、上海、新加坡、弗吉尼亚地域下的模型；  
  - 告警功能目前仅支持北京、新加坡、弗吉尼亚地域下的模型。  

- **核心功能模块**：  
  - 调用记录追踪（含 Request ID、状态码、错误码）；  
  - 多维指标监控：RPM、TPM、调用时长、首[Token](../concepts/token.md)延时（TTFT）、非首[Token](../concepts/token.md)延时、失败率、限流错误次数、内容安全错误次数；  
  - Token 消耗精细化追踪（按次、按业务空间、按 API Key）；  
  - 推理日志回溯（输入/输出内容，需手动开通）；  
  - 基于 Prometheus 的自定义集成（Grafana / 自建应用）。  

> **注意**：文档 1 中称“模型用量数据延迟约为 1 小时”，而文档 2 明确区分了普通监控（小时级）与高级监控/推理日志（分钟级）——二者不矛盾，但需注意功能层级差异。实际使用中，若需分钟级洞察，请务必启用[高级监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识，所有监控数据按此维度隔离和聚合 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `model` | 模型 Code（如 `qwen-plus`），用于指标过滤与告警绑定 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `apikey_id` | API Key ID（非密钥本身），用于归因调用来源；值为 `-1` 表示来自控制台调用 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC），影响延迟与吞吐特征 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `max_tokens` | 控制输出长度的关键参数，直接影响 Token 消耗与费用，建议在生产调用中显式设置 | [模型用量 (统计单位说明)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |

## 使用方式

1. **基础监控查看**：  
   - 进入控制台 [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 页面，系统自动列出当前业务空间内已调用过的模型；  
   - 点击目标模型右侧「监控」，切换「调用统计」与「性能指标」页签，支持按 API Key、推理类型（实时/批量）、时间范围（最近30天）及时间精度（分钟/小时）筛选；  
   - 「调用量」区域直接展示 Token 消耗趋势，失败详情可点击图表下钻定位根因。

2. **开启高级能力（日志 + Prometheus）**：  
   - 在模型监控页面右上角点击「模型监控配置」，依次开通**审计日志**与**推理日志**（仅对开通后调用生效）；  
   - 开通后，点击「日志」页签即可查看请求/响应原文（支持模型见[文档 2 的“支持请求和响应的模型”章节](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）；  
   - 同一配置页中开启「性能和用量指标监控」，获取 Prometheus HTTP API 地址，用于 Grafana 可视化或自建系统集成。

3. **配置告警**：  
   - 进入 [模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert) 页面，点击「创建告警规则」；  
   - 选择模型、监控模板（如“失败率突增”、“TPM超阈值”），设置触发条件与通知渠道（短信/邮件/钉钉/企业微信/Webhook）；  
   - 告警等级分为 INFO / WARNING / ERROR / CRITICAL，不同等级对应不同通知方式，不可自定义。

## 限制和注意事项

- **数据时效性**：  
  - 普通监控（用量汇总、失败率等）延迟约 1–2 小时；  
  - 推理日志与高级监控指标为分钟级延迟，但需等待日志开通完成且调用发生后才可查；  
  - 历史数据仅保留最近 30 天，更早用量需通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)页面查询。

- **地域与模型限制**：  
  - 高级监控、告警、Prometheus 导出等功能**不支持杭州、深圳等非标地域**；  
  - 推理日志（请求/响应内容）**并非所有模型均支持**，具体清单以[文档 2 的“支持请求和响应的模型”章节](../../raw/model-user-guide/model-monitoring/model-telemetry.md)为准；不支持时界面明确提示“当前模型暂不支持日志”。

- **权限与范围**：  
  - 主账号可查看全部业务空间数据；子账号仅能访问其所属业务空间，无法跨空间切换；  
  - 开通推理日志需主账号或具备 `AliyunBailianFullAccess` 权限的子账号操作；  
  - 免费额度相关功能（如「免费额度用完即停」）仅在[免费额度](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)页面管理，与模型监控功能解耦。

- **其他重要约束**：  
  - Token 统计单位因模型类型而异（文本模型按 Token，图像按张，语音按秒等），详见[模型用量统计单位说明](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)；  
  - 批量推理调用**不产生推理日志**，仅计入用量统计；  
  - Prometheus 查询需使用与 Prometheus 实例同账号的 AccessKey，并进行 Base64 编码认证，凭证泄露风险需自行管控。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


