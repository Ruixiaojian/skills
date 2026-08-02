# application support

application support 指百炼平台为开发者提供的应用层能力支撑体系，涵盖插件集成、RAG增强、API调用控制、[流式输出](../concepts/streaming-output.md)等核心功能，同时明确服务边界与售后支持范围。该支持体系面向构建智能体（Agent）和调用 Assistant API 的开发者，需结合具体模型能力与协议约束使用。所有功能均以百炼平台服务端能力为准，第三方工具集成不在标准支持范围内。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件——Python代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub搜索；部分插件需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持多[知识库](../concepts/knowledge-base.md)并行检索，按配置得分选取 topN 结果后融合生成，适用于问答、客服、教育等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 可实现增量式[流式输出](../concepts/streaming-output.md)（即每次返回新增内容，非全量重传） [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持基于 OpenAPI 规范注册的自定义函数，大模型可理解参数结构并调用；但**仅支持透传 `Authorization` header，不支持其他自定义 header**（如 `X-API-Key` 等），该限制已在实际调用中验证 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中第4条称“Assistant API 可以提供各种类，方便调优”，但未明确定义“类”指代对象类型或 SDK 接口抽象；当前百炼 Python SDK 中 `Assistant` 为客户端类，而 `Agent` 为服务端运行时概念，二者并非同层级可比对象。建议以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中定义的服务边界为准，避免混淆模型能力与 SDK 封装层级。

## 关键参数

| 参数 | 类型 | 说明 | 是否必需 |
|------|------|------|----------|
| `stream` | bool | 启用流式响应（逐 token 返回） | 否，默认 `False` |
| `incremental_output` | bool | 在 `stream=True` 基础上启用增量模式（仅返回新 token，非累积） | 否，默认 `False` |
| `knowledge_config` | dict | RAG 配置，含 `knowledge_base_ids`、`top_k`、`score_threshold` 等 | 否（启用 RAG 时必需） |
| `tools` | list | 指定可用插件列表（ID 或配置对象） | 否（调用插件时必需） |

> **注意**：`incremental_output=True` 仅在 `stream=True` 为 `True` 时生效；单独设置 `incremental_output=True` 无效果。

## 使用方式

- 插件调用需在请求中显式声明 `tools`，并确保对应插件已开通权限；自定义插件需完成注册并通过审核。  
- RAG 应用需提前创建并配置[知识库](../concepts/knowledge-base.md)，测试阶段若结果不准，可通过界面反馈按钮提交问题，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- 文件上传接口要求 `MD5` 参数用于校验文件完整性；PDF 文件后缀必须为小写 `pdf`，否则触发错误码 `140010` [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- 所有 API 调用须遵守 [阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md) 及 [体验功能特别说明](../../raw/application-user-guide/application-support/application-related-agreements.md)，尤其注意免费额度与商用授权条款。

## 限制和注意事项

- **第三方工具支持边界**：阿里云百炼仅保障自身服务端（API、SDK、控制台）可用性与计费准确性；对 Cursor、Windsurf 等第三方工具的安装、配置、本地环境（代理/防火墙/内网）、业务代码调试等问题**不提供支持** [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **[知识库](../concepts/knowledge-base.md)容量限制**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **结构化数据导入容错**：表格中存在空行将导致后续数据被跳过（含首行为空则视为无效文件），需预处理清理 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **备案与合规**：接入通义千问模型并上架应用市场/小程序前，须完成[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)并申请合作协议 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


