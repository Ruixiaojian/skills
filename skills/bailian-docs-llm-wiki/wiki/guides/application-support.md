# application [support](support.md)

`application support` 指百炼平台为开发者在构建和运行 AI 应用（如智能体、RAG 应用、[插件](../concepts/plugin.md)集成等）过程中提供的功能支持、参数配置指导、调用方式说明及服务边界定义。它覆盖模型能力调用、[插件](../concepts/plugin.md)扩展、知识库增强、[流式输出](../concepts/streaming-output.md)控制等核心开发环节，同时也明确了阿里云侧的技术支持范围与责任边界。开发者需结合具体场景选择合适的能力组合，并注意协议约束与技术限制。

## 支持的模型/功能

- **内置[插件](../concepts/plugin.md)能力**：当前官方支持六类插件，包括 Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；部分插件需申请开通 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索，按配置权重与得分选取 topN 结果后融合生成，适用于问答系统、客服对话、教育辅助等场景 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过符合 OpenAPI 规范的 HTTP 接口注册插件，大模型可理解其参数结构并自主调用；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming-output.md)控制**：支持两种流式模式：`stream=True`（全量分块返回）与 `incremental_output=True`（增量式[流式输出](../concepts/streaming-output.md)，即每次返回新增内容而非累积重发）。

> **注意**：文档 1 中“Agent 和 Assistant API 的最大区别”描述模糊且未明确定义二者技术差异，实际开发中应以控制台/API 文档为准，避免依赖该条目做架构决策。

## 关键参数

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `stream` | bool | 启用流式响应（SSE），返回分块 token | `True` |
| `incremental_output` | bool | 启用增量式流式输出（仅限部分模型），避免重复渲染 | `True` |
| `retrieval_top_k` | int | RAG 检索时每个知识库返回的最大文档数 | `3` |
| `plugin_ids` | list[str] | 显式指定启用的插件 ID 列表（需已授权） | `["qwen-calculator", "qwen-qrcode"]` |
| `md5` | string | 文件上传必填校验字段，用于验证文件完整性 | `"d41d8cd98f00b204e9800998ecf8427e"` |

## 使用方式

- **插件调用**：在应用配置或 API 请求中声明 `plugin_ids`，模型将自动识别用户意图并触发对应插件；自定义插件需提前在控制台完成注册与鉴权。  
- **RAG 集成**：上传 PDF/DOC/DOCX 格式知识文件（注意后缀必须为小写 `pdf`），导入结构化数据时需确保无空行，否则后续行将被忽略 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式响应处理**：前端需解析 SSE 响应，对 `incremental_output=True` 的流式结果直接追加渲染，避免重复解析 markdown（如 `**text**` 需由前端转换为 HTML 加粗）[常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **问题反馈**：RAG 输出不准确时，可通过控制台“问题反馈”按钮提交，或复制 `RequestId` 提交工单 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。

## 限制和注意事项

- **文件上传限制**：单业务空间最多支持 10 万文档，超限时需提交工单申请扩容；PDF 文件后缀必须为小写 `pdf`，否则报错 `140010`。  
- **第三方工具支持边界**：阿里云仅保障百炼服务端 API 可用性、提供标准 SDK 与调用示例，**不支持第三方工具（如 Cursor、Windsurf 等）的安装、配置、调试及本地环境（代理/防火墙/VPN）问题排查** [阿里云百炼平台售后服务范围说明 (raw/application-user-guide/application-support/application-after-sales-service-scope.md)](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：所有使用须遵守《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)》及《[阿里云百炼体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html)》，开源模型还需遵循对应 [开源模型协议条款说明](https://help.aliyun.com/zh/model-studio/open-source-model-terms) [相关协议 (raw/application-user-guide/application-support/application-related-agreements.md)](../../raw/application-user-guide/application-support/application-related-agreements.md)。  
- **计费说明**：自定义插件本身免费，但通过智能体 API 进行 [prompt](prompt.md) 优化、应用调用测试等操作将产生费用。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


