# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标与资源消耗。它支持从宏观用量统计到单次请求级日志的全链路观测，并可基于关键指标（如失败率、首[Token](../concepts/token.md)延时、TPM）配置主动告警。该功能面向生产环境稳定性保障与成本精细化治理，不依赖应用层埋点，数据由平台自动采集。

## 支持的模型/功能

- **监控覆盖范围**：  
  - 普通监控支持[所有在模型列表中可选的模型](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)，包括基于它们调优后的自定义模型；  
  - 高级监控（含分钟级延迟、TPS、推理日志等）仅支持北京、上海、新加坡、弗吉尼亚地域下的模型；  
  - 告警功能仅支持北京、新加坡、弗吉尼亚地域下的模型。  

- **核心功能模块**：  
  - **调用记录追踪**：支持按 Request ID 查看单次调用的输入、输出、状态码、耗时及 [Token](../concepts/token.md) 用量；  
  - **多维指标监控**：涵盖安全（内容安全错误次数）、成本（平均单次请求调用量）、性能（RPM、TPM、调用时长、首[Token](../concepts/token.md)延时、非首Token延时）、错误（失败率、限流错误次数）四大类；  
  - **历史对话审计**：仅对已开通推理日志且模型明确支持的版本（如 `qwen3-plus-2025-12-01` 及之后快照）生效；  
  - **Grafana / 自建系统集成**：通过私有 Prometheus HTTP API 提供标准指标查询能力，详见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

> **注意**：文档1中称“模型用量页面数据延迟约为 1 小时”，而文档2明确区分普通监控（小时级）与高级监控（分钟级）——二者不矛盾，但需注意：**普通监控不提供首Token延时、TPS、单次请求日志等高级能力**，这些仅在开通高级监控后可用。开发者应依据 SLA 要求选择对应能力层级。

## 关键参数

| 参数 | 说明 | 来源约束 |
|------|------|----------|
| `workspace_id` | 业务空间 ID，为监控数据隔离与筛选的关键 Label | 必填（Prometheus 查询中需显式指定） |
| `model` | 模型 Code（如 `qwen-plus`），区分大小写 | 必填（Prometheus 查询中需显式指定） |
| `apikey_id` | API Key ID（非密钥本身），值为 `-1` 表示控制台调用 | 可选，用于按密钥维度归因 |
| `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC） | 影响性能分析粒度，异步调用常见于图像生成等场景 |
| `step` | Prometheus 查询时间步长，最小支持 `60s`（即分钟级） | 高级监控下有效；普通监控无此参数暴露 |

## 使用方式

1. **基础监控查看**：  
   进入 [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 页面，系统自动列出当前业务空间内所有已调用模型。点击某行「监控」可查看调用统计（失败详情、Token 消耗趋势）与性能指标（RPM、TPM、延时分布）；点击「日志」可查看已开通推理日志的调用记录。

2. **开通高级能力**：  
   在目标业务空间的模型监控页右上角点击「模型监控配置」，依次开通：  
   - 审计日志（用于操作审计）  
   - 推理日志（用于请求/响应内容记录，**必须开通才可查看单次 Token 用量与对话内容**）  
   > 开通后数据同步存在分钟级延迟，历史调用无法补录 —— 此限制在 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 中明确强调。

3. **创建告警规则**：  
   进入 [模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert) 页面，点击「创建告警规则」，选择模型、监控模板（如“失败率突增”、“TPM超阈值”）并配置通知渠道（短信/邮件/钉钉机器人/Webhook）。告警等级（INFO/ WARNING/ ERROR/ CRITICAL）决定通知方式组合。

4. **对接自建系统**：  
   获取 Prometheus HTTP API 地址后，使用标准 PromQL 查询，例如：  
   ```http
   GET {API}/api/v1/query_range?query=model_usage{workspace_id="llm-xxx",model="qwen-plus"}&start=2025-11-20T00:00:00Z&end=2025-11-20T23:59:59Z&step=60s
   ```  
   认证需提供 Base64 编码的 `AccessKey:AccessKeySecret`，且 AKSK 必须与 Prometheus 实例归属同一账号 —— 具体参数与指标清单见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 限制和注意事项

- **地域与模型支持限制**：  
  - 推理日志（含请求/响应内容）**仅支持北京、新加坡、弗吉尼亚地域**，且仅限文档2中明确列出的模型快照版本（如 `qwen3.7-plus-2026-05-26`）；未列明的模型或旧快照版本即使开通日志也无法记录内容。  
  - 上海地域虽支持高级监控，但**不支持推理日志**（文档2未提上海支持日志，仅列北京/新加坡/弗吉尼亚）。

- **数据时效性**：  
  - 普通监控（用量汇总、失败率等）延迟为 **1–2 小时**；  
  - 高级监控（推理日志、TPS、首Token延时）延迟为 **分钟级**；  
  - 免费额度数据在控制台**分钟级更新**，但账单中免费额度消耗记录按分钟汇总生成，存在轻微滞后。

- **权限与范围**：  
  - 子业务空间成员**仅能查看本空间数据**，无法跨空间筛选；  
  - 主账号可查看全部空间，但告警规则需在**目标业务空间内单独创建**；  
  - 开通推理日志需主账号或具备 `AliyunBaiLianFullAccess` 权限的 RAM 用户。

- **成本与计费**：  
  - 高级监控（含推理日志、TPS指标、Prometheus接入）为**收费功能**，具体资费以控制台报价为准；  
  - 免费额度用完即停功能开启后，若额度耗尽将返回 `403 AllocationQuota.FreeTierOnly` 错误 —— 此行为在 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) 中明确定义，开发者需在监控中重点告警该错误码。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


