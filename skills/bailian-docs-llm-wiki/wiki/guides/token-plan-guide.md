# token plan guide

Token Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 统一计量，支持多种 AI 编程和智能体工具。它提供个人版和团队版两种形态，分别面向个人开发者和企业团队，覆盖文本、多模态生成及 Harness 工具调用等能力。

## 支持的模型与功能

Token Plan 支持广泛的模型类型和扩展功能：

- **模型类型**：覆盖文本生成（如 `qwen3.8-max-preview`、`glm-5.2`）、视觉理解（`qwen3.7-plus`、`kimi-k2.5`）、图片生成（`wan2.7-image`、`qwen-image-2.0`）、视频生成（`happyhorse-1.1-t2v`）和语音合成（`qwen-audio-3.0-tts-plus`）等 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。
- **Harness 工具**：部分 Qwen 模型（`qwen3.7-plus`、`qwen3.8-max-preview`）原生支持联网搜索、代码解释器、网页抓取、文搜图、图搜图等工具，需通过 Responses API 调用 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。
- **多模态生成模型**：图像、视频、语音模型需通过 AI 工具的 Skill/Slash Command/Agent 扩展机制接入，不支持直接通过 Chat Completions 接口调用 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

> **注意**：文档 12 和文档 14 中关于 Coding Plan 的内容明确指出其已停止新购和续费，且与 Token Plan 是独立产品；而文档 1 中强调“推荐使用 Token Plan”，说明 Coding Plan 已被逐步替代，开发者应避免混淆两者配置。

## 关键参数

- **Credits 计量单位**：所有模型调用和 Harness 工具均按 Credits 抵扣，实际消耗由模型类型、Token 数量、思考模式及工具调用动态决定。
- **限额机制**：
  - *个人版*：采用双层窗口限额——**5 小时限额**（自首次调用起计时）和**7 天限额**（自首次调用起计时），任一层触顶即暂停服务 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)。
  - *团队版*：采用**月度总额度制**，无窗口限制，额度到期清零，支持共享用量包补充。
- **API Key 格式**：Token Plan 专属 API Key 以 `sk-sp-` 开头，与百炼通用 API Key（`sk-` 开头）及 Coding Plan Key 完全隔离，不可混用。

## 使用方式

1. **地域要求**：必须在华北2（北京）地域购买和使用，控制台左上角需手动切换 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-guide/token-plan-overview.md)。
2. **获取凭证**：
   - *个人版*：在控制台「我的订阅」页面生成 API Key 和 Base URL（OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`）。
   - *团队版*：管理员在「成员管理」中分配席位后，为成员生成专属 API Key 和 Base URL。
3. **工具接入**：将上述凭证配置到 Cursor、Claude Code、Qwen Code、Qoder 等兼容工具中即可使用；多模态模型需按工具规范配置 Slash Command 或 Skill。
4. **视觉能力启用**：对 `qwen3.7-plus` 等原生支持视觉的模型，直接切换模型并传入图片即可；对 `glm-5` 等纯文本模型，需通过 Skill/Agent 调用视觉模型辅助分析。

## 限制和注意事项

- **使用范围限制**：仅限交互式开发场景，严禁用于自动化脚本、批量调用或生产环境后端服务；违规可能导致 API Key 封禁。
- **数据授权差异**：
  - *个人版*：输入和输出内容可能用于服务改进与模型优化；
  - *团队版*：承诺不使用对话数据训练模型，满足企业级数据安全要求。
- **并发与性能**：
  - 个人版并发 Agent 数受套餐档位限制（Lite：1–2 个；Pro：6–8 个）；
  - 团队版基于多租户隔离架构，高峰期不排队。
- **额度重置与补充**：
  - 个人版支持手动重置 5 小时/7 天限额；
  - 用量包可突破套餐限额约束，但有效期仅 1 个月，到期作废；
  - 团队版共享用量包优先抵扣最近到期的包。
- **地域与网络**：当前仅支持华北2（北京）地域；海外用户需确保网络可达 `token-plan.cn-beijing.maas.aliyuncs.com`。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)


