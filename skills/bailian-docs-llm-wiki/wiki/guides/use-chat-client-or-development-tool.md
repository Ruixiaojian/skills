# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、桌面应用和低代码工作流平台。开发者可根据使用场景选择适配的客户端，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan 或按量计费）配置对应凭证与端点。所有工具均基于 OpenAI 或 Anthropic 兼容协议，无需修改业务逻辑即可快速集成。

## 支持的模型/功能

百炼支持的模型能力因计费方案而异，且不同客户端对模型特性的支持程度不同：

- **文本生成模型**：所有方案均支持 `qwen3.8-max`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro`、`deepseek-v4-flash-0731` 等主流模型；其中 `qwen3.8-max` 支持思考模式（`enable_thinking: true`），需在请求体或客户端高级配置中显式启用 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)。
- **[多模态](../concepts/multi-modal.md)输入**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash` 支持 text + image 输入，但部分客户端（如 Cursor 免费版）仅限 Auto 模式，不支持自定义[多模态](../concepts/multi-modal.md)模型 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)。
- **图像/视频生成**：仅支持通过按量计费 API 调用（如 `wan2.6-t2i`），且必须使用异步机制（`X-DashScope-Async: enable`）创建任务并轮询结果 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。
- **不支持场景**：[Token](../concepts/token.md) Plan 和 Coding Plan **不可用于工作流平台（如 Dify）或 API 测试工具（如 Postman）**；Dify 明确要求仅使用按量计费 API Key，否则可能触发封禁 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

> **注意**：文档 17 明确指出 [Token](../concepts/token.md) Plan/Coding Plan 不支持 Dify、n8n、Coze 等工作流平台，但文档 12（Qoder）和文档 13（Qoder CN）未强调此限制，实际部署时应以文档 17 的合规要求为准。

## 关键参数

| 参数 | 说明 | 常见值示例 |
|------|------|------------|
| `base_url` | 服务端点地址，协议决定路径后缀 | OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| `api_key` | 方案专属密钥，**不可跨方案复用** | Token Plan 个人版 API Key 仅适用于 Token Plan 个人版 Base URL |
| `model_id` | 模型标识符，部分客户端需转换命名格式 | `kimi-k2.6` → `kimi-k2-6`，`glm-5.2` → `glm-5-2`（见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)） |
| `workspace_id` | 按量计费必需，需替换为真实 ID | 华北2 地域：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `enable_thinking` | Qwen3 系列思考模式开关 | 需在 `extra_body`（Qwen Code）、`thinking.budgetTokens`（OpenCode/Kilo CLI）或客户端 UI 中启用 |

## 使用方式

### 安装与初始化
- **CLI 工具**（Hermes Agent、Claude Code、Qwen Code、Kilo CLI）：依赖 Node.js ≥18 或 Python，通过 `npm install -g` 或 `curl` 脚本安装，安装后需重载 shell 环境（如 `source ~/.zshrc`）。
- **桌面客户端**（Cursor、Cherry Studio、Chatbox）：直接下载安装包，启动后进入设置 > 模型 > 添加，填入 Base URL、API Key 和 Model ID。
- **IDE 插件**（Cline、Qoder JetBrains 插件）：在 VS Code 或 JetBrains 扩展市场搜索安装，配置界面选择 OpenAI Compatible 协议并填写凭证。
- **Agent 平台**（OpenClaw、QwenPaw）：通过 `curl` 脚本或 `pip install` 安装，首次运行自动启动向导，模型配置文件位于 `~/.openclaw/openclaw.json` 或 Web Console 设置页。

### 配置验证
- 终端工具：执行 `hermes --version` 或 `claude "hello"`，检查是否返回响应。
- GUI 工具：在聊天框输入“你好”，确认模型正常回复；若报错 `401 Incorrect API key`，需核对 API Key 与 Base URL 是否同属一个方案及地域 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)。

## 限制和注意事项

- **地域绑定**：按量计费的 API Key 与 `base_url` 中的地域必须严格匹配（如北京 Key 不能用于新加坡 endpoint），否则返回 401 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)。
- **免费额度限制**：新人免费额度仅限华北2（北京）地域模型，其他地域调用将产生费用 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **模型兼容性**：部分工具（如 Codex）对 API 版本有要求——`qwen3.8-max` 需用 Responses API，而 `glm-5` 等旧模型需降级至 Codex v0.80.0 并使用 Chat API [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)。
- **命名冲突**：Cursor 免费版仅支持 Auto 模式，自定义模型需升级至 Pro 版本；且部分模型名（如 `kimi-k2.6`）需转义为 `kimi-k2-6` 才能识别 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)。
- **协议差异**：Anthropic 兼容端点（`/apps/anthropic`）需设置 `api_mode: anthropic_messages`，而 OpenAI 兼容端点（`/compatible-mode/v1`）则无需该参数，混用会导致 404 或 400 错误。

## 来源文档

- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/cline-tool.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


