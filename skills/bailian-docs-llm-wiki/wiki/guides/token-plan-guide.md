# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 统一计量，支持文本、多模态模型及 Harness 工具，适配主流 AI 编程和智能体工具。该服务分为个人版与团队版，均仅支持华北2（北京）地域，需在控制台切换地域后购买使用 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。Credits 消耗受模型类型、[Token](../concepts/token.md) 用量、思考模式及工具调用动态影响，实际消耗以控制台用量详情为准 [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。

## 支持的模型/功能

- **模型覆盖**：支持千问（qwen3.8-max-preview、qwen3.7-plus、qwen3.6-flash 等）、智谱 AI（glm-5.2）、DeepSeek（deepseek-v4-pro）、万相（wan2.7-image）、HappyHorse（happyhorse-1.1-t2v）等数十款文本、视觉理解、图片生成、视频生成及语音合成模型。qwen3.8-max-preview 为预览模型，能力持续迭代，预览期结束后可能下线或替换 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。
- **Harness 工具**：支持联网搜索（`web_search`）、文搜图（`t2i_search`）、图搜图（`i2i_search`）、网页抓取（`web_extractor`）、代码解释器（`code_interpreter`），仅 qwen3.7 及 qwen3.8 系列模型原生支持 [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。
- **多模态能力**：qwen3.7-plus、qwen3.6-plus、kimi-k2.5 等模型原生支持视觉理解；glm-5、MiniMax-M2.5 等纯文本模型可通过 Skill 或 Agent 辅助实现图片分析 [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)。

> **注意**：文档 11（Coding Plan 概述）中列出的 `qwen3-coder-next`、`qwen3-coder-plus` 等模型未出现在 [Token](../concepts/token.md) Plan 个人版或团队版的任一支持列表中，属于 Coding Plan 专属模型，Token Plan 不支持。请勿混用模型 ID。

## 关键参数

- **Credits 计费机制**：单次调用消耗由模型类型、输入/输出 Token 数、缓存 Token、思考模式及工具调用共同决定。例如 qwen3.6-plus 单次请求预估消耗约 3.18 Credits（含输入、缓存、输出分项）[概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)。
- **限额策略**：
  - *个人版*：双层窗口限额——**5 小时限额**（自首次调用起计时，触顶即暂停）与**7 天限额**（同理），额度不结转。Lite/Standard/Pro 套餐对应限额分别为 (700, 2500) / (3000, 10000) / (12000, 40000) Credits。
  - *团队版*：**月度总额度制**，无窗口限制。标准/高级/尊享坐席分别为 25,000 / 100,000 / 250,000 Credits/坐席/月，额度到期清零。
- **并发与 Agent**：个人版 Lite/Standard/Pro 套餐分别支持 1–2 / 3–4 / 6–8 个并发 Agent；团队版无明确并发上限，依托多租户隔离架构保障高峰期不排队 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)。

## 使用方式

1. **订阅与配置**：
   - 访问控制台 [Token Plan 购买页](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)，选择个人版或团队版套餐完成订阅。
   - 获取专属 API Key（以 `sk-sp-` 开头）与 Base URL：
     - OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
     - Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
   - RAM 用户需主账号授予 `AliyunTokenPlanFullAccess` 及 `AliyunBSSReadOnlyAccess` 策略，并在百炼控制台分配权限 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)。

2. **接入工具**：
   - 将 API Key 与 Base URL 配置至 Cursor、Claude Code、Qwen Code、Qoder、OpenClaw 等兼容工具。
   - 多模态模型（如 `wan2.7-image`）需通过工具的 Skill、Slash Command 或 Agent 扩展机制接入，不可直接通过文本模型 Base URL 调用 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)。

3. **Harness 工具调用**：切换至支持模型（如 `qwen3.7-plus`），在对话中直接提问，模型将自动触发联网搜索、代码解释器等能力，无需额外配置 [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。

## 限制和注意事项

- **地域限制**：个人版与团队版均**仅支持华北2（北京）地域**，控制台左上角必须切换至此地域方可购买与调用 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。
- **使用范围**：严禁用于自动化脚本、生产环境后端服务或非交互式批量调用；仅限在官方指定工具（Cursor、Claude Code 等）中交互式使用。违规可能导致订阅暂停或 API Key 封禁 [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。
- **API Key 隔离**：Token Plan（`sk-sp-`）、Coding Plan（`sk-sp-` but different domain）、按量付费（`sk-`）三者 API Key 与 Base URL 完全隔离，混用将导致鉴权失败（401）或意外扣费 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)。
- **数据条款**：
  - 个人版：输入与生成内容将用于服务改进与模型优化；停止使用可终止后续授权，但已授权数据不溯及既往 [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。
  - 团队版：承诺**不使用对话数据训练模型**，满足企业级数据隐私要求 [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)。
- **升级与退订**：
  - 个人版支持升配（补差价，限额立即提升），**不支持降配**；订阅到期后重新购买将变更 API Key，需重新配置 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)。
  - 团队版支持坐席升配、加购、退订；续费不变更 API Key，仅到期后重购或退订重购才需重新配置 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)


