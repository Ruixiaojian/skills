# bailian [application call](../api/application-call.md)ing

百炼应用调用是将阿里云百炼平台创建的智能体应用或工作流应用集成到业务系统的核心方式，支持通过 DashScope SDK 或标准 HTTP API 进行同步调用。所有调用均需有效 API Key 和应用 ID，并遵循统一的请求结构与认证机制。该能力适用于单轮问答、多轮对话及带[插件](../concepts/plugin.md)参数的复杂任务编排。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - **智能体应用（Single Agent Application）**：面向单一角色、任务导向的轻量级智能体，适用于客服问答、知识检索等场景 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - **工作流应用（Workflow Application）**：支持多节点编排（如大模型节点、[插件](../concepts/plugin.md)节点、条件分支），适用于需组合工具调用、逻辑判断的复杂业务流程 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心能力**：
  - 单轮文本生成（`prompt` 输入 → `text` 输出）；
  - 多轮对话支持（通过 `session_id` 或显式 `messages` 数组维护上下文）；
  - 自定义[插件](../concepts/plugin.md)参数透传（`biz_params.user_defined_params`），用于向关联插件传递业务字段 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)；
  - 调试信息返回（`debug` 字段可启用）；
  - [Token](../concepts/token.md) 使用统计（`usage.models` 中包含 `input_tokens`/`output_tokens` 及对应 `model_id`）。

> **注意**：文档 2 明确声明“本文档仅适用于华北2（北京）地域”，而文档 1 和 3 均未限定地域。实际调用时若在非北京地域遇到 `404` 或 `InvalidRegionId` 错误，应优先确认应用部署地域并使用对应 endpoint —— 当前生产环境默认 endpoint 为 `https://dashscope.aliyuncs.com`，其路由已自动适配地域，但部分旧版 SDK 或手动构造 URL 的场景仍可能受地域约束。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✓ | 百炼控制台中应用卡片显示的唯一 ID，区分智能体应用与工作流应用 |
| `prompt` | string | ✓（除 `messages` 模式外） | 用户输入的自然语言指令；若使用 `messages` 多轮模式，则此项忽略 |
| `biz_params` | object | ✗ | 用于传递插件参数，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }`，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |
| `parameters` | object | ✗ | 预留扩展字段，当前暂未开放通用参数配置 |
| `debug` | object | ✗ | 设为空对象 `{}` 即可启用调试模式，返回更详细的执行链路信息 |
| `input`（HTTP） | object | ✓ | HTTP 请求体顶层字段，必须包裹 `prompt` 或 `messages` 等子字段 |

## 使用方式

### 1. 准备工作
- 获取 API Key：前往 [密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并复制；
- 获取 `app_id`：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面复制目标应用的 ID；
- （推荐）配置环境变量：`export DASHSCOPE_API_KEY=sk-xxx`，避免代码硬编码。

### 2. SDK 调用（Python 示例）
```python
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 自动读取环境变量
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)
if response.status_code == 200:
    print(response.output.text)
```

### 3. HTTP 直接调用（curl 示例）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "input": {"prompt": "你是谁？"},
        "parameters": {},
        "debug": {}
      }'
```

### 4. 多轮对话（推荐 `messages` 模式）
```python
# 显式维护 messages（更可控）
messages = [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！我是通义千问。"},
    {"role": "user", "content": "今天天气如何？"}
]
response = Application.call(
    app_id="YOUR_APP_ID",
    messages=messages  # 此时忽略 prompt 字段
)
```

## 限制和注意事项

- **地域限制**：工作流应用调用明确要求华北2（北京）地域，智能体应用虽未明示，但建议统一部署在北京 region 以确保兼容性；
- **会话有效期**：`session_id` 有效期为 1 小时，最多支持 50 轮对话；超时或超轮次后需新建会话；
- **参数冲突规则**：若请求中同时提供 `session_id` 和 `messages`，系统**优先使用 `messages`**，`session_id` 将被忽略；
- **插件参数要求**：自定义插件的输入参数必须在控制台配置为 **“业务透传”** 方式，否则无法通过 `biz_params` 传递；
- **SDK 版本依赖**：
  - Java SDK 推荐 ≥ 2.12.0（文档 1 & 2）；
  - Python SDK 推荐 ≥ 1.14.0（文档 3 中插件调用所需）；
- **错误处理**：所有调用均返回 `request_id`，用于问题排查；常见错误码参考 [开发者参考错误码](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


