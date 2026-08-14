# application support

`application support` 指百炼平台为开发者构建和运行 AI 应用所提供的技术支撑能力，涵盖[插件](../concepts/plugin.md)集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、API 调用规范及售后支持边界等核心环节。该支持体系面向生产环境设计，强调可配置性、可观测性和责任边界清晰性。所有能力均需在阿里云百炼服务协议约束下使用，具体条款详见 [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)。

## 支持的模型/功能

- **[插件](../concepts/plugin.md)能力**：官方提供六类内置[插件](../concepts/plugin.md)：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索。部分插件需申请开通；自定义插件支持函数参数透传，但仅限 `authorization` header，不支持其他自定义 header [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。
- **RAG 检索增强**：支持多知识库并行检索，按用户配置的权重与得分选取 topN 结果，适用于问答系统、客户服务、教育等场景 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。
- **[流式输出](../concepts/streaming-output.md)**：支持增量式流式响应，需显式设置 `stream=True` 和 `incremental_output=True` 参数。
- **数据管理**：支持 PDF/DOC/DOCX 格式文件上传（注意 `.pdf` 后缀必须小写），单业务空间上限 10 万文档，超限时需提交工单扩容 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（默认 `False`） |
| `incremental_output` | bool | 启用增量式流式输出（仅当 `stream=True` 时生效） |
| `MD5` | string | 文件上传必填，用于校验文件完整性 |
| `authorization` | string | 唯一支持透传的 HTTP Header，用于身份认证 |

> **注意**：文档中提及“自定义插件服务目前暂时不收费”，但该表述未明确适用范围（如是否含调用计费）。实际计费以控制台实时报价及 [阿里云百炼体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html) 为准 [原文标题](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 使用方式

- 插件调用：通过 Assistant API 或 Agent 框架声明插件 schema，模型自动解析参数并调度执行；
- RAG 应用：在应用配置中绑定知识库，系统自动完成分块、向量化与混合检索；
- 流式响应：在请求 payload 中设置 `stream` 和 `incremental_output`，前端需按 chunk 解析并渲染；
- 文件上传：确保文件后缀为小写（如 `report.pdf`），避免空行导致结构化数据截断；
- 问题反馈：RAG 输出不准确时，可通过界面反馈按钮提交或复制 `RequestId` 提交工单 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。

## 限制和注意事项

- **Header 限制**：自定义插件调用时，仅 `Authorization` 可透传，其他 header（如 `X-User-ID`、`Cookie`）将被丢弃；
- **文件格式与结构**：PDF 必须为小写后缀；Excel/CSV 导入时首行为空则视为无效文件；
- **第三方工具支持边界**：阿里云百炼仅保障自身 API 可用性与计费准确性，不支持 Cursor、Windsurf 等第三方工具的部署、配置或故障排查 [原文标题](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)；
- **服务责任范围**：售后支持覆盖模型服务、API、SDK、控制台及账号/计费问题；业务代码编写、本地网络环境（代理/防火墙）、非标集成等问题不在基础支持范围内 [原文标题](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


