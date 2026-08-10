# bailian [application call](../api/application-call.md)ing

百炼 Application Calling 是百炼平台提供的统一 API 调用机制，支持通过 DashScope SDK 或标准 HTTP 接口调用已发布的智能体应用（Agent 1.0）和工作流应用（Workflow Application），实现业务系统与大模型能力的快速集成。调用方式一致，但不同应用类型在模型支持、参数传递和上下文管理上存在差异，需按实际应用场景选择。

## 支持的模型/功能

- **支持的应用类型**：智能体应用（[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)）和工作流应用（[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）。文档明确指出“智能体编排应用已被工作流应用替代”，因此不再支持旧版智能体编排应用。
- **模型能力限制**：工作流应用**不支持文生图大模型**（如wanx系列），仅支持文本生成类大模型（如 qwen-max、qwen-plus 等）；智能体应用未声明此项限制，但实际能力取决于其内部节点配置。
- **核心功能**：
  - 单轮问答（`prompt` 字段）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理历史）
  - 自定义插件参数透传（仅限智能体应用及工作流应用中的插件节点，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）

> **注意**：文档1强调“本文档仅适用于华北2（北京）地域”，而文档2和3未提及地域限制。若跨地域调用失败，请优先确认 endpoint 是否匹配所在地域（如华东1使用 `https://dashscope.aliyuncs.com/api/v1/apps/...` 可能不适用，需查阅最新地域 endpoint 列表）。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 来源 |
|------|------|------|------|------|
| `app_id` | string | ✓ | 应用唯一标识，在百炼控制台「应用管理」页面获取 | 所有文档均要求 |
| `prompt` | string | ✓（单轮） | 用户输入的自然语言指令；若使用 `messages` 进行多轮，则此字段可省略 | [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)、[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) |
| `messages` | array | ✗（推荐用于多轮） | 显式维护的对话历史数组，格式为 `[{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]`；若同时提供 `session_id` 和 `messages`，系统**优先使用 `messages`** | [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) |
| `session_id` | string | ✗（可选） | 服务端托管的会话 ID，有效期 1 小时，最多支持 50 轮对话；适合轻量级状态管理 | [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) |
| `biz_params.user_defined_params` | object | ✗（插件场景） | 用于向关联的自定义插件透传参数，结构为 `{ "plugin_code": { "param_key": value } }`；仅对已关联插件的智能体/工作流应用生效 | [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |

## 使用方式

### 通用前提
- 获取并配置 `DASHSCOPE_API_KEY`（推荐设为环境变量 `DASHSCOPE_API_KEY`，避免硬编码）
- 确保应用已发布，且 `app_id` 正确

### SDK 调用（Python 示例）
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

### HTTP 调用（curl 示例）
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

### 多轮对话（推荐 `messages` 方式）
```python
messages = [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！我是千问。"},
    {"role": "user", "content": "今天天气如何？"}
]
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    messages=messages  # 注意：此时无需 prompt
)
```

### 插件参数透传（仅智能体/工作流应用）
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
    biz_params=biz_params
)
```

## 限制和注意事项

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**，其他地域需确认 endpoint 兼容性（见上方注意）。
- **安全实践**：所有文档均**强烈反对在代码中硬编码 `API Key`**，必须通过环境变量或密钥管理服务注入。
- **SDK 版本要求**：
  - Java SDK：建议 ≥ 2.12.0（见文档1、2）
  - Python SDK：插件场景建议 ≥ 1.14.0（见文档3）
- **多轮对话限制**：`session_id` 有效期为 1 小时，最多 50 轮；`messages` 长度受模型 context window 限制，需自行截断。
- **错误处理**：响应含 `request_id`，应记录该 ID 用于问题排查；错误码参考 [开发者参考错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。
- **模型返回信息**：HTTP 响应中 `usage.models` 数组包含实际调用的模型 ID（如 `qwen-max`）及 token 消耗，可用于计费与性能分析。

## 来源文档

- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


