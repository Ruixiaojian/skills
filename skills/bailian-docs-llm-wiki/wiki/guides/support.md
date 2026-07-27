# support

阿里云百炼平台的 `support` 模块涵盖模型服务调用、计费、权限、数据安全及售后响应等全链路支持能力，面向开发者提供标准化 API/SDK 接入、错误诊断与合规保障。所有支持行为均以《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=a2ty02.30260209.aillm.1.d8bb74a10sknig)》和 SLA 为法律与服务基准，不覆盖第三方工具或用户侧环境问题。

## 支持的模型/功能

- **模型类型**：支持千问系列（Qwen-Turbo、Qwen-Max、Qwen-Plus、Qwen-VL-Plus 等）、万相系列及其他第三方模型；其中 Qwen-VL-Plus 支持图片训练微调，但纯文本模型不支持结构化数据库（如 MySQL、Hive）直连，该能力“已在开发中，优先对接 RDS 服务” [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **核心功能**：
  - Completion API（基础文本生成）
  - Assistant API（支持 function call，但**不支持单次调用中依次执行两个本地函数**；当前亦**不支持 memory 配置**）
  - RAG 增强生成（需手动开启“展示回答来源”开关，`doc_reference_type` 参数仅在旧版应用中生效）
  - 模型微调（SFT）、自定义模型训练（仅支持平台内训练产出模型的二次训练，**不支持上传本地训练模型**）

> **注意**：文档 1 中称“qwen-plus-latest 属于 Qwen3 系列”，而文档 1 同时提及“Qwen3.5、Qwen3.7 等是独立并列系列”，该表述存在逻辑矛盾——若 Qwen3.5 是独立系列，则不应归入 Qwen3。实际版本映射应以控制台模型市场实时信息为准，建议通过 [百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all) 查阅具体模型元数据。

## 关键参数

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `temperature` / `top_k` / `top_p` | 控制输出随机性与确定性 | 降低可减少幻觉，但可能削弱创造力；`max_tokens` 过大易引发冗余捏造 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) |
| `doc_reference_type` | 控制答案来源标注方式 | **仅旧版应用生效**；新版需在控制台应用配置中开启“展示回答来源”开关，否则该参数无效 |
| `RequestId`, `AppId`, `User`, `Bot` | Completion API 必填字段 | 缺失或格式错误将返回错误码 `100004`（参数缺失） |

## 使用方式

- **开通服务**：使用阿里云主账号登录 [百炼控制台](https://bailian.console.aliyun.com/?tab=model#/model-market)，切换目标地域后同意协议即可开通；未实名认证需先完成 [实名认证](https://help.aliyun.com/zh/account/verify-your-identity-individual-account)。
- **API 调用**：
  - 必须携带 `Authorization: Bearer <API-Key>` 请求头；
  - SDK 仅官方支持 Java 和 Python，安装方法见 [安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)；
  - 错误码详情请查阅 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code)。
- **售后响应**：
  - 基础服务：7×24 小时电话（95187/4008013260）、智能在线、标准工单；
  - 支持范围包括模型功能咨询、API/SDK 故障诊断、控制台问题、账号与计费问题；
  - **不支持**第三方工具（如 Cursor、Windsurf）部署配置、用户本地环境（代理/防火墙/VPN）、业务代码编写等 [阿里云百炼平台售后服务范围说明 (raw/model-user-guide/support/after-sales-service-scope.md)](../../raw/model-user-guide/support/after-sales-service-scope.md)。

## 限制和注意事项

- **数据与隐私**：
  - 所有传输数据经 AES-256 加密；
  - **阿里云绝不会将您的数据用于模型训练**；
  - 调用日志按法规要求存储，具体条款见 [《阿里云百炼服务协议》](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=a2ty02.30260209.aillm.1.d8bb74a10sknig) [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **计费与额度**：
  - 后付费按分钟出账、按月结算；
  - 开通服务前需确保账户余额 ≥ 0 元；
  - 万相会员权益**不适用于百炼 API 调用**，二者计费体系完全独立。
- **功能限制**：
  - 控制台历史对话最多保留 100 条，无时间限制；未登录状态及推理报错对话不保存；
  - 不支持手机端独立 App，仅 Web 控制台访问；
  - 不支持为生成文本添加隐式标识；
  - 模型训练结果**不支持导出**。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)


