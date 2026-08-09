# support

阿里云百炼平台的 `support` 体系涵盖计费、API/SDK、产品使用、模型能力及法律协议等多个维度，为开发者提供从开通、调用到问题排查的全链路支持。核心支持渠道包括控制台工单、智能在线客服、400电话（4008013260）及7×24小时服务热线（95187），同时明确划定了官方支持边界与第三方工具的责任归属。所有服务均以《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=a2ty02.30260209.aillm.1.d8bb74a10sknig)》为法律基础。

## 支持的模型/功能

- **模型覆盖**：支持千问系列（Qwen-Turbo、Qwen-Plus、Qwen-Max、Qwen3、qwen-plus-latest 等）、Qwen-VL-Plus（支持图像微调）等[多模态](../concepts/multimodal.md)与文本大模型；支持14种语言（含中、英、日、韩、阿拉伯语等）[原文标题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **核心功能**：
  - Completion API 与 Assistant API（当前不支持连续 function call 或 memory 配置）；
  - RAG 增强生成、[插件](../concepts/plugin.md)/MCP 调用、结构化数据对接（RDS 已优先开发，MySQL/Hive 暂不支持）；
  - 模型微调（SFT）、自定义训练集上传（需符合格式规范）、体验中心对话（最多保留100条历史记录）；
- **不支持能力**：万相会员权益不可用于百炼 API 调用；不支持模型导出、隐式标识添加、手机端独立 App；不支持直接对接非阿里云第三方数据库（如 Hive、MySQL）[原文标题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

> **注意**：文档 1 中提到“qwen-plus-latest 属于 Qwen3 系列”，而未提及 Qwen3.5/Qwen3.7 为其子版本；但该表述与常规语义易引发歧义。实际应理解为 qwen-plus-latest 是 qwen-plus 的最新迭代版，与 Qwen3、Qwen3.5、Qwen3.7 并列为独立模型系列 [原文标题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 关键参数

- `doc_reference_type`：仅在旧版应用中生效；新版需在控制台开启「展示回答来源」开关，否则该参数无效；
- `temperature` / `top_p` / `top_k` / `max_tokens`：用于抑制幻觉——降低随机性参数可提升输出稳定性，缩短 `max_tokens` 可防止冗余捏造；
- `RequestId`、`AppId`、`Prompt`、`User`、`Bot`：Completion API 必填字段，缺失或格式错误将返回错误码 `100004`；
- 限流参数：按 RPS/RPM 控制，触发后需等待对应时间窗口（如 120 RPM 下需间隔约 0.8 秒）[原文标题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 使用方式

- **开通服务**：使用阿里云主账号登录百炼控制台，切换目标地域并同意协议；未实名认证用户需先完成[实名认证](https://help.aliyun.com/zh/account/verify-your-identity-individual-account)；
- **API 调用**：推荐使用官方 Python/Java SDK（参见[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)），或直接调用 RESTful 接口（需携带 `Authorization: Bearer <API-Key>`）；
- **问题反馈**：
  - 技术问题 → 提交[阿里云工单](https://smartservice.console.aliyun.com/service/create-ticket)；
  - 产品使用 → 通过[官网-售后服务](https://smartservice.console.aliyun.com/service/robot-chat)；
  - 业务合作 → 拨打 4008013260 或使用[售前咨询](https://smartservice.console.aliyun.com/service/pre-sales-chat)；
- **计费查询**：账单按分钟出账、月度结算；明细与开票均在[费用与成本](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)及[发票管理](https://usercenter2.aliyun.com/invoice/list/aliyun)页面操作。

## 限制和注意事项

- **数据与安全**：所有传输数据经 AES-256 加密；阿里云**不将客户数据用于模型训练**，但依据法规需存储调用日志；具体条款详见[《阿里云百炼服务协议》](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=a2ty02.30260209.aillm.1.d8bb74a10sknig) [原文标题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；
- **服务边界**：
  - 官方售后**不支持**第三方工具（如 Cursor、Windsurf）的部署、配置、故障诊断；
  - 不承担用户本地环境（代理、防火墙、VPN、操作系统）导致的问题；
  - 不提供业务代码编写、定制化集成方案等深度开发支持（需另行订购增值服务）；
- **模型行为**：幻觉属固有风险，可通过更强模型选型、提示词工程、RAG、参数调优等方式缓解，但无法完全消除；
- **协议约束**：SLA、体验功能特别说明、开源模型条款等均纳入法律协议体系，详见[相关协议](../../raw/model-user-guide/support/related-agreements.md)。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)


