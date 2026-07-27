Thinking...
```

## OpenCode

**开启思考模式**：在配置文件`opencode.json`中添加如下配置：

```json
"options": {
  "thinking": {
    "type": "enabled",
    "budget[Token](../concepts/token.md)s": 1024
  }
}
```

**查看思考过程**：使用快捷键 `Ctrl + O` 可查看思考过程。

## Qwen Code

**开启思考模式**：输入`/config`，移动到`Thinking mode`，通过`Enter`切换为`true`开启思考模式。

**查看思考过程**：使用快捷键 `Ctrl + O` 可查看思考过程。

### **Coding Plan 支持的模型有哪些？**

Coding Plan 支持的模型请参见[Coding Plan](https://help.aliyun.com/zh/model-studio/coding-plan#dc0d98da6ev4j)文档中的“支持的模型”章节。该列表为精确字符串白名单，必须逐字符完全匹配，版本号/子型号任何差异均视为不支持。

### **Coding Plan Lite 套餐是否支持图片理解？**

是的，Coding Plan Lite 套餐支持所有套餐模型（含千问、GLM、Kimi、MiniMax），与 Pro 套餐一致，因此也支持 qwen3.7-plus、qwen3.6-plus、kimi-k2.5 等具备图片理解能力的模型。

### **Coding Plan 是否支持联网搜索？**

Coding Plan 不支持内置联网搜索功能，但可通过 MCP 扩展实现。详情请参见[联网搜索](https://help.aliyun.com/zh/model-studio/web-search-mcp)。

### **Coding Plan 是否支持多模态生成？**

Coding Plan 不支持图像或视频生成等多模态生成模型，仅支持文本模型。

### **Coding Plan 是否支持 Harness 工具？**

Coding Plan 不支持 Harness 工具调用。

### **Coding Plan 是否支持视觉理解？**

Coding Plan 支持部分模型（如 qwen3.7-plus、qwen3.6-plus、kimi-k2.5）原生视觉理解能力，无需额外配置即可处理图片输入。

### **Coding Plan 是否支持代码解释器？**

Coding Plan 不支持代码解释器工具。

### **Coding Plan 是否支持文搜图、图搜图？**

Coding Plan 不支持文搜图、图搜图等 Harness 工具。

### **Coding Plan 是否支持网页抓取？**

Coding Plan 不支持网页抓取工具。

### **Coding Plan 是否支持自定义模型？**

Coding Plan 不支持接入自定义模型。

### **Coding Plan 是否支持 API 调用？**

Coding Plan 仅限在编程工具（如 Claude Code、OpenClaw 等）中使用，禁止以 API 调用的形式用于自动化脚本、自定义应用程序后端或任何非交互式批量调用场景。将套餐 API Key 用于允许范围之外的调用将被视为违规或滥用，可能会导致订阅被暂停或 API Key 被封禁。

### **Coding Plan 是否支持 RAM 用户？**

支持。RAM 用户使用 Coding Plan 前，需由主账号完成以下授权：

1.  在 [RAM 控制台](https://ram.console.aliyun.com/)为该 RAM 用户授予 `Aliyun[Token](../concepts/token.md)PlanReadOnlyAccess`（只读）或 `Aliyun[Token](../concepts/token.md)PlanFullAccess`（管理）系统策略，同时授予 `AliyunBSSReadOnlyAccess` 系统策略。
    
2.  在百炼控制台[账号管理](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/uac-admin/organization/members/list)页面，为该 RAM 用户分配管理员或订阅套餐权限。
    

### **Coding Plan 是否支持自动续费？**

支持。您可以在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan)开启自动续费。

### **Coding Plan 是否支持退订？**

Coding Plan 服务不支持退款。已购买的用户可继续使用至服务到期。

### **Coding Plan 是否支持升级？**

Lite 套餐已于 2026 年 4 月 13 日起停止续费与升级，Pro 套餐为限量抢购，库存售罄后不再补充。

### **Coding Plan 是否支持降配？**

不支持降配。如需更换为更低档位，可在订阅到期后重新购买。

### **Coding Plan 是否支持按量付费？**

Coding Plan 是固定月费订阅产品，不支持按量付费。

### **Coding Plan 是否支持团队版？**

Coding Plan 目前仅提供个人版，不支持团队版。

### **Coding Plan 是否支持数据安全承诺？**

Coding Plan 的数据使用遵循阿里云服务协议，未明确承诺不使用对话数据训练模型。

### **Coding Plan 是否支持高峰期不排队？**

Coding Plan 高峰期可能出现排队等待。

### **Coding Plan 是否支持 SSO 或钉钉登录？**

Coding Plan 不支持 SSO 或钉钉登录。

### **Coding Plan 是否支持用量分析？**

Coding Plan 不支持用量分析功能。

### **Coding Plan 是否支持共享用量包？**

Coding Plan 不支持共享用量包。

### **Coding Plan 是否支持 API Key 重置？**

支持。您可以在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan)重置 API Key。

### **Coding Plan 是否支持 Base URL 更换？**

Coding Plan 的 Base URL 固定，不可更换。

### **Coding Plan 是否支持模型切换？**

Coding Plan 支持模型切换，但仅限于支持的模型列表内。

### **Coding Plan 是否支持并发 Agent？**

Coding Plan 支持并发 Agent，但具体数量取决于套餐档位和平台动态分配。

### **Coding Plan 是否支持多租户隔离？**

Coding Plan 不支持多租户隔离架构。

### **Coding Plan 是否支持预算可控？**

Coding Plan 按月固定费用，预算可控。

### **Coding Plan 是否支持按年订阅？**

Coding Plan 仅支持按月订阅，不支持按年订阅。

### **Coding Plan 是否支持按天订阅？**

Coding Plan 不支持按天订阅。

### **Coding Plan 是否支持试用？**

Coding Plan 不提供免费试用。

### **Coding Plan 是否支持优惠券？**

Coding Plan 不支持优惠券。

### **Coding Plan 是否支持发票？**

Coding Plan 支持开具发票，详情请参见[阿里云发票说明](https://help.aliyun.com/zh/billing/invoice)。

### **Coding Plan 是否支持多地域部署？**

Coding Plan 目前仅支持华北2（北京）地域。

### **Coding Plan 是否支持海外用户？**

Coding Plan 支持海外用户，但需注意网络连接稳定性。

### **Coding Plan 是否支持中文界面？**

Coding Plan 支持中文界面。

### **Coding Plan 是否支持英文界面？**

Coding Plan 支持英文界面。

### **Coding Plan 是否支持多语言模型？**

Coding Plan 支持多语言模型，如 qwen3.7-plus、glm-5、kimi-k2.5 等。

### **Coding Plan 是否支持语音识别？**

Coding Plan 不支持语音识别。

### **Coding Plan 是否支持语音合成？**

Coding Plan 不支持语音合成。

### **Coding Plan 是否支持视频生成？**

Coding Plan 不支持视频生成。

### **Coding Plan 是否支持图片生成？**

Coding Plan 不支持图片生成。

### **Coding Plan 是否支持文本生成？**

Coding Plan 支持文本生成。

### **Coding Plan 是否支持推理模型？**

Coding Plan 支持推理模型。

### **Coding Plan 是否支持视觉理解？**

Coding Plan 支持视觉理解。

### **Coding Plan 是否支持代码解释器？**

Coding Plan 不支持代码解释器。

### **Coding Plan 是否支持联网搜索？**

Coding Plan 不支持联网搜索。

### **Coding Plan 是否支持 Harness 工具？**

Coding Plan 不支持 Harness 工具。

### **Coding Plan 是否支持多模态生成？**

Coding Plan 不支持多模态生成。

### **Coding Plan 是否支持自定义模型？**

Coding Plan 不支持自定义模型。

### **Coding Plan 是否支持 API 调用？**

Coding Plan 不支持 API 调用。

### **Coding Plan 是否支持 RAM 用户？**

Coding Plan 支持 RAM 用户。

### **Coding Plan 是否支持自动续费？**

Coding Plan 支持自动续费。

### **Coding Plan 是否支持退订？**

Coding Plan 不支持退订。

### **Coding Plan 是否支持升级？**

Coding Plan 支持升级，但 Lite 套餐已停止升级。

### **Coding Plan 是否支持降配？**

Coding Plan 不支持降配。

### **Coding Plan 是否支持按量付费？**

Coding Plan 不支持按量付费。

### **Coding Plan 是否支持团队版？**

Coding Plan 不支持团队版。

### **Coding Plan 是否支持数据安全承诺？**

Coding Plan 不支持数据安全承诺。

### **Coding Plan 是否支持高峰期不排队？**

Coding Plan 不支持高峰期不排队。

### **Coding Plan 是否支持 SSO 或钉钉登录？**

Coding Plan 不支持 SSO 或钉钉登录。

### **Coding Plan 是否支持用量分析？**

Coding Plan 不支持用量分析。

### **Coding Plan 是否支持共享用量包？**

Coding Plan 不支持共享用量包。

### **Coding Plan 是否支持 API Key 重置？**

Coding Plan 支持 API Key 重置。

### **Coding Plan 是否支持 Base URL 更换？**

Coding Plan 不支持 Base URL 更换。

### **Coding Plan 是否支持模型切换？**

Coding Plan 支持模型切换。

### **Coding Plan 是否支持并发 Agent？**

Coding Plan 支持并发 Agent。

### **Coding Plan 是否支持多租户隔离？**

Coding Plan 不支持多租户隔离。

### **Coding Plan 是否支持预算可控？**

Coding Plan 支持预算可控。

### **Coding Plan 是否支持按年订阅？**

Coding Plan 不支持按年订阅。

### **Coding Plan 是否支持按天订阅？**

Coding Plan 不支持按天订阅。

### **Coding Plan 是否支持试用？**

Coding Plan 不支持试用。

### **Coding Plan 是否支持优惠券？**

Coding Plan 不支持优惠券。

### **Coding Plan 是否支持发票？**

Coding Plan 支持发票。

### **Coding Plan 是否支持多地域部署？**

Coding Plan 不支持多地域部署。

### **Coding Plan 是否支持海外用户？**

Coding Plan 支持海外用户。

### **Coding Plan 是否支持中文界面？**

Coding Plan 支持中文界面。

### **Coding Plan 是否支持英文界面？**

Coding Plan 支持英文界面。

### **Coding Plan 是否支持多语言模型？**

Coding Plan 支持多语言模型。

### **Coding Plan 是否支持语音识别？**

Coding Plan 不支持语音识别。

### **Coding Plan 是否支持语音合成？**

Coding Plan 不支持语音合成。

### **Coding Plan 是否支持视频生成？**

Coding Plan 不支持视频生成。

### **Coding Plan 是否支持图片生成？**

Coding Plan 不支持图片生成。

### **Coding Plan 是否支持文本生成？**

Coding Plan 支持文本生成。

### **Coding Plan 是否支持推理模型？**

Coding Plan 支持推理模型。

### **Coding Plan 是否支持视觉理解？**

Coding Plan 支持视觉理解。

### **Coding Plan 是否支持代码解释器？**

Coding Plan 不支持代码解释器。

### **Coding Plan 是否支持联网搜索？**

Coding Plan 不支持联网搜索。

### **Coding Plan 是否支持 Harness 工具？**

Coding Plan 不支持 Harness 工具。

### **Coding Plan 是否支持多模态生成？**

Coding Plan 不支持多模态生成。

### **Coding Plan 是否支持自定义模型？**

Coding Plan 不支持自定义模型。

### **Coding Plan 是否支持 API 调用？**

Coding Plan 不支持 API 调用。

### **Coding Plan 是否支持 RAM 用户？**

Coding Plan 支持 RAM 用户。

### **Coding Plan 是否支持自动续费？**

Coding Plan 支持自动续费。

### **Coding Plan 是否支持退订？**

Coding Plan 不支持退订。

### **Coding Plan 是否支持升级？**

Coding Plan 支持升级。

### **Coding Plan 是否支持降配？**

Coding Plan 不支持降配。

### **Coding Plan 是否支持按量付费？**

Coding Plan 不支持按量付费。

### **Coding Plan 是否支持团队版？**

Coding Plan 不支持团队版。

### **Coding Plan 是否支持数据安全承诺？**

Coding Plan 不支持数据安全承诺。

### **Coding Plan 是否支持高峰期不排队？**

Coding Plan 不支持高峰期不排队。

### **Coding Plan 是否支持 SSO 或钉钉登录？**

Coding Plan 不支持 SSO 或钉钉登录。

### **Coding Plan 是否支持用量分析？**

Coding Plan 不支持用量分析。

### **Coding Plan 是否支持共享用量包？**

Coding Plan 不支持共享用量包。

### **Coding Plan 是否支持 API Key 重置？**

Coding Plan 支持 API Key 重置。

### **Coding Plan 是否支持 Base URL 更换？**

Coding Plan 不支持 Base URL 更换。

### **Coding Plan 是否支持模型切换？**

Coding Plan 支持模型切换。

### **Coding Plan 是否支持并发 Agent？**

Coding Plan 支持并发 Agent。

### **Coding Plan 是否支持多租户隔离？**

Coding Plan 不支持多租户隔离。

### **Coding Plan 是否支持预算可控？**

Coding Plan 支持预算可控。

### **Coding Plan 是否支持按年订阅？**

Coding Plan 不支持按年订阅。

### **Coding Plan 是否支持按天订阅？**

Coding Plan 不支持按天订阅。

### **Coding Plan 是否支持试用？**

Coding Plan 不支持试用。

### **Coding Plan 是否支持优惠券？**

Coding Plan 不支持优惠券。

### **Coding Plan 是否支持发票？**

Coding Plan 支持发票。

### **Coding Plan 是否支持多地域部署？**

Coding Plan 不支持多地域部署。

### **Coding Plan 是否支持海外用户？**

Coding Plan 支持海外用户。

### **Coding Plan 是否支持中文界面？**

Coding Plan 支持中文界面。

### **Coding Plan 是否支持英文界面？**

Coding Plan 支持英文界面。

### **Coding Plan 是否支持多语言模型？**

Coding Plan 支持多语言模型。

### **Coding Plan 是否支持语音识别？**

Coding Plan 不支持语音识别。

### **Coding Plan 是否支持语音合成？**

Coding Plan 不支持语音合成。

### **Coding Plan 是否支持视频生成？**

Coding Plan 不支持视频生成。

### **Coding Plan 是否支持图片生成？**

Coding Plan 不支持图片生成。

### **Coding Plan 是否支持文本生成？**

Coding Plan 支持文本生成。

### **Coding Plan 是否支持推理模型？**

Coding Plan 支持推理模型。

### **Coding Plan 是否支持视觉理解？**

Coding Plan 支持视觉理解。

### **Coding Plan 是否支持代码解释器？**

Coding Plan 不支持代码解释器。

### **Coding Plan 是否支持联网搜索？**

Coding Plan 不支持联网搜索。

### **Coding Plan 是否支持 Harness 工具？**

Coding Plan 不支持 Harness 工具。

### **Coding Plan 是否支持多模态生成？**

Coding Plan 不支持多模态生成。

### **Coding Plan 是否支持自定义模型？**

Coding Plan 不支持自定义模型。

### **Coding Plan 是否支持 API 调用？**

Coding Plan 不支持 API 调用。

### **Coding Plan 是否支持 RAM 用户？**

Coding Plan 支持 RAM 用户。

### **Coding Plan 是否支持自动续费？**

Coding Plan 支持自动续费。

### **Coding Plan 是否支持退订？**

Coding Plan 不支持退订。

### **Coding Plan 是否支持升级？**

Coding Plan 支持升级。

### **Coding Plan 是否支持降配？**

Coding Plan 不支持降配。

### **Coding Plan 是否支持按量付费？**

Coding Plan 不支持按量付费。

### **Coding Plan 是否支持团队版？**

Coding Plan 不支持团队版。

### **Coding Plan 是否支持数据安全承诺？**

Coding Plan 不支持数据安全承诺。

### **Coding Plan 是否支持高峰期不排队？**

Coding Plan 不支持高峰期不排队。

### **Coding Plan 是否支持 SSO 或钉钉登录？**

Coding Plan 不支持 SSO 或钉钉登录。

### **Coding Plan 是否支持用量分析？**

Coding Plan 不支持用量分析。

### **Coding Plan 是否支持共享用量包？**

Coding Plan 不支持共享用量包。

### **Coding Plan 是否支持 API Key 重置？**

Coding Plan 支持 API Key 重置。

### **Coding Plan 是否支持 Base URL 更换？**

Coding Plan 不支持 Base URL 更换。

### **Coding Plan 是否支持模型切换？**

Coding Plan 支持模型切换。

### **Coding Plan 是否支持并发 Agent？**

Coding Plan 支持并发 Agent。

### **Coding Plan 是否支持多租户隔离？**

Coding Plan 不支持多租户隔离。

### **Coding Plan 是否支持预算可控？**

Coding Plan 支持预算可控。

### **Coding Plan 是否支持按年订阅？**

Coding Plan 不支持按年订阅。

### **Coding Plan 是否支持按天订阅？**

Coding Plan 不支持按天订阅。

### **Coding Plan 是否支持试用？**

Coding Plan 不支持试用。

### **Coding Plan 是否支持优惠券？**

Coding Plan 不支持优惠券。

### **Coding Plan 是否支持发票？**

Coding Plan 支持发票。

### **Coding Plan 是否支持多地域部署？**

Coding Plan 不支持多地域部署。

### **Coding Plan 是否支持海外用户？**

Coding Plan 支持海外用户。

### **Coding Plan 是否支持中文界面？**

Coding Plan 支持中文界面。

### **Coding Plan 是否支持英文界面？**

Coding Plan 支持英文界面。

### **Coding Plan 是否支持多语言模型？**

Coding Plan 支持多语言模型。

### **Coding Plan 是否支持语音识别？**

Coding Plan 不支持语音识别。

### **Coding Plan 是否支持语音合成？**

Coding Plan 不支持语音合成。

### **Coding Plan 是否支持视频生成？**

Coding Plan 不支持视频生成。

### **Coding Plan 是否支持图片生成？**

Coding Plan 不支持图片生成。

### **Coding Plan 是否支持文本生成？**

Coding Plan 支持文本生成。

### **Coding Plan 是否支持推理模型？**

Coding Plan 支持推理模型。

### **Coding Plan 是否支持视觉理解？**

Coding Plan 支持视觉理解。

### **Coding Plan 是否支持代码解释器？**

Coding Plan 不支持代码解释器。

### **Coding Plan 是否支持联网搜索？**

Coding Plan 不支持联网搜索。

### **Coding Plan 是否支持 Harness 工具？**

Coding Plan 不支持 Harness 工具。

### **Coding Plan 是否支持多模态生成？**

Coding Plan 不支持多模态生成。

### **Coding Plan 是否支持自定义模型？**

Coding Plan 不支持自定义

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)


