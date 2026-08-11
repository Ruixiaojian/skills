# use chat client or development tool

阿里云百炼支持多种第三方 AI 工具通过 OpenAI 或 Anthropic 兼容协议接入，覆盖终端 CLI、IDE [插件](../concepts/plugin.md)、桌面客户端及低代码平台等场景。开发者可根据使用习惯选择合适工具，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan、按量计费）配置对应凭证。所有工具均需使用百炼提供的 API Key 与 Base URL，且不同计费方案的凭证不可混用。

## 支持的模型/功能

百炼支持的模型因计费方案而异，**[Token](../concepts/token.md) Plan 个人版与团队版仅限文本生成类模型**（如 `qwen3.8-max`、`qwen3.7-plus`、`glm-5.2`、`deepseek-v4-pro`），不支持图像、视频、语音等[多模态](../concepts/multi-modal.md)模型；**Coding Plan 和按量计费支持更广谱模型**，包括文生图（`wan2.6-t2i`）、文生视频、Qwen-VL、QVQ 等 [支持的模型](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#7f9c78ae99pwz)。  
> **注意**：Dify 等工作流平台明确[不支持 Token Plan 个人版、团队版和 Coding Plan 接入](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)，仅允许使用按量计费 API Key，否则可能触发违规封禁 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

常用模型能力概览：
- `qwen3.8-max`：支持 reasoning（思考模式）、超长上下文（983,616 tokens）、[多模态](../concepts/multi-modal.md)输入（text + image）
- `qwen3.7-max` / `qwen3.7-plus`：默认启用 thinking，支持 image 输入
- `qwen3.6-flash`：轻量级[多模态](../concepts/multi-modal.md)模型，适合高频低延迟场景
- `glm-5.2`、`deepseek-v4-pro`：纯文本推理模型，无原生多模态支持

部分工具（如 Claude Code、Qwen Code）支持子任务模型（`CLAUDE_CODE_SUBAGENT_MODEL`）与主模型分离配置，可提升复杂任务调度效率 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)。

## 关键参数

| 参数 | 说明 | 示例值 | 注意事项 |
|------|------|--------|----------|
| `API Key` | 百炼专属密钥，**严格按计费方案隔离** | `sk-xxx`（[Token](../concepts/token.md) Plan 个人版） | Token Plan 个人版/团队版/Coding Plan 的 Key 互不通用；按量计费 Key 必须与 Base URL 地域一致 |
| `Base URL` | 模型服务端点，分 OpenAI 兼容与 Anthropic 兼容两类 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（OpenAI）<br>`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`（Anthropic） | OpenAI 兼容路径为 `/compatible-mode/v1`，Anthropic 兼容路径为 `/apps/anthropic`；按量计费 URL 中 `{WorkspaceId}` 必须替换为真实 ID [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) |
| `Model ID` | 模型标识符，需与所选方案支持列表完全一致 | `qwen3.8-max`、`kimi-k2-6`（注意连字符替代小数点） | Cursor 等工具要求模型名标准化（如 `kimi-k2.6` → `kimi-k2-6`，`glm-5.2` → `glm-5-2`） |
| `enable_thinking` / `effort` | 启用思考模式及推理强度 | `"enable_thinking": true` 或 `"effort": "xhigh"` | Qwen3 系列模型需显式开启；部分工具（如 Cline）需勾选 **Enable R1 messages format** 才能生效 |

## 使用方式

### 1. 安装与初始化
- **CLI 工具**（OpenClaw、Hermes Agent、Claude Code、Qwen Code 等）：依赖 Node.js ≥18（OpenClaw 要求 ≥22.19.0），通过 `npm install -g` 或一键脚本安装 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)。
- **IDE [插件](../concepts/plugin.md)**（Cline、Qoder JetBrains [插件](../concepts/plugin.md)）：在 VS Code 或 JetBrains IDE 扩展市场搜索安装。
- **桌面客户端**（Cursor、Cherry Studio、Chatbox）：从官网下载安装包。
- **Web 平台**（Dify）：直接访问 cloud.dify.ai 部署应用。

### 2. 凭证配置
所有工具均需配置 `API Key` + `Base URL` + `Model ID`，但路径与格式各异：
- **OpenClaw**：编辑 `~/.openclaw/openclaw.json`，`models.providers.bailian-token-plan` 下声明模型数组；
- **Hermes Agent**：运行 `hermes config set` 命令或编辑 `~/.hermes/config.yaml`；
- **Cursor**：Settings > Models > OpenAI API Key + Override Base URL；
- **Dify**：安装「通义千问」插件后，在 Settings > Model Providers 中填入 API Key 并开关模型。

> **注意**：QwenPaw 等 GUI 工具提供可视化配置界面（Console > 设置 > 模型），避免手动编辑 JSON 文件出错 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)。

### 3. 验证与调试
- 发送简单请求（如 `"你好"`）观察是否返回响应；
- 使用 `/status`（Claude Code）或 `/model`（Qoder CLI）检查当前配置；
- 报错时优先核对 `401 Unauthorized`（Key/Base URL 不匹配）与 `400 InvalidParameter`（未启用 R1 格式或 thinking 参数缺失）。

## 限制和注意事项

- **计费方案适用范围严格限定**：Token Plan 个人版/团队版/Coding Plan **仅允许用于 AI 编程工具与 OpenClaw 类 Agent**（如 OpenClaw、Hermes Agent、Qwen Code、Cursor），**禁止用于 Dify、n8n、Postman 等工作流或测试工具**。违规使用将导致订阅暂停或 API Key 封禁 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。
- **地域绑定**：按量计费的 API Key 与 Base URL 必须同地域（如北京 Key 配北京 URL），跨地域调用会失败；免费额度也仅限华北2（北京）地域生效。
- **模型兼容性**：OpenAI 兼容协议（`/compatible-mode/v1`）支持 `chat/completions` 等标准接口；Anthropic 兼容协议（`/apps/anthropic`）需使用 `messages` 接口，且部分工具（如 Hermes Agent）需显式设置 `api_mode: anthropic_messages`。
- **上下文长度**：`qwen3.8-max` 最大支持 983,616 tokens，但实际可用长度受工具自身限制（如 Claude Code 默认 200K，需通过 `CLAUDE_CODE_MAX_CONTEXT_TOKENS` 扩展）。
- **图像/视频生成特殊流程**：此类 API 采用异步机制（创建任务 → 轮询 task_id），不可直接同步调用，详见 [Postman/cURL 调用指南](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)


