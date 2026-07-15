# application [support](support.md)

`application support` 指百炼平台为构建和运行 AI 应用（如智能体、RAG 应用、[插件](../concepts/plugin.md)集成应用等）所提供的核心能力支持体系，涵盖模型调用、[插件](../concepts/plugin.md)扩展、知识检索增强、[流式输出](../concepts/streaming-output.md)等关键功能。开发者可通过 Assistant API 或 Agent 框架接入，需关注参数配置、协议约束及服务边界。所有能力均受 [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE) 约束，具体条款详见 [原文标题](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 支持的模型与功能

- **内置[插件](../concepts/plugin.md)**：当前官方支持 6 类插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索。部分插件需申请开通 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。
- **自定义插件**：支持通过符合 OpenAPI 规范的 HTTP 接口注册；大模型可理解插件描述及参数结构，并据此生成调用逻辑；但**仅支持透传 `Authorization` header**，其他自定义 header 将被忽略（见文档 1 第 10 条）。
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置权重与相似度得分聚合结果后选取 topN 片段；适用于问答、客服、教育等场景 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。
- **[流式输出](../concepts/streaming-output.md)**：支持增量式流式响应，需同时设置 `stream=True` 和 `incremental_output=True`（文档 1 第 8 条）。

> **注意**：文档 1 中“Agent 和 Assistant API 的最大区别”（第 4 条）表述模糊且缺乏技术细节，实际差异应以最新版 [Assistant API 文档](https://help.aliyun.com/zh/model-studio/assistant-api-overview) 为准；该 FAQ 条目已过时，不建议作为架构选型依据。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回） |
| `incremental_output` | bool | 启用增量式流式输出（仅返回新增内容，非全量重传） |
| `knowledge_retrieval` | object | 控制 RAG 行为，含 `top_k`、`score_threshold`、`enable_rerank` 等子字段 |
| `plugins` | list | 指定启用的插件 ID 列表（如 `["python_interpreter", "qrcode_generator"]`） |

## 使用方式

- **调用入口**：统一通过 `/v1/applications/{app_id}/chat` 接口发起请求（RESTful）或使用 SDK 封装的 `assistant.chat()` 方法。
- **插件配置**：在应用控制台中绑定插件，或在 API 请求中显式声明 `plugins` 参数；自定义插件需提前在「插件管理」中完成注册与鉴权配置。
- **RAG 配置**：上传文件至知识库（仅支持小写后缀 `.pdf`, `.doc`, `.docx`；见文档 1 数据管理第 1 条），并在应用中关联知识库 ID；空行会导致结构化数据截断（文档 1 第 4 条）。
- **错误处理**：RAG 结果不准确时，可通过界面反馈按钮提交问题，或复制 `RequestId` 提交工单 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。

## 限制和注意事项

- **文件上传**：单业务空间上限 10 万个文档；超限时需提交工单申请扩容（文档 1 第 2 条）。
- **MD5 校验**：上传接口必填 `Content-MD5` 头，用于验证文件完整性（文档 1 第 3 条）。
- **协议约束**：
  - 自定义插件不收费，但 [prompt](prompt.md) 优化、API 调用及测试窗使用将计费；
  - 所有应用上线前须完成 [应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)，并签署通义千问合作协议（文档 1 应用备案章节）；
  - 开源模型使用须遵守 [开源模型协议条款说明](https://help.aliyun.com/zh/model-studio/open-source-model-terms)（见 [原文标题](../../raw/application-user-guide/application-support/application-related-agreements.md)）。
- **渲染提示**：模型输出中的 `**text**` 为 Markdown 加粗语法，需前端自行解析渲染（文档 1 第 7 条）。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


