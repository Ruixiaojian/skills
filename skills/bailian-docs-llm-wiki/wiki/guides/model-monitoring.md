# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标、成本消耗及安全风险。它支持从基础用量统计到分钟级推理日志的全链路观测，并提供告警、Grafana对接和自建系统集成能力。所有监控数据按“模型 + 业务空间”维度隔离，确保租户级数据隐私与权限控制。

## 支持的模型/功能

- **监控覆盖范围**：普通监控支持[选择模型](https://help.aliyun.com/zh/model-studio/models)中全部公开模型及基于其调优的[自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)；高级监控（含分钟级日志与Prometheus指标）仅限北京、上海、新加坡、弗吉尼亚地域下的模型 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **日志支持模型**：仅部分模型支持请求/响应内容记录，包括 `qwen3-max` 系列、`qwen-plus` 系列、`qwen-flash`、`qwen-turbo`、`qwen3-coder-*`、开源模型（如 `qwen3-235b-a22b`）及三方模型（如 `deepseek-v3.1`）。不支持的模型在日志页签会明确提示“当前模型暂不支持日志” [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **用量统计范围**：所有模型均支持用量查看，包括调优后模型，但免费额度管理仅对已开通服务的模型生效 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。  
> **注意**：文档1称“高级监控支持北京、上海、新加坡、弗吉尼亚”，而文档2未提上海地域；实际以控制台可用地域为准，上海地域支持需确认控制台界面是否显示对应入口。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识，用于过滤特定空间数据 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `model` | 模型Code（如 `qwen-plus`），区分大小写 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `apikey_id` | API Key ID（非密钥本身），值为 `-1` 表示调用源自百炼控制台 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `protocol` / `sub_protocol` | 协议类型（`HTTP`/`SSE`/`WS`）与子协议（`DEFAULT`/`ASYNC`），影响TPS等指标计算逻辑 | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `user_id` | 阿里云账号UID（RAM用户为RAM UID） | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

## 使用方式

1. **启用监控**：  
   - 普通监控自动开启，无需配置；  
   - **高级监控（含分钟级日志与Prometheus指标）需手动开通**：进入目标业务空间的[模型监控配置](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)，开启“性能和用量指标监控”及“推理日志” [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  

2. **查看数据**：  
   - **用量与概览**：访问[模型用量](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/usage-statistics)页面，支持按模型、API Key、时间精度（分钟/小时/天）筛选，数据延迟约1小时 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)；  
   - **详细指标**：点击模型列表中的「监控」，查看安全、成本、性能、错误四类指标，支持按API Key、推理类型（实时/批量）、时间范围筛选；  
   - **原始日志**：点击「日志」，查看含Request ID、状态码、用量、请求/响应内容的调用记录（仅限支持模型且已开通推理日志） [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  

3. **接入外部系统**：  
   - 获取Prometheus HTTP API地址后，通过标准PromQL查询指标（如 `model_usage{workspace_id="xxx",model="qwen-plus"}`），支持Basic Auth认证 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  

## 限制和注意事项

- **数据延迟**：普通监控（调用次数、[Token](../concepts/token.md)总量）延迟为**小时级**（高峰期可达1–2小时）；高级监控（推理日志、Prometheus指标）延迟为**分钟级**；免费额度数据分钟级更新，支持手动刷新 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **地域与功能绑定**：告警功能仅支持北京、新加坡、弗吉尼亚地域；上海地域虽在文档1中被列为高级监控支持地域，但文档2未提及，实际使用前请以控制台功能开关为准。  
- **历史数据不可追溯**：所有日志与高级指标仅从**开通对应功能后**开始采集，开通前调用无数据补录 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **权限隔离**：子业务空间成员**仅能查看本空间数据**，无法切换或跨空间查询；主账号成员可查看全部业务空间 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **[Token](../concepts/token.md)统计口径**：大语言模型按输入+输出[Token](../concepts/token.md)计费；视觉模型按“张”、视频按“秒”、语音模型按“秒/字符/Token”计费，详见[模型用量统计单位说明](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)
- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


