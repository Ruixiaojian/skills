# bailian [application call](../api/application-call.md)ing

百炼应用调用是指通过 DashScope SDK 或 HTTP API，将百炼平台创建的智能体应用（Agent 1.0）或工作流应用集成至第三方业务系统的能力。调用过程统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话及自定义参数透传，适用于各类 AI 增强型业务场景。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - 智能体应用（Agent 1.0），详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - 工作流应用（Workflow Application），详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心能力**：
  - 单轮文本生成（`prompt` 输入 → `output.text` 输出）；
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）；
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 向插件节点传递业务参数），详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)；
  - 调试信息返回（`debug` 字段可启用）；
  - [Token](../concepts/token.md) 使用统计（`usage.models` 中含 `input_tokens`/`output_tokens` 及 `model_id`）。

> **注意**：文档 2 明确声明“百炼工作流不支持使用文生图大模型”，而文档 1 和 3 均未提及此限制；实际调用时若涉及图像生成类插件或节点，需确认所选模型是否在工作流应用支持范围内。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✓ | 百炼控制台应用卡片中复制的 APP_ID，区分智能体应用与工作流应用 |
| `prompt` | string | ✓（单轮） | 用户输入的自然语言指令；若使用 `messages` 进行多轮对话，则此项可省略 |
| `biz_params` | object | ✗ | 用于透传自定义插件参数，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }` |
| `session_id` | string | ✗（多轮） | 由服务端生成并返回的会话标识，有效期 1 小时，最多支持 50 轮；与 `messages` 同时存在时，**优先使用 `messages`** |
| `messages` | array | ✗（多轮） | 显式维护的对话历史数组，格式同 OpenAI：`[{ "role": "user/system/assistant", "content": "..." }]`；推荐用于精确控制上下文 |
| `parameters` | object | ✗ | 预留扩展字段，当前暂无通用参数；部分应用内节点可能支持特定配置（需参考应用内部设置） |
| `debug` | object | ✗ | 设置为 `{}` 可启用调试模式，返回更详细的执行链路信息 |

## 使用方式

### 1. 前置准备
- 获取 API Key：前往 [密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并配置环境变量 `DASHSCOPE_API_KEY`（[推荐做法](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)）；
- 获取目标应用的 `app_id`：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面复制对应应用卡片 ID；
- （SDK 方式）安装对应语言 SDK：Python、Java、Node.js 等均需安装 [DashScope SDK](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；HTTP 方式跳过此步。

### 2. 调用示例（Python SDK）
```python
from dashscope import Application
import os

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)
if response.status_code == 200:
    print(response.output.text)
```

### 3. HTTP 调用（curl）
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

### 4. 自定义插件参数传递（HTTP）
```json
{
  "input": {
    "prompt": "查询寝室公约第3条",
    "biz_params": {
      "user_defined_params": {
        "plugin_abc123": {"article_index": 3}
      }
    }
  }
}
```

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持华北2（北京）地域，见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)；智能体应用无明确地域限制，但建议与应用部署地域保持一致以降低延迟。
- **会话管理**：
  - `session_id` 有效期为 1 小时，超时后需新建会话；
  - 单个 `session_id` 最多承载 50 轮对话，超出后需创建新会话；
  - 若同时提供 `session_id` 和 `messages`，服务端**优先采用 `messages`**，忽略 `session_id` 的历史加载逻辑。
- **安全规范**：
  - **禁止硬编码 API Key**：所有示例均强调应通过环境变量 `DASHSCOPE_API_KEY` 加载密钥，而非写入源码；
  - 插件鉴权配置需与调用方一致（如 Header Basic Auth），否则插件调用将失败。
- **版本兼容性**：
  - Java SDK 要求 ≥ 2.12.0（见文档 1 和 2）；
  - Python SDK 要求 ≥ 1.14.0（仅文档 3 明确提及，其他文档未标注，建议统一升级至最新稳定版）；
- **错误处理**：响应非 `200 OK` 时，务必检查 `response.status_code`、`response.message` 和 `response.request_id`，并参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code) 定位问题。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


