# bailian [application call](../api/application-call.md)ing

百炼应用调用是指通过 DashScope SDK 或标准 HTTP API，将已发布的百炼智能体应用（Agent 1.0）或工作流应用集成至第三方业务系统的能力。调用过程统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义[插件](../concepts/plugin.md)参数透传等核心能力，适用于各类 AI 增强型业务场景。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - 智能体应用（Agent 1.0），详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - 工作流应用（Workflow Application），详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **模型能力**：底层由百炼托管的大模型（如 `qwen-max`、`qwen-plus` 等）提供推理服务，具体模型由应用发布时绑定的节点决定；**工作流应用不支持文生图大模型**（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 中“说明”部分）。
- **高级功能**：
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理历史）；
  - 自定义[插件](../concepts/plugin.md)参数透传（通过 `biz_params.user_defined_params` 传递[插件](../concepts/plugin.md)入参），该能力同时适用于智能体应用和工作流应用，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

> **注意**：文档 1 和文档 2 的示例代码完全一致（包括 Python/Java/curl 等所有语言片段），但文档 2 明确声明“本文档仅适用于华北2（北京）地域”，而文档 1 未提及地域限制。实际调用前请确认应用所在地域与 API Endpoint 匹配（默认 `dashscope.aliyuncs.com` 对应华北2）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台中应用卡片显示的唯一 ID，非模型 ID |
| `prompt` | string | 否（若提供 `messages` 则可省略） | 当前轮次用户输入文本；若使用 `messages` 数组则无需此字段 |
| `messages` | array | 否（推荐用于多轮） | 按时间顺序排列的对话消息数组，格式为 `[{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]` |
| `session_id` | string | 否（用于云端会话） | 服务端维护的会话标识，有效期 1 小时，最多支持 50 轮；若同时传 `messages`，则优先使用 `messages` |
| `biz_params` | object | 否 | 用于传递自定义插件参数，结构为 `{"user_defined_params": {"<plugin_code>": {<param_key>: <param_value>}}}`，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |

## 使用方式

### 1. 前置准备
- 获取 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`（推荐，避免硬编码）；
- 在百炼控制台获取目标应用的 `APP_ID`；
- 若使用 SDK，安装对应语言的 DashScope SDK（Python ≥1.14.0，Java ≥2.12.0）。

### 2. 调用方式（任选其一）
- **SDK 调用（推荐）**：  
  Python 示例：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
  )
  ```
- **HTTP API 调用**：  
  curl 示例：
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

### 3. 多轮对话（两种模式）
- **云端会话模式**：首次调用不传 `session_id`，响应中返回 `session_id`；后续请求携带该 `session_id` 即可自动加载历史。
- **本地管理模式（推荐）**：客户端自行维护 `messages` 数组，每次请求完整提交全部历史 + 新消息，精度更高、可控性更强。

## 限制和注意事项

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**，智能体应用无明确地域限制，但建议与应用部署地域保持一致（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）。
- **安全要求**：API Key **严禁硬编码在源码中**，必须通过环境变量或密钥管理服务注入。
- **插件参数**：自定义插件参数必须通过 `biz_params.user_defined_params` 传递，且插件工具的“传参方式”需设置为 **业务透传**（见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）。
- **错误处理**：所有调用均需检查 `status_code`（HTTP）或 `response.status_code`（SDK），失败时解析 `request_id` 和 `message` 用于问题定位，参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。
- **[Token](../concepts/token.md) 限制**：单次请求总 token 数受所绑定模型的上下文窗口限制，超限将触发截断或报错。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


