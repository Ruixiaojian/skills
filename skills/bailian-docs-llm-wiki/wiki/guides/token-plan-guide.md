# token plan guide

[Token](../concepts/token.md) Plan 团队版是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 统一计量，支持文本与图像生成模型，兼容主流 AI 编程及智能体工具。其核心面向团队协作场景，提供席位管理、用量分析与多模型灵活切换能力，所有调用均通过专属 API Key 和隔离 Base URL 进行鉴权与路由。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 团队版支持以下精确匹配的模型 ID（区分大小写，版本号必须完全一致）：  
- **文本模型**：`qwen3.7-max`（限时活动）、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.6-flash`、`deepseek-v4-pro`、`deepseek-v4-flash`、`deepseek-v3.2`、`kimi-k2.7-code`、`kimi-k2.6`、`kimi-k2.5`、`glm-5.2`、`glm-5.1`、`glm-5`、`MiniMax-M2.5`；  
- **图像生成模型**：`qwen-image-2.0`、`qwen-image-2.0-pro`、`wan2.7-image`、`wan2.7-image-pro`。  

> **注意**：文档 10（`raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md`）中列出的 `qwen3.5-plus`、`qwen3-coder-next` 等模型属于 Coding Plan 套餐，**不在 [Token](../concepts/token.md) Plan 团队版支持范围内**，该文档混淆了两个独立产品线。请严格以 [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 中的白名单为准。

图像生成模型需通过工具扩展机制（如 Slash Command、Skill 或 Agent）接入，**不可直接通过文本模型 Base URL 调用**，详见 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。  
部分模型（`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.6-flash`）原生支持联网搜索、代码解释器等 5 种内置工具，调用不额外收费，Credits 统一抵扣；其余模型需通过 MCP 服务接入工具能力，MCP 调用单独计费（如联网搜索 MCP 免费额度用尽后按 29 元/千次计费），详见 [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| **API Key** | Token Plan 专属密钥，格式为 `sk-sp-xxxxx`，仅在首次生成或重置时完整显示一次，后续仅脱敏显示（如 `sk-sp-****`）。丢失后需重置，原 Key 立即失效。 | [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md) |
| **Base URL** | 必须配套使用：<br>- OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>- Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md) |
| **模型 ID** | 必须逐字符完全匹配白名单，禁止版本兼容推理（如 `qwen3.7-max` ≠ `qwen3.7-max-2026-01-23`）。 | [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) |
| **Credits 抵扣顺序** | 1. 坐席月度额度 → 2. 共享用量包（优先抵扣最近到期）→ 3. 全部用尽后服务暂停。 | [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) |

## 使用方式

1. **订阅与分配**：主账号或已授权 RAM 用户登录 [Token Plan 控制台](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/token-plan)，完成套餐购买后，在「我的订阅」→「分配座席」中为成员分配席位，系统自动生成 API Key 和 Base URL。  
2. **配置工具**：将 API Key 和对应协议的 Base URL 配置至兼容工具（如 Cursor、Qwen Code、Claude Code 等），确保协议匹配（OpenAI 协议配 `/compatible-mode/v1`，Anthropic 协议配 `/apps/anthropic`）。  
3. **调用模型**：  
   - 文本模型：直接指定模型 ID（如 `qwen3.6-plus`）发起请求；  
   - 图像生成模型：需按工具规范配置扩展（如 Claude Code 的 Slash Command、OpenCode 的 Agent），调用 `multimodal-generation` API endpoint；  
   - 工具调用：对支持内置工具的模型，启用 Responses API 即可自动触发；对其他模型，需先开通 MCP 服务并配置至工具（如联网搜索 MCP 地址为 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`，鉴权使用百炼通用 API Key `sk-xxx`）。  

## 限制和注意事项

- **地域限制**：Token Plan 团队版目前仅支持 **华北2（北京）** 地域，跨地域调用将失败。  
- **使用范围限制**：仅限在兼容的 AI 编程与智能体工具中**交互式使用**，禁止用于自动化脚本、应用后端或批量调用。违规可能导致订阅暂停或 API Key 封禁。  
- **API Key 隔离**：Token Plan、Coding Plan 和按量付费三者的 API Key 与 Base URL 完全隔离，混用会导致 401/403 错误或意外按量扣费。  
- **席位绑定**：每个席位绑定唯一成员，不可共享；回收席位后原 API Key 失效，重新分配将生成新 Key。  
- **额度重置规则**：坐席月度 Credits 在订阅周期结束时重置，**不累积**；共享用量包有效期为 1 个月，到期自动清零，不随坐席周期重置。  
- **错误处理**：常见报错如 `404 model 'xxx' not found` 表示模型 ID 不在白名单或拼写错误；`401 InvalidApiKey` 通常因误用通用 API Key（`sk-xxx`）或 Base URL 不匹配导致，需核对 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md) 中的配置指引。

## 来源文档

- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)
- [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/web-search-for-coding-plan.md)
- [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)


