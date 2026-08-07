好的，已开启思考模式。
```

## OpenCode

**开启思考模式**：在配置文件`opencode.json`中添加以下内容：

```json
"options": {
  "thinking": {
    "type": "enabled",
    "budget[Token](../concepts/token.md)s": 1024
  }
}
```

> `budget[Token](../concepts/token.md)s` 的值需根据模型支持的最大思维链长度进行调整，详见[OpenCode](https://help.aliyun.com/zh/model-studio/opencode)。

### **Coding Plan 支持哪些模型？**

Coding Plan 支持的模型如下表所示。请务必注意：模型名称必须逐字符完全匹配，版本号/子型号任何差异均视为不支持。

| 模型 | 是否支持视觉理解 |
| --- | --- |
| qwen3.7-plus | ✅ |
| qwen3.6-plus | ✅ |
| kimi-k2.5 | ✅ |
| glm-5 | ❌ |
| MiniMax-M2.5 | ❌ |
| qwen3.5-plus | ✅ |
| qwen3-max-2026-01-23 | ❌ |
| qwen3-coder-next | ❌ |
| qwen3-coder-plus | ❌ |
| glm-4.7 | ❌ |

### **Coding Plan 支持多模态生成吗？**

不支持。Coding Plan 不支持图像、视频等多模态生成模型（如 wan2.7-image、happyhorse-1.1-t2v 等）。如需使用多模态生成能力，请升级至 Token Plan。

### **Coding Plan 支持 Harness 工具吗？**

不支持。Coding Plan 不支持联网搜索、代码解释器等 Harness 工具。如需使用 Harness 工具，请升级至 Token Plan。

### **Coding Plan 支持 MCP 吗？**

不支持。Coding Plan 不支持 MCP（Model Control Protocol）协议。如需使用 MCP 协议，请升级至 Token Plan。

### **Coding Plan 和 Token Plan 的区别是什么？**

| 对比项 | Coding Plan | Token Plan |
| --- | --- | --- |
| **计费方式** | 固定月费 + 请求次数限制 | Credits 统一计量，按模型和工具动态计费 |
| **支持模型** | 千问、GLM、Kimi、MiniMax 等主流文本模型 | 更多模型，包括 Qwen、DeepSeek、HappyHorse、万相等，覆盖文本、图像、视频、语音全模态 |
| **支持功能** | 仅支持文本对话 | 支持 Harness 工具（联网搜索、代码解释器等）、MCP、多模态生成 |
| **适用场景** | 纯文本编程辅助 | 多模态 AI 开发、智能体构建、复杂任务自动化 |

> **推荐**：如需更丰富的模型选择、多模态能力、Harness 工具及 MCP 协议支持，建议使用 Token Plan。

### **Coding Plan Lite 停止新购后，用户如何过渡到 Token Plan？**

Coding Plan Lite 用户可直接购买 Token Plan 个人版或团队版，两者独立计费，无迁移路径。Token Plan 提供更多模型、多模态能力和 Harness 工具支持，是 Coding Plan 的升级替代方案。

### **Coding Plan Pro 是限量抢购，库存售罄后是否还会补充？**

Coding Plan Pro 为限量抢购，库存售罄后不再补充。推荐使用 Token Plan，支持更多模型和 Harness 工具。

### **Coding Plan 的 API Key 能用在 Token Plan 上吗？**

不能。Coding Plan 和 Token Plan 使用不同的 API Key 和 Base URL，不可混用。Token Plan 使用 `sk-sp-` 开头的 Key 和 `token-plan.cn-beijing.maas.aliyuncs.com` 域名，Coding Plan 使用 `sk-sp-` 开头的 Key 和 `coding.dashscope.aliyuncs.com` 域名。

> **注意**：虽然 Key 前缀相同，但域名不同，必须配套使用。

### **Coding Plan 的用量在哪里查看？**

在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan)查看当前订阅的请求额度及消耗情况。

### **Coding Plan 的额度机制是怎样的？**

Coding Plan 采用每 5 小时、每周、每月三重限额，单位为请求次数：

-   **每 5 小时额度**：滚动恢复，每分钟自动释放 5 小时前的额度。
    
-   **每周额度**：每周一 00:00:00（UTC+08:00）重置。
    
-   **每月额度**：在下一个月订阅日的 00:00:00 (UTC+08:00) 重置。
    

### **Coding Plan 的额度用完了怎么办？**

额度用完后调用会被阻断，不会按量计费。恢复方式：

-   等待额度释放。
    
-   升级套餐（Lite → Pro）。
    
-   等待下一周期额度重置。
    

### **Coding Plan 的用量包是什么？**

Coding Plan 不提供用量包。额度用尽后只能等待周期重置或升级套餐。

### **Coding Plan 的并发限制是多少？**

Coding Plan 的并发上限由平台动态分配，高峰时段可能触发限流。具体数值未公开，建议降低请求频率以避免触发限流。

### **Coding Plan 的限流阈值（TPM/RPM）是多少？能否提升？**

官方未公开具体的 TPM/TPS/RPM 数值，限流阈值会根据整体负载动态调整以保障服务稳定性。套餐限流额度不支持提升。

优化建议：精简上下文、降低任务复杂度以减少单次输入 Token 数量；遇到限流时等待约 1 分钟后重试。

### **Coding Plan 的数据使用政策是什么？**

使用 Coding Plan 期间，模型输入以及模型生成的内容将用于服务改进与模型优化。停止使用 Coding Plan 服务可终止后续数据授权，但终止授权的范围不涵盖已授权使用的 Coding Plan 数据。详细条款请参见[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)第 5.2 条。

### **Coding Plan 的账号使用规范是什么？**

套餐为订阅人专享使用，禁止共享。账号共享可能导致订阅权益受限。同一实名认证主体限购一份。

### **Coding Plan 的 RAM 子账号授权步骤是什么？**

RAM 子账号使用 Coding Plan 前，需主账号完成以下授权：

1.  在 RAM 控制台为该 RAM 用户授予 `AliyunCodingPlanReadOnlyAccess`（只读）或 `AliyunCodingPlanFullAccess`（管理）系统策略。
    
2.  在百炼控制台账号管理页面，为该 RAM 用户分配管理员或订阅套餐权限。
    

### **Coding Plan 的续费规则是什么？**

Coding Plan 支持手动续费和自动续费。续费仅延长订阅有效期，不会叠加补充至当前计费周期的额度。

### **Coding Plan 的退订规则是什么？**

Coding Plan 不支持退订。如需取消服务，请等待订阅到期后不再续费。

### **Coding Plan 的学生代金券能用吗？**

不支持。学生代金券仅适用于活动界面指定的产品，不能用于购买 Coding Plan。

### **Coding Plan 的限时优惠是什么？**

首次订阅 Pro 套餐可享首月 ¥39.90（官网目录价 ¥200/月），后续按 ¥200/月 续费。该活动已于 2026 年 4 月 1 日结束。

### **Coding Plan 的地域支持情况如何？**

Coding Plan 目前仅支持华北2（北京）地域。

### **Coding Plan 的 API Key 格式是什么？**

Coding Plan API Key 以 `sk-sp-` 开头，与百炼通用 API Key（`sk-` 开头）格式不同，两者不可混用。

### **Coding Plan 的 Base URL 是什么？**

Coding Plan Base URL 包含 `coding.dashscope.aliyuncs.com`，具体如下：

-   Anthropic 兼容端点：`https://coding.dashscope.aliyuncs.com/apps/anthropic`
    
-   OpenAI 兼容端点：`https://coding.dashscope.aliyuncs.com/v1`
    

### **Coding Plan 的模型 ID 白名单是什么？**

Coding Plan 模型 ID 白名单为精确字符串匹配，必须逐字符完全匹配，版本号/子型号任何差异均视为不支持。完整白名单请参见[Coding Plan 文档](https://help.aliyun.com/zh/model-studio/coding-plan#dc0d98da6ev4j)。

### **Coding Plan 的技术支持渠道是什么？**

如遇问题，请通过[阿里云百炼帮助中心](https://help.aliyun.com/zh/model-studio/)获取支持，或联系阿里云客服。

### **Coding Plan 的产品生命周期是什么？**

Coding Plan Lite 已于 2026 年 3 月 20 日起停止新购，并于 4 月 13 日起停止续费与升级。Coding Plan Pro 为限量抢购，库存售罄后不再补充。推荐使用 [Token](../concepts/token.md) Plan 作为长期替代方案。

### **Coding Plan 的未来规划是什么？**

Coding Plan 将逐步被 Token Plan 替代，未来重点发展 Token Plan，提供更多模型、[多模态](../concepts/multi-modal.md)能力和企业级功能。

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


