# support

阿里云百炼平台的 `support` 指代面向开发者的一整套服务支持体系，涵盖技术咨询、故障排查、计费与合规、协议保障及售后响应机制。该体系以自助文档、自动化工具和人工通道为支撑，核心目标是保障模型调用与应用开发的稳定性与可预期性。所有支持能力均基于百炼平台的服务边界定义，不延伸至第三方工具或用户侧基础设施。

## 支持的模型/功能

- **模型覆盖**：支持千问系列（Qwen-Max、Qwen-Plus、Qwen-Turbo、Qwen-VL-Plus 等）、万相系列及其他接入百炼平台的第三方模型；其中 Qwen-VL-Plus 支持图文[多模态](../concepts/multi-modal.md)微调 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **核心功能支持**：
  - Completion API 与 Assistant API 的基础调用与错误诊断；
  - RAG 应用构建、知识库配置与 `doc_reference_type` 参数行为（仅旧版应用生效）；
  - 模型训练（SFT/RLHF）、微调及效果评估；
  - 业务空间权限隔离与子账号数据隔离策略；
  - 模型体验中心的历史对话管理（最多保留 100 条，未登录/报错对话不保存）。

> **注意**：文档中提及“Assistant API 当前暂不支持 memory 配置功能”与部分 SDK 示例中隐含的上下文保持逻辑存在潜在冲突；实际行为以 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中明确说明为准——即无原生 memory 能力，需由应用层自行维护会话状态。

## 关键参数

- `doc_reference_type`：仅在旧版本应用中生效；新版本需通过控制台开启「展示回答来源」开关，否则该参数无效 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- `temperature` / `top_p` / `top_k` / `max_tokens`：用于抑制幻觉、控制输出确定性与长度，属通用推理参数，适用于所有支持 Completion 的模型。
- `RequestId`、`AppId`、`User`、`Bot`：Completion API 必填字段，缺失或格式错误将返回错误码 `100004` [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 使用方式

- **自助支持**：
  - 错误码查询：参考 [错误码](https://help.aliyun.com/zh/model-studio/error-code) 文档；
  - SDK 安装：官方提供 Python 和 Java SDK，详见 [安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)；
  - 模型体验：通过 [模型体验中心（北京）](https://bailian.console.aliyun.com/?&tab=model#/efm/model_experience_center/text) 或新加坡地域入口快速验证。
- **人工支持**：
  - 基础服务：7×24 小时电话（95187 / 4008013260）、智能在线客服、标准工单；
  - 支持范围包括产品功能咨询、API/SDK 故障诊断、控制台问题、账号与计费问题等，详见 [阿里云百炼平台售后服务范围说明 (raw/model-user-guide/support/after-sales-service-scope.md)](../../raw/model-user-guide/support/after-sales-service-scope.md)；
  - 售后增值服务（如支持计划）需另行订购。

## 限制和注意事项

- **服务开通与关闭**：百炼服务按地域开通，开通后不可关闭；如需停用，须删除对应地域的 API-Key [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **第三方工具免责**：阿里云不承担 Cursor、Windsurf 等第三方工具的安装、配置、兼容性或运维责任；仅提供百炼 API 可达性、调用示例及计费核查等方向性建议 [阿里云百炼平台售后服务范围说明 (raw/model-user-guide/support/after-sales-service-scope.md)](../../raw/model-user-guide/support/after-sales-service-scope.md)。
- **数据与合规**：
  - 所有调用数据经 AES-256 加密传输，但根据法规要求会被存储；严禁用于模型再训练 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；
  - 万相会员权益不适用于百炼 API 调用，二者计费体系完全独立；
  - 协议依据以 [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=a2c4g.2667824.0.0.6a2f6f83Ivpy5F) 及 [SLA](https://terms.alicdn.com/legal-agreement/terms/b_end_product_protocol/20250923215800868/20250923215800868.html) 为准 [相关协议 (raw/model-user-guide/support/related-agreements.md)](../../raw/model-user-guide/support/related-agreements.md)。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)


