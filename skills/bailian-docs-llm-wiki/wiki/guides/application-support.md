# application support

`application support` 指百炼平台为开发者在构建和运行 AI 应用（如智能体、RAG 应用、插件集成等）过程中提供的功能支持、接口能力、参数配置及配套服务保障。它覆盖模型调用、插件扩展、知识库检索、[流式输出](../concepts/streaming-output.md)等核心开发环节，并包含明确的服务边界与售后支持范围。开发者需结合具体场景选择合适的能力组合，并注意平台限制与协议约束。

## 支持的模型/功能

- **内置插件能力**：当前官方支持六类插件，包括 Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；部分插件需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置得分选取 topN 结果后融合生成，适用于问答系统、客服、教育等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件/API 函数**：支持通过协议声明函数签名，大模型可理解参数结构并生成调用请求；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：可通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 实现增量式[流式输出](../concepts/streaming-output.md)（即每次返回新 token 而非全量重发）。  

> **注意**：文档中提及“Agent 和 Assistant API 的最大区别是调整插件模型、基于上下文的理解，用户可以自己去开发”，该描述模糊且未定义关键术语（如“调整插件模型”具体指代何种操作），与当前百炼控制台实际能力不符；建议以[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)中明确的服务边界为准，避免对能力边界产生误判。

## 关键参数

| 参数名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md) | `True` |
| `incremental_output` | bool | 启用增量式[流式输出](../concepts/streaming-output.md)（需配合 `stream=True`） | `True` |
| `MD5` | string | 文件上传必填，用于校验文件完整性 | `"d41d8cd98f00b204e9800998ecf8427e"` |

## 使用方式

- 插件调用：在智能体配置中启用对应插件，自定义插件需按 OpenAPI Schema 规范定义函数描述；调用时由大模型自动解析参数并构造请求。  
- RAG 应用：上传 PDF/DOC/DOCX 格式知识文档（注意 PDF 后缀必须为小写 `pdf`），单业务空间上限 10 万文档，超限时需提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- 错误排查：RAG 输出不准确时，可通过回复下方“问题反馈”按钮提交，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- 渲染处理：模型输出含 `**text**` 等 Markdown 语法时，需在前端自行解析渲染，平台不提供富文本转换能力。  

## 限制和注意事项

- **Header 限制**：自定义插件调用时，仅支持透传 `Authorization` 请求头，其他 Header（如 `X-User-ID`、`Cookie`）将被丢弃。  
- **文件格式与结构**：上传文件仅支持 `.pdf`（小写）、`.doc`、`.docx`；结构化数据导入时，空行会导致后续行被跳过，首行为空则视为无效文件 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **第三方工具支持边界**：阿里云百炼仅保障自身服务端（API、SDK、控制台、计费系统）的可用性与正确性；对 Cursor、Windsurf 等第三方工具的安装、配置、本地环境（代理/防火墙/OS）或业务代码问题，不提供直接支持，仅提供方向性建议 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：使用前须遵守《阿里云百炼服务协议》《体验功能特别说明》及开源模型相关条款，详见 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)




