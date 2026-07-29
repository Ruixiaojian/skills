# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标、成本消耗及异常事件。它覆盖从基础用量统计到细粒度推理日志的全链路数据采集，并支持告警、自定义分析与第三方集成。该功能面向生产环境运维与成本治理场景，为开发者提供分钟级（高级监控）或小时级（普通监控）的数据洞察。

## 支持的模型/功能

- **监控覆盖范围**：  
  - 普通监控支持[所有在模型列表中可选的模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)，包括基于其调优的[自定义模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)；  
  - 高级监控（含推理日志、TPS、Prometheus API等）仅支持部署在**华北2（北京）、华东2（上海）、新加坡、美国弗吉尼亚**地域的模型；  
  - 告警功能当前仅支持**北京、新加坡、弗吉尼亚**地域的模型。

- **关键功能模块**：  
  - **调用记录追踪**：支持按 Request ID 查看单次调用的输入、输出、状态码、用量（[Token](../concepts/token.md) 数）等；  
  - **多维指标监控**：涵盖安全（内容安全错误次数）、成本（平均单次请求调用量、[Token](../concepts/token.md) 消耗）、性能（RPM、TPM、调用时长、首 [Token](../concepts/token.md) 延时、非首 Token 延时）、错误（失败率、限流错误次数）四大类；  
  - **历史对话审计**：仅对明确[支持的模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)（如 `qwen3-plus`、`qwen-flash`、`deepseek-v3.2` 等快照版本）开放，且需提前开通推理日志；  
  - **主动告警**：支持基于失败率、TPM 突增、首 Token 延时超阈值等条件创建多级告警（INFO / WARNING / ERROR / CRITICAL），通知方式含邮件、短信、钉钉机器人等；  
  - **Grafana 与自建应用集成**：通过私有 Prometheus 实例暴露标准 HTTP API，支持 `model_call_count`、`model_usage`、`model_tps_per_request` 等 [完整监控指标列表](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 查询。

> **注意**：文档 1 中称“模型列表中的所有模型均支持查看用量”，而文档 2 明确指出**推理日志、TPS、分钟级延迟监控、Grafana 接入等高级能力仅限特定地域且依赖模型快照版本支持**。二者不矛盾，但需区分“基础用量统计”与“高级监控能力”的适用边界——前者全域通用，后者受地域与模型版本双重约束。

## 关键参数

| 参数 | 说明 | 来源约束 |
|------|------|----------|
| `workspace_id` | 业务空间 ID，所有监控数据按此维度隔离与聚合 | 必填（Prometheus 查询、控制台筛选均依赖） |
| `model` | 模型 Code（如 `qwen-plus`），区分大小写 | 必填（日志、告警、API 查询均需精确匹配） |
| `apikey_id` | API Key ID（非密钥本身），用于归因调用来源；值为 `-1` 表示来自控制台调用 | 可选，但推荐用于多 Key 成本分摊 |
| `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC），影响延时与吞吐特征 | 高级监控专属标签，用于精细化分析 |
| `start` / `end` / `step` | Prometheus 查询时间范围与步长；`step=60s` 为分钟级精度最低要求 | 仅高级监控 API 支持，普通监控无此接口 |

## 使用方式

1. **基础用量查看**：  
   进入[模型用量](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/usage-statistics)页面，按模型类型、时间范围（≤30 天）、API Key 筛选，查看 Token/张/秒等用量汇总。数据延迟约 **1 小时**（见[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

2. **模型监控详情**：  
   进入[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面 → 点击目标模型操作列的 **监控** 或 **日志**：  
   - “监控”页签查看调用统计（失败详情可下钻）、性能趋势（RPM/TPM/延时）；  
   - “日志”页签查看单次调用明细（需已开通推理日志，且模型在[支持列表](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中）。

3. **开通高级能力**：  
   在模型监控页面右上角点击 **模型监控配置** → 开启：  
   - **审计日志 + 推理日志**（用于日志回流、内容审计）；  
   - **性能和用量指标监控**（启用 Prometheus 数据源与 TPS 等指标）。

4. **创建告警**：  
   进入[模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert)页面 → **创建告警规则** → 选择模型、模板（如“TPM 异常突增”）、阈值、通知渠道。

5. **接入 Grafana / 自建系统**：  
   获取 Prometheus HTTP API 地址后，使用标准 PromQL 查询，例如：  
   ```http
   GET {API}/api/v1/query_range?query=model_usage{workspace_id="llm-xxx",model="qwen-plus"}&start=2025-11-20T00:00:00Z&end=2025-11-20T23:59:59Z&step=60s
   ```

## 限制和注意事项

- **数据延迟**：  
  - 普通监控（用量汇总、失败率等）延迟 **1–2 小时**；  
  - 高级监控（推理日志、Prometheus 指标）延迟为**分钟级**，但首次同步需等待日志开通生效。

- **地域与模型限制**：  
  - 推理日志、TPS 指标、Grafana 集成、分钟级告警仅支持北京/上海/新加坡/弗吉尼亚地域；  
  - 并非所有模型都支持请求/响应内容记录，具体以[支持列表](../../raw/model-user-guide/model-monitoring/model-telemetry.md)为准；不支持的模型在日志页签会明确提示“当前模型暂不支持日志”。

- **免费额度联动**：  
  - “免费额度用完即停”开关仅影响计费行为（返回 403），**不影响监控数据采集**；用量与告警仍持续上报，便于及时发现额度耗尽风险（见[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

- **权限约束**：  
  - 主账号默认可查看全部业务空间数据；子账号仅能访问其所属业务空间，且需被授予 `AliyunBaiLianFullAccess` 或等效权限才能开通日志与告警。

- **历史数据不可追溯**：  
  - 推理日志仅记录**开通后**的调用；开通前的历史请求无法补录。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


