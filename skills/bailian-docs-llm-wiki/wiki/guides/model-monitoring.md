# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标与资源消耗。它支持从基础用量统计到分钟级延迟分析的多维度监控，并可基于关键指标（如失败率、TPM、首[Token](../concepts/token.md)延时）配置主动告警。该功能面向生产环境稳定性保障与成本精细化治理，不依赖应用层日志，直接采集服务网关侧原始调用数据。

## 支持的模型/功能

- **监控覆盖范围**：  
  - *普通监控*：支持[模型列表](https://help.aliyun.com/zh/model-studio/models)中所有模型（含调优后的自定义模型）[原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)；  
  - *高级监控*（含推理日志、TPS、分钟级指标）：仅支持北京、上海、新加坡、弗吉尼亚地域下的模型；  
  - *告警功能*：仅支持北京、新加坡、弗吉尼亚地域下的模型。  

- **核心功能模块**：  
  - 调用记录追踪（含 Request ID、状态码、错误码）；  
  - 四类监控视图：**安全**（内容安全错误次数）、**成本**（单次请求调用量、[Token](../concepts/token.md) 消耗）、**性能**（RPM、TPM、调用时长、首/非首 [Token](../concepts/token.md) 延时）、**错误**（失败次数、限流错误次数）；  
  - 推理日志回溯（输入/输出内容），但**仅限指定模型版本**（如 `qwen3-plus-2025-12-01` 及之后快照），详见[原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)；  
  - 日志回流至训练数据集（支持模型微调闭环）。  

> **注意**：文档1中称“模型列表中的所有模型均支持查看用量”，而文档2明确限定高级监控（含日志、TPS、分钟级延迟）仅限特定地域且部分模型不支持请求/响应记录。二者不矛盾——前者指**用量统计口径通用**，后者指**深度可观测能力有地域与模型版本限制**。实际使用应以文档2的[原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)为准。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspace_id` | 业务空间 ID，为监控数据隔离的关键维度（子空间成员仅可见本空间数据） | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `model` | 模型 Code（如 `qwen-plus`），用于指标过滤与告警绑定 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `apikey_id` | API Key ID（非密钥本身），用于按调用来源归因；值为 `-1` 表示控制台内调用 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC），影响延迟与吞吐特征 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `max_tokens` | 控制输出长度的核心参数，直接影响 Token 消耗与费用，建议在 API 调用中显式设置 | [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |

## 使用方式

1. **访问入口**：  
   - 控制台路径：`百炼控制台 > 模型 > 模型监控`（[北京](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) / [新加坡](https://modelstudio.console.aliyun.com/?tab=dashboard#/model-telemetry)）；  
   - 免费额度与用量统计入口独立：`费用与成本 > 免费额度` / `模型用量`（[原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

2. **启用深度能力**：  
   - 开通**推理日志**：进入目标业务空间的「模型监控配置」→ 启用审计日志 + 推理日志（开通后生效，历史调用不补录）；  
   - 开启**高级监控**：同上配置页中启用「性能和用量指标监控」（收费功能，TPS 等指标仅在此模式下可用）。

3. **查询与分析**：  
   - 在「模型监控」列表点击目标模型的 **监控**，切换「调用统计」或「性能指标」页签，按 API Key、推理类型（实时/批量）、时间范围（支持分钟/小时精度）筛选；  
   - 点击 **日志** 查看单次调用详情（含用量、请求/响应原文）；  
   - 通过 Prometheus HTTP API 直接拉取指标（需开启高级监控），例如：  
     ```bash
     GET {prometheus_api}/api/v1/query_range?query=model_usage{workspace_id="xxx",model="qwen-plus"}&start=...&end=...&step=60s
     ```

4. **告警配置**：  
   - 进入「模型告警」页面 → 「创建告警规则」→ 选择模型、指标模板（如「失败率突增」、「Token 消耗超阈值」）→ 设置通知渠道（短信/邮件/钉钉等）与等级（CRITICAL/ERROR/WARNING/INFO）。

## 限制和注意事项

- **数据延迟**：  
  - 普通监控（调用次数、总量）延迟约 **1–2 小时**；  
  - 高级监控（推理日志、TPM/RPM、首Token延时）延迟为 **分钟级**；  
  - 费用类数据（账单、免费额度）延迟为 **分钟级，支持手动刷新**（[原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

- **地域与模型限制**：  
  - 推理日志（请求/响应内容）**仅支持北京、新加坡、弗吉尼亚地域**，且仅限文档2中明确列出的模型快照版本；  
  - 上海地域当前**不支持高级监控与告警**（文档2未提上海支持告警，仅列于监控支持地域中）。

- **功能边界**：  
  - **不支持跨账号统计**：用量与监控数据严格按业务空间维度聚合，无法按阿里云主账号汇总（[原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）；  
  - **30天窗口限制**：模型用量与监控图表默认最多查看最近30天数据，更早数据需通过[费用与成本](https://billing-cost.console.aliyun.com/...)页面查询；  
  - **批量推理监控缺失**：当前监控列表与日志页签**仅展示实时推理调用**，批量推理（OpenAI Batch）无独立监控视图，其用量仅计入模型用量总表。

- **权限要求**：  
  - 开通日志与高级监控需主账号或具备 `AliyunBailianFullAccess` 权限的子账号；  
  - 子业务空间成员**无法切换查看其他空间数据**，权限隔离严格。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


