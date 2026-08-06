# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 为统一计量单位，支持文本、[多模态](../concepts/multimodal.md)生成、实时语音及 Harness 工具调用。它面向个人开发者与团队提供预付费套餐，通过专属 API Key 和 Base URL 隔离计费链路，确保额度精准抵扣。服务当前仅支持华北2（北京）地域。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 支持覆盖文本、视觉、语音、视频全模态的主流模型，包括千问系列（`qwen3.8-max`、`qwen3.7-plus` 等）、万相（`wan2.7-image`、`wan2.7-image-pro`）、HappyHorse（`happyhorse-1.1-t2v` 等）、DeepSeek（`deepseek-v4-pro`）、GLM（`glm-5.2`）、Kimi（`kimi-k2.7-code`）等。所有模型均为完整版，未量化压缩或功能裁剪 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

Harness 工具（联网搜索、代码解释器、网页抓取、文搜图、以图搜图）已集成至 `qwen3.7-plus`、`qwen3.7-max`、`qwen3.8-max` 等模型，需通过 Responses API 调用方可触发并消耗 Credits [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。[多模态](../concepts/multimodal.md)生成模型（图像、视频、语音）不兼容标准 Chat Completions 接口，必须通过工具的 Skill/Slash Command/Agent 扩展机制接入 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

> **注意**：文档 2（团队版概述）中列出 `qwen3.8-max` 为 NEW，而文档 14（个人版概述）明确其享有“限时夜间五折”权益；但文档 2 同时声明 `qwen3.8-max-preview` 已下线并自动路由至 `qwen3.8-max`。这表明 `qwen3.8-max` 已正式发布，文档中“NEW”标识属冗余描述，应以实际模型 ID `qwen3.8-max` 为准，且该模型在个人版与团队版中能力一致。

## 关键参数

- **Credits 计量**：无固定 [Token](../concepts/token.md) 换算比例，实际抵扣由模型单价、输入/输出/缓存 Token 数、思考模式、工具调用次数等动态计算，公式为 `Credits = 模型推理用量（百万） × 单价（元/百万） × 官网折扣 × 100` [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。
- **限额机制**：
  - *个人版*：采用双重窗口——**5 小时滚动限额**（当前限时取消）和**7 天固定窗口限额**（自首次调用起计时，不按日历重置），任一触顶即暂停服务 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)。
  - *团队版*：采用**月度总额度制**，无窗口限制，额度按订阅月一次性发放，到期未用完不结转 [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)。
- **并发与席位**：个人版按档位限制并发 Agent 数（Lite: 1–2 个，Pro: 6–8 个）；团队版以“坐席”为最小单位，每个坐席绑定独立成员与 API Key，不可共享 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 使用方式

1. **订阅与配置**：在华北2（北京）地域控制台完成订阅后，于「我的订阅」页面获取专属 API Key（以 `sk-sp-` 开头）和 Base URL（OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`）[快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)。
2. **工具接入**：将上述 Key 和 URL 配置至支持自定义端点的 AI 工具（如 Cursor、Claude Code、Qwen Code、Qoder 等）。严禁混用百炼通用 API Key（`sk-`）或 Coding Plan 的 Key/Base URL，否则将导致鉴权失败或意外按量扣费 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)。
3. **高级功能接入**：
   - *Harness 工具*：切换至 `qwen3.7-plus` 等支持模型后直接提问，模型自动调用；若工具仅支持 Chat Completions，则无法触发，需改用 Responses API 或兼容工具 [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。
   - *[多模态](../concepts/multimodal.md)模型*：须通过工具扩展机制（如 Claude Code 的 Slash Command、OpenCode 的 Agent）调用独立 API 接口，不可直接使用 Chat Completions [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。
   - *联网搜索*：需额外开通 MCP 服务，并使用**百炼通用 API Key**（`sk-`）而非 Token Plan Key 进行鉴权 [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-for-coding-plan.md)。

## 限制和注意事项

- **地域与协议隔离**：服务仅限华北2（北京）地域；Token Plan、Coding Plan、按量付费三者 API Key 与 Base URL 完全隔离，必须严格配套使用，混用将导致 401/403 错误或按量扣费 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)。
- **使用范围限制**：仅限交互式 AI 工具（如 Claude Code、Cursor）中使用，**禁止用于自动化脚本、应用后端或非交互式批量调用**。违规使用可能导致订阅暂停或 API Key 封禁 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。
- **数据安全承诺**：团队版明确承诺“不使用对话数据训练模型”；个人版则说明数据将用于服务改进与模型优化，终止服务可停止后续授权 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。
- **额度与续费**：个人版暂不支持退订；续费仅延长有效期，不补充当前周期额度；团队版升级/加购按剩余时长折算费用，退订席位后 API Key 变更需重新配置 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)。
- **模型兼容性**：Coding Plan 与 Token Plan 模型白名单不同，例如 Coding Plan 明确要求精确匹配 `glm-5`，而 `GLM-5.1` 不被支持；Token Plan 个人版明确支持 `glm-5.2` [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-for-coding-plan.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)


