# application [support](support.md)

`application support` 指百炼平台为开发者构建和运行 AI 应用所提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、API 调用规范及售后响应机制等核心环节。其目标是保障应用在模型调用、知识融合、外部服务协同及生产环境稳定性等方面的可预期行为。所有能力均需遵循[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)约束。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索。部分插件需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索，按配置策略（如相似度得分）选取 topN 结果后融合生成，适用于问答、客服、教育等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过符合协议的 API 接入，大模型可理解参数结构并调用；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming-output.md)**：支持增量式流式响应，需同时设置 `stream=True` 和 `incremental_output=True`。  

> **注意**：文档中提及“Agent 和 Assistant API 的最大区别是用户可自行开发插件模型”，但该描述未明确对应具体 API 接口或能力边界，与当前公开 SDK 文档存在表述差异；实际开发应以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中定义的 API 支持范围为准。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回） | 否 |
| `incremental_output` | bool | 启用增量式流式输出（仅返回新增内容） | 否，但需与 `stream=True` 共同使用 |
| `MD5` | string | 文件上传时用于校验完整性的哈希值 | 是（结构化数据/文件导入必填） |

## 使用方式

- 插件调用：通过 `Assistant API` 或 `Agent` 框架声明插件 schema，由大模型自动编排执行；自定义插件需提供 OpenAPI v3 格式描述。  
- RAG 应用调试：若检索结果不准确，可通过界面反馈按钮提交问题，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- 文件上传：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；空行会导致后续数据被截断 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- 备案与合规：接入通义千问模型的应用上架前，须完成[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)并申请合作协议。

## 限制和注意事项

- **插件限制**：自定义插件不支持除 `Authorization` 外的任何请求头透传；非官方插件的稳定性、安全性及计费归属由用户自行承担。  
- **数据规模**：单业务空间最多支持 10 万个文档，超限时需提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **第三方工具支持边界**：阿里云仅对百炼服务端状态、API 可用性、SDK 调用及计费明细提供支持；第三方工具（如 Cursor、Windsurf 等）的部署、配置、故障排查不在售后范围内 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **责任划分**：阿里云不对外部第三方工具的陈述、行为或故障承担责任；所有非百炼平台原生能力引发的问题（如本地网络、代理、权限、业务代码逻辑），需用户或相应服务方独立解决。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


