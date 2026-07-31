# bailian [application call](../api/application-call.md)ing

百炼应用调用是指通过 DashScope SDK 或标准 HTTP API，将已发布的百炼智能体应用或工作流应用集成至第三方业务系统。调用过程统一使用 `POST /api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话及自定义插件参数透传，适用于各类 AI 增强型业务场景。

## 支持的模型/功能

- **应用类型**：同时支持[智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)和[工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)，二者调用方式完全一致（SDK `Application.call()` 或 HTTP `POST /completion`）。
- **核心能力**：
  - 单轮文本生成（`prompt` 字段）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 传递插件入参）
- **底层模型**：由应用发布时绑定的模型自动执行，不需调用方指定；响应中 `usage.models[].model_id` 字段可查实际使用的模型（如 `qwen-max`、`qwen-plus`）。

> **注意**：文档 2 明确声明“本文档仅适用于华北2（北京）地域”，而文档 1 和文档 3 均未限定地域。实际调用时若在非北京地域失败，请优先检查地域合规性——该限制属于服务端部署约束，非 SDK 层面兼容性问题。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✓ | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 |
| `prompt` | string | ✓（单轮） | 用户输入的自然语言指令；若使用 `messages` 则此项可省略 |
| `biz_params` | object | ✗ | 用于传递自定义插件参数，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }`，详见[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |
| `session_id` | string | ✗ | 启用云端会话管理时必填；有效期 1 小时，最多支持 50 轮对话 |
| `messages` | array | ✗ | 替代 `prompt` 的推荐方式，格式同 OpenAI：`[{ "role": "user/system/assistant", "content": "..." }]`；若与 `session_id` 同时存在，以 `messages` 为准 |

## 使用方式

### 1. 准备工作
- 获取 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key) 并配置为环境变量 `DASHSCOPE_API_KEY`
- 在控制台创建应用并复制 `APP_ID`
- （SDK 方式）安装对应语言 SDK：Python (`pip install -U dashscope`)、Java（Maven/Gradle 依赖）、Node.js（`npm install axios`）等

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

### 3. HTTP 直接调用（curl）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "input": {
      "prompt": "你是谁？"
    }
  }'
```

### 4. 多轮对话（推荐 `messages` 方式）
```python
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    messages=[
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！有什么可以帮您？"},
        {"role": "user", "content": "今天天气如何？"}
    ]
)
```

## 限制和注意事项

- **地域限制**：工作流应用调用[仅支持华北2（北京）地域](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)，智能体应用无此限制，但建议统一部署在北京地域以确保兼容性。
- **安全实践**：API Key **严禁硬编码**，必须通过环境变量（如 `DASHSCOPE_API_KEY`）注入；SDK 默认读取该变量。
- **参数冲突**：当请求同时包含 `session_id` 和 `messages` 时，系统优先采用 `messages`，忽略云端历史（[工作流应用文档](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)明确说明）。
- **插件参数**：自定义插件参数必须通过 `biz_params.user_defined_params` 传递，且插件工具配置中“传参方式”必须设为 **业务透传**，否则参数无法到达插件后端。
- **错误处理**：所有调用均需检查 `status_code`（HTTP 状态码）和 `response.message`，错误码详情见[开发者参考文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


