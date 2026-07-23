# support

阿里云百炼平台的 `support` 体系涵盖计费、API/SDK、产品使用、模型能力及法律合规等多个维度，为开发者提供从开通、调用到问题排查的全链路支持。核心支持渠道包括控制台、官方文档、错误码中心、工单系统及7×24小时客服（95187/4008013260）。所有服务均以《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=a2ty02.30260209.aillm.1.d8bb74a10sknig)》为法律基础，数据隐私与安全严格遵循协议约定 [原文标题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 支持的模型/功能

- **模型类型**：支持千问系列（Qwen-Turbo、Qwen-Max、Qwen-Plus、Qwen-VL-Plus等）、万相（图像生成）及其他第三方模型；Qwen-VL-Plus 已支持图片微调训练 [原文标题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **语言支持**：千问系列支持中文、英文、阿拉伯语、西班牙语等共14种语言。
- **关键能力**：
  - RAG（[检索增强生成](../concepts/rag.md)）：可显著降低幻觉，需配合高质量检索系统与来源标注；
  - Function Calling：当前**不支持单次调用中依次执行多个本地函数**，需拆分为多个 Assistant API 实例 [原文标题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；
  - Memory：Assistant API 当前**暂不支持 memory 配置功能**；
  - 结构化数据对接：当前**不支持直接对接 MySQL/Hive 等外部数据库**，RDS 接入正在开发中。

> **注意**：文档1中提及“qwen-plus-latest 属于 Qwen3 系列”，但未明确其与 Qwen3.5/Qwen3.7 的关系；而实际模型命名体系中 Qwen3.5、Qwen3.7 为独立并列系列，并非 Qwen3 子版本——该表述易引发歧义，应以控制台模型市场实时展示为准。

## 关键参数

- `doc_reference_type`：仅在旧版应用中生效；新版应用需在控制台开启「展示回答来源」开关，否则该参数无效 [原文标题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- `temperature` / `top_k` / `top_p`：用于抑制幻觉，降低值可使输出更保守（但可能牺牲多样性）。
- `max_tokens`：合理设置可防止模型在关键信息后继续捏造内容。
- 必填参数（Completion API）：`AppId`、`Prompt`、`RequestId`、`User`、`Bot`；缺失或格式错误将返回错误码 `100004`。

## 使用方式

- **开通服务**：需使用阿里云主账号，在目标地域的[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/model-market)开通；未实名认证用户需先完成[实名认证](https://help.aliyun.com/zh/account/verify-your-identity-individual-account)。
- **API 调用**：
  - 支持 Python/Java SDK，安装指引见[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)；
  - 请求示例需严格遵循 JSON 格式与 Header（含 `Authorization: Bearer <token>`）；
  - 错误码详情请查阅[错误码文档](https://help.aliyun.com/zh/model-studio/error-code)。
- **售后支持渠道**：
  - 基础服务：7×24 小时电话（95187、4008013260）、智能在线、标准工单；
  - 技术问题诊断范围覆盖 API/SDK、控制台、账号、计费等 [原文标题](../../raw/model-user-guide/support/after-sales-service-scope.md)；
  - 业务合作类需求请提交[阿里云工单](https://smartservice.console.aliyun.com/service/create-ticket?spm=a2c4g.2667824.0.0.6a2f6f83Ivpy5F)。

## 限制和注意事项

- **数据隔离**：通过业务空间（Business Space）实现租户级数据隔离，子账号权限需按空间粒度授权 [原文标题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **数据留存**：
  - 控制台体验对话最多保留 **100 条历史记录**，无时间限制；未登录或推理报错对话不保存；
  - 所有调用数据经 AES-256 加密传输，**绝不用于模型训练**，但依法依规存储用于服务审计与合规要求。
- **第三方工具支持边界**：
  - 阿里云仅对百炼服务端状态、API 可达性、调用明细提供支持；
  - **不承担第三方工具（如 Cursor、Windsurf 等）的安装、配置、故障排查责任**，也不对其显示的 [Token](../concepts/token.md)/费用统计差异负责 [原文标题](../../raw/model-user-guide/support/after-sales-service-scope.md)。
- **其他限制**：
  - 万相会员权益**不适用于百炼 API 调用**，二者计费体系完全独立；
  - 自定义模型仅支持平台内训练产出模型的二次微调，**不支持上传本地训练模型**；
  - 训练完成的开源模型**暂不支持导出**。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)


