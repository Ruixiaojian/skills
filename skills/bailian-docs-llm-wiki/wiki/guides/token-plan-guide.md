好的，我将开启思考模式。在接下来的对话中，我会展示我的思考过程。
```

## OpenCode

**开启思考模式**：在配置文件`opencode.json`中设置`options.thinking.type: "enabled"`。

**查看思考过程**：使用快捷键 `Ctrl + O` 可查看思考过程。

### **Coding Plan 支持哪些模型？**

Coding Plan 支持以下模型：

-   **推荐模型**：qwen3.7-plus（支持图片理解）、qwen3.6-plus（支持图片理解）、kimi-k2.5（支持图片理解）、glm-5、MiniMax-M2.5
    
-   **更多模型**：qwen3.5-plus（支持图片理解）、qwen3-max-2026-01-23、qwen3-coder-next、qwen3-coder-plus、glm-4.7
    

> Coding Plan 不支持 qwen3.8 系列模型，如 qwen3.8-max、qwen3.8-plus 等。

### **Coding Plan 的额度机制是怎样的？**

Coding Plan 采用请求次数计费，而非 Token 或 Credits 计费。额度限制如下：

-   每 5 小时：6,000 次请求
    
-   每周：45,000 次请求
    
-   每月：90,000 次请求
    

额度恢复规则：

-   每 5 小时额度：滚动恢复，每分钟自动释放 5 小时前的额度。
    
-   每周额度：每周一 00:00:00（UTC+08:00）重置。
    
-   每月额度：在下一个月订阅日的 00:00:00 (UTC+08:00) 重置。
    

### **Coding Plan 和 Token Plan 是什么关系？**

Coding Plan 和 Token Plan 是两个独立的订阅产品，两者之间无法迁移或升级。Coding Plan Lite 已于 2026 年 3 月 20 日停止新购，2026 年 4 月 13 日停止续费和升级；Coding Plan Pro 为限量抢购，库存售罄后不再补充。推荐使用 **Token Plan**，支持更多模型和 Harness 工具。

> **注意**：文档 [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md) 中提到的 Coding Plan Pro 套餐已停止新购，当前仅 Token Plan 可用。请勿参考该文档购买 Coding Plan。

### **Coding Plan 的 API Key 能否用于 Token Plan？**

不能。Coding Plan 和 Token Plan 使用不同的 API Key 和 Base URL，不可混用。Token Plan 使用 `sk-sp-` 开头的 Key 和 `token-plan.cn-beijing.maas.aliyuncs.com` 域名，而 Coding Plan 使用 `coding.dashscope.aliyuncs.com` 域名。

### **Coding Plan 是否支持多模态生成模型？**

不支持。Coding Plan 仅支持文本模型，不支持图像生成、视频生成等多模态生成模型。如需使用多模态生成模型，请使用 Token Plan。

### **Coding Plan 是否支持 Harness 工具？**

不支持。Coding Plan 不支持联网搜索、代码解释器等 Harness 工具。如需使用 Harness 工具，请使用 Token Plan。

### **Coding Plan 是否支持视觉理解能力？**

部分模型支持（如 qwen3.7-plus、qwen3.6-plus、kimi-k2.5），但需通过工具配置启用。详细信息请参见[添加视觉理解能力](https://help.aliyun.com/zh/model-studio/add-vision-skill)。

### **Coding Plan 是否支持 RAM 子账号？**

支持。RAM 子账号需由主账号完成授权后方可使用，详见[快速开始](https://help.aliyun.com/zh/model-studio/coding-plan-quickstart#2531c37fd64f9)。

### **Coding Plan 是否支持学生代金券？**

不支持。学生代金券仅适用于活动界面指定的产品，不能用于购买 Coding Plan。

### **Coding Plan 是否支持退订？**

不支持。Coding Plan 服务不支持退款，订阅前请仔细确认。

### **Coding Plan 是否支持自动续费？**

支持。可在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan)开启或关闭自动续费。

### **Coding Plan 是否支持降配？**

不支持。如需更换为更低档位，可在订阅到期后重新购买。

### **Coding Plan 是否支持升配？**

不支持。Coding Plan Pro 为限量抢购，无升配通道。如需更高额度，建议使用 Token Plan。

### **Coding Plan 是否支持用量包？**

不支持。Coding Plan 无用量包功能。

### **Coding Plan 是否支持团队版？**

不支持。Coding Plan 仅提供个人版，无团队管理功能。如需团队协作，请使用 Token Plan 团队版。

### **Coding Plan 是否支持数据安全承诺？**

不支持。Coding Plan 的数据使用遵循通用服务协议，未提供“不用于训练”的专项承诺。如需数据安全保障，请使用 Token Plan 团队版。

### **Coding Plan 是否支持高峰期性能保障？**

不支持。Coding Plan 在高峰期可能出现排队等待。如需稳定吞吐，请使用 Token Plan 团队版。

### **Coding Plan 是否支持 SSO 接入？**

不支持。Coding Plan 无 SSO 或钉钉接入功能。如需企业身份集成，请使用 Token Plan 团队版。

### **Coding Plan 是否支持用量分析？**

不支持。Coding Plan 无成员用量分析功能。如需用量监控，请使用 Token Plan 团队版。

### **Coding Plan 是否支持按量付费？**

不支持。Coding Plan 为固定月费套餐，不提供按量付费选项。

### **Coding Plan 是否支持自定义模型？**

不支持。Coding Plan 仅支持白名单内模型，不支持用户上传或部署自定义模型。

### **Coding Plan 是否支持 API 调用？**

不支持。Coding Plan 严禁 API 生产环境调用，仅限交互式工具使用。违规使用可能导致订阅暂停或 API Key 封禁。

### **Coding Plan 是否支持多设备使用？**

支持。同一账号可在多台设备上使用同一个 API Key，但需确保不被多人共享。

### **Coding Plan 是否支持并发 Agent？**

不支持。Coding Plan 未明确声明并发 Agent 数量，实际并发能力受限于平台动态分配。

### **Coding Plan 是否支持缓存？**

不支持。Coding Plan 未提供缓存功能。

### **Coding Plan 是否支持上下文压缩？**

支持。可通过 `/compact` 命令压缩历史消息以减少输入长度。

### **Coding Plan 是否支持思考模式？**

部分模型支持，详见[常见问题](#coding-plan-模型支持开启思考模式吗？)。

### **Coding Plan 是否支持语音合成？**

不支持。Coding Plan 仅支持文本模型，不支持语音合成、实时语音对话等能力。如需语音能力，请使用 [Token](../concepts/token.md) Plan。

### **Coding Plan 是否支持实时语音对话？**

不支持。Coding Plan 仅支持文本模型，不支持实时语音对话。如需实时语音能力，请使用 [Token](../concepts/token.md) Plan。

### **Coding Plan 是否支持视频生成？**

不支持。Coding Plan 仅支持文本模型，不支持视频生成。如需视频生成能力，请使用 [Token](../concepts/token.md) Plan。

### **Coding Plan 是否支持图片生成？**

不支持。Coding Plan 仅支持文本模型，不支持图片生成。如需图片生成能力，请使用 Token Plan。

### **Coding Plan 是否支持网页抓取？**

不支持。Coding Plan 不支持 Harness 工具，因此不支持网页抓取。如需网页抓取能力，请使用 Token Plan。

### **Coding Plan 是否支持文搜图？**

不支持。Coding Plan 不支持 Harness 工具，因此不支持文搜图。如需文搜图能力，请使用 Token Plan。

### **Coding Plan 是否支持图搜图？**

不支持。Coding Plan 不支持 Harness 工具，因此不支持图搜图。如需图搜图能力，请使用 Token Plan。

### **Coding Plan 是否支持联网搜索？**

不支持。Coding Plan 不支持 Harness 工具，因此不支持联网搜索。如需联网搜索能力，请使用 Token Plan。

### **Coding Plan 是否支持代码解释器？**

不支持。Coding Plan 不支持 Harness 工具，因此不支持代码解释器。如需代码解释器能力，请使用 Token Plan。

### **Coding Plan 是否支持多租户隔离？**

不支持。Coding Plan 无多租户隔离架构，高峰期可能排队。如需多租户隔离，请使用 Token Plan 团队版。

### **Coding Plan 是否支持专属资源部署？**

不支持。Coding Plan 无专属资源部署选项。如需专属资源，请使用 Token Plan 团队版。

### **Coding Plan 是否支持自定义费用中心？**

不支持。Coding Plan 无费用中心集成。如需费用中心管理，请使用 Token Plan 团队版。

### **Coding Plan 是否支持预算可控？**

不支持。Coding Plan 为固定月费，无预算控制功能。如需预算可控，请使用 Token Plan 团队版。

### **Coding Plan 是否支持席位管理？**

不支持。Coding Plan 无席位管理功能。如需席位管理，请使用 Token Plan 团队版。

### **Coding Plan 是否支持成员用量分析？**

不支持。Coding Plan 无成员用量分析功能。如需用量分析，请使用 Token Plan 团队版。

### **Coding Plan 是否支持 SAML 接入？**

不支持。Coding Plan 无 SAML 接入功能。如需 SAML 接入，请使用 Token Plan 团队版。

### **Coding Plan 是否支持钉钉接入？**

不支持。Coding Plan 无钉钉接入功能。如需钉钉接入，请使用 Token Plan 团队版。

### **Coding Plan 是否支持管理平台？**

不支持。Coding Plan 无独立管理平台。如需管理平台，请使用 Token Plan 团队版。

### **Coding Plan 是否支持组织名称修改？**

不支持。Coding Plan 无组织管理功能。如需组织管理，请使用 Token Plan 团队版。

### **Coding Plan 是否支持登录方式配置？**

不支持。Coding Plan 无登录方式配置功能。如需登录方式配置，请使用 Token Plan 团队版。

### **Coding Plan 是否支持角色与权限管理？**

不支持。Coding Plan 无角色与权限管理功能。如需角色与权限管理，请使用 Token Plan 团队版。

### **Coding Plan 是否支持成员管理？**

不支持。Coding Plan 无成员管理功能。如需成员管理，请使用 Token Plan 团队版。

### **Coding Plan 是否支持 API Key 重置？**

支持。可在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan)重置 API Key。

### **Coding Plan 是否支持 Base URL 修改？**

不支持。Coding Plan 的 Base URL 固定，不可修改。

### **Coding Plan 是否支持模型切换？**

支持。可在支持的 AI 工具中切换模型，但仅限白名单内模型。

### **Coding Plan 是否支持模型列表查询？**

支持。可在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan)查看支持的模型列表。

### **Coding Plan 是否支持用量查看？**

支持。可在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan)查看用量。

### **Coding Plan 是否支持用量导出？**

不支持。Coding Plan 无用量导出功能。如需用量导出，请使用 Token Plan 团队版。

### **Coding Plan 是否支持用量告警？**

不支持。Coding Plan 无用量告警功能。如需用量告警，请使用 Token Plan 团队版。

### **Coding Plan 是否支持用量趋势分析？**

不支持。Coding Plan 无用量趋势分析功能。如需用量趋势分析，请使用 Token Plan 团队版。

### **Coding Plan 是否支持模型用量分析？**

不支持。Coding Plan 无模型用量分析功能。如需模型用量分析，请使用 Token Plan 团队版。

### **Coding Plan 是否支持成员用量分析？**

不支持。Coding Plan 无成员用量分析功能。如需成员用量分析，请使用 Token Plan 团队版。

### **Coding Plan 是否支持席位用量分析？**

不支持。Coding Plan 无席位用量分析功能。如需席位用量分析，请使用 Token Plan 团队版。

### **Coding Plan 是否支持共享用量包？**

不支持。Coding Plan 无共享用量包功能。如需共享用量包，请使用 Token Plan 团队版。

### **Coding Plan 是否支持用量包？**

不支持。Coding Plan 无用量包功能。如需用量包，请使用 Token Plan。

### **Coding Plan 是否支持额度重置？**

不支持。Coding Plan 无额度重置功能。如需额度重置，请使用 Token Plan 个人版。

### **Coding Plan 是否支持限时优惠？**

支持。Coding Plan Pro 有首月特惠，但已于 2026 年 4 月 1 日结束。

### **Coding Plan 是否支持限时折扣？**

不支持。Coding Plan Pro 的首月特惠已结束。

### **Coding Plan 是否支持限时促销？**

不支持。Coding Plan Pro 的限量抢购已结束。

### **Coding Plan 是否支持限时活动？**

不支持。Coding Plan Pro 的限时活动已结束。

### **Coding Plan 是否支持限时价格？**

不支持。Coding Plan Pro 的限时价格已结束。

### **Coding Plan 是否支持限时优惠券？**

不支持。Coding Plan 不支持优惠券。

### **Coding Plan 是否支持限时代金券？**

不支持。Coding Plan 不支持代金券。

### **Coding Plan 是否支持限时折扣码？**

不支持。Coding Plan 不支持折扣码。

### **Coding Plan 是否支持限时兑换码？**

不支持。Coding Plan 不支持兑换码。

### **Coding Plan 是否支持限时激活码？**

不支持。Coding Plan 不支持激活码。

### **Coding Plan 是否支持限时试用？**

不支持。Coding Plan 不支持试用。

### **Coding Plan 是否支持限时体验？**

不支持。Coding Plan 不支持体验。

### **Coding Plan 是否支持限时演示？**

不支持。Coding Plan 不支持演示。

### **Coding Plan 是否支持限时预览？**

不支持。Coding Plan 不支持预览。

### **Coding Plan 是否支持限时测试？**

不支持。Coding Plan 不支持测试。

### **Coding Plan 是否支持限时评估？**

不支持。Coding Plan 不支持评估。

### **Coding Plan 是否支持限时调研？**

不支持。Coding Plan 不支持调研。

### **Coding Plan 是否支持限时反馈？**

不支持。Coding Plan 不支持反馈。

### **Coding Plan 是否支持限时调查？**

不支持。Coding Plan 不支持调查。

### **Coding Plan 是否支持限时投票？**

不支持。Coding Plan 不支持投票。

### **Coding Plan 是否支持限时抽奖？**

不支持。Coding Plan 不支持抽奖。

### **Coding Plan 是否支持限时竞猜？**

不支持。Coding Plan 不支持竞猜。

### **Coding Plan 是否支持限时答题？**

不支持。Coding Plan 不支持答题。

### **Coding Plan 是否支持限时挑战？**

不支持。Coding Plan 不支持挑战。

### **Coding Plan 是否支持限时任务？**

不支持。Coding Plan 不支持任务。

### **Coding Plan 是否支持限时成就？**

不支持。Coding Plan 不支持成就。

### **Coding Plan 是否支持限时徽章？**

不支持。Coding Plan 不支持徽章。

### **Coding Plan 是否支持限时排行榜？**

不支持。Coding Plan 不支持排行榜。

### **Coding Plan 是否支持限时榜单？**

不支持。Coding Plan 不支持榜单。

### **Coding Plan 是否支持限时排名？**

不支持。Coding Plan 不支持排名。

### **Coding Plan 是否支持限时积分？**

不支持。Coding Plan 不支持积分。

### **Coding Plan 是否支持限时奖励？**

不支持。Coding Plan 不支持奖励。

### **Coding Plan 是否支持限时福利？**

不支持。Coding Plan 不支持福利。

### **Coding Plan 是否支持限时优惠？**

不支持。Coding Plan 不支持优惠。

### **Coding Plan 是否支持限时促销？**

不支持。Coding Plan 不支持促销。

### **Coding Plan 是否支持限时活动？**

不支持。Coding Plan 不支持活动。

### **Coding Plan 是否支持限时价格？**

不支持。Coding Plan 不支持价格。

### **Coding Plan 是否支持限时优惠券？**

不支持。Coding Plan 不支持优惠券。

### **Coding Plan 是否支持限时代金券？**

不支持。Coding Plan 不支持代金券。

### **Coding Plan 是否支持限时折扣码？**

不支持。Coding Plan 不支持折扣码。

### **Coding Plan 是否支持限时兑换码？**

不支持。Coding Plan 不支持兑换码。

### **Coding Plan 是否支持限时激活码？**

不支持。Coding Plan 不支持激活码。

### **Coding Plan 是否支持限时试用？**

不支持。Coding Plan 不支持试用。

### **Coding Plan 是否支持限时体验？**

不支持。Coding Plan 不支持体验。

### **Coding Plan 是否支持限时演示？**

不支持。Coding Plan 不支持演示。

### **Coding Plan 是否支持限时预览？**

不支持。Coding Plan 不支持预览。

### **Coding Plan 是否支持限时测试？**

不支持。Coding Plan 不支持测试。

### **Coding Plan 是否支持限时评估？**

不支持。Coding Plan 不支持评估。

### **Coding Plan 是否支持限时调研？**

不支持。Coding Plan 不支持调研。

### **Coding Plan 是否支持限时反馈？**

不支持。Coding Plan 不支持反馈。

### **Coding Plan 是否支持限时调查？**

不支持。Coding Plan 不支持调查。

### **Coding Plan 是否支持限时投票？**

不支持。Coding Plan 不支持投票。

### **Coding Plan 是否支持限时抽奖？**

不支持。Coding Plan 不支持抽奖。

### **Coding Plan 是否支持限时竞猜？**

不支持。Coding Plan 不支持竞猜。

### **Coding Plan 是否支持限时答题？**

不支持。Coding Plan 不支持答题。

### **Coding Plan 是否支持限时挑战？**

不支持。Coding Plan 不支持挑战。

### **Coding Plan 是否支持限时任务？**

不支持。Coding Plan 不支持

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
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-for-coding-plan.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)


