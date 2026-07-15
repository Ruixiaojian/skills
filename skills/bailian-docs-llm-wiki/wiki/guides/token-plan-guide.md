# token plan guide

Token Plan 团队版是阿里云百炼面向企业团队提供的 AI 大模型订阅服务，以 Credits 为统一计量单位，支持文本生成与图像生成模型，兼容主流 AI 编程与智能体工具。服务基于多租户隔离架构，承诺不使用对话数据训练模型，并仅在华北2（北京）地域提供。开发者需严格按白名单模型 ID 调用，配套专属 API Key（`sk-sp-` 开头）与 Base URL 使用。

## 支持的模型/功能

Token Plan 团队版支持的模型为精确字符串白名单，**必须逐字符完全匹配**，版本号或子型号任何差异均视为不支持（如 `qwen3-coder-max` 不在列表中即不可用）[Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。当前支持以下模型：

- **文本生成与视觉理解**：`qwen3.7-max`（限时活动）、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.6-flash`、`kimi-k2.7-code`、`kimi-k2.6`、`kimi-k2.5`、`glm-5.2`、`glm-5.1`、`glm-5`、`MiniMax-M2.5`、`deepseek-v4-pro`、`deepseek-v4-flash`、`deepseek-v3.2`
- **图像生成**：`qwen-image-2.0`、`qwen-image-2.0-pro`、`wan2.7-image`、`wan2.7-image-pro`

> **注意**：文档 7（Coding Plan 概述）中列出的 `qwen3-coder-next`、`qwen3-coder-plus`、`qwen3-max-2026-01-23` 等模型**未出现在 Token Plan 团队版支持列表中**，不可用于 Token Plan 订阅。二者模型白名单独立，不可混用。

核心功能包括：
- **模型内置工具调用**：`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.6-flash` 支持通过 Responses API 直接调用联网搜索、代码解释器、网页抓取、以图搜图、文搜图五种工具，费用统一从套餐 Credits 抵扣 [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)。
- **图像生成能力**：需通过工具的扩展机制（如 Slash Command、Skill 或 Agent）接入 `multimodal-generation` API，**不可通过文本模型 Base URL 直接调用** [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。
- **视觉理解能力**：`qwen3.6-plus`、`qwen3.7-plus` 等原生支持图片输入；非视觉模型（如 `glm-5`）需通过 Skill/Agent 辅助实现，但该能力属于 Coding Plan 文档范畴，Token Plan 团队版默认不提供此类 Skill 配置说明。

## 关键参数

| 参数 | 说明 | 取值/格式 |
|------|------|-----------|
| **API Key** | Token Plan 专属密钥 | 以 `sk-sp-` 开头，仅在创建或重置时完整显示一次，后续仅脱敏显示（如 `sk-sp-****`） |
| **Base URL** | 兼容 OpenAI/Anthropic 协议的端点 | OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| **Model ID** | 模型唯一标识符 | 必须严格匹配白名单（如 `qwen3.6-plus`），区分大小写，无空格 |
| **Credits** | 计费单位 | 按输入 tokens、缓存 tokens、输出 tokens 动态计算，优先抵扣坐席月度额度，再抵扣共享用量包 |

> **注意**：文档 3（快速开始）明确指出 Token Plan、Coding Plan 和按量付费三者的 API Key 与 Base URL **完全隔离，不可混用**；误用通用 API Key（`sk-`）或 Coding Plan Base URL 将导致 401/403 错误或意外按量扣费 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)。

## 使用方式

1. **订阅与分配**：在 [Token Plan 购买页面](https://common-buy.aliyun.com/token-plan/)完成坐席（标准/高级/尊享）订阅；管理员登录控制台，在「我的订阅」→「分配座席」为成员分配席位，系统自动生成专属 API Key。
2. **配置工具**：将 API Key 和对应协议的 Base URL 配置至 AI 工具（如 Cursor、Qwen Code、Claude Code 等）。确认工具协议（OpenAI vs Anthropic）与 Base URL 后缀（`/compatible-mode/v1` vs `/apps/anthropic`）严格匹配。
3. **调用模型**：直接使用支持的 Model ID 发起请求；如需工具调用，对 `qwen3.6-plus` 等模型启用 Responses API 即可自动触发；如需图像生成，按 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md) 文档配置 Slash Command 或 Skill。
4. **管理用量**：通过控制台「用量分析」查看团队/成员/模型级 Credits 消耗趋势，或在「我的订阅」页面监控额度剩余百分比与重置时间。

## 限制和注意事项

- **地域限制**：仅支持华北2（北京）地域，海外调用需自行确保合规性 [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。
- **使用范围限制**：**仅限在兼容的 AI 编程与智能体工具中交互式使用**，禁止用于自动化脚本、应用后端或批量调用；违规可能导致订阅暂停或 API Key 封禁。
- **API Key 规范**：每个席位绑定一个成员、一个 API Key，不可共享；丢失后需重置，原 Key 立即失效。
- **额度规则**：坐席月度额度到期自动重置，不累积；共享用量包有效期 1 个月，到期清零；抵扣顺序为「坐席额度 → 共享用量包 → 服务暂停」。
- **错误处理**：
  - `404 model 'xxx' not found`：检查模型 ID 是否拼写正确且在白名单中；
  - `401 InvalidApiKey`：确认使用 `sk-sp-` 开头 Key 及配套 Base URL；
  - `429 Allocated quota exceeded`：可能因额度用尽或 TPS/TPM 限流触发，需加购用量包或实施请求平滑策略；
  - `400 InvalidParameter: Range of input length`：输入超上下文长度，建议新建会话或切换更大上下文模型。

> **注意**：文档 4（常见问题）指出，Token Plan 团队版与 Coding Plan 是两个**完全独立的订阅计划，不支持相互转换**；退订重购会导致 API Key 和 Base URL 变更，需重新配置所有工具 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)。

## 来源文档

- [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)
- [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/web-search-for-coding-plan.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)


