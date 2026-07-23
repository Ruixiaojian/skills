# application [support](support.md)

`application support` 指百炼平台为开发者在构建和运行 AI 应用（含智能体、RAG 应用、插件集成等）过程中提供的功能能力、调用接口、参数配置及配套服务支持。它覆盖模型调用、插件扩展、知识检索增强、[流式输出](../concepts/streaming-output.md)等核心开发场景，并明确界定平台侧与用户侧的责任边界。相关能力与限制需结合具体 API 行为与服务协议综合理解。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置策略打分后选取 topN 结果用于生成，适用于问答系统、客户服务、教育等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过符合协议的 API 接入，大模型可理解其参数结构并自主调用；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming-output.md)**：支持增量式流式响应，需同时设置 `stream=True` 和 `incremental_output=True`。

## 关键参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（默认 `False`） |
| `incremental_output` | bool | 启用增量式流式输出（仅当 `stream=True` 时生效） |
| `MD5` | string | 文件上传必填，用于校验文件完整性（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)） |

> **注意**：文档 1 中第 8 条明确要求 `incremental_output=True` 实现增量输出，但当前 Assistant API 的 OpenAPI 规范中该参数名为 `enable_incremental_output`（v2024-06+），实际调用请以控制台 SDK 或最新 OpenAPI 文档为准。

## 使用方式

- 插件调用：通过 `tools` 字段声明插件列表，由模型自动选择并填充参数；自定义插件需提供符合 OpenAPI 3.0 规范的 `function` 描述。  
- RAG 应用：在应用配置中绑定知识库，测试时若结果不准确，可通过界面反馈按钮提交问题，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- 文件上传：仅支持小写后缀的 `pdf`/`doc`/`docx`；结构化数据导入需避免空行，否则后续行将被跳过。  
- 售后支持入口：7×24 小时电话（95187）、智能在线、标准工单；基础服务覆盖 API 故障诊断、SDK 使用、控制台问题等 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **插件 Header 限制**：自定义插件调用时，仅 `Authorization` 可透传，其他 Header（如 `X-User-ID`、`Cookie`）会被丢弃。  
- **知识库容量**：单业务空间上限 10 万文档，超限时需提交工单申请扩容。  
- **第三方工具责任边界**：阿里云不负责 Cursor、Windsurf 等第三方工具的安装、配置、故障排查或本地环境（代理/防火墙/VPN）问题；仅提供百炼服务端连通性验证与调用示例参考 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **合规与备案**：接入通义千问模型上架应用市场或小程序前，须完成[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)并申请合作协议。  
- **协议约束**：所有使用须遵守《阿里云百炼服务协议》及《阿里云百炼体验功能特别说明》，开源模型还需符合对应[开源模型协议条款](https://help.aliyun.com/zh/model-studio/open-source-model-terms) [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


