# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务。开发者可根据使用场景选择 CLI 工具（如 Hermes Agent、Qwen Code）、IDE 插件（如 Cline、Qoder JetBrains 插件）、桌面应用（如 Cursor、Cherry Studio）或低代码平台（如 Dify），并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan、按量计费）配置对应凭证。所有工具均基于 OpenAI 或 Anthropic 兼容协议，无需修改业务逻辑即可快速集成。

## 支持的模型与功能

- **通用文本模型**：qwen3.8-max-preview（强制开启思考模式）、qwen3.7-max、qwen3.7-plus、qwen3.6-flash、glm-5.2、deepseek-v4-pro 等，均支持文本输入，部分支持图像输入（如 qwen3.7-plus、qwen3.6-flash）。
- **视觉模型**：Qwen-VL、QVQ、Qwen-Omni、Qwen-Audio、Qwen-OCR 等需通过 HTTP 节点或专用 API 调用，[Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 明确说明不支持直接配置此类模型。
- **生成类模型**：万相（wan2.6-t2i 等）仅支持异步调用，需通过任务 ID 轮询结果，详见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 文档。
- **协议兼容性**：
  - OpenAI 兼容：Base URL 以 `/compatible-mode/v1` 结尾，适用于 Cursor、QwenPaw、Cherry Studio 等。
  - Anthropic 兼容：Base URL 以 `/apps/anthropic` 结尾，适用于 Hermes Agent、Claude Code、OpenClaw 等。
  > **注意**：同一计费方案下，OpenAI 和 Anthropic 协议的 Base URL 不可混用；例如 [Token](../concepts/token.md) Plan 个人版的 `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` 与 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` 对应不同协议栈，参数行为（如 `enable_thinking` 是否允许关闭）存在差异。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `API Key` | 方案专属密钥，不可跨方案复用 | [Token](../concepts/token.md) Plan 个人版：`sk-xxx`（见 [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)） |
| `Base URL` | 必须与 API Key 地域和计费方案严格匹配 | 按量计费北京地域：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `Model ID` | 模型标识符，部分工具要求别名（如 `kimi-k2.6` → `kimi-k2-6`） | `qwen3.8-max-preview` |
| `thinking` / `enable_thinking` | qwen3.8-max-preview 强制启用，传入 `temperature < 0.6` 时自动修正为 `0.6` | `true`（不可设为 `false`） |
| `reasoning_effort` | 控制推理深度，取值 `xhigh`/`medium`/`low`，默认 `xhigh` | `xhigh` |

> **注意**：`qwen3.8-max-preview` 的思考模式参数在多个文档中重复强调但存在表述冲突——[Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) 和 [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md) 均明确“thinking 始终开启，不支持关闭”，而 [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md) 配置示例中却允许设置 `"type": "enabled"`，暗示存在禁用可能。实际行为以服务端强制策略为准，客户端配置无效。

## 使用方式

### 1. 安装与初始化
- CLI 工具（Hermes Agent、Qwen Code、Kilo CLI 等）：依赖 Node.js ≥18，通过 `npm install -g` 或一键脚本安装。
- 桌面应用（Cursor、Cherry Studio）：从官网下载安装包，无需命令行依赖。
- IDE 插件（Cline、Qoder JetBrains）：在 VS Code 或 JetBrains 插件市场搜索安装。
- 平台类（Dify、QwenPaw）：需 Python 3.10+ 或 Docker，执行 `pip install` 或运行安装脚本。

### 2. 配置凭证
- **统一原则**：API Key、Base URL、Model ID 三者必须属于同一计费方案且地域一致。
- **配置路径示例**：
  - OpenClaw：`~/.openclaw/openclaw.json`
  - Hermes Agent：`~/.hermes/config.yaml`
  - Cursor：Settings → Models → OpenAI API Key + Override Base URL
  - QwenPaw：Web Console → 设置 → 模型 → 内置提供商页面填写
- **环境变量**：Codex 等工具需设置 `OPENAI_API_KEY`，Qoder CLI 需 `QODER_PERSONAL_ACCESS_TOKEN`。

### 3. 验证与调试
- 发送简单请求（如 `"你好"`）确认基础连通性。
- 遇到 `401 Unauthorized`：检查 API Key 是否过期、是否与 Base URL 方案匹配（如 Token Plan 团队版 Key 不能用于 Coding Plan URL）。
- 遇到 `400 InvalidParameter`：CLI 工具（如 Cline）需勾选 `Enable R1 messages format`；思考模式模型需确保 `enable_thinking: true`。

## 限制和注意事项

- **方案适用范围限制**：Token Plan 个人版、团队版及 Coding Plan **仅限 AI 编程工具和 OpenClaw 类 Agent 使用**，明确禁止用于工作流平台（Dify、n8n）、API 测试工具（Postman、cURL）或自定义后端应用。违规使用可能导致订阅暂停或 API Key 封禁，详见 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。
- **地域绑定**：按量计费的 API Key 与 Workspace ID 必须同地域（如北京地域 Key 不能用于新加坡 URL），免费额度也仅限华北2（北京）地域生效。
- **模型能力差异**：并非所有模型支持全部功能。例如：
  - `qwen3.8-max-preview` 支持长上下文（983616 tokens）和思考模式，但 `glm-5.2` 仅支持文本输入且无思考能力。
  - 视觉模型（Qwen-VL）需在 Dify 的 LLM 节点中手动开启“视觉”开关，并设置分辨率。
- **命名规范**：Cursor、Chatbox 等工具要求模型 ID 使用连字符而非点号（如 `kimi-k2-6` 而非 `kimi-k2.6`），否则报错 `The model xxx does not work with your current plan`。
- **认证失败排查**：若持续 `401`，优先确认 RAM 子账号是否被授予模型调用权限（参见 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md) 常见问题）。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)


