# application support

`application support` 指百炼平台为开发者构建和运行 AI 应用所提供的全链路支撑能力，涵盖模型调用、[插件](../concepts/plugin.md)集成、RAG 增强、[流式输出](../concepts/streaming-output.md)、API 配置及售后响应等核心环节。其目标是保障应用在开发、测试、上线与运维各阶段的稳定性与可调试性。所有能力均需结合具体 API 参数与服务协议使用，部分功能存在权限或配额限制。

## 支持的模型/功能

- **内置[插件](../concepts/plugin.md)能力**：当前官方支持 6 类[插件](../concepts/plugin.md)：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索，按配置策略（如相似度得分）选取 topN 结果后融合生成；广泛应用于问答系统、客服对话、教育辅助等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 可实现增量式[流式输出](../concepts/streaming-output.md)（即每次返回新增 token，而非全量重传）[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持基于 OpenAPI 规范注册的[函数调用](../concepts/function-calling.md)，大模型可理解参数结构并自主编排调用逻辑；但**不支持透传自定义 HTTP Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中第 4 条称 “Assistant API 可提供各种类，方便调优”，但未明确类名、接口契约或 SDK 版本要求；而文档 3 未提及任何 API 抽象类设计。该描述缺乏可操作依据，建议以最新版 [阿里云百炼 SDK 文档](https://help.aliyun.com/zh/model-studio/developer-reference/sdk-reference) 为准，避免依赖模糊表述。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `stream` | bool | 必须设为 `True` 才启用流式响应（默认 `False`） |
| `incremental_output` | bool | 仅当 `stream=True` 时生效；设为 `True` 启用增量式 token 流（避免重复渲染） |
| `MD5`（文件上传） | string | 文件完整性校验值，必填；上传 PDF 时须确保后缀为小写 `pdf` |
| `authorization`（插件调用） | string | 插件请求中唯一允许透传的 Header 字段；其他 Header 将被丢弃 |

## 使用方式

- **插件调用**：在 Assistant API 请求中声明 `tools` 列表，包含插件 ID 与 OpenAPI Schema；模型自动选择并填充参数后触发调用。  
- **RAG 应用调试**：若检索结果不准确，可通过控制台问题反馈按钮提交（需勾选类型），或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **文件上传**：仅支持 `.pdf` / `.doc` / `.docx`（注意 `.pdf` 必须小写）；单业务空间上限 10 万文档，超限时需提交工单申请扩容。  
- **合规备案**：上架应用市场或小程序前，须完成 [应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model) 并申请通义千问合作协议。

## 限制和注意事项

- **第三方工具支持边界明确**：阿里云百炼售后**不负责**第三方工具（如 Cursor、Windsurf 等）的安装、配置、升级或故障排查；仅提供百炼侧接口可用性确认、SDK 示例、计费核查及基础连通性建议 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **Header 透传限制**：自定义插件调用时，除 `Authorization` 外的所有 HTTP Header 均被过滤，不可用于身份透传或上下文携带。  
- **结构化数据导入陷阱**：Excel/CSV 导入时，空行将导致后续数据被跳过；首行为空则整份文件被判定为空 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **协议约束**：所有服务受《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)》及《[阿里云百炼体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html)》约束 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


