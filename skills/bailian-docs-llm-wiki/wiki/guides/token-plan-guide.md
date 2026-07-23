# token plan guide

Token Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 为统一计量单位，支持文本、图像、视频生成及 Harness 工具调用，适用于个人开发者与团队协作场景。服务当前仅限华北2（北京）地域使用，需在控制台手动切换地域后方可购买与调用。Token Plan 分为个人版与团队版，二者独立计费、额度不共享，且 API Key 与 Base URL 完全隔离，不可混用。

## 支持的模型/功能

Token Plan 支持多模态模型与扩展能力，覆盖推理、视觉理解、图片/视频生成等场景：

- **文本与推理模型**：`qwen3.8-max-preview`（预览版，享限时 1 折+夜间 0.2 折）、`qwen3.7-plus`、`qwen3.6-plus`、`deepseek-v4-pro`、`glm-5.2`、`kimi-k2.7-code` 等；
- **图像生成模型**：`qwen-image-2.0`、`wan2.7-image`、`qwen-image-2.0-pro`、`wan2.7-image-pro`；
- **视频生成模型**：`happyhorse-1.1-t2v`、`happyhorse-1.1-i2v`、`happyhorse-1.1-r2v`；
- **Harness 工具**（仅 qwen3.7+/qwen3.8 系列原生支持）：联网搜索（`web_search`）、代码解释器（`code_interpreter`）、网页抓取（`web_extractor`）、文搜图（`t2i_search`）、图搜图（`i2i_search`），详见 [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)；
- **视觉理解能力**：`qwen3.8-max-preview`、`qwen3.7-plus` 等模型原生支持；`glm-5`、`MiniMax-M2.5` 等纯文本模型需通过 Skill/Agent 辅助实现，详见 [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)；
- **多模态生成模型接入**：需通过工具扩展机制（如 Slash Command、Skill、Agent）调用独立 API 接口，例如 `/text-to-image` 或 `@image-analyzer`，具体路径与配置见 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

> **注意**：文档 10（Coding Plan 概述）中列出的模型白名单（如 `qwen3-coder-next`）**不适用于 Token Plan**。Token Plan 的模型支持范围以 [Token Plan 个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md) 和 [Token Plan 团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md) 文档为准，二者均明确列出 `qwen3.8-max-preview`、`qwen3.7-plus` 等型号，且未将 `qwen3-coder-*` 系列纳入支持列表。

## 关键参数

- **API Key**：Token Plan 专属 Key 以 `sk-sp-` 开头，生成后仅完整显示一次，需立即复制保存；与百炼通用 Key（`sk-` 开头）及 Coding Plan Key 严格隔离；
- **Base URL**：
  - OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
  - Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
- **Credits 计费逻辑**：单次调用消耗 Credits 由模型类型、输入/输出 tokens、缓存 tokens、思考模式及 Harness 工具调用共同决定，非固定值。例如 `qwen3.6-plus` 一次请求预估消耗约 3.18 Credits（含输入 8,349 tokens、缓存 40,794 tokens、输出 573 tokens）；
- **限额窗口**：
  - 个人版：双层窗口——**5 小时限额**（滚动计时，满 5 小时重置）与**7 天限额**（自首次调用起计时 7 天，非日历周期）；
  - 团队版：**月度总额度制**，无 5 小时/7 天限制，额度按坐席类型分配（标准 25,000/月，高级 100,000/月，尊享 250,000/月），到期未用完不结转。

## 使用方式

1. **订阅与配置**：
   - 访问 [Token Plan 购买页](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)，选择个人版或团队版套餐并完成支付；
   - RAM 用户需由主账号授予 `AliyunTokenPlanFullAccess` 及 `AliyunBSSReadOnlyAccess` 权限，并在百炼控制台分配订阅权限；
2. **获取凭证**：
   - 在控制台「我的订阅」页面生成 API Key，并选择对应协议的 Base URL；
   - 团队版管理员需先分配席位，再为成员生成专属 Key；
3. **工具接入**：
   - 将 API Key 与 Base URL 配置至 Cursor、Claude Code、Qwen Code、Qoder 等兼容工具；
   - 多模态模型（图像/视频）需通过工具扩展机制接入，如 Claude Code 的 Slash Command（`.claude/commands/text-to-image.md`）或 OpenCode 的 Agent（`.opencode/agents/image-analyzer.md`）；
4. **Harness 工具调用**：直接在对话中提问（如“查一下今天北京天气”），模型自动触发联网搜索；无需额外配置，但仅限 `qwen3.7-plus` 等指定模型。

## 限制和注意事项

- **地域限制**：Token Plan 全量服务仅支持 **华北2（北京）** 地域，控制台需手动切换；
- **使用场景限制**：严禁用于自动化脚本、生产环境后端服务或批量非交互式调用；仅限交互式 AI 编程与智能体工具（如 Cursor、Claude Code）内使用，违规将导致订阅暂停或 Key 封禁；
- **数据安全差异**：
  - 个人版：输入与输出内容可能用于服务改进与模型优化（见 [Token Plan 个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)）；
  - 团队版：明确承诺**不使用对话数据训练模型**，满足企业级隐私要求；
- **额度与升级**：
  - 个人版不支持退订，升级按剩余天数补差价，降配需到期后重新购买；
  - 团队版支持加购/升级坐席，但**不支持降配**；共享用量包（625,000 Credits/个）可临时补充额度，有效期 1 个月，优先抵扣最近到期包；
- **API Key 与 Base URL 必须配套使用**：混用 Token Plan Key 与 Coding Plan Base URL（`coding.dashscope.aliyuncs.com`）或百炼通用 Base URL（`dashscope.aliyuncs.com`）将导致 `401` 或 `403` 错误；
- **并发与性能**：个人版高峰期可能出现排队；团队版采用多租户隔离架构，高峰期不排队，且支持 SSO/钉钉集成与用量分析。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)


