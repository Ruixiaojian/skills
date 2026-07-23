# use chat client or development tool

阿里云百炼支持通过多种主流 AI 开发工具和客户端接入，包括终端编程助手（如 Hermes Agent、Claude Code）、IDE 插件（如 Cline、Qoder）、桌面应用（如 Cursor、Cherry Studio）以及开源 Agent 框架（如 OpenClaw、QwenPaw）。所有工具均通过 OpenAI 或 Anthropic 兼容协议对接，开发者可基于自身技术栈选择合适工具，快速集成百炼模型能力。

## 支持的模型/功能

百炼支持的模型因计费方案而异，**[Token](../concepts/token.md) Plan 个人版**与**团队版**均支持 `qwen3.8-max-preview`（强制开启思考模式）、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro` 等文本生成模型；**Coding Plan** 主要面向开发场景，推荐 `qwen3.7-plus`；**按量计费**覆盖最全模型集，包括文生图（`wan2.6-t2i`）、文生视频（`wan2.1-t2v-turbo`）等 AIGC 模型。视觉与[多模态](../concepts/multi-modal.md)能力需显式启用（如 Qwen-VL、QVQ），详见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

> **注意**：文档中多次提及 `qwen3.8-max-preview` 的思考模式为“始终开启，不支持关闭”，但不同工具对参数暴露程度不一：OpenClaw 配置中未显式声明 `thinking` 字段 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)，而 Claude Code 和 Qwen Code 明确要求设置 `enable_thinking: true` 或 `thinking.type: "enabled"`。实际调用时应以具体工具配置为准。

部分工具（如 Cursor、Chatbox、Cherry Studio）要求模型 ID 使用别名格式（如 `kimi-k2.6` → `kimi-k2-6`，`glm-5.2` → `glm-5-2`），否则报错 `Named models unavailable` 或 `Unknown Custom model Exception` [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)。Dify 等低代码平台则需通过插件（如“通义千问”）或 HTTP 节点间接接入万相模型，不支持直接配置 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

## 关键参数

| 参数 | 说明 | 典型值 |
|------|------|--------|
| `base_url` | API 端点地址，协议决定兼容性 | OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| `api_key` | 方案专属密钥，**不可跨方案复用** | [Token](../concepts/token.md) Plan 个人版 Key 仅适用于 [Token](../concepts/token.md) Plan Base URL，与 Coding Plan Key 不互通 |
| `model_id` | 模型标识符，需与套餐支持列表严格匹配 | `qwen3.8-max-preview`、`wan2.6-t2i`、`text-embedding-v4` |
| `reasoning_effort` | 仅 `qwen3.8-max-preview` 支持，控制推理深度 | `xhigh`（默认）、`high`、`low` |
| `enable_thinking` | 思考模式开关，部分工具强制为 `true` | Qwen Code 中需在 `extra_body` 中显式设为 `true` |

地域相关参数需严格对齐：按量计费的 `base_url` 与 `api_key` 必须同属华北2（北京）、新加坡或美国（弗吉尼亚）任一地域，否则返回 401 错误 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)。

## 使用方式

1. **安装工具**：根据操作系统选择安装方式（如 `npm install -g`、一键脚本、GUI 安装包），确保依赖版本满足要求（Node.js ≥ 18，Python 3.10–3.13）。
2. **配置凭证**：  
   - CLI 工具（Hermes Agent、Claude Code）通过命令行或配置文件（`~/.hermes/config.yaml`、`~/.claude/settings.json`）设置；  
   - GUI 工具（Cursor、Cherry Studio）在设置界面填写 API Key、Base URL 和 Model ID；  
   - Agent 框架（OpenClaw、QwenPaw）通过交互式向导或 Web Console 配置提供商。
3. **验证连接**：发送简单请求（如 `"你好"`）确认响应正常；AIGC 类任务需遵循异步流程（创建任务 → 轮询 `task_id`）[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。
4. **高级能力**：启用思考模式、[多模态](../concepts/multi-modal.md)输入（图片）、自定义 Skill（如百炼 CLI）需按各工具文档单独配置。

## 限制和注意事项

- **套餐适用范围严格受限**：Token Plan 个人版/团队版及 Coding Plan **仅允许用于 AI 编程工具和 OpenClaw 类 Agent**，禁止用于 Dify、n8n、Postman 等工作流平台或自动化脚本，违规可能导致订阅暂停 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。
- **模型兼容性差异**：`qwen3.8-max-preview` 在 Anthropic 协议下需 `api_mode: anthropic_messages`，而在 OpenAI 协议下需 `extra_body: {enable_thinking: true}`；部分工具（如 Codex）对 `qwen3.8-max-preview` 要求 Responses API，其他模型需降级至旧版 Codex 使用 Chat API。
- **免费额度约束**：按量计费新用户免费额度**仅限华北2（北京）地域**，跨地域调用（如新加坡 Workspace）将立即计费 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **错误排查优先级**：报错 `401 Incorrect API key provided` 应首先核对 Key 与 Base URL 是否来自同一方案及地域；`400 InternalError.Algo.InvalidParameter` 通常需启用 R1 messages 格式（Cline）或思考模式开关（Cherry Studio）。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)


