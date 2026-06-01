# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，分为 **[Token](../concepts/token.md) Plan 团队版**（面向团队/企业，按 Credits 计量）和 **Coding Plan**（面向个人开发者，按调用次数计量）。本文汇总两种套餐的支持模型、接入方式、关键参数及使用限制，帮助开发者快速选型和接入。

## 产品对比

| 维度 | [Token](../concepts/token.md) Plan 团队版 | Coding Plan |
|------|-------------------|-------------|
| 适用场景 | 团队/企业日常办公 | 个人开发 |
| 支持模型 | 文本生成 + 图像生成 | 文本生成 |
| 计费方式 | 按 Token 消耗抵扣 Credits | 按模型调用次数 |
| 使用频次 | 无每 5 小时/每周限额 | 有频次限制 |
| 高峰期性能 | 多租户隔离，不排队 | 可能排队 |
| 数据安全 | 不使用数据训练模型 | 数据用于服务改进 |

详细对比见 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)。

## 支持的模型

### Token Plan 团队版

模型清单为精确字符串白名单，必须逐字符完全匹配：

| 品牌 | 模型 ID | 能力 |
|------|---------|------|
| 千问 | qwen3.7-max（限时活动：Credits 消耗减半） | 推理、文本生成 |
| 千问 | qwen3.6-plus | 推理、视觉理解、文本生成 |
| 千问 | qwen3.6-flash | 推理、视觉理解、文本生成 |
| 千问 | qwen-image-2.0 / qwen-image-2.0-pro | 图像生成 |
| 万相 | wan2.7-image / wan2.7-image-pro | 图像生成 |
| DeepSeek | deepseek-v4-pro / deepseek-v4-flash / deepseek-v3.2 | 推理、文本生成 |
| 月之暗面 | kimi-k2.6 / kimi-k2.5 | 推理、视觉理解、文本生成 |
| 智谱 AI | glm-5.1 / glm-5 | 文本生成 |
| MiniMax | MiniMax-M2.5 | 推理、文本生成 |

### Coding Plan

推荐模型：qwen3.6-plus、kimi-k2.5、glm-5、MiniMax-M2.5

更多模型：qwen3.5-plus、qwen3-max-2026-01-23、qwen3-coder-next、qwen3-coder-plus、glm-4.7

> **注意**：Token Plan 团队版与 Coding Plan 支持的模型列表不完全相同。例如 Token Plan 团队版支持 deepseek 和图像生成模型，而 Coding Plan 支持 qwen3-coder-next 等编码模型。请严格按各自文档中的白名单使用。

## 关键参数

### Token Plan 团队版

| 协议 | Base URL |
|------|----------|
| OpenAI 兼容 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Anthropic 兼容 | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |

- **API Key**：由管理员在管理后台为成员生成（格式为 `sk-sp-xxx`）
- **地域限制**：仅支持华北2（北京）

### Coding Plan

| 协议 | Base URL |
|------|----------|
| OpenAI 兼容 | `https://coding.dashscope.aliyuncs.com/v1` |
| Anthropic 兼容 | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |

- **API Key**：在 Coding Plan 页面获取（格式为 `sk-sp-xxx`）

> **注意**：Token Plan 团队版、Coding Plan 和百炼按量计费三者的 API Key 和 Base URL 互不相通，请勿混用。误用会导致报错 `InvalidApiKey` 或 `invalid api-key`。

## 快速开始（Token Plan 团队版）

详见 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)：

1. **订阅**：访问购买页面，选择坐席类型（标准 ¥198/月/25K Credits、高级 ¥698/月/100K Credits、尊享 ¥1398/月/250K Credits）
2. **获取凭证**：管理员在管理后台创建成员、分配席位、生成 API Key
3. **接入工具**：在 Claude Code、Cursor、Cline、OpenClaw 等工具中配置 API Key 和 Base URL

## 团队管理

Token Plan 团队版提供完整的团队管理能力，详见 [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)：

- **角色体系**：拥有者、管理员（可管理成员和席位）、成员（仅使用）
- **成员接入**：支持手动添加、SAML SSO、钉钉三种方式
- **席位管理**：支持分配、回收、升级、退订、批量操作
- **用量分析**：查看 Credits 消耗趋势、模型用量、成员用量

## Credits 计费机制（Token Plan 团队版）

单次消耗由模型类型、输入/缓存/输出 Token 用量共同决定。抵扣顺序：

1. 坐席套餐月度额度
2. 共享用量包（¥5000/625K Credits，优先抵扣最近到期的）
3. 全部用尽后服务暂停

## 工具调用

Token Plan 团队版支持两种方式扩展工具能力：

### 模型内置工具（qwen3.7-max / qwen3.6-plus / qwen3.6-flash）

通过 Responses API 直接使用，无需额外配置：
- 联网搜索、代码解释器、网页抓取、以图搜图、文搜图
- 不额外收费，Token 消耗从 Credits 中抵扣

### MCP 服务（其他模型）

通过百炼 MCP 广场接入，需要百炼通用 API Key（`sk-xxx` 格式，非套餐专属 Key）。详见 [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)。

## 图像生成模型接入

图像生成模型（qwen-image-2.0、wan2.7-image 等）使用独立接口，无法通过文本模型的 Base URL 调用。需通过工具的 Skill / Slash Command / Agent 机制接入，API 端点为：

```
POST https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

## 限制和注意事项

1. **使用范围**：仅限在兼容的 AI 编程和智能体工具中交互式使用，**禁止**用于自动化脚本或应用后端，违规可能导致订阅暂停或 API Key 封禁
2. **账号规范**：API Key 仅限分配的成员本人使用，不可共享或公开
3. **地域限制**：Token Plan 团队版仅支持华北2（北京）地域
4. **退订规则**：已有用量消耗的席位不可退订；Coding Plan 不支持退款
5. **Coding Plan 频次限制**：每 5 小时 6000 次、每周 45000 次、每月 90000 次（Pro 套餐）
6. **Coding Plan 数据授权**：输入和输出内容将用于服务改进与模型优化

> **注意**：Coding Plan Lite 套餐已于 2026 年 3 月 20 日停止新购，4 月 13 日停止续费与升级。已购用户可继续使用至到期。

## 来源文档

- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)
- [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)
- [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/web-search-for-coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)

