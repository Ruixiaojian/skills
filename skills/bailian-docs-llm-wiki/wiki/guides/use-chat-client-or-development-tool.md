# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程客户端、桌面 IDE、命令行工具及开发平台接入模型服务。开发者可根据使用场景（终端编程、IDE 集成、低代码工作流等）选择兼容 OpenAI 或 Anthropic 协议的客户端，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan、按量计费）配置对应凭证。所有工具均需正确匹配 API Key、Base URL 和模型 ID，否则将触发 401 或 400 错误。

## 支持的模型/功能

百炼当前支持的主流模型包括 `qwen3.8-max`（支持思考模式与[多模态](../concepts/multimodal.md)输入）、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2`、`deepseek-v4-pro`、`deepseek-v4-flash-0731` 等，具体覆盖范围依所选计费方案而异：

- **[Token](../concepts/token.md) Plan 个人版/团队版**：仅限文本生成类模型（如 `qwen3.8-max`, `glm-5.2`），不支持万相（文生图/视频）、Qwen-VL、QVQ、Qwen-Omni 等[多模态](../concepts/multimodal.md)或专用模型 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)；
- **Coding Plan**：支持 `qwen3.7-plus` 等 Coding Plan 专属模型，但不支持 `qwen3.8-max`（该模型未在 [Coding Plan 支持的模型](https://help.aliyun.com/zh/model-studio/coding-plan) 列表中）；
- **按量计费**：覆盖最全，支持文生图（`wan2.6-t2i`）、文生视频、Qwen-VL、QVQ、Qwen-Omni、万相等全部 AIGC 模型，且可通过 [Postman 或 cURL 调用图像/视频生成 API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 实现异步任务管理。

> **注意**：文档 1 中 OpenClaw 配置示例列出了 `qwen3.8-max` 的 `compat.thinkingFormat: "openai"`，但文档 12（Qwen Code）和文档 15（Kilo CLI）明确要求对 `qwen3.8-max` 启用 `enable_thinking: true`；而文档 16 的“更多工具”表格中未声明思考模式支持，存在隐含矛盾。实际调用时，**必须显式启用 `enable_thinking` 才能激活 `qwen3.8-max` 的完整推理能力**，否则将降级为普通响应。

## 关键参数

所有客户端均依赖以下三类核心参数，且必须严格匹配：

| 参数类型 | 说明 | 示例值 |
|----------|------|--------|
| **API Key** | 方案专属密钥，不可跨方案复用 | [Token](../concepts/token.md) Plan 个人版：`sk-xxx`（见 [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)）；按量计费：需与 Workspace ID 所在地域一致 |
| **Base URL** | 决定协议兼容性与模型可用性 | OpenAI 兼容：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| **Model ID** | 必须与套餐支持列表完全一致，部分工具需转义（如 `kimi-k2.6` → `kimi-k2-6`） | `qwen3.8-max`, `glm-5.2`, `wan2.6-t2i`（仅按量计费） |

此外，部分工具需额外配置：
- `CLAUDE_CODE_MAX_CONTEXT_TOKENS`（Claude Code，文档 3）用于扩展上下文窗口至 1M；
- `extra_body.enable_thinking: true`（Qwen Code，文档 12）为 Qwen3 思考模式必需；
- `X-DashScope-Async: enable`（Postman/cURL，文档 14）为图像/视频 API 异步调用必需头。

## 使用方式

### 客户端接入流程（通用）
1. **安装工具**：根据操作系统执行对应安装命令（如 `npm install -g opencode-ai`、`curl -fsSL https://qoder.com/install \| bash`）；
2. **配置凭证**：通过 CLI 命令（`hermes config set`）、配置文件（`~/.qwen/settings.json`）、GUI 设置（Cursor、Cherry Studio）或交互式向导（Qwen Code `/auth`）写入参数；
3. **验证连接**：发送测试请求（如 `claude "你好"` 或对话框输入“你好”），确认返回非空响应。

### 特殊场景
- **IDE 插件集成**：Cline（VSCode）、Qoder（JetBrains）、Claude Code（VSCode/JetBrains）均需在插件设置中启用 `Enable R1 messages format` 以支持 Qwen3 思考模式 [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)；
- **Dify 工作流**：因 Dify 属于工作流平台，**禁止使用 Token Plan/Coding Plan 套餐**，仅允许按量计费 API Key；视觉模型（Qwen-VL/QVQ）需在 LLM 节点开启“视觉”开关，并通过正则提取 `\`\`\`` 包裹的思考内容 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)；
- **图像/视频生成**：必须采用两步式异步调用（创建任务 → 轮询 task_id），不可直接同步请求 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

## 限制和注意事项

- **套餐适用范围严格受限**：Token Plan 个人版、Token Plan 团队版、Coding Plan **仅限 AI 编程工具（如 Hermes Agent、Qwen Code）和 OpenClaw 类 Agent 使用**；Dify、n8n、Coze、Postman、自定义后端脚本等均被明确禁止，违规将导致订阅暂停或 API Key 封禁 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)；
- **地域强绑定**：按量计费的 API Key 与 Workspace ID 必须同地域（如北京 Key + 北京 WorkspaceId），跨地域（如北京 Key + 新加坡 URL）将返回 401；
- **模型命名差异**：Cursor、Cherry Studio 等工具要求模型 ID 使用连字符替代点号（`kimi-k2.6` → `kimi-k2-6`），而 CLI 工具（Hermes、Claude Code）接受原名，配置时需按客户端文档调整；
- **免费额度限制**：按量计费新人免费额度**仅适用于华北2（北京）地域**，且各模型额度独立计算，控制台数据每小时更新，可能存在延迟 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)；
- **认证失败排查**：若报错 `401 Incorrect API key provided`，需逐项核对：① Key 与 Base URL 是否属同一方案；② 按量计费 Key 与 URL 地域是否一致；③ Key 是否复制完整（无空格/换行） [Qoder CN](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)


