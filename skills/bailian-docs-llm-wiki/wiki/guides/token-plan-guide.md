# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 统一计量，支持文本、多模态生成及 Harness 工具调用，适配主流 AI 编程与智能体工具。服务目前仅支持华北2（北京）地域，个人版与团队版独立计费、额度不共享，且均禁止用于非交互式自动化场景。

## 支持的模型与功能

[Token](../concepts/token.md) Plan 支持覆盖文本生成、视觉理解、图片/视频生成、语音合成等能力的多模态模型，并集成联网搜索、代码解释器等 Harness 工具。  
- **个人版**支持 `qwen3.8-max-preview`（预览版）、`qwen3.7-plus`、`wan2.7-image`、`happyhorse-1.1-t2v` 等模型，详见[Token Plan 个人版概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)；  
- **团队版**额外支持 `qwen-image-2.0-pro`、`deepseek-v4-flash`、`kimi-k2.7-code` 等模型，且明确承诺不使用对话数据训练模型，详见[Token Plan 团队版概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)；  
- **Harness 工具**（如 `web_search`、`code_interpreter`）仅在 `qwen3.7-plus` 及更高版本（含 `qwen3.8-max-preview`）中原生支持，调用时按成功次数抵扣 Credits [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。

> **注意**：文档 1 与文档 5 均称 `qwen3.8-max-preview` 为“预览版”，但文档 1 提到“预览结束后该模型会下线或替换成正式版本”，而文档 2 和文档 5 仅强调“预览期间能力持续迭代升级”，未明确下线策略。实际行为以控制台最新公告为准。

## 关键参数

| 参数 | 个人版 | 团队版 |
|------|--------|--------|
| **额度机制** | 5 小时 + 7 天双窗口限额（任一触顶即暂停） | 固定月度额度（无窗口限制，到期清零） |
| **额度重置** | 不自动结转；可手动重置窗口起点 [Token Plan 个人版概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md) | 每月 1 日 00:00:00（UTC+8）自动重置，不结转 |
| **并发 Agent** | Lite：1–2 个；Standard：3–4 个；Pro：6–8 个 | 无显式并发数限制，但高峰期性能保障优于个人版 |
| **API Key 格式** | `sk-sp-xxxxx`（专属，不可与通用 Key 混用） | `sk-sp-xxxxx`（席位级独立生成，不可跨席位复用） |
| **Base URL** | OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | 同个人版，但需与对应席位的 API Key 配套使用 |

## 使用方式

1. **订阅与配置**：  
   - 访问[Token Plan 购买页](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)，选择个人版或团队版套餐；  
   - RAM 用户需主账号授予 `AliyunTokenPlanFullAccess` 和 `AliyunBSSReadOnlyAccess` 策略，并在百炼控制台分配权限；  
   - 在“我的订阅”页面生成 API Key（仅显示一次，务必保存），并获取 Base URL。

2. **工具接入**：  
   - 将 API Key 与 Base URL 配置至 Cursor、Claude Code、Qwen Code、Qoder 等兼容工具；  
   - 多模态生成模型（如 `wan2.7-image`）需通过 Slash Command/Skill/Agent 扩展机制接入，不可直接调用文本模型接口 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)；  
   - 视觉理解模型（如 `qwen3.7-plus`）需在 OpenCode 等工具中显式声明 `"modalities": {"input": ["text", "image"]}`，否则无法处理图片输入 [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)。

3. **Harness 工具启用**：  
   - 切换至支持模型（如 `qwen3.7-plus`），直接提问即可触发联网搜索或代码解释器，无需额外配置。

## 限制和注意事项

- **地域限制**：所有 [Token](../concepts/token.md) Plan 服务仅在华北2（北京）地域可用，跨地域调用将失败；  
- **使用范围**：严禁用于自动化脚本、批量任务、应用后端等非交互式场景，违规可能导致 API Key 封禁；  
- **额度补充**：个人版用量包需先订阅有效套餐方可购买，最多持有 5 个；团队版共享用量包按月失效，优先抵扣最近到期者；  
- **模型兼容性**：Coding Plan 与 Token Plan 的 API Key/Base URL 完全隔离，混用将导致鉴权失败或意外按量扣费；  
- **数据政策**：个人版数据可能用于服务优化；团队版明确承诺不用于模型训练；  
- **升级降配**：支持个人版/团队版档位升级（补差价生效），但均不支持降配，需到期后重新订阅。

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
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)


