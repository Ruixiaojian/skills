# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理能力集合，涵盖新人免费额度、按量调用、模型训练/部署、成本优化（节省计划/资源包）及账单治理等全链路能力。其设计目标是为开发者提供透明、可控、可预测的模型服务使用成本模型，支持从试用到规模化生产的平滑演进。所有能力均以华北2（北京）地域为默认基准，跨地域使用需注意价格与额度差异。

## 支持的模型/功能

- **实时推理**：支持千问（Qwen）、GLM、DeepSeek、Kimi 等主流文本生成模型，以及万相（图像/视频生成）、CosyVoice（语音合成）等多模态模型，全部按输入/输出 Token 或等效计量单位计费 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **模型训练**：支持文本（千问）、图像（万相）、视频（万相）、语音（CosyVoice）四类模型的微调，计费基于训练 Token 总量或视频时长×像素数×轮次等复合公式 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **模型部署**：提供两种计费模式：**预置吞吐**（按 TPM × 时长）和**模型单元**（按算力规格 × 小时），适用于不同负载场景 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **成本优化工具**：包括 AI 通用型节省计划（跨模型抵扣）、模型专属节省计划（如千问语音、万相）、资源包（指定模型 Token 预购）三类方案，覆盖按量付费全场景 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

> **注意**：文档 5 中 `qwen3.7-max` 在华北2（北京）标注“当前能力等同于 `qwen3.7-max-2026-05-20`”，而文档 2 的部署计费表中仅列出 `qwen3.7-max-2026-05-20`，未提及其别名。实际调用时应以控制台模型广场展示的 Model ID 为准，避免因别名映射不一致导致计费偏差。

## 关键参数

- **免费额度**：默认 100 万 Token/模型，仅限华北2（北京）地域的实时推理调用，有效期 90 天（自开通/模型发布/申请通过日起较晚者计算），不同模型（含快照版本）额度完全独立 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **Token 计费粒度**：输入/输出 Token 均按百万为单位计价，部分模型（如 `qwen3-max`）实行阶梯计费，单价取决于单次请求的输入 Token 总量区间 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **抵扣优先级**：系统严格按 `免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费` 顺序抵扣费用，该逻辑贯穿所有计费场景 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **账单延迟**：模型推理账单为分钟级出账（通常 2–10 分钟），训练/批量/知识库类账单为小时级出账，高峰期可能进一步延迟 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 使用方式

1. **开通与初始化**：首次访问华北2（北京）地域百炼控制台并同意协议后，系统自动发放免费额度，无需额外操作 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
2. **API 调用**：使用通用 API Key（非 Token Plan/Coding Plan 专属 Key）发起 HTTP 请求，系统自动按优先级抵扣额度；若需强制使用节省计划，须确保已关闭对应模型的“免费额度用完即停”功能 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
3. **成本配置**：
   - 开启“免费额度用完即停”防止意外扣费；
   - 购买 AI 通用型节省计划（推荐）或资源包，通过控制台或 OpenAPI 绑定；
   - 为业务空间绑定标签，实现分账管理 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
4. **账单监控**：通过控制台「费用概览」查看月度总消费，通过「账单详情」下载明细并解析 `实例 ID（出账粒度）` 字段（格式：`ApiKeyID;业务空间ID;模型名称;...`）定位具体费用来源 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **地域限制**：免费额度、部分模型训练（如 CosyVoice）及多数部署选项仅在华北2（北京）可用；跨地域调用将产生全额计费且无额度抵扣 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **功能排除**：免费额度**不覆盖** Batch 调用、模型训练、模型部署、自定义模型（调优后/已部署）等场景，此类操作直接按量计费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费影响**：账户欠费时，**所有按量付费服务（含仍有剩余额度的模型）将立即暂停**，必须结清欠费才能恢复；Coding Plan/Token Plan 等预付费产品不受影响 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **额度时效性**：控制台显示的免费额度为分钟级更新，需手动刷新页面获取最新余量；若页面显示有余额但调用失败，应首先检查账户是否欠费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


