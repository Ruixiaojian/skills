# application [support](support.md)

阿里云百炼平台为应用开发者提供覆盖模型调用、智能体（Agent）构建、RAG增强、插件集成等场景的端到端技术支持。支持范围明确区分平台原生能力与第三方工具责任边界，以工单、7×24电话及在线服务为主要响应渠道。所有服务均受[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)约束，具体权益详见[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 支持的模型与功能

- **核心模型能力**：支持通义千问系列大模型（Qwen）、百炼定制模型及开源模型（需遵守[开源模型协议条款说明](../../raw/application-user-guide/application-support/application-related-agreements.md)）。
- **智能体（Agent）能力**：提供 Assistant API 与 Agent 框架，支持插件编排、上下文感知决策与[函数调用](../concepts/function-calling.md)；当前官方插件包括 Python 解释器、计算器、图片生成、夸克搜索、二维码生成、GitHub 搜索（部分需申请开通）。
- **RAG 增强**：支持多知识库并行检索（按配置权重打分后取 topN），适用于问答、客服、教育等场景；检索结果精度可通过反馈机制优化（见[常见问题](../../raw/application-user-guide/application-support/application-faq.md)第6条）。
- **流式与增量输出**：`stream=True` 启用基础流式，`incremental_output=True` 启用增量式[流式输出](../concepts/streaming-output.md)（避免重复渲染）。

> **注意**：文档3中称“Assistant API 可以提供各种类，方便调优”，但未明确定义“类”的技术含义；实际开发中应以 [Assistant API 官方文档](https://help.aliyun.com/zh/model-studio/developer-reference/assistant-api) 为准，避免将此表述误解为面向对象编程中的 class 实例。

## 关键参数

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `stream` | bool | 是否启用流式响应 | `True` |
| `incremental_output` | bool | 是否启用增量式流式（仅当 `stream=True` 时生效） | `True` |
| `md5`（文件上传） | string | 用于校验文件完整性，必填 | `"d41d8cd98f00b204e9800998ecf8427e"` |
| `authorization`（插件调用） | header | 唯一支持透传的 HTTP Header；自定义 header（如 `X-Api-Key`）**不被支持** | `Bearer <token>` |

## 使用方式

- **基础支持渠道**：7×24 电话（95187 / 400）、智能在线客服、标准工单（[提交入口](https://smartservice.console.aliyun.com/service/create-ticket)）。
- **API/SDK 问题**：优先查阅 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 第1条（4）款所列范围，确认属百炼服务端问题后再提工单。
- **RAG 问题定位**：若检索结果不准确，可点击回复下方“问题反馈”按钮提交类型，或复制 `RequestId` 提交工单（见[常见问题](../../raw/application-user-guide/application-support/application-faq.md)第6条）。
- **备案与合作**：应用上架前需完成[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)，并[提交工单](https://smartservice.console.aliyun.com/service/create-ticket)申请通义千问合作协议。

## 限制和注意事项

- **第三方工具责任边界**：阿里云百炼**不支持**第三方工具（如 Cursor、Windsurf 等）的安装、配置、升级、本地环境（代理/防火墙/VPN/OS）问题排查、业务代码调试，也不对第三方工具内部统计（如 [Token](../concepts/token.md) 数量、费用预估）与阿里云计费数据差异负责（详见[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)第4条）。
- **插件调用限制**：自定义插件仅支持透传 `Authorization` header；其他 header 将被丢弃（见[常见问题](../../raw/application-user-guide/application-support/application-faq.md)第10条）。
- **文件上传限制**：PDF 文件后缀必须为小写 `pdf`；结构化数据导入时，空行将导致后续行被跳过（见[常见问题](../../raw/application-user-guide/application-support/application-faq.md)第1、4条）。
- **法律协议约束**：所有使用行为须同时遵守[阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md)、[体验功能特别说明](../../raw/application-user-guide/application-support/application-related-agreements.md)及开源模型相关条款。

## 来源文档

- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)


