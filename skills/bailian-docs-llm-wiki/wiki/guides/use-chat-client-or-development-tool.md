# use chat client or development tool

阿里云百炼平台支持多种第三方 Chat 客户端与开发工具接入，开发者可通过 [Token](../concepts/token.md) Plan 个人版、[Token](../concepts/token.md) Plan 团队版、Coding Plan 或按量计费四种方案，使用 OpenAI 兼容协议或 Anthropic 兼容协议调用百炼托管的模型。所有工具均需配置对应套餐的专属 API Key 与 Base URL，且 Key 与 URL 必须严格匹配所属计费方案及地域。

## 支持的模型与功能

百炼支持的模型因计费方案而异，**[Token](../concepts/token.md) Plan 个人版**和**Token Plan 团队版**均支持 `qwen3.8-max-preview`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro` 等文本生成模型；**Coding Plan** 主要支持 `qwen3.7-plus` 等面向编程场景的模型；**按量计费**覆盖最全，包括文生图（如 `wan2.6-t2i`）、文生视频、[多模态](../concepts/multi-modal.md)（Qwen-VL、QVQ）及语音模型（Qwen-Audio），详见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

关键功能特性：
- `qwen3.8-max-preview` 强制启用思考模式（`thinking: enabled`），不支持关闭；`temperature` 小于 0.6 时自动上调至 0.6；`reasoning_effort` 可设为 `xhigh`/`high`/`low`，默认 `xhigh`。
- 图像/视频类 API 采用异步机制：先调用 `/api/v1/services/aigc/.../synthesis` 创建任务获取 `task_id`，再轮询 `/api/v1/tasks/{task_id}` 查询结果。
- [多模态](../concepts/multi-modal.md)模型（如 Qwen-VL）需在客户端显式启用视觉开关，并支持上传图片输入。

> **注意**：文档 [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) 明确指出“企业版不支持接入百炼”，而其他文档（如 [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)）未作此限制，实际接入前请以 Qoder CN 官方说明为准。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `API Key` | 各计费方案专属密钥，**不可混用**。Token Plan 个人版 Key 仅适用于 Token Plan Base URL，按量计费 Key 必须与所选地域一致。 | `sk-xxxxxxxxxxxxx` |
| `Base URL` | 决定协议类型与服务端点。OpenAI 兼容协议路径为 `/compatible-mode/v1`；Anthropic 兼容协议路径为 `/apps/anthropic`。地域需匹配：北京为 `dashscope.aliyuncs.com`，新加坡需替换 `WorkspaceId`。 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `Model ID` | 必须为当前套餐支持的模型名，如 `qwen3.8-max-preview`。部分工具（如 Codex）要求预先配置模型元数据文件定义 `context_window`、`supported_reasoning_levels` 等。 | `qwen3.7-plus` |
| `enable_thinking` / `thinking` | 思考模式开关。`qwen3.8-max-preview` 等模型强制开启，部分工具（如 Qwen Code）需在 `extra_body` 中显式设置 `"enable_thinking": true`。 | `true` |

## 使用方式

### 1. 安装与初始化
- **CLI 工具**（如 OpenClaw、Hermes Agent、Kilo CLI）：依赖 Node.js（v18+）或 Python（3.10~3.13），通过 `npm install -g` 或 `pip install` 安装，首次运行通常触发交互式配置向导（如 `openclaw onboard`）。
- **桌面/IDE [插件](../concepts/plugin.md)**（如 Cherry Studio、Cline、Qwen Code）：下载安装包或从扩展市场安装，配置入口位于设置 > 模型 > 添加。
- **开发平台**（如 Dify）：需安装官方[插件](../concepts/plugin.md)（如“通义千问”），在模型供应商设置中填入 API Key 并选择地域端点。

### 2. 配置凭证
所有工具均需将 API Key 与 Base URL 绑定：
- **OpenAI 兼容协议**：Base URL 以 `/compatible-mode/v1` 结尾，Key 填入 `Authorization: Bearer <key>` 或环境变量 `OPENAI_API_KEY`。
- **Anthropic 兼容协议**：Base URL 以 `/apps/anthropic` 结尾，Key 填入 `ANTHROPIC_AUTH_TOKEN` 或 `X-API-Key` 请求头。
- **验证**：发送测试请求（如 `claude "你好"` 或对话框输入“你好”），成功返回即配置生效。

> **注意**：文档 [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md) 要求跳过 Anthropic 官方登录（设置 `hasCompletedOnboarding: true`），而 [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) 和 [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md) 无此步骤，表明该配置是 Claude Code 特有前置条件，非百炼通用要求。

### 3. 高级能力调用
- **思考模式**：`qwen3.8-max-preview` 等模型需在请求体中携带 `{"enable_thinking": true}`（Qwen Code）或 `{"thinking": {"type": "enabled"}}`（OpenCode），否则返回 `400 The value of the enable_thinking parameter is restricted to True` 错误。
- **长上下文**：部分工具（如 Claude Code）支持通过 `CLAUDE_CODE_MAX_CONTEXT_TOKENS` 环境变量扩展至 1M tokens，但需模型本身支持（如 `qwen3.8-max-preview` 上下文窗口为 983616）。
- **异步任务**：图像/视频生成必须分两步调用，详见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

## 限制和注意事项

- **套餐隔离**：Token Plan 个人版、团队版、Coding Plan 的 API Key **完全不互通**。将 Token Plan Key 用于 Coding Plan Base URL 会导致 `401 Incorrect API key provided`（见 [Qoder CN](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) 和 [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md) 文档）。
- **地域绑定**：按量计费 Key 必须与 Base URL 地域一致。北京 Key 不能用于新加坡 URL，否则产生费用或认证失败（见 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md) “接入按量计费时，有免费额度但产生了费用”说明）。
- **工具类型限制**：Token Plan 个人版/团队版/**Coding Plan 仅允许用于 AI 编程工具（如 Hermes、Qwen Code）和 Agent 类工具（如 OpenClaw、QwenPaw）**，明确禁止用于工作流平台（Dify、n8n）、API 测试工具（Postman）或自定义应用后端（见 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)）。
- **模型兼容性**：并非所有模型都支持全部协议。例如 `qwen3.8-max-preview` 仅支持 Anthropic 协议下的思考模式，若通过 OpenAI 协议调用需确认 `enable_thinking` 参数是否被正确透传（见 [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md) 区分 Responses API 与 Chat/Completions API 的说明）。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)


