# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标与资源消耗。它支持从基础用量统计到分钟级延迟分析的多维度监控，并可结合告警与日志回溯实现生产环境下的主动运维。该功能与[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)形成互补：前者侧重细粒度运行时指标与异常检测，后者聚焦账单级用量汇总与成本管理。

## 支持的模型/功能

- **监控覆盖范围**：  
  - 普通监控（小时级延迟）支持所有在[模型列表](https://help.aliyun.com/zh/model-studio/models)中可选的模型，包括基于它们调优后的[自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)；  
  - 高级监控（分钟级延迟，含TPS等指标）仅支持部署在北京、上海、新加坡、弗吉尼亚地域的模型；  
  - 告警功能仅支持北京、新加坡、弗吉尼亚地域的模型。  

- **关键功能**：  
  - 调用记录追踪（含Request ID、状态码、错误码）；  
  - 多维指标监控：RPM、TPM、调用时长、首Token延时（TTFT）、非首Token延时、失败率、限流错误次数、内容安全错误次数；  
  - Token消耗明细（按次、按业务空间、按API Key）；  
  - 推理日志（请求/响应内容）查看（需开通，且仅限[指定模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）；  
  - 告警规则配置（支持短信、邮件、钉钉、Webhook等通知方式）；  
  - Prometheus API对接，支持Grafana可视化或自建系统集成。

> **注意**：文档1中称“模型用量页面数据延迟约为1小时”，而文档2明确区分普通监控（小时级）与高级监控（分钟级），且强调推理日志为“分钟级延迟”。二者不矛盾，但需注意：**模型用量统计（如`model-usage-statistics.md`）仅提供聚合用量，不支持单次调用详情；而模型监控（`model-telemetry.md`）在开启高级监控后才提供分钟级指标与原始日志**。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspace_id` | 业务空间ID，用于过滤特定空间的数据，是Prometheus查询必需Label | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `model` | 模型Code（如`qwen-plus`），区分大小写，必须与控制台模型列表一致 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `apikey_id` | API Key ID（非密钥字符串），值为`-1`表示调用来自控制台 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC），影响延迟与吞吐特征 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `max_tokens` | 控制输出长度的关键请求参数，直接影响Token消耗与费用（见[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)） | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |

## 使用方式

1. **基础监控访问**：  
   进入[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面，选择目标业务空间，查看模型列表及汇总卡片（总调用次数、失败率、平均时长等）。

2. **查看模型详情**：  
   点击模型行右侧「监控」，切换「调用统计」与「性能指标」页签，支持按API Key、推理类型（实时/批量）、时间范围（最近30天）和时间精度（分钟/小时）筛选。

3. **启用高级能力（必选步骤）**：  
   - 在模型监控页面右上角点击「模型监控配置」，开通**审计日志**与**推理日志**（用于查看请求/响应）；  
   - 开启**性能和用量指标监控**（用于获取TPS、p99延迟等高级指标及Prometheus接入）。

4. **查看单次调用详情**：  
   点击「日志」，在表格中定位目标Request ID，展开「请求和响应」列查看原始输入输出及精确Token用量（仅限[支持的模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。

5. **配置告警**：  
   进入[模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert)页面，点击「创建告警规则」，选择模型、指标（如`model_call_count`突增）、阈值与通知方式。

6. **Prometheus API集成**：  
   获取私有Prometheus HTTP API地址后，使用标准Query Range接口拉取指标，例如：  
   ```http
   GET {API}/api/v1/query_range?query=model_usage{workspace_id="xxx",model="qwen-plus"}&start=...&end=...&step=60s
   ```

## 限制和注意事项

- **数据时效性**：  
  - 普通监控（用量汇总、失败率等）延迟约1–2小时；  
  - 高级监控（TPS、p99延迟、推理日志）延迟为分钟级，但需手动开通；  
  - **未开通推理日志前的历史调用无法补录**，日志功能仅对开通后的新调用生效。

- **地域与模型限制**：  
  - 高级监控、告警、推理日志功能**不支持杭州、深圳等非标地域**；  
  - 并非所有模型均支持请求/响应内容记录，具体支持列表详见[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中的「支持请求和响应的模型」章节。

- **权限与范围**：  
  - 主账号可查看全业务空间数据；子账号仅能查看其所属业务空间，且需被授予`AliyunBailianFullAccess`或等效权限；  
  - 「免费额度用完即停」开关仅在账户仍有未消耗免费额度时可开启，关闭需待额度完全耗尽后操作（见[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

- **计费提示**：  
  - 高级监控（含TPS指标、Prometheus实例）为**收费功能**，开通前请确认计费策略；  
  - 推理日志存储与传输会产生额外费用，建议按需开通并定期清理。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


