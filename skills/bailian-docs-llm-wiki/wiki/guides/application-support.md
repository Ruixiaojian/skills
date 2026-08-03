# application support

`application support` 指百炼平台为开发者在构建和运行 AI 应用（含智能体、RAG 应用、插件集成等）过程中提供的功能能力、调用接口、配置参数及配套服务支持。它覆盖模型调用、插件扩展、知识检索增强、[流式输出](../concepts/streaming-output.md)控制等核心场景，同时明确服务边界与售后响应范围。开发者需结合具体功能需求与限制条件进行集成设计。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件，包括 Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；部分插件需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置策略打分后选取 topN 结果用于上下文增强，适用于问答系统、客服对话、教育辅助等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过符合协议的 API 接入自定义函数，大模型可理解其参数结构并生成调用逻辑；但**不支持透传除 `Authorization` 外的任意 HTTP Header**，该限制已在实际调试中验证 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming-output.md)控制**：支持两种模式：`stream=True`（全量流式）、`incremental_output=True`（增量式流式），后者可避免重复渲染历史内容。

> **注意**：文档 1 中第 4 条称 “Assistant API 可提供各种类，方便调优”，但未说明具体类名或 SDK 接口形态；当前百炼 Python SDK 中并无 `Assistant` 类，实际调用统一通过 `BailianClient.chat()` 或 `BailianClient.agent()` 等方法实现。该描述易引发误解，应以 [SDK 文档](https://help.aliyun.com/zh/model-studio/developer-reference/sdk-reference) 为准。

## 关键参数

| 参数名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `stream` | bool | 启用流式响应（逐 token 返回） | `True` |
| `incremental_output` | bool | 启用增量式流式（仅返回新增 token） | `True` |
| `retrieval_config` | dict | RAG 检索配置，含 `top_k`、`score_threshold` 等 | `{"top_k": 3}` |
| `plugins` | list[str] | 指定启用的插件 ID 列表 | `["calculator", "qwen-vl"]` |

> **注意**：`incremental_output=True` 仅在 `stream=True` 时生效，单独设置无效。

## 使用方式

- 插件调用需在应用配置或 API 请求中显式声明 `plugins` 参数，并确保已开通对应权限；  
- RAG 应用需预先创建知识库并绑定至应用，检索行为由平台自动触发，无需手动调用检索接口；  
- 自定义插件需提供符合 OpenAPI 3.0 规范的 JSON Schema 描述，平台据此生成[工具调用](../concepts/tool-use.md)指令；  
- 流式响应需客户端正确处理 `text/event-stream` MIME 类型及 `data:` 前缀格式；增量模式下，每个 chunk 的 `content` 字段为本次新增文本，非累计全文。

## 限制和注意事项

- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入时，空行将导致后续行被截断 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **知识库容量**：单业务空间上限为 10 万文档，超限时需提交工单申请扩容。  
- **Header 透传**：自定义插件调用时，仅 `Authorization` 头可被透传，其他 header（如 `X-User-ID`、`Cookie`）会被丢弃。  
- **售后支持边界**：阿里云百炼仅保障自身服务端可用性、API 正确性及计费准确性；第三方工具（如 Cursor、Windsurf）的部署、配置、兼容性问题不在标准售后范围内 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：使用百炼服务须遵守《阿里云百炼服务协议》及《阿里云百炼体验功能特别说明》，开源模型还需额外遵循对应协议条款 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


