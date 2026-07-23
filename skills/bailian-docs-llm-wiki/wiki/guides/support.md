# support

阿里云百炼平台的 `support` 模块涵盖服务开通、计费、API/SDK 使用、模型能力边界、数据安全与合规、售后响应范围等核心支持事项。本文档面向开发者，聚焦可操作的技术支持要点，明确功能边界与限制条件，避免模糊表述或营销性描述。所有引用均指向原始技术文档，确保信息溯源清晰。

## 支持的模型/功能

- **模型调用**：支持千问系列（Qwen-Turbo、Qwen-Plus、Qwen-Max、Qwen3 等）、万相（图像生成）等模型，但需注意：[万相会员](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)不支持百炼 API 调用，其权益与百炼计费体系完全独立。
- **训练与微调**：支持文本及图像（qwen-vl-plus）微调；自定义模型仅支持平台内训练完成的模型二次训练，**不支持本地训练模型上传**；训练完成的开源模型当前**不支持导出**。
- **RAG 与插件**：支持 RAG（[检索增强生成](../concepts/rag.md)）降低幻觉；支持通过插件/MCP 调用外部系统（如数据库），但平台**暂不原生对接 MySQL、Hive 等结构化数据源**，RDS 接入已在开发中。
- **Assistant API**：支持 function call，但**不支持单次请求中依次调用两个本地函数**；当前**暂不支持 memory 配置功能**。

> **注意**：文档 1 中“模型中心”第 10 条称“当前不支持”结构化数据对接，而文档 3 未提及此能力；该限制仍有效，无矛盾。但文档 1 第 17 条明确 `qwen-plus-latest` 属于 Qwen3 系列（非 Qwen3.5/Qwen3.7 子版本），该说明比部分旧版文档更准确，应以该条为准。

## 关键参数

- `doc_reference_type`：仅在旧版本应用中生效；新版本应用需在控制台开启**展示回答来源**开关，否则该参数无效（参见 [FAQ 文档](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)）。
- `temperature` / `top_k` / `top_p` / `max_tokens`：可用于抑制幻觉（降低随机性、限制输出长度），但需权衡创造力与准确性。
- `RequestId`、`AppId`、`Prompt`、`User`、`Bot`：Completion API 必填参数，缺失或格式错误将返回错误码 `100004`（参见 [FAQ 文档](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)）。

## 使用方式

- **开通服务**：需使用阿里云主账号，在目标地域的[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/model-market)开通；若提示“未实名认证”，须先完成[实名认证](https://help.aliyun.com/zh/account/verify-your-identity-individual-account)。
- **API 调用**：推荐使用官方 Python/Java SDK（安装指引见 [安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)）；基础 cURL 示例见 [FAQ 文档](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **问题反馈**：
  - 功能/技术问题 → [官网售后服务](https://smartservice.console.aliyun.com/service/robot-chat?spm=a2cwt.28446455.0.0.5bc14e0btuByqM)；
  - 业务合作 → [阿里云工单](https://smartservice.console.aliyun.com/service/create-ticket?spm=a2c4g.2667824.0.0.6a2f6f83Ivpy5F) 或拨打 4008013260；
  - 计费/开票 → [费用与成本控制台](https://usercenter2.aliyun.com/finance/expense-report/expense-detail) 及 [发票管理](https://usercenter2.aliyun.com/invoice/list/aliyun?pageIndex=1&pageSize=20&ownerId=1990699401005016&invoiceType=aliyun&1990699401005016%23ownerId=1990699401005016)。

## 限制和注意事项

- **数据隐私**：百炼**绝不会将用户数据用于模型训练**；所有传输数据经 AES-256 加密；但根据法规要求，调用日志等数据会被存储，详见 [《阿里云百炼服务协议》](../../raw/model-user-guide/support/related-agreements.md)。
- **历史记录**：控制台体验页最多保留 **100 条历史对话**，无时间限制；未登录状态或推理报错的对话**不保存**。
- **限流策略**：触发限流后，重试等待时间取决于您的 RPS/RPM 配额（例如 120 RPM 下需等待约 0.8 秒）；生成速度受服务负载与并发请求影响，**非固定值**。
- **第三方工具支持边界**：阿里云仅对百炼服务端本身（API 可用性、计费明细、连通性测试）提供支持；**不负责第三方工具（如 Cursor、Windsurf）的安装、配置、故障排查或本地环境（代理/防火墙/VPN）问题**（参见 [售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)）。
- **服务关闭**：百炼服务开通后**暂不支持关闭**；如需停用，建议删除对应地域的 API-Key。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)


