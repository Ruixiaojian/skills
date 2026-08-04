# use chat client or development tool

阿里云百炼支持通过多种主流 AI 开发工具和聊天客户端接入，包括 OpenClaw、Claude Code、Hermes Agent、Cursor 等终端/桌面工具，以及 VS Code 插件（如 Cline、Qwen Code）、JetBrains 插件等。所有工具均通过 OpenAI 或 Anthropic 兼容协议对接，支持按量计费、Coding Plan、[Token](../concepts/token.md) Plan 个人版及 [Token](../concepts/token.md) Plan 团队版四种计费方案，开发者可根据场景选择合适工具与配置方式。

## 支持的模型/功能

百炼当前支持的主流模型（以 [Token](../concepts/token.md) Plan 个人版为例）包括 `qwen3.8-max`、`qwen3.8-max-preview`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro`、`deepseek-v4-flash-0731` 等文本生成模型；部分模型（如 `qwen3.8-max-preview`）强制启用思考模式（`thinking: enabled`），不支持关闭，且 `temperature` 在思考模式下有最低阈值（0.6）[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)。图像/视频生成类模型（如 `wan2.6-t2i`）需通过专用 AIGC API 异步调用，不适用于通用聊天客户端 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。注意：Token Plan 个人版、团队版及 Coding Plan **仅支持文本生成类模型**，不支持多模态或 AIGC 类模型直接接入聊天客户端 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。

> **注意**：文档 1（OpenClaw）中列出的 `qwen3.7` 模型 ID 截断（`"bailian-token-plan/qwen3.7`），而其他文档（如文档 2、5、8）均使用完整 ID `qwen3.7-max` 或 `qwen3.7-plus`，应以完整命名为准，避免配置失败。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `API Key` | 各计费方案专属密钥，**不可跨方案混用**。Token Plan 个人版 Key 仅可用于 Token Plan Base URL，否则返回 401 错误 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md) | `sk-xxxxxxxxxxxxx` |
| `Base URL` | 必须与 API Key 方案及地域严格匹配：<br>• Token Plan：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（OpenAI）或 `/apps/anthropic`（Anthropic）<br>• Coding Plan：`https://coding.dashscope.aliyuncs.com/v1`（OpenAI）或 `/apps/anthropic`（Anthropic）<br>• 按量计费：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（需替换 WorkspaceId） | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `Model ID` | 模型标识符，部分工具（如 Cursor、Chatbox）要求对含点号的模型名做转换（如 `glm-5.2` → `glm-5-2`）[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) | `qwen3.8-max-preview` |
| `thinking` / `enable_thinking` | Qwen3 系列思考模式开关。`qwen3.8-max-preview` 等模型强制启用，传入 `false` 将被忽略 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md) | `true` |

## 使用方式

1. **安装工具**：根据工具要求安装依赖（如 Node.js ≥18.0，Python 3.10–3.13）及 CLI/IDE 插件；
2. **配置凭证**：
   - 终端工具（OpenClaw、Claude Code、Hermes Agent 等）：编辑配置文件（如 `~/.openclaw/openclaw.json`、`~/.claude/settings.json`）或执行 `hermes config set` 命令；
   - 桌面/IDE 工具（Cursor、Cherry Studio、Cline 等）：在图形界面设置中填写 API Key、Base URL 和 Model ID；
   - Web 工具（Chatbox、Qoder IDE）：通过“添加模型”向导配置；
3. **验证连接**：发送简单请求（如 `"你好"`）或执行 `/status` 命令检查响应；
4. **高级配置（可选）**：调整 `max_tokens`、`temperature`、`reasoning_effort`（xhigh/medium/low）等生成参数，或启用 R1 messages format（Qwen3/R1 模型必需）[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)。

## 限制和注意事项

- **地域绑定**：按量计费的 API Key 与 Workspace ID 必须同地域（如北京 Key 配北京 URL），跨地域将导致 401 或费用异常 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)；
- **免费额度限制**：新人免费额度仅限华北2（北京）地域模型，且各模型额度独立计算，不共享 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)；
- **协议兼容性**：同一工具可能同时支持 OpenAI 和 Anthropic 协议，但 Base URL 和模型参数需严格对应（如 Anthropic 协议需 `/apps/anthropic` 路径，OpenAI 协议需 `/compatible-mode/v1`）；
- **禁止用途**：Token Plan 及 Coding Plan **严禁用于工作流平台（Dify/n8n）、API 测试工具（Postman）或自定义后端应用**，违规将导致订阅暂停或 Key 封禁 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)；
- **模型别名要求**：Cursor 等工具对部分模型名（如 `kimi-k2.6`）要求转义为 `kimi-k2-6`，否则报错 `The model xxx does not work with your current plan` [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


