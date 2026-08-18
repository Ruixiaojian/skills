# token plan guide

Token Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 统一计量，支持文本、多模态生成（图像/视频/语音）及 Harness 工具调用，兼容 OpenAI/Anthropic 协议。它面向个人开发者与团队提供两种独立计费模式，需在华北2（北京）地域使用，且必须配套使用 `sk-sp-` 开头的专属 API Key 与指定 Base URL 才能抵扣套餐额度。

## 支持的模型与功能

Token Plan 支持覆盖文本推理、视觉理解、图像生成、视频生成、语音合成与识别等全栈能力的模型，包括千问系列（`qwen3.8-max`、`qwen3.7-plus`、`qwen-image-3.0-pro` 等）、万相（`wan2.7-image`）、DeepSeek（`deepseek-v4-pro-0813`）、智谱（`glm-5.2`）、月之暗面（`kimi-k2.7-code`）及 HappyHorse（`happyhorse-1.1-t2v`）等。  
**注意**：个人版与团队版支持的模型列表存在差异。例如，`kimi-k2.7-code`、`glm-5.1`、`glm-5` 仅在团队版中明确列出 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)，而个人版文档未包含这些模型；同时，`qwen3.8-max-preview` 已下线，请求自动路由至 `qwen3.8-max`，建议更新配置 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。  
Harness 工具（联网搜索、代码解释器、文搜图等）仅对 `qwen3.7-plus`、`qwen3.7-max`、`qwen3.8-max` 等特定 Qwen 模型原生支持，且**必须通过 Responses API 调用才触发并消耗 Credits**；若工具仅支持 Chat Completions 协议，则不会自动调用 Harness 工具，相关请求将按量付费 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。  
多模态生成模型（如图像、视频、语音）不通过标准 `/chat/completions` 接口调用，需借助 AI 工具的 Skill/Slash Command/Agent 扩展机制接入，例如在 Claude Code 中通过 `/text-to-image` 命令调用 `qwen-image-2.0` [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

## 关键参数

- **API Key 格式**：必须为 `sk-sp-` 开头的专属密钥，与百炼通用 `sk-` 或 Coding Plan 的 `sk-sp-`（不同 Base URL）严格隔离，不可混用。
- **Base URL**：
  - OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
  - Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
- **Credits 计费逻辑**：单次消耗由模型类型、Token 数量、思考模式、工具调用等动态决定，非固定 Token-to-Credits 比例。高消耗场景包括：视频生成（随分辨率/时长上升）、异步任务集中结算、长上下文缓存未命中等。
- **限额机制**：
  - **个人版**：采用 **7 天固定窗口限额**（自首次调用起计时），无自然周/月限制；5 小时限额当前已限时取消 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)。
  - **团队版**：采用 **月度总额度制**（按订阅日起算的“订阅月”，非自然月），无窗口限制，额度到期不结转。

## 使用方式

1. **订阅与配置**：在华北2（北京）地域的[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)完成购买；RAM 用户需主账号授予 `AliyunTokenPlanFullAccess` 及 `AliyunBSSReadOnlyAccess` 权限 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)。
2. **获取凭证**：在“我的订阅”页生成 `sk-sp-` API Key（仅显示一次，务必保存），并选择对应协议的 Base URL。
3. **工具接入**：将 Key 和 URL 配置至支持自定义协议的工具（如 Cursor、Claude Code、Qwen Code、Qoder、OpenClaw 等）。**严禁用于自动化脚本或后端服务**，仅限交互式开发场景。
4. **高级功能启用**：
   - **Harness 工具**：切换至支持模型（如 `qwen3.7-plus`），直接提问即可触发，无需额外配置（但需工具支持 Responses API）。
   - **视觉理解**：对纯文本模型（如 `glm-5`）可通过 Skill/Agent 调用 `qwen3.7-plus` 进行图片分析 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)。
   - **联网搜索**：需单独开通 MCP 服务（使用百炼通用 `sk-` Key 鉴权），与 Token Plan Credits 无关 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-for-coding-plan.md)。

## 限制和注意事项

- **地域强制**：所有调用必须在华北2（北京）地域发起，其他地域请求将失败。
- **额度不可共享/转移**：个人版与团队版额度完全独立，不可互通；团队版席位不可转让，移出成员后若已消耗 Credits，席位不返还资源池 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)。
- **并发与限流**：个人版档位限制并发 Agent 数（Lite: 1–2，Pro: 6–8）；团队版虽承诺“高峰期不排队”，但仍存在平台级并发限制，触发时需等待重试 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)。
- **关键风险点**：
  - 配置错误（如误用 `dashscope.aliyuncs.com` Base URL 或 `sk-` Key）将导致请求走按量计费通道，产生意外扣费；
  - 调用白名单外模型（如 `Qwen3-VL-Plus`）或未授权模型 ID（大小写/空格错误）将返回 `404 model_not_found`；
  - 视频生成等异步任务 Credits 在任务完成时统一结算，短时提交多个任务易致 7 天限额瞬时触顶。
- **数据与合规**：团队版承诺“不使用对话数据训练模型”；个人版数据授权条款适用于服务改进，终止使用可停止后续授权，但已授权数据不可撤回 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。

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
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-for-coding-plan.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)


