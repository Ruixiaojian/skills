# support

阿里云百炼平台的 `support` 模块涵盖服务开通、计费、API/SDK 使用、模型能力边界及合规协议等核心支持事项。它面向开发者提供可落地的技术指引与约束说明，而非泛泛的服务承诺。所有功能与限制均以控制台实际行为和最新 API 文档为准，历史文档中未同步更新的内容需谨慎参考。

## 支持的模型/功能

- **模型类型**：支持千问系列（Qwen-Turbo、Qwen-Max、Qwen3、Qwen-VL-Plus 等）、开源模型及第三方模型；其中 Qwen-VL-Plus 已支持图片训练 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **核心能力**：
  - Completion API（基础文本生成）
  - Assistant API（支持 function call，但**不支持连续调用多个本地函数**；当前**不支持 memory 配置**）
  - RAG 增强（通过 `doc_reference_type` 参数或应用配置中的“展示回答来源”开关控制答案溯源，该参数仅在旧版应用中生效 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)）
- **数据对接**：当前**不支持直接对接 MySQL、Hive 等结构化数据源**，RDS 接入正在开发中。

## 关键参数

| 参数名 | 说明 | 注意事项 |
|--------|------|----------|
| `temperature` / `top_k` / `top_p` | 控制输出随机性与确定性 | 降低这些值可抑制幻觉，但可能削弱创造性；需结合任务人工评估效果 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) |
| `max_tokens` | 限制响应长度 | 过长易引发后半段捏造，适当截断可缓解幻觉 |
| `doc_reference_type` | 控制答案来源标注方式 | **仅在旧版本应用中生效**；新版本需在应用配置中开启“展示回答来源”开关，否则该参数无效 |

> **注意**：文档 1 中提到“Assistant API 有 memory 相关的能力吗？当前暂不支持”，而部分早期 SDK 示例曾隐含 session state 语义，该能力**已明确废弃且无替代方案**，开发者须自行维护上下文。

## 使用方式

- **服务开通**：需使用阿里云主账号，在目标地域（如北京、新加坡）的[百炼控制台](https://bailian.console.aliyun.com/)开通；未实名认证将被拦截 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **API 调用**：
  - 必须携带 `Authorization: Bearer <API-Key>` 及 `AppId`、`Prompt` 等必需字段；
  - 错误码 `100004` 表示参数缺失或格式错误，需严格校验 JSON 结构与字段命名；
  - SDK 仅官方支持 Python 和 Java，安装方式见[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。
- **计费与资源管理**：
  - 后付费按分钟出账、按月结算；
  - 部分模型支持预付费（节省计划/资源包），详情见[节省计划与资源包](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package)；
  - 万相会员**不支持百炼 API 调用**，二者计费体系完全独立。

## 限制和注意事项

- **数据与隐私**：
  - 所有传输数据经 AES-256 加密；
  - 阿里云**不会将用户数据用于模型训练**；
  - 模型与应用调用日志依法律法规留存，具体条款见[《阿里云百炼服务协议》](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=a2ty02.30260209.aillm.1.d8bb74a10sknig) [相关协议 (raw/model-user-guide/support/related-agreements.md)](../../raw/model-user-guide/support/related-agreements.md)。
- **功能限制**：
  - 百炼控制台最多保留 **100 条历史对话记录**（未登录或推理报错对话不保存）；
  - 不支持为生成文本添加隐式标识；
  - 无官方手机端应用，仅支持 Web 访问；
  - 自定义模型训练完成后**不支持导出**。
- **SLA 与合规**：
  - 服务可用性、响应延迟等承诺详见[阿里云百炼模型推理服务等级协议（SLA）](https://terms.alicdn.com/legal-agreement/terms/b_end_product_protocol/20250923215800868/20250923215800868.html) [相关协议 (raw/model-user-guide/support/related-agreements.md)](../../raw/model-user-guide/support/related-agreements.md)；
  - 应用上架需完成[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)，合作协议需通过工单申请。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)


