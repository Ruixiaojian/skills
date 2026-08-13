# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标、成本消耗及异常事件。它覆盖从基础用量统计到细粒度推理日志的全链路监控能力，支持开发者快速定位性能瓶颈、成本异常和稳定性问题。该功能分为普通监控（免费）与高级监控（需开通，支持分钟级延迟与Prometheus集成），适用于生产环境的日常运维与故障排查。

## 支持的模型/功能

- **监控范围**：  
  - 普通监控支持[所有在模型列表中可选的模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)，包括基于它们调优后的自定义模型；  
  - 高级监控（含推理日志、TPS、Grafana接入等）仅支持北京、上海、新加坡、弗吉尼亚地域下的模型；  
  - 告警功能目前仅支持北京、新加坡、弗吉尼亚地域下的模型。  

- **关键功能能力**：  
  - 调用记录追踪（含Request ID、状态码、错误码）；  
  - 多维指标监控：RPM、TPM、调用时长、首[Token](../concepts/token.md)延时（TTFT）、非首[Token](../concepts/token.md)延时、失败率、限流错误次数、内容安全错误次数；  
  - [Token](../concepts/token.md)消耗明细追踪（需开启推理日志）；  
  - 历史对话查看（输入/输出原文，仅限[指定模型列表](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）；  
  - 主动告警（支持短信/邮件/钉钉/企业微信/Webhook）；  
  - Prometheus指标导出与Grafana可视化接入。  

> **注意**：文档1中称“模型列表中的所有模型均支持查看用量”，但文档2明确指出**推理日志与请求/响应内容查看仅限部分模型**（如qwen3-max、qwen-plus等快照版本），且地域与开通状态强约束。实际能力以[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)文档为准，不可默认所有模型均支持日志级监控。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspace_id` | 业务空间ID，监控数据按此维度隔离与聚合 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `model` | 模型Code（如`qwen-plus`），用于指标过滤与告警绑定 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `apikey_id` | API Key ID（非密钥字符串），用于溯源调用方 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC），影响延时与吞吐统计口径 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `max_tokens` | 控制输出长度的关键参数，直接影响Token消耗与费用，建议在API调用中显式设置 | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |

## 使用方式

1. **基础监控访问**：  
   进入控制台 → [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)，默认展示当前业务空间下所有已调用模型的汇总卡片与表格。支持按API Key、推理类型（实时/批量）、时间范围（支持分钟/小时/天精度）筛选。

2. **开启高级能力（必选）**：  
   - 点击右上角「模型监控配置」→ 开通「审计日志」与「推理日志」（仅北京/新加坡/弗吉尼亚地域支持）；  
   - 开通后，日志与分钟级指标（如TPS、单次Token消耗）方可生效；未开通前的历史调用**无法补录**。

3. **查看细粒度数据**：  
   - 点击模型行「监控」→ 切换「调用统计」或「性能指标」页签；  
   - 点击「日志」→ 查看含输入/输出、用量、耗时的原始调用记录（仅支持模型见[文档2列表](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。

4. **创建告警**：  
   进入[模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert) → 「创建告警规则」→ 选择模型、指标模板（如“失败率突增”、“Token消耗超阈值”）→ 设置通知渠道与等级。

5. **Prometheus/Grafana接入**：  
   获取Prometheus HTTP API地址后，使用标准PromQL查询（如 `model_usage{workspace_id="xxx",model="qwen-plus"}`），详见[接入 Grafana 与自建应用](../../raw/model-user-guide/model-monitoring/model-telemetry.md)章节。

## 限制和注意事项

- **数据延迟**：  
  - 普通监控（用量汇总、失败率等）延迟约**1–2小时**；  
  - 高级监控（推理日志、TPS、单次用量）为**分钟级延迟**，但需等待日志开通后首次调用完成同步。

- **地域与模型限制**：  
  - 推理日志、TPS指标、Grafana接入、告警功能**仅限北京/新加坡/弗吉尼亚地域**；  
  - 上海地域仅支持普通监控（无日志、无TPS、无告警）；  
  - 并非所有模型支持请求/响应内容记录，具体支持列表以[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)为准。

- **权限与范围**：  
  - 主账号可查看所有业务空间数据；子账号仅能查看其所属业务空间的数据；  
  - 免费额度管理（如「免费额度用完即停」开关）仅对**仍有未消耗额度的模型**生效，额度耗尽后需先关闭再重新开启。

- **用量统计差异**：  
  - 模型用量页面（[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）按**业务空间维度**统计，不支持账号级汇总；  
  - Token统计单位因模型类型而异（文本模型按Token、图像模型按张、语音模型按秒/字符），详见[模型用量统计单位说明](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


