# application [support](support.md)

`application support` 指百炼平台为开发者在构建和运行 AI 应用过程中提供的能力支撑与服务保障，涵盖插件集成、RAG 增强、[流式输出](../concepts/streaming-output.md)等核心功能，以及售后响应、协议约束与使用边界。该支持体系面向生产环境，强调可配置性、可观测性和责任边界划分。开发者需结合具体场景选择合适的能力组合，并严格遵循平台限制。

## 支持的模型/功能

- **内置插件**：当前官方支持六类插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索。部分插件需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过 API 接入自定义函数，大模型可理解其参数结构并参与推理调度；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持多知识库并行检索，按得分聚合后选取 topN 结果用于生成；广泛应用于问答系统、客服对话、教育辅助等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming-output.md)**：支持两种模式：`stream=True`（全量流式）、`incremental_output=True`（增量式流式），适用于前端实时渲染场景。

> **注意**：文档 1 中“Agent 和 Assistant API 的最大区别”描述模糊且缺乏技术细节（如调用协议、状态管理差异），未明确区分二者在插件编排、上下文维护或重试机制上的实际差异，建议以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中定义的服务边界为准，避免依赖该条目做架构选型。

## 关键参数

| 参数名 | 类型 | 说明 | 来源 |
|--------|------|------|------|
| `stream` | bool | 启用流式响应（逐 token 返回） | [常见问题](../../raw/application-user-guide/application-support/application-faq.md) |
| `incremental_output` | bool | 启用增量式[流式输出](../concepts/streaming-output.md)（仅返回新增内容） | [常见问题](../../raw/application-user-guide/application-support/application-faq.md) |
| `MD5` | string | 文件上传必填，用于校验文件完整性 | [常见问题](../../raw/application-user-guide/application-support/application-faq.md) |

## 使用方式

- 插件调用：通过 `tools` 字段声明插件列表，模型自动选择并填充参数；自定义插件需符合 OpenAI-style function calling 协议。  
- RAG 配置：在应用设置中绑定知识库，支持按权重调整各库检索优先级；测试阶段若结果不准，可通过回复下方反馈按钮提交问题，或复制 `RequestId` 提交工单。  
- 文件上传：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入时需确保无空行，否则后续行将被忽略。  
- 增量渲染：前端需解析模型返回的 Markdown 格式（如 `**text**` 表示加粗），自行实现渲染逻辑。

## 限制和注意事项

- **插件限制**：自定义插件不支持除 `Authorization` 外的任何 HTTP Header 透传；非官方插件的稳定性、安全性及计费由用户自行负责。  
- **数据规模**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容。  
- **服务边界**：阿里云百炼售后仅覆盖平台自身服务（API、控制台、计费系统等），**不提供第三方工具（如 Cursor、Windsurf）的部署、调试或兼容性支持**，也不承担其行为导致的问题 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：使用前须阅读并接受《阿里云百炼服务协议》及《开源模型协议条款说明》等法律文件 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。  
- **备案要求**：若应用拟上架至应用市场或小程序平台，须完成[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)，并单独申请通义千问合作协议。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


