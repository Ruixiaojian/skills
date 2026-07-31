# model monitoring

模型监控（Model Monitoring）是百炼平台提供的用量与成本可观测能力，用于帮助开发者实时掌握模型调用行为、资源消耗及费用趋势。它覆盖所有已部署和调用的模型（包括调优后模型），支持按业务空间维度查看分钟级延迟的用量统计、免费额度状态、费用告警等核心指标。该能力不依赖额外埋点，直接对接平台底层计费与日志系统。

## 支持的模型与功能

- **支持的模型范围**：所有在[模型列表](https://help.aliyun.com/zh/model-studio/model-list)中可见的模型（含基于其调优后的模型）均支持用量监控，详见 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
- **核心监控维度**：
  - 免费额度使用概览（含“即将用尽 Top 3”模型识别）
  - 模型用量（调用次数、[Token](../concepts/token.md) 数、图像张数、视频秒数等，按模型 Code 统计）
  - 费用概览（账期总消费、订阅与账单费用、费用趋势图）
  - 用量告警（可配置阈值触发通知）
- **推理类型区分**：仅「大语言模型」页签支持按[实时推理](https://help.aliyun.com/zh/model-studio/model-telemetry#fde237cc636jb)或[批量推理](https://help.aliyun.com/zh/model-studio/batch-inference)筛选；其他模型类型（如视觉、语音）统一归入对应二级分类统计。

## 关键参数与统计单位

| 模型类型       | 二级分类             | 统计单位 | 计费说明                                                                 |
|----------------|----------------------|----------|--------------------------------------------------------------------------|
| 大语言模型     | 文本生成、深度思考等 | [Token](../concepts/token.md)    | 按输入 + 输出 [Token](../concepts/token.md) 总数计费；[Token 定义详见原文](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| 视觉模型       | 图像生成             | 张       | 按成功生成的图像张数计费                                                 |
|                | 视频生成             | 秒       | 按成功生成的视频秒数计费                                                 |
| 语音模型       | 语音合成、识别等     | 秒/字符/Token | 因模型而异，具体见[模型定价文档](https://help.aliyun.com/zh/model-studio/model-pricing) |
| 全模态模型     | Qwen-Omni 等         | Token    | 文本部分按 Token，[多模态输入](../concepts/multimodal-input.md)按等效 Token 数折算                          |
| 向量模型       | 多模态/文本向量      | Token    | 按输入文本 Token 数计费                                                  |

> **注意**：文档中“实时推理”定义包含模型广场、应用测试态/发布态、Prompt 反馈优化、模型评测等场景，但[模型监控](https://help.aliyun.com/zh/model-studio/model-telemetry)页面本身**不提供**这些场景的细粒度调用链路追踪（如具体 Prompt 内容、节点 ID），仅聚合用量。如需调试级日志，请结合[模型评测](https://help.aliyun.com/zh/model-studio/model-evaluation-overview)或应用内日志导出。

## 使用方式

1. **访问入口**：
   - 免费额度管理：[免费额度](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)
   - 模型用量查看：[模型用量](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/usage-statistics)
   - 费用概览：[费用概览](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/cost-overview)

2. **关键操作**：
   - 在「全部模型」表格中，可搜索模型 Code（如 `qwen-plus`）、切换「免费额度用完即停」开关、批量开启/关闭该策略；
   - 在用量页面，支持按时间范围（≤30 天）、时间精度（分钟/小时/天）、API-KEY、推理类型（仅 LLM）筛选；
   - 点击单行「查看详情」进入模型用量详情页，查看分钟级调用趋势与 Token 分布；
   - 「总调用成功次数 Top 10 模型」区域支持全屏与数据下载。

3. **告警配置**：在费用概览页设置费用告警阈值，异常时通过短信/邮件/钉钉通知；用量告警需通过[模型监控](https://help.aliyun.com/zh/model-studio/model-telemetry)控制台单独配置（当前文档未覆盖该路径，参见 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) 中“监控与告警”建议）。

## 限制和注意事项

- **数据延迟**：用量数据延迟约 1 小时，控制台支持手动刷新同步；免费额度数据为分钟级更新。
- **时间范围限制**：用量页面最多查询最近 30 天数据；更早记录需通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)页面导出账单获取。
- **统计维度限制**：用量与费用均按**业务空间**（Workspace）维度统计，**不支持按阿里云主账号或子账号汇总**（详见 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。
- **免费额度策略约束**：
  - “免费额度用完即停”仅可在仍有未消耗额度时开启；
  - 关闭该功能需等待免费额度完全耗尽后才可操作；
  - 批量操作失败时提示绑定有效支付方式。
- **Token 估算参考**：1 汉字 ≈ 1.5–2 Token，1 英文字母 ≈ 0.25 Token，1 英文单词 ≈ 1.3 Token；实际以模型分词器为准，超限将导致请求失败。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


