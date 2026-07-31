# application support

application support 是阿里云百炼平台为开发者提供的应用层能力支撑体系，涵盖模型集成、插件扩展、RAG增强、API调用及售后保障等核心环节。它面向构建智能体（Agent）、知识库应用和自定义业务逻辑的开发者，提供功能接口、参数配置规范与服务边界说明。所有能力均需遵守[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)及相关法律条款。

## 支持的模型/功能

- **插件能力**：官方预置六类插件——Python代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub搜索；其中部分需申请开通 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置策略打分后选取 topN 结果，适用于问答系统、客服、教育等场景 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件/API**：支持通过 OpenAPI 协议注册函数，模型可理解参数结构并生成调用指令；但**仅支持 `Authorization` header 透传，不支持其他自定义 header** [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming-output.md)控制**：支持增量式流式响应，需同时设置 `stream=True` 和 `incremental_output=True`。  

> **注意**：文档2中“Agent 和 Assistant API 的最大区别”描述模糊且缺乏技术定义（如未明确 Agent 是否指百炼平台内置 Agent 框架，或泛指用户自建逻辑），该条目未在其他文档中交叉验证，建议以[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)中定义的服务边界为准，避免对能力归属产生误判。

## 关键参数

| 参数名 | 类型 | 说明 | 必填 |
|--------|------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回） | 否 |
| `incremental_output` | bool | 启用增量式[流式输出](../concepts/streaming-output.md)（仅返回新增内容） | 否，但与 `stream=True` 配合使用才生效 |
| `MD5` | string | 文件上传时用于校验完整性的哈希值 | 是（见[原文标题](../../raw/application-user-guide/application-support/application-faq.md)） |

## 使用方式

- **插件调用**：在智能体配置中启用对应插件，自定义插件需按 OpenAPI v3 规范提供 `spec` 描述；模型将基于描述自动构造调用请求。  
- **RAG 应用调试**：若检索结果不准确，可通过回复下方“问题反馈”按钮提交，或复制 `RequestId` 提交工单 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；空行会导致后续数据被截断 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **备案与合规**：上架应用市场或小程序前，须完成[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)，并申请通义千问合作协议 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。  

## 限制和注意事项

- **服务边界**：阿里云百炼售后支持限于平台自身服务（API、控制台、计费、SDK），**不覆盖第三方工具（如 Cursor、Windsurf 等）的部署、配置或故障排查**，详见[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **数据规模**：单业务空间最多上传 10 万份文档；超限时需提交工单申请扩容。  
- **协议约束**：使用开源模型需遵守对应[开源模型协议条款说明](https://help.aliyun.com/zh/model-studio/open-source-model-terms)，商用场景须额外确认授权范围。  
- **Header 限制**：自定义插件调用时，仅 `Authorization` 可透传至目标服务端，其他 header 将被丢弃 —— 此为硬性限制，非配置问题 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。

## 来源文档

- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


