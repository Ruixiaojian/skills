# use chat client or development tool

阿里云百炼支持多种主流 AI 编程工具与开发平台通过 OpenAI 或 Anthropic 兼容协议接入，开发者可根据使用场景（终端 CLI、IDE [插件](../concepts/plugin.md)、桌面应用、工作流平台等）选择适配的客户端，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan、按量计费）配置对应凭证。所有工具均需正确匹配 Base URL、API Key 与模型 ID，否则将触发 401 或 400 错误。

## 支持的模型/功能

百炼支持的模型因计费方案而异，**仅文本生成类模型**在 [Token](../concepts/token.md) Plan 个人版、[Token](../concepts/token.md) Plan 团队版和 Coding Plan 中可用；图像/视频生成（如 `wan2.6-t2i`）、多模态（如 `qwen-vl`）、语音（如 `qwen-audio`）及 OCR 模型**仅支持按量计费方案**。常见支持模型包括：

- `qwen3.8-max`（支持思考模式、1M 上下文、图文输入）
- `qwen3.7-plus` / `qwen3.7-max` / `qwen3.6-flash`
- `glm-5.2`、`deepseek-v4-pro`、`deepseek-v4-flash-0731`
- `kimi-k2-6`、`glm-5-2` 等别名形式（[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) 中明确要求模型名需用连字符替换点号）

> **注意**：Dify 等工作流平台**不支持**Token Plan 个人版、Token Plan 团队版和 Coding Plan 接入，仅允许使用按量计费 API Key，否则可能被封禁 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。该限制同样适用于 Postman、cURL 等测试工具——它们仅用于快速验证，不可用于生产调用 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `Base URL` | 必须与计费方案和协议严格匹配。OpenAI 兼容协议路径为 `/compatible-mode/v1`；Anthropic 兼容协议路径为 `/apps/anthropic`（或 `/apps/anthropic/v1`） | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（Token Plan 个人版 + OpenAI）<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`（按量计费 + Anthropic） |
| `API Key` | 方案专属密钥，**不可跨方案复用**。Token Plan 个人版 Key 不能用于 Coding Plan，按量计费 Key 必须与 Base URL 地域一致 | `sk-xxx`（从控制台对应页面获取） |
| `Model ID` | 模型标识符，部分工具（如 Cursor、Qwen Code）要求使用别名（如 `kimi-k2-6` 而非 `kimi-k2.6`） | `qwen3.8-max`、`glm-5-2` |
| `Context Window` | 多数工具支持扩展上下文（如 Claude Code 可设 `CLAUDE_CODE_MAX_CONTEXT_TOKENS=1000000`），但需模型本身支持（如 `qwen3.8-max` 支持 983616 tokens） | `983616` |

## 使用方式

### 1. 安装与初始化
- **CLI 工具**（Hermes Agent、Qwen Code、Kilo CLI、Claude Code）：通常通过 `curl` 脚本或 `npm install -g` 安装，安装后需重载 shell（如 `source ~/.zshrc`）。
- **IDE [插件](../concepts/plugin.md)**（Cline、Qoder JetBrains [插件](../concepts/plugin.md)）：在 VS Code 或 JetBrains IDE 扩展市场中搜索安装。
- **桌面应用**（Cursor、Chatbox、Qoder CN）：从官网下载安装包。
- **Web 平台**（Dify、OpenClaw）：直接访问网页或部署私有实例。

### 2. 配置凭证
所有工具均需配置以下三要素：
- **API Key**：从百炼控制台对应方案页面获取（如 [Token Plan 个人版 API Key](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)）。
- **Base URL**：严格按方案+协议选择（参见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 中的完整对照表）。
- **Model ID**：填入方案支持的模型列表中的确切名称（注意别名规则）。

配置方式分两类：
- **命令行工具**：写入 YAML/JSON/TOML 配置文件（如 `~/.hermes/config.yaml`、`~/.codex/config.toml`）或执行 `config set` 命令。
- **GUI 工具**：在设置界面填写表单（如 Cursor 的 Models 页面、Qoder CN 的模型添加向导）。

### 3. 验证与调试
- 发送简单请求（如 `hermes chat -q "你好"` 或在 Chatbox 输入“你好”）确认基础连通性。
- 若报错 `401 Incorrect API key provided`，优先检查 Key 与 Base URL 是否来自同一方案且地域一致。
- 若报错 `400 InternalError.Algo.InvalidParameter`（如 Cline），需启用 R1 messages format 或检查 thinking 参数是否被模型支持。

## 限制和注意事项

- **方案隔离性**：Token Plan 个人版、Token Plan 团队版、Coding Plan 的 API Key **完全不通用**，混用必报 401。按量计费 Key 必须与 Base URL 地域一致（如北京地域 Key 不可配新加坡 URL）。
- **模型能力限制**：Token Plan/Coding Plan **仅支持文本生成模型**；万相（文生图/视频）、Qwen-VL、QVQ、Qwen-Audio 等需使用按量计费方案，并通过 HTTP 节点或 cURL 异步调用（参见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)）。
- **工具类型限制**：工作流平台（Dify、n8n）、API 测试工具（Postman）、自定义后端代码**禁止使用套餐 Key**，仅允许按量计费 Key，违规将导致订阅暂停或 Key 封禁。
- **Windows 兼容性**：Hermes Agent、Claude Code 等 CLI 工具在 Windows 原生不支持，需 WSL2 或 Git Bash 运行。
- **上下文与参数**：部分模型（如 `qwen3.8-max`）支持 `effort: xhigh` 或 `enable_thinking: true`，但并非所有工具都暴露该参数（如 Codex 需额外配置 `model-catalog.local.json`）。

## 来源文档

- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)


