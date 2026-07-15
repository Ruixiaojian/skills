# support

阿里云百炼平台的 `support` 模块涵盖服务开通、计费、API/SDK 使用、模型能力边界及合规协议等核心支持事项。本文档面向开发者，系统梳理当前平台在功能支持、参数配置、调用方式、限制条件等方面的明确要求与实践指引，所有信息均基于最新公开文档与控制台行为验证。

## 支持的模型/功能

- **模型类型**：支持千问系列（Qwen-Turbo、Qwen-Max、Qwen3、Qwen-VL-Plus 等）及其他第三方模型，覆盖文本生成、多模态（图像训练）、RAG 增强等场景；其中 Qwen-VL-Plus 明确支持图片微调训练 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **功能范围**：
  - Completion API 与 Assistant API 均已上线，但 Assistant API **暂不支持 memory 配置**，且 **不支持单次调用中依次执行两个本地函数**（需拆分为两个独立 Assistant API 调用）。
  - RAG 功能可用，`doc_reference_type` 参数仅在旧版应用中生效；新版应用需通过控制台「展示回答来源」开关启用答案溯源能力 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **数据对接**：当前**不支持直接对接 MySQL、Hive 等结构化数据库**，RDS 接入正在开发中。

> **注意**：文档 1 中“模型中心”第10条称“当前不支持”结构化数据对接，而文档 2 未涉及此内容；该限制仍有效，无更新说明。

## 关键参数

- **必需参数**：Completion API 调用必须包含 `AppId`、`Prompt`、`RequestId`；缺失或格式错误将返回错误码 `100004` [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **幻觉抑制参数**：可通过降低 `temperature`、`top_k`、`top_p` 提升输出确定性；缩短 `max_tokens` 可防止冗余捏造；这些参数调整是降低模型幻觉的有效手段之一。
- **RAG 相关参数**：`doc_reference_type` 仅对旧版应用生效，新版依赖控制台开关，参数设置无效。

## 使用方式

- **服务开通**：需以阿里云主账号在目标地域（如北京、新加坡）的[百炼控制台](https://bailian.console.aliyun.com/)开通，开通前须完成实名认证。
- **API 调用**：
  - 支持 Python 和 Java SDK，安装方法详见官方指南；
  - 请求需携带 `Authorization: Bearer <API-Key>`，Header 中 `Content-Type` 必须为 `application/json`；
  - 错误码含义及处理方案请查阅 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code)。
- **计费与账单**：
  - 后付费按分钟出账、按月结算；
  - 扣款明细与发票申请均通过阿里云[费用与成本控制台](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)操作；
  - 预付费支持节省计划与资源包，详情见 [节省计划与资源包](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package)。

## 限制和注意事项

- **服务关闭**：百炼服务开通后**不可主动关闭**；如需停用，仅能删除对应地域的 API-Key 以阻断调用。
- **数据隐私与存储**：
  - 所有传输数据经 AES-256 加密；
  - 平台依法律法规存储调用日志，**不用于模型训练**；
  - 控制台历史对话最多保留 100 条，未登录状态及推理报错对话不保存。
- **模型能力边界**：
  - 万相会员权益**不适用于百炼 API 调用**，二者计费体系完全独立；
  - 不支持为生成文本添加隐式标识；
  - 无官方手机端 App，仅提供 Web 控制台访问。
- **合规与协议**：使用前须阅读并接受 [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=a2c4g.2667824.0.0.6a2f6f83Ivpy5F) 及 [SLA 协议](https://terms.alicdn.com/legal-agreement/terms/b_end_product_protocol/20250923215800868/20250923215800868.html)，相关条款详见 [相关协议 (raw/model-user-guide/support/related-agreements.md)](../../raw/model-user-guide/support/related-agreements.md)。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)


