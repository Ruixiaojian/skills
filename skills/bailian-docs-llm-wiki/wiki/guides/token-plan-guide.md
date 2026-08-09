# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 统一计量，支持文本、图像、视频、语音等[多模态](../concepts/multimodal.md)生成及 Harness 工具调用。它面向个人开发者与团队提供两种独立计费模式，地域限定为华北2（北京），需通过专属 API Key 和 Base URL 接入，与按量付费及 Coding Plan 完全隔离。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 支持以下核心能力：

- **模型类型**：文本生成（qwen3.5-plus 至 qwen3.8-max）、视觉理解（qwen3.6-plus、qwen3.7-plus、kimi-k2.5 等）、图像生成（qwen-image-2.0、wan2.7-image）、视频生成（happyhorse-1.1-t2v）、语音合成（qwen-audio-3.0-tts-plus）及实时语音对话模型。
- **Harness 工具**：仅 qwen3.7 和 qwen3.8 系列模型原生支持，包括联网搜索、代码解释器、网页抓取、文搜图、以图搜图等，需通过 Responses API 触发，[接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md) 详细说明了工具列表与调用约束。
- **[多模态](../concepts/multimodal.md)生成**：图像、视频、语音模型不兼容标准 Chat Completions 协议，必须通过工具扩展机制（如 Slash Command、Skill 或 Agent）接入，[接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md) 提供了 Claude Code、Qwen Code 等主流工具的完整配置示例。
- **视觉理解能力**：qwen3.6-plus 及以上版本原生支持图片输入；glm-5、MiniMax-M2.5 等纯文本模型需通过 Skill/Agent 辅助实现，[添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md) 文档明确了配置要点与 OpenCode/OpenClaw 的 modalities 字段要求。

> **注意**：文档 9（Coding Plan概述）中列出的模型白名单（如 `glm-5.1` 不支持）与 [Token](../concepts/token.md) Plan 实际支持范围存在差异。Token Plan 模型支持以控制台实时列表为准，且不继承 Coding Plan 的模型兼容性规则；Coding Plan 已于 2026 年 4 月 13 日停止 Lite 版续费，推荐迁移至 Token Plan，详见 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 关键参数

| 参数 | 说明 | 值域/示例 |
|------|------|-----------|
| **API Key** | Token Plan 专属密钥，以 `sk-sp-` 开头，与百炼通用 Key（`sk-`）和 Coding Plan Key 严格隔离 | `sk-sp-xxxxxxxx` |
| **Base URL** | 协议绑定地址，OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | 必须与 Key 配套使用 |
| **Credits 计量单位** | 所有调用（含模型推理、Harness 工具、[多模态](../concepts/multimodal.md)生成）均按实际消耗抵扣 Credits，非 Token 数 | 模型单价由抵扣系数决定，高价模型（如 qwen3.7-max）相同 Token 数下 Credits 消耗更高 |
| **限额窗口（个人版）** | 5 小时滚动窗口（当前限时取消）、7 天固定窗口（自首次调用起计时） | Lite 套餐：7 天限额 2,500 Credits；Pro 套餐：40,000 Credits |
| **额度机制（团队版）** | 月度总额度制，无滚动窗口限制，按订阅月发放全量额度 | 标准座席：25,000 Credits/座席/月；尊享座席：250,000 Credits/座席/月 |

## 使用方式

1. **订阅与授权**  
   - 地域切换至**华北2（北京）**后，在 [Token Plan 购买页](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview) 完成订阅。  
   - RAM 用户需主账号授予 `AliyunTokenPlanFullAccess` + `AliyunBSSReadOnlyAccess` 策略，并在百炼控制台分配订阅权限（[快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md) 与 [团队版快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md) 均明确此步骤）。

2. **获取凭证**  
   - 个人版：在「我的订阅」页面生成 API Key（仅显示一次，需立即复制）。  
   - 团队版：在成员管理页为成员分配席位后，系统自动生成专属 Key；成员无法查看完整 Key，重置后旧 Key 立即失效。

3. **接入工具**  
   - 配置 Key + Base URL 至 Cursor、Claude Code、Qwen Code 等工具（支持 OpenAI/Anthropic 协议）。  
   - Harness 工具：仅当工具支持 Responses API 时自动触发；若仅支持 Chat Completions，则调用不消耗套餐 Credits，转为按量计费（见 [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)）。  
   - 多模态模型：必须通过工具扩展机制接入（如 Claude Code 的 Slash Command），不可直接调用文本模型 Base URL（见 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)）。

## 限制和注意事项

- **地域强制约束**：仅支持华北2（北京）地域，控制台未切换地域将无法购买或调用，该限制在所有文档中一致强调。
- **额度隔离与不可迁移**：个人版与团队版 Credits 完全独立，不可共享或转换；Coding Plan 与 Token Plan 为独立产品，无法升级或迁移（[Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 明确说明）。
- **并发与限流**：个人版并发 Agent 数受档位限制（Lite：1–2 个；Pro：6–8 个）；所有套餐均不公开 TPM/RPM 阈值，限流由系统动态调整，建议精简上下文、降低请求频率（[常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)）。
- **使用场景限制**：个人版禁止用于生产环境自动化调用（如后台脚本、定时任务），仅限交互式开发；团队版无此限制，但承诺不使用对话数据训练模型（[Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)）。
- **用量包规则**：用量包需先持有有效套餐方可购买，最多 5 个；额度无窗口限制，有效期 1 个月，到期作废（[常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)）。
- **API Key 泄露风险**：Key 重置后立即失效，所有设备需同步更新；多人共用同一 Key 违反个人版协议，团队版应通过成员管理分配独立 Key（[常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)）。

> **注意**：文档 7（联网搜索）要求使用百炼通用 API Key（`sk-`）调用 MCP 服务，而 Token Plan 专属 Key（`sk-sp-`）仅用于模型调用——二者用途严格分离，混用将导致鉴权失败或额外扣费。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-for-coding-plan.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)


