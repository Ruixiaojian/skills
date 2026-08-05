# application support

application support 指百炼平台为开发者提供的应用层技术支撑能力，涵盖模型集成、插件调用、RAG增强、API使用及售后响应等关键环节。它不包含第三方工具运维或业务代码开发支持，所有服务边界以官方协议与售后范围说明为准。开发者需结合 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)、[常见问题](../../raw/application-user-guide/application-support/application-faq.md) 和 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 三类文档协同使用。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件——Python代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub搜索；其中部分需申请开通。  
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置策略打分后选取 topN 结果，适用于问答系统、客服、教育、内容创作等场景。  
- **自定义插件**：支持通过 API 注册函数，模型可理解参数结构并生成调用请求；但仅支持 `Authorization` header 透传，**不支持其他自定义 header**（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第10条）。  
> **注意**：文档2中第4条称“Assistant API 可提供各种类，方便调优”，但未明确具体类名或接口契约；该描述缺乏可操作性，实际开发请以控制台插件配置页和 SDK 文档为准，避免依赖此模糊表述。

## 关键参数

- `stream=True`：启用[流式输出](../concepts/streaming-output.md)（全量 chunk 流）。  
- `incremental_output=True`：启用增量式[流式输出](../concepts/streaming-output.md)（仅返回新增 token，非累计内容）。  
- 文件上传必填 `MD5`：用于校验文件完整性（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第3条）。  
- 知识库检索配置：支持按权重、相似度阈值、topK 等参数调整 RAG 行为，具体以控制台设置项为准。

## 使用方式

- **插件调用**：内置插件在应用编排中直接启用；自定义插件需注册 API 地址、描述及参数 schema，由模型自动解析并构造请求。  
- **RAG 调试**：测试时若结果不准，可通过回复下方“问题反馈”按钮提交，或复制 `RequestId` 提交工单（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第6条）。  
- **Markdown 渲染**：模型输出中的 `**text**` 需前端自行解析渲染为加粗样式，平台不默认处理（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第7条）。  
- **备案与合作**：上架应用市场或小程序前，须完成 [应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)，并提交工单申请通义千问合作协议。

## 限制和注意事项

- **文件限制**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；单业务空间最多 10 万文档，超限需提工单扩容（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第1、2条）。  
- **结构化数据导入**：空行会导致后续数据被跳过；首行为空则视为无效文件（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第4条）。  
- **第三方工具支持边界**：阿里云仅对百炼服务端状态、API 可用性、SDK 调用、计费明细提供支持；**不负责 Cursor/Windsurf/OpenClaw 等第三方工具的安装、配置、故障排查或本地环境（如代理、防火墙）问题**（见 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 第4条）。  
- **法律与合规**：所有使用须遵守 [阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md) 及开源模型协议条款，违规使用可能导致服务终止。

## 来源文档

- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


