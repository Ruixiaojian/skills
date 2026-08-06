# use chat client or development tool

阿里云百炼支持多种主流 AI 编程工具、桌面客户端及命令行工具通过 OpenAI 或 Anthropic 兼容协议接入。开发者可根据使用场景（CLI、IDE 插件、桌面应用或 Agent 平台）选择合适工具，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan 或按量计费）配置对应 API Key 与 Base URL。所有工具均需正确匹配协议类型、地域和模型支持范围，否则将触发 401 或 400 错误。

## 支持的模型/功能

百炼当前支持的主流模型包括 `qwen3.8-max`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro` 和 `deepseek-v4-flash-0731` 等文本生成模型；部分工具（如 Qwen Code、Claude Code、OpenClaw）还支持图像输入（`input: ["text", "image"]`）及思考模式（`enable_thinking` / `thinking: { type: "enabled" }`）。视觉模型（如 Qwen-VL、QVQ、万相）**不支持直接在 Chat Client 中配置**，需通过 Dify 工作流或 HTTP 节点调用 [图像/视频生成 API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)，详见[文档 17](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

> **注意**：文档 5（Codex）中提到“部分模型需通过 Chat/Completions API 接入并降级至 v0.80.0”，而其他工具（如 Cursor、Cherry Studio、Qoder）均明确要求使用 OpenAI 兼容协议（`/compatible-mode/v1`），且未提及版本限制。该矛盾表明 Codex 对百炼的支持存在兼容性断层，**不推荐在生产环境使用 Codex 接入百炼**，应优先选用文档 12（Cline）、文档 6（Cursor）或文档 7（Qwen Code）等明确支持新版协议的工具。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `API Key` | 方案专属密钥，**不可跨方案复用**。[Token](../concepts/token.md) Plan 个人版、团队版、Coding Plan 的 Key 互不通用；按量计费 Key 必须与 Base URL 所属地域一致。 | `sk-xxxxxxxxxxxxx` |
| `Base URL` | 协议与地域强绑定：<br>- OpenAI 兼容：`{scheme}/compatible-mode/v1`<br>- Anthropic 兼容：`{scheme}/apps/anthropic`<br>其中 `{scheme}` 需按方案替换（见下表） | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `Model ID` | 模型名称必须与所选方案支持列表完全一致。部分工具（如 Cursor、Chatbox）要求对带小数点的模型名做转换（如 `glm-5.2` → `glm-5-2`），否则报错 `The model xxx does not work with your current plan`。 | `qwen3.8-max` |

**各方案 Base URL 映射表**：

| 计费方案 | OpenAI 兼容 Base URL | Anthropic 兼容 Base URL |
|----------|----------------------|---------------------------|
| [Token](../concepts/token.md) Plan 个人版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/v1` | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| 按量计费（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic` |

> **注意**：文档 15（更多工具）中明确指出，Token Plan 个人版/团队版和 Coding Plan **仅限 AI 编程工具和 OpenClaw 类 Agent 使用**，禁止用于 Dify、n8n、Postman 等工作流/自动化平台或 API 测试工具，否则可能被封禁 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。

## 使用方式

1. **安装工具**：根据工具文档安装依赖（Node.js ≥18.0 或 Python 3.10–3.13），执行全局安装命令（如 `npm install -g qwen-code` 或 `curl ... \| bash`）。
2. **配置凭证**：
   - CLI 工具（Claude Code、Hermes Agent、Kilo CLI）：写入 JSON/YAML 配置文件（如 `~/.claude/settings.json` 或 `~/.hermes/config.yaml`）；
   - 桌面/IDE 工具（Cursor、Cherry Studio、Cline）：在图形界面设置中填入 API Key、Base URL 和 Model ID；
   - Agent 平台（OpenClaw、QwenPaw）：通过 `/auth` 命令或 Web Console 可视化配置。
3. **验证连接**：运行简单指令（如 `claude "你好"` 或在 Cursor 中发送“你好”），确认返回非空响应；若失败，检查 `ANTHROPIC_BASE_URL`（Claude Code）或 `OPENAI_API_KEY`（Codex）等环境变量是否生效 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)。

## 限制和注意事项

- **地域一致性**：按量计费的 `API Key`、`WorkspaceId` 和 `Base URL` 必须同属一个地域（如北京地域 Key 不可用于新加坡 URL），否则返回 `401 Incorrect API key provided`。
- **免费额度限制**：新人免费额度**仅适用于华北2（北京）地域的模型**，使用其他地域会产生费用 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **模型能力差异**：`qwen3.8-max` 支持 `reasoning: true` 和 `contextWindow: 983616`，而 `qwen3.6-flash` 仅支持 `maxTokens: 32768`；调用时需确保 `max_tokens` 参数不超过模型上限，否则触发 `400 InternalError.Algo.InvalidParameter`。
- **协议选择**：启用思考模式（R1 messages）时，Cline、Qwen Code 等工具需显式勾选 `Enable R1 messages format`；若未启用，`qwen3.*` 模型将拒绝请求。
- **Dify 特殊限制**：Dify 属于工作流平台，**禁止使用 Token Plan/Coding Plan Key**，必须使用按量计费 Key，且需通过 OpenAI 兼容插件或 HTTP 节点调用 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/cline-tool.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)


