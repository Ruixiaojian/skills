# support

阿里云百炼平台为开发者提供了完善的技术支持体系，涵盖常见问题解答、服务协议、计费说明及联系渠道等内容。本文汇总了平台使用过程中的核心支持信息，帮助开发者快速定位和解决问题。

## 服务开通与基本使用

使用**阿里云主账号**前往百炼控制台（北京或新加坡），阅读并同意协议后即可自动开通服务。开通前需完成实名认证，并确保账户余额不小于 0 元。

- 目前百炼服务开通后**暂不支持关闭**。如需停止调用，可在控制台删除已创建的 API-Key。
- 阿里云百炼是大模型服务平台，提供包括千问系列在内的多种模型，与"千问"本身是平台与模型的关系。
- 如需实现业务数据隔离，可通过主账号为不同子账号授予不同业务空间权限。

## 计费与付费方式

根据 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中的说明，百炼平台的计费要点如下：

| 项目 | 说明 |
|------|------|
| 模型调用 | 按量后付费，按分钟级出账、按月结算 |
| 模型训练/部署 | 另有独立计费方式 |
| 预付费 | 部分模型支持节省计划与资源包 |
| 万相会员 | 与百炼 API 调用计费体系**完全独立**，不可互用 |

扣款明细可在阿里云 [费用与成本](https://usercenter2.aliyun.com/finance/expense-report/expense-detail) 控制台查看，发票通过 [发票管理](https://usercenter2.aliyun.com/invoice/list/aliyun) 页面申请。

## API / SDK 使用要点

### SDK 安装

百炼支持 Java 和 Python 语言的 SDK，详见官方文档 [安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

### 常见调用问题

- **错误码 100004（参数缺失）**：检查必须参数是否完整，以及参数格式是否正确（如 JSON key 的拼写、大小写）。
- **错误码查询**：参见 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code)。
- **`doc_reference_type` 不生效**：该参数仅在旧版应用中有效，新版应用需在操作页面开启"展示答案来源"开关。

### Assistant API 限制

- 不支持在单次调用中分别调用两个本地函数（function call），需手动创建两个 Assistant API 分别处理。
- 当前暂不支持 memory 配置功能。

## 模型选择与训练

### 千问系列模型概况

- 支持 **14 种语言**：中文、英文、阿拉伯语、西班牙语、法语、葡萄牙语、德语、意大利语、俄语、日语、韩语、越南语、泰语、印度尼西亚语。
- 已支持图片训练（qwen-vl-plus 模型支持训练微调）。
- 本地训练的模型**不支持上传**到平台；平台训练完成的模型**不支持导出**。

### 模型选择建议

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| qwen-turbo | 速度快、费用低 | 对响应速度和部署便捷性要求高 |
| qwen-max | 性能强、知识全面 | 对精度和复杂任务处理能力要求高 |

### 训练最佳实践

根据 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中模型中心部分的说明：

1. **数据质量优先**：答案应准确、简洁，避免冗余；同一语义用多种 [prompt](prompt.md) 表达以提升多样性。
2. **避免灾难性遗忘**：仅用垂直领域数据做 SFT 可能导致模型遗忘通用知识。
3. **超参数调优**：循环次数无固定规律，需根据具体任务实验确定。数据量少时可适当增加循环次数，数据量大时需警惕过拟合。
4. **评估方式**：不应仅通过 loss 判断过拟合，最终效果以人工评估为准。

## 模型幻觉处理

降低模型幻觉的推荐方法（按实施难度排序）：

1. **选择更强模型**：Max > Plus > Turbo。
2. **提示词工程**：添加约束指令，如"仅基于提供的文档回答"。
3. **RAG（检索增强生成）**：让模型回复基于检索到的知识。
4. **插件 / MCP**：将数值计算等任务交给外部工具完成。
5. **调低随机性参数**：降低 `temperature`、`top_k`、`top_p`，降低 `max_tokens` 可防止模型在关键信息后继续捏造。
6. **后处理验证**：用 AI 校验回答的正确性（会增加成本和延迟）。

## 限流与性能

- 模型生成速度**不固定**，受服务整体负载和请求并发影响。
- 限流触发后的等待时间取决于具体限流值（RPS/RPM）。例如 120 RPM 限流下，0.2 秒内提交 2 次请求后，第 3 次需等待约 0.8 秒。

## 数据安全与合规

- 阿里云**不会**将用户数据用于模型训练。
- 传输数据使用 AES-256 加密。
- 根据法律法规要求，百炼将存储模型与应用调用时产生的数据，具体条款见服务协议。
- 控制台最多展示 100 条历史对话记录，不设时间限制；未登录体验及推理报错的对话不保存。

## 相关协议

根据 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 页面，使用百炼平台前应了解以下协议：

- [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html)
- [阿里云百炼模型推理服务等级协议（SLA）](https://terms.alicdn.com/legal-agreement/terms/b_end_product_protocol/20250923215800868/20250923215800868.html)
- [阿里云百炼服务特别说明](https://help.aliyun.com/zh/model-studio/bailian-service-notes)
- [开源模型协议条款说明](https://help.aliyun.com/zh/model-studio/open-source-model-terms)
- [三方模型服务协议和使用条款清单](https://terms.alicdn.com/legal-agreement/terms/common_product_agreement/20260207131114217/20260207131114217.html)

## 联系方式

| 场景 | 渠道 |
|------|------|
| 业务合作 | 服务热线 4008013260 或 [官网-售前咨询](https://smartservice.console.aliyun.com/service/pre-sales-chat) |
| 产品使用问题 | [官网-售后服务](https://smartservice.console.aliyun.com/service/robot-chat) |
| 合作协议申请 | 提交 [阿里云工单](https://smartservice.console.aliyun.com/service/create-ticket) |

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)

