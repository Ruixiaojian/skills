# support

阿里云百炼平台的 `support` 体系涵盖计费咨询、API/SDK 技术支持、产品使用答疑、法律协议保障及售后服务范围界定。开发者可通过多渠道获取基础支持，但需注意服务边界（如第三方工具、本地环境问题不属标准支持范围）。所有服务均以阿里云官方文档与协议为最终依据。

## 支持的模型/功能

- **模型调用**：支持千问系列（Qwen-Turbo、Qwen-Plus、Qwen-Max、Qwen3 等）、qwen-vl-plus（支持图文训练）等主流模型，具体模型列表及能力详见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)；  
- **核心功能**：Completion API、Assistant API（当前不支持连续 function call 或 memory 配置）、RAG 应用构建、模型微调（SFT）、结构化数据对接（RDS 正在开发中，暂不支持 MySQL/Hive）；  
- **体验与调试**：提供模型体验中心（北京/新加坡）、100 条历史对话记录保留（未登录或报错对话不保存），但**不支持隐式标识添加**；  
- **数据隔离**：通过业务空间（Business Space）实现子账号级数据隔离，不同空间数据互不影响 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 关键参数

- `doc_reference_type`：仅在旧版应用中生效；新版需在控制台开启「展示回答来源」开关，否则该参数无效；  
- `temperature` / `top_p` / `top_k` / `max_tokens`：可用于抑制幻觉（如降低 `temperature` 提高确定性），但需权衡生成质量与多样性；  
- `RequestId`、`AppId`、`Prompt`、`User`、`Bot`：Completion API 必填字段，缺失或格式错误将返回错误码 `100004` [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；  
- > **注意**：文档 1 中提及“Assistant API 当前暂不支持 memory 配置”，但未说明未来是否支持；而文档 3 未涉及此功能定义，建议以最新控制台配置和 SDK 文档为准。

## 使用方式

- **开通服务**：需使用阿里云主账号，在目标地域（如北京、新加坡）控制台开通；未实名认证用户需先完成[实名认证](https://help.aliyun.com/zh/account/verify-your-identity-individual-account)；  
- **API 调用**：推荐使用 Python/Java 官方 SDK（安装指引见[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)），或直接调用 RESTful 接口（需携带 `Authorization: Bearer <API-Key>`）；  
- **错误排查**：所有 API 错误码含义及解决方案统一归集于[错误码](https://help.aliyun.com/zh/model-studio/error-code)文档；  
- **售后入口**：  
  - 技术问题 → [官网-售后服务](https://smartservice.console.aliyun.com/service/robot-chat)；  
  - 业务合作 → [官网-售前咨询](https://smartservice.console.aliyun.com/service/pre-sales-chat) 或拨打 4008013260；  
  - 计费与开票 → [费用与成本控制台](https://usercenter2.aliyun.com/finance/expense-report/expense-detail) 及 [发票管理](https://usercenter2.aliyun.com/invoice/list/aliyun)；  
- **法律依据**：服务协议、SLA、开源模型条款等详见[相关协议 (raw/model-user-guide/support/related-agreements.md)](../../raw/model-user-guide/support/related-agreements.md)。

## 限制和注意事项

- **服务不可关闭**：百炼服务开通后无法主动关闭，仅能通过删除 API-Key 阻断调用；  
- **计费模式**：后付费按分钟出账、月度结算；预付费需购买[节省计划与资源包](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package)；万相会员**不支持**百炼 API 调用 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；  
- **数据安全**：调用数据经 AES-256 加密传输，阿里云**绝不用于模型训练**，但依法依规存储调用日志（详见《阿里云百炼服务协议》）；  
- **第三方工具支持边界**：阿里云仅提供百炼侧接口连通性、调用示例及计费核查支持，**不负责**第三方工具（如 Cursor、Windsurf）的部署、配置、故障诊断或本地网络/代理/防火墙问题排查 [阿里云百炼平台售后服务范围说明 (raw/model-user-guide/support/after-sales-service-scope.md)](../../raw/model-user-guide/support/after-sales-service-scope.md)；  
- **模型幻觉应对**：无绝对消除方案，推荐组合策略：选用高阶模型（如 Qwen-Max）、优化 [prompt](prompt.md)、启用 RAG、调低随机性参数，并辅以后处理验证。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)


