# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务。开发者可根据使用场景选择 CLI 工具（如 Qwen Code、Hermes Agent）、图形化客户端（如 Cursor、Cherry Studio）或低代码平台（如 Dify），统一使用 OpenAI 或 Anthropic 兼容协议进行配置。所有工具均支持按量计费、Coding Plan、[Token](../concepts/token.md) Plan 个人版和 [Token](../concepts/token.md) Plan 团队版四种接入方式，但不同工具对套餐的适用性存在明确限制。

## 支持的模型/功能

百炼当前支持的主流模型包括 `qwen3.8-max-preview`（强制启用思考模式）、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro` 等文本生成模型，部分工具还支持视觉模型（如 Qwen-VL、QVQ）和多模态能力（见 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 文档）。图像/视频生成类 API（如万相文生图）需通过异步调用机制使用，不适用于同步聊天客户端，详见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

> **注意**：`qwen3.8-max-preview` 的思考模式为强制开启且不可关闭，`temperature` 小于 0.6 时将自动修正为 0.6，`reasoning_effort` 默认为 `xhigh` —— 此行为在 [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)、[Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md) 和 [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md) 等多份文档中一致确认，属模型固有约束，非配置错误。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `Base URL` | 必填，决定协议类型与计费方案 | OpenAI 协议：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Anthropic 协议：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| `API Key` | 必填，严格绑定计费方案与地域 | [Token](../concepts/token.md) Plan 个人版 Key 仅可用于对应 Base URL，不可混用于 Coding Plan 或按量计费 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) |
| `Model ID` | 必填，需与所选套餐支持的模型列表一致 | `qwen3.8-max-preview`、`qwen3.7-plus`；注意 Cursor 等工具要求模型名转义（如 `kimi-k2.6` → `kimi-k2-6`） |
| `thinking` / `enable_thinking` | 部分模型（如 qwen3.8-max-preview）需显式启用 | OpenCode 配置中为 `"thinking": {"type": "enabled"}`；Qwen Code 中为 `"extra_body": {"enable_thinking": true}` |

## 使用方式

### 安装与初始化
- CLI 工具（如 [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)、Qwen Code、Hermes Agent）通常依赖 Node.js（v18+）或 Python（3.10~3.13），推荐使用官方一键脚本安装；
- 桌面客户端（如 Cursor、Cherry Studio、Chatbox）需下载安装包后，在设置界面手动填写 API Key 与 Base URL；
- IDE 插件（如 Cline、Qoder JetBrains 插件）需先安装插件，再通过图形化配置面板添加模型。

### 配置路径（常见）
- OpenClaw：`~/.openclaw/openclaw.json`
- Hermes Agent：`~/.hermes/config.yaml`
- Claude Code：`~/.claude/settings.json`
- Qwen Code：`~/.qwen/settings.json`
- Chatbox / Cherry Studio / Cursor：GUI 设置界面，无固定文件路径

### 协议选择指南
- **OpenAI 兼容协议**（推荐）：Base URL 以 `/compatible-mode/v1` 结尾，适用于绝大多数工具（Cursor、Chatbox、Qwen Code、Kilo CLI 等）；
- **Anthropic 兼容协议**：Base URL 以 `/apps/anthropic` 结尾，适用于 Hermes Agent、Claude Code、OpenClaw 等明确声明支持 `anthropic-messages` 的工具；
- **不支持混合使用**：同一工具不可混用两种协议，否则触发 401 或 404 错误。

## 限制和注意事项

- **套餐适用性限制**：Token Plan 个人版、Token Plan 团队版和 Coding Plan **仅限 AI 编程工具与 OpenClaw 类 Agent 使用**，**严禁用于工作流平台（如 Dify、n8n、Coze）或 API 测试工具（如 Postman、cURL）**。Dify 明确要求仅使用按量计费 API Key，违规使用将导致订阅暂停或 Key 封禁 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。
  
- **地域与 Workspace ID 绑定**：按量计费的 Base URL 中 `{WorkspaceId}` 必须与 API Key 所属业务空间完全匹配，且地域（如华北2、新加坡）必须一致；Token Plan/Coding Plan 的 Base URL 为固定域名，无需替换 Workspace ID。

- **模型兼容性差异**：
  - Codex 对 `qwen3.8-max-preview` 等支持 Responses API 的模型需使用新版（≥0.90.0），而 `glm-5` 等旧模型需降级至 v0.80.0 并改用 Chat API；
  - Cursor 免费版仅支持 Auto 模式，无法调用自定义模型，必须升级至 Pro 版本；
  - Qoder CN（原 Lingma）企业版不支持接入百炼，仅限个人社区版/专业版。

- **思考模式参数一致性**：`qwen3.8-max-preview` 的 `thinking` 参数在所有支持该模型的工具中均为强制启用，但参数名不统一（如 `enable_thinking`、`thinking.type`、`reasoning`），需按工具文档严格配置，否则返回 `400 InternalError.Algo.InvalidParameter`。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


