# application support

百炼平台的应用支持体系面向开发者提供模型调用、插件集成、RAG增强、[流式输出](../concepts/streaming-output.md)等核心能力，同时明确划定了服务边界与技术限制。本文档结构化梳理关键能力、参数配置、使用方式及注意事项，帮助开发者快速定位可用能力与支持范围。所有功能均需在阿里云百炼控制台或通过 Assistant API 调用，部分能力需申请开通。

## 支持的模型/功能

- **内置插件能力**：当前官方支持六类插件：Python代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub搜索；其中部分插件需[申请通过后方可使用](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置策略打分后选取 topN 结果融合生成；已广泛应用于问答系统、对话系统、客户服务、教育与内容创作等场景（详见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)）。  
- **自定义插件/API**：支持注册符合 OpenAPI 3.0 规范的 HTTP 接口，大模型可理解其参数定义并自主编排调用；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第10条）。  
- **流式与增量输出**：可通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 实现增量式[流式输出](../concepts/streaming-output.md)（即每次返回新 token，而非全量重发），适用于前端实时渲染场景。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | bool | 启用流式响应（SSE 格式） | 否（默认 `False`） |
| `incremental_output` | bool | 在 `stream=True` 下启用增量输出模式（避免重复返回历史 tokens） | 否（默认 `False`） |
| `file_md5` | string | 上传文件时必填，用于校验文件完整性（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第3条） | 是（仅限文件上传接口） |
| `knowledge_base_ids` | array[string] | 指定参与 RAG 检索的知识库 ID 列表 | 否（未指定则不启用 RAG） |

> **注意**：文档 1 中第4条称“Assistant API 可以提供各种类，方便调优”，但未说明具体类名或 SDK 接口形态；而当前百炼 Python SDK 中实际暴露的是 `AssistantClient` 及 `create_run` 等方法，无泛化“类库”概念。该描述易引发误解，建议以 [SDK 文档](https://help.aliyun.com/zh/model-studio/developer-reference/assistant-api) 为准。

## 使用方式

- **插件调用**：在应用配置中启用对应插件，或在 Assistant API 请求体中通过 `tools` 字段声明（格式同 OpenAI Tools）；自定义插件需先在控制台完成注册与授权。  
- **RAG 集成**：上传文件至知识库（仅支持小写后缀 `.pdf`、`.doc`、`.docx`；见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第1条），并在应用/调用时绑定知识库 ID。  
- **错误反馈与调试**：RAG 输出不准确时，可通过界面“问题反馈”按钮提交，或复制 `RequestId` 提交工单（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第6条）。  
- **合规与备案**：若应用需上架至外部应用市场或小程序平台，须按 [应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model) 流程完成备案，并单独申请通义千问合作协议。

## 限制和注意事项

- **文件与数据限制**：单业务空间最多上传 10 万个文档；结构化数据导入时，空行将导致后续行被截断（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第2、4条）。  
- **第三方工具支持边界**：阿里云百炼售后**不支持**第三方工具（如 Cursor、Windsurf 等）的安装、配置、升级或故障排查；仅提供方向性建议，例如连通性测试、API 示例参考、计费明细核查等（详见 [售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 第4条）。  
- **协议约束**：使用前须接受《阿里云百炼服务协议》及《体验功能特别说明》，开源模型还需遵守对应 [开源模型协议条款](../../raw/application-user-guide/application-support/application-related-agreements.md)。  
- **Header 限制**：自定义插件调用时，仅 `Authorization` 头可被透传至目标服务，其他 header（如 `X-User-ID`、`X-Tenant`）将被丢弃——此为硬性限制，非配置问题（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第10条）。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


