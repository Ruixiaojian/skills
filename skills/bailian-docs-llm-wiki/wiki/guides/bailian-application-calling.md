# bailian [application call](../api/application-call.md)ing

百炼应用调用是将阿里云百炼平台构建的智能体应用或工作流应用集成至第三方业务系统的标准方式，支持通过 DashScope SDK 或原生 HTTP API 进行同步调用。所有调用均需有效 API Key 和应用 ID，并遵循统一的请求结构与认证机制。该能力适用于单轮问答、多轮对话及带插件参数的复杂任务编排场景。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)（即“单智能体应用”），适用于轻量级、规则明确的对话任务；
  - [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)，适用于多节点编排、含条件分支与插件调用的复杂业务流程。
- **核心能力**：
  - 单轮 [prompt](prompt.md) 响应（`prompt` 字段）；
  - 多轮对话支持（通过 `session_id` 或显式 `messages` 数组）；
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 结构传递插件入参）；
  - 调试信息返回（`debug` 字段可启用）；
  - Token 消耗统计（响应中 `usage.models` 包含各模型 `input_tokens`/`output_tokens`）。

> **注意**：文档 2 明确声明“本文档仅适用于华北2（北京）地域”，而文档 1 和文档 3 均未提及地域限制。实际调用时若在非北京地域失败，请优先检查 endpoint 是否适配当前地域（如华东1使用 `dashscope.aliyuncs.com` 仍为通用域名，但部分内部路由可能受地域约束），建议以控制台应用详情页显示的 endpoint 为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✅ | 百炼应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取。 |
| `prompt` | string | ⚠️（见下文） | 用户输入文本。若使用 `messages` 进行多轮对话，则此字段**不可提供**；否则为必需字段。 |
| `biz_params` | object | ❌ | 用于传递自定义插件参数，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }`。详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。 |
| `parameters` | object | ❌ | 预留扩展字段，当前暂无公开可用参数。 |
| `debug` | object | ❌ | 设为空对象 `{}` 可启用调试模式，返回更详细的执行链路信息（如节点耗时、插件调用日志等）。 |

## 使用方式

### 1. 准备工作
- 获取 API Key：前往 [密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并复制；
- 获取 `app_id`：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面复制目标应用卡片上的 ID；
- （推荐）配置环境变量：`export DASHSCOPE_API_KEY=sk-xxx`，避免代码硬编码。

### 2. SDK 调用（Python 示例）
```python
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
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

### 4. 多轮对话
- **云端 session 管理**：首次调用后从响应中提取 `session_id`，后续请求携带该值即可自动续接上下文（有效期 1 小时，上限 50 轮）；
- **自主 messages 管理（推荐）**：构造 `messages` 数组（格式同 OpenAI），在 `input` 中传入，**此时必须省略 `prompt` 字段**。此方式完全可控，规避 session 过期与并发冲突问题。

### 5. 插件参数透传
需在应用内已关联插件，并确保插件工具的输入参数设置为“业务透传”。调用时通过 `biz_params.user_defined_params` 传入插件 ID 及对应参数键值对，例如：
```json
{
  "input": {
    "prompt": "查询寝室公约",
    "biz_params": {
      "user_defined_params": {
        "plugin_abc123": {"article_index": 2}
      }
    }
  }
}
```

## 限制和注意事项

- **地域限制**：工作流应用调用[仅支持华北2（北京）地域](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)，智能体应用无明确地域限制，但建议与应用部署地域保持一致；
- **SDK 版本要求**：
  - Java SDK：建议 ≥ 2.12.0（文档 1 和文档 2 均明确要求）；
  - Python SDK：插件参数功能要求 ≥ 1.14.0（见[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）；
- **安全实践**：
  - 绝对禁止在代码中硬编码 `api_key`，必须通过环境变量或密钥管理服务注入；
  - `biz_params` 中的插件参数应经业务侧校验，避免注入恶意值；
- **错误处理**：
  - 所有调用均返回标准 HTTP 状态码（如 `401 Unauthorized`, `404 Not Found`, `429 Too Many Requests`）；
  - 错误详情见 `message` 字段，`request_id` 用于阿里云技术支持排查；
  - 完整错误码参考：[开发者参考-错误码](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


