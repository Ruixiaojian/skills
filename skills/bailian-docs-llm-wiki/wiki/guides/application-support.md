# application [support](support.md)

`application support` 指百炼平台为构建和运行 AI 应用（含智能体、RAG 应用、插件集成等）所提供的核心能力支持体系，涵盖模型调用、插件扩展、知识检索增强、[流式输出](../concepts/streaming-output.md)及数据管理等关键环节。开发者需结合服务协议与技术规范进行开发与部署。相关法律约束和合规要求详见 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 支持的模型与功能

- **插件能力**：官方提供六类内置插件：Python代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub搜索；其中部分插件需申请开通。  
- **自定义插件**：支持通过 API 注册自定义插件，大模型可解析其参数定义并调用（参见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第3条）。  
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置策略（如相似度得分）选取 topN 片段后融合生成，适用于问答、客服、教育等场景（[常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第5条）。  
- **流式与增量输出**：支持 `stream=True` 实现流式响应；进一步启用 `incremental_output=True` 可获得真正增量式 token 输出（非全量重传），适用于前端实时渲染（[常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第8条）。

> **注意**：文档2中第4条称“Assistant API 可提供各种类，方便调优”，但未明确具体类名或接口契约；当前 SDK 与 OpenAI 兼容 API 中实际暴露的是 `assistant` 类型资源（非 `Assistant` 类），该描述易引发歧义，建议以 [API 参考文档](https://help.aliyun.com/zh/model-studio/developer-reference) 为准。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回） |
| `incremental_output` | bool | 在 `stream=True` 基础上启用增量式输出（仅返回新增 token，非累计内容） |
| `MD5`（文件上传） | string | 文件完整性校验值，必填（[常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第3条） |
| `authorization`（插件调用） | header | 插件 HTTP 请求中唯一支持透传的 header；其他自定义 header 将被丢弃（[常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第10条） |

## 使用方式

- **插件调用**：注册插件时需声明 `name`、`description`、`parameters`（JSON Schema 格式），系统自动注入至模型上下文；调用时模型生成结构化 function call 请求，平台负责路由与执行。  
- **RAG 应用测试**：若检索结果不准确，可通过回复下方“问题反馈”按钮提交，或复制 `RequestId` 提交工单（[常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第6条）。  
- **Markdown 渲染**：模型输出中的 `**text**` 等标记需由前端自行解析并渲染为加粗等样式（[常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第7条）。  
- **备案与合作**：接入通义千问模型并上架应用市场/小程序前，须完成 [应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)，并提交工单申请合作协议（[常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第11条）。

## 限制和注意事项

- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入时，空行将导致后续行被截断（[常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第1、4条）。  
- **知识库容量**：单业务空间上限为 10 万个文档；超限时需提交工单申请扩容（[常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第2条）。  
- **协议约束**：所有应用必须遵守 [阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md) 及 [开源模型协议条款说明](../../raw/application-user-guide/application-support/application-related-agreements.md)，尤其注意数据使用、模型输出责任归属等条款。  
- **插件安全限制**：自定义插件无法透传除 `Authorization` 外的任何 HTTP header，服务端会主动剥离其余 header 字段（[常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第10条）。

## 来源文档

- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)


