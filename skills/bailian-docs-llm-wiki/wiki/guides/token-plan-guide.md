# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 为统一计量单位，支持文本、多模态生成及 Harness 工具调用，适用于个人开发者与团队协作场景。服务当前仅支持华北2（北京）地域，需在控制台手动切换地域后方可购买与使用。其核心设计兼顾灵活性与可控性，通过分层限额（个人版）或月度配额（团队版）实现预算管理，并严格限定使用范围为交互式编程工具。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 支持覆盖文本生成、视觉理解、图片生成、视频生成、语音合成/识别等能力的多模态模型，以及联网搜索、代码解释器、网页抓取、文搜图、图搜图等 Harness 工具。具体支持列表因版本而异：

- **个人版**：支持 `qwen3.8-max-preview`（含限时夜间折上折）、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro`、`wan2.7-image`、`happyhorse-1.1-t2v` 等；Harness 工具需模型原生支持（如 `qwen3.8-max-preview`、`qwen3.7-plus`），详见[接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。
- **团队版**：模型范围更广，额外支持 `kimi-k2.7-code`、`deepseek-v4-flash`、`glm-5.1` 等；同样支持 Harness 工具，且承诺不使用对话数据训练模型 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)。

> **注意**：文档 1 和文档 2 均列出 `qwen3.8-max-preview` 的“限时夜间折上折”权益，但文档 11（团队版概述）仅提及“限时加量 10 倍”，未包含夜间优惠。该差异表明夜间权益可能仅限个人版，团队版用户应以控制台实时说明为准。

## 关键参数

- **Credits 计费**：单次消耗由模型类型、输入/输出 [Token](../concepts/token.md) 数、思考模式启用状态及 Harness 工具调用次数动态计算，实际消耗以控制台用量明细为准 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。
- **限额机制**：
  - *个人版*：采用双层固定窗口限额——**5 小时限额**（自首次调用起计时）和**7 天限额**（自首次调用起计时），任一触顶即暂停服务，额度不结转。
  - *团队版*：采用**月度总额度制**，无窗口限制，额度按坐席类型分配（标准/高级/尊享），到期未用完自动清零。
- **并发与 Agent**：个人版各档位对应不同并发上限（Lite：1–2 个，Pro：6–8 个）；团队版基于多租户隔离，高峰期不排队。

## 使用方式

1. **订阅与配置**：在华北2（北京）地域的[Token Plan 控制台](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/token-plan)完成购买；获取专属 API Key（以 `sk-sp-` 开头）及 Base URL（OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`）。
2. **工具接入**：将 API Key 与 Base URL 配置至支持的 AI 工具（如 Claude Code、Qwen Code、Cursor、OpenClaw 等）。详细步骤见[快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)。
3. **扩展能力**：
   - *Harness 工具*：直接在对话中提问，模型自动调用（如 `qwen3.7-plus` 调用 `web_search`），无需额外配置。
   - *多模态生成*（图像/视频）：需通过工具的 Skill/Slash Command/Agent 扩展机制接入，调用独立 API 接口，详见[接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。
   - *视觉理解*：对 `qwen3.7-plus` 等原生支持模型，直接传入图片；对 `glm-5` 等纯文本模型，需配置 `image-analyzer` Skill 或 Agent 辅助。

## 限制和注意事项

- **地域限制**：服务仅在华北2（北京）地域可用，跨地域调用将失败。
- **使用范围**：严禁用于自动化脚本、生产环境后端服务或非交互式批量调用；违规可能导致 API Key 封禁 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。
- **API Key 隔离**：Token Plan（`sk-sp-`）、Coding Plan（`sk-sp-` but different domain）、按量付费（`sk-`）的 API Key 与 Base URL 完全隔离，混用将导致鉴权失败或意外扣费。
- **模型兼容性**：部分工具（如 OpenCode）需在配置文件中显式声明 `modalities.input = ["text", "image"]` 才能启用视觉能力；多模态生成模型不可通过文本模型 Base URL 直接调用。
- **升级与退订**：个人版支持升配（补差价，额度立即生效），不支持降配；团队版支持加购/升级坐席，退订后 API Key 变更，需重新配置工具。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)


