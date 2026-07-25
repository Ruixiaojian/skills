# support

阿里云百炼平台的 `support` 模块涵盖售后服务范围、计费与API问题响应、模型使用咨询及合规协议等完整支持体系。开发者可通过标准工单、智能在线、7×24电话（95187/400）获取基础技术支持，同时需明确区分阿里云百炼平台自身责任边界与第三方工具、用户侧环境的责任归属。所有服务均以[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)为法律基准。

## 支持的模型/功能

- **模型覆盖**：支持千问系列（Qwen-Turbo、Qwen-Max、Qwen-Plus、Qwen-VL-Plus等）、万相系列及其他接入百炼平台的开源与三方模型；其中 Qwen-VL-Plus 已支持图片训练微调 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **核心功能支持**：
  - 模型调用（Completion / Assistant API）、RAG 应用构建、自定义模型微调（SFT）、[模型部署](../concepts/model-deployment.md)与推理；
  - 控制台操作（业务空间权限管理、API-Key 管理、模型体验中心）、计费查询与开票；
  - 数据隔离（通过主账号/子账号+业务空间实现）、AES-256 加密传输与存储。
- **不支持场景**：  
  > **注意**：万相会员权益**不支持百炼API调用**，二者计费体系完全独立 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；  
  > **注意**：当前**不支持直接对接 MySQL/Hive 等结构化数据库**，RDS 对接正在开发中 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 关键参数

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `temperature` / `top_p` / `top_k` | 控制生成随机性与多样性 | 降低 `temperature` 可减少幻觉，但可能削弱创造力；`doc_reference_type` 仅在旧版应用生效，新版需在控制台开启「展示回答来源」开关 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) |
| `max_tokens` | 限制输出长度 | 过长易引发幻觉续写，建议按实际需求设合理上限 |
| `RequestId` / `AppId` / `Authorization` | API 必填字段 | 缺失或格式错误将返回错误码 `100004`（参数缺失），需严格按示例校验 JSON 结构与 Header [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) |

## 使用方式

- **基础支持渠道**（免费）：
  - 7×24 电话：95187（阿里云客服）、400-801-3260（售前）；
  - 在线：[官网售后服务入口](https://smartservice.console.aliyun.com/service/robot-chat)、阿里云APP、智能在线机器人；
  - 工单：通过[阿里云工单系统](https://smartservice.console.aliyun.com/service/create-ticket)提交技术问题。
- **增值服务**：付费支持计划（含专属客户经理、SLA 保障等），详情见[客户服务权益](https://www.aliyun.com/service/customer-service-benefits)。
- **自助资源**：
  - 错误码排查：[错误码文档](https://help.aliyun.com/zh/model-studio/error-code)；
  - SDK 安装：支持 Python/Java，参见[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)；
  - 计费查询：[费用与成本控制台](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)；
  - 协议查阅：所有法律条款集中于[相关协议](../../raw/model-user-guide/support/related-agreements.md)。

## 限制和注意事项

- **责任边界明确**：
  - 阿里云百炼仅保障自身服务端（API 接口、计量计费、控制台、模型推理服务）的可用性与稳定性；
  - **不支持**：第三方工具（如 Cursor、Windsurf）的部署/配置/故障诊断；用户本地环境（代理、防火墙、VPN、OS 兼容性）问题；业务代码编写与调试；非百炼服务导致的 [Token](../concepts/token.md)/费用统计差异解释 [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)。
- **数据与合规**：
  - 所有调用数据经 AES-256 加密，**绝不用于模型再训练**；
  - 历史对话记录在控制台最多保留 100 条，未登录状态及推理报错对话不保存；
  - 数据存储与处理条款详见[《阿里云百炼服务协议》](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=a2ty02.30260209.aillm.1.d8bb74a10sknig)。
- **其他限制**：
  - 百炼服务开通后**暂不支持关闭**，如需停用，须删除对应地域的 API-Key；
  - 训练完成的开源模型**不支持导出**；
  - Assistant API 当前**不支持 memory 配置**，且 function call 不支持单次调用多个本地函数。

## 来源文档

- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)
- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)


