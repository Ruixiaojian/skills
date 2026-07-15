# use chat client or development tool

阿里云百炼支持通过多种主流 AI 开发工具和客户端接入模型服务，包括终端 CLI 工具（如 Hermes Agent、Qwen Code）、桌面 IDE（如 Cursor、Qoder CN）、开源平台（如 Dify）以及通用 HTTP 客户端（如 Postman）。所有工具均通过 OpenAI 或 Anthropic 兼容 API 协议对接，开发者可根据使用场景选择按量计费、Coding Plan 或 Token Plan 团队版三种计费方案。

## 支持的模型/功能

百炼支持的模型因计费方案而异，且需匹配对应协议（OpenAI 兼容或 Anthropic 兼容）与 Base URL。核心模型覆盖 Qwen 系列（如 `qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`）、DeepSeek（如 `deepseek-v4-pro`）、Kimi（如 `kimi-k2.7-code`）、GLM（如 `glm-5.2`）及 MiniMax 等。部分模型（如 Qwen3 系列）支持思考模式（`enable_thinking: true`），需在请求体或配置中显式启用 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)。

图像与视频生成类模型（如 `wan2.6-t2i`）**不适用**于常规聊天客户端，必须通过异步 API 调用，且仅支持直接 HTTP 请求（cURL/Postman）或 Dify 工作流等支持长轮询的平台 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。此外，Token Plan 团队版和 Coding Plan **明确禁止**用于工作流平台（Dify、n8n、Coze）、API 测试工具（Postman、Insomnia）或自定义后端应用——该限制在 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 中有明确定义。

> **注意**：文档 1 和文档 2 均列出 `qwen3.6-flash` 为 Token Plan 团队版支持模型，但文档 1 的 JSON 配置中其 `contextWindow` 为 `1000000`，而文档 4（OpenCode）中同模型未声明上下文长度；文档 7（Qwen Code）则明确要求 `qwen3.6-flash` 必须启用 `enable_thinking`。实际行为以控制台公布的[Token Plan 团队版支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)为准，建议以官方模型页描述为最终依据。

## 关键参数

所有工具共用三类核心参数：

- **API Key**：严格按计费方案隔离。Token Plan 团队版、Coding Plan 与按量计费的 API Key **互不通用**，混用将导致 401 错误。
- **Base URL**：必须与 API Key 所属地域及计费方案完全匹配。例如：
  - Token Plan 团队版（北京）：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（OpenAI）或 `/apps/anthropic`（Anthropic）
  - Coding Plan：`https://coding.dashscope.aliyuncs.com/v1`（OpenAI）或 `/apps/anthropic`（Anthropic）
  - 按量计费（北京）：`https://dashscope.aliyuncs.com/compatible-mode/v1`（OpenAI）或 `/apps/anthropic`（Anthropic）
- **Model ID**：部分工具（如 Cursor、Chatbox）要求对带点号的模型名做转换（如 `kimi-k2.6` → `kimi-k2-6`），详见各工具文档；Qwen3 系列模型在启用思考模式时，部分工具（如 Qwen Code）需在 `generationConfig.extra_body` 中设置 `"enable_thinking": true` [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)。

## 使用方式

1. **安装工具**：各工具提供标准化安装路径，如 `npm install -g`（Hermes Agent、Claude Code）、一键脚本（OpenClaw、QwenPaw）、GUI 下载（Cursor、Cherry Studio）或 VS Code 插件（Cline）。
2. **配置凭证**：绝大多数工具通过编辑配置文件（如 `~/.hermes/config.yaml`、`~/.qwen/settings.json`）或图形化设置界面完成。环境变量（如 `OPENAI_API_KEY`）在 Codex 等工具中仍被广泛使用。
3. **验证与调用**：配置后执行简单命令（如 `hermes chat -q "你好"`）或在 GUI 中发送测试消息。对于支持多模型的工具（如 Qoder、Cursor），需在对话界面手动切换模型，且免费版（如 Cursor Free）可能限制自定义模型调用 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)。
4. **高级能力**：部分工具（Qoder、Cline、Cursor）支持通过百炼 CLI 注册 Skills，实现自然语言驱动的代码生成、图像/视频生成等扩展能力，需提前全局安装 `bailian-cli` 并配置 API Key。

## 限制和注意事项

- **地域强绑定**：按量计费的 API Key 与 Base URL 必须属于同一地域（如北京 Key + 北京 URL），否则报错 401；Token Plan 团队版与 Coding Plan 的 Base URL 固定，无需选择地域。
- **协议差异**：OpenAI 兼容端点（`/compatible-mode/v1`）接受标准 `/chat/completions` 请求；Anthropic 兼容端点（`/apps/anthropic`）需使用 `/messages` 接口及 `anthropic-messages` 协议，二者不可混用。
- **免费额度限制**：按量计费新用户享免费额度，但**仅限华北2（北京）地域**的模型生效；使用新加坡或美国地域将立即产生费用 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **模型兼容性**：Codex 对不同模型需区分 `wire_api`（`responses` vs `chat`），且仅新版支持 Qwen3 系列；旧版 Codex（v0.80.0）是 Coding Plan 的强制要求 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)。
- **违规风险**：将 Token Plan 团队版或 Coding Plan 的 API Key 用于 Dify、Postman 等非授权场景，可能触发订阅暂停或 Key 封禁 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


