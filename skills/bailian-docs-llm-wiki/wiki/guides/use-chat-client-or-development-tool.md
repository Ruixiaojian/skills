# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程客户端与开发工具接入，涵盖 CLI 工具（如 Hermes Agent、Claude Code）、桌面/IDE 插件（如 Cursor、Cline、Qoder）、开源 Agent 平台（如 OpenClaw、QwenPaw）以及工作流平台（如 Dify）。所有工具均通过 OpenAI 兼容协议或 Anthropic 兼容协议对接百炼模型服务，开发者可根据使用场景选择合适工具并配置对应计费方案的凭证。

## 支持的模型/功能

百炼支持的模型能力因接入方式和计费方案而异：

- **通用文本生成模型**：`qwen3.8-max`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro` 等在 [Token](../concepts/token.md) Plan 个人版、[Token](../concepts/token.md) Plan 团队版、Coding Plan 及按量计费中均广泛可用，详见 [Token Plan 个人版支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview) 和 [Coding Plan 支持的模型](https://help.aliyun.com/zh/model-studio/coding-plan)。  
- **多模态能力**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash` 支持图像输入；`Qwen-VL`、`QVQ`、`Qwen-Omni` 等视觉/语音模型需通过 HTTP 节点或专用 API（如文生图）调用，**不支持直接在 Dify 的千问插件中配置** [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。  
- **思考模式（Reasoning）**：`qwen3.8-max` 默认启用高阶推理（`effort: xhigh`），部分工具（如 Claude Code、Qwen Code）需显式设置 `enable_thinking: true` 或 `CLAUDE_CODE_SUBAGENT_MODEL` 等参数以激活 [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)。  
- **图像/视频生成**：万相（Wan2.x）、通义万相等 AIGC 模型仅支持通过异步 API 调用（如 `text2image/image-synthesis`），**不支持在 Chatbox、Cherry Studio 等通用聊天客户端中直接使用** [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

> **注意**：文档 15 明确指出，[Token](../concepts/token.md) Plan 个人版、Token Plan 团队版和 Coding Plan **仅限 AI 编程工具和 OpenClaw 类 Agent 使用**；Dify、n8n、Coze 等工作流平台及 Postman、cURL 等测试工具**不支持**接入这些套餐，否则可能触发风控封禁。

## 关键参数

所有工具均依赖以下核心参数完成百炼接入：

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `API Key` | 各计费方案专属密钥，**不可跨方案混用**。Token Plan 个人版、团队版、Coding Plan 的 Key 互不通用；按量计费 Key 必须与 Base URL 地域一致。 | `sk-xxxxxxxxxxxxx` |
| `Base URL` | 服务端点地址，分 OpenAI 兼容（`/compatible-mode/v1`）与 Anthropic 兼容（`/apps/anthropic`）两类。地域需匹配 API Key 所属 Workspace。 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `Model ID` | 百炼模型标识符，注意命名规范：Cursor 要求 `kimi-k2.6` → `kimi-k2-6`，`glm-5.2` → `glm-5-2` [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)。 | `qwen3.8-max` |
| `API Mode / Protocol` | 工具需明确声明协议类型。Hermes Agent 需设 `api_mode: anthropic_messages`；OpenClaw 配置 `"api": "anthropic-messages"`；其余多数工具默认 OpenAI 兼容。 | `anthropic_messages` 或 `openai` |

## 使用方式

### 1. 安装与初始化
- CLI 工具（Hermes Agent、Claude Code、Qwen Code）：通过 `curl` 或 `npm install -g` 安装，执行 `--version` 验证。
- 桌面应用（Cherry Studio、Chatbox、Qoder IDE）：从官网下载安装包，首次启动完成向导配置。
- IDE 插件（Cline、Cursor、JetBrains Qoder）：在 VS Code 或 JetBrains 扩展市场搜索安装。
- 开源 Agent（OpenClaw、QwenPaw）：推荐一键脚本（`curl ... \| bash`）或 `pip install`，启动后访问本地 Web 控制台。

### 2. 配置凭证（四类方案统一逻辑）
所有工具均遵循相同凭证映射规则：
- **Token Plan 个人版**：Base URL = `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，API Key 来自 [个人版控制台](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)。  
- **Token Plan 团队版**：Base URL 同上，API Key 来自 [团队版成员管理页](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/uac-admin/organization/members/list)。  
- **Coding Plan**：Base URL = `https://coding.dashscope.aliyuncs.com/v1`，API Key 来自 [Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)。  
- **按量计费**：Base URL 格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，`WorkspaceId` 和 `region` 必须与 API Key 所属业务空间完全一致 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。

> **注意**：文档 5（Codex）指出，部分模型（如 `glm-5`）需降级至 `@openai/codex@0.80.0` 并使用 `wire_api = "chat"`，而 `qwen3.8-max` 等新模型需 `wire_api = "responses"` —— 此处存在版本兼容性差异，建议优先选用官方推荐的最新稳定版工具。

### 3. 高级能力启用
- **思考模式**：Qwen Code 需在 `settings.json` 中 `extra_body.enable_thinking: true`；Claude Code 需设置 `CLAUDE_CODE_SUBAGENT_MODEL`；Qoder/Cline 需勾选 **Enable R1 messages format**。  
- **上下文扩展**：Claude Code 支持通过 `CLAUDE_CODE_MAX_CONTEXT_TOKENS` 环境变量提升至 `1000000` tokens（需模型支持）[Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)。  
- **多模态输入**：OpenClaw、Qwen Code、Kilo CLI 等明确声明 `input: ["text", "image"]`，调用时需传入 base64 图像数据。

## 限制和注意事项

- **套餐适用范围严格隔离**：Token Plan 个人版/团队版/Coding Plan **禁止用于 Dify、Postman、自定义脚本等非编程助手类工具**。违规使用将导致订阅暂停或 API Key 封禁 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。  
- **地域强绑定**：按量计费的 API Key 与 Base URL 地域必须一致（如北京 Key 只能配北京 URL），否则返回 `401` 错误；免费额度也仅限华北2（北京）地域生效 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。  
- **模型兼容性差异**：  
  - Anthropic 协议工具（Hermes Agent、Claude Code）要求 Base URL 以 `/apps/anthropic` 结尾，且需显式指定 `api_mode`；  
  - OpenAI 协议工具（Cursor、Chatbox、Cherry Studio）必须使用 `/compatible-mode/v1` 路径，且部分模型名需转义（如 `kimi-k2.6` → `kimi-k2-6`）[Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)。  
- **调试建议**：  
  - 配置后务必执行 `/status`（Claude Code）或发送 `你好` 测试响应；  
  - 报错 `401 Incorrect API key provided` 优先检查 Key 与 URL 方案/地域是否匹配；  
  - 报错 `400 InternalError.Algo.InvalidParameter` 多因未启用思考模式或 R1 格式，按工具文档启用对应开关。

## 来源文档

- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)


