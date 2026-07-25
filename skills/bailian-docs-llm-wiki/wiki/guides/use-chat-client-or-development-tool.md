# use chat client or development tool

阿里云百炼支持通过多种主流 AI 开发工具和客户端接入模型服务，包括终端编程助手（如 Hermes Agent、Qwen Code）、桌面 IDE（如 Cursor、Qoder）、开源平台（如 Dify、OpenClaw）及通用 HTTP 工具（如 Postman、cURL）。所有工具均基于 OpenAI 或 Anthropic 兼容协议，通过配置 API Key 和 Base URL 即可快速对接，无需修改业务逻辑。本文档汇总各工具共性能力与关键配置要点，供开发者统一参考。

## 支持的模型/功能

百炼当前支持的模型因计费方案而异，但核心文本生成模型在各方案中高度重叠。**[Token](../concepts/token.md) Plan 个人版**与**[Token](../concepts/token.md) Plan 团队版**均明确支持 `qwen3.8-max-preview`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2` 和 `deepseek-v4-pro` 等模型 [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)。**Coding Plan** 主要覆盖 `qwen3.7-plus` 等中高阶模型，而**按量计费**支持最全模型集，包括万相（WanX）、Qwen-VL、QVQ 等多模态模型 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

> **注意**：`qwen3.8-max-preview` 的思考模式（thinking）为强制开启且不可关闭，其 `temperature` 在思考模式下有硬性下限 0.6，低于该值将被自动修正；`reasoning_effort` 参数仅在该模型上生效，可选 `xhigh`/`high`/`low` [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)。其他模型（如 `qwen3.7-plus`）虽支持 `enable_thinking: true`，但无 `reasoning_effort` 控制能力。

所有工具均支持标准聊天接口（`/chat/completions`）与流式响应。部分工具（如 Qoder、Cline）还支持通过 Skill/MCP 扩展调用百炼 CLI 能力（如文生图、视频生成），需额外安装 `bailian-cli` 并配置 Node.js 18+ 环境 [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)。

## 关键参数

| 参数 | 说明 | 取值示例 |
|------|------|----------|
| `Base URL` | 必填，决定协议类型与计费归属 | OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic 兼容：`https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| `API Key` | 必填，严格绑定计费方案与地域 | [Token](../concepts/token.md) Plan 个人版 Key 仅可用于对应 `token-plan.*` 域名，与 Coding Plan Key 不互通 |
| `Model ID` | 必填，需与所选方案支持列表一致 | `qwen3.8-max-preview`（Token Plan）、`qwen3.7-plus`（Coding Plan）；注意命名规范：`kimi-k2.6` → `kimi-k2-6` [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) |
| `thinking` / `enable_thinking` | 部分模型（如 qwen3.8-max-preview）需显式启用 | `true`（OpenAI 兼容需通过 `extra_body.enable_thinking`；Anthropic 兼容由 `api_mode: anthropic_messages` 自动启用） |

## 使用方式

### 安装与初始化
- **终端工具**（Hermes Agent、Qwen Code、Kilo CLI）：依赖 Node.js（v18+）或 Python（3.10~3.13），通过 `npm install -g` 或 `curl` 一键脚本安装。
- **桌面客户端**（Cursor、Cherry Studio、Chatbox）：直接下载安装包，启动后进入设置界面配置模型提供方。
- **IDE 插件**（Cline、Qoder JetBrains）：在 VS Code 或 JetBrains 插件市场搜索安装，配置入口位于侧边栏或设置菜单。
- **平台型工具**（Dify、OpenClaw）：需先完成基础环境（Node.js 22.19+ 或 Python），再通过 CLI 初始化或 Web UI 引导配置。

### 配置流程（通用）
1. 获取对应计费方案的专属 API Key（[Token Plan 个人版](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)、[Coding Plan](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan) 等）；
2. 根据方案选择 Base URL（区分 OpenAI/Anthropic 协议及地域）；
3. 在工具配置界面填写 Key、URL、Model ID；
4. 保存并验证：发送 `你好` 或运行 `/auth` 命令，确认模型返回有效响应。

> **注意**：`qwen3.8-max-preview` 在 Anthropic 兼容模式下必须使用 `api_mode: anthropic_messages`，若误配为 OpenAI 模式将导致 `400 Bad Request` [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)。

## 限制和注意事项

- **方案隔离性**：Token Plan 个人版、团队版、Coding Plan 的 API Key 互不通用，且不能混用 Base URL。例如，Token Plan Key 用于 `coding.dashscope.aliyuncs.com` 将返回 `401 Unauthorized` [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)。
- **地域一致性**：按量计费的 API Key 必须与 Base URL 地域严格匹配（如北京 Key 配北京 URL），否则触发 `401` 或额度无法抵扣 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **模型兼容性**：Token Plan 与 Coding Plan **不支持**工作流平台（Dify、n8n）、API 测试工具（Postman、Insomnia）及自定义后端代码直接调用，仅限 AI 编程工具和 OpenClaw 类 Agent 使用 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。
- **免费额度限制**：新人免费额度仅适用于华北2（北京）地域的模型，且各模型额度独立计算，不跨模型共享 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **图像/视频生成特殊性**：此类 API 采用异步机制（`X-DashScope-Async: enable`），需先创建任务获取 `task_id`，再轮询查询结果，**不支持同步响应** [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

## 来源文档

- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)


