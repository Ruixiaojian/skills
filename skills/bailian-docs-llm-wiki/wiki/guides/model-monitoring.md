# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标、成本消耗及异常事件。它覆盖从基础用量统计到细粒度推理日志的全链路数据采集，支持开发者进行容量规划、故障排查、成本优化与安全审计。该功能默认启用普通监控，高级监控（含分钟级延迟、TPS、推理日志等）需手动开通。

## 支持的模型/功能

- **监控范围**：普通监控支持[模型列表](https://help.aliyun.com/zh/model-studio/models)中所有模型（含调优后的自定义模型）；高级监控仅支持北京、上海、新加坡、弗吉尼亚地域下的模型 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **告警能力**：告警功能覆盖北京、新加坡、弗吉尼亚地域的所有模型，不支持上海地域 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **日志能力**：推理日志（含请求/响应内容）仅限特定模型，如 `qwen3-plus`、`qwen-flash`、`qwen-turbo` 及部分开源/三方模型；不支持的模型在界面明确提示“当前模型暂不支持日志” [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **功能维度**：  
  - **调用记录**：按 Request ID 追踪单次调用详情（需开启推理日志）；  
  - **指标监控**：RPM、TPM、调用时长、首 Token 延时（TTFT）、非首 Token 延时、失败率、限流错误次数、内容安全错误次数；  
  - **Token 消耗**：支持按业务空间、API Key、时间范围汇总与单次调用粒度追踪；  
  - **主动告警**：支持对成本、性能、错误类指标设置阈值告警，并通过短信/邮件/钉钉等渠道通知。

> **注意**：文档 1 中称“模型用量页面支持查看所有模型的用量”，但文档 2 明确限定高级监控（含分钟级日志与TPS）仅限四大地域，且日志功能存在明确模型白名单。二者无本质矛盾，但需强调：**普通用量统计（小时级）全域可用，而细粒度监控与日志能力受地域和模型双重约束**。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `workspace_id` | 业务空间唯一标识，用于多空间隔离统计 | 必填过滤条件，见 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `model` | 模型 Code（如 `qwen-plus`），区分大小写 | 必填过滤条件，见 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `apikey_id` | API Key ID（非密钥字符串），控制台密钥管理页可查；值为 `-1` 表示控制台调用 | 过滤条件，见 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC） | 影响性能分析维度，见 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `max_tokens` | 控制输出长度的关键参数，直接影响 Token 消耗与费用 | 推荐在 API 调用中显式设置，见 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |

## 使用方式

1. **访问入口**：  
   - 普通监控：进入 [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 页面（按业务空间展示）；  
   - 高级监控与告警：需先在对应地域的模型监控页点击 **模型监控配置** → 开启「性能和用量指标监控」；  
   - 推理日志：同上路径开通「审计日志」与「推理日志」后，方可查看请求/响应内容。

2. **核心操作流程**：  
   - **查看用量趋势**：在「调用统计」页签筛选时间范围（支持分钟/小时/天）、API Key、推理类型，查看调用次数、失败率、Token 消耗；  
   - **定位单次调用**：在「日志」页签按 Request ID 或时间筛选，查看用量、状态码、错误码及原始输入/输出（需模型支持且日志已开通）；  
   - **创建告警**：进入 [模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert) 页面 → 「创建告警规则」→ 选择模型、指标模板、阈值与通知方式；  
   - **对接 Grafana**：获取 Prometheus HTTP API 地址后，使用标准 PromQL 查询（如 `model_usage{model="qwen-plus", workspace_id="xxx"}`），详见 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

3. **数据时效性**：  
   - 普通监控（调用次数、总量）：延迟约 **1 小时**，高峰期可达 1–2 小时；  
   - 高级监控（TPS、推理日志）：延迟为 **分钟级**；  
   - 免费额度数据：控制台分钟级更新，支持手动刷新。

## 限制和注意事项

- **地域限制**：高级监控、告警、推理日志功能**仅在北京、新加坡、弗吉尼亚地域可用**；上海地域暂不支持 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **时间范围限制**：  
  - 模型用量与监控数据默认仅保留最近 **30 天**；更早数据需通过 [费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance) 页面查询；  
  - 模型用量页面不支持查看 **30 天以前** 的统计数据 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。  
- **权限约束**：  
  - 主账号可查看所有业务空间数据；子业务空间成员**仅能查看当前空间数据**，无法跨空间切换；  
  - 开通高级监控与日志需主账号或具备 `AliyunBailianFullAccess` 权限的子账号操作。  
- **模型兼容性**：  
  - 并非所有模型支持推理日志（请求/响应内容），具体支持列表以 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 中“支持请求和响应的模型”为准；  
  - TPS（`model_tps_per_request`）指标**仅高级监控提供**，且与非首 Token 延时呈倒数关系，分析性能问题时需结合 TTFT、输入 Token 数综合判断。  
- **计费说明**：  
  - 普通监控免费；高级监控为**收费功能**，开通即产生费用；  
  - 免费额度用完即停功能开启后，服务将返回 `403 AllocationQuota.FreeTierOnly` 错误，避免意外扣费 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


