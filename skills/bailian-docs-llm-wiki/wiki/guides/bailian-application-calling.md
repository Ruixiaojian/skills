# bailian [application call](../api/application-call.md)ing

百炼应用调用是将阿里云百炼平台构建的智能体应用或工作流应用集成到业务系统的核心方式，支持通过 DashScope SDK 或标准 HTTP API 进行同步调用。所有调用均需有效 API Key 和应用 ID，并遵循统一的请求结构与认证机制。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - **智能体应用（Single Agent Application）**：面向单任务、轻量级对话场景，适用于问答、摘要、指令执行等。
  - **工作流应用（Workflow Application）**：面向多步骤、编排型任务，支持插件调用、条件分支、节点串联等复杂逻辑（[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 和 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 均明确支持该类型）。
- **核心能力**：
  - 单轮文本生成（`prompt` 输入 → `text` 输出）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组维护上下文）
  - 自定义插件参数透传（仅限已关联插件的智能体/工作流应用，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）
- **底层模型**：实际执行由应用绑定的模型（如 `qwen-max`、`qwen-plus`）完成，调用方无需指定模型 ID；模型选择在百炼控制台配置并发布应用时确定。

> **注意**：文档 2 明确声明“本文档仅适用于华北2（北京）地域”，而文档 1 和文档 3 未限定地域。若跨地域调用失败，请优先确认应用部署地域与 API Endpoint 是否匹配（当前统一使用 `https://dashscope.aliyuncs.com`，但后端路由受地域约束）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✓ | 百炼控制台生成的应用唯一标识（APP_ID），见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 前提条件 |
| `prompt` | string | ✓（基础调用） | 用户输入的自然语言指令；若使用 `messages` 多轮模式则可省略 |
| `biz_params` | object | ✗（可选） | 用于传递自定义插件参数，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }`，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |
| `session_id` | string | ✗（可选） | 启用云端会话管理时使用，有效期 1 小时，最多 50 轮；与 `messages` 同时存在时以 `messages` 为准 |
| `messages` | array | ✗（可选） | 显式维护的对话历史数组，格式同 OpenAI `messages`，推荐用于精确上下文控制 |

## 使用方式

### 1. 准备工作
- 获取 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`（强烈推荐，避免硬编码）；
- 在百炼控制台获取目标应用的 `app_id`；
- 若使用 SDK，按语言安装对应版本（Python 推荐 ≥1.14.0；Java 推荐 ≥2.12.0）。

### 2. 调用方式（三选一）
- **DashScope SDK（推荐）**：封装了认证、序列化、错误处理，各语言示例见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 的 Python/Java 章节；
- **HTTP API（通用）**：向 `https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion` 发起 POST 请求，Header 包含 `Authorization: Bearer ${DASHSCOPE_API_KEY}`，Body 为 JSON 格式；
- **Responses API（OpenAI 兼容）**：文档 2 提示“如需使用 Responses API 调用，请参阅 [Responses API](https://help.aliyun.com/zh/model-studio/openai-responses-api/)”，但原始文档未提供具体用法，开发者需另行查阅该独立文档。

### 3. 多轮对话实现
- **`session_id` 模式**：首次调用不传，响应中返回 `session_id`；后续请求携带该值，服务端自动加载历史；
- **`messages` 模式（推荐）**：客户端自行维护 `[{ "role": "user", "content": "..." }, { "role": "assistant", "content": "..." }]` 数组，每次请求完整提交，完全可控。

## 限制和注意事项

- **地域限制**：工作流应用调用明确限定于华北2（北京）地域（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)），智能体应用未声明此限制，但建议统一部署地域；
- **会话时效**：`session_id` 有效期为 1 小时，超时后需新建会话；
- **插件参数**：`biz_params.user_defined_params` 中的 `plugin_code` 必须与百炼控制台中插件卡片显示的 ID 完全一致，且插件必须已成功关联至目标应用并发布；
- **错误处理**：所有调用均返回标准 HTTP 状态码及 `request_id`，生产环境务必捕获异常并记录 `request_id` 用于问题排查；
- **安全实践**：严禁在代码中硬编码 `api_key`，必须通过环境变量或密钥管理服务注入。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


