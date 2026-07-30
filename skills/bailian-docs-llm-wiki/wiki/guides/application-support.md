# application support

application support 指百炼平台为应用开发者提供的模型调用、插件集成、RAG增强、API使用及售后支持等能力集合。它覆盖从功能配置、参数控制到问题排查的全生命周期，适用于构建智能体（Agent）、[知识库](../concepts/knowledge-base.md)问答、流式交互等典型场景。开发者需结合官方协议与服务边界合理规划集成方案。

## 支持的模型/功能

- **插件能力**：平台官方支持六类插件：Python代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub搜索；部分插件需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG检索增强**：支持多[知识库](../concepts/knowledge-base.md)并行检索，按配置得分选取 topN 结果，广泛应用于问答系统、客户服务、教育与内容创作等领域 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过符合协议的 API 接入，大模型可理解参数结构并生成调用逻辑；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
> **注意**：文档 1 中“Assistant API 可提供各种类，方便调优”表述模糊且未明确定义“类”的语义，与当前百炼 SDK 文档中 `Assistant` 作为封装调用入口的定位不一致，建议以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中明确的 API 和 SDK 支持范围为准。

## 关键参数

- `stream=True`：启用[流式输出](../concepts/streaming-output.md)，返回分块响应。  
- `incremental_output=True`：启用增量式[流式输出](../concepts/streaming-output.md)（区别于全量重传），适用于前端逐字渲染场景。  
- 文件上传必需 `MD5` 参数：用于校验文件完整性，避免传输损坏。  
- RAG 检索依赖[知识库](../concepts/knowledge-base.md)配置的 `top_k` 与相关性阈值，无全局串行顺序，实际为并行检索后聚合排序。

## 使用方式

- 插件调用需在应用配置中显式启用，并确保权限已开通；自定义插件需遵循 OpenAPI Schema 协议注册。  
- RAG 应用调试时若出现回复不准，可通过界面反馈按钮提交问题，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- Markdown 渲染需由前端自行解析（如 `**text**` → `<strong>text</strong>`），百炼 API 不做富文本转换。  
- 外部第三方工具（如 Cursor、Windsurf）接入百炼 API 时，仅能获得方向性建议（如连通性测试、SDK 示例），具体部署与运维责任归属用户或工具方 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- 文件上传仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入时，空行将导致后续行被截断。  
- 单业务空间最多上传 10 万个文档，超限时需提交工单申请扩容。  
- 自定义插件不支持除 `Authorization` 外的任何 HTTP Header 透传；函数参数理解依赖模型对 Schema 的泛化能力，非强类型校验。  
- 售后支持范围明确排除：第三方工具运维、本地网络/代理/防火墙问题排查、业务代码编写指导、非百炼侧服务的故障诊断 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- 所有服务受《[阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md)》约束，体验功能另需遵守《阿里云百炼体验功能特别说明》。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


