# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将阿里云百炼平台创建的智能体应用或工作流应用集成至第三方业务系统的能力。该机制统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义插件参数透传等核心能力，适用于从简单问答到复杂编排的各类 AI 应用场景。所有调用均需有效 API Key 和已发布的应用 ID。

## 支持的模型/功能

- **应用类型**：同时支持**智能体应用**（[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)）和**工作流应用**（[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）。文档 3 明确指出“智能体编排应用已被工作流应用替代”，因此新项目应优先选用工作流应用。
- **核心能力**：
  - 单轮文本生成（基础 [prompt](prompt.md) 输入）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 向关联插件传递业务参数）
- **模型绑定**：底层模型由应用发布时配置决定，调用方无需指定模型 ID；响应中 `usage.models[].model_id` 字段可回溯实际执行模型（如 `qwen-max`、`qwen-plus`）。

> **注意**：文档 2 明确声明“本文档仅适用于华北2（北京）地域”，而文档 1 和 3 均未注明地域限制。生产环境部署前请确认目标应用所在地域与 API 端点兼容性。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台应用卡片上复制的唯一 ID，区分智能体应用与工作流应用 |
| `prompt` | string | 否（若提供 `messages` 则不可用） | 单轮对话的用户输入文本；若启用多轮对话且使用 `messages`，则此项必须省略 |
| `messages` | array | 否（若提供则替代 `prompt`） | 按时间序排列的对话历史数组，格式为 `[{"role": "user/system/assistant", "content": "..."}]`；SDK 和 HTTP 均支持 |
| `session_id` | string | 否 | 用于启用云端会话存储的字符串标识；有效期 1 小时，最多支持 50 轮；若与 `messages` 同时存在，系统**优先使用 `messages`**（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)） |
| `biz_params` | object | 否 | 用于向应用内自定义插件透传参数，结构为 `{"user_defined_params": {"{plugin_code}": {...}}}`；详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |

## 使用方式

### 1. 前置准备
- 获取 API Key：前往 [密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并记录；
- 获取 `app_id`：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面复制目标应用卡片上的 ID；
- （推荐）配置环境变量：`export DASHSCOPE_API_KEY=sk-xxx`，避免代码硬编码。

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
  --header 'Content-Type: application/json' \
  --data '{
    "input": {
      "prompt": "你是谁？"
    }
  }'
```

### 4. 多轮对话（显式 messages）
```python
response = Application.call(
    app_id="YOUR_APP_ID",
    messages=[
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！有什么可以帮您？"},
        {"role": "user", "content": "今天天气如何？"}
    ]
)
```

### 5. 插件参数透传
```python
biz_params = {
    "user_defined_params": {
        "your_plugin_code": {"article_index": 2}
    }
}
response = Application.call(
    app_id="YOUR_APP_ID",
    prompt="查询寝室公约",
    biz_params=biz_params
)
```

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持华北2（北京）地域，智能体应用无明确限制，但建议统一部署于北京地域以确保兼容性（参见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）。
- **会话管理**：`session_id` 有效期为 1 小时且上限 50 轮；生产环境推荐自行维护 `messages` 数组以获得完全控制权。
- **安全实践**：API Key **严禁硬编码**，必须通过环境变量或密钥管理服务注入；所有 SDK 示例均强调此原则。
- **插件参数要求**：自定义插件的输入参数在控制台配置时，“传参方式”必须设为 **业务透传**，否则 `biz_params` 无法生效（见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）。
- **SDK 版本**：Java SDK 要求 ≥ 2.12.0（文档 1 & 2），Python SDK 要求 ≥ 1.14.0（文档 3），低版本可能缺失 `biz_params` 或 `messages` 支持。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


