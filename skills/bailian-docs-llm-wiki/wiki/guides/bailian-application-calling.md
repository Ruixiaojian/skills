# bailian [application call](../api/application-call.md)ing

百炼平台支持通过统一的 Application API 调用多种类型的应用（工作流应用、智能体应用），开发者可使用 DashScope SDK 或标准 HTTP 接口快速集成。该能力屏蔽底层模型与编排细节，提供一致的调用契约，适用于对话生成、插件协同、多轮会话等场景。所有调用均需在华北2（北京）地域执行。

## 支持的模型/功能

- **应用类型**：当前支持两类应用：
  - **工作流应用**（Workflow Application）：基于可视化节点编排（如大模型节点、条件分支、插件节点等）构建的复杂逻辑应用，适用于需多步骤决策或外部系统集成的场景 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
  - **智能体应用**（Single Agent Application）：基于单一大模型驱动、支持插件调用的轻量级智能体，适用于快速构建具备工具调用能力的助手 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)。
- **核心能力**：
  - 单轮文本生成（`prompt` 输入）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）
  - 自定义插件参数透传（`biz_params.user_defined_params`）[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
  - 调试信息返回（`debug` 字段）

> **注意**：文档 1 明确声明“本文档仅适用于华北2（北京）地域”，而文档 2 和 3 均未提及地域限制。实际生产环境必须严格遵循文档 1 的地域要求，否则请求将失败。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在控制台「应用管理」页面获取。文档 1 和文档 2 使用 `APP_ID` 占位符，文档 3 使用 `YOUR_APP_ID`，语义一致。 |
| `prompt` | string | 否（若提供 `messages` 则非必填） | 用户输入的自然语言指令。当使用 `messages` 进行多轮对话时，此字段被忽略。 |
| `messages` | array | 否（若提供则替代 `prompt`） | 消息数组，格式为 `[{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]`，用于精确控制上下文。 |
| `session_id` | string | 否 | 由服务端维护的会话 ID，有效期 1 小时，最多支持 50 轮。若同时提供 `session_id` 和 `messages`，系统优先使用 `messages`。 |
| `biz_params` | object | 否 | 用于传递自定义插件参数，结构为 `{"user_defined_params": {"<plugin_code>": {"param_key": "param_value"}}}`。仅在关联了自定义插件的应用中生效。 |
| `parameters` | object | 否 | 预留扩展字段，当前暂未开放用户可配置的模型超参。 |
| `debug` | object | 否 | 空对象 `{}` 即可启用调试模式，返回更详细的执行链路信息（如插件调用日志、节点耗时）。 |

## 使用方式

### 1. 前置准备
- 获取并配置 `DASHSCOPE_API_KEY` 至环境变量（推荐），避免硬编码 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
- 确保应用已发布，且 `app_id` 正确无误。
- （SDK 方式）安装对应语言的 DashScope SDK，Python 推荐 ≥1.14.0，Java 推荐 ≥2.12.0。

### 2. 调用示例（以 Python SDK 为例）
```python
from dashscope import Application
import os

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？",
    # 多轮对话（显式 messages）
    # messages=[{"role": "user", "content": "你好"}, {"role": "assistant", "content": "我是通义千问"}],
    # 插件参数透传
    # biz_params={"user_defined_params": {"plugin_abc123": {"query": "天气"}}}
)

if response.status_code == 200:
    print(response.output.text)
else:
    print(f"Error {response.status_code}: {response.message}")
```

### 3. HTTP 接口（通用）
- **Endpoint**: `POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`
- **Headers**: 
  - `Authorization: Bearer <your_api_key>`
  - `Content-Type: application/json`
- **Body**:
  ```json
  {
    "input": {
      "prompt": "你是谁？",
      "biz_params": { /* 可选 */ }
    },
    "parameters": {},
    "debug": {}
  }
  ```

## 限制和注意事项

- **地域限制**：所有调用必须在 **华北2（北京）** 地域发起，跨地域请求将返回 403 错误。这是硬性约束，不可绕过。
- **会话管理**：
  - `session_id` 由服务端生成并返回在响应中（`output.session_id`），客户端需自行保存并在后续请求中复用。
  - `session_id` 有效期为 1 小时，超时后需新建会话；单个会话最多承载 50 轮交互。
- **安全实践**：
  - 绝对禁止在代码中硬编码 `DASHSCOPE_API_KEY`，必须通过环境变量或密钥管理服务注入。
  - 生产环境应配置 API Key 的访问策略（如 IP 白名单、权限最小化）。
- **插件参数**：
  - `biz_params.user_defined_params` 中的 `plugin_code` 必须与控制台中插件卡片显示的 ID 完全一致（区分大小写）。
  - 插件工具的输入参数在创建时必须设置为 **业务透传**（Business Pass-through），否则无法通过 API 传递。
- **错误处理**：所有失败响应均包含 `request_id`，可用于问题定位；详细错误码请查阅 [开发者参考错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


