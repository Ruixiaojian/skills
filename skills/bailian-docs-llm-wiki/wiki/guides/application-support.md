# application support

`application support` 指百炼平台为开发者构建和运行 AI 应用所提供的全链路支撑能力，涵盖模型调用、插件集成、RAG 增强、[流式输出](../concepts/streaming-output.md)、API 配置及售后响应等核心环节。它不包含第三方工具的运维支持，也不覆盖用户侧业务代码或本地环境问题的深度排查。所有服务均以阿里云百炼平台自身服务边界为基准，详见 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 支持的模型/功能

- **内置插件**：当前官方支持 6 类插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置得分选取 topN 结果后融合生成；适用于问答、客服、教育、内容创作等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：支持 `stream=True` 实现流式响应；进一步启用 `incremental_output=True` 可返回增量式 token（非全量重传）。  
- **自定义插件**：支持通过标准协议注册函数/API，大模型可理解参数结构并调用；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中“Agent 和 Assistant API 的最大区别”描述模糊且缺乏技术定义（如未明确 Agent 是否指百炼的智能体编排能力），该条目与当前控制台实际能力存在偏差，建议以[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)中定义的服务边界为准，避免依赖该主观对比。

## 关键参数

| 参数名 | 类型 | 说明 | 必填 |
|--------|------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回） | 否（默认 `False`） |
| `incremental_output` | bool | 在 `stream=True` 下启用增量式 token 输出（避免重复返回历史内容） | 否（默认 `False`） |
| `MD5` | string | 文件上传时必填，用于校验文件完整性 | 是（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)） |

## 使用方式

- 插件调用：通过应用配置页绑定插件，或在 Assistant API 请求中声明 `tools` 列表；自定义插件需符合 OpenAI-style function calling 协议。  
- RAG 集成：在应用中关联已创建的知识库，系统自动执行并行检索 + 重排序 + 提示注入。  
- 流式响应：设置 `stream=True` 并按 SSE 或 chunked transfer 解析响应体；如需前端渲染 Markdown（如 `**text**` → 加粗），需自行解析并渲染 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- 工单反馈：RAG 结果不准确时，可点击回复下方“问题反馈”按钮提交，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 限制和注意事项

- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入时，空行将导致后续行被忽略。  
- **知识库容量**：单业务空间上限 10 万个文档；超限时需提交工单申请扩容。  
- **第三方工具支持边界**：阿里云仅提供百炼服务端状态确认、API 示例、计费核查及基础连通性建议；**不支持**第三方工具（如 Cursor、Windsurf 等）的安装、配置、升级或故障诊断，亦不对其行为担责 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议与合规**：应用上架前须完成[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)，并按需申请通义千问合作协议；相关法律条款参见 [阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


