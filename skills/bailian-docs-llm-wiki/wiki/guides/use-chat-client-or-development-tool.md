# use chat client or development tool

阿里云百炼支持多种主流 AI 编程工具与开发平台接入，开发者可通过 [Token](../concepts/token.md) Plan 个人版、[Token](../concepts/token.md) Plan 团队版、Coding Plan 或按量计费四种方案，使用 OpenAI 兼容或 Anthropic 兼容协议调用百炼模型。所有工具均需正确配置 API Key、Base URL 及模型 ID，且不同计费方案的凭证不互通。本文档汇总关键能力、参数规范、配置方式及限制条件，供开发者快速落地。

## 支持的模型/功能

百炼支持的模型因计费方案而异，全部为文本生成类模型（部分支持多模态输入），**不支持图像/视频生成、Embedding、Rerank 等非文本生成类模型在编程工具中直接调用**（图像/视频生成需通过专用异步 API 调用，详见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)）。各方案支持的核心模型如下：

- **[Token](../concepts/token.md) Plan 个人版 & 团队版**：`qwen3.8-max`（支持思考模式、1M 上下文）、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro`、`deepseek-v4-flash-0731`  
- **Coding Plan**：`qwen3.7-plus`（默认）、`qwen3.6-flash` 等，**不支持 `qwen3.8-max`**  
- **按量计费**：覆盖全部公开文本模型，包括 `qwen3.8-max`、`wan2.6-t2i`（需专用 API）、`qwen-vl`（需视觉开关）等；但 `wan2.6-t2i` 等 AIGC 模型**必须通过异步 HTTP 接口调用，不可在 CLI/IDE 工具中直接配置为聊天模型**  

> **注意**：Dify 等工作流平台明确不支持 Token Plan 和 Coding Plan 套餐，仅允许使用按量计费 API Key，否则将触发违规封禁 —— 详见 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 文档说明。

## 关键参数

| 参数 | 说明 | 示例值 | 注意事项 |
|------|------|--------|----------|
| `Base URL` | 必填，决定协议类型与计费归属 | OpenAI 兼容：<br>`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic 兼容：<br>`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | - Token Plan/Coding Plan 的 Base URL **固定**，不可替换地域<br>- 按量计费必须匹配 `WorkspaceId` 与 API Key 所属地域<br>- `compatible-mode/v1` 与 `/apps/anthropic` **不可混用**，否则返回 404 或 401 |
| `API Key` | 必填，与 Base URL 方案严格绑定 | `sk-xxx`（Token Plan 个人版） | - 三种订阅套餐的 API Key **完全隔离**，跨方案使用必报 `401 Incorrect API key provided`<br>- Dify 等平台若误用套餐 Key，将导致订阅暂停 |
| `Model ID` | 必填，区分大小写，部分工具需别名 | `qwen3.8-max`（标准）<br>`kimi-k2-6`（Cursor 中需替换点号为短横线） | - Cursor、Cherry Studio 等工具对模型名有格式要求（如 `kimi-k2.6` → `kimi-k2-6`）<br>- Qwen3 系列启用思考模式需额外参数（如 `enable_thinking: true` 或 `thinking.budgetTokens`） |

## 使用方式

### 1. 安装与初始化
- **CLI 工具**（Hermes Agent、Qwen Code、Kilo CLI）：依赖 Node.js（v18+）或 Python，通过 `curl`/`npm install -g` 安装，安装后需重载 shell 环境（如 `source ~/.zshrc`）  
- **桌面/IDE 工具**（Cursor、Cherry Studio、Cline）：下载安装包或插件，无需命令行依赖  
- **Agent 平台**（OpenClaw、QwenPaw）：支持一键脚本（`curl \| bash`）或 `pip install`，首次运行自动启动配置向导  

### 2. 凭证配置路径（通用规则）
| 工具 | 配置文件路径 | 协议支持 |
|------|--------------|----------|
| Hermes Agent | `~/.hermes/config.yaml` | Anthropic / OpenAI（通过 `api_mode` 切换） |
| OpenCode / Kilo CLI | `~/.config/opencode/opencode.json` / `~/.config/kilo/config.json` | Anthropic（`@ai-sdk/anthropic`） |
| Claude Code | `~/.claude/settings.json` | Anthropic（环境变量 `ANTHROPIC_BASE_URL`） |
| Cursor / Cherry Studio / Chatbox / Cline | GUI 设置界面 → 模型配置页 | OpenAI 兼容（`compatible-mode/v1`） |
| Qoder / Qoder CN | GUI 设置 → 模型 → 添加 → 选择“阿里云百炼 - 国内” | OpenAI 兼容（GUI 下拉选择） |

> **注意**：Claude Code 默认强制跳过 Anthropic 官方登录，需手动创建 `~/.claude.json` 并设 `"hasCompletedOnboarding": true`，否则无法连接百炼 —— 此细节在 [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md) 文档中有明确说明。

### 3. 验证与调试
- 所有工具配置完成后，执行最简请求验证：`claude "你好"`、`qwen "test"` 或 GUI 中输入“你好”  
- 报错时优先检查：  
  - `Base URL` 与 `API Key` 是否同属一个方案（如 Token Plan 个人版 Key + Coding Plan URL → 401）  
  - 模型名是否在对应方案支持列表中（如在 Coding Plan 中配置 `qwen3.8-max` → 400）  
  - 地域是否匹配（按量计费 Key 与 `WorkspaceId` 所在地域不一致 → 401）

## 限制和注意事项

- **协议隔离**：Anthropic 兼容端点（`/apps/anthropic`）仅接受 `anthropic_messages` 格式请求；OpenAI 兼容端点（`/compatible-mode/v1`）仅接受 `chat/completions` 格式。混用将导致 `400 Bad Request`。  
- **免费额度约束**：按量计费新用户免费额度**仅限华北2（北京）地域**，使用新加坡/美国端点将立即计费 —— 详见 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md) 常见问题说明。  
- **工具类型限制**：Token Plan 个人版、Token Plan 团队版、Coding Plan **禁止用于工作流平台（Dify/n8n）、API 测试工具（Postman/cURL）、自定义后端服务**。违规使用将触发封禁，此限制在 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 文档中明确定义。  
- **上下文长度**：`qwen3.8-max` 支持 1M tokens，但多数工具（如 Claude Code）默认上限为 200K，需显式配置 `CLAUDE_CODE_MAX_CONTEXT_TOKENS=1000000` 或等效参数。  
- **模型能力差异**：`qwen3.8-max` 支持 `reasoning: true` 与 `thinking.budgetTokens`，而 `qwen3.6-flash` 仅支持基础推理，配置错误参数将被忽略或报错。

## 来源文档

- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/cline-tool.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


