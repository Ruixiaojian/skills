# use chat client or development tool

阿里云百炼支持通过多种主流 AI 开发工具和客户端接入模型服务，覆盖命令行、IDE 插件、桌面应用及自定义开发场景。开发者可根据使用习惯选择 OpenClaw、Claude Code、Hermes Agent 等 CLI 工具，或 Cursor、Cline、Qoder 等 IDE 集成方案，亦可直接通过 Postman/cURL 进行 API 测试。所有工具均兼容 OpenAI 或 Anthropic 协议，需按计费方案配置对应 Base URL 与 API Key。

## 支持的模型/功能

百炼支持的模型因计费方案而异，**[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan 和按量计费**均提供 Qwen3 系列（如 `qwen3.8-max`、`qwen3.7-plus`）、GLM-5.2、DeepSeek-V4 等文本生成模型；部分工具（如 [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)）还支持多模态输入（text + image）。Qwen3 系列模型普遍支持 **thinking 模式**（需显式启用 `enable_thinking` 或 `thinking: { type: "enabled" }`），适用于复杂推理任务。

> **注意**：文档中对 `qwen3.8-max` 的上下文窗口描述存在不一致——[OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md) 标注为 `983616` tokens，而 [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md) 和 [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md) 均标注为 `983616`，但 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md) 未明确说明。以官方模型文档为准，实际值应以控制台或 `GET /models` 接口返回为准。

图像/视频生成类模型（如 `wan2.6-t2i`）**不通过 Chat Client 接入**，需使用专用异步 API（参见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)），且仅支持按量计费方案。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `Base URL` | 必填，协议与计费方案强绑定：<br>- OpenAI 兼容：`/compatible-mode/v1` 结尾<br>- Anthropic 兼容：`/apps/anthropic` 结尾 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（[Token](../concepts/token.md) Plan 个人版，OpenAI）<br>`https://coding.dashscope.aliyuncs.com/apps/anthropic`（Coding Plan，Anthropic） |
| `API Key` | 方案专属，**不可混用**。[Token](../concepts/token.md) Plan 个人版 Key 无法用于 Coding Plan，按量计费 Key 必须与 Base URL 地域匹配 | `sk-xxx`（需从对应控制台页面获取） |
| `Model ID` | 必填，需严格匹配套餐支持列表中的模型 ID。部分工具（如 Cursor）要求特殊格式：`kimi-k2.6` → `kimi-k2-6`，`glm-5.2` → `glm-5-2` | `qwen3.8-max`, `qwen3.6-flash` |
| `thinking` / `enable_thinking` | Qwen3 系列模型启用思考模式的必需参数，不同工具配置方式不同：<br>- OpenClaw：`compat.thinkingFormat: "openai"` + 请求体传 `"enable_thinking": true`<br>- Qwen Code：`generationConfig.extra_body.enable_thinking: true`<br>- Kilo CLI：`options.thinking.type: "enabled"` | `{"type": "enabled", "budgetTokens": 262144}` |

## 使用方式

### 1. 客户端/CLI 工具（推荐快速上手）
- **安装**：统一依赖 Node.js ≥18（[Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)、[Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)、[Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md) 等）或 Python（[Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)、[QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)）。
- **配置**：  
  - CLI 工具（如 `claude`, `hermes`, `qwen`）：编辑 `~/.<tool>/config.json` 或运行交互式 `/auth` 命令。  
  - 桌面/IDE 工具（如 Cherry Studio、Cursor、Cline）：在设置界面填写 Base URL、API Key、Model ID。  
- **验证**：执行简单命令（如 `claude "hello"`）或对话框输入“你好”，确认响应正常。

### 2. 自定义开发（生产环境）
- 使用官方 SDK（Node.js/Python/Java）或直接调用 HTTP API。  
- **必须遵循协议**：OpenAI 兼容端点使用 `/v1/chat/completions`；Anthropic 兼容端点使用 `/v1/messages`。  
- **异步任务**（图像/视频生成）：需两步调用——先 `POST /api/v1/services/aigc/text2image/image-synthesis` 创建任务，再轮询 `GET /api/v1/tasks/{task_id}` 获取结果（详见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)）。

### 3. 不支持的场景
- **工作流平台**（Dify、n8n、Coze）：**禁止使用 Token Plan/Coding Plan**，仅允许按量计费（[Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 文档明确强调此限制）。  
- **API 测试工具**（Postman、Insomnia）：仅限测试，**不得用于生产调用**。  
- **自定义后端脚本**：同上，需使用按量计费 Key 并确保合规调用。

## 限制和注意事项

- **地域一致性**：按量计费的 `API Key`、`Base URL`、`WorkspaceId` 必须属于同一地域（华北2/新加坡/美国），否则返回 401。  
- **模型权限隔离**：各套餐支持的模型列表独立，Token Plan 团队版 Key 无法调用 Coding Plan 模型（反之亦然）。  
- **免费额度限制**：新人免费额度**仅限华北2（北京）地域**的按量计费模型，其他地域或套餐不享受（[Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md) 常见问题已说明）。  
- **凭证安全**：避免硬编码 API Key，CLI 工具建议使用环境变量（如 `ANTHROPIC_AUTH_TOKEN`）；桌面工具应启用本地加密存储。  
- **错误排查优先级**：  
  1. 检查 `401`：确认 Key 与 Base URL 方案/地域匹配；  
  2. 检查 `400`：确认 Model ID 拼写正确（如 `qwen3.8-max` 非 `qwen38max`），Qwen3 模型是否启用 `enable_thinking`；  
  3. 检查 `429`：超出套餐速率限制，需降频或升级套餐。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)


