# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，涵盖 OpenAI / Anthropic 兼容协议的 CLI 工具（如 Hermes Agent、Claude Code）、IDE 插件（如 Cline、Qoder JetBrains 插件）、桌面应用（如 Cursor、Cherry Studio）以及低代码平台（如 Dify）。所有工具均支持按量计费、Coding Plan、Token Plan 个人版和 Token Plan 团队版四种计费方案，配置方式统一为设置 `API Key`、`Base URL` 和 `Model ID`，无需修改业务逻辑即可切换模型与后端服务。

## 支持的模型/功能

- **通用文本生成模型**：所有工具均支持 `qwen3.8-max-preview`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro` 等主流模型。其中 `qwen3.8-max-preview` 默认启用思考模式（`thinking: enabled`），不支持关闭；`temperature` 在思考模式下低于 0.6 时将自动提升至 0.6；`reasoning_effort` 可设为 `xhigh`/`high`/`low` [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)。
- **多模态能力**：`qwen3.7-plus`、`qwen3.6-flash` 等模型支持 `text` + `image` 输入，但需工具显式声明（如 OpenClaw 配置中 `"input": ["text", "image"]`）[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)。
- **图像/视频生成**：仅适用于直接调用 API 的场景（如 Postman/cURL），不支持通过 Chatbox、Cursor 等客户端直接调用万相（WanX）系列模型；推荐使用 Dify 的 Chatflow 工作流模板集成 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。
- **专属协议支持**：
  - OpenAI 兼容协议：Base URL 以 `/compatible-mode/v1` 结尾，适用于 Cursor、Chatbox、QwenPaw、Cherry Studio 等。
  - Anthropic 兼容协议：Base URL 以 `/apps/anthropic` 结尾，适用于 Hermes Agent、Claude Code、OpenClaw 等。

> **注意**：文档 4（Cursor）与文档 16（更多工具）对 Token Plan 个人版 Base URL 的表述存在差异——前者明确写为 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，后者表格中亦列此值；但文档 1 中 OpenClaw 示例配置却使用了 Anthropic 协议路径 `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`。实际应以计费方案和所选工具协议为准：**OpenAI 兼容工具必须用 `/compatible-mode/v1`，Anthropic 兼容工具必须用 `/apps/anthropic`**。混用将导致 404 或 401 错误。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `API Key` | 方案专属密钥，**不可跨方案复用**（Token Plan 个人版 Key ≠ Coding Plan Key） | `sk-xxx`（从控制台对应页面获取） |
| `Base URL` | 必须与 API Key 所属地域及计费方案严格匹配；地域不一致将触发 401 | 华北2（北京）按量计费：`https://dashscope.aliyuncs.com/compatible-mode/v1`；Token Plan 个人版：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `Model ID` | 模型标识符，部分工具要求别名（如 Cursor 要求 `kimi-k2.6` → `kimi-k2-6`） | `qwen3.8-max-preview`、`glm-5.2` |
| `enable_thinking` / `thinking` | Qwen3 思考模式开关，`qwen3.8-max-preview` 强制开启，部分工具（如 Qwen Code）需在 `extra_body` 中显式传入 `{"enable_thinking": true}` | `true`（必需） |

## 使用方式

1. **安装工具**：根据工具文档安装（如 `npm install -g @anthropic-ai/claude-code`、`curl -fsSL https://qwenpaw.agentscope.io/install.sh \| bash`）。
2. **配置凭证**：
   - CLI 工具（Hermes Agent、Claude Code、Qwen Code）：通过命令行配置或编辑 `~/.hermes/config.yaml`、`~/.claude/settings.json`、`~/.qwen/settings.json`。
   - 桌面/IDE 工具（Cursor、Chatbox、Cline）：在图形界面设置中填入 API Key、Base URL、Model ID。
   - 平台类工具（Dify、Qoder）：通过插件市场安装模型供应商，再在设置页填入 Key 和端点。
3. **验证连接**：发送简单请求（如 `"你好"`）并检查响应；若失败，优先排查 `API Key` 与 `Base URL` 是否同属一个方案及地域。

## 限制和注意事项

- **套餐适用范围限制**：Token Plan 个人版、Token Plan 团队版和 Coding Plan **仅限用于 AI 编程工具和 OpenClaw 类 Agent**，明确禁止用于工作流平台（Dify、n8n）、API 测试工具（Postman、Insomnia）或自定义后端应用 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。违规使用可能导致订阅暂停或 Key 封禁。
- **模型兼容性**：并非所有模型在所有工具中可用。例如：
  - Codex 对 `glm-5` 等旧模型需降级至 v0.80.0 并使用 `chat` API，而 `qwen3.8-max-preview` 则需 `responses` API [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)。
  - Cursor 免费版仅支持 Auto 模式，无法调用自定义模型，需升级至 Pro 版本。
- **地域与免费额度绑定**：按量计费的新人免费额度**仅适用于华北2（北京）地域**的模型调用；使用新加坡或美国地域端点将立即计费 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **思考模式强制性**：`qwen3.8-max-preview` 在所有支持该模型的工具中均强制启用思考，且 `temperature` 下限为 0.6，试图设置更低值将被忽略。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)


