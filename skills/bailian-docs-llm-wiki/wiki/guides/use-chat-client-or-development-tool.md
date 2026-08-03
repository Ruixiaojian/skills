# use chat client or development tool

阿里云百炼支持多种主流 AI 编程工具、桌面客户端及开发平台接入，开发者可通过 [Token](../concepts/token.md) Plan 个人版、[Token](../concepts/token.md) Plan 团队版、Coding Plan 或按量计费四种方案调用百炼模型。所有工具均基于 OpenAI 或 Anthropic 兼容协议，无需修改业务代码即可快速集成。配置核心为三要素：API Key、Base URL 和模型 ID，且各套餐凭证严格隔离，不可混用。

## 支持的模型/功能

百炼提供统一的模型能力矩阵，但不同接入方案支持的模型范围存在差异：

- **[Token](../concepts/token.md) Plan 个人版/团队版**：支持 `qwen3.8-max`、`qwen3.8-max-preview`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro` 等文本生成模型；`qwen3.8-max-preview` 强制启用思考模式（thinking），不支持关闭，且 `temperature < 0.6` 时自动修正为 `0.6` [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)。部分工具（如 Cursor）要求模型名转义，例如 `glm-5.2` → `glm-5-2` [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)。

- **Coding Plan**：主要支持 `qwen3.7-plus` 等高性价比编码模型，不支持 `qwen3.8-max-preview` 等预览模型 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)。

- **按量计费**：覆盖最全模型集，包括视觉（Qwen-VL）、音频（Qwen-Audio）、OCR（Qwen-OCR）、多模态（Qwen-Omni）及万相（wan2.6-t2i）等 AIGC 模型，但需通过 HTTP 节点或专用 API 调用，不支持直接在 Dify 插件中配置 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

> **注意**：Dify 明确不支持 Token Plan 个人版、Token Plan 团队版和 Coding Plan 接入，仅允许使用按量计费 API Key；违规使用将导致订阅暂停或 Key 封禁 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `API Key` | 各方案专属密钥，不可跨方案复用 | `sk-xxxxxxxxxxxxx`（Token Plan 个人版） |
| `Base URL` | 协议与地域强绑定：<br>- OpenAI 兼容：`/compatible-mode/v1`<br>- Anthropic 兼容：`/apps/anthropic`<br>- 地域需与 API Key 一致 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `Model ID` | 必须与所选方案支持列表完全匹配，大小写敏感 | `qwen3.8-max-preview`（Token Plan）<br>`qwen3.7-plus`（Coding Plan） |
| `thinking` / `enable_thinking` | Qwen3 系列思考模式开关，部分工具（如 Cherry Studio）强制开启时需显式设置为 `true` | `"thinking": true`（OpenCode）<br>`"enable_thinking": true`（Qwen Code） |

## 使用方式

### 1. 安装与初始化
- 终端工具（Hermes Agent、Claude Code、Qwen Code 等）依赖 Node.js ≥18.0，推荐通过 npm 全局安装；
- 桌面客户端（Cursor、Cherry Studio、Chatbox）直接下载安装包；
- IDE 插件（Cline、Qoder JetBrains）在对应 IDE 扩展市场搜索安装；
- 开发平台（Dify）通过插件市场安装“通义千问”或“OpenAI-API-compatible”插件。

### 2. 配置凭证
所有工具均需配置三要素，但路径与格式各异：
- **CLI 工具**：编辑 JSON/YAML 配置文件（如 `~/.hermes/config.yaml`、`~/.qwen/settings.json`）；
- **桌面客户端**：通过图形界面设置 > 模型 > 添加，填入 API Key、Base URL、Model ID；
- **Dify**：在“模型供应商”中配置插件，**必须使用按量计费 Key**，并根据地域切换国际端点开关。

### 3. 验证与调试
- 发送简单请求（如 `"你好"`）验证基础连通性；
- 对于长上下文或[工具调用](../concepts/tool-use.md)失败，检查模型 `max_tokens` 限制并在提供商设置中手动调整 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)；
- 报错 `401 Incorrect API key provided` 时，优先核对 Key 与 Base URL 是否来自同一方案及地域。

## 限制和注意事项

- **方案隔离**：Token Plan 个人版、Token Plan 团队版、Coding Plan 的 API Key 与 Base URL 严格绑定，互不通用；按量计费 Key 亦需与 Base URL 地域一致（如北京 Key 不可配新加坡 URL）。
- **模型兼容性**：并非所有模型支持所有协议。例如 `qwen3.8-max-preview` 在 Anthropic 协议下需 `api_mode: anthropic_messages`，而在 OpenAI 协议下需 `extra_body: { "enable_thinking": true }`。
- **不支持场景**：工作流平台（Dify、n8n）、API 测试工具（Postman、cURL）、自定义后端应用**禁止使用 Token Plan/Coding Plan Key**，仅限按量计费 Key [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。
- **免费额度限制**：新人免费额度仅适用于华北2（北京）地域的按量计费模型，跨地域调用（如新加坡）将立即计费 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **思考模式约束**：`qwen3.8-max-preview` 在所有支持工具中均强制开启 thinking，且 temperature 下限为 0.6，此行为已在 Hermes Agent、Claude Code、OpenCode 等多份文档中一致确认。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


