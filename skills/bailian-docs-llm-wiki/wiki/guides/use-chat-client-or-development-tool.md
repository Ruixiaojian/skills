# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、Web 应用和低代码工作流等场景。开发者可根据使用习惯选择适配 OpenAI 或 Anthropic 兼容协议的客户端，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan、按量计费）配置对应凭证。所有工具均需使用百炼提供的标准化 Base URL 和专属 API Key，**严禁跨方案混用凭证**。

## 支持的模型/功能

百炼当前支持的模型因计费方案而异，**仅文本生成类模型在 [Token](../concepts/token.md) Plan 和 Coding Plan 中可用**；图像/视频/多模态模型（如 `wan2.6-t2i`、`qwen-vl`、`qvq`）**仅支持按量计费调用**。常见模型包括：

- `qwen3.8-max-preview`：强制启用思考模式（`thinking: true`），不支持关闭；`temperature < 0.6` 时自动修正为 0.6；`reasoning_effort` 可设为 `xhigh`/`medium`/`low`（[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)）。
- `qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro`：均支持思考模式，但部分工具（如 Codex）对 `glm-5.2` 等旧模型需降级至 v0.80.0 并使用 Chat/Completions API（[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)）。
- 视觉与多模态模型（如 `qwen-vl`、`wan2.6-t2i`）：**仅限按量计费**，不可用于 [Token](../concepts/token.md) Plan 或 Coding Plan（[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)）。

> **注意**：Dify 明确不支持 Token Plan 个人版、Token Plan 团队版和 Coding Plan 接入，仅允许使用按量计费 API Key；将套餐 API Key 用于 Dify 等工作流平台属于违规行为，可能导致订阅暂停或 Key 封禁（见 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 文档）。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `Base URL` | 必填，决定协议类型与地域。OpenAI 兼容端点以 `/compatible-mode/v1` 结尾；Anthropic 兼容端点以 `/apps/anthropic` 结尾。地域必须与 API Key 匹配。 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（Token Plan 个人版，OpenAI 协议）<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`（按量计费，Anthropic 协议） |
| `API Key` | 必填，严格绑定计费方案与地域。Token Plan 个人版 Key 不能用于 Token Plan 团队版，按量计费 Key 必须与 Base URL 中的 `WorkspaceId` 所属地域一致。 | `sk-xxxxxxxxxxxxx`（需从控制台对应页面获取） |
| `Model ID` | 必填，模型名称需与所选方案支持列表完全一致。部分工具（如 Cursor、Cherry Studio）要求特殊别名：`kimi-k2.6` → `kimi-k2-6`，`glm-5.2` → `glm-5-2`。 | `qwen3.8-max-preview`、`qwen3.7-plus` |
| `enable_thinking` / `thinking` | 对于 Qwen3 思考模型，多数工具默认启用；若显式传参，值必须为 `true`（如 Chatbox 报错 `The value of the enable_thinking parameter is restricted to True` 即因传 `false`）。 | `{"extra_body": {"enable_thinking": true}}`（Qwen Code） |

## 使用方式

### 1. 安装与初始化
- **CLI 工具**（如 `OpenClaw`、`Hermes Agent`、`Claude Code`、`Qwen Code`）：依赖 Node.js ≥18（`OpenClaw` 要求 ≥22.19.0），通过 `npm install -g` 或一键脚本安装（[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)）。
- **IDE 插件**（如 `Cline`、`Qoder JetBrains 插件`）：在 VS Code 或 JetBrains 市场搜索安装，配置入口通常在侧边栏图标或设置 > 模型。
- **桌面/Web 客户端**（如 `Cursor`、`Cherry Studio`、`Chatbox`）：从官网下载安装包，配置入口在设置 > 模型 > 添加提供商。
- **低代码平台**（如 `Dify`）：需安装官方插件（如“通义千问”），并在模型供应商中配置 API Key 与端点。

### 2. 配置凭证（通用流程）
1. 获取对应计费方案的 API Key（链接见各文档）；
2. 根据协议选择 Base URL（OpenAI 或 Anthropic）；
3. 在工具配置界面填写 Key、URL、Model ID；
4. **验证**：发送简单请求（如“你好”），确认返回非错误响应。

### 3. 特殊能力启用
- **思考模式**：`qwen3.8-max-preview` 等模型需在请求体中显式启用（如 Qwen Code 的 `extra_body.enable_thinking: true`）；
- **视觉能力**：Dify 中需在 LLM 节点开启“视觉”开关；QwenPaw 等需在模型设置中启用 `input: ["text", "image"]`；
- **异步任务**（图像/视频生成）：必须使用 `X-DashScope-Async: enable` 头创建任务，再轮询 `GET /tasks/{task_id}` 查询结果（[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)）。

## 限制和注意事项

- **方案隔离**：Token Plan 个人版、Token Plan 团队版、Coding Plan 的 API Key **完全不通用**，且仅限指定工具类型（AI 编程工具、OpenClaw 类 Agent）。工作流平台（Dify、n8n）、API 测试工具（Postman）、自定义后端应用**禁止使用**这些套餐 Key（见 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)）。
- **地域强绑定**：按量计费 Key 与 `WorkspaceId` 所属地域必须一致；免费额度仅适用于华北2（北京）地域，其他地域调用直接计费（[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)）。
- **模型兼容性**：
  - `qwen3.8-max-preview` 的 `temperature` 低于 0.6 时会被强制修正，`reasoning_effort` 未提供时默认 `xhigh`；
  - Codex 对 `glm-5.2` 等模型需降级并切换 API（Responses vs Chat/Completions）；
  - Cursor 免费版仅支持 Auto 模式，调用自定义模型需升级至 Pro 及以上。
- **错误排查**：
  - `401 Unauthorized`：检查 Key 与 URL 是否同属一方案及地域；
  - `400 InvalidParameter`：启用 R1 messages format（Cline）或确认 `enable_thinking` 为 `true`（Qwen Code）；
  - `Unknown Custom model Exception`（Qoder CN）：确认提供商类型（Token Plan/Coding Plan）与实际套餐一致。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


