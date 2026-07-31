# application support

阿里云百炼平台的应用支持覆盖模型服务使用、API调用、插件集成及RAG等核心能力，面向开发者提供基础技术咨询、故障诊断与工单响应。支持范围严格限定于百炼平台自身服务（含控制台、API、SDK、计量计费系统），不包含第三方工具运维、用户本地环境问题或业务代码实现。超出平台责任边界的事项，将提供方向性建议并引导至对应责任方。

## 支持的模型/功能

- **模型服务**：包括通义千问系列大模型（Qwen）、百炼自研模型及开源模型（需符合[开源模型协议条款说明](https://help.aliyun.com/zh/model-studio/open-source-model-terms)）的推理调用；
- **应用能力**：Agent 与 Assistant API（后者提供更便捷的类封装与调优接口）、知识检索增强（RAG）、自定义插件（当前支持 Python 解释器、计算器、图片生成、夸克搜索、二维码生成、GitHub 搜索六类官方插件）；
- **数据管理**：文档上传（PDF/DOC/DOCX，注意后缀须为小写 `pdf`）、结构化数据导入（空行会截断后续数据）、知识库配置与检索（RAG 默认并行检索各知识库，按得分聚合 TopN 结果）。

> **注意**：文档2中称“自定义插件服务目前暂时不收费”，但未明确是否包含调用产生的模型推理费用；实际计费以[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)为准，建议结合[阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md)确认费用边界。

## 关键参数

- **[流式输出](../concepts/streaming-output.md)**：启用增量响应需同时设置 `stream=True` 和 `incremental_output=True`（见[常见问题](../../raw/application-user-guide/application-support/application-faq.md)第8条）；
- **插件调用**：仅支持透传 `Authorization` header，**不支持自定义 header**（见[常见问题](../../raw/application-user-guide/application-support/application-faq.md)第10条）；
- **文件校验**：上传接口必填 `MD5` 参数，用于验证文件完整性（见[常见问题](../../raw/application-user-guide/application-support/application-faq.md)第3条）；
- **RAG 检索**：默认并行执行，结果按各知识库配置的评分规则加权聚合（见[常见问题](../../raw/application-user-guide/application-support/application-faq.md)第9条）。

## 使用方式

- **基础支持渠道**：7×24 小时电话（95187 / 400）、智能在线客服、标准工单（通过[阿里云工单系统](https://smartservice.console.aliyun.com/service/create-ticket)提交）；
- **问题反馈**：RAG 测试中模型回复不准确时，可点击回复下方“问题反馈”按钮提交，或复制 `RequestId` 提交工单（见[常见问题](../../raw/application-user-guide/application-support/application-faq.md)第6条）；
- **合规备案**：接入通义千问模型上架应用市场或小程序，需按[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)流程操作，并[提交工单](https://smartservice.console.aliyun.com/service/create-ticket)申请合作协议；
- **第三方对接**：仅提供方向性建议，如确认百炼 API 可用性、提供官方 SDK 示例、协助核查调用明细与计费记录（见[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)第4节）。

## 限制和注意事项

- **责任边界明确**：阿里云不承担第三方工具（如 Cursor、Windsurf 等）的安装、配置、升级、故障诊断及日常运维责任；也不处理用户本地环境（内网、代理、VPN、防火墙、OS 兼容性）导致的问题（见[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)第4节）；
- **插件限制**：自定义插件需遵循协议规范，模型理解参数依赖传入的描述质量；部分官方插件（如图片生成）需单独申请开通；
- **数据容量**：单个业务空间最多上传 10 万个文档，超限时需[提交工单](https://smartservice.console.aliyun.com/service/create-ticket)申请扩容（见[常见问题](../../raw/application-user-guide/application-support/application-faq.md)第2条）；
- **法律依据**：所有支持行为均以[阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md)及官网公布的[客户服务权益](https://www.aliyun.com/service/customer-service-benefits?spm=5176.support-home.J_3451238410.1.12d1156fPBBxO0)为准，付费增值服务需另行订购。

## 来源文档

- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


