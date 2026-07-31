# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 为统一计量单位，支持文本、多模态生成模型及 Harness 工具，适配主流 AI 编程与智能体工具。服务当前仅限华北2（北京）地域使用，个人版与团队版独立计费、额度不互通，均需通过专属 `sk-sp-` 开头的 API Key 和配套 Base URL 接入。

## 支持的模型与功能

[Token](../concepts/token.md) Plan 支持覆盖文本生成、视觉理解、图像/视频生成、语音合成等能力的多模态模型，并集成联网搜索、代码解释器等 Harness 工具。  
- **核心模型**：qwen3.8-max-preview（预览版，享限时 1 折+夜间 0.2 折）、qwen3.7-plus、qwen3.6-flash、wan2.7-image、happyhorse-1.1-t2v、glm-5.2、deepseek-v4-pro、kimi-k2.5 等（详见 [Token Plan 个人版概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md) 和 [Token Plan 团队版概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)）。  
- **Harness 工具**：仅 qwen3.7/qwen3.8 系列模型原生支持，包括 `web_search`、`t2i_search`、`i2i_search`、`web_extractor`、`code_interpreter`，须通过 Responses API 调用（[接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)）。  
- **多模态生成模型**（如图像、视频、语音）需通过 AI 工具的 Skill/Slash Command/Agent 扩展机制接入，不可直接通过 Chat Completions 接口调用（[接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)）。

> **注意**：文档 12（Coding Plan 概述）中声明“Coding Plan Lite 已于 2026 年 3 月 20 日停止新购”，而文档 1 明确指出“Coding Plan 和 [Token](../concepts/token.md) Plan 是两个独立的订阅产品，两者之间无法迁移或升级。推荐使用 **Token Plan**，支持更多模型和 Harness 工具”。该信息无矛盾，但需强调 Token Plan 是当前主推且功能更全的替代方案。

## 关键参数

| 参数 | 个人版 | 团队版 |
|------|--------|--------|
| **地域限制** | 华北2（北京） | 华北2（北京） |
| **额度机制** | 双层窗口限额：每 5 小时 + 每 7 天（独立触发暂停） | 月度固定额度（无窗口限制） |
| **额度重置** | 窗口到期自动重置；支持手动重置（清零当前窗口消耗） | 每月 1 日 00:00:00（UTC+8）自动重置 |
| **并发能力** | Lite：1–2 Agent；Standard：3–4；Pro：6–8 | 无明确并发上限，高峰期不排队（多租户隔离） |
| **API Key 格式** | `sk-sp-xxxxx`（仅限 Token Plan 个人版） | `sk-sp-xxxxx`（仅限 Token Plan 团队版，按席位分配） |
| **Base URL** | OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | 同上（与个人版共用同一 Base URL，但 Key 自动路由） |
| **用量包** | 100 元/个/月，20,000 Credits/个，无窗口限制，需先订阅套餐 | 共享用量包：5,000 元/个/月，625,000 Credits/个，有效期 1 个月，团队内共享 |

## 使用方式

1. **订阅与授权**：  
   - 访问 [Token Plan 购买页](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)，选择个人版或团队版完成订阅。  
   - RAM 用户需由主账号授予 `AliyunTokenPlanFullAccess`（或 ReadOnly）及 `AliyunBSSReadOnlyAccess`（个人版）/`AliyunBSSFullAccess`（团队版）策略，并在百炼控制台分配相应权限（[快速开始（个人版）](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)、[快速开始（团队版）](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)）。

2. **获取凭证**：  
   - 个人版：在「我的订阅」页面生成唯一 API Key（仅显示一次）。  
   - 团队版：在成员管理中为成员分配席位后，系统自动生成专属 API Key。

3. **配置工具**：  
   - 将 API Key 与对应 Base URL 配置至 Cursor、Claude Code、Qwen Code、Qoder 等兼容工具。  
   - Harness 工具需确保工具通过 Responses API 接入（非 Chat Completions）；多模态模型需按工具规范配置 Skill/Slash Command（如 Claude Code 的 `.claude/commands/text-to-image.md`）。

4. **扩展能力**：  
   - 视觉理解：直接使用 `qwen3.7-plus` 等原生支持模型，或为 `glm-5` 等纯文本模型配置 `image-analyzer` Skill（[添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)）。  
   - 联网搜索：若需 MCP 方式（非 Harness 内置），须使用百炼通用 API Key（`sk-xxx`）开通 MCP 服务（[联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)）。

## 限制和注意事项

- **地域与协议隔离**：仅支持华北2（北京）；Token Plan、Coding Plan、按量付费三者 API Key 与 Base URL 完全隔离，混用将导致 401/403 错误或意外扣费（[快速开始（个人版）](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)、[快速开始（团队版）](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)）。  
- **使用场景限制**：严禁用于生产环境自动化脚本、后台定时任务或批量 API 调用；仅限交互式开发工具使用（[个人版订阅前须知](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)、[团队版使用细则](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)）。  
- **额度与并发**：个人版任一窗口（5 小时或 7 天）限额触顶即暂停服务，即使另一窗口有余量；团队版无窗口限制，但坐席额度用尽后需购买共享用量包或升配（[常见问题（个人版）](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)、[常见问题（团队版）](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)）。  
- **模型与工具兼容性**：多模态生成模型（如 `happyhorse-1.1-t2v`）必须通过异步任务流程（提交→轮询→下载），且 Credits 在任务完成时结算，可能集中触发限额（[接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)）。  
- **数据安全**：团队版明确承诺“不使用对话数据训练模型”；个人版数据用于服务改进（[Token Plan 个人版概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)、[Token Plan 团队版概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)）。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)


