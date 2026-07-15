# use chat client or development tool

阿里云百炼平台支持通过多种主流 AI 开发工具和客户端接入模型服务，包括终端 CLI 工具（如 Hermes Agent、Qwen Code）、IDE [插件](../concepts/plugin.md)（如 Cline、Kilo CLI）、桌面应用（如 Cursor、Cherry Studio）以及开源平台（如 Dify、Qoder）。所有工具均通过 OpenAI 或 Anthropic 兼容协议对接，开发者可基于自身工作流选择合适工具，并按 [Token](../concepts/token.md) Plan 团队版、Coding Plan 或按量计费三种方案配置凭证。

## 支持的模型/功能

百炼支持的模型因计费方案而异，且需匹配对应协议（OpenAI 兼容或 Anthropic 兼容）：

- **[Token](../concepts/token.md) Plan 团队版**：支持 `qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.6-flash`、`deepseek-v4-pro`、`deepseek-v4-flash`、`kimi-k2.7-code`、`glm-5.2` 等文本生成模型；部分模型（如 Qwen3 系列）支持 `enable_thinking` 参数开启思考模式。[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md) 明确列出其 [Token](../concepts/token.md) Plan 配置中支持的全部模型 ID 及 thinking 启用方式。
- **Coding Plan**：主要支持 `qwen3.7-plus`、`qwen3.6-plus` 等，不支持 Qwen3.7-max；仅提供 Chat/Completions API 接入，需使用旧版 Codex（如 0.80.0）[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md) 指出该限制。
- **按量计费**：覆盖最广，除上述模型外，还支持万相（wanx）系列图像/视频生成模型（如 `wan2.6-t2i`），但需通过异步 API 调用 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 详细说明了该机制。

> **注意**：文档间存在模型命名不一致问题。例如 Cursor 要求将 `kimi-k2.6` 写为 `kimi-k2-6`，而 OpenCode 和 Qwen Code 直接使用 `kimi-k2.6`；Dify [插件](../concepts/plugin.md)对 `qwen-turbo` 的权限校验也与官方模型列表存在偏差。实际配置时请以各工具文档的命名要求为准。

## 关键参数

所有工具共用以下核心参数，但字段名和协议适配方式不同：

- **API Key**：必须与所选计费方案严格匹配。Token Plan、Coding Plan 和按量计费的 API Key 互不通用，且按量计费 Key 必须与 Base URL 所在地域一致（如北京 Key 不可用于新加坡 endpoint）。
- **Base URL**：
  - OpenAI 兼容协议：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（Token Plan）、`https://coding.dashscope.aliyuncs.com/v1`（Coding Plan）、`https://dashscope.aliyuncs.com/compatible-mode/v1`（按量，北京）。
  - Anthropic 兼容协议：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`（Token Plan）、`https://coding.dashscope.aliyuncs.com/apps/anthropic`（Coding Plan）、`https://dashscope.aliyuncs.com/apps/anthropic`（按量，北京）。
- **Model ID**：必须从对应方案的支持列表中选取，例如 Token Plan 不支持 `qwen-turbo`，Coding Plan 不支持 `qwen3.7-max`。
- **高级参数**：`enable_thinking`（Qwen3 系列）、`max_tokens`（用于规避上下文超限）、`CLAUDE_CODE_MAX_CONTEXT_TOKENS`（Claude Code 扩展上下文至 1M）等，需在配置文件或 UI 中显式设置。

## 使用方式

配置流程高度统一，分为三步：

1. **安装工具**：多数工具提供一键脚本（如 `curl -fsSL ... | bash`）、npm 全局安装（如 `npm install -g opencode-ai`）或 GUI 下载（如 Cursor、Cherry Studio）。
2. **配置凭证**：
   - CLI 工具（Hermes Agent、Qwen Code）通常提供交互式命令（如 `hermes config set` 或 `/auth`）或编辑 JSON/YAML 配置文件（路径见各文档）。
   - IDE [插件](../concepts/plugin.md)（Cline、Kilo CLI）通过图形化设置界面填写 Base URL、API Key 和 Model ID。
   - 桌面应用（Cursor、Chatbox）在 Settings > Models 中添加 OpenAI 兼容 Provider 并填入参数。
3. **验证与调用**：执行简单命令（如 `hermes chat -q "你好"`）或发送测试消息，观察是否返回有效响应。部分工具（如 Qoder CN）要求先完成账号登录才能启用模型配置。

## 限制和注意事项

- **套餐适用范围严格受限**：Token Plan 团队版和 Coding Plan **仅允许用于 AI 编程工具和 OpenClaw 类 Agent**，明确禁止用于 Dify、n8n、Postman 等工作流平台或 API 测试工具 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。违规使用可能导致订阅暂停或 API Key 封禁。
- **地域绑定强制**：按量计费的 API Key 与 Base URL 地域必须一致（如北京 Key + 北京 endpoint），否则返回 401 错误；免费额度也仅限华北2（北京）地域生效 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **协议与版本兼容性**：Codex 对不同模型需切换 API 协议（Responses API vs Chat API）及版本（0.80.0），Claude Code 需跳过 Anthropic 官方登录验证，Cursor 免费版不支持自定义模型。这些细节均需严格遵循对应工具文档。
- **模型能力差异**：Qwen3 系列支持思考模式（需 `enable_thinking: true`），而 DeepSeek、GLM 等模型默认不启用；图像/视频生成模型（如 wan2.6-t2i）必须使用异步调用流程，无法通过标准聊天接口直接使用。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)


