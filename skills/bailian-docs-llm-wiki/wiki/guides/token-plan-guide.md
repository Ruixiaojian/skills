# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 为统一计量单位，支持文本、多模态生成及 Harness 工具调用，适配主流 AI 编程与智能体工具。服务目前仅支持华北2（北京）地域，个人版与团队版独立计费、额度不共享，且均需通过专属 API Key 与 Base URL 接入。[原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 明确指出其核心定位为“AI 编程和智能体工具的统一订阅入口”。

## 支持的模型与功能

[Token](../concepts/token.md) Plan 支持覆盖推理、视觉理解、图像/视频生成、语音合成等能力的多模态模型，并集成联网搜索、代码解释器等 Harness 工具。

- **模型范围**：  
  - 文本与推理：`qwen3.8-max-preview`（预览版，享限时 1 折+夜间 0.2 折）、`qwen3.7-plus`、`glm-5.2`、`deepseek-v4-pro`、`kimi-k2.5` 等；  
  - 图像生成：`wan2.7-image`、`qwen-image-2.0-pro`；  
  - 视频生成：`happyhorse-1.1-t2v`、`happyhorse-1.1-r2v`；  
  - 语音合成：`qwen-audio-3.0-tts-plus`。  
  完整列表见 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md) 与 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)。

- **Harness 工具**：  
  支持 `web_search`、`code_interpreter`、`t2i_search`、`i2i_search`、`web_extractor`，仅 `qwen3.7-plus`、`qwen3.8-max-preview` 等 Qwen 系列模型原生支持，调用按成功次数抵扣 Credits。详见 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。

- **视觉理解**：  
  `qwen3.7-plus`、`qwen3.6-plus`、`kimi-k2.5` 等模型原生支持图片输入；对 `glm-5` 等纯文本模型，可通过 Skill/Agent 封装视觉模型实现间接支持（如用 `qwen3.7-plus` 分析图片后返回结果）。[原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md) 提供了具体配置示例。

> **注意**：文档 12（Coding Plan）中声明 `qwen3-coder-next` 和 `qwen3-coder-plus` 为 Coding Plan 支持模型，但所有 [Token](../concepts/token.md) Plan 文档（1、2、10）均未将其列入支持列表，且明确限定模型 ID 必须精确匹配白名单。因此，`qwen3-coder-next` 和 `qwen3-coder-plus` **不支持** Token Plan，开发者应严格依据 Token Plan 文档中的模型 ID 列表选用。

## 关键参数

- **Credits 计费机制**：  
  单次调用消耗由模型类型、输入/输出 Token 数、思考模式启用状态及 Harness 工具调用共同决定，实际消耗以控制台用量明细为准。例如 `qwen3.6-plus` 一次请求可能消耗约 3.18 Credits（含输入、缓存、输出 tokens）。

- **额度结构**：  
  - **个人版**：双层窗口限额——**5 小时限额**（自首次调用起滚动计时）与**7 天限额**（自首次调用起固定窗口），任一触顶即暂停服务。Lite/Standard/Pro 套餐对应额度分别为 (700, 2500) / (3000, 10000) / (12000, 40000) Credits。  
  - **团队版**：**月度总额度制**，无窗口限制。标准/高级/尊享坐席分别为 25,000 / 100,000 / 250,000 Credits/坐席/月，未用完额度不结转。

- **并发与 Agent 限制**：  
  个人版 Lite/Standard/Pro 套餐分别支持 1–2 / 3–4 / 6–8 个 Agent 并发；团队版无显式并发上限，依托多租户隔离架构保障高峰期不排队。

## 使用方式

1. **订阅与凭证获取**：  
   在华北2（北京）地域的百炼控制台完成订阅。API Key 以 `sk-sp-` 开头，Base URL 固定为：  
   - OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`  
   - Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`  
   （注意：与 Coding Plan 的 `coding.dashscope.aliyuncs.com` 及通用 API 的 `dashscope.aliyuncs.com` 完全隔离）

2. **接入 AI 工具**：  
   将上述 API Key 与 Base URL 配置至 Cursor、Claude Code、Qwen Code、Qoder 等兼容工具。[原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md) 与 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md) 提供了详细步骤。

3. **扩展能力接入**：  
   - **多模态生成**（图像/视频/语音）：必须通过工具的扩展机制（如 Claude Code 的 Slash Command、Qwen Code 的 Skill）调用独立 API 接口，不可直接使用文本模型 Base URL。[原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md) 给出完整配置模板。  
   - **联网搜索（MCP）**：需额外开通百炼通用 API Key（`sk-xxx`）认证的 MCP 服务，Endpoint 为 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`，与 Token Plan API Key 分离使用。[原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md) 说明此关键区别。

## 限制和注意事项

- **地域限制**：强制要求华北2（北京）地域，控制台地域切换失败将导致购买或调用异常。
- **使用场景限制**：严禁用于自动化脚本、后台定时任务、生产环境后端服务等非交互式场景；仅限在官方指定工具（如 Cursor、Claude Code）中交互式使用。违规可能导致 API Key 封禁。
- **账号规范**：个人版禁止共享；团队版 API Key 与席位绑定，仅限分配成员本人使用。
- **数据政策**：个人版数据可用于服务改进；团队版明确承诺**不使用对话数据训练模型**。
- **额度补充**：个人版可购用量包（20,000 Credits/100 元，无窗口限制）；团队版可购共享用量包（625,000 Credits/5000 元，跨坐席共享）。
- **模型时效性**：`qwen3.8-max-preview` 为预览模型，能力持续迭代，预览结束后可能下线或替换，不保证长期可用。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)


