# bailian [application call](../api/application-call.md)ing

百炼应用调用是指通过 DashScope SDK 或标准 HTTP API，将已发布的百炼智能体应用或工作流应用集成到自有业务系统中。调用过程统一使用 `POST /api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话及插件参数透传，适用于各类 AI 增强场景。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)（即单智能体应用）
  - [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)（原“智能体编排应用”，已由工作流应用替代）
- **核心能力**：
  - 单轮文本生成（`prompt` 输入 → `output.text` 输出）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）
  - 自定义插件参数透传（需在应用内配置插件并启用“业务透传”参数模式）  
- **底层模型**：实际执行模型由应用发布时绑定的模型决定（如 `qwen-max`、`qwen-plus`），调用方无需指定；响应中 `usage.models[].model_id` 字段可查实际使用的模型。

> **注意**：文档 2 明确声明“本文档仅适用于华北2（北京）地域”，而文档 1 和文档 3 未限定地域。若跨地域调用失败，请优先确认应用所在地域与 API Endpoint 是否匹配（当前仅北京地域支持工作流应用调用）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 |
| `prompt` | string | 否（多轮对话时可省略） | 当前轮次的用户输入指令；若使用 `messages` 则此字段被忽略 |
| `biz_params` | object | 否 | 用于传递自定义插件参数，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }`；详见[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |
| `session_id` | string | 否 | 启用云端会话管理时使用，有效期 1 小时，最多 50 轮 |
| `messages` | array | 否 | 替代 `prompt` 的推荐方式，格式同 OpenAI：`[{ "role": "user", "content": "..." }, { "role": "assistant", "content": "..." }]`；若同时传 `session_id` 和 `messages`，以 `messages` 为准 |

## 使用方式

### 1. 准备工作
- 获取 API Key：前往[密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key)创建并配置为环境变量 `DASHSCOPE_API_KEY`（**强烈推荐**，避免硬编码）  
- 获取 `app_id`：在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)中复制目标应用 ID  
- 安装 SDK（可选）：Python 执行 `pip install -U dashscope`；Java/Node.js 等参见对应语言示例  

### 2. 发起调用
- **SDK 方式（推荐）**：  
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？",
      biz_params={"user_defined_params": {"plugin_abc": {"query": "test"}}}
  )
  print(response.output.text)
  ```
- **HTTP 方式（通用）**：  
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "input": {
        "prompt": "你是谁？",
        "biz_params": {
          "user_defined_params": {
            "plugin_abc": {"query": "test"}
          }
        }
      }
    }'
  ```

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持华北2（北京）地域；智能体应用无明确地域限制，但建议与应用部署地域一致以降低延迟。
- **会话管理**：`session_id` 有效期为 1 小时且最多承载 50 轮对话；生产环境推荐自行维护 `messages` 数组以获得完全控制权。
- **插件参数**：必须在插件工具配置中将参数“传参方式”设为 **业务透传**，否则 `biz_params` 中的参数不会生效。
- **错误处理**：所有调用均返回标准 HTTP 状态码（如 `401 Unauthorized`、`404 Not Found`）及 `request_id`，用于问题定位；错误码详情请参考[开发者参考文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。
- **安全要求**：API Key **严禁硬编码**于源码或前端代码中；务必通过环境变量或密钥管理服务注入。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


