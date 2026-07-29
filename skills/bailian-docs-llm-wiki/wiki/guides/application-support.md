# application support

`application support` 指百炼平台为开发者在构建和运行 AI 应用（如智能体、RAG 应用、[插件](../concepts/plugin.md)集成等）过程中提供的功能能力、调用接口、参数配置及配套支持服务。它涵盖模型与[插件](../concepts/plugin.md)能力接入、流式/增量输出控制、知识检索增强（RAG）机制、API 调用限制与售后响应边界等核心环节，是应用稳定上线与持续迭代的技术基础。开发者需结合具体场景选择合适的能力组合，并严格遵循平台约束条件。

## 支持的模型/功能

- **内置[插件](../concepts/plugin.md)能力**：当前官方支持六类插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索。部分插件需申请开通 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持多知识库并行检索，按用户配置的权重与相似度得分选取 topN 片段后融合生成，广泛应用于问答系统、客户服务、教育培训等场景 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过符合协议的 API 接入，大模型可理解其参数结构并自主调用；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：可通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 实现真正增量式 token 输出（即每次返回新生成内容，而非全量重发）。

> **注意**：文档 1 中“Agent 和 Assistant API 的最大区别”描述模糊且缺乏技术细节（如未说明 Agent 是否指百炼原生智能体或第三方框架），该条目未被其他文档佐证，建议以控制台实际能力与 [阿里云百炼平台售后服务范围说明 (raw/application-user-guide/application-support/application-after-sales-service-scope.md)](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中定义的服务边界为准。

## 关键参数

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `stream` | bool | 控制是否启用流式响应 | `True` |
| `incremental_output` | bool | 在 `stream=True` 基础上启用增量式输出（避免重复渲染） | `True` |
| `top_k`（RAG） | int | 检索结果返回的最大片段数 | `3` |
| `score_threshold`（RAG） | float | 过滤低相关性检索结果的阈值 | `0.3` |
| `MD5`（文件上传） | string | 用于校验上传文件完整性，必填 | `"d41d8cd98f00b204e9800998ecf8427e"` |

## 使用方式

- **插件调用**：在智能体配置中启用对应插件，自定义插件需提供符合 OpenAPI 3.0 规范的 Schema 描述；模型将基于 Schema 自动解析参数并构造请求。  
- **RAG 配置**：在应用编辑页绑定知识库，设置检索策略（如关键词+向量混合）、重排序规则及上下文长度限制。  
- **流式/增量输出**：在调用 `Assistant API` 或 `ChatCompletion` 接口时，显式传入 `stream=True` 和 `incremental_output=True`。前端需按 chunk 解析并拼接，而非累积覆盖。  
- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入需确保无空行，否则后续行将被忽略。

## 限制和注意事项

- **插件限制**：自定义插件不支持除 `Authorization` 外的任何 HTTP Header 透传；非官方插件的稳定性、安全性及计费归属由用户自行承担。  
- **知识库容量**：单业务空间最多支持 10 万个文档，超限时需提交工单申请扩容 [常见问题 (raw/application-user-guide/application-support/application-faq.md)](../../raw/application-user-guide/application-support/application-faq.md)。  
- **售后支持边界**：阿里云百炼仅保障自身服务端（API、控制台、计费系统）的可用性与正确性；**不支持**第三方工具（如 Cursor、Windsurf 等）的部署、配置、调试，也不承担其与百炼集成过程中的兼容性问题 [阿里云百炼平台售后服务范围说明 (raw/application-user-guide/application-support/application-after-sales-service-scope.md)](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **合规要求**：接入通义千问模型的应用上架至应用市场或小程序平台前，必须完成[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)，并签署合作协议。  
- **协议约束**：所有使用均须遵守《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)》及《[阿里云百炼体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html)》 [相关协议 (raw/application-user-guide/application-support/application-related-agreements.md)](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


