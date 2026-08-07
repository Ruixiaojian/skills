# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 为统一计量单位，支持文本、多模态及 Harness 工具调用，适用于个人开发者与企业团队。其核心特点是地域限定（仅华北2）、专属 API Key 隔离链路、以及按套餐档位提供差异化额度与管理能力。所有调用必须使用 `sk-sp-` 开头的专属密钥与配套 Base URL，否则将落入按量计费通道 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 支持覆盖文本生成、视觉理解、图像/视频生成、语音合成与实时语音对话的全栈模型，同时集成联网搜索、代码解释器等 Harness 工具能力。

- **文本与推理模型**：`qwen3.8-max`、`qwen3.7-plus`、`glm-5.2`、`deepseek-v4-pro`、`kimi-k2.7-code` 等（[Token Plan 个人版概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)）；
- **多模态生成模型**：`wan2.7-image`、`happyhorse-1.1-t2v`、`qwen-audio-3.0-realtime-plus` 等，需通过工具扩展机制（如 Slash Command、Skill、Agent）接入，**不可直接通过 Chat Completions 接口调用** [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)；
- **Harness 工具**：仅 `qwen3.7-plus`、`qwen3.7-max`、`qwen3.8-max` 等 Qwen 系列模型原生支持，且**必须通过 Responses API 触发**；若客户端仅支持 OpenAI Chat Completions 协议，则工具不会自动调用，相关请求将按量计费 [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)；
- **视觉理解**：`qwen3.7-plus`、`qwen3.6-plus`、`kimi-k2.5` 等模型原生支持图片输入；`glm-5`、`MiniMax-M2.5` 等纯文本模型需通过 Skill/Agent 借力视觉模型实现，且需在配置中显式声明 `modalities.input = ["text", "image"]` [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)。

> **注意**：文档 4（Coding Plan概述）中列出的 `qwen3-coder-next`、`qwen3-coder-plus` 等模型未出现在 [Token](../concepts/token.md) Plan 个人版或团队版的支持列表中，属于 Coding Plan 白名单特有型号，**Token Plan 不支持**。实际调用时若指定此类模型 ID，将返回 `404 model 'xxx' not found or not supported` 错误。

## 关键参数

| 参数 | 说明 | 取值示例 |
|------|------|----------|
| **API Key** | Token Plan 专属密钥，以 `sk-sp-` 开头，与通用 `sk-` Key 完全隔离 | `sk-sp-xxxxxxxxxxxx` |
| **Base URL** | 必须与 API Key 配套使用：<br>- OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>- Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | 同上 |
| **地域** | 强制要求：所有 Token Plan 调用必须在 **华北2（北京）** 地域发起，控制台需手动切换 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) | `cn-beijing` |
| **Credits 计费因子** | 无固定 Token→Credits 换算比；实际消耗取决于模型单价、输入/输出/缓存 Token 数、思考模式启用状态及 Harness 工具调用次数 | 示例：`qwen3.6-plus` 单次请求约 3.18 Credits（见 [Token Plan 团队版概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)） |

## 使用方式

1. **订阅与授权**  
   - 访问 [Token Plan 购买页](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview) 完成订阅；  
   - RAM 用户需由主账号授予 `AliyunTokenPlanFullAccess` + `AliyunBSSReadOnlyAccess` 策略，并在百炼控制台分配订阅权限 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)。

2. **获取凭证**  
   - 在控制台「我的订阅」页面生成 API Key（仅显示一次，请立即保存）；  
   - 根据工具协议选择对应 Base URL（OpenAI 或 Anthropic）。

3. **配置工具**  
   - 将 API Key 与 Base URL 填入支持自定义端点的工具（如 Cursor、Claude Code、Qwen Code、Qoder、OpenClaw 等）；  
   - **多模态模型**：需通过工具扩展机制接入（如 Claude Code 的 Slash Command、OpenCode 的 Agent），详见 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)；  
   - **Harness 工具**：确保使用 `qwen3.7-plus` 等支持模型，并确认工具调用的是 Responses API（非 Chat Completions）。

4. **用量监控**  
   - 个人版：控制台「我的订阅」→「Token Plan」标签页查看 7 天限额及剩余 Credits；  
   - 团队版：控制台「用量分析」可查看成员级、模型级明细（仅所有者可见） [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)。

## 限制和注意事项

- **地域强制**：Token Plan 仅在华北2（北京）可用，其他地域调用将失败；
- **额度机制差异**：
  - 个人版：采用 **7 天滚动窗口限额**（5 小时限额当前限时取消）；额度不结转，触顶即暂停服务，可购用量包补充 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)；
  - 团队版：采用 **月度固定额度**，无窗口限制；额度按订阅月发放（非自然月），到期未用完不结转 [Token Plan 团队版概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)；
- **API Key 隔离**：Token Plan、Coding Plan、按量付费三者 Key 与 Base URL 完全独立，混用将导致鉴权失败（401）或意外扣费；
- **使用场景限制**：仅限交互式 AI 工具使用，**禁止用于自动化脚本、后端服务或批量调用**；违规可能导致订阅暂停或 Key 封禁 [订阅前须知](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)；
- **数据安全承诺**：团队版明确承诺“不使用对话数据训练模型”；个人版数据将用于服务改进，终止使用可终止后续授权 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)；
- **模型兼容性**：部分模型（如 `qwen3.8-max-preview`）已下线，请求将自动路由至正式版 `qwen3.8-max`，但需更新配置中的 Model ID [Token Plan 团队版概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-for-coding-plan.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)


