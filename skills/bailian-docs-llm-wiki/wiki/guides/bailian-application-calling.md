# bailian [application call](../api/application-call.md)ing

百炼应用调用是指通过 DashScope SDK 或标准 HTTP API，将百炼平台创建的智能体应用（Agent 1.0）或工作流应用集成至外部业务系统的能力。该机制统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义插件参数透传等核心能力，适用于构建 AI 增强型业务服务。

## 支持的模型/功能

- **应用类型**：同时支持 [调用智能体应用 (raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 和 [调用工作流应用 (raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)，二者调用方式完全一致。
- **核心功能**：
  - 单轮文本生成（基于 `prompt` 字段）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）
  - 自定义插件参数传递（通过 `biz_params.user_defined_params` 透传至关联插件）
- **模型绑定**：应用在控制台发布时已绑定底层大模型（如 `qwen-max`、`qwen-plus`），调用时无需指定模型；响应中 `usage.models[].model_id` 可查实际执行模型。

> **注意**：[调用工作流应用 (raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 文档明确声明“本文档仅适用于华北2（北京）地域”，而 [调用智能体应用 (raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 未限定地域。生产环境应以控制台实际可用地域为准，建议优先参考控制台地域支持列表。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼应用管理页面获取的唯一 ID，非模型 ID |
| `prompt` | string | 否（若提供 `messages` 则可省略） | 单轮请求的用户输入文本；多轮场景下建议改用 `messages` |
| `messages` | array | 否（推荐用于多轮） | 消息数组，格式为 `[{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]`；若与 `session_id` 同时存在，以 `messages` 为准 |
| `session_id` | string | 否（云端存储模式） | 由服务端生成或客户端维护的会话标识，有效期 1 小时，最多 50 轮 |
| `biz_params` | object | 否 | 用于传递自定义插件参数，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": "<value>" } } }`；详见 [应用的自定义参数传递 (raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |

## 使用方式

### 1. 准备工作
- 获取 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`（**强烈推荐**，避免硬编码）
- 在百炼控制台创建并发布应用，复制其 `APP_ID`
- （SDK 方式）安装对应语言 SDK：Python（`pip install -U dashscope`）、Java（Maven/Gradle 引入 `dashscope-sdk-java` ≥ 2.12.0）、其他语言见各文档示例

### 2. 发起调用
- **SDK 调用**（以 Python 为例）：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
  )
  ```
- **HTTP 调用**（curl 示例）：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
        "input": {"prompt": "你是谁？"},
        "parameters": {},
        "debug": {}
    }'
  ```

### 3. 处理响应
- 成功响应（HTTP 200）包含 `output.text`（生成结果）和 `usage`（token 统计）
- 错误响应需检查 `status_code`、`message` 和 `request_id`，并参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持华北2（北京）地域，智能体应用无明确限制，但建议与应用部署地域保持一致。
- **多轮对话限制**：`session_id` 会话有效期为 1 小时，且最多承载 50 轮对话；超出后需新建会话。
- **插件参数安全**：`biz_params.user_defined_params` 中的插件 ID 和参数名必须与控制台配置完全一致，否则参数将被忽略。
- **鉴权要求**：所有调用均需 `Authorization: Bearer <API_KEY>` 请求头，API Key 须具备对应应用的调用权限。
- **模型能力差异**：工作流应用明确不支持文生图大模型，智能体应用亦同；图文混合类任务需确认应用内节点配置。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


