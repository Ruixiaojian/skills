# application support

百炼平台的应用支持体系面向开发者提供模型调用、[插件](../concepts/plugin.md)集成、RAG增强、[流式输出](../concepts/streaming-output.md)等核心能力，同时明确划定了服务边界与技术限制。本文档结构化梳理关键能力、参数配置、使用方式及注意事项，帮助开发者快速定位可用能力与支持范围。所有功能均需在阿里云百炼控制台开通对应权限，并遵循[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)约束。

## 支持的模型/功能

- **内置[插件](../concepts/plugin.md)能力**：当前官方支持 6 类[插件](../concepts/plugin.md)：Python代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub搜索。部分插件需申请开通 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置策略打分后选取 topN 结果融合生成；适用于问答系统、对话系统、客户服务等场景 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件/API**：支持通过标准 OpenAPI 协议注册函数，大模型可理解参数结构并自主调用；但**仅支持 `Authorization` header 透传，不支持其他自定义 header** [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：可通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 实现增量式[流式输出](../concepts/streaming-output.md)（即每次返回新片段而非全量重发）。

## 关键参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `stream` | bool | 启用流式响应（SSE），默认 `False` |
| `incremental_output` | bool | 仅在 `stream=True` 时生效，启用增量式[流式输出](../concepts/streaming-output.md)（避免重复渲染） |
| `MD5`（文件上传） | string | 必填，用于校验文件完整性，注意大小写敏感（如 PDF 文件后缀须为小写 `pdf`） |

> **注意**：文档 1 中第 8 条明确 `incremental_output=True` 为增量式流式输出开关，但该参数未在官方 SDK 文档或 OpenAPI 规范中统一定义；实际使用前请以最新版 [原文标题](../../raw/application-user-guide/application-support/application-faq.md) 及控制台调试结果为准。

## 使用方式

- **插件调用**：在智能体（Agent）配置中启用插件，或通过 Assistant API 的 `tools` 字段声明函数 schema；模型将自动规划并调用。  
- **RAG 应用测试**：在应用测试窗中提交问题，若回复不准确，可点击反馈按钮提交问题类型，或**复制 RequestId 提交阿里云工单** [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入需避免空行（首行为空则视为无效文件）。  
- **售后支持接入**：7×24 小时支持渠道包括官网在线客服、电话（95187 / 400）、阿里云 APP 及标准工单；覆盖模型服务咨询、API/SDK 故障诊断、控制台问题等 [原文标题](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **第三方工具免责**：阿里云百炼**不负责第三方工具（如 Cursor、Windsurf 等）的安装、配置、运维或故障排查**；仅提供百炼侧接口连通性建议与调用示例 [原文标题](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **自定义插件限制**：除 `Authorization` 外，不支持透传任意 HTTP header；插件调用失败时需检查服务端鉴权逻辑是否兼容该限制。  
- **数据容量上限**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容。  
- **协议约束**：所有使用须遵守 [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE) 及 [阿里云百炼体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html)，后者对免费体验功能有额外条款约束 [原文标题](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


