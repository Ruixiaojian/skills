# application support

`application support` 指百炼平台为开发者在构建和运行 AI 应用（含智能体、RAG 应用、插件集成等）过程中提供的技术能力支持、服务边界说明及使用约束。它涵盖模型与功能支持范围、关键参数配置、调用方式、以及明确的服务限制。开发者需结合具体场景，在平台能力边界内进行集成与优化。

## 支持的模型/功能

百炼平台当前支持以下核心应用能力：
- **插件能力**：官方提供六款内置插件，包括 Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分插件需申请开通 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。
- **RAG（知识检索增强）**：支持多知识库并行检索，并按得分选取 topN 结果，适用于问答系统、客服、教育、内容创作等场景 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。
- **自定义插件/API**：支持通过协议注册自定义函数或 API，大模型可理解其参数结构并参与推理调度；但**仅支持 `Authorization` header 透传，不支持其他自定义 header** [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档中提及“Agent 和 Assistant API 的最大区别是用户可自行开发插件模型”，但该表述模糊且未定义术语边界；实际开发中应以 [阿里云百炼平台售后服务范围说明 (raw/application-user-guide/application-support/application-after-sales-service-scope.md)](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中明确的服务范围为准——即平台仅保障自身 API、SDK、控制台及计费系统的可用性与基础咨询，不承担第三方工具或用户侧业务逻辑的实现责任。

## 关键参数

- `stream=True`：启用[流式输出](../concepts/streaming-output.md)，适用于前端实时渲染。
- `incremental_output=True`：启用增量式[流式输出](../concepts/streaming-output.md)（非全量重传），需配合前端正确处理 token 流。
- 文件上传必需 `MD5` 参数：用于校验文件完整性，避免传输损坏。
- 知识库检索配置：支持按权重、相似度阈值等参数调整 RAG 行为，但底层并行检索逻辑不可更改。

## 使用方式

- 插件调用：通过 `tools` 字段声明插件 schema，由模型自主决策是否调用及传参；自定义插件需严格遵循 OpenAI-style function calling 协议。
- RAG 应用调试：若检索结果不准确，可通过模型回复下方的「问题反馈」按钮提交，或复制 `RequestId` 提交工单 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。
- 增量渲染：AI 输出中的 `**text**` 等 Markdown 格式需由前端解析渲染，平台不直接返回 HTML。
- 备案与合规：接入通义千问模型的应用上架前，须完成[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)，并申请合作协议。

## 限制和注意事项

- **文件限制**：上传仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入时，空行将导致后续行被截断。
- **容量限制**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容。
- **服务边界**：
  - 阿里云百炼售后**不覆盖**第三方工具（如 Cursor、Windsurf 等）的部署、配置、故障排查；
  - 不提供用户本地环境（代理、防火墙、内网策略等）导致的问题诊断；
  - 不承担业务代码编写、调试或定制化集成方案设计 [阿里云百炼平台售后服务范围说明 (raw/application-user-guide/application-support/application-after-sales-service-scope.md)](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。
- **协议约束**：所有使用须遵守《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)》及《[阿里云百炼体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html)》[相关协议 (raw/application-user-guide/application-support/application-related-agreements.md)](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


