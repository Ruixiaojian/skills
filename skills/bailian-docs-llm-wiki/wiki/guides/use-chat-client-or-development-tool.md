# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务。开发者可基于 OpenAI 或 Anthropic 兼容协议，使用 [Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan 或按量计费方案快速集成。所有工具均需正确配置 API Key、Base URL 及模型 ID，且不同计费方案的凭证不互通。

## 支持的模型/功能

- **通用文本模型**：qwen3.8-max-preview（强制启用思考模式）、qwen3.7-max、qwen3.7-plus、qwen3.6-flash、glm-5.2、deepseek-v4-pro 等，详见 [Token Plan 个人版支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview)。
- **视觉与[多模态](../concepts/multi-modal.md)模型**：Qwen-VL、QVQ、Qwen-Omni、Qwen-Audio、Qwen-OCR 等，**仅支持通过 Dify 的 HTTP 节点或百炼原生 API 调用**，不支持直接在 Chatbox、Cursor 等客户端中配置 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。
- **图像/视频生成模型**：wan2.6-t2i、wan2.5-t2i-preview 等，**必须使用异步调用机制**（创建任务 + 轮询查询），不支持同步 REST 调用 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。
- **Embedding/Rerank 模型**：text-embedding-v4、gte-rerank-v2 等，仅限在 Dify 知识库等特定场景中配置使用。

> **注意**：[Token](../concepts/token.md) Plan 个人版、[Token](../concepts/token.md) Plan 团队版和 Coding Plan **不支持工作流/自动化平台（如 Dify、n8n、Coze）及 API 测试工具（如 Postman、cURL）**；违规使用可能导致订阅暂停或 API Key 封禁 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `API Key` | 方案专属密钥，不可跨方案复用 | [Token](../concepts/token.md) Plan 个人版：`sk-xxx`（控制台获取） |
| `Base URL` | 必须与 API Key 所属方案及地域严格匹配 | OpenAI 兼容：<br>`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic 兼容：<br>`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| `Model ID` | 模型名称需与方案支持列表一致；部分工具要求别名（如 `kimi-k2.6` → `kimi-k2-6`） | `qwen3.8-max-preview`, `glm-5-2` |
| `thinking` / `enable_thinking` | qwen3.8-max-preview 强制启用，不可关闭；temperature < 0.6 时自动设为 0.6 | `true`（必填） |
| `reasoning_effort` | 控制推理深度，取值 `xhigh`/`medium`/`low`，默认 `xhigh` | `xhigh` |

## 使用方式

1. **安装工具**：根据文档要求安装对应 CLI 或 GUI 工具（如 `npm install -g opencode-ai`、下载 Cursor 安装包等）。
2. **配置凭证**：
   - 多数工具提供交互式 `/auth` 或图形化设置界面（如 Qwen Code、Qoder、Cherry Studio）；
   - 部分工具需手动编辑配置文件（如 `~/.hermes/config.yaml`、`~/.qwen/settings.json`）；
   - 环境变量方式（如 Codex 的 `OPENAI_API_KEY`）需 `source` 生效。
3. **验证连接**：发送简单请求（如“你好”）或运行 `--version` 命令确认环境就绪。
4. **高级能力**：
   - 启用思考模式需显式设置 `enable_thinking: true` 或勾选对应开关；
   - 使用百炼 CLI 技能需先全局安装 `npm install -g bailian-cli`，再在工具中配置 API Key [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)。

## 限制和注意事项

- **地域绑定**：按量计费的 `WorkspaceId` 和 API Key 必须同地域；免费额度仅限华北2（北京）地域 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **模型兼容性**：
  - qwen3.8-max-preview 仅支持 Anthropic 协议下的 `thinking` 模式，OpenAI 协议下需额外配置 `extra_body.enable_thinking=true`；
  - 部分旧版工具（如 Codex v0.80.0）对非 Responses API 模型（如 glm-5）需降级使用。
- **权限校验**：RAM 子账号需在业务空间中显式授予模型调用权限 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **错误排查**：
  - `401 Incorrect API key provided`：检查 Key/URL 是否同方案、同地域；
  - `400 InternalError.Algo.InvalidParameter`：Qwen3/QwQ 模型需启用 R1 messages format（Cline 设置中勾选）；
  - “Named models unavailable”：Cursor 免费版仅支持 Auto 模式，需升级至 Pro 版本 [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)。

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
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)




