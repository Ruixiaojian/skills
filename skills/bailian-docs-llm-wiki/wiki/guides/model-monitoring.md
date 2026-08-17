# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标与资源消耗。它支持从基础用量统计到分钟级推理日志的全链路观测，并可基于关键指标（如失败率、首[Token](../concepts/token.md)延时、TPM）配置主动告警。该功能面向生产环境运维与成本治理场景，为模型服务稳定性、安全性和成本优化提供数据依据。

## 支持的模型/功能

- **监控覆盖范围**：  
  - 普通监控支持[所有在模型列表中可选的模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)，包括基于它们调优后的自定义模型；  
  - 高级监控（含分钟级日志、TPS、Prometheus指标导出）仅支持北京、上海、新加坡、弗吉尼亚地域下的模型；  
  - 告警功能仅支持北京、新加坡、弗吉尼亚地域下的模型。  

- **核心功能能力**：  
  - 调用记录追踪（含 Request ID、状态码、错误码）；  
  - 多维指标监控：RPM、TPM、调用时长、首[Token](../concepts/token.md)延时（TTFT）、非首[Token](../concepts/token.md)延时（ITL）、失败率、限流错误次数、内容安全错误次数；  
  - Token 消耗明细（按次、按模型、按业务空间、按 API Key 维度）；  
  - 推理日志回溯（输入/输出内容，需手动开通）；  
  - 告警规则配置（支持短信/邮件/钉钉/企业微信/Webhook）；  
  - Prometheus HTTP API 对接，支持 Grafana 可视化与自建系统集成。  

> **注意**：文档1中称“模型用量页面数据延迟约为 1 小时”，而文档2明确区分普通监控（小时级延迟）与高级监控（分钟级延迟），且强调“推理日志从调用发生到可查询存在分钟级延迟”。二者不矛盾，但需注意：**用量统计（如总调用次数）与日志内容（如请求/响应体）属于不同数据通道，延迟策略不同**。实际使用中应以[模型监控 (model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)所述的高级监控能力为准获取低延迟数据。

## 关键参数

| 参数 | 说明 | 来源依据 |
|------|------|----------|
| `workspace_id` | 业务空间唯一标识，所有监控数据按此维度隔离与聚合 | [模型监控 (model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 中 Prometheus 查询示例及说明 |
| `model` | 模型 Code（如 `qwen-plus`, `qwen3-flash`），用于指标过滤与日志筛选 | 同上，见 `model_usage{workspace_id="...",model="..."}` 示例 |
| `apikey_id` | API Key 的唯一 ID（非密钥字符串），值为 `-1` 表示调用来自控制台 | 同上，LabelKey 说明表 |
| `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC），影响性能分析粒度 | 同上，LabelKey 说明表 |
| `max_tokens` | 控制输出长度的关键请求参数，直接影响 Token 消耗与费用 | [模型用量 (model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) 中“应用于生产环境”建议 |

## 使用方式

1. **基础监控入口**：  
   登录百炼控制台 → 进入[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面，查看按“模型 + 业务空间”聚合的监控概览与表格列表。

2. **查看模型详情**：  
   在列表中点击目标模型操作列的 **监控**，进入详情页：  
   - **调用统计**页签：查看调用次数、失败率、Token 消耗、限流/内容安全错误等；支持按 API Key、推理类型（实时/批量）、时间范围（分钟/小时精度）筛选；  
   - **性能指标**页签：查看 RPM、TPM、调用时长、TTFT、ITL 等；  

3. **查看推理日志（含输入/输出）**：  
   - 先在目标业务空间的模型监控页面点击右上角 **模型监控配置** → 开通 **审计日志** 和 **推理日志**；  
   - 返回列表，点击目标模型操作列的 **日志** → 在日志页签查看请求/响应内容（仅限[文档2所列支持模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）；  
   - 注意：日志仅记录开通后的新调用，历史调用不可追溯。

4. **配置告警**：  
   - 确保已开启高级监控 → 进入[模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert)页面 → 点击 **创建告警规则** → 选择模型、指标模板（如“失败率突增”、“Token 消耗超阈值”）→ 设置通知方式与等级。

5. **对接 Prometheus/Grafana**：  
   - 开启高级监控后，在模型监控配置中获取 Prometheus HTTP API 地址；  
   - 使用标准 PromQL 查询，例如：`model_usage{workspace_id="xxx",model="qwen-plus"}`；  
   - 认证需提供 Base64 编码的 `AccessKey:AccessKeySecret`（必须与 Prometheus 实例同账号）。

## 限制和注意事项

- **地域限制**：高级监控、告警、推理日志、Prometheus API 仅在北京、新加坡、弗吉尼亚地域可用；上海地域仅支持普通监控（无分钟级日志与告警）。  
- **模型兼容性**：并非所有模型均支持推理日志（请求/响应内容记录），具体支持列表详见[模型监控 (model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 中“支持请求和响应的模型”章节。不支持时界面提示“当前模型暂不支持日志”。  
- **数据延迟差异**：  
  - 普通监控（用量汇总类指标）：延迟约 1–2 小时；  
  - 高级监控（日志、TPS、分钟级趋势）：延迟为分钟级；  
  - 账单级用量（用于计费对账）：以[费用与成本](https://billing-cost.console.aliyun.com/...)页面为准，T+1 日更新。  
- **免费额度联动**：“免费额度用完即停”开关仅影响计费行为，**不影响监控数据采集**；即使额度耗尽导致返回 403，该调用仍会被记录在监控与日志中（状态码、失败原因可查）。  
- **权限约束**：子业务空间成员默认仅能查看本空间数据；跨空间查看或配置高级监控需主账号或具备 `AliyunBailianFullAccess` 等高权限策略。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


