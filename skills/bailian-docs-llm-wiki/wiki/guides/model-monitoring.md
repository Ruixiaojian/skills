# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标、成本消耗及异常事件。它覆盖从基础用量统计到高级性能分析的全链路监控场景，支持开发者快速定位问题、优化成本并保障服务稳定性。监控数据按业务空间维度隔离，需在对应空间内配置后方可生效。

## 支持的模型/功能

- **监控范围**：普通监控支持[所有公开模型及调优后的自定义模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)，包括千问系列（qwen3-max、qwen-plus 等）、Coder、Flash、Turbo 及部分开源与三方模型；高级监控（含推理日志、TPS、细粒度延迟分位数等）仅限北京、上海、新加坡、弗吉尼亚地域部署的模型。
- **日志能力**：请求/响应内容记录（即“历史对话”）**并非所有模型均支持**，具体支持列表详见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 中“支持请求和响应的模型”章节。不支持的模型即使开通推理日志，界面也会明确提示“当前模型暂不支持日志”。
- **告警能力**：告警功能仅支持北京、新加坡、弗吉尼亚地域的模型，且需先开启[高级监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

> **注意**：文档 1 中称“模型列表中的所有模型均支持查看用量”，而文档 2 明确限定高级监控与日志功能的地域和模型范围。二者不矛盾——**用量统计（如总调用次数、[Token](../concepts/token.md) 总量）是基础能力，全域通用；而细粒度指标（如首 [Token](../concepts/token.md) 延时 P99）、原始日志、TPS 等属于高级监控，受地域与模型支持度双重约束**。实际使用中应以文档 2 的限制为准。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识，用于多空间隔离查询，必须显式指定 | [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `model` | 模型 Code（如 `qwen-plus`），区分大小写，用于精确过滤 | [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `apikey_id` | API Key ID（非密钥字符串），值为 `-1` 表示控制台调用 | [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC），影响延迟与吞吐解读 | [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `step` | Prometheus 查询时间步长，最小支持 `60s`（分钟级），不支持秒级聚合 | [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

## 使用方式

1. **基础监控入口**：进入控制台 → [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)，默认展示当前业务空间下所有已调用模型的汇总卡片与表格。
2. **查看细粒度指标**：
   - 点击模型行右侧「监控」→ 切换「调用统计」或「性能指标」页签；
   - 支持按 API Key、推理类型（实时/批量）、时间范围（最大 30 天）、时间精度（分钟/小时）筛选；
   - 「失败详情」可下钻查看错误码（如 `429` 限流、`content_moderation` 内容安全拦截）。
3. **查看单次调用 [Token](../concepts/token.md) 消耗**：
   - 先开通推理日志（仅北京/新加坡/弗吉尼亚支持）；
   - 点击「日志」页签 → 查看「用量」列（单位为 Token）；
   - 注意：仅记录开通日志**之后**的调用，历史数据不可追溯。
4. **接入外部系统**：
   - 开启高级监控后，获取 Prometheus HTTP API 地址；
   - 使用标准 PromQL 查询，例如：`model_usage{workspace_id="xxx",model="qwen-plus"}`；
   - 需提供 Base64 编码的 `AccessKey:AccessKeySecret` 认证。

## 限制和注意事项

- **数据延迟**：普通监控（调用次数、总量）延迟约 **1–2 小时**；高级监控（推理日志、性能指标）延迟为 **分钟级**；费用类数据（如账单）延迟更长，需通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)页面查询历史数据。
- **时间范围限制**：模型监控页面仅支持查看 **最近 30 天** 数据；超期数据需导出账单或使用费用平台查询。
- **地域与模型约束**：推理日志、TPS、P99 延迟等高级指标**仅在北京、新加坡、弗吉尼亚地域可用**，且依赖模型本身是否开放该能力（如 qwen-turbo 支持，部分旧版模型不支持）。
- **权限隔离**：子业务空间成员**只能查看本空间数据**，无法跨空间切换；主账号可查看全部空间，但需手动选择目标空间。
- **免费额度联动**：监控本身不触发计费，但用量数据与[免费额度管理](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)强关联——例如「免费额度用完即停」开关状态直接影响服务可用性，建议结合用量趋势提前预警。

> **注意**：文档 1 中提到“模型用量页面支持按分钟精度查看”，但实际受限于数据延迟与聚合逻辑，**分钟级图表仅在时间跨度 ≤1 天时可用，且数据非实时**；文档 2 明确指出高级监控延迟为“分钟级”，而普通监控为“小时级”。开发者应避免依赖分钟级图表做实时告警决策，推荐使用 Prometheus API + 自建告警规则实现亚分钟级响应。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


