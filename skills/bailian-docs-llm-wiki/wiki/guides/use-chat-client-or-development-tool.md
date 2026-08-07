# use chat client or development tool

阿里云百炼支持多种第三方 AI 编程工具、桌面客户端与开发平台通过标准 API 协议接入，开发者可基于自身工作流选择合适的客户端（如 Cursor、Claude Code）或开发工具（如 Dify、Postman）调用百炼模型。所有接入均需配置对应计费方案的 API Key 与 Base URL，并严格遵循各方案的使用范围限制。

## 支持的模型/功能

百炼提供统一的 OpenAI 兼容协议（`/compatible-mode/v1`）和 Anthropic 兼容协议（`/apps/anthropic`），支持主流文本生成模型，部分工具还支持多模态与思考模式：

- **核心文本模型**：`qwen3.8-max`（支持思考模式、983616 tokens 上下文）、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro`、`deepseek-v4-flash-0731`  
- **多模态能力**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash` 等明确标注 `"input": ["text", "image"]` 的模型支持图文输入（见 [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md) 配置示例）  
- **思考模式（Reasoning）**：Qwen3 系列模型需显式启用 `enable_thinking: true` 或设置 `thinking.budgetTokens`（如 [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md) 和 [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md) 所示）  
- **图像/视频生成**：需通过异步 API 调用（如 `wan2.6-t2i`），不适用于常规聊天客户端，详见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)  

> **注意**：Dify 等工作流平台**不支持** [Token](../concepts/token.md) Plan 个人版、[Token](../concepts/token.md) Plan 团队版和 Coding Plan 接入，仅允许使用按量计费 API Key；违规使用将导致订阅暂停或 Key 封禁（见 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 和 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 文档）。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `API Key` | 各计费方案专属密钥，**不可跨方案混用** | [Token](../concepts/token.md) Plan 个人版 Key：`sk-xxx`（见 [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)） |
| `Base URL` | 必须与 API Key 方案及地域严格匹配 | OpenAI 协议：<br>`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic 协议：<br>`https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| `Model ID` | 模型名称需与套餐支持列表一致，部分工具要求别名（如 `kimi-k2.6` → `kimi-k2-6`） | `qwen3.8-max`, `glm-5-2`（见 [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)） |
| `WorkspaceId` | 按量计费必需，需从控制台获取并替换 URL 中占位符 | `w-abc123xyz`（见 [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)） |

## 使用方式

### 1. 客户端类工具（推荐快速上手）
- **安装**：多数工具提供一键脚本（如 `curl -fsSL https://openclaw.ai/install.sh \| bash`）或 npm 全局安装（如 `npm install -g @anthropic-ai/claude-code`）  
- **配置**：通过 CLI 命令（`hermes config set`）、配置文件（`~/.qwen/settings.json`）或 GUI 设置界面（Cursor、Cherry Studio）完成  
- **验证**：发送 `你好` 或执行 `/status` 命令检查连接状态  

### 2. IDE 插件类工具（深度集成）
- **Cline / Qoder JetBrains 插件**：在 VS Code 或 JetBrains IDE 中安装插件，通过设置面板填入 Base URL、API Key 和 Model ID  
- **启用高级功能**：Qwen3 思考模式需勾选 `Enable R1 messages format`（见 [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)）  

### 3. 开发平台类工具（自定义工作流）
- **Dify**：安装“通义千问”插件，配置按量计费 API Key 及对应地域端点；视觉模型需开启 LLM 节点的“视觉”开关  
- **Postman/cURL**：仅用于 API 测试，需处理[异步任务](../concepts/asynchronous-task.md)（创建任务 → 轮询 `task_id` → 获取结果），**不适用于生产环境**（见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)）  

## 限制和注意事项

- **方案隔离性**：Token Plan 个人版、Token Plan 团队版、Coding Plan 的 API Key 与 Base URL **完全不互通**；按量计费 Key 必须与 WorkspaceId 所在地域一致（如北京 Key 不可用于新加坡 URL）  
- **模型兼容性**：  
  - Cursor 免费版仅支持 Auto 模式，调用自定义模型需升级至 Pro 版本  
  - Qoder CN 企业版不支持接入百炼，仅限个人社区版/专业版  
  - 部分模型（如 `qwen3.8-max`）需显式启用思考模式，否则返回 `400 InternalError.Algo.InvalidParameter`（见 [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)）  
- **地域与额度**：按量计费免费额度仅限华北2（北京）地域；其他地域调用将直接计费（见 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)）  
- **安全实践**：  
  - 生产环境禁止硬编码 API Key，应使用环境变量或密钥管理服务  
  - 配置文件路径需注意权限（如 `~/.hermes/config.yaml` 应设为 `600`）  
  - 避免在公开仓库提交含 Key 的配置（见 [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md) 安全提示）

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/cline-tool.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


