# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标、成本消耗及异常事件。它覆盖从基础用量统计到细粒度推理日志的全链路数据采集，支持开发者快速定位性能瓶颈、成本突增或内容安全风险。该功能与[模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)形成互补：前者侧重分钟级实时诊断与告警，后者侧重小时级账单对齐与资源规划。

## 支持的模型/功能

- **监控范围**：  
  - *普通监控*（免费）：支持所有在[模型列表](https://help.aliyun.com/zh/model-studio/models)中可选的模型，包括基于它们调优后的[自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)；  
  - *高级监控*（收费）：仅限北京、上海、新加坡、弗吉尼亚地域下的模型（注意：文档2明确列出上海地域支持，但文档1未提及，需以文档2为准）；  
  - *告警功能*：仅支持北京、新加坡、弗吉尼亚地域（**不支持上海地域告警**）。  

- **核心功能**：  
  - 调用记录追踪（含 Request ID、状态码、错误码）；  
  - 多维指标监控：RPM、TPM、调用时长、首 [Token](../concepts/token.md) 延时（TTFT）、非首 [Token](../concepts/token.md) 延时、失败率、限流错误次数、内容安全错误次数；  
  - [Token](../concepts/token.md) 消耗明细（按次、按业务空间、按 API Key）；  
  - 推理日志查看（输入/输出原文，仅限[支持的模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)#支持请求和响应的模型)；  
  - 主动告警（基于成本、性能、错误类指标）；  
  - Prometheus 数据导出（供 Grafana 或自建系统集成）。

> **注意**：文档1称“模型列表中的所有模型均支持查看用量”，而文档2明确限定高级监控和告警仅支持部分地域。二者无本质矛盾——文档1描述的是用量统计（基础能力），文档2描述的是实时监控与告警（增强能力）。但需注意：**上海地域模型可被监控，但无法配置告警**，此限制在文档2中明确，文档1未覆盖。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识，所有监控数据按此维度隔离；子空间成员仅能查看本空间数据 | [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `apikey_id` | API Key 的 ID（非密钥本身），用于按调用来源归因；值为 `-1` 表示控制台调用 | [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `model` | 模型 Code（如 `qwen-plus`），区分大小写，必须与模型列表中完全一致 | [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC），影响延时与吞吐分析 | [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

## 使用方式

1. **启用监控**：  
   - 普通监控默认开启，数据延迟约 **1 小时**；  
   - 高级监控（含分钟级日志、TPS、Prometheus 导出）需手动开通：进入目标业务空间的[模型监控页面](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) → 右上角「模型监控配置」→ 开启「性能和用量指标监控」及「推理日志」（后者为查看请求/响应所必需）。

2. **查看数据**：  
   - **概览**：在[模型监控列表页](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)查看各模型的调用总量、失败率、平均时长等卡片指标；  
   - **详情**：点击模型行右侧「监控」→ 切换「调用统计」或「性能指标」页签，支持按 API Key、推理类型（实时/批量）、时间范围（最近30天）、时间精度（分钟/小时）筛选；  
   - **日志**：点击「日志」→ 查看带用量（Token数）、请求/响应原文的调用记录（仅限[支持的模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)#支持请求和响应的模型)；  
   - **历史用量**：[模型用量页面](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/usage-statistics)提供更长周期（30天）的汇总视图，但延迟更高（约1小时）且不支持单次调用明细。

3. **配置告警**：  
   - 进入[模型告警页面](https://bailian.console.aliyun.com/?tab=model#/model-alert) → 「创建告警规则」→ 选择模型、监控模板（如「Token消耗突增」、「失败率超阈值」）→ 设置通知方式（短信/邮件/钉钉等）与等级（CRITICAL/ERROR/WARNING/INFO）。

4. **对接自建系统**：  
   - 获取 Prometheus HTTP API 地址（通过「模型监控配置」→ 「查看详情」）；  
   - 使用标准 PromQL 查询，例如：  
     ```http
     GET {API}/api/v1/query_range?query=model_usage{workspace_id="llm-xxx",model="qwen-plus"}&start=2025-11-20T00:00:00Z&end=2025-11-20T23:59:59Z&step=60s
     ```

## 限制和注意事项

- **数据延迟**：  
  - 普通监控（调用次数、总Token）：**小时级延迟**（高峰期达1–2小时）；  
  - 高级监控（推理日志、TPS、单次调用明细）：**分钟级延迟**；  
  - 免费额度数据：**分钟级更新**，支持手动刷新同步。

- **地域与模型限制**：  
  - 推理日志（请求/响应内容）**仅支持北京、新加坡、弗吉尼亚地域**，且仅限[明确列出的模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)#支持请求和响应的模型；  
  - 上海地域模型**不支持告警配置**（文档2明确限定告警地域为北京/新加坡/弗吉尼亚）；  
  - 批量推理调用**不记录在模型监控日志页**（仅实时推理支持），但会纳入用量统计。

- **权限与范围**：  
  - 主账号可查看全部业务空间数据；子账号/业务空间成员**仅能查看当前空间数据**，无法跨空间切换；  
  - 推理日志仅记录**开通后**的调用，历史调用**不可补录**。

- **计费与开通**：  
  - 普通监控免费；高级监控（含推理日志、Prometheus导出）为**收费功能**；  
  - 开通高级监控前，需确保账号已绑定有效支付方式，否则批量操作将失败。

- **关键行为约束**：  
  - 「免费额度用完即停」开关**仅能在仍有未消耗额度时开启**；关闭该功能需等待额度完全耗尽后才可操作；  
  - Token 统计单位因模型类型而异（文本模型按 Token、图像模型按张、语音模型按秒等），详见[模型用量统计单位说明](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)#模型用量统计单位说明。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


