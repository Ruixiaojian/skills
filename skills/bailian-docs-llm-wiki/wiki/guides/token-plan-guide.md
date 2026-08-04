# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 为统一计量单位，支持文本、多模态生成模型及 Harness 工具，适配主流 AI 编程与智能体工具。该服务分为个人版和团队版，均仅支持华北2（北京）地域，需在控制台切换地域后方可购买与使用 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 支持覆盖文本生成、视觉理解、图片生成、视频生成、语音合成等能力的多模态模型，并集成联网搜索、代码解释器等 Harness 工具。

- **核心模型**：  
  - 千问系列：`qwen3.8-max`、`qwen3.8-max-preview`（预览版，能力持续迭代）、`qwen3.7-plus`、`qwen3.6-flash` 等；  
  - 图像生成：`wan2.7-image`、`qwen-image-2.0`；  
  - 视频生成：`happyhorse-1.1-t2v`、`happyhorse-1.1-r2v`；  
  - 语音合成：`qwen-audio-3.0-tts-plus`；  
  - 第三方模型：`glm-5.2`（智谱）、`deepseek-v4-pro`（DeepSeek）、`kimi-k2.7-code`（月之暗面）等。  
  > **注意**：`qwen3.8-max-preview` 在个人版和团队版中均标注为“预览版本”，但文档 3 和文档 4 均明确说明“预览期间模型能力会持续迭代升级”，且“预览结束后该模型会下线或替换成正式版本”——该描述一致，无矛盾；但需注意其非稳定正式模型，不建议用于生产环境长期依赖。

- **Harness 工具**（仅限 `qwen3.7`/`qwen3.8` 系列模型，且**必须通过 Responses API 调用**）：  
  `web_search`（联网搜索）、`code_interpreter`（代码解释器）、`web_extractor`（网页抓取）、`t2i_search`（文搜图）、`i2i_search`（图搜图）[接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。  
  > **注意**：Harness 工具**不支持通过 Chat Completions 接口调用**，若工具仅支持 OpenAI 标准接口，需确认其底层是否封装了 Responses API 或提供对应扩展机制。

- **多模态生成模型**（图像/视频/语音）：  
  使用独立 API 接口（如 `/api/v1/services/aigc/multimodal-generation/generation`），**不可通过标准文本模型 Base URL 直接调用**，必须通过工具的 Skill、Slash Command 或 Agent 扩展机制接入 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

## 关键参数

| 参数 | 说明 | 适用版本 |
|------|------|----------|
| **Credits** | 统一计费单位，按模型类型、[Token](../concepts/token.md) 用量、工具调用动态计算，实际消耗以控制台用量详情为准 | 全部 |
| **5 小时限额** | 自首次调用起开启 5 小时滚动窗口，触顶即暂停服务，额度不结转 | 仅个人版 |
| **7 天限额** | 自首次调用起开启 7 天滚动窗口（非固定日历周期），触顶即暂停服务，额度不结转 | 仅个人版 |
| **月度总额度** | 固定周期额度，每月重置，未用完不结转 | 仅团队版 |
| **并发 Agent 数** | Lite/Standard/Pro 套餐分别支持 1–2 / 3–4 / 6–8 个并发 Agent | 仅个人版 |
| **API Key 前缀** | 必须为 `sk-sp-` 开头，与百炼通用 `sk-` Key 及 Coding Plan Key 完全隔离 | 全部 |

## 使用方式

1. **地域与授权**：  
   - 控制台左上角切换至 **华北2（北京）**；  
   - RAM 用户需由主账号授予 `AliyunTokenPlanFullAccess` + `AliyunBSSReadOnlyAccess`（或 `AliyunBSSFullAccess`，见文档 6）策略，并在百炼控制台分配订阅权限 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)。

2. **获取凭证**：  
   - **API Key**：在「我的订阅」页面生成，仅显示一次，务必立即复制保存；  
   - **Base URL**：  
     - OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；  
     - Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`。

3. **接入工具**：  
   - 配置上述 Key 与 URL 至 Cursor、Claude Code、Qwen Code、Qoder、OpenClaw 等兼容工具；  
   - 多模态模型需按工具规范配置 Skill/Agent（如 Claude Code 的 Slash Command、OpenCode 的 Agent）；  
   - Harness 工具需切换至支持模型（如 `qwen3.7-plus`）并直接提问触发，无需额外配置。

## 限制和注意事项

- **地域限制**：个人版与团队版均**仅支持华北2（北京）**，跨地域调用将失败。
- **使用范围限制**：  
  - 严禁用于自动化脚本、批量任务、应用后端等非交互式场景；违规可能导致 API Key 封禁 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)；  
  - 个人版禁止账号共享；团队版 API Key 仅限分配成员本人使用。
- **额度机制差异**：  
  - 个人版采用双层限额（5 小时 + 7 天），任一触顶即停服；团队版为单层月度额度，无短期窗口限制；  
  - 用量包（个人版）与共享用量包（团队版）均有效期 1 个月，到期清零，不退款。
- **模型与协议隔离**：  
  - Token Plan、Coding Plan、按量付费三者 API Key 与 Base URL **完全不互通**；混用将导致鉴权失败（401）或意外扣费；  
  - Coding Plan 已于 2026 年 3 月 20 日起停止 Lite 新购，4 月 13 日起停止续费，推荐迁移至 Token Plan [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-for-coding-plan.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)


