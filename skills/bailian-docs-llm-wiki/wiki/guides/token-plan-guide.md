# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼面向开发者推出的 AI 大模型统一订阅服务，以 Credits 为计量单位，支持文本、[多模态](../concepts/multi-modal.md)生成及 Harness 工具调用。它分为个人版（面向单人交互式开发）和团队版（面向多人协作与企业级管理），均仅限华北2（北京）地域使用。服务通过专属 `sk-sp-` 开头的 API Key 与隔离 Base URL 实现计费隔离，严禁用于生产环境自动化调用。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 支持覆盖推理、视觉理解、图像生成、视频生成、语音处理等能力的[多模态](../concepts/multi-modal.md)模型，以及联网搜索、代码解释器等 Harness 工具：

- **主流模型**：`qwen3.8-max-preview`（预览版，享限时 1 折+夜间 0.2 折优惠）、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro`、`wan2.7-image`、`happyhorse-1.1-t2v` 等（[完整列表见文档](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)）。
- **Harness 工具**：仅 `qwen3.7` 及以上系列模型原生支持，包括 `web_search`、`code_interpreter`、`t2i_search`、`i2i_search`、`web_extractor`（[接入说明详见](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)）。
- **[多模态](../concepts/multi-modal.md)生成**：图像生成（`qwen-image-2.0`、`wan2.7-image`）和视频生成（`happyhorse-1.1-t2v` 等）需通过工具扩展机制（如 Slash Command、Skill、Agent）调用独立 API（[接入指南见](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)）。
- **视觉理解**：`qwen3.7-plus`、`qwen3.6-plus`、`kimi-k2.5` 等模型原生支持图片输入；纯文本模型（如 `glm-5`）需通过 Skill 或 Agent 借助视觉模型实现（[配置方法见](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)）。

> **注意**：文档 8（Coding Plan 概述）中列出的 `qwen3-coder-next`、`qwen3-coder-plus` 等模型虽在 Coding Plan 中支持，但**未出现在 [Token](../concepts/token.md) Plan 个人版或团队版的任一支持模型列表中**，实际不可用。请以 [token-plan-personal-overview.md](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md) 和 [token-plan-team-overview.md](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md) 的白名单为准。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| **API Key** | 必须为 `sk-sp-` 开头的 Token Plan 专属密钥，与百炼通用 `sk-` Key 及 Coding Plan Key 完全隔离 | `sk-sp-xxxxxxxx` |
| **Base URL** | OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | 同上 |
| **Credits 消耗** | 动态计算，取决于模型类型、输入/输出 token 数、思考模式启用状态及 Harness 工具调用次数 | `qwen3.6-plus` 单次请求约 3.18 Credits（[计算示例见](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)） |
| **并发 Agent 数** | 个人版按档位限制：Lite（1–2）、Standard（3–4）、Pro（6–8）；团队版无硬性并发上限，依赖席位额度与系统负载 | Standard 套餐支持 3–4 个并发 Agent |

## 使用方式

1. **订阅与授权**  
   - 访问 [Token Plan 控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview) 完成购买。  
   - RAM 用户需由主账号授予 `AliyunTokenPlanFullAccess`（或 `ReadOnlyAccess`）及 `AliyunBSSReadOnlyAccess`（个人版）或 `AliyunBSSFullAccess`（团队版）策略，并在百炼控制台分配订阅权限（[授权步骤详见](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)）。

2. **获取凭证**  
   - 个人版：在「我的订阅」页面生成 API Key（仅显示一次）。  
   - 团队版：在成员管理页为成员分配席位后，为其生成专属 API Key（[操作流程见](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)）。

3. **配置工具**  
   - 将 API Key 与对应协议的 Base URL 配置至 Cursor、Claude Code、Qwen Code、Qoder 等兼容工具。  
   - 多模态生成与 Harness 工具需额外配置（如 Claude Code 的 Slash Command、OpenCode 的 Agent、MCP 服务等），具体路径与脚本参见各实践文档。

## 限制和注意事项

- **地域限制**：个人版与团队版均**仅支持华北2（北京）地域**，控制台需手动切换（[原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)）。
- **额度机制差异**：  
  - 个人版采用 **5 小时 + 7 天双窗口限额**（非日历周期，自首次调用起计时），任一窗口触顶即暂停服务；  
  - 团队版采用 **月度总额度制**（无窗口限制），支持加购共享用量包（625,000 Credits/个）补充额度（[对比详见](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)）。
- **使用场景限制**：  
  - 严禁用于 API 自动化调用（如后台服务、定时任务、批量脚本），仅限交互式开发工具内使用；违规将导致 API Key 封禁（[原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)）。  
  - 个人版数据授权条款允许用于服务改进；团队版明确承诺**不使用对话数据训练模型**。
- **模型与工具兼容性**：  
  - qwen3.8-max-preview 为预览模型，能力持续迭代，预览结束后可能下线或替换（[原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)）。  
  - 联网搜索 MCP 需使用**百炼通用 API Key（`sk-`）**，而非 Token Plan 专属 Key（[原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)）。  
- **其他**：API Key 重置或退订重购后会变更，需在工具中重新配置；同一账号可同时持有个人版与团队版，额度与计费完全独立。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)


