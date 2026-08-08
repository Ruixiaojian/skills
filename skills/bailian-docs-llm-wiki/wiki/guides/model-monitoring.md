# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时跟踪模型调用行为、性能指标、成本消耗及安全风险。它覆盖从基础用量统计到高级性能告警的全链路监控场景，支持开发者快速定位异常、优化成本并保障服务稳定性。该功能与[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)形成互补：前者侧重细粒度运行时指标与日志，后者聚焦账单级用量汇总与免费额度管理。

## 支持的模型/功能

- **监控范围**：  
  - *普通监控*（免费）：支持所有在[模型列表](https://help.aliyun.com/zh/model-studio/models)中可选的模型，包括基于其调优的[自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)；  
  - *高级监控*（收费）：仅限北京、上海、新加坡、弗吉尼亚地域下的模型；  
  - *告警功能*：仅支持北京、新加坡、弗吉尼亚地域下的模型。  

- **核心功能**：  
  - 调用记录追踪（含 Request ID、状态码、错误码）；  
  - 实时性能指标：RPM、TPM、调用时长、首 [Token](../concepts/token.md) 延时（TTFT）、非首 [Token](../concepts/token.md) 延时；  
  - 成本监控：单次调用 [Token](../concepts/token.md) 消耗、历史 Token 汇总；  
  - 安全审计：内容安全错误次数（涉黄/涉政/广告等拦截）；  
  - 日志回流：将推理日志导出为训练数据集。  

> **注意**：文档 1 中称“模型列表中的所有模型均支持查看用量”，而文档 2 明确区分了普通监控与高级监控的地域限制。实际能力以[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)为准——**用量统计（文档 1）无地域限制，但细粒度性能指标、日志与告警（文档 2）受地域约束**。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspace_id` | 业务空间 ID，监控数据按此维度隔离；子空间成员仅能查看当前空间数据 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `apikey_id` | API Key ID（非密钥本身），用于按调用方筛选用量；值为 `-1` 表示调用源自控制台 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `model` | 模型 Code（如 `qwen-plus`），必须与模型列表中一致 | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| `protocol` / `sub_protocol` | 协议类型（HTTP/SSE/WS）与子协议（DEFAULT/ASYNC），影响延时与吞吐分析 | [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

## 使用方式

1. **基础监控（控制台）**：  
   - 进入 [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 页面，按模型 Code 或业务空间筛选；  
   - 点击操作列 **监控** 查看安全/成本/性能/错误四类指标；  
   - 点击 **日志** 查看已开通推理日志的调用详情（含输入/输出、Token 用量）。  

2. **高级监控与告警**：  
   - 在目标业务空间的模型监控页点击 **模型监控配置** → 开启 **性能和用量指标监控**；  
   - 进入 [模型告警](https://bailian.console.aliyun.com/?tab=model#/model-alert) → 创建规则，支持按 RPM、TPM、失败率、TTFT 等阈值触发；  
   - 通知方式支持短信、邮件、钉钉机器人、Webhook 等。  

3. **API 集成（Prometheus）**：  
   - 获取私有 Prometheus HTTP API 地址（需开启高级监控）；  
   - 使用标准 PromQL 查询，例如：  
     ```http
     GET {API}/api/v1/query_range?query=model_usage{workspace_id="xxx",model="qwen-plus"}&start=...&end=...&step=60s
     ```  
   - 认证需提供 Base64 编码的 `AccessKey:AccessKeySecret`。  

## 限制和注意事项

- **数据延迟**：  
  - 普通监控（用量汇总）延迟约 **1 小时**，高峰期可达 2 小时；  
  - 高级监控（推理日志、实时指标）延迟为 **分钟级**；  
  - 免费额度数据支持手动刷新，以控制台显示为准。  

- **地域与模型限制**：  
  - 推理日志（请求/响应内容）**仅支持特定模型版本**（如 `qwen3-plus-2025-12-01+`），不支持的模型会明确提示；  
  - 弗吉尼亚地域虽支持告警，但部分文档链接指向北京控制台，实际操作请切换至对应地域控制台。  

- **功能依赖**：  
  - 日志与告警功能**仅记录开启后的新调用**，历史调用无法补录；  
  - “免费额度用完即停”开关仅在账户仍有未消耗额度时可开启，关闭需待额度完全耗尽后操作；  
  - 批量操作（如批量开启即停）需账号已绑定有效支付方式，否则失败。  

- **用量统计口径差异**：  
  - 文本生成类模型按 **Token** 计费（输入+输出）；  
  - 图像生成按 **张**；视频生成按 **秒**；语音合成按 **秒/字符/Token**（依模型而定）；  
  - 具体计费单位详见[模型用量统计单位说明](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


