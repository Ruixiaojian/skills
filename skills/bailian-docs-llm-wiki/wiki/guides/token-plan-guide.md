# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 为统一计量单位，支持文本、多模态生成及 Harness 工具调用，适用于个人开发者与团队协作场景。服务当前仅限华北2（北京）地域，需在控制台手动切换地域后方可购买和使用。其核心设计兼顾灵活性与可控性：个人版采用双窗口限额机制（5 小时滚动 + 7 天固定），团队版则采用月度总额度制，并提供席位管理与用量分析能力。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 支持覆盖文本、视觉、语音、视频等多模态能力的模型，以及联网搜索、代码解释器等 Harness 工具：

- **文本与推理模型**：`qwen3.8-max`、`qwen3.7-plus`、`deepseek-v4-pro`、`glm-5.2`、`kimi-k2.5` 等（[原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)）；
- **多模态生成模型**：图像生成（`wan2.7-image`、`qwen-image-2.0`）、视频生成（`happyhorse-1.1-t2v`）、语音合成（`qwen-audio-3.0-tts-plus`）及实时语音对话（`qwen-audio-3.0-realtime-plus`）；
- **Harness 工具**：`web_search`、`code_interpreter`、`t2i_search`、`i2i_search`、`web_extractor`，仅 `qwen3.7` 及 `qwen3.8` 系列模型原生支持，且**必须通过 Responses API 调用才可触发并抵扣套餐 Credits**；若工具仅支持 Chat Completions 协议，则 Harness 不生效，相关请求将按量计费（[原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)）；
- **视觉理解能力**：`qwen3.7-plus`、`qwen3.6-plus`、`kimi-k2.5` 等模型原生支持图片输入；对 `glm-5`、`MiniMax-M2.5` 等纯文本模型，可通过 Skill/Agent 代理调用视觉模型实现（[原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)）。

> **注意**：文档 1 和文档 14 均声明 `qwen3.8-max-preview` 已下线，请求自动路由至 `qwen3.8-max`，但文档 2 明确指出该预览版“已结束预览并正式下线”，而文档 14 仅称“已结束预览并正式下线”，未强调“正式下线”状态。实际行为一致（路由生效），但术语表述存在冗余，以文档 2 的明确说明为准。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| **Credits 计量单位** | 所有模型调用与 Harness 工具均按 Credits 抵扣，消耗由模型类型、[Token](../concepts/token.md) 数量、思考模式、工具调用次数等动态决定 | `qwen3.6-plus` 单次请求约 3.18 Credits（见文档 14） |
| **限额机制（个人版）** | 双窗口：5 小时滚动限额（当前限时取消）、7 天固定窗口限额；额度不结转 | Lite 套餐：7 天限额 2,500 Credits |
| **限额机制（团队版）** | 月度总额度制，无滚动/固定窗口限制；额度按订阅月一次性发放，到期清零 | 标准坐席：25,000 Credits/坐席/月 |
| **并发 Agent 数** | 个人版档位决定最大并发数（Lite: 1–2；Standard: 3–4；Pro: 6–8）；团队版无显式并发限制，依赖多租户隔离保障高峰性能 |
| **用量包** | 补充额度，无窗口限制，有效期 1 个月，需先订阅有效套餐方可购买 | 100 元/个，含 20,000 Credits（个人版）；5,000 元/个，含 625,000 Credits（团队版共享） |

## 使用方式

1. **地域与订阅**：务必在百炼控制台左上角切换至**华北2（北京）**，再访问 [Token Plan 购买页](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview) 完成订阅（[原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)）；
2. **获取凭证**：
   - API Key：以 `sk-sp-` 开头，仅在生成/重置时完整显示一次，需立即复制保存；
   - Base URL：OpenAI 兼容为 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，Anthropic 兼容为 `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`；
3. **接入工具**：将上述 Key 和 URL 配置至 Cursor、Claude Code、Qwen Code、Qoder 等兼容工具；**严禁用于自动化脚本或非交互式批量调用**；
4. **多模态与 Harness 接入**：
   - 多模态模型（图像/视频/语音）需通过工具的 Skill/Slash Command/Agent 扩展机制调用，不可直接使用 Chat Completions 协议（详见文档 6）；
   - Harness 工具仅在 Responses API 下自动触发，若工具不支持，需改用 Responses API 或选择兼容工具（如 OpenClaw、Hermes Agent）。

## 限制和注意事项

- **地域限制**：Token Plan（含个人版与团队版）当前仅支持华北2（北京）地域，跨地域调用将失败；
- **API Key 隔离**：Token Plan、Coding Plan、按量付费三者 Key 与 Base URL 完全隔离，混用将导致 401/403 错误或意外按量扣费；
- **额度重置**：个人版 7 天限额支持手动重置（2026 年 8 月 5 日起新用户获赠 1 次），重置后已消耗 Credits 归零重新累计；团队版无重置功能，仅靠月度自动重置；
- **升级与退订**：
  - 个人版支持升配（补差价，额度按剩余天数折算），**不支持降配**；订阅到期后重新购买将变更 API Key，需重新配置；
  - 团队版支持加购/升级/回收席位，但**已消耗 Credits 的席位不可退订**；续费仅延长有效期，不补充当期额度；
- **数据与安全**：个人版数据可能用于服务优化；团队版明确承诺**不使用对话数据训练模型**；
- **模型兼容性**：调用前须确认模型 ID 精确匹配白名单（如 `qwen3.7-plus` ≠ `qwen3.7`），大小写与版本号均敏感；部分模型（如 `deepseek-v4-flash-0731`）暂不支持 Responses API，无法调用 Harness 工具。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-for-coding-plan.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)


