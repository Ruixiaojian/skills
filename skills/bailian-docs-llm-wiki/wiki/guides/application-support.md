# application [support](support.md)

application [support](support.md) 指阿里云百炼平台为开发者提供的模型服务使用保障体系，涵盖售后响应、功能支持边界、技术接入规范及常见问题处理机制。该支持体系以百炼平台自身服务（API、控制台、计费系统、模型推理能力）为核心责任范围，明确区分阿里云侧与用户侧/第三方侧的责任边界。所有支持均以服务协议和官方文档为准，不覆盖非百炼原生组件的运维与开发。

## 支持的模型/功能

- **官方插件能力**：当前提供 Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索六类插件；部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **RAG（知识检索增强）**：支持多知识库并行检索、topN 聚合排序，适用于问答、客服、教育等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **Agent 与 Assistant API**：Agent 提供插件编排与上下文理解能力；Assistant API 提供标准化接口与调优类支持，二者在模型调度与开发自由度上存在差异 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **[流式输出](../concepts/streaming-output.md)**：支持 `stream=True` 全量流式与 `incremental_output=True` 增量式[流式输出](../concepts/streaming-output.md)，适用于前端实时渲染场景。

> **注意**：文档 3 中“自定义插件服务目前暂时不收费”与实际计费策略可能存在时效偏差——配置智能体 API 时涉及 [prompt](prompt.md) 优化、应用调用及测试窗测试均按标准 API 调用量计费，建议以[阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md)及控制台最新计费说明为准。

## 关键参数

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回） | `True` |
| `incremental_output` | bool | 启用增量式流式输出（仅返回新增内容） | `True` |
| `authorization` | string | 唯一支持透传的 HTTP Header，用于身份认证 | `Bearer <token>` |
| `MD5` | string | 文件上传必填校验参数，用于完整性验证 | `d41d8cd98f00b204e9800998ecf8427e` |

> **注意**：自定义插件调用**不支持透传任意 header**，仅 `Authorization` 可被识别；其他 header（如 `X-User-ID`、`X-Tenant`）将被忽略 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 使用方式

- **基础支持渠道**：7×24 小时电话（95187 / 400）、智能在线客服、标准工单，覆盖模型功能咨询、API/SDK 故障诊断、控制台操作、账号与计费问题 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。
- **第三方集成建议**：阿里云可提供方向性指导，包括确认百炼 API 可用性、提供官方 SDK 示例、协助核查调用明细与计费记录、建议基础连通性测试（如 `curl` 测试 endpoint） [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。
- **问题反馈路径**：RAG 回复不准确时，可通过界面“问题反馈”按钮提交，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 限制和注意事项

- **责任边界明确**：阿里云仅对百炼服务端（API 接口、计量计费、控制台、模型推理服务）负责；第三方工具（如 Cursor、Windsurf 等）的安装、配置、升级、故障排查均由用户或其提供方承担 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。
- **本地环境免责**：因用户本地网络（代理、VPN、防火墙）、操作系统、内网策略或业务代码导致的问题，不在标准支持范围内。
- **文件上传限制**：PDF 文件后缀必须为小写 `pdf`；结构化数据导入时，空行将导致后续行被截断；单业务空间上限 10 万文档，超限需提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **合规要求**：接入通义千问模型并上架应用市场/小程序，须完成[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)并单独申请合作协议 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 来源文档

- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)


