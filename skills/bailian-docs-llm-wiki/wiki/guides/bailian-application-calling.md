# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将阿里云百炼平台创建的智能体应用（Agent 1.0）或工作流应用集成至第三方业务系统的开发能力。该机制统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义插件参数透传及调试信息返回，是生产环境集成的核心方式。所有调用均需有效 API Key 和已发布的应用 ID。

## 支持的模型/功能

- **应用类型**：同时支持 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)（Agent 1.0）和 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)，二者调用接口、参数结构与响应格式完全一致。
- **核心能力**：
  - 单轮文本生成（`prompt` 输入）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 传递插件入参）
  - 调试信息输出（启用 `debug` 字段可获取执行路径、节点耗时等）
- **模型绑定**：底层实际调用的模型由应用在控制台配置决定（如 `qwen-max`、`qwen-plus`），API 层不暴露模型选择参数；[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) 文档明确指出该能力适用于两类应用，且“智能体编排应用已被工作流应用替代”，表明功能已收敛。

> **注意**：文档 2 明确声明“本文档仅适用于华北2（北京）地域”，而文档 1 和 3 均未提及地域限制。实际调用时若在非北京地域失败，应优先检查地域合规性。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台应用卡片上复制的 APP_ID，区分智能体与工作流应用 |
| `prompt` | string | 否（但 `input.messages` 或 `biz_params` 至少需其一） | 单轮指令文本；若使用 `messages` 数组则此项忽略 |
| `input.prompt` | string | 同上 | HTTP 方式下位于 `input` 对象内 |
| `input.messages` | array | 否（推荐用于多轮） | 消息数组，格式为 `[{"role": "user", "content": "..."}, ...]`，替代 `prompt` |
| `session_id` | string | 否 | 云端维护对话历史的会话标识，有效期 1 小时，最多 50 轮 |
| `biz_params.user_defined_params` | object | 否 | 传递自定义插件参数，结构为 `{"plugin_code": {"param_key": "value"}}`，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |
| `debug` | object | 否 | 空对象 `{}` 即可启用调试模式，返回详细执行日志 |

## 使用方式

### 1. 准备工作
- 获取 API Key：前往 [密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并记录；
- 获取 APP_ID：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面复制目标应用的 ID；
- （推荐）配置环境变量：`export DASHSCOPE_API_KEY=sk-xxx`，避免代码硬编码。

### 2. SDK 调用（Python 示例）
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

### 3. HTTP 调用（curl 示例）
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

### 4. 多轮对话（推荐 `messages` 方式）
```python
response = Application.call(
    api_key=...,
    app_id=...,
    input={  # 注意：SDK v2+ 支持直接传 input 字典
        "messages": [
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "我是千问"},
            {"role": "user", "content": "今天天气如何？"}
        ]
    }
)
```

## 限制和注意事项

- **地域限制**：工作流应用调用强制要求华北2（北京）地域，智能体应用虽未明示，但为兼容性建议统一部署在北京地域。
- **会话管理**：`session_id` 有效期为 1 小时，超时后需新建会话；若请求中同时存在 `session_id` 和 `messages`，系统**优先使用 `messages`**（文档 2 明确说明）。
- **插件参数安全**：`biz_params.user_defined_params` 中的插件 ID（`plugin_code`）必须与控制台中插件卡片显示的 ID 完全一致，且插件需已发布并关联至目标应用。
- **错误处理**：所有语言示例均展示对 `status_code != 200` 的基础处理，并建议查阅 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。
- **SDK 版本**：Java 示例注明“建议 >= 2.12.0”，Python 示例未指定，但 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 文档中 Python SDK 安装命令隐含要求最新版；若遇到 `biz_params` 不生效，请先升级 SDK。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


