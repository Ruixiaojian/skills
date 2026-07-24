# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 统一计量，支持文本、多模态生成模型及 Harness 工具，适配主流 AI 编程与智能体工具。服务当前仅支持华北2（北京）地域，个人版与团队版独立计费、额度不共享，且均需通过专属 `sk-sp-` 开头的 API Key 与配套 Base URL 接入。

## 支持的模型与功能

[Token](../concepts/token.md) Plan 支持覆盖文本生成、视觉理解、图片生成、视频生成、语音合成/识别等能力的多模态模型，并集成联网搜索、代码解释器、网页抓取、文搜图、图搜图等 Harness 工具。  
- **个人版**支持模型包括 `qwen3.8-max-preview`（预览版）、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro`、`wan2.7-image`、`happyhorse-1.1-t2v` 等；[详见支持的模型列表](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tpp01-models)。  
- **团队版**额外支持 `qwen-image-2.0`、`kimi-k2.7-code`、`glm-5.1`、`MiniMax-M2.5` 等模型，且明确承诺不使用对话数据训练模型 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)。  
- Harness 工具仅在 `qwen3.7` 及以上系列模型（如 `qwen3.7-plus`、`qwen3.8-max-preview`）中支持原生调用，按成功调用次数抵扣 Credits [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。  
> **注意**：文档 9（Coding Plan 概述）中列出的 `qwen3-coder-next`、`qwen3-coder-plus` 等模型未出现在 [Token](../concepts/token.md) Plan 任一版本的支持列表中，属 Coding Plan 专属模型，不可在 Token Plan 中调用。

## 关键参数

- **Credits 计费机制**：单次消耗由模型类型、输入/输出 Token 数、缓存 Token、思考模式及工具调用动态计算，实际消耗以控制台用量明细为准。  
- **额度机制**：  
  - *个人版*：双层固定窗口限额——**5 小时限额**（自首次调用起滚动计时）与**7 天限额**（自首次调用起滚动计时），任一层触顶即暂停服务，额度不结转 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)。  
  - *团队版*：**月度总额度制**，无窗口限制，坐席额度按月重置，未用完额度不结转；超出后可购买共享用量包（625,000 Credits/个，有效期 1 个月）补充。  
- **并发能力**：个人版 Pro 套餐支持 6–8 个 Agent 并发；团队版基于多租户隔离架构，高峰期不排队。

## 使用方式

1. **订阅与授权**：  
   - 访问 [Token Plan 购买页](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)，选择个人版或团队版套餐完成订阅。  
   - RAM 用户需由主账号授予 `AliyunTokenPlanFullAccess`（或 ReadOnly）及 `AliyunBSSReadOnlyAccess`（或 FullAccess）策略，并在百炼控制台分配订阅权限。  

2. **获取凭证**：  
   - **API Key**：以 `sk-sp-` 开头，仅在生成/重置时完整显示一次，必须立即复制保存。  
   - **Base URL**：  
     - OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`  
     - Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`  
   > **注意**：Token Plan、Coding Plan 与按量付费的 API Key 和 Base URL 完全隔离，混用将导致 401/403 错误或意外按量扣费 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)。  

3. **接入工具**：  
   - 直接配置 API Key 与 Base URL 至 Cursor、Claude Code、Qwen Code、Qoder、OpenClaw 等兼容工具。  
   - 多模态模型（如 `wan2.7-image`、`happyhorse-1.1-t2v`）需通过工具的 Skill/Slash Command/Agent 机制接入，详见 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。  
   - 视觉理解能力：`qwen3.7-plus` 等模型原生支持；`glm-5` 等纯文本模型需通过 Skill 或 Agent 辅助调用视觉模型 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)。  

## 限制和注意事项

- **使用范围限制**：仅限在官方指定交互式 AI 工具（如 Cursor、Claude Code、Qoder）中使用，**严禁用于自动化脚本、批量调用、应用后端等非交互场景**；违规可能导致 API Key 封禁。  
- **地域限制**：服务仅部署于华北2（北京），调用请求必须路由至此地域。  
- **账号规范**：个人版禁止共享；团队版 API Key 仅限已分配席位的成员本人使用。  
- **模型时效性**：`qwen3.8-max-preview` 为预览模型，能力持续迭代，预览结束后可能下线或替换为正式版，活动权益（如 1 折、夜间 0.2 折）随时可能调整。  
- **退订与续费**：个人版不支持退订；团队版支持席位退订（退款原路返回），但续费仅延长有效期，不补充当期额度。  
- **错误排查**：常见报错如 `429 Allocated quota exceeded`（额度用尽）、`404 model 'xxx' not found`（模型名大小写/拼写错误）、`401 InvalidApiKey`（Key 或 Base URL 不匹配）需对照 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md) 逐一验证。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)


