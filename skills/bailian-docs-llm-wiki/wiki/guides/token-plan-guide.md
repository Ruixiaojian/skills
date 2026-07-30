# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 统一计量，支持多种 AI 编程和智能体工具。该服务分为个人版和团队版，分别面向个人开发者与企业团队，提供文本、[多模态](../concepts/multi-modal.md)及 Harness 工具能力。所有功能当前仅支持华北2（北京）地域。

## 支持的模型与功能

[Token](../concepts/token.md) Plan 支持覆盖文本生成、视觉理解、图片生成、语音合成、视频生成等能力的[多模态](../concepts/multi-modal.md)模型，以及联网搜索、文搜图、图搜图、网页抓取、代码解释器等 Harness 工具。具体模型列表详见 [Token Plan 个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md) 和 [Token Plan 团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md) 文档。

- **个人版**：支持 `qwen3.8-max-preview`（预览版，享限时 1 折+夜间 0.2 折优惠）、`qwen3.7-plus`、`wan2.7-image`、`happyhorse-1.1-t2v` 等；Harness 工具需通过 Responses API 调用，仅 `qwen3.7`/`qwen3.8` 系列原生支持。
- **团队版**：除上述模型外，额外支持 `qwen-image-2.0`、`deepseek-v4-flash`、`kimi-k2.7-code` 等；同样仅 `qwen3.7`/`qwen3.8` 系列支持 Harness 工具调用。
- **[多模态](../concepts/multi-modal.md)生成模型**（图像/视频/语音）需通过工具扩展机制（如 Slash Command、Skill 或 Agent）接入，不可直接通过标准文本模型 Base URL 调用，详见 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

> **注意**：文档 13（Coding Plan概述）中提及的 `qwen3-coder-next`、`qwen3-coder-plus` 等模型未在 [Token](../concepts/token.md) Plan 任一版本的支持列表中出现，不应视为 Token Plan 可用模型。

## 关键参数

- **Credits 计费单位**：单次调用消耗由模型类型、Token 用量、思考模式及工具调用动态决定，实际消耗以控制台用量明细为准。
- **额度机制**：
  - *个人版*：采用双层窗口限额——**5 小时限额**（自首次调用起计时）和**7 天限额**（自首次调用起计时），任一触顶即暂停服务；额度不结转。
  - *团队版*：采用**月度总额度制**，无窗口限制；各坐席额度按月重置，不结转。
- **并发能力**：个人版 Lite/Standard/Pro 套餐分别支持 1–2 / 3–4 / 6–8 个 Agent 并发；团队版基于多租户隔离架构，高峰期不排队。
- **API Key 格式**：均为 `sk-sp-` 开头，与百炼通用 API Key（`sk-` 开头）及 Coding Plan Key 完全隔离，不可混用。

## 使用方式

1. **订阅与配置**：  
   访问 [Token Plan 控制台](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)，选择地域为**华北2（北京）**后完成订阅。RAM 用户需主账号授予 `AliyunTokenPlanFullAccess` 和 `AliyunBSSReadOnlyAccess` 权限，并在百炼账号管理中分配权限。

2. **获取凭证**：  
   - *个人版*：在“我的订阅”页面生成专属 API Key 和 Base URL（OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`）。  
   - *团队版*：需先在成员管理中分配席位，系统自动生成成员专属 API Key；Base URL 同上。

3. **接入工具**：  
   将凭证配置至 Cursor、Claude Code、Qwen Code、Qoder 等兼容工具。Harness 工具可直接在支持模型对话中触发；多模态模型需按 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md) 文档配置扩展机制。

4. **视觉理解**：  
   `qwen3.7-plus` 等原生支持视觉的模型可直接传入图片；`glm-5` 等纯文本模型需通过 Skill/Agent 调用视觉模型辅助分析，详见 [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)。

## 限制和注意事项

- **地域限制**：Token Plan 当前仅支持华北2（北京）地域，跨地域调用将失败。
- **使用范围限制**：严禁用于自动化脚本、后台定时任务或非交互式批量调用；违规可能导致订阅暂停或 API Key 封禁。
- **数据政策差异**：  
  - *个人版*：输入及生成内容可能用于服务改进与模型优化（参见[服务协议第 5.2 条](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html)）；  
  - *团队版*：明确承诺**不使用对话数据训练模型**。
- **额度补充**：个人版可购买用量包（20,000 Credits/100 元，有效期 1 个月）突破窗口限制；团队版可购买共享用量包（625,000 Credits/5,000 元，有效期 1 个月）供全体成员共享。
- **升级与退订**：个人版支持升配（按剩余时长补差价），但**不支持降配**；团队版支持加购/升级/退订席位，退订后 API Key 失效，需重新配置。
- **模型预览风险**：`qwen3.8-max-preview` 为预览模型，能力持续迭代，预览结束后可能下线或替换，不保证长期可用。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)


