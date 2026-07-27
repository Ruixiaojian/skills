# use chat client or development tool

阿里云百炼支持多种主流 AI 编程客户端与开发工具（如 Hermes Agent、Cursor、Qwen Code 等）通过 OpenAI 或 Anthropic 兼容协议接入。开发者可根据计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan、按量计费）选择对应 Base URL 和 API Key，快速启用百炼模型能力。所有工具均需配置正确的地域、协议类型与模型 ID，部分工具对思考模式（`thinking`）有强制要求。

## 支持的模型与功能

- **通用文本生成模型**：所有工具均支持 `qwen3.8-max-preview`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro` 等主流文本模型。其中 `qwen3.8-max-preview` 强制启用思考模式（`thinking: true`），且 `temperature` 小于 0.6 时将自动提升至 0.6，`reasoning_effort` 默认为 `xhigh`，详见 [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) 文档说明。
- **多模态支持**：`qwen3.7-plus`、`qwen3.6-flash` 等模型支持 `text` + `image` 输入，但需工具本身具备图像上传能力（如 Cursor、Dify 的视觉开关）；Qwen-VL、QVQ、万相等专用多模态模型**不支持直接在标准聊天客户端中配置**，需通过 HTTP 节点或 cURL 调用，参见 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 和 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 文档。
- **协议兼容性**：
  - **OpenAI 兼容协议**（推荐）：Base URL 以 `/compatible-mode/v1` 结尾，适用于 Cursor、Cherry Studio、Cline、Qoder、Qwen Code、Kilo CLI、OpenClaw、Dify 等绝大多数工具。
  - **Anthropic 兼容协议**：Base URL 以 `/apps/anthropic` 结尾，适用于 Hermes Agent、Claude Code、OpenClaw（可选）等工具。注意：[Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md) 默认使用 Anthropic 协议，但其 `ANTHROPIC_BASE_URL` 配置必须严格匹配所选套餐的地址，否则会返回 401 错误。

> **注意**：文档间存在关键矛盾——[Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) 明确指出其默认使用 Anthropic 协议（`/apps/anthropic`），而 [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md) 和 [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md) 均仅提供 OpenAI 协议（`/compatible-mode/v1`）配置示例，且未提及 Anthropic 协议支持。实际接入时，请严格依据各工具官方文档指定的协议类型配置，混用将导致认证失败。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` / `baseUrl` | 百炼服务端点，**必须与计费方案和地域严格匹配** | [Token](../concepts/token.md) Plan 个人版：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；按量计费（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` / `apiKey` / `ANTHROPIC_AUTH_TOKEN` / `OPENAI_API_KEY` | 方案专属凭证，**不可跨方案复用** | [Token](../concepts/token.md) Plan 个人版 API Key 仅可用于 Token Plan 个人版 Base URL |
| `model` / `model_id` | 模型标识符，**需与套餐支持列表一致**，部分工具要求别名（如 Cursor 中 `kimi-k2.6` → `kimi-k2-6`） | `qwen3.8-max-preview`, `qwen3.7-plus` |
| `thinking` / `enable_thinking` | `qwen3.8-max-preview` 等模型必需开启，多数工具（如 Qwen Code、Kilo CLI）需显式配置 `{"enable_thinking": true}` 或 `{"thinking": {"type": "enabled"}}` | `true`（强制） |

## 使用方式

1. **安装工具**：按各工具要求安装（如 `npm install -g opencode-ai`、`curl ... | bash` 或桌面应用下载）。
2. **配置凭证**：
   - CLI 工具（Hermes、Claude Code、Codex、Kilo CLI）：编辑配置文件（如 `~/.hermes/config.yaml`、`~/.claude/settings.json`）或设置环境变量（`OPENAI_API_KEY`）。
   - GUI 工具（Cursor、Cherry Studio、Qoder）：在设置界面填写 API Key、Base URL 和 Model ID。
   - 平台类工具（Dify、OpenClaw）：通过插件市场安装适配器（如 OpenAI-API-compatible 插件），再填入凭证。
3. **验证连接**：运行简单命令（如 `hermes --version`）或发送测试消息（如 `"你好"`），确认返回有效响应。
4. **高级配置（可选）**：调整 `max_tokens`、`temperature`、`reasoning_effort` 等参数，需参考具体工具文档（如 [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md) 的进阶配置 JSON 格式）。

## 限制和注意事项

- **地域绑定**：按量计费的 `WorkspaceId` 必须与 API Key 所属地域一致（如北京地域 Key 需配北京地域 URL），否则报错 `401 Incorrect API key provided`。Token Plan/Coding Plan 的 Base URL 已固化地域，无需替换 `WorkspaceId`。
- **套餐隔离**：Token Plan 个人版、团队版、Coding Plan 的 API Key **完全不互通**。将 Token Plan 团队版 Key 用于 Coding Plan Base URL 会导致 `401` 或 `Unknown Custom model Exception`（见 [Qoder CN](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) 文档）。
- **工具类型限制**：Token Plan 个人版/团队版/Coding Plan **仅限 AI 编程工具与 OpenClaw 类 Agent 使用**，明确禁止用于 Postman、Insomnia、Dify 工作流、自定义后端脚本等场景（见 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 文档）。违规使用可能导致订阅暂停。
- **免费额度限制**：新人免费额度**仅适用于华北2（北京）地域的按量计费模型**，使用新加坡或美国地域会产生费用（见 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md) 文档）。
- **模型兼容性**：`qwen3.8-max-preview` 的思考模式为硬性约束，若工具未正确传递 `enable_thinking=true`（如 Cline 未勾选 *Enable R1 messages format*），将报错 `The value of the enable_thinking parameter is restricted to True`。

## 来源文档

- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)


