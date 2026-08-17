# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、Web 应用和工作流系统等场景。开发者可根据使用习惯选择适配的客户端，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan 或按量计费）配置对应凭证与端点。所有工具均基于 OpenAI 或 Anthropic 兼容协议，无需修改业务逻辑即可快速集成。

## 支持的模型/功能

百炼当前支持的主流模型包括 `qwen3.8-max`（支持思考模式与超长上下文）、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro` 系列等文本生成模型；部分工具（如 Qwen Code、Cursor、Qoder）还支持图像理解（Qwen-VL）、[多模态](../concepts/multi-modal.md)推理（QVQ）及音视频生成（需通过 HTTP 节点或百炼 CLI 调用）。  
**注意**：并非所有模型在所有工具中均可用。例如，Dify 明确不支持 [Token](../concepts/token.md) Plan 个人版/团队版和 Coding Plan 接入，仅允许使用按量计费 API Key [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)；而 OpenClaw 的配置示例中列出的 `deepseek-v4-flash-0731` 模型在文档末尾被截断，其完整参数需参考 [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md) 原文确认。

图像与视频生成类 API（如万相文生图）采用异步机制，需先创建任务获取 `task_id`，再轮询查询结果，不适用于同步调用场景 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` / `API 主机` | 必填，决定协议类型与计费方案归属 | OpenAI 协议：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Anthropic 协议：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| `api_key` / `API 密钥` | 必填，与 `base_url` 严格绑定，不可跨方案混用 | [Token](../concepts/token.md) Plan 个人版 API Key 仅可用于 Token Plan 的 Base URL |
| `model` / `模型 ID` | 必填，需与所选方案支持的模型列表一致 | `qwen3.8-max`、`qwen3.7-plus`；注意 Cursor 等工具要求别名（如 `glm-5.2` → `glm-5-2`）[Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) |
| `enable_thinking` / `effort` | 可选，启用思考模式需显式设置（如 `extra_body: { "enable_thinking": true }` 或 `effort: "xhigh"`） | Qwen3 系列默认需开启思考模式才能发挥全部能力 |

> **注意**：`base_url` 中的 `{WorkspaceId}` 在按量计费方案中必须替换为真实值，且 API Key 必须与该 Workspace 所属地域一致；Token Plan 和 Coding Plan 的 Base URL 为固定地址，无须替换。

## 使用方式

### 1. 客户端安装
- **CLI 工具**（如 Hermes Agent、Claude Code、Qwen Code）：依赖 Node.js ≥18，通过 `npm install -g` 或一键脚本安装。
- **桌面应用**（如 Cursor、Cherry Studio、Qoder IDE）：从官网下载安装包，无需额外依赖。
- **IDE 插件**（如 Cline、Qoder JetBrains 插件）：在 VS Code 或 JetBrains 扩展市场搜索安装。
- **Web 平台**（如 Dify、QwenPaw）：Dify 为 SaaS 服务；QwenPaw 支持本地 `pip install` 或 Docker 部署。

### 2. 凭证配置
所有工具均遵循统一配置逻辑：
- **Token Plan 个人版/团队版**：使用专属 API Key + 固定 Base URL（`token-plan.cn-beijing.maas.aliyuncs.com`）；
- **Coding Plan**：使用 Coding Plan API Key + `coding.dashscope.aliyuncs.com` 域名；
- **按量计费**：使用百炼通用 API Key + `{WorkspaceId}.<region>.maas.aliyuncs.com` 地域化 Base URL。

配置路径示例：
- Hermes Agent：`~/.hermes/config.yaml`
- Claude Code：`~/.claude/settings.json`
- Cursor：GUI 设置 > Models > OpenAI API Key & Override Base URL
- Dify：需使用按量计费 API Key 配置「通义千问」插件 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)

### 3. 验证与调试
- 发送简单请求（如 `curl -X POST <base_url>/chat/completions -H "Authorization: Bearer <api_key>" -d '{"model":"qwen3.7-plus","messages":[{"role":"user","content":"你好"}]}'`）；
- 工具内执行 `/status`（Claude Code）、`/model`（Qoder CLI）等内置命令检查连接状态；
- 若报错 `401 Incorrect API key provided`，优先核对 API Key 与 Base URL 是否来自同一计费方案及地域。

## 限制和注意事项

- **方案隔离性**：Token Plan 个人版、Token Plan 团队版、Coding Plan 的 API Key **完全不通用**，混用将导致 401 错误；按量计费 API Key 亦不可用于前三者 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。
- **工具兼容性限制**：
  - Token Plan/Coding Plan **禁止用于工作流平台**（Dify、n8n、Coze）和 **API 测试工具**（Postman、cURL），仅限编程助手类工具（如 Hermes、Cursor、Qoder）及 OpenClaw 类 Agent [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)；
  - Postman/cURL 仅推荐用于图像/视频 API 的**功能验证**，生产环境应使用 SDK 或封装 HTTP 调用 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。
- **模型命名差异**：Cursor、Chatbox 等工具要求模型 ID 使用连字符替代点号（如 `glm-5.2` → `glm-5-2`），否则报错 `The model xxx does not work with your current plan` [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)。
- **上下文与性能**：`qwen3.8-max` 支持 983616 tokens 上下文，但实际可用长度受客户端实现限制（如 Claude Code 默认 200K，需手动配置 `CLAUDE_CODE_MAX_CONTEXT_TOKENS`）；长对话或工具调用易触发超限，建议在提供商设置中显式配置 `max_tokens` [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)


