# use chat client or development tool

阿里云百炼平台支持通过多种第三方聊天客户端和开发工具接入 AI 模型。这些工具涵盖终端编程助手、IDE 插件、桌面客户端和 API 测试工具，均可通过 OpenAI 或 Anthropic 兼容 API 协议进行对接。本文汇总了各工具的接入方式、计费方案、关键参数和注意事项。

## 支持的工具概览

根据工具类型，百炼支持以下几类接入：

| 类型 | 工具 | 接入协议 |
|------|------|----------|
| 终端编程助手 | Claude Code、Codex、Qwen Code、Hermes Agent、OpenCode、Kilo CLI | OpenAI / Anthropic |
| IDE 插件/桌面 IDE | Cline（VSCode）、Cursor、Qoder、Qoder CN（原 Lingma） | OpenAI Compatible |
| 桌面聊天客户端 | Cherry Studio、Chatbox | OpenAI Compatible |
| AI Agent 平台 | OpenClaw、Dify | OpenAI / Anthropic |
| API 测试工具 | Postman、cURL | HTTP 直接调用 |

如需接入上述之外的工具，只要兼容 OpenAI 或 Anthropic API 协议且支持自定义服务端点，即可参照 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 中的通用配置进行接入。

## 计费方案与接入凭证

百炼提供三种计费方案，不同方案的 API Key、Base URL 和支持模型各不相同，**凭证不可混用**。

### Token Plan 团队版

按坐席订阅，按 token 消耗抵扣 Credits。

| API 协议 | Base URL |
|----------|----------|
| OpenAI | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Anthropic | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |

- **API Key**：Token Plan 团队版专属 API Key，在[控制台](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview)获取。
- **可用模型**：参见 Token Plan 团队版支持的模型列表。

### Coding Plan

固定月费订阅，按模型调用次数计量。

| API 协议 | Base URL |
|----------|----------|
| OpenAI | `https://coding.dashscope.aliyuncs.com/v1` |
| Anthropic | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |

- **API Key**：Coding Plan 专属 API Key，在[控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)获取。

### 按量计费

按实际调用量后付费，支持多地域。

| API 协议 | 华北2（北京） | 新加坡 | 美国（弗吉尼亚） |
|----------|---------------|--------|-------------------|
| OpenAI | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| Anthropic | `https://dashscope.aliyuncs.com/apps/anthropic` | `https://dashscope-intl.aliyuncs.com/apps/anthropic` | — |

- **API Key**：阿里云百炼 API Key，须与所选地域对应。

> **注意**：免费额度仅适用于中国内地版（北京地域）模型，使用其他地域会产生费用。各模型免费额度独立，不可跨模型共享。

## 各工具配置要点

### 终端编程工具

**Claude Code** 通过环境变量（`ANTHROPIC_AUTH_TOKEN`、`ANTHROPIC_BASE_URL` 等）在 `~/.claude/settings.json` 中配置，详见 [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)。安装前需编辑 `~/.claude.json` 将 `hasCompletedOnboarding` 设为 `true` 以跳过 Anthropic 官方登录验证。还可使用社区工具 CC Switch 实现多套餐一键切换。

**Codex** 通过 `~/.codex/config.toml` 配置文件和 `OPENAI_API_KEY` 环境变量接入。需注意：qwen3.7-max 和 qwen3.6-plus 支持 Responses API（可用最新版 Codex），其他模型需通过 Chat/Completions API 接入，需安装旧版本（如 0.80.0）。Coding Plan 仅支持 Chat/Completions API。

**Hermes Agent** 通过 `hermes config set` 命令或 `~/.hermes/config.yaml` 配置，使用 Anthropic Messages API 协议。注意 `model.provider` 必须设置为 `custom`，否则会默认连接 OpenRouter。详见 [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)。

**Qwen Code** 支持通过 `/auth` 命令进行可视化配置，也可通过 `settings.json` 手动配置。使用 OpenAI 兼容协议。

**OpenCode** 和 **Kilo CLI** 配置方式类似，均通过 JSON 配置文件指定 provider、模型和 thinking 参数。部分模型支持 thinking 模式，需配置 `budgetTokens`。

### IDE 插件

**Cline**（VSCode 插件）选择 OpenAI Compatible 作为 API Provider，填入 Base URL、API Key 和 Model ID。使用 Qwen3 思考模式或 QwQ 模型时，需勾选 **Enable R1 messages format**。

**Cursor** 在 Settings > Models 中开启 OpenAI API Key 和 Override OpenAI Base URL 进行配置。

> **注意**：Cursor 免费版仅支持 Auto 模式，无法调用自定义模型，需升级至 Pro 及以上套餐。部分模型名称与 Cursor 内置模型冲突，需使用别名（如 `kimi-k2.6` 写为 `kimi-k2-6`，`glm-5` 写为 `glm-5-0`）。

**Qoder** 和 **Qoder CN（原 Lingma）** 内置了阿里云百炼供应商选项，可在设置中直接选择。Qoder CN 企业版不支持接入百炼，仅个人社区版和个人专业版支持。

### 桌面客户端

**Cherry Studio** 和 **Chatbox** 均通过 OpenAI 兼容协议接入，在设置中添加供应商、填入 API Key 和 API 地址即可。配置方式参见 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。

### 应用开发平台

**Dify** 通过安装通义千问插件接入百炼模型（包括 DeepSeek 等非千问模型也使用此插件）。支持聊天助手、Agent、Chatflow/工作流、知识库等多种应用类型。万相等图像/视频模型需通过工作流 HTTP 节点接入。

**OpenClaw** 通过 `~/.openclaw/openclaw.json` 配置，使用 Anthropic Messages API 协议。

### API 测试

使用 **Postman** 或 **cURL** 可直接调用百炼 API，适用于快速测试。图像和视频生成 API 采用异步调用机制：先创建任务获取 `task_id`，再轮询查询结果。生产环境建议使用官方 SDK。

## 关键参数说明

| 参数 | 说明 |
|------|------|
| `enable_thinking` / `thinking` | 启用模型思考模式，部分模型（如 Qwen3 系列、Kimi K2 系列、GLM-5 系列）支持 |
| `budgetTokens` | 思考 token 预算，控制推理深度 |
| `wire_api` | Codex 专用，指定 `responses`（Responses API）或 `chat`（Chat/Completions API） |
| `thinkingFormat` | OpenClaw 中指定思考格式，如 `"openai"` |
| 模型别名 | 在 Cursor 等工具中，含 `.` 的模型名需替换为 `-`（如 `glm-5.1` → `glm-5-1`） |

## 限制和注意事项

- **凭证隔离**：Token Plan、Coding Plan 和按量计费的 API Key 不通用，必须与对应的 Base URL 配套使用。
- **套餐使用范围**：Token Plan 团队版和 Coding Plan 仅限在 AI 编程工具和 OpenClaw 类型 Agent 中使用，**不支持**工作流/自动化平台（如 Dify、n8n）、API 测试工具（如 Postman）及自定义应用程序。违规使用可能导致订阅暂停或 API Key 封禁。
- **工具兼容性**：部分工具（如通义灵码个人版、Cursor 免费版、Trae）不支持自定义服务端点，无法直接使用 Token Plan 或 Coding Plan。
- **Codex 版本**：使用 Coding Plan 或不支持 Responses API 的模型时，需安装旧版 Codex（如 0.80.0）。
- **Dify 插件**：千问插件由 Dify 官方维护，非阿里云提供。最新版插件可能不稳定，可尝试较早版本。子业务空间 API Key 可能触发 `qwen-turbo` 权限校验。
- **地域匹配**：按量计费时，API Key 必须与 Base URL 的地域一致，否则会报 401 错误。

## 常见错误排查

| 错误 | 可能原因 | 解决方案 |
|------|----------|----------|
| 401 Incorrect API key | API Key 与 Base URL 不匹配或地域不一致 | 确认凭证来自同一方案和地域 |
| 400 InternalError.Algo.InvalidParameter | 思考模式未正确开启 | 勾选 Enable R1 messages format（Cline）或配置 `enable_thinking` |
| enable_thinking parameter is restricted to True | 模型仅支持思考模式 | 在客户端开启思考模式 |
| Model does not work with your current plan | Cursor 免费版限制 | 升级至 Cursor Pro 及以上 |
| Hermes 仍连接 OpenRouter | provider 未设为 custom | 执行 `hermes config set model.provider custom` |

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)

