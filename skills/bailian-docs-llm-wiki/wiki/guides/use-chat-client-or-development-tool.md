# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发框架接入模型服务，覆盖 OpenAI 和 Anthropic 两种兼容协议。开发者可根据使用场景（终端 CLI、IDE 插件、桌面应用或自定义开发）选择合适工具，并按计费方案（Token Plan 个人版/团队版、Coding Plan 或按量计费）配置对应 API Key 与 Base URL。所有工具均需严格匹配套餐类型与地域，否则将触发 401 错误或额度失效。

## 支持的模型/功能

- **通用文本生成模型**：`qwen3.8-max-preview`（思考模式强制开启）、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro`、`deepseek-v4-flash-0731` 等，详见 [Token Plan 个人版支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview)。
- **多模态能力**：`qwen3.7-plus`、`qwen3.6-flash` 等支持图像输入；`qwen-vl`、`qwen-ocr`、`qwen-audio`、`qwen-omni` 需通过 HTTP 节点调用（如 Dify 工作流），不支持直接在模型下拉菜单中选择 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。
- **图像/视频生成**：`wan2.6-t2i`、`wan2.5-t2i-preview` 等 AIGC 模型仅支持异步调用，需通过 `task_id` 轮询获取结果，详见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。
- **思考模式（Reasoning）**：`qwen3.8-max-preview` 始终启用 `thinking`，`temperature` < 0.6 时自动修正为 0.6，`reasoning_effort` 可设为 `xhigh`/`medium`/`low`；其他 Qwen3 模型默认启用但可关闭（部分工具如 Codex 需显式配置 `enable_thinking: true`）。

> **注意**：文档中 `qwen3.8-max-preview` 的 `contextWindow` 存在不一致描述——[OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md) 标注为 `983616`，而 [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md) 和 [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md) 均标注为 `983616`，但 [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md) 未提供该值。以官方模型文档为准，实际调用应以 API 返回的 `context_window` 字段为准。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `Base URL` | 必须与计费方案和协议严格匹配 | OpenAI 协议：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Anthropic 协议：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| `API Key` | 方案专属，不可跨方案复用 | Token Plan 个人版 Key 无法用于 Coding Plan 或按量计费 |
| `WorkspaceId` | 按量计费必需，需从控制台获取并替换 URL 中占位符 | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `model` | 模型 ID 必须存在于对应套餐的支持列表中，且名称格式需适配工具要求（如 Cursor 要求 `kimi-k2.6` → `kimi-k2-6`） | `qwen3.8-max-preview` |
| `enable_thinking` / `thinking` | Qwen3 思考模式开关，部分工具（如 Qwen Code、Cline）需显式启用 | `"extra_body": {"enable_thinking": true}`（Qwen Code）；`"thinking": {"type": "enabled"}`（Kilo CLI） |

## 使用方式

1. **安装工具**  
   - CLI 工具（Hermes Agent、Claude Code、Qwen Code、Kilo CLI 等）：依赖 Node.js ≥18（部分如 OpenClaw 要求 ≥22.19.0）或 Python ≥3.10（QwenPaw）。  
   - IDE 插件（Cline、Qoder JetBrains 插件）：直接从 VS Code 或 JetBrains Marketplace 安装。  
   - 桌面应用（Cursor、Cherry Studio、Chatbox）：从官网下载安装包。

2. **配置凭证**  
   - **统一原则**：API Key 与 Base URL 必须同属一个计费方案与地域。  
   - **配置路径示例**：  
     - Hermes Agent：`~/.hermes/config.yaml`  
     - OpenCode：`~/.config/opencode/opencode.json`  
     - QwenPaw：Web Console → 设置 → 模型 → 对应提供商设置页  
     - Postman/cURL：手动填入 Headers（`Authorization: Bearer <key>`）与 Body（JSON payload）  

3. **验证与调试**  
   - 发送简单请求（如 `"你好"`）确认基础连通性。  
   - 遇到 `401 Incorrect API key provided`，优先检查 Key/URL 方案一致性及地域匹配（[QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md) 明确指出此为常见原因）。  
   - 图像/视频生成必须实现两步调用（创建任务 + 轮询 `task_id`），不可同步等待响应。

## 限制和注意事项

- **套餐适用范围严格受限**：Token Plan 个人版、Token Plan 团队版、Coding Plan **仅允许用于 AI 编程工具（如 Hermes、Qwen Code）和 OpenClaw 类 Agent**，禁止用于工作流平台（Dify、n8n、Coze）、API 测试工具（Postman、Insomnia）或自定义后端应用。违规使用将导致订阅暂停或 Key 封禁 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。
- **地域与免费额度绑定**：按量计费的新人免费额度**仅限华北2（北京）地域**，使用新加坡或美国端点将立即计费 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **模型命名兼容性**：Cursor、Cherry Studio 等工具要求模型 ID 使用连字符替代点号（如 `kimi-k2.6` → `kimi-k2-6`），否则报错 `The model xxx does not work with your current plan`。
- **思考模式强制约束**：`qwen3.8-max-preview` 在所有工具中均不支持关闭 `thinking`，传入 `temperature: 0.3` 将被服务端自动修正为 `0.6`，开发者无需在请求中重复指定。
- **Dify 特殊限制**：Dify 属于工作流平台，**明确不支持 Token Plan/Coding Plan**，必须使用按量计费 API Key；视觉模型（Qwen-VL、QVQ）需在 LLM 节点启用“视觉”开关，并注意输出中思考内容被 ```` 包裹，需正则提取 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)


