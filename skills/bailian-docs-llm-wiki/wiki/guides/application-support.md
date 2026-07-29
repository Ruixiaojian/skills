# application support

`application support` 指百炼平台为开发者在构建和运行 AI 应用（如智能体、RAG 应用、插件集成等）过程中提供的功能能力、调用接口、参数配置及配套服务支持。它涵盖模型与插件能力接入、API 行为控制、知识库检索机制、[流式输出](../concepts/streaming-output.md)设置，以及售后响应边界等关键维度。开发者需结合具体场景选择合适的能力组合，并注意平台对第三方依赖的职责划分。

## 支持的模型/功能

- **内置插件能力**：当前官方支持六类插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索。部分插件需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **自定义插件**：支持通过符合协议的 API 接入自定义函数，大模型可理解其参数结构并生成调用逻辑；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **RAG（知识检索增强）**：支持多知识库并行检索，按用户配置的权重与得分选取 topN 结果后融合生成，适用于问答、客服、教育等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中第 4 条称 “Agent 和 Assistant API 的最大区别是……用户可以自己去开发”，但未明确定义二者技术边界；而实际开发中，Assistant API 是百炼封装的标准化应用调用接口，Agent 则指基于插件编排与工具调用的自主推理流程。该描述易引发歧义，建议以控制台实际能力为准，避免将 Assistant API 等同于可任意开发的 Agent 框架。

## 关键参数

- `stream=True`：启用[流式输出](../concepts/streaming-output.md)，返回分块响应；
- `incremental_output=True`：启用增量式[流式输出](../concepts/streaming-output.md)（即每次返回新增内容，非全量重传）；
- 文件上传必需 `MD5` 参数：用于校验文件完整性；
- RAG 检索结果数量由 `top_k` 控制（虽未在原始文档显式列出，但属通用实践，且与文档 1 第 9 条“选取 topN”一致）。

## 使用方式

- 插件调用：通过 Assistant API 提交包含工具描述（function definition）的请求，模型自动决定是否调用及如何填充参数；
- RAG 应用测试：可在控制台测试窗验证效果，若回复不准确，可通过问题反馈按钮提交或复制 `RequestId` 提交工单；
- 文件导入：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入时需确保无空行，否则后续行将被忽略；
- 增量渲染：前端需自行解析模型返回的 Markdown 格式（如 `**text**`），并做对应样式渲染。

## 限制和注意事项

- **Header 限制**：自定义插件调用时，仅支持透传 `Authorization`，其他 Header（如 `X-User-ID`、`Cookie`）会被过滤 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **文件容量与数量**：单业务空间最多上传 10 万个文档；PDF 文件后缀必须为小写 `pdf`，否则报错 `140010`。
- **第三方工具支持边界**：阿里云百炼售后**不负责**第三方工具（如 Cursor、Windsurf 等）的安装、配置、升级或故障排查，仅提供方向性建议（如连通性测试、SDK 示例、计费核查） [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。
- **服务协议约束**：使用前须遵守《阿里云百炼服务协议》及《阿里云百炼体验功能特别说明》，开源模型还需遵循对应协议条款 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


