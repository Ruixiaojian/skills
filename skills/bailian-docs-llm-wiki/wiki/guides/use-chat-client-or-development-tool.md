# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、Web 应用和低代码工作流等场景。开发者可根据使用习惯选择 OpenAI 兼容协议或 Anthropic 兼容协议，按需配置 [Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan 或按量计费方案。所有工具均需正确匹配 API Key 与 Base URL 的计费方案及地域，否则将触发 401 错误。

## 支持的模型/功能

百炼支持的模型因计费方案而异，**[Token](../concepts/token.md) Plan 个人版/团队版**和**Coding Plan**仅限在 AI 编程工具（如 Hermes Agent、Qwen Code）和 OpenClaw 类型 Agent 中使用；**按量计费**是唯一支持 Dify 等工作流平台的方案 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。各方案支持的核心模型包括：

- **Qwen 系列**：`qwen3.8-max`（支持思考模式、[多模态](../concepts/multi-modal.md)输入）、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`
- **GLM 系列**：`glm-5.2`（仅文本）
- **DeepSeek 系列**：`deepseek-v4-pro`、`deepseek-v4-flash-0731`
- **万相（AIGC）模型**：如 `wan2.6-t2i`，需通过异步 API 调用，不支持直接集成到 Chat Client [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)

> **注意**：部分工具对模型名称有特殊要求。例如 Cursor 要求 `kimi-k2.6` 写为 `kimi-k2-6`，`glm-5.2` 写为 `glm-5-2`；而 OpenClaw 配置中直接使用 `qwen3.8-max` 等原始 ID [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)。

## 关键参数

所有工具均依赖以下三类核心参数，且必须严格匹配：

| 参数 | 说明 | 示例值 |
|------|------|--------|
| **API Key** | 方案专属密钥，不可跨方案复用 | [Token](../concepts/token.md) Plan 个人版 Key：`sk-xxx`（控制台获取） |
| **Base URL** | 必须与 API Key 所属方案及地域一致 | OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic 兼容：`https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| **Model ID** | 模型标识符，需从对应方案支持列表中选取 | `qwen3.8-max`、`glm-5.2` |

> **注意**：`WorkspaceId` 在按量计费的 Base URL 中为必填项，需从[业务空间管理页面](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)获取，遗漏或错误将导致 404 或 401 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)。

## 使用方式

### 安装与初始化
- **CLI 工具**（如 Hermes Agent、Qwen Code）：推荐使用官方一键脚本（`curl`/`iwr`）或 `npm install -g`，安装后需执行 `hermes config set` 或 `/auth` 命令完成向导式配置。
- **IDE 插件**（如 Cline、Claude Code）：在 VS Code 或 JetBrains 插件市场安装后，在设置界面填写 Base URL、API Key 和 Model ID。
- **桌面/Web 应用**（如 Cursor、Cherry Studio）：下载安装后，在 Settings > Models 中添加自定义提供方，选择 OpenAI 兼容协议并填入凭证。
- **低代码平台**（如 Dify）：仅支持按量计费，需安装“通义千问”插件并在设置中填入 API Key；万相等 AIGC 模型需通过 HTTP 节点调用异步 API [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

### 协议选择
- **OpenAI 兼容协议**：Base URL 以 `/compatible-mode/v1` 结尾，适用于绝大多数工具（Cursor、Qwen Code、Cherry Studio 等）。
- **Anthropic 兼容协议**：Base URL 以 `/apps/anthropic` 结尾，适用于 Hermes Agent、Claude Code 等明确支持该协议的工具。

## 限制和注意事项

- **方案隔离性**：Token Plan 个人版、Token Plan 团队版、Coding Plan 的 API Key 与 Base URL 严格绑定，混用将返回 `401 Incorrect API key provided`。Dify 等工作流平台明确禁止使用套餐 Key，仅允许按量计费 Key [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。
- **地域约束**：按量计费的免费额度仅适用于华北2（北京）地域；若使用新加坡或美国端点，即使 Key 有效也会产生费用 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **模型能力差异**：`qwen3.8-max` 支持 `enable_thinking` 参数和[多模态](../concepts/multi-modal.md)输入，而 `glm-5.2` 仅支持文本；部分工具（如 Codex）需额外配置 `model-catalog.local.json` 以声明上下文窗口等元数据。
- **AIGC 异步限制**：图像/视频生成 API 不支持同步响应，必须通过 `task_id` 轮询查询结果，且 `task_id` 有效期仅 24 小时 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。
- **认证失败排查**：若报错 `Unknown Custom model Exception`（Qoder CN）或 `The model xxx does not work with your current plan`（Cursor），应首先核对提供商类型（Token Plan/Coding Plan/按量付费）是否与所填 API Key 一致，并确认模型在该方案支持列表中。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/cline-tool.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)


