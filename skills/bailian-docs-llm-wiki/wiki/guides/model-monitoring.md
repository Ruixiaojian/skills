# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能表现、成本消耗及安全合规性。它覆盖从基础调用统计到高级指标告警、日志回溯与外部系统集成的全链路监控场景，适用于生产环境下的稳定性保障与精细化成本治理。所有监控数据按“模型 + 业务空间”维度隔离，确保租户级数据可见性与权限收敛。

## 支持的模型/功能

- **监控覆盖范围**：  
  - **普通监控**（免费）支持[选择模型](https://help.aliyun.com/zh/model-studio/models)中的全部模型，包括基于其调优的[自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)；  
  - **高级监控**（收费）仅支持北京、上海、新加坡、弗吉尼亚地域下的模型；  
  - **告警功能**仅限北京、新加坡、弗吉尼亚地域（见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。  

- **日志能力限制**：  
  推理日志（含请求/响应内容）**并非所有模型均支持**，仅限明确列出的千问系列（如 `qwen3-max`、`qwen-plus`、`qwen-flash` 等）、部分开源模型（如 `qwen3-235b-a22b`）及三方模型（如 `deepseek-v3.1`）。不支持的模型在界面显示“当前模型暂不支持日志”。该能力与模型是否为多模态无关，且**仅记录开启推理日志后的调用**（见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。  

- **用量统计口径**：  
  不同模型类型采用不同计费单位：大语言模型按 **[Token](../concepts/token.md)**，图像生成按 **张**，视频生成按 **秒**，语音模型按 **秒/字符/[Token](../concepts/token.md)**（视具体模型而定），全模态模型文本部分按 [Token](../concepts/token.md)、其他模态按对应 Token 数（见 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

> **注意**：文档1称“高级监控支持北京、上海、新加坡、弗吉尼亚地域”，但文档2未提及上海地域对高级监控的支持；实际开通时请以控制台配置页为准，上海地域支持状态可能存在滞后或未同步更新。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **过滤标签（LabelKey）** | `workspace_id`, `model`, `apikey_id`, `user_id`, `protocol`, `sub_protocol` | 用于Prometheus API查询过滤，例如 `model_usage{workspace_id="llm-nymssti2mzww****",model="qwen-plus"}`；`apikey_id=-1` 表示调用源自百炼控制台（见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)） |
| **核心监控指标** | `model_call_count`, `model_usage`, `model_call_duration`, `model_first_token_duration`, `model_generation_duration_per_token`, `model_tps_per_request` | 其中 `model_tps_per_request` 仅高级监控提供，且与非首Token延时呈倒数关系（TPS ≈ 1 ÷ 非首包时长均值） |
| **告警等级** | `INFO` / `WARNING` / `ERROR` / `CRITICAL` | 不可自定义；通知渠道绑定严格（如 `CRITICAL` 仅支持电话/短信/邮件） |

## 使用方式

1. **启用基础监控**：  
   无需手动开通，主账号下所有业务空间的模型调用数据自动采集（延迟：普通监控小时级，高峰期达1–2小时）。

2. **开通高级能力（日志/告警/Prometheus）**：  
   - 进入目标业务空间的[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面 → 右上角「模型监控配置」→ 开启**审计日志**、**推理日志**（日志）或**性能和用量指标监控**（告警与Prometheus）；  
   - 开通后数据延迟为分钟级（见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。

3. **查看与分析**：  
   - 在模型监控列表点击「监控」查看安全/成本/性能/错误四类指标；  
   - 点击「日志」查看带Token用量、请求/响应内容的调用明细（需模型支持且已开通推理日志）；  
   - 在[模型用量](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/usage-statistics)页面按业务空间、时间范围、API Key筛选用量趋势（延迟约1小时）。

4. **接入外部系统**：  
   - 获取Prometheus HTTP API地址后，通过标准Query API拉取指标（如 `GET {HTTP API}/api/v1/query_range?query=model_usage&start=...&end=...&step=60s`）；  
   - Authorization头需使用同一阿里云账号的 `AccessKey:AccessKeySecret` Base64编码（见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。

## 限制和注意事项

- **地域与功能绑定**：告警、高级监控、推理日志均**不支持杭州、深圳等非标地域**，仅限北京/上海/新加坡/弗吉尼亚（文档1明确列出，文档2未覆盖此约束，以文档1为准）。
- **数据时效性**：  
  - 普通监控（调用次数、Token总量）延迟 **1–2小时**；  
  - 高级监控（日志、TPS、分钟级指标）延迟 **分钟级**；  
  - 免费额度数据分钟级更新，账单费用数据按分钟汇总（见 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。
- **历史数据不可追溯**：所有日志与高级指标**仅从开通功能后开始采集**，开通前调用无数据补录。
- **权限隔离**：子业务空间成员**仅能查看本空间数据**，无法切换查看其他业务空间（见 [模型监控 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。
- **Token估算差异**：中文平均1.5–2 Token/字，英文单词约1.3 Token/词；实际分词结果受模型tokenizer影响，`max_tokens`设置不当可能导致截断或失败（见 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

## 来源文档

- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)
- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


