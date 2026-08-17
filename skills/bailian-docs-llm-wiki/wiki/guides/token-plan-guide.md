# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 统一计量，支持文本、图像、视频、语音等多模态模型及 Harness 工具调用。它面向个人开发者与团队提供两种独立套餐，通过 `sk-sp-` 开头的专属 API Key 和配套 Base URL 实现额度抵扣，不兼容按量付费或 Coding Plan 的凭证体系。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 支持广泛的模型与扩展能力，覆盖主流编程和智能体场景：

- **模型类型**：包括文本生成（如 `qwen3.8-max`、`deepseek-v4-pro-0813`）、图像生成（`qwen-image-2.0-pro`、`wan2.7-image`）、视频生成（`happyhorse-1.1-t2v`）、语音合成与识别（`qwen-audio-3.0-tts-plus`、`qwen-audio-3.0-asr-flash`）等。完整列表见 [Token Plan 团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md) 和 [Token Plan 个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md) 文档。
- **Harness 工具**：仅 `qwen3.7-plus`、`qwen3.7-max`、`qwen3.8-max` 等 Qwen 系列模型原生支持联网搜索、代码解释器、网页抓取、文搜图、以图搜图等功能，且**必须通过 Responses API 调用才可触发并抵扣 Credits**；若工具仅支持 Chat Completions 协议，则工具调用不会生效，相关请求将按量计费 [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。
- **多模态生成模型**：图像、视频、语音类模型需通过 AI 工具的 Skill、Slash Command 或 Agent 扩展机制接入，不可直接使用 Chat Completions 接口调用 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。
- **视觉理解**：`qwen3.7-plus`、`kimi-k2.5` 等模型原生支持图片输入；`glm-5`、`MiniMax-M2.5` 等纯文本模型需通过 Skill/Agent 借助视觉模型完成分析，且 OpenCode 等工具需在配置中显式声明 `"input": ["text", "image"]` 才能启用该能力 [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)。

> **注意**：文档 12（Coding Plan概述）明确指出其模型白名单为“精确字符串匹配”，而 [Token](../concepts/token.md) Plan 文档未设同等严格限制，但实际调用仍需确保模型 ID 完全一致且在控制台支持列表内。两者模型支持范围存在差异，不可混用。

## 关键参数

- **API Key**：必须为 `sk-sp-` 开头的专属密钥，在控制台「我的订阅」页面生成，仅显示一次，需立即保存。误用 `sk-`（按量）或 `sk-ws-`（WebSocket）密钥将导致按量扣费。
- **Base URL**：
  - OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
  - Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
- **地域约束**：当前**仅支持华北2（北京）**，控制台需手动切换地域后方可购买与使用 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-guide/token-plan-overview.md)。
- **Credits 计费逻辑**：单次消耗由模型单价、Token 数量、思考模式、工具调用次数等动态决定，非简单 Token × 固定系数。例如 `qwen3.6-plus` 一次请求可能消耗约 3.18 Credits（含输入、缓存、输出分项）[Token Plan 团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)。

## 使用方式

1. **订阅与授权**：  
   - 个人版/团队版均需在华北2（北京）地域购买；RAM 用户需主账号授予 `AliyunTokenPlanFullAccess` + `AliyunBSSReadOnlyAccess` 策略，并在百炼控制台分配相应权限 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)。
   - 团队版还需在「团队管理」中为成员分配席位，系统自动生成专属 API Key [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)。

2. **配置工具**：  
   将上述 API Key 与 Base URL 配置至支持 OpenAI/Anthropic 协议的工具（如 Cursor、Claude Code、Qwen Code、OpenClaw 等）。界面相似但协议不兼容的自研工具无法接入 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-guide/token-plan-overview.md)。

3. **高级功能接入**：  
   - **Harness 工具**：切换至支持模型后直接提问，无需额外指令；但务必确认工具支持 Responses API，否则无效 [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。  
   - **多模态生成**：需在工具中创建 Slash Command（Claude Code）、Skill（Codex/Qwen Code）或 Agent（OpenCode），调用专用 HTTP 接口，不可直连 Base URL [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。  
   - **联网搜索（MCP）**：需单独开通百炼通用 API Key（`sk-` 开头）驱动的 MCP 服务，与 Token Plan 专属 Key 分离 [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-for-coding-plan.md)。

## 限制和注意事项

- **额度机制差异**：  
  - 个人版采用 **7 天固定窗口限额**（Lite/Standard/Pro 分别为 2,500/10,000/40,000 Credits），窗口期内额度不结转；5 小时限额当前已限时取消 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)。  
  - 团队版采用 **月度总额度制**（标准/高级/尊享座席分别为 25,000/100,000/250,000 Credits/座席/月），无滚动窗口，到期未用完额度清零 [Token Plan 团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)。

- **并发与性能**：  
  - 个人版并发建议值为 Lite（1–2）、Standard（3–4）、Pro（6–8）个 Agent；团队版虽无明确并发数上限，但存在平台级动态限流，高峰时可能排队 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)。  
  - 团队版承诺“高峰期不排队”，依托多租户隔离架构，而个人版高峰期可能出现等待 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)。

- **合规与安全**：  
  - 严禁将 Token Plan API Key 用于生产环境自动化脚本、后台任务或批量调用；仅限交互式开发 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)。  
  - 团队版承诺“不使用对话数据训练模型”，个人版则遵循通用服务协议 [Token Plan 团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)。  
  - 同一 API Key 可在多台设备使用，但多人共用同一账号或 Key 违反条款，须使用团队版实现协作 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)。

- **其他关键限制**：  
  - 用量包仅限已订阅有效套餐后购买，最多持有 5 个，有效期 1 个月，额度无窗口限制 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)。  
  - 重置卡为一次性权益，用于立即重置个人版 7 天限额，非定期发放 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)。  
  - 个人版与团队版可同时持有、独立计费，但额度不共享、Key 不互通 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
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


