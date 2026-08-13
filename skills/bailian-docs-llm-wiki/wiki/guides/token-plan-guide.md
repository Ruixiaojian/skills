```

## OpenCode

**开启思考模式**：在配置文件`opencode.json`中，为对应模型添加以下配置：

```json
"options": {
  "thinking": {
    "type": "enabled",
    "budget[Token](../concepts/token.md)s": 1024
  }
}
```

> `budget[Token](../concepts/token.md)s` 表示思考链的最大 Token 数量，可根据任务复杂度调整。

### **Coding Plan 是否支持多模态？**

Coding Plan 支持部分多模态模型（如 qwen3.7-plus、qwen3.6-plus、kimi-k2.5），但不支持图像生成、视频生成等 AIGC 多模态模型。如需使用文生图、文生视频等功能，请使用 Token Plan。

### **Coding Plan 是否支持 Harness 工具？**

Coding Plan 不支持 Harness 工具（联网搜索、代码解释器、网页抓取等）。如需使用 Harness 工具，请使用 Token Plan。

### **Coding Plan 是否支持 MCP？**

Coding Plan 不支持 MCP（Model Calling Protocol）协议。如需使用 MCP 协议调用外部工具，请使用 Token Plan。

### **Coding Plan 是否支持自定义模型？**

Coding Plan 不支持用户上传或部署自定义模型。仅支持套餐白名单内的模型。

### **Coding Plan 是否支持 API 调用？**

Coding Plan 仅限在编程工具（如 Claude Code、Qoder、Qoder CN、OpenClaw 等）中使用，禁止以 API 调用的形式用于自动化脚本、自定义应用程序后端或任何非交互式批量调用场景。将套餐 API Key 用于允许范围之外的调用将被视为违规或滥用，可能会导致订阅被暂停或 API Key 被封禁。

### **Coding Plan 是否支持 RAM 子账号？**

支持。RAM 子账号使用 Coding Plan 前，需由主账号完成以下授权：

1.  在 [RAM 控制台](https://ram.console.aliyun.com/)为该 RAM 用户授予 `Aliyun[Token](../concepts/token.md)PlanReadOnlyAccess`（只读）或 `AliyunTokenPlanFullAccess`（管理）系统策略，同时授予 `AliyunBSSReadOnlyAccess` 系统策略。
    
2.  在百炼控制台[账号管理](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/uac-admin/organization/members/list)页面，为该 RAM 用户分配管理员或订阅套餐权限。
    

### **Coding Plan 是否支持学生代金券购买？**

不支持。学生代金券无法用于购买 Coding Plan。

### **Coding Plan 是否支持免费试用额度或赠送 Token？**

Coding Plan 套餐本身不提供试用额度，也不包含免费赠送的 Token 额度。百炼平台针对部分模型提供独立的免费额度，可以在控制台查询可用免费额度的模型列表。

### **Coding Plan 的用量在哪里查看？**

在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan)可以查看用量。

### **Coding Plan 是否支持退订？**

Coding Plan 不支持退订。如需停止服务，请等待订阅到期后不再续费。

### **Coding Plan 是否支持自动续费？**

支持。您可在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan)开启或关闭自动续费。

### **Coding Plan 是否支持升配？**

Coding Plan Lite 套餐已停止新购和续费，当前仅 Pro 套餐可购买。Lite 套餐不支持升级至 Pro 套餐，Pro 套餐暂不支持升级。

### **Coding Plan 是否支持降配？**

不支持降配。如需更换为更低档位，可在订阅到期后重新购买。

### **Coding Plan 是否支持按年订阅？**

不支持按年订阅。Coding Plan 仅支持按月订阅。

### **Coding Plan 是否支持多设备使用？**

支持。同一账号可在多台设备上使用同一个 API Key，无需为每台设备重新生成。

### **Coding Plan 是否支持多人共用一个账号？**

不可以。Coding Plan 限单人使用，不允许多人共用同一账号或 API Key。如需多人协作，请使用 Token Plan 团队版。

### **Coding Plan 是否支持团队管理？**

不支持团队管理。如需团队协作，请使用 Token Plan 团队版。

### **Coding Plan 是否支持数据安全承诺？**

Coding Plan 未明确承诺不使用对话数据训练模型。如需企业级数据安全保障，请使用 Token Plan 团队版。

### **Coding Plan 是否支持 SSO 或钉钉接入？**

不支持 SSO 或钉钉接入。如需企业身份集成，请使用 Token Plan 团队版。

### **Coding Plan 是否支持用量分析？**

不支持用量分析。如需详细用量监控，请使用 Token Plan 团队版。

### **Coding Plan 是否支持共享用量包？**

不支持共享用量包。如需弹性扩容，请使用 Token Plan 团队版的共享用量包。

### **Coding Plan 是否支持并发限制？**

Coding Plan 存在并发限制。平台会根据整体资源负载动态调整并发上限，避免高峰时段资源过载，确保每个 Agent 获得稳定的响应速度和推理质量。触发并发限制时，等待片刻后重试即可。

### **Coding Plan 是否支持高峰期性能保障？**

Coding Plan 在高峰期可能出现排队等待。如需更稳定的吞吐，可使用 Token Plan 团队版。

### **Coding Plan 是否支持 RAM 子账号购买？**

支持。RAM 子账号使用前，需主账号完成以下授权：

1.  在 RAM 控制台为该 RAM 用户授予 `AliyunTokenPlanReadOnlyAccess`（只读）或 `AliyunTokenPlanFullAccess`（管理）系统策略。
    
2.  在百炼控制台账号管理页面，为该 RAM 用户分配管理员或订阅套餐权限。
    

**说明**

RAM 子账号授权与**席位分配**是两个独立的概念：RAM 授权决定谁可以在阿里云控制台**管理**（购买、续费、配置）Coding Plan 订阅；席位分配决定谁可以**使用**模型（获得 API Key）。即使 RAM 子账号拥有管理权限，团队成员仍需通过[团队管理](https://help.aliyun.com/zh/model-studio/token-plan-team-management)中的**添加成员并分配席位**操作才能获得 API Key 并调用模型。

### **Coding Plan 是否支持限时优惠？**

Coding Plan Pro 套餐为限量抢购，库存售罄后不再补充。推荐使用 **Token Plan**，支持更多模型和 Harness 工具。

### **Coding Plan 是否支持免费额度？**

Coding Plan 套餐本身不提供试用额度，也不包含免费赠送的 Token 额度。百炼平台针对部分模型提供独立的免费额度，可以在控制台查询可用免费额度的模型列表。

### **Coding Plan 是否支持学生代金券？**

不支持。学生代金券无法用于购买 Coding Plan。

### **Coding Plan 是否支持退款？**

Coding Plan 服务**不支持退款**。因此在订阅前请知悉以下重要内容：

1.  **严禁 API 调用**：仅限在编程工具（如 Claude Code、Qoder、Qoder CN、OpenClaw 等）中使用，禁止以 API 调用的形式用于自动化脚本、自定义应用程序后端或任何非交互式批量调用场景。**将套餐 API Key 用于允许范围之外的调用将被视为违规或滥用，可能会导致订阅被暂停或 API Key 被封禁。**
    
2.  **数据使用授权**：使用 Coding Plan 期间，模型输入以及模型生成的内容将用于服务改进与模型优化。停止使用 Coding Plan 服务可终止后续数据授权，但终止授权的范围不涵盖已授权使用的 Coding Plan 数据。详细条款请参见[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)第 5.2 条。
    
3.  **账号使用规范**：套餐为订阅人专享使用，禁止共享。账号共享可能导致订阅权益受限。
    
4.  **速率与资源调度说明**：为保障全体用户的公平使用，除上述额度上限外，本服务对单账号的并发请求数与单位时间请求速率设有技术上限；在平台整体负载较高，或单账号短时间内资源占用异常集中时，我们可能对该账号的请求进行临时排队、降速或短时中断，相关调节通常在数分钟至数小时内自动解除。上述调节属于服务的正常技术保障措施，不视为服务中断或违约。具体阈值属平台安全与稳定性策略，可能根据运行情况动态调整。
    

---

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-for-coding-plan.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)


