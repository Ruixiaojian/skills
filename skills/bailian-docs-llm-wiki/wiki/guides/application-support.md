# application support

`application support` 指百炼平台为开发者在构建和运行 AI 应用（含智能体、RAG 应用、插件集成等）过程中提供的功能能力、调用接口、参数配置及配套支持服务。它覆盖模型能力调用、插件扩展、知识检索增强、[流式输出](../concepts/streaming-output.md)控制等核心开发场景，并通过工单、文档与基础技术支持提供问题响应通道。开发者需关注平台能力边界与第三方集成限制，以确保应用稳定性和合规性。

## 支持的模型/功能

- **插件能力**：官方支持六类内置插件：Python代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub搜索；其中部分需申请开通 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置得分选取 topN 结果后融合生成，适用于问答系统、客户服务、教育等场景 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming-output.md)**：支持 `stream=True` 全量[流式输出](../concepts/streaming-output.md)；如需增量式（即仅返回本次新增 token），需显式设置 `incremental_output=True` [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过协议注册 API 插件，大模型可理解其参数结构并调用；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中“Agent 和 Assistant API 的最大区别”描述模糊且缺乏技术定义（如未说明 Agent 是否指百炼智能体 SDK 或特定 runtime），与当前平台公开文档中对 `Assistant API`（即 `/v1/assistant/chat/completions` 接口）的定位存在不一致，建议以 [阿里云百炼 API 文档](https://help.aliyun.com/zh/model-studio/developer-reference/assistant-api) 为准，避免依赖该条目做架构设计。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `stream` | bool | 启用流式输出（true/false），默认 false |
| `incremental_output` | bool | 仅当 `stream=True` 时生效，启用增量式 token 返回（true/false），默认 false |
| `tool_choice` | string / object | 控制插件调用策略（如 `"auto"`、`{"type": "function", "function": {"name": "xxx"}}`） |
| `knowledge_config` | object | RAG 相关配置，含知识库 ID 列表、top_k、rerank 等字段（详见 API 文档） |

## 使用方式

- **调用入口**：通过百炼控制台「应用中心」创建应用，或直接调用 `Assistant API`（HTTP POST `/v1/assistant/chat/completions`）。  
- **插件集成**：内置插件开箱即用；自定义插件需在控制台完成注册、Schema 配置与授权，并确保 endpoint 可被百炼服务端访问。  
- **RAG 配置**：在应用编辑页绑定知识库，设置检索权重与重排策略；测试阶段可通过「问题反馈」按钮提交不准确回复，或复制 `RequestId` 提交工单 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **技术支持**：7×24 小时提供电话（95187）、智能在线与标准工单支持，覆盖 API 调用、SDK 问题、控制台操作等 [阿里云百炼平台售后服务范围说明 (raw/application-user-guide/application-support/application-after-sales-service-scope.md)](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入时，空行将导致后续行被跳过 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **知识库容量**：单业务空间上限 10 万文档，超限需提交工单申请扩容 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **第三方集成责任边界**：阿里云百炼仅保障自身服务端可用性与 API 正确性；对第三方工具（如 Cursor、Windsurf）的部署、配置、兼容性及本地网络环境问题不提供支持 [阿里云百炼平台售后服务范围说明 (raw/application-user-guide/application-support/application-after-sales-service-scope.md)](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：所有使用须遵守《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)》及《[阿里云百炼体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html)》 [相关协议 (raw/application-user-guide/application-support/application-related-agreements.md)](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


