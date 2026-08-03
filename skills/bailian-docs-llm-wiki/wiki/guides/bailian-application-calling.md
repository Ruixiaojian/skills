# bailian [application call](../api/application-call.md)ing

百炼应用调用是将阿里云百炼平台创建的智能体应用或工作流应用集成至业务系统的标准方式，支持通过 DashScope SDK 或 HTTP API 发起请求。调用过程统一使用 `APP_ID` 标识目标应用，并通过 `prompt` 输入指令，返回结构化文本响应。所有调用均需有效 API Key 和地域合规性保障。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - **智能体应用**（Single-Agent Application）：适用于单一角色、任务导向的轻量级智能体，如问答助手、内容生成器等 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - **工作流应用**（Workflow Application）：适用于多节点编排、含插件/条件分支/循环等复杂逻辑的流程型应用，已替代旧版“智能体编排应用” [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。

- **核心能力**：
  - 单轮指令响应（`prompt` + `biz_params`）；
  - 多轮对话支持（通过 `session_id` 或显式 `messages` 数组）；
  - 自定义插件参数透传（仅限工作流应用及已关联插件的智能体应用）[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

> **注意**：文档 2 明确声明“本文档仅适用于华北2（北京）地域”，而文档 1 和文档 3 均未提及地域限制。实际调用时，若跨地域（如华东1）调用工作流应用，可能因服务端路由失败导致 `404 Not Found` 或 `403 Forbidden` 错误。请优先在控制台确认应用部署地域，并匹配 API Endpoint（如 `https://dashscope.aliyuncs.com` 默认指向华北2；其他地域需使用对应 endpoint，详见 [DashScope 地域与 Endpoint](https://help.aliyun.com/zh/model-studio/developer-reference/endpoint)）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✓ | 应用唯一标识，从百炼控制台「应用管理」页面获取。 |
| `prompt` | string | ✓（单轮） | 用户输入的自然语言指令，用于驱动应用执行。多轮对话中可省略（当使用 `messages` 时）。 |
| `biz_params` | object | ✗ | 用于传递自定义插件参数或业务上下文。结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }`。详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。 |
| `session_id` | string | ✗（可选） | 启用云端会话管理，有效期 1 小时，最多支持 50 轮。与 `messages` 同时存在时，**以 `messages` 为准**。 |
| `messages` | array | ✗（可选） | 显式维护的对话历史数组，格式同 OpenAI `messages`（`[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]`），推荐用于精确控制上下文。 |

## 使用方式

### 1. 准备工作
- 获取 API Key：前往 [密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并记录；
- 获取 `APP_ID`：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面复制对应应用卡片 ID；
- （推荐）配置环境变量：`export DASHSCOPE_API_KEY=sk-xxx`，避免代码硬编码。

### 2. SDK 调用（Python 示例）
```python
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？",
    biz_params={"user_defined_params": {"plugin_abc123": {"query_id": 42}}}
)
if response.status_code == 200:
    print(response.output.text)
```

### 3. HTTP 调用（curl 示例）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "input": {
          "prompt": "你是谁？",
          "biz_params": {
            "user_defined_params": {
              "plugin_abc123": {"query_id": 42}
            }
          }
        }
      }'
```

SDK 支持 Python、Java、Node.js、C#、Go、PHP（见各文档完整示例），HTTP 方式兼容任意语言。

## 限制和注意事项

- **地域限制**：工作流应用调用**强制限定华北2（北京）地域**，智能体应用无明确地域约束，但建议保持应用与调用方地域一致以降低延迟 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **会话限制**：`session_id` 有效期为 1 小时，最大轮次 50；超出后需新建会话或切换为 `messages` 管理。
- **插件参数要求**：自定义插件的输入参数**必须配置为“业务透传”**，否则 `biz_params.user_defined_params` 中的值将被忽略 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。
- **错误处理**：所有调用均返回标准 HTTP 状态码（如 `400`, `401`, `429`, `500`）及 `request_id`，应结合 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code) 进行诊断。
- **安全实践**：禁止在代码中硬编码 `API Key`；生产环境务必通过环境变量或密钥管理服务注入。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


