# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发框架接入模型服务，涵盖 OpenAI 兼容协议与 Anthropic 兼容协议两种 API 模式。开发者可根据使用场景（终端 CLI、IDE [插件](../concepts/plugin.md)、桌面应用或自定义开发）选择适配工具，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan 或按量计费）配置对应凭证。所有工具均需正确匹配 API Key、Base URL 与模型 ID，否则将触发 401 或 400 错误。

## 支持的模型/功能

百炼当前支持的主流模型包括 `qwen3.8-max`（支持 reasoning）、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro` 等文本生成模型；部分工具（如 [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)、Qwen Code、Claude Code）还支持图像输入（`input: ["text", "image"]`）及长上下文（最高 983616 tokens）。Qwen3 系列模型普遍支持思考模式（`enable_thinking: true` 或 `effort: "xhigh"`），需在请求体或配置中显式启用。

> **注意**：文档 1 中 OpenClaw 配置示例列出 `deepseek-v4-flash-0731` 但未给出完整字段（截断），而文档 4 和文档 13 的 `qwen3.8-max` 配置中明确包含 `thinking` 参数与 `budgetTokens: 262144`，表明该模型对思考预算有强约束；实际使用时应以 [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) 和 [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md) 的完整配置为准，避免因参数缺失导致 `400 InternalError.Algo.InvalidParameter`。

视觉与多模态能力（如 Qwen-VL、QVQ、万相文生图/视频）**不通过标准聊天客户端直接支持**，需调用独立 AIGC API（如 `/services/aigc/text2image/image-synthesis`），详见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

## 关键参数

| 参数 | 说明 | 常见取值 |
|------|------|----------|
| `API Key` | 计费方案专属密钥，**不可跨方案复用** | [Token](../concepts/token.md) Plan 个人版：`https://bailian.console.aliyun.com/.../subscription/overview`；按量计费：`https://help.aliyun.com/zh/model-studio/get-api-key` |
| `Base URL` | 必须与 API Key 所属方案及地域严格匹配 | OpenAI 兼容：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| `Model ID` | 模型标识符，部分工具要求别名（如 Cursor 中 `glm-5.2` → `glm-5-2`） | `qwen3.8-max`, `qwen3.7-plus`, `glm-5.2`, `wan2.6-t2i`（AIGC 专用） |
| `API Mode` | 协议类型，决定请求格式与路径 | `anthropic_messages`（Anthropic 兼容）、无此字段即默认 OpenAI 兼容 |
| `Thinking Mode` | Qwen3 系列必需启用，否则报错 `The value of the enable_thinking parameter is restricted to True` | `extra_body: {"enable_thinking": true}`（Qwen Code）、`"thinking": {"type": "enabled"}`（Kilo CLI、OpenCode） |

> **注意**：文档 16 明确指出，[Token](../concepts/token.md) Plan 个人版/团队版和 Coding Plan **仅限 AI 编程工具和 OpenClaw 类 Agent 使用**，禁止用于 Postman、Dify 等工作流平台；若违规使用，可能导致订阅暂停或 API Key 封禁。

## 使用方式

### 1. 安装与初始化
- **CLI 工具**（如 Hermes Agent、Claude Code、Qwen Code）：依赖 Node.js ≥18（部分要求 ≥22），通过 `npm install -g` 或一键脚本安装。
- **桌面客户端**（如 Cursor、Cherry Studio、Chatbox）：从官网下载安装包，无需命令行依赖。
- **IDE [插件](../concepts/plugin.md)**（如 Cline、Qoder JetBrains [插件](../concepts/plugin.md)）：在 VS Code 或 JetBrains 扩展市场搜索安装。
- **Agent 平台**（如 OpenClaw、QwenPaw）：支持 `curl` 脚本一键安装或 `pip` 安装。

### 2. 凭证配置
所有工具均需配置三项核心参数：
- **Token Plan 个人版/团队版**：`Base URL = https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（OpenAI）或 `/apps/anthropic`（Anthropic），API Key 来自对应控制台。
- **Coding Plan**：`Base URL = https://coding.dashscope.aliyuncs.com/v1`（OpenAI）或 `/apps/anthropic`（Anthropic）。
- **按量计费**：`Base URL` 中 `{WorkspaceId}` 必须替换为真实值，且 API Key 与地域严格一致（如北京地域 Key 不能用于新加坡 URL）。

配置路径示例：
- Hermes Agent：`~/.hermes/config.yaml`
- Claude Code：`~/.claude/settings.json`
- Cursor：设置界面 > Models > Override OpenAI Base URL
- Dify：需使用**按量计费 Key**，通过通义千问插件或 OpenAI-API-compatible 插件配置端点（[Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)）

### 3. 验证与调试
- 发送简单请求（如 `"你好"`）确认基础连通性。
- 对于 AIGC 任务（图像/视频），必须采用**异步流程**：先 `POST /image-synthesis` 获取 `task_id`，再 `GET /tasks/{task_id}` 轮询结果（参见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)）。
- 报错 `401 Incorrect API key provided`：立即检查 Key 与 URL 是否同属一方案及地域。

## 限制和注意事项

- **套餐隔离性**：Token Plan 个人版、团队版、Coding Plan 的 API Key **完全不互通**，混用必报 401。按量计费 Key 亦不可用于 Token Plan URL。
- **地域绑定**：按量计费的 `WorkspaceId` 与 API Key 必须同地域（北京/新加坡/美国），否则费用异常或调用失败（见文档 9 报错说明）。
- **模型兼容性**：并非所有模型支持全部协议。例如 `qwen3.8-max` 在 Anthropic 模式下需 `api_mode: anthropic_messages`，而在 OpenAI 模式下需 `enable_thinking: true`；`wan2.6-t2i` 等 AIGC 模型**仅支持独立 API**，不可在聊天客户端中调用。
- **免费额度限制**：新人免费额度**仅限华北2（北京）地域**，且按模型独立计算（文档 9）。
- **工具类型限制**：Dify、n8n、Coze 等工作流平台**明确不支持 Token Plan/Coding Plan**（文档 16、17），必须使用按量计费 Key，否则视为违规。
- **思考模式强制性**：`qwen3.8-max` 等模型若未启用 `enable_thinking`，将返回 `400` 错误（文档 9、12），需在配置文件或请求体中显式设置。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)


