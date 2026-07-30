# application support

`application support` 指百炼平台为开发者构建和运行 AI 应用所提供的全链路支撑能力，涵盖模型调用、插件集成、RAG 增强、[流式输出](../concepts/streaming-output.md)等核心功能，以及配套的售后响应机制与服务边界说明。该支持体系面向生产环境设计，强调可配置性、可观测性与责任边界清晰性。具体能力与约束详见下文。

## 支持的模型/功能

- **内置插件能力**：当前官方提供六类插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索，按配置策略（如相似度得分）选取 topN 结果后融合生成，广泛应用于问答、客服、教育等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过符合协议的 API 接入，大模型可理解参数结构并自主调用；但**不支持透传自定义 Header**，仅保留 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：可通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 实现增量式[流式输出](../concepts/streaming-output.md)（即每次返回新片段，非全量重发）。  

> **注意**：文档 1 中第 4 条称 “Agent 和 Assistant API 的最大区别是……Assistant API 可以提供各种类，方便调优”，该描述模糊且未定义“类”指代对象（SDK 类？API 类型？），与百炼当前公开的 Assistant API 设计（基于 `messages` + `tools` 的标准调用范式）不符，建议以 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中其他明确参数说明为准，此条视为过时表述。

## 关键参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回） |
| `incremental_output` | bool | 在 `stream=True` 下启用增量模式（仅返回新增内容，非历史拼接） |
| `tool_choice` | string / object | 控制工具调用策略（如 `"auto"`、`{"type": "function", "function": {"name": "xxx"}}`） |
| `max_tokens` | int | 限制模型生成的最大 token 数（含输入 context） |
| `temperature` | float | 控制输出随机性（0.0–2.0，默认 1.0） |

> **注意**：`incremental_output` 仅在流式场景下生效，非流式请求中该参数无效。

## 使用方式

- **插件调用**：在 `tools` 数组中声明函数 schema，由模型自主决定是否及如何调用；自定义插件需确保 endpoint 可被百炼服务端直连（不经过用户侧代理或内网网关）。  
- **RAG 集成**：在应用配置中绑定知识库，系统自动注入检索结果至 [prompt](prompt.md) 上下文；测试阶段若回复不准确，可通过界面反馈按钮提交问题，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；上传时必填 `MD5` 校验值以保障文件完整性。  
- **备案与合规**：上架应用市场或小程序前，须完成[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)，并单独申请通义千问合作协议 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  

## 限制和注意事项

- **插件限制**：自定义插件不支持除 `Authorization` 外的任何 HTTP Header 透传；插件调用超时默认为 30 秒，不可配置。  
- **数据规模**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **结构化数据导入**：表格中存在空行将导致后续数据被截断（含首行为空则视为无效文件）。  
- **售后支持边界**：  
  - ✅ 覆盖：API 故障诊断、SDK 使用、控制台操作、计费核查、百炼服务端连通性测试；  
  - ❌ 不覆盖：第三方工具（如 Cursor、Windsurf）的部署/配置/调试、用户本地网络/防火墙/代理问题、业务代码实现、非百炼侧服务的运维支持 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **法律协议**：使用前须接受《阿里云百炼服务协议》《体验功能特别说明》及开源模型相关条款 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


