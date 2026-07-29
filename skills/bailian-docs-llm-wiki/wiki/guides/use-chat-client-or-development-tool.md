# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，涵盖 OpenAI 兼容协议与 Anthropic 兼容协议。开发者可根据使用场景（CLI、IDE 插件、桌面应用或低代码平台）选择适配工具，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan 或按量计费）配置凭证。所有工具均需正确匹配 API Key、Base URL 与模型 ID，否则将触发 401 或 400 错误。

## 支持的模型/功能

- **通用文本生成模型**：`qwen3.8-max-preview`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro` 等，覆盖 [Token](../concepts/token.md) Plan 个人版、[Token](../concepts/token.md) Plan 团队版、Coding Plan 及按量计费全套餐 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)。
- **思考模式（Reasoning）**：`qwen3.8-max-preview` 强制启用 thinking，不支持关闭；`temperature` 小于 0.6 时自动修正为 0.6；`reasoning_effort` 可设为 `xhigh`/`medium`/`low` [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)。
- **多模态能力**：`qwen3.7-plus`、`qwen3.6-flash` 等支持 `text` + `image` 输入，但仅限输出 `text`；Qwen-VL、QVQ、Qwen-Omni 等视觉/音频模型**不可直接在 Dify 插件中配置**，需通过 Chatflow 的 HTTP 节点调用 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。
- **图像/视频生成**：`wan2.6-t2i`、`wan2.2-t2v-turbo` 等万相模型需通过异步 API 调用（创建任务 → 轮询查询），不支持同步响应 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

> **注意**：文档 17 明确指出，Token Plan 个人版、团队版和 Coding Plan **不支持接入工作流平台（如 Dify、Coze、n8n）或 API 测试工具（如 Postman、cURL）**；但文档 15 却以 Postman/cURL 为例演示图像生成 API 调用。该矛盾表明：Postman/cURL 仅适用于**功能验证与调试**，且必须使用**按量计费 API Key**（非 Token Plan/Coding Plan Key），否则将因权限不符导致 401。生产环境应使用 SDK 或自实现 HTTP 客户端。

## 关键参数

| 参数 | 含义 | 常见取值 | 注意事项 |
|------|------|----------|----------|
| `base_url` | 模型服务端点 | OpenAI 协议：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic 协议：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | 地域必须与 API Key 匹配；按量计费需替换 `{WorkspaceId}`；Token Plan/Coding Plan 的 URL **不可混用** |
| `api_key` | 认证凭证 | Token Plan 个人版 Key、Coding Plan Key、按量计费 Key | 三类 Key **完全不通用**；子账号需确保业务空间模型调用权限 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md) |
| `model_id` | 模型标识符 | `qwen3.8-max-preview`、`qwen3.7-plus`、`glm-5.2` | Cursor 等工具需对部分模型名做转换（如 `glm-5.2` → `glm-5-2`）；Qwen3 思考模式模型需显式启用 `enable_thinking: true` |
| `thinking` / `enable_thinking` | 思考模式开关 | `true`（强制启用）或 `false`（部分模型不支持） | `qwen3.8-max-preview` 的 `thinking` 不可设为 `false`；CLI 工具（如 Cline）需勾选 **Enable R1 messages format** 才能正确解析思考流 |

## 使用方式

### 1. 工具安装
- **CLI 工具**（OpenClaw、Hermes Agent、Claude Code、Qwen Code、Kilo CLI）：依赖 Node.js ≥18（部分要求 ≥22），通过 `npm install -g` 或一键脚本安装。
- **IDE 插件**（Cline、Claude Code、Kilo Code）：在 VS Code 或 JetBrains IDE 扩展市场搜索安装。
- **桌面客户端**（Cursor、Cherry Studio、Chatbox、Qoder IDE）：从官网下载安装包。
- **低代码平台**（Dify）：通过云服务或私有化部署，安装「通义千问」插件或配置 OpenAI 兼容端点。

### 2. 凭证配置
- **统一原则**：所有工具均需配置 `API Key` + `Base URL` + `Model ID` 三元组。
- **配置路径示例**：
  - OpenClaw：`~/.openclaw/openclaw.json`
  - Hermes Agent：`~/.hermes/config.yaml`
  - Qwen Code：`~/.qwen/settings.json`
  - Dify：插件设置页或 Chatflow 的 HTTP 节点环境变量。
- **协议选择**：
  - OpenAI 兼容：`base_url` 含 `/compatible-mode/v1`，使用 `openai` SDK 或 `@ai-sdk/openai-compatible`。
  - Anthropic 兼容：`base_url` 含 `/apps/anthropic`，使用 `anthropic` SDK 或 `@ai-sdk/anthropic`。

### 3. 高级能力启用
- **思考模式**：在请求体中添加 `"extra_body": {"enable_thinking": true}`（Qwen Code）、`"thinking": {"type": "enabled"}`（OpenCode/Kilo CLI）或启用客户端 UI 开关（Cline、Cursor）。
- **[多模态输入](../concepts/multi-modal-input.md)**：确保模型支持 `image` 输入（如 `qwen3.7-plus`），并在请求中构造 `content` 数组包含 `{"type": "image_url", "image_url": {...}}`。
- **[异步任务](../concepts/asynchronous-task.md)**（图像/视频）：调用 `POST /api/v1/services/aigc/text2image/image-synthesis` 获取 `task_id`，再轮询 `GET /api/v1/tasks/{task_id}` 直至 `task_status == "SUCCEEDED"`。

## 限制和注意事项

- **套餐适用范围限制**：Token Plan 个人版/团队版、Coding Plan **仅允许用于 AI 编程工具（如 Cursor、Qoder）和 Agent 类应用（如 OpenClaw、QwenPaw）**；禁止用于 Dify、Postman、自定义后端等场景，违规可能导致订阅暂停 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。
- **地域绑定**：按量计费的 API Key 与 `WorkspaceId` 必须同地域（北京/新加坡/美国）；Token Plan 的 Base URL 固定为 `cn-beijing`，**不支持跨地域调用**。
- **模型兼容性**：
  - `qwen3.8-max-preview` 在 Codex 中需使用 Responses API（`wire_api = "responses"`），而 `glm-5` 等旧模型需降级到 Codex v0.80.0 并使用 Chat API。
  - Cursor 免费版仅支持 Auto 模式，**无法手动选择模型**，必须升级至 Pro 版本。
- **错误排查优先级**：
  1. 检查 `API Key` 与 `Base URL` 是否来自同一计费方案（如 Token Plan Key 配 Token Plan URL）；
  2. 验证 `model_id` 是否在对应套餐的支持列表中（如 Token Plan 团队版不支持 `wan2.6-t2i`）；
  3. 确认客户端是否启用思考模式开关（报错 `The value of the enable_thinking parameter is restricted to True` 即为此因）。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


