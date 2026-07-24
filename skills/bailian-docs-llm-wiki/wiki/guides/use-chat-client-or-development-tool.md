# use chat client or development tool

阿里云百炼支持通过多种开源或商业 AI 开发工具接入模型服务，包括终端编程助手（如 Hermes Agent、Claude Code）、桌面 IDE（如 Cursor、Qoder）、Agent 框架（如 OpenClaw、QwenPaw）及低代码平台（如 Dify）。所有工具均通过 OpenAI 或 Anthropic 兼容协议对接，开发者可基于自身技术栈和使用场景选择合适客户端，无需修改业务逻辑即可切换模型与计费方案。

## 支持的模型/功能

百炼支持的模型因计费方案而异，**[Token](../concepts/token.md) Plan 个人版**和**[Token](../concepts/token.md) Plan 团队版**均支持 `qwen3.8-max-preview`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro` 等文本生成模型；**Coding Plan** 主要覆盖 `qwen3.7-plus` 等高性价比编码模型；**按量计费**支持最全模型集，包括文生图（`wan2.6-t2i`）、文生视频（`wan2.2-t2v`）等 AIGC 模型。  
视觉与多模态能力需显式启用：`qwen3.7-plus`、`qwen3.6-flash` 等模型支持 `text` + `image` 输入（见 [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md) 配置示例），而 Qwen-VL、QVQ 等专用视觉模型需通过 Dify 的 LLM 节点视觉开关或 HTTP 节点调用（参见 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 文档）。  
> **注意**：部分工具（如 Cursor 免费版）仅支持 Auto 模式，不支持自定义模型调用；Qoder CN 企业版明确不支持百炼接入（[Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)）。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` | API 端点地址，**必须与计费方案和地域严格匹配** | [Token](../concepts/token.md) Plan 个人版 OpenAI 协议：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Anthropic 协议：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| `api_key` | 方案专属密钥，**不可跨方案复用** | Token Plan 个人版 API Key 仅可用于对应 Base URL，混用将返回 401 错误（[QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md) 常见问题） |
| `model_id` | 模型标识符，部分工具要求别名转换（如 `kimi-k2.6` → `kimi-k2-6`） | `qwen3.8-max-preview`（思考模式强制开启） |
| `thinking` / `reasoning_effort` | `qwen3.8-max-preview` 等模型的推理控制参数，`temperature < 0.6` 时自动修正为 0.6，`reasoning_effort` 可设 `xhigh`/`high`/`low` | `{"thinking": true, "reasoning_effort": "xhigh"}` |

## 使用方式

1. **安装工具**：根据工具文档安装 CLI（如 `npm install -g hermes-agent`）、桌面应用（Cursor、Cherry Studio）或插件（VS Code 的 Cline、JetBrains 的 Qoder）；  
2. **配置凭证**：  
   - 终端工具（Hermes Agent、Claude Code）通过命令行或 YAML/JSON 配置文件设置 `base_url`、`api_key` 和 `model_id`；  
   - GUI 工具（Cursor、Chatbox）在设置界面填写 API Key、Base URL 并选择模型；  
   - Agent 框架（OpenClaw、QwenPaw）通过交互式向导或 Web Console 配置提供商；  
3. **验证连接**：发送简单请求（如 `"你好"`）确认响应正常；  
4. **高级用法**：  
   - 图像/视频生成需异步调用（创建任务 → 轮询 `task_id` 获取结果），详见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)；  
   - Dify 等低代码平台需安装通义千问插件并配置 API Key，视觉模型需开启 LLM 节点的“视觉”开关。

## 限制和注意事项

- **协议兼容性**：OpenAI 协议端点（`/compatible-mode/v1`）适用于绝大多数工具（Cursor、Cherry Studio、Qwen Code），Anthropic 协议端点（`/apps/anthropic`）需工具显式支持（如 Hermes Agent、Claude Code）；  
- **地域绑定**：API Key 与 Base URL 必须同地域（如北京地域 Key 不可配新加坡 Base URL），否则报错 401（[QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md) 和 [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md) 均强调此限制）；  
- **套餐适用范围**：Token Plan 个人版/团队版、Coding Plan **禁止用于工作流平台（Dify、n8n）、API 测试工具（Postman）或自定义后端应用**，违规可能导致订阅暂停（[更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 明确声明）；  
- **免费额度限制**：按量计费新用户免费额度**仅限华北2（北京）地域**，其他地域调用将产生费用（[Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md) 常见问题）；  
- **模型能力差异**：`qwen3.8-max-preview` 思考模式不可关闭且 `temperature` 下限为 0.6，而 `qwen3.7-max` 等模型默认不启用思考（需显式传参 `enable_thinking: true`）。

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
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


