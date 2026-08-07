# bailian [application call](../api/application-call.md)ing

百炼应用调用是将阿里云百炼平台构建的智能体应用或工作流应用集成至业务系统的标准方式，支持通过 DashScope SDK 或原生 HTTP API 进行同步调用。所有调用均统一使用 `/api/v1/apps/{app_id}/completion` 接口，无需区分应用类型底层实现，但需注意不同应用类型对参数和能力的支持差异。

## 支持的模型/功能

- **应用类型**：支持两类应用——[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)（Agent 1.0）与[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)，后者已替代旧版“智能体编排应用”。
- **核心能力**：
  - 单轮文本生成（`prompt` 输入）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）
  - 自定义插件参数透传（仅限已关联插件的智能体/工作流应用，详见[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）
- **模型绑定**：应用在控制台发布时已绑定后端模型（如 `qwen-max`、`qwen-plus`），调用时**不可动态指定模型**；模型信息仅在响应 `usage.models[].model_id` 中返回，用于计费与调试。

> **注意**：文档2明确声明“本文档仅适用于华北2（北京）地域”，而文档1与文档3未限定地域。实际调用时若在非北京地域遇到 `404 Not Found` 或 `InvalidRegionId` 错误，请确认应用部署地域并使用对应 endpoint —— 当前生产环境统一使用 `https://dashscope.aliyuncs.com`，其路由由服务端自动调度，开发者无需手动切换域名。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✅ | 百炼控制台应用卡片中复制的唯一 ID，区分智能体与工作流应用 |
| `prompt` | string | ⚠️（见下文） | 单轮请求必需；若使用 `messages` 进行多轮对话，则**不可同时传 `prompt`** |
| `messages` | array | ⚠️（见下文） | 多轮对话推荐方式，格式为 `[{ "role": "user/system/assistant", "content": "..." }]`；若同时传 `prompt` 和 `messages`，SDK 与 HTTP 接口均以 `messages` 为准 |
| `session_id` | string | ❌ | 云端托管对话历史，有效期 1 小时、最多 50 轮；与 `messages` 冲突时优先使用 `messages` |
| `biz_params` | object | ❌ | 用于透传自定义插件参数，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }`，详见[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |

## 使用方式

### 1. 前置准备
- 获取 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key) 并配置为环境变量 `DASHSCOPE_API_KEY`（**强烈推荐**，避免硬编码）；
- 获取目标应用的 `app_id`（[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面）；
- 若使用 SDK：安装对应语言版本（Python ≥1.14.0，Java ≥2.12.0），参考 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 中的依赖配置。

### 2. 调用示例（Python SDK）
```python
from dashscope import Application
import os

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 自动读取环境变量
    app_id="YOUR_APP_ID",
    prompt="你是谁？",
    # 多轮场景（推荐）：
    # messages=[{"role": "user", "content": "你好"}],
    # biz_params={"user_defined_params": {"plugin_abc123": {"query": "天气"}}}
)

if response.status_code == 200:
    print(response.output.text)
else:
    print(f"Error {response.status_code}: {response.message}")
```

### 3. HTTP 直接调用（curl）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "input": {
          "prompt": "你是谁？"
          // "messages": [...],  // 替代 prompt
          // "biz_params": {...} // 插件参数
        }
      }'
```

## 限制和注意事项

- **地域限制**：工作流应用调用[仅支持华北2（北京）地域](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)，智能体应用无此限制；跨地域调用将失败。
- **并发与配额**：受账号级 QPS 与 [Token](../concepts/token.md) 配额限制，具体数值请查阅控制台配额管理页；超限返回 `429 Too Many Requests`。
- **安全要求**：
  - 禁止在代码中硬编码 `api_key`，必须通过环境变量或密钥管理服务注入；
  - 插件鉴权配置（如 Basic Auth）需在插件创建时完成，`biz_params` 仅透传业务参数，不参与鉴权流程。
- **调试建议**：
  - 开启 `debug` 字段（HTTP 请求中设 `"debug": {}`）可获取更详细的执行链路日志；
  - 所有错误均返回 `request_id`，用于工单排查，错误码含义参考 [开发者参考文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

> **注意**：文档2中“多轮对话”章节的 Python 示例代码被截断（末尾为 `if response.status_code != HTTPStatus.OK:` 后无内容），实际应参考文档1中完整示例；该处为原文笔误，非功能性差异。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


