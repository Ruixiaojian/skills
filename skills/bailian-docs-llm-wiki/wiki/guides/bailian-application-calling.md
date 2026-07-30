# bailian [application call](../api/application-call.md)ing

百炼应用调用是将阿里云百炼平台构建的智能体应用或工作流应用集成至业务系统的标准方式，支持通过 DashScope SDK 或 HTTP API 进行同步调用。所有调用均需有效 API Key 和应用 ID，并遵循统一的请求结构与认证机制。

## 支持的模型/功能

- **智能体应用（Single Agent Application）**：适用于单一角色、任务导向的轻量级智能体，如问答助手、内容生成器等。[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)  
- **工作流应用（Workflow Application）**：支持多节点编排（如大模型节点、插件节点、条件分支等），适用于复杂业务逻辑，例如审批流程、多步骤信息聚合等。[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)  
- **自定义插件参数传递**：仅限已关联插件的智能体应用或工作流应用，可通过 `biz_params.user_defined_params` 向指定插件透传业务参数（如 `article_index`）。该能力不适用于纯大模型节点直出的应用。[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)  

> **注意**：文档 3 明确声明“本文档仅适用于华北2（北京）地域”，而文档 1 和文档 2 均未限定地域。实际调用时，若在非北京地域调用工作流应用失败，请确认 endpoint 是否适配当前地域（如华东1使用 `https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion` 仍为通用地址，但后端路由可能受地域限制）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台应用卡片上获取的唯一应用 ID，区分智能体应用与工作流应用 |
| `prompt` | string | 是（单轮） | 用户输入的原始指令文本；若启用 `messages` 多轮模式则可省略 |
| `biz_params` | object | 否 | 用于传递插件参数等业务上下文，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }` |
| `session_id` | string | 否 | 启用云端对话历史管理时提供，有效期 1 小时，最多 50 轮 |
| `messages` | array | 否（替代 [prompt](prompt.md)） | 自行维护的对话历史数组，格式同 OpenAI `messages`，优先级高于 `session_id` |

## 使用方式

### 1. 准备工作
- 获取 API Key：前往 [密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并复制；
- 获取 `app_id`：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面对应应用卡片中复制；
- （推荐）配置环境变量：`export DASHSCOPE_API_KEY=sk-xxx`，避免硬编码。

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

### 3. HTTP 调用（curl 示例）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "input": {"prompt": "你是谁？"},
    "parameters": {},
    "debug": {}
  }'
```

### 4. 插件参数传递（SDK Python 示例）
```python
biz_params = {
    "user_defined_params": {
        "your_plugin_code": {"article_index": 2}
    }
}
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="查询寝室公约",
    biz_params=biz_params  # 仅对已关联该插件的应用生效
)
```

## 限制和注意事项

- **地域限制**：工作流应用调用明确要求华北2（北京）地域，智能体应用无显式地域约束，但建议优先使用与应用创建地域一致的 endpoint。  
- **SDK 版本要求**：Java SDK 需 ≥ 2.12.0（见文档 1 和文档 3），Python SDK 推荐 ≥ 1.14.0（见文档 2）以支持 `biz_params`；低版本可能忽略该字段。  
- **多轮对话**：`session_id` 由服务端自动维护，但最长仅保留 1 小时且最多 50 轮；生产环境强烈推荐自行管理 `messages` 数组以保障上下文可控性。  
- **安全实践**：API Key 绝不可硬编码于源码或前端代码中，必须通过环境变量或密钥管理服务注入。  
- **错误处理**：所有响应均含 `request_id`，用于问题排查；具体错误码含义请查阅 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)


