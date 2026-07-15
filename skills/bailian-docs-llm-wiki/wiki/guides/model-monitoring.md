# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能表现、成本消耗与异常事件。它覆盖从基础调用统计到细粒度 Token 追踪、从控制台可视化到 Prometheus 自建集成的全链路监控能力，适用于生产环境下的稳定性保障与成本精细化治理。所有监控数据默认按「模型 + 业务空间」维度聚合，主账号可跨空间查看，子账号仅限当前业务空间。

## 支持的模型与功能

- **监控覆盖范围**：  
  - **普通监控**支持[选择模型](https://help.aliyun.com/zh/model-studio/models)中的全部模型（含基于其调优的[自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)）；  
  - **高级监控**（含分钟级指标、告警、Prometheus 接入）仅支持北京、新加坡、弗吉尼亚地域下的模型；  
  - **告警功能**仅支持北京、新加坡地域（见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。  

- **核心功能模块**：  
  - **调用统计**：调用次数、失败次数、失败率、限流错误（429）、内容安全拦截次数；  
  - **性能指标**：RPM、TPM、调用时长、首Token延时、非首Token延时；  
  - **成本监控**：Token 消耗汇总与单次追踪（仅北京地域部分模型支持）；  
  - **日志审计**：输入/输出对话记录（仅北京地域且限于[指定模型列表](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）；  
  - **用量统计**：按业务空间维度的模型用量（含免费额度使用情况），延迟约 1 小时（见 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。  

> **注意**：文档 1 称“普通监控延迟通常为小时级”，而文档 2 明确用量统计延迟“约为 1 小时”；二者一致。但文档 1 中“新模型在首次数据同步完成后自动加入列表”未说明是否含自定义模型——文档 2 明确“调优后的模型”同样支持用量查看，故可推断其也纳入普通监控范围，无额外限制。

## 关键参数与指标

| 类别 | 指标名 | 说明 | 支持过滤 Label |
|--------|---------|------|----------------|
| 调用次数 | `model_call_count` | 总调用次数 | `user_id`, `apikey_id`, `workspace_id`, `model`, `protocol`, `sub_protocol`, `status_code`, `error_code` |
| 调用时长 | `model_call_duration`, `model_call_duration_p99` | 均值/P99 时长（秒） | 同上 |
| 首Token延时 | `model_first_token_duration` | 首包响应时间 | 同上 |
| 非首Token延时 | `model_generation_duration_per_token` | 每 Token 生成耗时 | 同上 |
| Token用量 | `model_usage` | 总 Token 数（支持 `usage_type` 过滤：`input_tokens`/`output_tokens`/`total_tokens` 等） | `usage_type`, `workspace_id`, `model`, `apikey_id` |

所有指标均通过 Prometheus HTTP API 提供，需开启[高级监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)并配置 AccessKey 认证（见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。

## 使用方式

1. **控制台访问**：  
   - 普通监控入口：[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)（北京）或对应地域控制台；  
   - 用量统计入口：[模型用量](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/usage-statistics)（仅业务空间维度）；  
   - 免费额度管理：[免费额度](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)。  

2. **日志与单次 Token 查看**（仅北京地域）：  
   - 需先在「模型监控配置」中开通**审计日志 + 推理日志**；  
   - 开通后，在模型列表点击「日志」页签，查看请求/响应及 `用量` 字段（见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。  

3. **告警配置**：  
   - 仅北京、新加坡地域支持；  
   - 需先开启高级监控 → 进入[模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert) → 创建规则（支持短信/邮件/钉钉/Webhook 等通知方式）。  

4. **Grafana / 自建应用接入**：  
   - 获取 Prometheus HTTP API 地址（需开启高级监控）；  
   - 使用 `Basic` 认证（AccessKey:AccessKeySecret Base64 编码）调用 `/api/v1/query_range`；  
   - 示例：`GET {API}/api/v1/query_range?query=model_usage{workspace_id="xxx",model="qwen-plus"}&start=...&step=60s`（详见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。

## 限制和注意事项

- **地域限制严格**：  
  - 日志审计、单次 Token 追踪、告警、Prometheus 接入等功能**仅限北京、新加坡、弗吉尼亚地域**；其他地域仅提供小时级普通监控（如调用总量、失败率等基础卡片）。  

- **模型兼容性差异**：  
  - 并非所有模型均支持全部监控能力。例如，历史对话（输入/输出日志）仅支持文档 1 列出的千问系列、开源及三方模型快照版本（如 `qwen3-max-2025-09-23`），旧版快照或未列型号不支持（见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。  

- **数据延迟与范围**：  
  - 普通监控数据延迟约 **1 小时**；高级监控支持分钟级洞察；  
  - 控制台用量页面**最多查看最近 30 天数据**，更早数据需通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)查询（见 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。  

- **权限约束**：  
  - 主账号及具备足够权限的子账号可开通日志与高级监控；  
  - 子业务空间成员**无法切换查看其他业务空间数据**，仅限当前空间（见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。  

- **用量单位差异**：  
  - 大语言模型按 **Token** 计费；视觉模型按 **张**（图像）、**秒**（视频）；语音模型按 **秒/字符/Token**（依模型而定）；全模态模型文本部分按 Token，其他模态按对应 Token 数（见 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

## 来源文档

- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)
- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


