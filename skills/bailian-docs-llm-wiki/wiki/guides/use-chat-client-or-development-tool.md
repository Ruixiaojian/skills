# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端和开发平台接入模型服务，涵盖 OpenAI 兼容协议与 Anthropic 兼容协议。开发者可根据使用场景（如终端 CLI、IDE 插件、Web 应用或工作流平台）选择适配的客户端，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan 或按量计费）配置对应凭证。所有工具均需正确匹配 API Key、Base URL 和模型 ID，否则将触发 401 或 400 错误。

## 支持的模型/功能

- **通用文本生成模型**：`qwen3.8-max-preview`（强制开启思考模式）、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro` 等，均支持 `text` 输入；部分支持 `image` 输入（如 `qwen3.7-plus`、`qwen3.6-flash`），详见各工具文档中的 `input` 字段声明。
- **思考模式（Thinking Mode）**：`qwen3.8-max-preview` 始终启用，不可关闭；`temperature` 小于 0.6 时自动修正为 0.6；`reasoning_effort` 可设为 `xhigh`/`medium`/`low`（[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) 中明确说明该行为）。
- **[多模态](../concepts/multi-modal.md)能力**：Qwen-VL、QVQ、万相（文生图/视频）等模型**不支持直接在 Dify 插件中配置**，需通过 HTTP 节点调用异步 API（[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 明确指出此限制）。
- **图像/视频生成**：仅支持通过 Postman/cURL 等工具调用异步 API（如 `wan2.6-t2i`），不适用于 Chat Client 类工具（[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 定义了该调用范式）。

> **注意**：Dify 属于工作流平台，**明确不支持** [Token](../concepts/token.md) Plan 个人版、[Token](../concepts/token.md) Plan 团队版和 Coding Plan 接入，仅允许使用按量计费 API Key；违规使用将导致订阅暂停或 Key 封禁（[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 强调此策略）。

## 关键参数

| 参数 | 含义 | 示例值 | 注意事项 |
|------|------|--------|----------|
| `API Key` | 计费方案专属密钥 | `sk-xxx`（Token Plan 个人版） | **不可跨方案复用**：Token Plan 个人版 Key 不能用于 Coding Plan 或按量计费（[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md) 指出“提供商或类型与实际套餐不一致”是常见报错原因） |
| `Base URL` | 服务端点地址 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（OpenAI 协议）<br>`https://coding.dashscope.aliyuncs.com/apps/anthropic`（Anthropic 协议） | 地域必须匹配：按量计费的 `WorkspaceId` 需与 API Key 所属地域一致；Token Plan 团队版与个人版共用同一 Base URL，但 Key 不互通 |
| `Model ID` | 模型标识符 | `qwen3.8-max-preview` | 部分工具（如 Cursor、Chatbox）要求模型名格式转换：`kimi-k2.6` → `kimi-k2-6`，`glm-5.2` → `glm-5-2`（见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)） |
| `enable_thinking` / `thinking` | 思考模式开关 | `true`（Qwen Code）<br>`{"type": "enabled"}`（Kilo CLI） | `qwen3.8-max-preview` 必须显式启用；未设置将报错 `"The value of the enable_thinking parameter is restricted to True"`（见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)） |

## 使用方式

1. **安装客户端**  
   - CLI 工具（如 `hermes`、`qwen`、`kilo`）：依赖 Node.js ≥18，通过 `npm install -g` 安装。  
   - 桌面应用（如 `Cursor`、`Cherry Studio`、`Qoder CN`）：从官网下载安装包。  
   - IDE 插件（如 `Cline`、`Qoder` JetBrains 插件）：在 VS Code 或 JetBrains 扩展市场安装。

2. **配置凭证**  
   - **统一原则**：Key + Base URL + Model ID 三者必须同属一个计费方案且地域一致。  
   - **配置路径示例**：  
     - OpenClaw：`~/.openclaw/openclaw.json`  
     - Hermes Agent：`~/.hermes/config.yaml`  
     - Qwen Code：`~/.qwen/settings.json`  
     - Dify：通过插件 UI 设置（仅限按量计费 Key）  

3. **验证与调试**  
   - 发送简单请求（如 `"你好"`）确认响应正常。  
   - 报错时优先检查：  
     - `401 Incorrect API key provided` → Key 与 Base URL 方案/地域不匹配；  
     - `400 InternalError.Algo.InvalidParameter` → 未启用 `Enable R1 messages format`（Cline）或 `enable_thinking`（Qwen Code）；  
     - 模型不可用 → 检查所选模型是否在当前套餐支持列表内（如 Token Plan 团队版不支持 `wan2.6-t2i`）。

## 限制和注意事项

- **计费方案适用范围严格隔离**：  
  Token Plan 个人版/团队版、Coding Plan **仅限 AI 编程工具（Hermes、Claude Code、Qwen Code 等）和 OpenClaw 类 Agent（QwenPaw、OpenClaw）使用**；工作流平台（Dify、n8n）、API 测试工具（Postman）、自定义后端代码**禁止接入**（[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 明确列出不支持类型并警告封禁风险）。

- **地域与免费额度绑定**：  
  按量计费的新人免费额度**仅限华北2（北京）地域**；使用新加坡或美国端点将产生费用（[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md) 提示此细节）。

- **模型兼容性差异**：  
  - `qwen3.8-max-preview` 等思考模型需显式启用 `thinking`，且 `temperature` 下限为 0.6；  
  - `glm-5` 系列模型在 Codex 中需降级至 v0.80.0 并使用 `chat` API（而非 `responses`），否则报错（见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)）；  
  - Cursor 免费版仅支持 `Auto` 模式，调用自定义模型需升级至 Pro 版本（[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) 明确说明）。

- **异步任务特殊处理**：  
  图像/视频生成（如万相）必须采用两步式异步调用（创建任务 → 轮询查询），**不支持同步阻塞调用**；结果 URL 有效期为 24 小时（[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 定义该机制）。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


