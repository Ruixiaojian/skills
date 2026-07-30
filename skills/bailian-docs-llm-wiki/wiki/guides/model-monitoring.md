# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标、成本消耗及异常事件。它覆盖从基础用量统计到细粒度推理日志的全链路数据采集，支持开发者快速定位性能瓶颈、识别安全风险、优化成本结构，并通过告警与外部系统集成实现主动运维。该功能与[模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)形成互补：前者侧重分钟级实时诊断与深度分析，后者侧重小时级汇总与账单对齐。

## 支持的模型/功能

- **监控范围**：  
  - *普通监控*：支持[选择模型](https://help.aliyun.com/zh/model-studio/models)中的所有模型（含调优后的[自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)），数据延迟为小时级；  
  - *高级监控*：仅限北京、上海、新加坡、弗吉尼亚地域下的模型，提供分钟级延迟、TPS等高精度指标及Prometheus数据导出能力。  

- **核心功能**：  
  - 调用记录追踪（含Request ID、状态码、错误码）；  
  - 多维指标监控：RPM、TPM、调用时长、首[Token](../concepts/token.md)延时（TTFT）、非首[Token](../concepts/token.md)延时、失败率、限流错误次数、内容安全错误次数；  
  - [Token](../concepts/token.md)消耗明细（按次、按模型、按业务空间）；  
  - 推理日志查看（输入/输出原文，需开通日志功能）；  
  - 告警规则配置（支持失败率突增、Token消耗超阈值等场景）；  
  - Grafana与自建应用接入（通过Prometheus HTTP API）。  

> **注意**：文档1中称“模型用量页面数据延迟约为1小时”，而文档2明确区分普通监控（小时级）与高级监控（分钟级）。实际使用中，若需分钟级洞察，必须启用[模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中的高级监控，否则无法满足低延迟需求。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspace_id` | 业务空间ID，用于按空间维度隔离监控数据（必填过滤条件） | [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `model` | 模型Code（如`qwen-plus`），用于精确筛选目标模型 | 同上 |
| `apikey_id` | API Key ID（非密钥本身），用于归因调用来源；值为`-1`表示控制台调用 | 同上 |
| `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC），影响性能指标解读 | 同上 |
| `step` | Prometheus查询步长（如`60s`），决定时间序列分辨率 | 同上 |

## 使用方式

1. **基础监控入口**：  
   进入[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面，列表默认按“模型 + 业务空间”聚合，点击操作列的**监控**或**日志**进入详情页。

2. **开启高级能力**：  
   - 在模型监控页面右上角点击**模型监控配置** → 开通**审计日志**和**推理日志**（日志功能仅对北京/新加坡/弗吉尼亚地域生效）；  
   - 同一路径下开启**性能和用量指标监控**以启用高级监控（含TPS、Prometheus API等）。

3. **查看Token消耗**：  
   - *汇总视图*：在「调用统计」页签的**调用量**区域查看近30天历史；  
   - *单次明细*：在「日志」页签的**用量**列直接读取（需已开通推理日志）；  
   - *长期归档*：超过30天的数据请通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)页面查询。

4. **创建告警**：  
   进入[模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert)页面 → **创建告警规则** → 选择模型、监控模板（如“失败率突增”）、通知渠道（短信/邮件/钉钉等）及告警等级。

5. **Grafana接入**：  
   获取Prometheus HTTP API地址后，使用标准PromQL查询，例如：  
   ```http
   GET {API}/api/v1/query_range?query=model_usage{workspace_id="llm-nymssti2mzww****",model="qwen-plus"}&start=2025-11-20T00:00:00Z&end=2025-11-20T23:59:59Z&step=60s
   ```

## 限制和注意事项

- **地域限制**：  
  - 推理日志、高级监控、告警功能仅在北京、新加坡、弗吉尼亚地域可用；上海地域仅支持普通监控（无日志与告警）。  
  - 日志功能对模型有明确支持列表（如`qwen3-max`、`qwen-plus`等快照版本），不支持的模型会显示“当前模型暂不支持日志”提示。

- **数据时效性**：  
  - 普通监控（用量汇总）延迟约1–2小时；  
  - 高级监控（日志、TPS）延迟为分钟级；  
  - **未开通日志前的历史调用无法补录**，务必在业务上线前完成配置。

- **权限与范围**：  
  - 主账号可查看全部业务空间数据；子账号仅能访问所属业务空间，且需被授予`AliyunBaiLianFullAccess`或等效权限；  
  - `apikey_id = -1` 表示调用来自控制台（如模型广场测试、应用编排调试），不计入API Key用量统计。

- **计费差异**：  
  - 高级监控（含Prometheus API、TPS指标）为收费功能；  
  - 推理日志存储与查询按实际用量计费，详见[模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)定价说明。  

> **注意**：文档1中“模型用量”页面的免费额度管理（如「免费额度用完即停」开关）与文档2的“模型监控”功能完全解耦——前者属于计费策略控制，后者属于可观测性工具。二者虽均涉及用量数据，但触发动作（如开关切换）不会自动同步至监控告警阈值，需独立配置。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


