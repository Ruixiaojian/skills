# application support

`application support` 指百炼平台为开发者在构建和运行 AI 应用（含智能体、RAG 应用、插件集成等）过程中提供的功能能力、调用接口、参数配置及配套支持服务。它覆盖模型/插件调用、流式与增量输出、知识检索增强（RAG）、文件与数据管理，以及售后响应边界等关键环节。开发者需结合具体场景选择合适的能力组合，并注意平台对自定义行为（如 header 透传、插件协议）的明确限制。

## 支持的模型/功能

- **内置插件能力**：当前官方支持六类插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持多知识库并行检索，按用户配置策略执行检索，再基于得分选取 topN 结果用于生成；已广泛应用于问答系统、对话系统、客户服务、教育与内容创作等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件/API**：支持通过标准协议注册自定义函数或 API，大模型可理解其参数结构并参与推理调用；但**仅支持 `Authorization` header 透传，不支持其他自定义 header** [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：可通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 可启用增量式[流式输出](../concepts/streaming-output.md)（即每次返回新生成 token，而非全量重发）。

> **注意**：文档 1 中第4条称“Agent 和 Assistant API 的最大区别是……Assistant API 可以提供各种类，方便调优”，该表述模糊且未定义“类”指代对象（SDK 类？API 类型？），与百炼当前公开的 Assistant API 设计（基于 `messages` + `tools` 的标准 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)）不符；建议以 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中插件调用逻辑和实际 SDK 文档为准，此条信息应视为过时或表述不清。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `stream` | bool | 是否启用[流式输出](../concepts/streaming-output.md)（默认 `False`） |
| `incremental_output` | bool | 是否启用增量式[流式输出](../concepts/streaming-output.md)（仅当 `stream=True` 时生效） |
| `MD5`（上传接口） | string | 文件完整性校验值，必填；上传 PDF 时须确保后缀为小写 `pdf` [常见问题](../../raw/application-user-guide/application-support/application-faq.md) |

## 使用方式

- **插件调用**：在 Assistant API 请求中通过 `tools` 字段声明插件能力，模型将自主决定是否调用及如何填充参数；自定义插件需符合 OpenAI-style function calling 协议。  
- **RAG 应用测试与优化**：若检索结果不准确，可通过回复下方“问题反馈”按钮提交，或复制 `RequestId` 提交阿里云工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **文件上传**：仅支持 `pdf`/`doc`/`docx` 格式；PDF 文件名后缀必须为小写 `pdf`，否则报错 `140010`；结构化数据导入时需避免空行（含首行为空），否则后续数据将被跳过。  
- **备案与合规**：接入通义千问模型并上架应用市场/小程序前，须完成[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)并[提交工单](https://smartservice.console.aliyun.com/service/create-ticket)申请合作协议。

## 限制和注意事项

- **插件 header 限制**：调用自定义插件时，仅允许透传 `Authorization` header；其他 header 将被忽略（服务端实际未透传）[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **数据规模限制**：单业务空间最多上传 10 万个文档；超限时需提交阿里云工单申请扩容。  
- **第三方工具支持边界**：阿里云百炼售后**不支持**第三方工具（如 Cursor、Windsurf 等）的安装、配置、升级、故障诊断及业务代码编写；仅提供方向性建议，例如 API 连通性测试、SDK 示例参考、计费明细核查等 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **法律与协议约束**：使用百炼服务须遵守《阿里云百炼服务协议》《阿里云百炼体验功能特别说明》及开源模型相关条款，详见 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


