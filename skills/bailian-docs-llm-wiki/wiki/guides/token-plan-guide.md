# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 统一计量，支持文本、多模态模型及 Harness 工具，适配主流 AI 编程与智能体工具。其核心设计面向开发者实际工作流，通过 `sk-sp-` 开头的专属 API Key 与协议兼容的 Base URL 实现额度抵扣，不支持非交互式自动化调用场景。服务当前仅限华北2（北京）地域使用 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 支持的模型与功能

[Token](../concepts/token.md) Plan 分为个人版与团队版，均支持广泛的模型能力与扩展工具：

- **模型类型**：覆盖文本生成（qwen3.8-max、glm-5.2、kimi-k2.7-code 等）、视觉理解（qwen3.7-plus、qwen3.6-plus）、图像生成（qwen-image-3.0-pro、wan2.7-image）、视频生成（happyhorse-1.1-t2v）、语音合成（qwen-audio-3.0-tts-plus）及实时语音对话（qwen-audio-3.0-realtime-plus）等。完整列表详见 [Token Plan 个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md) 和 [Token Plan 团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md) 文档。
  
- **Harness 工具**：仅 qwen3.7 及 qwen3.8 系列模型原生支持，包括 `web_search`（联网搜索）、`code_interpreter`（代码解释器）、`web_extractor`（网页抓取）、`i2i_search`（以图搜图）、`t2i_search`（文搜图）。工具调用需通过 Responses API 触发，Chat Completions 协议客户端无法自动激活 [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。

- **多模态生成模型**：图像、视频、语音类模型使用独立接口（如 `/api/v1/services/aigc/multimodal-generation/generation`），**不可通过标准 Chat Completions Base URL 直接调用**，必须通过工具的 Skill/Slash Command/Agent 扩展机制接入 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

> **注意**：文档 4 明确指出“每 5 小时限额当前限时取消，暂不限制”，但文档 1 和文档 6 均仍列出该限额项。根据最新 FAQ，个人版实际已暂停执行 5 小时限额，仅保留 7 天固定窗口；团队版则完全无此限制。开发者应以文档 4 的说明为准。

## 关键参数

- **API Key**：必须为 `sk-sp-` 开头的专属密钥，与百炼通用 `sk-` 或 Coding Plan `sk-sp-`（不同 Base URL）密钥严格隔离。
- **Base URL**：
  - OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
  - Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
- **Credits 计费逻辑**：单次消耗由模型类型、[Token](../concepts/token.md) 数量、思考模式、工具调用等动态决定，非简单 Token × 固定单价。例如，视频生成随分辨率与时长线性增长消耗，[异步任务](../concepts/async-task.md)在完成时集中结算 [Token Plan 个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。
- **额度重置**：个人版支持手动重置 7 天限额（消耗重置次数），团队版无此机制，仅按月重置。

## 使用方式

1. **订阅与配置**：在华北2（北京）地域的百炼控制台完成订阅后，获取专属 API Key 与 Base URL [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)。
2. **工具接入**：将 Key 和 URL 配置至支持自定义协议的工具（如 Cursor、Claude Code、Qwen Code、Qoder、OpenClaw 等），无需 SDK。
3. **Harness 工具启用**：切换至 qwen3.7-plus 等支持模型，在对话中自然提问（如“帮我计算这个表格的平均值”），模型将自动调用 `code_interpreter`；若工具仅支持 Chat Completions，则需改用 Responses API 或选择兼容工具。
4. **多模态模型接入**：通过 Slash Command（Claude Code）、Skill（Codex/Qwen Code）或 Agent（OpenCode）等扩展机制调用独立接口，不可直接 POST 到标准 Base URL。

## 限制和注意事项

- **地域限制**：强制要求华北2（北京）地域，控制台需手动切换 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。
- **使用范围**：严禁用于自动化脚本、批量任务或应用后端；仅限交互式开发工具使用。违规可能导致 Key 封禁。
- **并发与性能**：
  - 个人版：Lite/Standard/Pro 套餐分别支持 1–2 / 3–4 / 6–8 个 Agent 并发；高峰期可能排队。
  - 团队版：多租户隔离，高峰期不排队，但存在动态并发上限，触发时需降频重试。
- **额度机制差异**：
  - 个人版：7 天固定窗口限额，额度不结转，触顶即停；可购用量包（20,000 Credits/100 元）补充。
  - 团队版：月度总额度（按坐席计），无窗口限制；超限后可购共享用量包（625,000 Credits/5000 元）。
- **数据安全**：团队版承诺不使用对话数据训练模型；个人版数据授权条款见服务协议第 5.2 条。
- **API Key 管理**：Key 泄露需立即重置，旧 Key 立即失效；续费不变更 Key，退订重购则 Key 更新。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-for-coding-plan.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)


