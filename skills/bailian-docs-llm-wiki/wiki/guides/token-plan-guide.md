# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 统一计量，支持多种 AI 编程和智能体工具。它提供个人版和团队版两个版本，满足从个人开发者到企业团队的不同需求，且与按量付费、Coding Plan 等计费模式完全隔离。

## 支持的模型与功能

[Token](../concepts/token.md) Plan 支持文本生成、图像生成、视频生成、实时语音对话等多种模型，以及联网搜索、代码解释器等 Harness 工具。所有模型均为完整版，未经过量化压缩或功能裁剪 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

- **个人版**：适配 Claude Code、Cursor、Qwen Code、Qoder、Qoder CN、OpenClaw 等主流 AI 编程和智能体工具；支持 qwen3.8-max、qwen3.7-plus、glm-5.2、wan2.7-image、happyhorse-1.1-t2v 等模型；Harness 工具（如 `web_search`、`code_interpreter`）需通过 Responses API 调用 [Token Plan 个人版概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。
- **团队版**：除个人版全部模型外，额外支持 kimi-k2.7-code、glm-5.1、MiniMax-M2.5 等三方模型；同样支持 Harness 工具，但仅限 qwen3.7/qwen3.8 系列模型原生调用 [Token Plan 团队版概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)。

> **注意**：文档 9 和文档 2 均列出 qwen3.7-plus 支持 Harness 工具，但文档 9 明确指出 qwen3.7-max 仅支持 `web_search`、`code_interpreter`、`web_extractor` 三项，而文档 2 的表格中未体现该限制。实际使用时请以控制台最新模型能力说明为准。

多模态生成模型（如图像、视频、语音合成）需通过 AI 工具的 Skill 或 Agent 扩展机制接入，不能直接通过 Chat Completions 接口调用 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

视觉理解能力方面，qwen3.7-plus、qwen3.6-plus、kimi-k2.5 等模型原生支持图片输入；glm-5、MiniMax-M2.5 等纯文本模型需通过 Skill/Agent 辅助实现 [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)。

## 关键参数

- **Credits 计量单位**：非固定 [Token](../concepts/token.md) 换算比例，实际抵扣取决于模型类型、Token 用量、思考模式及工具调用等因素。
- **限额机制**：
  - *个人版*：采用双层窗口限额——**5 小时限额**（自首次调用起计时）和**7 天限额**（自首次调用起计时），任一层触顶即暂停服务 [Token Plan 个人版常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)。
  - *团队版*：采用**月度总额度制**，无窗口限额，额度在订阅周期内可用，到期不结转 [Token Plan 团队版概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)。
- **并发能力**：个人版 Lite/Standard/Pro 套餐分别支持 1–2 / 3–4 / 6–8 个 Agent 并发；团队版基于多租户隔离架构，高峰期不排队。

## 使用方式

1. **订阅与配置**：仅支持华北2（北京）地域，在控制台完成订阅后，获取专属 `sk-sp-` 开头的 API Key 和对应 Base URL（OpenAI 兼容或 Anthropic 兼容）[Token Plan 个人版快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)。
2. **接入工具**：将 API Key 和 Base URL 配置至 Cursor、Claude Code、Qwen Code、Qoder 等兼容工具中即可使用。
3. **Harness 工具**：仅支持 Responses API，需确保工具通过该接口接入；调用成功后按次数抵扣 Credits [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。
4. **联网搜索**：需单独开通 MCP 服务，并使用百炼通用 API Key（`sk-` 开头）而非 Token Plan 专属 Key 进行鉴权 [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-for-coding-plan.md)。

## 限制和注意事项

- **地域限制**：Token Plan 目前仅支持华北2（北京）地域，购买和调用均需在此地域下进行。
- **使用范围限制**：严禁用于自动化脚本、批量调用或生产环境后端服务；仅限交互式开发场景 [Token Plan 个人版概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。
- **API Key 隔离**：Token Plan、Coding Plan 和按量付费的 API Key 与 Base URL 完全隔离，混用会导致鉴权失败或意外扣费。
- **数据安全**：团队版承诺不使用对话数据训练模型；个人版数据将用于服务改进，停止使用可终止后续授权。
- **升级与退订**：个人版不支持退订；团队版支持加购/升级席位，但不支持降配；续费仅延长有效期，不叠加当前周期额度。

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
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-for-coding-plan.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)


