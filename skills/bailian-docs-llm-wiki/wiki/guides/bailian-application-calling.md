# bailian [application call](../api/application-call.md)ing

百炼应用调用是指通过 DashScope SDK 或标准 HTTP API，将百炼平台创建的智能体应用（Agent 1.0）或工作流应用集成至外部业务系统的能力。该机制统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义[插件](../concepts/plugin.md)参数透传等核心能力，适用于构建 AI 增强型业务服务。

## 支持的模型/功能

- **应用类型**：同时支持 [调用智能体应用 (raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 和 [调用工作流应用 (raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)，二者调用方式完全一致。
- **核心功能**：
  - 单轮文本生成（基础 [prompt](prompt.md) 输入）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）
  - 自定义[插件](../concepts/plugin.md)参数透传（需在应用中已关联[插件](../concepts/plugin.md)，并通过 `biz_params.user_defined_params` 传递）
- **模型绑定**：应用内部已绑定具体大模型（如 `qwen-max`、`qwen-plus`），调用时无需指定模型 ID；响应中的 `usage.models[].model_id` 反映实际执行模型。

> **注意**：文档2明确声明“百炼工作流不支持使用文生图大模型”，而文档1和3未提及此限制。该限制仅适用于工作流应用，且为地域相关约束（文档2强调“仅适用于华北2（北京）地域”），开发者需根据所选应用类型和部署地域确认可用模型能力。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 |
| `prompt` | string | 否（若提供 `messages` 则可省略） | 单轮对话的用户输入文本；若启用多轮对话且使用 `messages`，则不应传此字段 |
| `messages` | array | 否（推荐用于多轮） | 消息历史数组，格式同 OpenAI `messages`，含 `role`（`user`/`assistant`）和 `content`；优先级高于 `session_id` |
| `session_id` | string | 否（仅用于云端存储模式） | 由服务端生成并返回，用于自动加载历史对话；有效期 1 小时，最多 50 轮 |
| `biz_params` | object | 否 | 用于传递自定义插件参数，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": "<value>" } } }`；详见 [应用的自定义参数传递 (raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |

## 使用方式

### 1. 准备工作
- 获取 API Key：前往[密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key)创建并配置为环境变量 `DASHSCOPE_API_KEY`（**强烈推荐**，避免硬编码）。
- 获取 `app_id`：在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面复制目标应用卡片上的 APP_ID。
- （可选）安装 SDK：Python、Java 等语言需安装对应 DashScope SDK；HTTP 调用无需安装。

### 2. 发起调用
- **SDK 方式（推荐）**：使用 `Application.call()` 方法，传入 `api_key`（或依赖环境变量）、`app_id`、`prompt`（或 `messages`）及可选 `biz_params`。
- **HTTP 方式**：向 `https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion` 发送 POST 请求，`Authorization: Bearer <API_KEY>`，请求体 JSON 中 `input` 字段包含 `prompt` 或 `messages` 及 `biz_params`。

示例（Python SDK，含插件参数）：
```python
from dashscope import Application
biz_params = {
    "user_defined_params": {
        "your_plugin_code": {"article_index": 2}
    }
}
response = Application.call(
    app_id='YOUR_APP_ID',
    prompt='寝室公约内容',
    biz_params=biz_params
)
```

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持华北2（北京）地域；智能体应用无此限制（依据文档1与文档2对比）。
- **多轮对话限制**：`session_id` 模式下，单个 session 最多 50 轮对话，有效期 1 小时；`messages` 模式无此限制，但需自行控制上下文长度（受模型 token 限制）。
- **插件参数要求**：自定义插件的输入参数必须在控制台配置为“业务透传”方式，否则无法通过 `biz_params` 传递。
- **错误处理**：所有调用均需检查 `response.status_code`（SDK）或 HTTP 状态码（HTTP），失败时参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。
- **安全实践**：API Key **严禁硬编码**，必须通过环境变量或密钥管理服务注入；生产环境应启用最小权限策略。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


