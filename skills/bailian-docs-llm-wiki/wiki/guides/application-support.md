# application support

`application support` 指百炼平台为开发者在构建和运行 AI 应用（含智能体、RAG 应用、插件集成等）过程中提供的功能能力、调用参数、使用规范及配套支持服务。它覆盖模型能力接入、插件扩展、知识库增强、API 调用控制，以及售后响应边界等关键环节。开发者需结合具体场景选择合适的能力组合，并注意平台对第三方集成与自定义行为的明确限制。

## 支持的模型/功能

- **内置插件能力**：当前官方支持六类插件，包括 Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；部分插件需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 知识检索增强**：支持多知识库并行检索，按配置策略打分后取 topN 结果，适用于问答系统、客服、教育等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件/API 集成**：支持通过协议注册自定义函数或 API，大模型可理解其参数结构并生成调用逻辑；但**仅支持 `Authorization` header 透传，不支持其他自定义 header** [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：可通过 `stream=True` 启用流式响应，进一步设置 `incremental_output=True` 实现真正增量式 token 输出（非全量重发）。  

> **注意**：文档中提及“Agent 和 Assistant API 的最大区别是‘调整插件模型、基于上下文的理解，用户可以自己去开发’”，该描述模糊且未定义技术边界；实际中两者均支持插件编排与上下文感知，差异主要体现在抽象层级与 SDK 封装粒度，建议以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中定义的服务支持范围为准。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回），默认 `False` |
| `incremental_output` | bool | 在 `stream=True` 下启用增量式输出（避免重复返回历史内容），默认 `False` |
| `MD5`（上传接口） | string | 文件完整性校验值，必填；用于验证上传文件是否完整 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) |

## 使用方式

- **插件调用**：在应用配置中启用对应插件，自定义插件需按 OpenAPI Schema 注册元数据，模型将基于描述自动推理参数。  
- **RAG 应用调试**：若检索结果不准确，可通过界面反馈按钮提交问题，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **前端渲染**：模型输出含 `**text**` 等 Markdown 格式时，需由前端自行解析并渲染（平台不提供富文本转换服务）。  
- **文件上传**：仅支持 `.pdf`、`.doc`、`.docx`；PDF 文件后缀必须为小写 `pdf`，否则报错 `140010` [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  

## 限制和注意事项

- **插件 header 限制**：调用自定义插件时，仅允许透传 `Authorization` header，其他 header（如 `X-User-ID`、`Cookie`）会被丢弃。  
- **知识库容量**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容。  
- **结构化数据导入**：表格中存在空行会导致后续数据被跳过（尤其首行为空时视为无效文件）。  
- **第三方工具支持边界**：阿里云百炼仅保障自身服务端可用性、API 正确性及计费一致性；对 Cursor、Windsurf 等第三方工具的安装、配置、本地环境兼容性、[Token](../concepts/token.md) 统计偏差等问题**不提供技术支持** [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **合规与备案**：接入通义千问模型并上架应用市场/小程序前，须完成[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)并申请合作协议。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


