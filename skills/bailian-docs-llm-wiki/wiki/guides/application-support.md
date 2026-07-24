# application [support](support.md)

百炼平台的应用支持体系面向开发者提供模型调用、[插件](../concepts/plugin.md)集成、RAG增强、[流式输出](../concepts/streaming-output.md)等核心能力，同时配套完善的售后响应机制与合规指引。本文档汇总了当前稳定支持的功能边界、关键参数配置、标准使用方式及常见限制，便于快速定位技术方案与问题排查路径。所有能力均需在阿里云百炼服务协议约束下使用，具体条款详见 [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)。

## 支持的模型/功能

- **内置[插件](../concepts/plugin.md)**：当前官方支持 6 类[插件](../concepts/plugin.md)：Python代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub搜索；其中部分需申请开通 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过符合协议的 API 插件接入，大模型可理解其参数结构并完成调用；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 增强**：支持多知识库并行检索（按用户配置独立执行），再基于得分聚合选取 topN 结果；已广泛应用于问答系统、客服、教育、内容创作等场景 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming-output.md)**：支持增量式流式响应，需同时设置 `stream=True` 和 `incremental_output=True`（注意：后者非所有 SDK 版本默认启用，建议核对文档）。

## 关键参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回） |
| `incremental_output` | bool | 启用增量式流式输出（仅返回新增内容，非全量重发） |
| `MD5` | string | 文件上传必填，用于校验文件完整性（见 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)） |

> **注意**：`incremental_output=True` 的行为在部分旧版 SDK 中可能未生效，若前端渲染出现重复或错乱，请确认 SDK 版本 ≥ v1.2.0 并参考最新 [API 参考文档](https://help.aliyun.com/zh/model-studio/developer-reference)。

## 使用方式

- **插件调用**：自定义插件需遵循 OpenAPI Schema 协议注册，模型将自动解析参数并生成调用请求；无需手动拼接 URL 或构造 body。  
- **RAG 测试优化**：若检索结果不准确，可通过控制台问题反馈按钮提交，或复制 `RequestId` 提交工单 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **Markdown 渲染**：模型输出中的 `**text**` 等 Markdown 标记需由前端自行解析渲染，平台不提供服务端富文本转换。  
- **备案与合作**：上架应用市场或小程序前，须完成 [应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model) 并提交工单申请通义千问合作协议。

## 限制和注意事项

- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入时，空行将导致后续行被跳过 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **知识库容量**：单业务空间上限为 10 万文档，超限时需提交工单申请扩容。  
- **第三方工具支持边界**：阿里云百炼售后**不负责**第三方工具（如 Cursor、Windsurf、开源代理框架等）的安装、配置、升级或故障排查；仅提供方向性建议，例如连通性测试、SDK 示例、计费核查等 [阿里云百炼平台售后服务范围说明 (raw/application-user-guide/application-support/application-after-sales-service-scope.md)](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **责任划分**：阿里云仅保障百炼服务端（API、控制台、计量计费）的可用性与正确性；用户本地环境（代理、防火墙、内网策略）、业务代码逻辑、第三方服务异常等问题不在标准支持范围内。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


