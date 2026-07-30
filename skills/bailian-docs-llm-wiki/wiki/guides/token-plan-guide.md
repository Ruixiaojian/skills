# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 统一计量，支持多种 AI 编程和智能体工具。该服务分为个人版和团队版，分别面向个人开发者与企业团队，提供模型调用、[多模态](../concepts/multi-modal.md)生成及 Harness 工具等能力，所有功能当前仅限华北2（北京）地域使用。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 支持文本生成、图像生成、视频生成、语音合成等[多模态](../concepts/multi-modal.md)模型，以及联网搜索、代码解释器、网页抓取等 Harness 工具。具体模型列表详见 [Token Plan 个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md) 和 [Token Plan 团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md) 的官方文档。

- **核心模型**：qwen3.8-max-preview（预览版，享限时 1 折+夜间 0.2 折）、qwen3.7-plus、qwen3.6-flash、wan2.7-image、happyhorse-1.1-t2v、qwen-audio-3.0-tts-plus 等。
- **Harness 工具**：仅 qwen3.7 及以上系列模型原生支持，包括 `web_search`、`code_interpreter`、`t2i_search`、`i2i_search`、`web_extractor`；调用按成功次数抵扣 Credits [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。
- **[多模态](../concepts/multi-modal.md)生成**：图像、视频、语音模型需通过工具扩展机制（如 Slash Command、Skill、Agent）接入，不可直接通过 OpenAI/Anthropic 兼容 Base URL 调用 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。
- **视觉理解**：qwen3.7-plus、qwen3.6-plus、kimi-k2.5 等模型原生支持；glm-5、MiniMax-M2.5 等纯文本模型需通过 Skill 或 Agent 辅助实现 [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)。

> **注意**：文档 13（Coding Plan概述）中声明“Lite 套餐已于 2026 年 3 月 20 日起停止新购”，而文档 1 中明确指出“推荐使用 [Token](../concepts/token.md) Plan，支持更多模型和 Harness 工具”。二者定位不同，Coding Plan 已逐步被 [Token](../concepts/token.md) Plan 替代，开发者应优先选用 [Token](../concepts/token.md) Plan。

## 关键参数

- **Credits 计费机制**：单次消耗由模型类型、[Token](../concepts/token.md) 用量、思考模式及工具调用动态决定，实际消耗以控制台用量明细为准。
- **限额机制**：
  - *个人版*：采用双层窗口限额——**每 5 小时**和**每 7 天**独立计时，任一触顶即暂停服务；额度不结转，可购买用量包补充或手动重置 [Token Plan 个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。
  - *团队版*：采用**月度总额度制**，无窗口限制；各坐席额度按月重置，未用完不结转；超出后可购买共享用量包（625,000 Credits/个，有效期 1 个月）[Token Plan 团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)。
- **并发能力**：个人版 Lite/Standard/Pro 套餐分别支持 1–2 / 3–4 / 6–8 个 Agent 并发；团队版无显式并发限制，依托多租户隔离架构保障高峰期不排队。

## 使用方式

1. **地域与订阅**：必须将百炼控制台地域切换至**华北2（北京）**，再访问对应购买页完成订阅。
2. **API Key 与 Base URL**：
   - API Key 以 `sk-sp-` 开头，仅限 [Token](../concepts/token.md) Plan 专属使用，与通用 API Key（`sk-`）及 Coding Plan Key 完全隔离。
   - Base URL 分协议：
     - OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
     - Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
3. **工具接入**：支持 Cursor、Claude Code、Qwen Code、Qoder、OpenClaw 等主流工具，配置 API Key 和 Base URL 即可启用 [快速开始（个人版）](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md) 和 [快速开始（团队版）](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)。
4. **高级能力接入**：
   - Harness 工具：切换至支持模型后直接提问，模型自动调用。
   - [多模态](../concepts/multi-modal.md)模型：需在工具中配置 Skill/Slash Command/Agent，调用独立接口（如 `/text-to-image`）。
   - 联网搜索 MCP：需额外开通百炼通用 API Key（`sk-`）驱动的 MCP 服务，与 [Token](../concepts/token.md) Plan 专属 Key 分离 [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)。

## 限制和注意事项

- **地域限制**：所有 [Token](../concepts/token.md) Plan 功能仅在华北2（北京）可用，跨地域调用将失败。
- **使用范围限制**：仅限交互式开发工具（如 Claude Code、Cursor）中使用，**严禁用于自动化脚本、应用后端或批量调用**；违规可能导致订阅暂停或 API Key 封禁 [Token Plan 个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。
- **数据安全**：团队版承诺不使用对话数据训练模型；个人版则授权用于服务改进与模型优化。
- **账号规范**：API Key 不可共享；团队版需通过成员管理分配席位，RAM 用户需主账号授予 `AliyunTokenPlanFullAccess` 及 `AliyunBSSReadOnlyAccess` 权限。
- **升级与退订**：
  - 个人版支持升配（补差价），不支持降配；暂不支持退订。
  - 团队版支持加购/升级席位，不支持降配；退订席位后 API Key 和 Base URL 将变更，需重新配置。
- **额度重置**：个人版可手动重置 5 小时/7 天限额；团队版仅支持等待月度重置或购买共享用量包。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)




