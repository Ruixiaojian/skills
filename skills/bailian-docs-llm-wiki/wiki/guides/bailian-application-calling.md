# bailian [application call](../api/application-call.md)ing

百炼应用调用是指通过 DashScope SDK 或标准 HTTP API，将已发布的百炼智能体应用或工作流应用集成至第三方业务系统。调用过程统一使用 `POST /api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义[插件](../concepts/plugin.md)参数透传等核心能力，适用于各类 AI 增强型业务场景。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)（即单智能体应用）
  - [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)（原“智能体编排应用”，已由工作流应用替代）
- **核心能力**：
  - 单轮文本生成（`prompt` 输入）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）
  - 自定义[插件](../concepts/plugin.md)参数透传（需在应用中配置[插件](../concepts/plugin.md)节点并启用业务透传）  
- **底层模型**：实际执行由应用绑定的模型（如 `qwen-max`、`qwen-plus` 等）完成，调用方无需指定模型 ID；模型信息在响应 `usage.models[].model_id` 中返回。

> **注意**：文档2明确声明“本文档仅适用于华北2（北京）地域”，而文档1和文档3未限定地域。若跨地域调用失败，请优先确认应用部署地域与 API Endpoint 是否匹配（当前所有示例均指向 `dashscope.aliyuncs.com`，该域名默认路由至北京地域）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✅ | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 |
| `prompt` | string | ⚠️（见下文） | 单轮请求时必需；若使用 `messages` 进行多轮对话，则此项可省略 |
| `biz_params` | object | ❌ | 用于传递自定义插件参数，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }`。详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |
| `session_id` | string | ❌ | 启用云端会话管理时提供，有效期 1 小时，最多支持 50 轮对话 |
| `messages` | array | ❌ | 替代 `prompt` 的多轮对话方式，格式同 OpenAI-style `[{ "role": "user/system/assistant", "content": "..." }]`；若同时传 `session_id` 和 `messages`，以 `messages` 为准 |

## 使用方式

### 1. 准备工作
- 获取 API Key：前往 [密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并复制。
- 获取 `app_id`：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面对应应用卡片上复制。
- （推荐）配置环境变量：`export DASHSCOPE_API_KEY=sk-xxx`，避免代码硬编码。

### 2. 调用方式（任选其一）
- **DashScope SDK**（Python/Java/Node.js/C#/Go 等）：封装了认证、序列化与错误处理，推荐生产环境使用。SDK 版本要求：Python ≥ 1.14.0（插件参数）、Java ≥ 2.12.0（多轮对话支持）。
- **HTTP API**：直接调用 `POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`，需手动设置 `Authorization: Bearer <API_KEY>` 请求头。

### 3. 示例（Python SDK）
```python
from dashscope import Application
import os

# 单轮调用（含插件参数）
biz_params = {
    "user_defined_params": {
        "your_plugin_code": {"article_index": 2}
    }
}
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="寝室公约内容",
    biz_params=biz_params
)

# 多轮调用（显式 messages）
messages = [
    {"role": "user", "content": "你是谁？"},
    {"role": "assistant", "content": "我是通义千问。"},
    {"role": "user", "content": "今天天气如何？"}
]
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    messages=messages  # 注意：此时不传 prompt
)
```

## 限制和注意事项

- **地域限制**：工作流应用调用[仅支持华北2（北京）地域](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)，智能体应用无明确地域限制，但建议保持应用与调用端地域一致。
- **会话管理**：`session_id` 由服务端生成并返回于响应中（`output.session_id`），客户端需自行保存并在后续请求中复用；若使用 `messages`，则完全由客户端维护上下文。
- **插件参数**：必须满足以下条件才能生效：
  - 插件工具的输入参数“传参方式”必须设为 **业务透传**；
  - 应用内已关联该插件且已发布；
  - `biz_params.user_defined_params.<plugin_code>` 中的 `plugin_code` 必须与控制台插件卡片显示的 ID 完全一致。
- **错误处理**：所有调用均需检查 `response.status_code`（HTTP）或 `response.status_code`（SDK），非 `200` 时解析 `message` 和 `request_id` 用于排查，参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。
- **安全实践**：严禁在代码中硬编码 `DASHSCOPE_API_KEY`；务必通过环境变量或密钥管理服务注入。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


