# token plan guide

Token Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 统一计量，支持多种 AI 编程和智能体工具。它提供个人版和团队版两个版本，满足从个人开发者到企业团队的不同需求，但需注意当前仅支持华北2（北京）地域。

## 支持的模型/功能

Token Plan 支持文本生成、多模态（视觉理解、图片生成、视频生成、语音合成）、推理等能力，并集成 Harness 工具扩展模型功能。

- **核心模型**：千问系列（`qwen3.8-max-preview`、`qwen3.7-plus`、`qwen3.6-flash` 等）、DeepSeek（`deepseek-v4-pro` 等）、万相（`wan2.7-image`、`happyhorse-1.1-t2v` 等）、智谱 AI（`glm-5.2`）、月之暗面（`kimi-k2.7-code`）等 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。
- **Harness 工具**：支持联网搜索、文搜图、图搜图、网页抓取、代码解释器，仅限 `qwen3.7` 和 `qwen3.8` 系列模型通过 Responses API 调用 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。
- **多模态生成模型**：图像生成（`qwen-image-2.0`、`wan2.7-image`）、视频生成（`happyhorse-1.1-t2v`）、语音合成（`qwen-audio-3.0-tts-plus`）需通过工具的 Skill/Slash Command/Agent 机制接入，不支持直接通过 Chat Completions 接口调用 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

> **注意**：文档 1 和文档 4 均列出支持模型，但文档 4 中 `qwen3.6-plus` 的描述为“推理模型、视觉理解、文本生成”，而文档 2 中同模型未提视觉理解；文档 13 明确指出 `qwen3.6-plus` 支持视觉，因此以文档 2 和文档 13 为准，`qwen3.6-plus` 具备视觉理解能力。

## 关键参数

- **Credits 计费**：单次消耗由模型类型、Token 用量、思考模式及工具调用动态决定，实际消耗以控制台用量详情为准。
- **额度机制**：
  - **个人版**：采用双层固定窗口限额——每 5 小时和每 7 天独立计费，任一层触顶即暂停服务。例如 Standard 套餐为 3,000 Credits/5h 和 10,000 Credits/7d [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)。
  - **团队版**：采用月度总额度制，无窗口限制，如标准坐席为 25,000 Credits/坐席/月。
- **并发能力**：个人版 Pro 套餐支持 6–8 个 Agent 并发；团队版基于多租户隔离架构，高峰期不排队。

## 使用方式

1. **地域与授权**：必须将百炼控制台地域切换至**华北2（北京）**；RAM 用户需由主账号授予 `AliyunTokenPlanReadOnlyAccess` 或 `AliyunTokenPlanFullAccess` 及 `AliyunBSSReadOnlyAccess` 策略 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)。
2. **API Key 与 Base URL**：Token Plan 专属 API Key 以 `sk-sp-` 开头，Base URL 为 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（OpenAI 兼容）或 `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`（Anthropic 兼容），三者必须配套使用。
3. **工具接入**：配置后即可在 Cursor、Claude Code、Qwen Code、Qoder、OpenClaw 等工具中使用；Harness 工具需确保使用 Responses API；多模态模型需通过 Slash Command（Claude Code）或 Skill（Qwen Code）等扩展机制接入。

## 限制和注意事项

- **使用范围限制**：仅限在官方指定的交互式 AI 工具中使用，禁止用于自动化脚本、批量调用或应用后端。违规可能导致订阅暂停或 API Key 封禁。
- **数据安全**：个人版数据将用于服务改进与模型优化；团队版承诺不使用对话数据训练模型。
- **地域限制**：当前仅支持华北2（北京）地域，海外用户需确认网络连通性。
- **额度重置**：个人版支持手动重置 5 小时/7 天限额；团队版月度额度到期自动重置，不结转。
- **模型预览权益**：`qwen3.8-max-preview` 为预览模型，享有 1 折调用优惠（个人版额外夜间 0.2 折），但预览结束后可能下线或替换，活动规则以最新页面为准。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)


