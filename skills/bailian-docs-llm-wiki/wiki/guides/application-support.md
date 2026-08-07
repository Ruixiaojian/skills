# application support

`application support` 指百炼平台为开发者在构建和运维 AI 应用过程中提供的技术能力支撑与服务保障，涵盖插件集成、RAG 检索、[流式输出](../concepts/streaming-output.md)、API 调用规范及售后支持边界等核心环节。其目标是确保应用功能可扩展、调用可预测、问题可定位、服务有兜底。所有能力均需遵循 [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE) 约束。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索。部分插件需申请开通；自定义插件支持通过 `Assistant API` 接入，模型可理解函数签名并参与推理决策 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **RAG 检索增强**：支持多知识库并行检索（按用户配置独立执行），再基于相关性得分聚合选取 topN 片段用于生成；适用于问答、客服、教育等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **[流式输出](../concepts/streaming-output.md)**：支持两种模式：
  - `stream=True`：标准流式响应（逐 token 返回）；
  - `incremental_output=True`：增量式[流式输出](../concepts/streaming-output.md)（仅返回本次新增内容，非全量重传）。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | bool | 启用流式响应 | 否（默认 `False`） |
| `incremental_output` | bool | 启用增量式流式输出（需 `stream=True` 时生效） | 否（默认 `False`） |
| `authorization` | string | 自定义插件调用时唯一允许透传的 Header 字段；其他 Header（如 `X-Custom-Token`）将被忽略 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) | 否（仅插件调用时需按需设置） |

> **注意**：文档 1 中提及 `incremental_output=True` 可实现“增量回复”，但未明确其依赖 `stream=True` 的前提；实际调用中若未启用 `stream`，该参数无效。请务必组合使用。

## 使用方式

- 插件调用：通过 `Assistant API` 提交包含工具描述（OpenAI-style function calling schema）的请求，模型自动选择并填充参数；自定义插件 URL 需在控制台配置，且仅支持 `authorization` header 透传。
- RAG 应用调试：若检索结果不准确，可通过界面“问题反馈”按钮提交或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- 文件上传：PDF 文件后缀必须为小写 `pdf`；结构化数据导入需避免空行（首行为空即视为无效文件）。

## 限制和注意事项

- **插件限制**：不支持自定义 HTTP Header 透传（除 `Authorization` 外）；自定义插件的 [prompt](prompt.md) 优化、API 调用及测试窗测试会产生计费。
- **数据管理限制**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容。
- **售后支持边界**：
  - ✅ 覆盖：API/SDK 故障诊断、控制台操作、计费核查、连通性基础测试（如 `curl` 测试服务地址）；
  - ❌ 不覆盖：第三方工具（如 Cursor、Windsurf）部署配置、用户本地网络/代理/防火墙问题、业务代码编写与调试、非百炼侧服务（如外部数据库、认证系统）的故障排查 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。
- **合规要求**：接入通义千问模型的应用上架前，须完成[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)并申请合作协议。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


