# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标与资源消耗。它支持从基础用量统计到分钟级推理日志的全链路观测，并可基于关键指标（如失败率、首[Token](../concepts/token.md)延时、TPM/RPM、[Token](../concepts/token.md)异常消耗）配置主动告警。该功能面向生产环境稳定性保障与成本精细化治理，不依赖应用层埋点，数据自动采集于模型服务网关层。

## 支持的模型/功能

- **监控覆盖范围**：  
  - 普通监控（免费）支持[所有在模型列表中可选的模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)，包括基于其调优的自定义模型；  
  - 高级监控（需开通，按地域计费）支持北京、上海、新加坡、弗吉尼亚地域下的全部模型；  
  - 告警功能仅限北京、新加坡、弗吉尼亚地域模型（上海地域暂不支持告警）；  
  - 推理日志（含请求/响应内容）仅对[明确列出的支持模型](../../raw/model-user-guide/model-monitoring/model-telemetry.md)生效，例如 `qwen3-plus`、`qwen3-flash`、`qwen-turbo` 及部分开源/三方模型，不支持的模型界面将提示“当前模型暂不支持日志”。

- **核心功能模块**：  
  - 调用记录追踪（含 Request ID、状态码、错误码、用量）；  
  - 多维指标监控：安全（内容安全错误次数）、成本（单次平均[Token](../concepts/token.md)用量）、性能（RPM、TPM、调用时长、首Token延时、非首Token延时）、错误（失败率、限流错误次数）；  
  - Token 消耗细粒度追踪（汇总 + 单次调用级）；  
  - 主动告警（支持失败率突增、TPM超阈值、首Token延时超标等场景）；  
  - Grafana 与自建系统集成（通过私有 Prometheus HTTP API）。

> **注意**：文档1中称“模型用量统计延迟约为 1 小时”，而文档2明确区分普通监控（小时级延迟）与高级监控/推理日志（分钟级延迟）。二者无矛盾，但需注意：**普通监控无法满足实时诊断需求，分钟级洞察必须开通高级监控**。该差异已在[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中明确定义。

## 关键参数

| 参数 | 说明 | 来源约束 |
|------|------|----------|
| `workspace_id` | 业务空间ID，监控数据按此维度隔离与聚合 | 必填（所有API查询与控制台筛选均以此为前提） |
| `model` | 模型Code（如 `qwen-plus`），区分大小写 | 控制台搜索与Prometheus查询均支持精确匹配 |
| `apikey_id` | API Key ID（非密钥本身），用于归因调用来源 | 在[密钥管理](../../raw/model-user-guide/model-monitoring/model-telemetry.md)页面获取；值为 `-1` 表示控制台内调用 |
| `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC） | 影响性能指标分布，例如 ASYNC 常见于图像生成，其首Token延时无意义 |
| `start` / `end` / `step` | Prometheus 查询时间范围与步长 | `step` 最小支持 `60s`；超过7天跨度时仅允许 `step=86400s`（按天） |

## 使用方式

1. **控制台入口**：  
   - 进入[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面，选择目标业务空间；  
   - 在模型列表中点击目标模型操作列的 **监控** 查看指标趋势，或点击 **日志** 查看调用明细（需已开通推理日志）；  
   - 点击右上角 **模型监控配置** 开通高级监控、审计日志与推理日志（开通后数据延迟降至分钟级）。

2. **告警配置**：  
   - 进入[模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert)页面；  
   - 确保已开启高级监控 → 点击 **创建告警规则** → 选择模型、指标模板（如“失败率突增”）、阈值与通知渠道（短信/邮件/钉钉等）。

3. **Prometheus API 集成**：  
   - 获取私有Prometheus实例的HTTP API地址（通过模型监控配置页）；  
   - 构造标准 `/api/v1/query_range` 请求，例如：  
     ```http
     GET {API}/api/v1/query_range?query=model_usage{workspace_id="llm-xxx",model="qwen-plus"}&start=2025-11-20T00:00:00Z&end=2025-11-20T23:59:59Z&step=60s
     Authorization: Basic base64Encode(AccessKey:AccessKeySecret)
     ```

4. **Token 消耗定位**：  
   - 在模型详情页的 **调用统计** 页签查看历史Token汇总；  
   - 在 **日志** 页签的“用量”列直接读取单次调用Token数（仅限支持推理日志的模型）；  
   - 更早数据请导出[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)账单。

## 限制和注意事项

- **地域限制**：高级监控、告警、推理日志功能**仅在北京、新加坡、弗吉尼亚地域可用**；上海地域目前仅支持普通监控（小时级延迟），且不支持告警（见[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。
- **数据时效性**：  
  - 普通监控（默认开启）：用量汇总延迟约 1–2 小时；  
  - 高级监控/推理日志：数据延迟为分钟级，但**仅记录开通后的新调用**，历史数据不可补录；  
  - 模型用量页面（文档1所述）与模型监控页面（文档2所述）数据源不同，前者侧重计费口径，后者侧重运行时指标，二者数值可能因统计周期与过滤逻辑存在微小差异。
- **权限隔离**：子业务空间成员**仅能查看本空间数据**，无法跨空间筛选或切换；主账号可查看全部空间。
- **模型兼容性**：并非所有模型均支持推理日志。是否支持由模型服务端能力决定，与模态（文本/[多模态](../concepts/multi-modal.md)）无关。不支持时界面明确提示，不可强制启用。
- **免费额度联动**：“免费额度用完即停”开关位于[免费额度](https://bailian.console.aliyun.com/cn-beijing/?tab=costing-balance#/costing-balance/free-quota)页面，**与模型监控功能独立**；监控本身不触发停服，仅提供用量预警（见[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


