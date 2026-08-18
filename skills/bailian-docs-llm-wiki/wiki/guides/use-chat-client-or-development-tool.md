# use chat client or development tool

阿里云百炼平台支持多种主流 AI 开发工具与聊天客户端（如 Hermes Agent、Cursor、Dify 等），开发者可通过按量计费、Coding Plan、Token Plan 个人版或 Token Plan 团队版四种计费方案接入。所有工具均基于 OpenAI 兼容协议或 Anthropic 兼容协议调用百炼模型，配置核心为 API Key、Base URL 和模型 ID。本文档结构化梳理关键能力、参数规范、接入方式及常见约束，便于快速选型与排障。

## 支持的模型/功能

百炼支持的模型因计费方案而异，且部分工具对模型能力有额外限制：

- **通用文本模型**：`qwen3.8-max`（支持思考模式、多模态输入）、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro` 等在 Token Plan 个人版、Token Plan 团队版、Coding Plan 及按量计费中均有覆盖，但具体可用性需以各方案[官方支持列表](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview)为准。  
- **多模态支持**：`qwen3.8-max` 和 `qwen3.7-plus` 明确支持 `text` + `image` 输入，而 `glm-5.2` 仅支持文本（见 [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md) 配置示例）。  
- **视觉/音视频专用模型**（如 `wan2.6-t2i`, `Qwen-VL`, `Qwen-Audio`）**不适用于多数编程客户端**，仅推荐通过 Postman/cURL 或 Dify 的 HTTP 节点调用异步 API（见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)）。  
- **Dify 是特例**：明确**不支持** Token Plan 个人版、Token Plan 团队版和 Coding Plan，仅允许使用按量计费 API Key；否则可能触发违规封禁 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

> **注意**：文档中 `qwen3.6-plus` 在 [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md) 的 Token Plan 团队版配置片段中出现，但该模型未在 Token Plan 团队版[官方支持列表](https://help.aliyun.com/zh/model-studio/token-plan-overview)中列出，属过时或错误引用，应以控制台实时列表为准。

## 关键参数

所有工具配置均围绕三个核心参数展开，但协议类型与路径细节存在差异：

| 参数 | 说明 | 协议要求 | 示例值 |
|------|------|----------|--------|
| **API Key** | 方案专属凭证，**不可跨方案复用**。Token Plan 个人版、Token Plan 团队版、Coding Plan、按量计费的 Key 完全隔离。 | 所有方案 | `sk-xxxxxxxxxxxxx`（需从对应控制台页面获取） |
| **Base URL** | 模型服务入口地址，**必须与 API Key 所属地域和方案严格匹配**。地域不匹配将导致 401 错误或费用异常。 | OpenAI 兼容协议（主流）：`/compatible-mode/v1`<br>Anthropic 兼容协议（少数）：`/apps/anthropic` | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（Token Plan 个人版）<br>`https://coding.dashscope.aliyuncs.com/v1`（Coding Plan）<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`（按量计费，Anthropic 协议） |
| **Model ID** | 模型标识符，**部分工具要求别名转换**。例如 Cursor 中 `glm-5.2` 需写为 `glm-5-2`，`kimi-k2.6` 需写为 `kimi-k2-6`（见 [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)）。 | 无强制格式，但需与百炼控制台模型名一致 | `qwen3.8-max`, `qwen3.7-plus` |

> **注意**：`CLAUDE_CODE_SUBAGENT_MODEL`（见 [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)）等子任务专用参数，仅在特定工具中生效，不属于通用参数。

## 使用方式

接入流程高度统一，分为安装、配置、验证三步，但配置载体各异：

- **安装**：绝大多数工具（Hermes Agent、OpenCode、Claude Code、Qwen Code 等）依赖 Node.js（v18+）或 Python（3.10~3.13），通过 `npm install -g`、`curl | bash` 或一键脚本完成。Windows 用户需注意 Hermes Agent 和 Claude Code 要求 WSL2 或 Git Bash。
- **配置**：
  - **命令行工具**（如 Hermes、OpenCode、Kilo CLI）：通过 CLI 命令（`hermes config set`）或编辑 JSON/YAML 配置文件（如 `~/.hermes/config.yaml`, `~/.config/opencode/opencode.json`）。
  - **桌面客户端**（如 Cursor、Cherry Studio、Chatbox）：通过图形界面设置 > 模型 > 添加提供方，填入 API Key、Base URL、Model ID。
  - **IDE 插件**（如 Cline、Qoder JetBrains 插件）：在插件设置面板中选择“OpenAI Compatible”，输入对应参数。
  - **Agent 平台**（如 OpenClaw、QwenPaw）：通过 Web Console 设置 > 模型 > 添加提供商，或编辑 `~/.openclaw/openclaw.json` 等本地文件。
- **验证**：通用方法为发送测试请求（如 `hermes chat -q "你好"`、`claude "你好"`），或在 GUI 中输入简单问题观察响应。若返回 `401 Incorrect API key provided`，首要排查 Key 与 Base URL 是否同属一方案及地域。

## 限制和注意事项

- **方案隔离性**：四种计费方案的 API Key、Base URL、支持模型完全独立。混用（如用 Token Plan 个人版 Key 配 Coding Plan URL）必然失败，且可能导致订阅异常 [Qoder CN](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)。
- **地域绑定**：按量计费的 API Key 必须与 Base URL 中的 `{WorkspaceId}` 所属地域一致（如北京地域 Key 不能用于新加坡 URL），否则产生费用或认证失败 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **免费额度限制**：新人免费额度**仅限华北2（北京）地域**，且按模型独立计算，不可跨模型共享 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **模型能力适配**：并非所有模型都支持全部功能。例如，`qwen3.8-max` 支持 `enable_thinking` 参数和 `effort: xhigh`，而 `glm-5.2` 在多数工具配置中未启用思考模式；调用 `qwen3.6-flash` 时需确认其 `contextWindow`（1M）与实际需求匹配 [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)。
- **生产环境建议**：Postman/cURL 仅用于调试，生产环境应使用官方 SDK 或封装 HTTP 调用逻辑，避免硬编码凭证 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

## 来源文档

- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)


