# bailian [application call](../api/application-call.md)ing

百炼应用调用是将百炼平台构建的智能体应用（Agent）和工作流应用（Workflow）集成至业务系统的标准方式，支持通过 DashScope SDK 或原生 HTTP API 发起请求。所有调用均基于统一的 `/api/v1/apps/{app_id}/completion` 接口，适用于华北2（北京）地域，且需使用有效的 API Key 和已发布的 APP_ID。

## 支持的模型/功能

- **应用类型**：同时支持**智能体应用**（[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)）和**工作流应用**（[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）。文档明确指出“智能体编排应用已被工作流应用替代”，因此新项目应优先选用工作流应用。
- **核心能力**：
  - 单轮问答与多轮对话（通过 `session_id` 或显式 `messages` 实现）
  - 自定义插件参数透传（仅限智能体应用及工作流应用中的插件节点，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）
  - 调试信息返回（通过 `debug` 字段启用）
- **底层模型**：响应中 `usage.models[].model_id` 字段（如 `qwen-max`、`qwen-plus`）表明实际执行模型由应用配置决定，调用方无需指定；SDK/API 不暴露模型切换参数。

> **注意**：文档 1 明确声明“本文档仅适用于华北2（北京）地域”，而文档 3 未提及地域限制。生产环境必须遵循文档 1 的地域约束，否则请求将失败。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✓ | 应用在百炼控制台「应用管理」中生成的唯一 ID，非模型 ID |
| `prompt` | string | ✓（除 `messages` 模式外） | 用户输入文本；若使用 `messages` 多轮模式则可省略 |
| `biz_params` | object | ✗ | 用于向插件节点透传参数，结构为 `{ "user_defined_params": { "<plugin_code>": { ... } } }`（见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)） |
| `session_id` | string | ✗ | 启用云端会话管理，有效期 1 小时，最多 50 轮；与 `messages` 共存时以 `messages` 为准 |
| `messages` | array | ✗ | 替代 `prompt` 的多轮格式，如 `[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]`；推荐自行管理上下文 |
| `parameters` | object | ✗ | 预留扩展字段，当前无公开可用参数 |
| `debug` | object | ✗ | 设为空对象 `{}` 可启用调试输出（如 token 详细拆分），用于问题排查 |

## 使用方式

### 前提条件
- 获取并配置 `DASHSCOPE_API_KEY` 环境变量（[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）
- 在百炼控制台创建应用并获取 `APP_ID`（[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)）
- SDK 用户需安装对应语言 SDK（Python: `pip install -U dashscope`；Java: 引入 `dashscope-sdk-java` ≥2.12.0）

### 调用示例（Python SDK）
```python
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？",
    # 多轮对话（推荐）：
    # messages=[{"role": "user", "content": "你好"}],
    # 插件参数透传：
    # biz_params={"user_defined_params": {"plugin_abc123": {"query": "2024年报"}}}
)
if response.status_code == 200:
    print(response.output.text)
```

### HTTP 请求（curl）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "input": {
          "prompt": "你是谁？",
          "biz_params": {"user_defined_params": {"plugin_xyz789": {"id": 42}}}
        }
      }'
```

## 限制和注意事项

- **地域限制**：所有调用必须在**华北2（北京）地域**发起，跨地域请求将返回错误（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）。
- **会话管理**：
  - `session_id` 有效期为 1 小时，超时后历史上下文丢失；
  - 若同时提供 `session_id` 和 `messages`，系统**强制忽略 `session_id`**，仅使用 `messages`（文档 1 明确说明）。
- **安全实践**：
  - 禁止在代码中硬编码 `DASHSCOPE_API_KEY`，必须通过环境变量或密钥管理服务注入；
  - 生产环境应配置 API Key 权限策略，遵循最小权限原则。
- **插件参数兼容性**：`biz_params.user_defined_params` 仅对关联了自定义插件的**智能体应用**或含插件节点的**工作流应用**生效；普通 LLM 应用忽略该字段。
- **错误处理**：所有 SDK 和 HTTP 响应均包含 `request_id`，务必记录该字段用于问题定位（参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)）。

## 来源文档

- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)


