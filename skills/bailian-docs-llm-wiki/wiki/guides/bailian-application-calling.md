# bailian [application call](../api/application-call.md)ing

百炼应用调用是将阿里云百炼平台构建的智能体应用或工作流应用集成至第三方业务系统的标准方式，支持通过 DashScope SDK 或 HTTP API 发起请求。所有调用均需提供有效的 API Key 和应用 ID，并遵循统一的请求结构与认证机制。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - **智能体应用（Agent 1.0）**：面向单任务、轻量级交互场景，适用于简单问答、内容生成等 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - **工作流应用**：面向多步骤、编排式复杂任务，支持插件节点、条件分支与状态管理，已替代旧版“智能体编排应用” [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。

- **核心能力**：
  - 单轮文本生成（`prompt` 输入 → `text` 输出）；
  - 多轮对话支持（通过 `session_id` 或显式 `messages` 数组维护上下文）；
  - 自定义插件参数透传（仅限已关联插件的应用，需通过 `biz_params.user_defined_params` 传递）[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

> **注意**：文档 2 明确指出“本文档仅适用于华北2（北京）地域”，而文档 1 和文档 3 均未声明地域限制。实际部署时，请确认目标应用所在地域是否支持对应调用方式；若跨地域调用失败，应优先检查地域合规性。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台中应用卡片显示的唯一 ID，非模型 ID |
| `prompt` | string | 否（但 `input.prompt` 或 `messages` 至少一项必填） | 主指令文本，用于单轮调用；若使用 `messages` 则可省略 |
| `biz_params` | object | 否 | 仅当需向自定义插件传参时使用，结构为 `{ "user_defined_params": { "<plugin_code>": { ... } } }` |
| `session_id` | string | 否 | 用于启用云端会话历史（有效期 1 小时，最多 50 轮） |
| `messages` | array | 否 | 替代 `prompt` 的推荐方式，格式同 OpenAI：`[{ "role": "user/system/assistant", "content": "..." }]` |

> **注意**：若请求中同时包含 `session_id` 和 `messages`，系统将**优先使用 `messages`**（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）。

## 使用方式

### 1. 准备工作
- 获取 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key) 并配置为环境变量 `DASHSCOPE_API_KEY`（推荐）；
- 在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面获取目标应用的 `APP_ID`；
- 若使用 SDK，安装对应语言版本（Python ≥ 1.14.0，Java ≥ 2.12.0）。

### 2. 调用示例（统一接口）
所有语言/方式均调用同一 HTTP 端点：  
`POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`

- **SDK 方式（Python）**：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
  )
  print(response.output.text)
  ```

- **HTTP 方式（curl）**：
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "input": {"prompt": "你是谁？"},
          "parameters": {},
          "debug": {}
        }'
  ```

- **插件参数传递（需 `biz_params`）**：
  ```python
  biz_params = {
      "user_defined_params": {
          "your_plugin_code": {"article_index": 2}
      }
  }
  response = Application.call(
      app_id="YOUR_APP_ID",
      prompt="寝室公约内容",
      biz_params=biz_params
  )
  ```

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持华北2（北京）地域，智能体应用无明确地域约束，但建议与应用部署地域保持一致；
- **会话管理**：`session_id` 由服务端生成并返回，客户端需自行保存并在后续请求中复用；若需精确控制上下文，**强烈推荐使用 `messages` 数组方式**；
- **安全要求**：API Key **严禁硬编码**于源码或前端代码中，必须通过环境变量或密钥管理服务注入；
- **插件约束**：自定义插件参数仅在应用已关联对应插件且插件配置中启用“业务透传”时生效；插件 ID 需从控制台插件卡片准确复制；
- **错误处理**：所有调用均返回 `request_id`，用于问题排查；具体错误码请查阅 [开发者参考文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


