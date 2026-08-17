# application support

`application support` 指阿里云百炼平台为开发者在应用构建、集成与运维全周期中提供的技术支撑体系，涵盖模型调用、插件扩展、RAG 应用、API 使用及售后响应等核心环节。其目标是保障开发者高效、合规、稳定地使用百炼能力，同时明确平台责任边界。所有支持活动均以《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)》为基础法律依据，具体范围详见 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 支持的模型与功能

- **内置插件能力**：官方提供 6 类开箱即用插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；部分需申请开通。  
- **自定义插件**：支持通过 Assistant API 接入用户自定义 HTTP API 插件，模型可理解参数结构并完成调用；但**仅支持 `Authorization` header 透传，不支持其他自定义 header**（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第 10 条）。  
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置策略打分后取 topN 结果融合生成；适用于问答、客服、教育等场景（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第 5–9 条）。  
- **流式与增量输出**：可通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 实现增量式[流式输出](../concepts/streaming-output.md)（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第 8 条）。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `stream` | bool | 控制是否启用[流式输出](../concepts/streaming-output.md)（默认 `False`） |
| `incremental_output` | bool | 仅在 `stream=True` 时生效，启用后返回增量 token（非全量重传） |
| `MD5` | string | 文件上传接口必填，用于校验文件完整性（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第 3 条） |
| `Authorization` | string | 自定义插件调用时唯一允许透传的 header 字段 |

> **注意**：文档 3 中第 4 条称 “Assistant API 可以提供各种类，方便调优”，但未明确定义“类”指代对象类型或 SDK 接口分类；该表述缺乏上下文与技术定义，建议以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中明确的 API 和 SDK 故障诊断支持范围为准，避免误解为平台提供通用编程框架级抽象。

## 使用方式

- **技术支持渠道**：购买服务期内，可通过官网、电话（95187 / 400）、阿里云 APP 获取 7×24 小时咨询；标准工单支持覆盖模型功能、API/SDK 故障、控制台问题、账号与计费咨询（见 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 第 1 条）。  
- **问题反馈路径**：RAG 测试中出现回复不准，可点击反馈按钮提交，或**复制 RequestId 提交工单**（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第 6 条）。  
- **备案与合作**：若需上架含通义千问的应用至外部市场，须按 [应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model) 指南操作，并[提交工单](https://smartservice.console.aliyun.com/service/create-ticket)申请合作协议（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第 11 条）。

## 限制和注意事项

- **第三方工具支持边界**：阿里云仅对百炼服务端状态、API 可达性、官方 SDK 示例及计费明细提供方向性建议；**不支持第三方工具（如 Cursor、Windsurf 等）的安装、配置、升级、故障排查，亦不承担其行为责任**（见 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 第 4–5 条）。  
- **文件上传限制**：PDF 文件后缀必须为小写 `pdf`；单业务空间最多上传 10 万个文档，超限时需[提交工单申请扩容](../../raw/application-user-guide/application-support/application-faq.md)（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第 1、2 条）。  
- **协议约束**：所有使用须遵守《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)》《[阿里云百炼体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html)》及开源模型相关条款（见 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)）。

## 来源文档

- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)


