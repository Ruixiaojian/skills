# application support

`application support` 指百炼平台为开发者在构建和运行 AI 应用（如智能体、RAG 应用、插件集成等）过程中提供的功能能力、调用接口、参数配置及配套服务支持。它涵盖模型与插件能力接入、流式/增量输出控制、知识库检索机制、API 使用规范，以及售后响应边界等核心维度。开发者需结合具体场景选择合适的能力组合，并注意平台对第三方依赖的职责划分。

## 支持的模型/功能

- **内置插件能力**：当前官方支持六类插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索。部分插件需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **RAG（知识检索增强）**：支持多知识库并行检索，按用户配置的权重与相关性得分选取 topN 片段后送入大模型生成答案；适用于问答系统、客服、教育、内容创作等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **自定义插件/API 函数**：支持通过协议声明函数签名，模型可理解参数语义并生成调用请求；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中提及“Agent 和 Assistant API 的最大区别是……用户可以自己去开发”，该描述模糊且未明确定义二者技术边界；实际开发中应以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中明确的服务边界为准——即平台仅保障自身 API 与控制台行为，不承担第三方工具或自建 Agent 框架的实现责任。

## 关键参数

- `stream=True`：启用[流式输出](../concepts/streaming-output.md)，逐 token 返回响应。
- `incremental_output=True`：启用增量式[流式输出](../concepts/streaming-output.md)（即每次返回新增内容，非全量重传）。
- 文件上传必需 `MD5` 参数：用于校验文件完整性。
- RAG 检索结果数量由 `top_k` 控制（文档未显式命名该参数，但逻辑对应“选取 topN”），具体值需在知识库配置中设定。

## 使用方式

- 插件调用：通过[函数调用](../concepts/function-calling.md)（Function Calling）协议声明插件能力，模型自动解析参数并生成结构化调用请求。
- RAG 应用调试：若模型回复不准确，可通过界面反馈按钮提交问题，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- Markdown 渲染：模型输出中的 `**text**` 等标记需由前端自行解析渲染，平台不提供自动富文本转换。
- 备案与合作：接入通义千问模型并上架应用市场/小程序前，须完成[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)并申请合作协议。

## 限制和注意事项

- **文件上传限制**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入时，空行将导致后续行被截断 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **容量限制**：单业务空间最多上传 10 万个文档，超限时需提交工单申请扩容。
- **第三方工具支持边界**：阿里云百炼仅提供 API 可用性验证、官方 SDK 问题诊断、基础连通性建议；**不支持**第三方工具（如 Cursor、Windsurf 等）的安装、配置、升级、故障排查及业务代码编写指导 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。
- **法律与协议约束**：使用前须遵守《阿里云百炼服务协议》《阿里云百炼体验功能特别说明》及开源模型相关条款 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


