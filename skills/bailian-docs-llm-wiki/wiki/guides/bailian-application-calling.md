# bailian [application call](../api/application-call.md)ing

百炼应用调用是将阿里云百炼平台构建的智能体应用或工作流应用集成至业务系统的标准方式，支持通过 DashScope SDK 或直接 HTTP API 调用。所有调用均需提供有效的 API Key 和应用 ID（APP_ID），并遵循统一的请求结构与认证机制。该能力适用于单轮问答、多轮对话及含自定义插件参数的复杂场景。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - **智能体应用**（Single Agent Application）：面向单一任务的轻量级智能体，适用于简单问答、内容生成等场景 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - **工作流应用**（Workflow Application）：支持多节点编排（如大模型节点、插件节点、条件分支等），适用于需流程控制、工具调用或状态管理的复杂业务逻辑 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
  
- **核心功能**：
  - 单轮文本生成（`prompt` 输入 → `text` 输出）；
  - 多轮对话支持（通过 `session_id` 或显式 `messages` 数组维护上下文）；
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 向关联插件传递业务参数）[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

> **注意**：文档 2 明确声明“本文档仅适用于华北2（北京）地域”，而文档 1 和文档 3 均未限定地域。实际调用时若在非北京地域遇到 `404 Not Found` 或 `RegionNotSupported` 错误，请确认应用部署地域与 API Endpoint 一致性（当前默认 endpoint `https://dashscope.aliyuncs.com` 仅服务北京地域）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在百炼控制台「应用管理」中获取。 |
| `prompt` | string | 否（但 `input` 中必须有 `prompt` 或 `messages`） | 用户输入的自然语言指令；若使用 `messages` 则此项可省略。 |
| `messages` | array | 否（替代 `prompt`） | 格式为 `[{"role": "user/system/assistant", "content": "..."}]`，用于显式管理多轮对话历史。 |
| `session_id` | string | 否 | 由服务端生成的会话标识，启用云端自动上下文恢复（有效期 1 小时，最多 50 轮）。 |
| `biz_params` | object | 否 | 用于传递自定义插件参数，结构为 `{"user_defined_params": {"plugin_code": {"param_key": "param_value"}}}`。 |
| `parameters` | object | 否 | 模型级超参（如 `temperature`, `max_tokens`），具体字段依底层模型而定。 |
| `debug` | object | 否 | 调试开关（如 `{"enable": true}`），用于返回中间执行日志（仅限调试环境）。 |

> **注意**：当请求中同时存在 `session_id` 和 `messages` 时，系统**优先使用 `messages`**（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 中的明确说明），`prompt` 将被忽略。

## 使用方式

### 1. 准备工作
- 获取 API Key：前往 [密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并配置为环境变量 `DASHSCOPE_API_KEY`（推荐）；
- 获取 APP_ID：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面复制目标应用的 ID；
- （SDK 方式）安装对应语言 SDK：Python（`pip install -U dashscope`）、Java（Maven/Gradle 依赖）、Node.js（`npm install axios`）等。

### 2. 调用示例（统一接口）
- **SDK 调用（Python）**：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
      # 或使用 messages: messages=[{"role": "user", "content": "你好"}]
      # 或传递插件参数: biz_params={"user_defined_params": {"plugin_abc": {"id": 123}}}
  )
  print(response.output.text)
  ```

- **HTTP 调用（curl）**：
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

### 3. 多轮对话处理
- **推荐方式（显式 `messages`）**：客户端维护完整对话历史数组，每次请求携带全部 `messages`，避免服务端状态依赖；
- **便捷方式（`session_id`）**：首次调用后从响应中提取 `session_id`，后续请求复用该 ID 即可加载历史（需注意时效性与轮数限制）。

## 限制和注意事项

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**，智能体应用虽未明文限定，但建议统一使用北京 endpoint 以确保兼容性；
- **认证安全**：严禁在代码中硬编码 `api_key` 或 `DASHSCOPE_API_KEY`，必须通过环境变量或密钥管理服务注入；
- **插件参数要求**：自定义插件的输入参数**必须配置为“业务透传”**（见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)），否则 `biz_params` 无法生效；
- **错误处理**：所有调用应检查 `status_code`（HTTP）或 `response.status_code`（SDK），失败时解析 `request_id` 和 `message` 并参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code) 排查；
- **SDK 版本**：Java SDK 建议 ≥ 2.12.0（见文档 1 和 2），Python SDK 建议 ≥ 1.14.0（见文档 3），低版本可能缺失 `biz_params` 或 `messages` 支持。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


