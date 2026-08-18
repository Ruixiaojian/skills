# application support

阿里云百炼平台的应用支持体系面向开发者提供覆盖模型调用、插件集成、RAG 应用构建及问题排查的全链路技术保障。支持范围以百炼平台自身服务（API、SDK、控制台、计量计费系统）为核心，不延伸至用户侧环境或第三方工具的运维。所有服务均以《[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)》为基准，开发者应优先确认问题是否属于平台责任边界。

## 支持的模型/功能

- **内置插件能力**：官方支持 Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索共六类插件；部分需申请开通 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。
- **自定义插件**：支持通过符合 OpenAPI 规范的 HTTP 接口注册插件，模型可理解参数结构并完成调用；但**不支持透传除 `Authorization` 外的任意自定义 Header** [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。
- **RAG（知识检索增强）**：支持多知识库并行检索、按得分聚合 topN 结果，适用于问答、客服、教育等场景；检索结果准确性优化可通过工单提交 `RequestId` 反馈 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。
- **[流式输出](../concepts/streaming-output.md)控制**：支持增量式流式响应，需同时设置 `stream=True` 和 `incremental_output=True` 参数。

> **注意**：文档 2 中“Agent 和 Assistant API 的最大区别”条目表述模糊（“调整插件模型、基于上下文的理解，用户可以自己去开发”），未明确技术边界，且与百炼当前统一的 `Assistant API` 设计不符；实际开发中应以控制台和 SDK 文档为准，该条目存在过时风险。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回） | 否（默认 `False`） |
| `incremental_output` | bool | 启用增量式[流式输出](../concepts/streaming-output.md)（仅返回新增内容，非全量重传） | 否（仅当 `stream=True` 时生效） |
| `file_md5` | string | 文件上传时必填，用于校验文件完整性 | 是（见 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)） |
| `Authorization` | string | 插件调用时唯一支持透传的 Header 字段 | 是（若插件要求鉴权） |

## 使用方式

- **问题反馈**：RAG 测试中模型回复不准确时，优先点击回复下方「问题反馈」按钮；或复制 `RequestId` 提交工单 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。
- **文件上传**：PDF 文件后缀必须为小写 `pdf`；结构化数据导入需避免空行（首行为空则视为无效文件） [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。
- **备案与协议**：应用上架前须完成合规备案，并申请通义千问合作协议；相关法律条款详见《[阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md)》及《阿里云百炼体验功能特别说明》。

## 限制和注意事项

- **第三方工具免责**：百炼仅对自身服务端状态、API 可用性、SDK 示例、调用明细及基础连通性（如 `curl` 测试）提供方向性建议；**不支持**第三方工具（如 Cursor、Windsurf 等）的安装、配置、升级、故障诊断或业务代码调试 [原文标题](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。
- **环境问题归属**：本地网络（代理/VPN/防火墙）、操作系统兼容性、账号权限配置、非标集成导致的问题，不属于百炼直接支持范围，需用户自行排查或联系对应服务方。
- **计费差异说明**：第三方工具界面显示的 Token 数量、费用预估值与阿里云实际计费数据可能存在差异，百炼不对此类差异提供解释 [原文标题](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。
- **责任边界声明**：第三方工具不构成阿里云代理或联合服务主体，其任何陈述、承诺或行为均由其自身承担法律责任 [原文标题](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 来源文档

- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


