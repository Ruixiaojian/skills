# application support

`application support` 指百炼平台为开发者在构建和运行 AI 应用（含智能体、RAG 应用、插件集成等）过程中提供的功能能力、调用接口、参数配置及配套服务支持。它覆盖模型能力接入、插件扩展、[流式输出](../concepts/streaming-output.md)控制、知识库检索增强等核心场景，同时明确服务边界与售后响应范围。开发者需结合具体文档理解能力限制与责任划分。

## 支持的模型/功能

- **内置插件能力**：当前官方支持六类插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索。部分插件需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **RAG 检索增强**：支持多知识库并行检索，按用户配置的权重与相关性得分选取 topN 结果，适用于问答系统、客户服务、教育等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **自定义插件/API 集成**：支持通过协议注册自定义函数或 API，大模型可理解其参数结构并生成调用逻辑；但**仅支持 `Authorization` header 透传，不支持其他自定义 header** [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **流式与增量输出**：可通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 实现增量式[流式输出](../concepts/streaming-output.md)（即每次返回新增 token，而非全量重发）。

> **注意**：文档中提及“Agent 和 Assistant API 的最大区别是‘调整插件模型、基于上下文的理解，用户可以自己去开发’”，但该描述模糊且未定义术语边界。实际开发中应以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中明确的服务范围为准——即百炼仅保障自身 API、SDK 及控制台功能，不承担第三方工具或自建 Agent 架构的实现责任。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回） | 否（默认 `False`） |
| `incremental_output` | bool | 在 `stream=True` 基础上启用增量模式（避免重复返回历史内容） | 否（默认 `False`） |
| `MD5` | string | 文件上传时必填，用于校验文件完整性 | 是（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)） |

## 使用方式

- 插件调用：通过应用配置界面启用内置插件，或在智能体编排中注册自定义 API；模型将自动解析函数描述并生成符合协议的调用请求。
- RAG 应用测试：在测试窗中验证检索效果；若结果不准确，可点击回复下方的“问题反馈”按钮提交，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- 文件上传：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入需避免空行，否则后续行将被忽略。
- 备案与合作：接入通义千问模型并上架应用市场前，须完成[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)，并[提交工单](https://smartservice.console.aliyun.com/service/create-ticket)申请合作协议。

## 限制和注意事项

- **插件限制**：自定义插件本身免费，但涉及 [prompt](prompt.md) 优化、应用调用测试等操作将产生计费；插件调用不支持除 `Authorization` 外的任何 HTTP header。
- **数据规模限制**：单个业务空间最多上传 10 万个文档；超限时需提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **服务边界**：阿里云百炼售后仅覆盖自身服务（API、SDK、控制台、计费系统），**不提供**以下支持：
  - 第三方工具（如 Cursor、Windsurf）的安装、配置或故障排查；
  - 用户本地环境（代理、防火墙、内网策略）导致的连通性问题；
  - 业务代码编写、调试或定制化集成方案（此类需求需联系商务经理订购增值服务）[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。
- **协议约束**：使用前须遵守《阿里云百炼服务协议》及《阿里云百炼体验功能特别说明》，开源模型还需遵循对应[开源模型协议条款说明](https://help.aliyun.com/zh/model-studio/open-source-model-terms)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


