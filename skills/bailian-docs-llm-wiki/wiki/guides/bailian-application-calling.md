# bailian [application call](../api/application-call.md)ing

百炼应用调用是指通过 DashScope SDK 或标准 HTTP API，将阿里云百炼平台创建的智能体应用（Single Agent Application）或工作流应用（Workflow Application）集成至自有业务系统的能力。该机制统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义插件参数透传等核心能力，适用于从简单问答到复杂编排的各类场景。

## 支持的模型/功能

- **应用类型**：同时支持[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)和[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)，二者调用方式完全一致，无需区分 SDK 或 HTTP 接口逻辑。
- **核心能力**：
  - 单轮文本生成（`prompt` 输入）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）
  - 自定义插件参数透传（需在应用中已关联插件，并通过 `biz_params.user_defined_params` 传递）
- **模型绑定**：底层模型由应用发布时所选模型决定（如 `qwen-max`、`qwen-plus`），调用方无需指定；响应中 `usage.models[].model_id` 字段可查实际调用模型。

> **注意**：文档2明确声明“本文档仅适用于华北2（北京）地域”，而文档1和文档3未限定地域。生产环境部署前请确认应用所在地域与 API Endpoint 匹配，否则可能返回 404 或权限错误。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台应用卡片上复制的唯一 ID，非模型 ID |
| `prompt` | string | 否（若提供 `messages` 则可省略） | 当前轮次用户输入文本；若启用多轮且使用 `messages`，则不应再传 `prompt` |
| `messages` | array | 否（推荐用于多轮） | 按时间序排列的对话历史，格式为 `[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]`；优先级高于 `session_id` |
| `session_id` | string | 否（仅用于云端托管多轮） | 由服务端生成并返回，有效期 1 小时，最多支持 50 轮；若与 `messages` 同时存在，以 `messages` 为准 |
| `biz_params` | object | 否 | 用于透传自定义插件参数，结构为 `{"user_defined_params": {"{plugin_code}": {"param_key": "value"}}}`；详见[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |

## 使用方式

### 前置准备
1. 获取 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key) 并配置为环境变量 `DASHSCOPE_API_KEY`（强烈推荐，避免硬编码）；
2. 在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取目标应用的 `app_id`；
3. （SDK 方式）安装对应语言 SDK：Python（`pip install -U dashscope`）、Java（Maven/Gradle 引入 `com.alibaba:dashscope-sdk-java`）、Node.js（`npm install axios`）等。

### 调用示例（统一接口）
- **HTTP Endpoint**：`POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`
- **认证头**：`Authorization: Bearer ${DASHSCOPE_API_KEY}`
- **请求体（JSON）**：
  ```json
  {
    "input": {
      "prompt": "你是谁？",
      "biz_params": {
        "user_defined_params": {
          "plugin_abc123": {"query_id": 42}
        }
      }
    },
    "parameters": {},
    "debug": {}
  }
  ```

- **SDK 调用（Python）**：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？",
      biz_params={"user_defined_params": {"plugin_abc123": {"query_id": 42}}}
  )
  ```

## 限制和注意事项

- **地域限制**：工作流应用调用[仅支持华北2（北京）地域](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)，智能体应用无此限制，但建议统一部署地域以避免跨域问题。
- **多轮对话**：
  - `session_id` 有效期为 1 小时，超时后需新建会话；
  - 显式 `messages` 方式更可控，推荐用于需精确控制上下文长度或敏感信息隔离的场景；
- **插件参数**：
  - `biz_params.user_defined_params` 中的 `{plugin_code}` 必须与百炼控制台中插件卡片显示的 ID 完全一致；
  - 插件节点必须已在目标应用中**发布**，否则参数不生效；
- **错误处理**：所有调用均应检查 `response.status_code`（HTTP）或 `response.status_code`（SDK），失败时解析 `request_id` 和 `message` 并参考[错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


