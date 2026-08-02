# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务。开发者可根据使用场景选择 CLI 工具（如 Hermes Agent、Claude Code）、桌面应用（如 Cursor、Cherry Studio）、IDE 插件（如 Cline、Qoder）或低代码平台（如 Dify），并按计费方案（Token Plan 个人版/团队版、Coding Plan、按量计费）配置对应凭证。所有工具均基于 OpenAI 或 Anthropic 兼容协议，无需修改业务逻辑即可快速对接。

## 支持的模型/功能

- **通用文本生成模型**：`qwen3.8-max-preview`（预览期）、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro`、`deepseek-v4-flash-0731` 等，覆盖长上下文（最高 983,616 tokens）、多模态（text + image）及推理增强能力。
- **思考模式（Thinking Mode）**：`qwen3.8-max-preview` 强制启用思考链，支持 `reasoning_effort`（xhigh/medium/low）和 `temperature`（≥0.6）参数调节；其他模型如 `qwen3.7-plus` 也支持可选开启（需显式传 `enable_thinking: true`）[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)。
- **多模态与专业模型**：Qwen-VL、QVQ、Qwen-Omni、Qwen-Audio、万相（wan2.6-t2i）等需通过 HTTP 节点或专用 API 调用，不直接暴露于多数客户端的模型下拉菜单中 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。
- **图像/视频生成**：需异步调用（创建任务 → 轮询查询），不适用于同步聊天客户端，推荐使用 Postman/cURL 或 Dify 工作流集成 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

> **注意**：`qwen3.8-max-preview` 的思考模式在不同工具中行为一致（始终开启、temperature 下限 0.6），但部分工具（如 Codex）要求额外配置 `model-catalog.local.json` 定义 `default_reasoning_level` 和 `supported_reasoning_levels`，而 OpenClaw、Hermes Agent 等则直接通过 `reasoning: true` 或 `thinking: enabled` 控制 —— 实际效果相同，仅配置方式差异。

## 关键参数

| 参数 | 说明 | 示例值 | 注意事项 |
|------|------|--------|----------|
| `base_url` | 服务端点，协议决定兼容性 | OpenAI: `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic: `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | Token Plan/Coding Plan 的 Base URL 固定；按量计费需替换 `{WorkspaceId}` 并匹配地域 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) |
| `api_key` | 方案专属密钥，不可跨方案复用 | `sk-xxx`（Token Plan 个人版） | 报错 `401 Incorrect API key provided` 多因 Key 与 Base URL 方案/地域不匹配 |
| `model_id` | 模型标识符，命名需严格一致 | `qwen3.8-max-preview`、`glm-5-2`（Cursor 中需转义小数点） | Cursor、Chatbox 等工具要求模型名格式化（如 `kimi-k2.6` → `kimi-k2-6`）[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) |
| `enable_thinking` / `thinking` | 启用思考链（R1 messages format） | `true`（Qwen Code）、`{"type": "enabled"}`（OpenCode） | Cline、Dify 等需手动勾选 `Enable R1 messages format` 才能正确解析思考内容 |

## 使用方式

1. **安装工具**  
   - CLI 工具（Hermes Agent、Claude Code、Qwen Code）：依赖 Node.js ≥18，通过 `npm install -g` 或一键脚本安装。  
   - 桌面应用（Cursor、Cherry Studio）：从官网下载安装包。  
   - IDE 插件（Cline、Qoder JetBrains 插件）：在 VS Code 或 JetBrains 扩展市场搜索安装。

2. **配置凭证**  
   - **CLI 工具**：编辑配置文件（如 `~/.hermes/config.yaml`、`~/.claude/settings.json`）或执行 `hermes config set` 命令。  
   - **GUI 工具**：在设置界面填写 API Key、Base URL、Model ID（如 Cursor 的 *Models* 设置页、Cherry Studio 的 *添加模型* 对话框）。  
   - **Dify 等平台**：安装「通义千问」插件后，在模型供应商设置中填入 API Key，并确保地域端点匹配 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

3. **验证与调试**  
   - 发送简单请求（如 `"你好"`）确认基础连通性。  
   - 遇到 `400 InternalError.Algo.InvalidParameter`：检查是否启用 R1 格式（Cline/Dify）或 `extra_body.enable_thinking`（Qwen Code）。  
   - 长对话超限：调整 `max_tokens` 或在提供商高级配置中设置 JSON 参数（QwenPaw）[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)。

## 限制和注意事项

- **套餐适用范围严格隔离**：Token Plan 个人版/团队版、Coding Plan 仅允许用于 AI 编程工具（Hermes、Claude Code、OpenClaw 等）和 OpenClaw 类 Agent；**禁止用于 Dify、n8n、Postman 等工作流/自动化平台或自定义应用**，否则可能导致订阅暂停或 API Key 封禁 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。
- **地域与免费额度绑定**：新人免费额度仅适用于华北2（北京）地域的按量计费模型；使用新加坡或美国端点将不享受免费额度 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **模型兼容性差异**：  
  - `qwen3.8-max-preview` 在 Anthropic 协议下必须启用 thinking，且 temperature < 0.6 会被自动修正；  
  - Codex 对 `qwen3.8-max-preview` 需用 Responses API，而 `glm-5` 等旧模型需降级至 v0.80.0 并改用 Chat API；  
  - Cursor 免费版仅支持 Auto 模式，调用自定义模型需升级至 Pro 版本。
- **图像/视频生成不支持同步交互**：必须采用异步轮询机制，无法在聊天客户端中直接返回结果，需通过 Dify 工作流或 cURL 脚本集成 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)


