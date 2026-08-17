# application support

`application support` 指百炼平台为开发者构建和运行 AI 应用所提供的全链路支撑能力，涵盖模型调用、插件集成、RAG 增强、[流式输出](../concepts/streaming-output.md)等核心功能，以及配套的售后响应机制与服务边界说明。该支持体系面向生产环境设计，强调可配置性、可观测性与责任边界清晰性。具体能力与约束详见下文。

## 支持的模型/功能

- **内置插件能力**：当前官方提供 6 类插件，包括 Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索，按配置策略（如相似度得分）选取 topN 结果后融合生成；适用于问答、客服、教育等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件/API**：支持通过协议注册函数或 API，大模型可理解参数结构并参与调用决策；但**仅支持 `Authorization` header 透传，不支持其他自定义 header** [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：可通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 实现增量式[流式输出](../concepts/streaming-output.md)（即每次返回新 token 而非全量重发）。  

> **注意**：文档 1 中第 4 条称 “Assistant API 可提供各种类，方便调优”，但未明确定义“类”指代 SDK 接口、抽象封装还是模型能力分组；该表述缺乏上下文与技术定义，建议以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中明确的 API/SDK 故障诊断范围为准，避免歧义。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（默认 `False`） |
| `incremental_output` | bool | 在 `stream=True` 下启用增量式流式（默认 `False`）；若为 `True`，每次响应仅含新增内容 |
| `MD5`（文件上传） | string | 必填，用于校验文件完整性，防止传输损坏 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) |

## 使用方式

- **插件调用**：在应用编排中配置插件节点，自定义插件需按 OpenAPI Schema 注册；调用时由大模型自动选择并填充参数。  
- **RAG 配置**：在知识库设置中指定分块策略、嵌入模型及检索 TopK；测试阶段若结果不准，可通过界面反馈按钮提交问题，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入需确保无空行，否则后续行将被跳过 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **合规与备案**：接入通义千问模型上架应用市场或小程序前，须完成[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)并申请合作协议。  

## 限制和注意事项

- **第三方工具支持边界**：阿里云百炼售后**不负责**第三方工具（如 Cursor、Windsurf 等）的安装、配置、升级或故障排查；仅提供方向性建议，例如连通性测试、官方 SDK 示例参考、计费明细核查等 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **服务容量限制**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **协议约束**：使用百炼服务须遵守《阿里云百炼服务协议》及《阿里云百炼体验功能特别说明》，开源模型还需符合对应[开源模型协议条款](https://help.aliyun.com/zh/model-studio/open-source-model-terms) [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。  
- **责任免责**：阿里云不对外部第三方工具的陈述、行为或故障承担责任；所有非百炼平台自身（API、控制台、计费系统等）引发的问题，均不在标准售后保障范围内 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


