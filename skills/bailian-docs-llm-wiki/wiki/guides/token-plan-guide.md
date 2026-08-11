# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 统一计量，支持文本、[多模态](../concepts/multi-modal.md)生成、语音及实时对话等模型，以及联网搜索、代码解释器等 Harness 工具。服务面向个人开发者与团队两类用户，提供独立的额度机制、API 接入方式和管理能力，当前仅支持华北2（北京）地域。[Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 明确了其作为统一抵扣平台的核心定位。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 支持覆盖文本、视觉、语音、视频的全模态模型，以及可扩展的 Harness 工具能力：

- **文本与推理模型**：`qwen3.8-max`、`qwen3.7-plus`、`deepseek-v4-pro`、`glm-5.2`、`kimi-k2.7-code` 等（详见 [Token Plan 团队版概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md) 和 [Token Plan 个人版概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)）；
- **[多模态](../concepts/multi-modal.md)生成模型**：图像生成（`qwen-image-2.0`、`wan2.7-image`）、视频生成（`happyhorse-1.1-t2v`）、语音合成（`qwen-audio-3.0-tts-plus`）及实时语音对话（`qwen-audio-3.0-realtime-plus`）；
- **Harness 工具**：仅 `qwen3.7` 和 `qwen3.8` 系列模型原生支持，包括 `web_search`、`code_interpreter`、`t2i_search`、`i2i_search`、`web_extractor`，需通过 Responses API 调用才触发并抵扣 Credits（[接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)）；
- **视觉理解能力**：`qwen3.7-plus`、`qwen3.6-plus`、`kimi-k2.5` 等模型原生支持图片输入；纯文本模型（如 `glm-5`）可通过 Skill/Agent 封装调用视觉模型实现间接支持（[添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)）。

> **注意**：文档 14（Coding Plan 概述）中列出的 `qwen3-coder-next`、`qwen3-coder-plus` 等模型未出现在 [Token](../concepts/token.md) Plan 任一版本的支持列表中，属 Coding Plan 专属模型，Token Plan 不支持。请勿在 Token Plan 配置中使用这些模型 ID，否则将返回 `404 model not found` 错误。

## 关键参数

| 参数 | 说明 | 取值/范围 |
|------|------|-----------|
| **API Key** | Token Plan 专属密钥，以 `sk-sp-` 开头，与百炼通用 Key（`sk-`）及 Coding Plan Key 完全隔离 | 必须完整复制，控制台仅显示脱敏格式（如 `sk-sp-****`） |
| **Base URL** | 协议兼容地址，按工具协议选择 | OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| **Credits** | 统一计费单位，消耗由模型类型、Token 数量、工具调用等动态计算 | 实际消耗以控制台用量明细为准，非简单 Token × 单价 |
| **限额窗口（个人版）** | 5 小时滚动 + 7 天固定双窗口，任一触顶即暂停服务 | 当前 5 小时限额已限时取消（见 [Token Plan 个人版概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)），7 天限额自首次调用起算 |
| **额度重置（个人版）** | 7 天限额支持手动重置，清零已用额度重新累计 | 每用户初始获赠 1 次权益（2026 年 8 月 5 日起生效） |

## 使用方式

1. **订阅与授权**  
   - 访问百炼控制台（华北2地域），完成个人版或团队版订阅；  
   - RAM 用户需由主账号授予 `AliyunTokenPlanFullAccess`（或 ReadOnly）及 `AliyunBSSReadOnlyAccess`（个人版）或 `AliyunBSSFullAccess`（团队版）策略，并在账号管理中分配权限（[快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md) / [Token Plan 团队版快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)）。

2. **获取凭证**  
   - 在「我的订阅」页面生成 API Key（仅显示一次，务必立即保存）；  
   - 根据所用工具协议选择对应 Base URL。

3. **配置工具**  
   - 将 API Key 与 Base URL 填入 Cursor、Claude Code、Qwen Code、Qoder 等兼容工具；  
   - [多模态](../concepts/multi-modal.md)模型（图像/视频/语音）需通过工具的 Skill/Slash Command/Agent 扩展机制接入，**不可直接通过 Chat Completions 接口调用**（[接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)）；  
   - Harness 工具需确保使用 Responses API（而非 Chat Completions），且模型为 `qwen3.7` 或 `qwen3.8` 系列（[接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)）。

4. **高级能力启用**  
   - 视觉理解：直接切换至 `qwen3.7-plus` 等原生支持模型，或为 `glm-5` 等模型配置 `image-analyzer` Skill（[添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)）；  
   - 联网搜索：需额外开通 MCP 服务（使用百炼通用 API Key `sk-`，非 `sk-sp-`），配置 Streamable HTTP Endpoint（[联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-for-coding-plan.md)）。

## 限制和注意事项

- **地域限制**：Token Plan（个人版与团队版）均**仅支持华北2（北京）地域**，跨地域调用将失败；
- **使用场景限制**：严禁用于自动化脚本、生产环境后端服务或非交互式批量调用；违规可能导致订阅暂停或 API Key 封禁（[Token Plan 个人版订阅前须知](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)）；
- **额度机制差异**：
  - 个人版：5 小时+7 天双窗口限额，用量包需先有有效套餐才能购买；
  - 团队版：月度总额度制（无滚动窗口），坐席额度到期不结转，共享用量包按“先到期先抵扣”原则使用；
- **Key/URL 隔离**：Token Plan、Coding Plan、按量付费三者 API Key 与 Base URL 完全不互通；混用将导致 401/403 错误或意外按量扣费（[Token Plan 团队版快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)）；
- **模型兼容性**：`qwen3.8-max-preview` 已下线，请求自动路由至 `qwen3.8-max`，建议更新配置中的 Model ID（[Token Plan 个人版概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)）；
- **RAM 用户用量查看**：被分配席位的成员**无法自行查看用量明细**，用量分析为所有者专属功能，需由主账号在控制台「用量分析」中查看（[Token Plan 团队版常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)）。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-for-coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)


