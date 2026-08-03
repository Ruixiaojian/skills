# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 统一计量，支持文本、多模态生成及 Harness [工具调用](../concepts/tool-use.md)，适用于个人开发者与团队协作场景。服务当前仅支持华北2（北京）地域，需在控制台手动切换地域后方可购买与使用。其核心设计目标是简化模型接入、统一计费口径，并通过分层限额或月度额度机制保障服务稳定性与公平性。

## 支持的模型与功能

[Token](../concepts/token.md) Plan 支持覆盖文本生成、视觉理解、图片/视频生成、语音合成等能力的多模态模型，以及联网搜索、代码解释器等 Harness 工具。  
- **主流模型**：`qwen3.8-max`、`qwen3.8-max-preview`（含限时 1 折+夜间折上折）、`qwen3.7-plus`、`wan2.7-image`、`happyhorse-1.1-t2v`、`glm-5.2`、`deepseek-v4-pro`、`kimi-k2.7-code` 等（完整列表见 [Token Plan 个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md) 和 [Token Plan 团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md) 文档）。  
- **Harness 工具**：仅 `qwen3.7-plus`、`qwen3.7-max` 及 `qwen3.8-max-preview` 等 Qwen 系列模型原生支持，包括 `web_search`、`code_interpreter`、`t2i_search`、`i2i_search`、`web_extractor`，且**必须通过 Responses API 调用**，不兼容 Chat Completions 接口 [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。  
- **多模态生成模型**（如图像/视频/语音）使用独立 HTTP API，需通过工具的 Skill、Slash Command 或 Agent 扩展机制接入，不可直接通过标准 OpenAI/Anthropic 兼容接口调用 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。  

> **注意**：文档 5（团队版概述）与文档 2（个人版概述）均列出 `qwen3.8-max-preview` 为预览模型，但文档 2 明确说明“预览期间模型能力会持续迭代升级”，而文档 5 未提迭代承诺；实际使用应以控制台实时模型列表为准，预览模型可能随时下线或变更行为。

## 关键参数

| 参数 | 个人版 | 团队版 |
|------|--------|--------|
| **地域要求** | 仅华北2（北京） | 仅华北2（北京） |
| **额度机制** | 双层窗口：每 5 小时 + 每 7 天固定限额（任一触顶即暂停） | 单层月度总额度（无窗口限制，到期清零） |
| **并发 Agent** | Lite: 1–2；Standard: 3–4；Pro: 6–8 | 无显式并发上限，依赖多租户隔离架构保障高峰不排队 |
| **API Key 格式** | `sk-sp-xxxxx`（专属，不可与通用 Key 混用） | `sk-sp-xxxxx`（席位级独立生成，不可跨成员共享） |
| **Base URL** | OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | 同个人版，但需配套团队版专属 Key 使用 |

- **Credits 消耗动态性**：单次调用消耗由模型类型、[Token](../concepts/token.md) 数量、思考模式启用状态及 Harness [工具调用](../concepts/tool-use.md)次数共同决定，**实际消耗以控制台「我的订阅」用量明细为准**，非静态定价表可完全覆盖。  
- **用量包**：个人版与团队版均支持，有效期 1 个月，额度不受套餐窗口/月度限额约束，但需先持有有效订阅方可购买。

## 使用方式

1. **订阅与授权**：  
   - 访问 [Token Plan 购买页](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)，选择个人版或团队版套餐并完成支付。  
   - RAM 用户需由主账号授予 `AliyunTokenPlanFullAccess`（或 ReadOnly）及 `AliyunBSSReadOnlyAccess` 策略，并在百炼控制台分配订阅权限 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)。  

2. **获取凭证**：  
   - 个人版：在「我的订阅」页面生成 `sk-sp-xxxxx` Key 并复制 Base URL。  
   - 团队版：管理员在「成员管理」中为成员分配席位后，系统自动生成专属 Key；成员无法自行查看完整 Key，需由管理员分发。  

3. **工具接入**：  
   - 将 Key 与对应 Base URL 配置至 Cursor、Claude Code、Qwen Code、Qoder 等兼容工具。  
   - 若需视觉理解能力，优先切换至 `qwen3.7-plus` 等原生支持模型；对 `glm-5` 等纯文本模型，需通过 Skill/Agent 调用视觉模型代理 [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)。  
   - 联网搜索等 MCP 服务需额外开通，且**必须使用百炼通用 API Key（`sk-xxx`）而非 Token Plan 专属 Key** 进行鉴权 [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)。  

## 限制和注意事项

- **严禁生产环境自动化调用**：Token Plan（含个人版与团队版）禁止用于 API 脚本、后台定时任务、自定义应用后端等非交互式场景；违规可能导致订阅暂停或 Key 封禁。  
- **数据使用条款差异**：个人版默认授权输入/输出数据用于服务优化；团队版明确承诺**不使用对话数据训练模型**，满足企业级隐私要求。  
- **地域与协议隔离**：所有 Token Plan 流量必须经 `token-plan.cn-beijing.maas.aliyuncs.com` 域名，混用 `dashscope.aliyuncs.com`（按量）或 `coding.dashscope.aliyuncs.com`（Coding Plan）将导致 401/403 错误或意外扣费。  
- **模型兼容性陷阱**：  
  - Coding Plan 与 Token Plan 模型白名单不完全重叠（如 Coding Plan 明确支持 `qwen3-coder-next`，而 Token Plan 文档未列），**不可假设模型互通**。  
  - 多模态生成模型（如 `wan2.7-image`）若直接通过 Chat Completions 接口调用，将返回 `400` 错误，必须走专用 multimodal-generation API。  
- **额度重置逻辑**：个人版 5 小时/7 天窗口自**首次调用时刻起滚动计算**，非固定日历周期；团队版月度额度在订阅周期结束日 00:00:00（UTC+8）重置，未用完额度不结转。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)


