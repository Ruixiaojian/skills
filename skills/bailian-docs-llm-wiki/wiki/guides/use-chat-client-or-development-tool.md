# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程客户端与开发工具接入模型服务，覆盖本地 CLI 工具（如 Hermes Agent、Qwen Code）、桌面 IDE（如 Cursor、Cherry Studio）、VS Code [插件](../concepts/plugin.md)（如 Cline）、开源 Agent 平台（如 OpenClaw、QwenPaw）以及工作流平台（如 Dify）。所有工具均通过 OpenAI 兼容协议或 Anthropic 兼容协议对接，开发者可基于自身技术栈和使用场景选择合适工具。

## 支持的模型/功能

百炼当前支持的模型因计费方案而异，**[Token](../concepts/token.md) Plan 个人版**与**[Token](../concepts/token.md) Plan 团队版**均支持 `qwen3.8-max-preview`（强制开启思考模式）、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro` 等文本生成模型；**Coding Plan** 主要支持 `qwen3.7-plus` 等面向编码优化的模型；**按量计费**方案覆盖最全，包括 Qwen-VL、QVQ、Qwen-Omni、万相（wan2.6-t2i）等多模态与 AIGC 模型。  
> **注意**：Dify 明确不支持 [Token](../concepts/token.md) Plan 个人版、Token Plan 团队版和 Coding Plan 接入，仅允许使用按量付费 API Key，详见 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 文档。  
视觉与视频生成类模型（如文生图、文生视频）需通过异步 API 调用，不适用于标准聊天客户端，推荐使用 Postman 或 cURL 进行测试验证，具体流程见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。  
此外，部分工具（如 Cursor 免费版、Codex 旧版本）对模型调用存在限制：Cursor 免费版仅支持 Auto 模式，不支持自定义模型；Codex 对 `glm-5` 等模型需降级至 v0.80.0 并使用 Chat/Completions API，详见 [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)。

## 关键参数

| 参数 | 说明 | 常见取值示例 |
|------|------|-------------|
| `base_url` / `baseUrl` / `API 主机` | 模型服务端点地址，**必须与所选计费方案及地域严格匹配** | Token Plan 个人版 OpenAI 协议：<br>`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>按量计费（北京）：<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` / `API 密钥` | 认证凭证，**不同计费方案的 API Key 不通用** | Token Plan 个人版专属 Key（控制台路径：`/efm/subscription/overview`） |
| `model` / `Model ID` | 模型标识符，注意命名规范差异 | `qwen3.8-max-preview`（标准名），但在 Cursor 中 `kimi-k2.6` 需写为 `kimi-k2-6`，`glm-5.2` 需写为 `glm-5-2`，详见 [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) |
| `api_mode` / `wire_api` | 协议类型标识（仅 Anthropic 协议工具需显式指定） | `anthropic_messages`（Hermes Agent）、`responses`（Codex） |
| `enable_thinking` / `thinking` | qwen3.8-max-preview 强制启用参数，不可关闭 | `true`（OpenClaw、Qwen Code 等均需在配置中显式启用） |

> **注意**：`qwen3.8-max-preview` 的 `temperature` 在思考模式下有硬性下限（0.6），传入值低于该阈值将被自动修正，此行为在 [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)、[Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)、[Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md) 等多份文档中一致确认。

## 使用方式

1. **安装工具**：根据操作系统选择对应安装方式（npm、curl 脚本、GUI 安装包等），多数工具要求 Node.js ≥18（如 [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)、[Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)）或 Python（如 [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)）。
2. **配置凭证**：  
   - CLI 工具（如 Hermes Agent、Qwen Code）通常提供 `hermes config set` 或 `/auth` 交互式命令；  
   - GUI 工具（如 Cursor、Cherry Studio）通过设置界面填写 API Key、Base URL 和 Model ID；  
   - [插件](../concepts/plugin.md)（如 Cline）在 VS Code 扩展设置中选择 “Bring my own API key” 并填入参数；  
   - 开源平台（如 QwenPaw）通过 Web Console 的「设置 > 模型」完成配置。
3. **验证连接**：发送简单请求（如“你好”）并检查响应；若报错，优先排查 API Key 与 Base URL 是否来自同一计费方案及地域（如 [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md) 报错 401 的常见原因）。
4. **高级功能**：启用思考模式（R1 messages format）、配置 `reasoning_effort`（xhigh/medium/low）、调整 `max_tokens` 等需查阅各工具专属文档的进阶配置节。

## 限制和注意事项

- **计费方案适用范围严格隔离**：Token Plan 个人版/团队版/Coding Plan 仅限 AI 编程工具（CLI、IDE、Agent）使用；工作流平台（Dify、n8n）、API 测试工具（Postman）、自定义后端应用等**明确禁止接入**，违规可能导致订阅暂停或 API Key 封禁，详见 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。
- **地域绑定强制**：按量计费的 API Key 与 `base_url` 中的 `WorkspaceId` 及地域必须一致；Token Plan 与 Coding Plan 的 Base URL 为固定域名，不支持跨地域调用。免费额度仅适用于华北2（北京）地域，其他地域调用将直接计费（[Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)）。
- **模型兼容性差异**：  
  - OpenAI 协议工具（Cursor、Cherry Studio、QwenPaw）普遍使用 `/compatible-mode/v1`；  
  - Anthropic 协议工具（Hermes Agent、Claude Code、OpenClaw）使用 `/apps/anthropic`；  
  - Codex 对部分模型需降级并切换 `wire_api` 为 `chat`（[Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)）；  
  - Qwen3.8-max-preview 的思考模式参数（`enable_thinking`）在 OpenClaw、Qwen Code、Kilo CLI 等配置中均为必需字段，缺失将导致调用失败。
- **错误排查优先级**：遇到 401（Unauthorized）先核对 API Key 与 Base URL 方案一致性；遇到 400（InvalidParameter）检查是否遗漏 `Enable R1 messages format`（Cline）或 `reasoning_effort` 格式错误；遇到模型不可用，确认所选模型是否在当前套餐支持列表内（如 [Qoder CN](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) 报错“自定义模型服务异常”常因模型不支持）。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


