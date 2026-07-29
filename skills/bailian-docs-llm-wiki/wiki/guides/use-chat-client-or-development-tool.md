# use chat client or development tool

阿里云百炼平台支持通过多种第三方 Chat 客户端与开发工具接入其模型服务，涵盖 OpenAI / Anthropic 兼容协议的 CLI 工具、桌面 IDE、VS Code 插件及 Web 应用。开发者可根据使用场景（本地调试、团队协作、IDE 集成）选择合适工具，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan、按量计费）配置对应 API Key 与 Base URL。所有工具均需严格匹配套餐类型与地域，否则将触发 401 或 400 错误。

## 支持的模型与功能

- **通用文本生成模型**：`qwen3.8-max-preview`（强制开启思考模式）、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro` 等，均支持 `text` 输入；部分模型（如 `qwen3.7-plus`、`qwen3.6-flash`）额外支持 `image` 输入 [OpenClaw (raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)。
- **思考模式（Thinking Mode）**：`qwen3.8-max-preview` 强制启用，不可关闭；`temperature` 在思考模式下最低为 `0.6`，低于该值将自动截断；`reasoning_effort` 可设为 `xhigh`（默认）、`medium` 或 `low`，控制推理深度 [Claude Code (raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)。
- **多模态能力**：Qwen-VL、QVQ、Qwen-Omni、Qwen-Audio、Qwen-OCR 等视觉/音频/OCR 模型**不支持直接在 Dify 插件中配置**，需通过 HTTP 节点或 cURL 调用专用 AIGC API [Dify (raw/model-user-guide/use-chat-client-or-development-tool/dify.md)](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。
- **图像/视频生成**：`wan2.6-t2i`、`wan2.5-t2i-preview` 等模型仅支持异步调用（创建任务 + 轮询查询），不兼容同步 Chat 接口，须使用 Postman/cURL 或自定义 SDK 实现 [使用Postman或cURL调用图像/视频生成API (raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

> **注意**：文档 15 明确指出 [Token](../concepts/token.md) Plan 个人版、[Token](../concepts/token.md) Plan 团队版和 Coding Plan **不支持工作流平台（如 Dify、n8n、Coze）、API 测试工具（Postman/cURL 仅限测试，非生产）及自定义应用后端调用**；违规使用可能导致订阅暂停或 API Key 封禁。而文档 17 进一步确认 Dify 必须使用按量计费 API Key，与前述限制一致。

## 关键参数

| 参数 | 说明 | 示例值 | 注意事项 |
|------|------|--------|----------|
| `API Key` | 各计费方案专属密钥，**不可跨方案混用** | `sk-xxx`（Token Plan 个人版） | Token Plan 团队版、Coding Plan、按量计费的 Key 互不通用；子账号需确保业务空间模型调用权限 [QwenPaw (raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md) |
| `Base URL` | 决定协议兼容性与地域 | OpenAI 兼容：<br>`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic 兼容：<br>`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | OpenAI 兼容路径为 `/compatible-mode/v1`，Anthropic 兼容路径为 `/apps/anthropic`；按量计费需替换 `{WorkspaceId}` 并匹配 API Key 所在地域 |
| `Model ID` | 模型标识符，**部分工具要求别名** | `qwen3.8-max-preview`，但 Cursor 中 `glm-5.2` 需写为 `glm-5-2` | Cursor、Chatbox 等工具对含小数点的模型名（如 `kimi-k2.6`）需转为连字符格式（`kimi-k2-6`）；Qoder CN 不支持万相等 AIGC 模型 [Qoder CN（原 Lingma） (raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) |
| `thinking` / `enable_thinking` | 思考模式开关 | `true`（Qwen3 系列必需） | `qwen3.8-max-preview` 强制启用；OpenCode、Qwen Code、Kilo CLI 等需在 `extra_body` 或 `options.thinking` 中显式声明；未启用将报错 `The value of the enable_thinking parameter is restricted to True` |

## 使用方式

### 1. 安装与初始化
- **CLI 工具**（如 `openclaw`、`claude-code`、`hermes`、`opencode`）：依赖 Node.js ≥18（`claude-code`、`opencode`）或 ≥22（`openclaw`），通过 `npm install -g` 或一键脚本安装。
- **桌面应用**（如 `Cursor`、`Cherry Studio`、`Qoder IDE`）：从官网下载安装包，启动后通过图形界面配置。
- **IDE 插件**（如 `Cline`（VS Code）、`Qoder JetBrains 插件`）：在扩展市场安装，配置入口位于侧边栏或设置面板。
- **Web 应用**（如 `Chatbox`、`QwenPaw Console`）：访问网页或运行本地服务（`qwenpaw app` 监听 `http://127.0.0.1:8088/`）。

### 2. 配置凭证（统一逻辑）
所有工具均需三要素：**API Key + Base URL + Model ID**，按计费方案选择对应组合：
- **Token Plan 个人版/团队版**：Base URL 统一为 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（OpenAI）或 `/apps/anthropic`（Anthropic），Key 从对应控制台获取。
- **Coding Plan**：Base URL 为 `https://coding.dashscope.aliyuncs.com/v1`（OpenAI）或 `/apps/anthropic`（Anthropic）。
- **按量计费**：Base URL 含 `{WorkspaceId}` 占位符，必须与 API Key 所属地域及业务空间一致（华北2、新加坡、美国弗吉尼亚）。

> **注意**：文档 4（OpenCode）与文档 2（Claude Code）对 `qwen3.8-max-preview` 的 `contextWindow` 声称 `983616`，但文档 1（OpenClaw）中同模型字段为 `983616`，文档 13（Kilo CLI）中为 `983616`，数值一致；而文档 5（Codex）元数据中 `context_window` 为 `983616`，亦无矛盾。但文档 6（Qwen Code）配置示例中未声明 `contextWindow`，属信息缺失，实际调用需依赖服务端默认值或客户端自动推导。

### 3. 高级能力启用
- **思考模式**：Qwen3 系列需显式启用（如 Qwen Code 的 `extra_body.enable_thinking: true`，OpenCode 的 `options.thinking.type: "enabled"`）。
- **R1 messages format**：Cline 插件调用 Qwen3 或 QwQ 模型时，必须勾选 `Enable R1 messages format`，否则报错 `400 InternalError.Algo.InvalidParameter`。
- **自定义技能**：Cursor、Cline、Qoder 等支持通过百炼 CLI 注册 Skills（如 `bailian-cli`），需先全局安装 CLI 并配置 API Key。

## 限制和注意事项

- **地域强绑定**：按量计费的 API Key 与 `WorkspaceId` 必须同地域（如北京 Key 只能配北京 URL）；Token Plan/Coding Plan 的 Base URL 固定，无需替换 `WorkspaceId`，但 Key 仍需对应方案。
- **免费额度限制**：新人免费额度**仅适用于华北2（北京）地域**的模型，且各模型额度独立计算、每小时更新延迟 [Cherry Studio (raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **模型兼容性限制**：
  - Cursor 免费版仅支持 Auto 模式，**无法调用自定义模型**，必须升级至 Pro 版本。
  - Qoder CN 企业版**不支持接入百炼**，仅限个人社区版/专业版。
  - Dify 等工作流平台**禁止使用 Token Plan/Coding Plan Key**，违者可能被封禁。
- **错误排查优先级**：
  1. 检查 `API Key` 与 `Base URL` 是否来自同一计费方案及地域；
  2. 核对 `Model ID` 是否为当前套餐支持列表中的模型（参考各文档链接的“支持的模型”）；
  3. 确认思考模式是否按要求启用（尤其 `qwen3.8-max-preview`）；
  4. 查阅对应方案的[错误码文档](https://help.aliyun.com/zh/model-studio/error-code)定位 HTTP 状态码。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)


