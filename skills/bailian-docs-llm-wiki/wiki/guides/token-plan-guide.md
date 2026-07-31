# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 统一计量，支持多种 AI 编程和智能体工具。它提供个人版和团队版两个版本，分别面向个人开发者与企业团队，覆盖文本、[多模态](../concepts/multi-modal.md)生成及 Harness [工具调用](../concepts/tool-use.md)等能力。所有服务当前仅支持华北2（北京）地域。

## 支持的模型与功能

[Token](../concepts/token.md) Plan 支持广泛的模型类型和扩展能力：

- **文本模型**：qwen3.8-max-preview（预览版）、qwen3.7-max、qwen3.7-plus、qwen3.6-flash、glm-5.2、deepseek-v4-pro 等；
- **[多模态](../concepts/multi-modal.md)模型**：wan2.7-image、wan2.7-image-pro（图片生成），happyhorse-1.1-t2v、happyhorse-1.1-i2v（视频生成），qwen-audio-3.0-tts-plus（语音合成）；
- **Harness 工具**：联网搜索（`web_search`）、文搜图（`t2i_search`）、图搜图（`i2i_search`）、网页抓取（`web_extractor`）、代码解释器（`code_interpreter`）。这些工具需通过 qwen3.7 或 qwen3.8 系列模型原生调用，详见 [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)；
- **视觉理解**：qwen3.8-max-preview、qwen3.7-plus、qwen3.6-plus、kimi-k2.5 等模型原生支持图片输入；glm-5、MiniMax-M2.5 等纯文本模型可通过 Skill/Agent 辅助实现，具体方法见 [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)。

> **注意**：文档 1 和文档 4 均声明 qwen3.8-max-preview 为预览模型，但文档 1 提到“预览结束后该模型会下线或替换成正式版本”，而文档 2 和文档 4 仅强调“预览期间模型能力会持续迭代升级”，未明确下线承诺。实际行为请以控制台最新说明为准。

## 关键参数

- **Credits 计费机制**：单次消耗由模型类型、[Token](../concepts/token.md) 用量、思考模式及[工具调用](../concepts/tool-use.md)动态决定，非固定单价。例如 qwen3.6-plus 单次请求约消耗 3.18 Credits（含输入、缓存、输出 tokens）[原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)；
- **额度结构**：
  - *个人版*：采用双层窗口限额——**5 小时限额**（自首次调用起计时）和**7 天限额**（同样滚动窗口），任一层触顶即暂停服务；
  - *团队版*：采用**月度总额度制**（如标准坐席 25,000 Credits/月），无窗口限制，额度到期不结转；
- **并发能力**：个人版 Lite/Standard/Pro 套餐分别支持 1–2 / 3–4 / 6–8 个 Agent 并发；团队版基于多租户隔离架构，高峰期不排队；
- **API Key 格式**：Token Plan 专属 API Key 以 `sk-sp-` 开头，与百炼通用 API Key（`sk-` 开头）及 Coding Plan Key 完全隔离，不可混用。

## 使用方式

1. **订阅与配置**：
   - 访问 [Token Plan 购买页](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)，选择个人版或团队版套餐并完成支付；
   - RAM 用户需由主账号授予 `AliyunTokenPlanFullAccess` 及 `AliyunBSSReadOnlyAccess` 策略，并在百炼控制台分配订阅权限 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)；
   - 在控制台「我的订阅」页面获取 API Key（仅生成时完整显示一次）和 Base URL（OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`）。

2. **接入工具**：
   - 将 API Key 和 Base URL 配置至 Cursor、Claude Code、Qwen Code、Qoder、OpenClaw 等兼容工具；
   - [多模态](../concepts/multi-modal.md)模型（如图像/视频生成）需通过工具的 Skill、Slash Command 或 Agent 扩展机制接入，不能直接使用文本模型 Base URL 调用 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)；
   - Harness [工具调用](../concepts/tool-use.md)无需额外配置，切换至支持模型（如 qwen3.7-plus）后直接提问即可触发。

## 限制和注意事项

- **地域限制**：Token Plan 当前仅支持华北2（北京）地域，控制台需手动切换；
- **使用范围**：严禁用于自动化脚本、批量调用或应用后端；仅限交互式 AI 编程/智能体工具中使用，违规可能导致 API Key 封禁；
- **数据政策**：
  - 个人版：输入及生成内容将用于服务改进与模型优化；
  - 团队版：承诺不使用对话数据训练模型；
- **额度管理**：
  - 个人版用量包需先订阅有效套餐才能购买，最多持有 5 个，有效期 1 个月，不支持退款；
  - 团队版共享用量包（625,000 Credits/个）按月清零，优先抵扣最近到期包；
- **模型兼容性**：部分工具（如 OpenCode）需在配置文件中显式声明 `modalities.input = ["text", "image"]` 才能启用视觉能力；
- **与 Coding Plan 的关系**：两者为独立产品，无法迁移或升级；Coding Plan Lite 已于 2026 年 3 月 20 日停止新购，推荐迁移到 Token Plan。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)


