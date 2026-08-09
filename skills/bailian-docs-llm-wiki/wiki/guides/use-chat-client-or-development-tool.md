# use chat client or development tool

阿里云百炼支持多种主流 AI 编程工具、桌面客户端及开发平台接入，开发者可基于 OpenAI 或 Anthropic 兼容协议，通过 [Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan 或按量计费方案调用百炼模型。所有工具均需正确配置 API Key、Base URL 及模型 ID，且不同计费方案的凭证不互通。[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 明确指出，[Token](../concepts/token.md) Plan 和 Coding Plan 仅限 AI 编程工具与 Agent 类应用使用，工作流平台（如 Dify）等类型工具不支持接入。

## 支持的模型/功能

- **通用文本模型**：`qwen3.8-max`（支持思考模式、983616 tokens 上下文）、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro`、`deepseek-v4-flash-0731` 等，均支持文本输入/输出；部分支持图像输入（如 `qwen3.8-max`、`qwen3.7-plus`）。
- **协议兼容性**：
  - OpenAI 兼容协议：Base URL 形如 `https://.../compatible-mode/v1`，适用于 Cursor、Cherry Studio、Qwen Code、Cline、Chatbox、Qoder CN 等绝大多数工具。
  - Anthropic 兼容协议：Base URL 形如 `https://.../apps/anthropic`，适用于 Hermes Agent、Claude Code、OpenClaw 等工具。
- **高级能力**：思考模式（`enable_thinking: true`）需在请求体或配置中显式启用；部分工具（如 Qwen Code、Kilo CLI）支持为不同模型配置独立 `budgetTokens`；视觉模型（Qwen-VL、QVQ）需在 Dify 等平台开启“视觉”开关并传入图片 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

> **注意**：文档 1（OpenClaw）中列出的 `qwen3.8-max` 模型 `compat.thinkingFormat: "openai"`，而文档 4（OpenCode）和文档 16（Kilo CLI）均要求 `thinking.type: "enabled"` 并指定 `budgetTokens`。二者配置方式不一致，实际调用时应以所用工具的 SDK 或协议规范为准——OpenAI 兼容端点使用 `extra_body.enable_thinking=true`（见文档 8），Anthropic 端点使用 `thinking` 字段（见文档 4）。开发者需严格匹配工具所采用的协议栈。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `API Key` | 方案专属密钥，不可跨方案复用 | [Token](../concepts/token.md) Plan 个人版：`sk-xxx`（控制台获取） |
| `Base URL` | 必须与计费方案和协议严格匹配 | OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| `Model ID` | 模型标识符，部分工具要求别名（如 Cursor 中 `kimi-k2.6` → `kimi-k2-6`） | `qwen3.8-max`, `glm-5.2` |
| `WorkspaceId` | 按量计费必需，需从控制台获取并替换 URL 中占位符 | `ws-abc123def456` |
| `enable_thinking` | 思考模式开关，Qwen3 系列模型需显式启用 | `true`（置于 `extra_body` 或 `thinking` 对象内） |

## 使用方式

1. **安装工具**：根据工具文档安装（如 `npm install -g opencode-ai`、`curl ... | bash` 或下载桌面版）。
2. **配置凭证**：
   - CLI 工具（Hermes、Claude Code、Qwen Code）：通过命令行配置（`hermes config set`）或编辑配置文件（`~/.hermes/config.yaml`、`~/.claude/settings.json`）。
   - 桌面/IDE 工具（Cursor、Cherry Studio、Cline）：在图形界面设置中填入 API Key、Base URL 和 Model ID。
   - Web/平台工具（Dify、Qoder）：在管理后台[插件](../concepts/plugin.md)设置中配置 API Key，并选择对应模型。
3. **验证连接**：发送简单请求（如 `"你好"`）或运行 `/status` 命令，确认返回非错误响应。
4. **进阶使用**：启用思考模式、调整 `max_tokens`、配置[多模态](../concepts/multimodal.md)输入（图像）、集成百炼 CLI 技能（见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)）。

## 限制和注意事项

- **方案隔离**：Token Plan 个人版、团队版、Coding Plan 的 API Key 与 Base URL 组合唯一且不可混用；按量计费 Key 必须与 `WorkspaceId` 所属地域一致（如北京 Key 不可用于新加坡 URL）。
- **模型范围限制**：Token Plan/Coding Plan 仅支持文本生成类模型；图像/视频生成（万相）、语音（Qwen-Audio）、OCR（Qwen-OCR）等需通过 Dify 的 HTTP 节点或直接 cURL 调用专用 API [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。
- **不支持场景**：Dify、n8n、Coze 等工作流平台禁止使用 Token Plan/Coding Plan Key；Postman/cURL 仅用于测试，生产环境应使用 SDK [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。
- **常见错误**：
  - `401 Unauthorized`：Key 与 URL 方案/地域不匹配，或 Key 复制含空格。
  - `400 InvalidParameter`：未启用 R1 messages format（Qwen3/QwQ 模型需勾选该选项，见文档 10）。
  - `上下文超限`：需在提供商设置中手动增大 `max_tokens`（见文档 9）。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/cline-tool.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


