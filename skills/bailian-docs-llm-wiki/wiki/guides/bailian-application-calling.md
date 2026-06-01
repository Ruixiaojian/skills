# bailian [application call](../api/application-call.md)ing

阿里云百炼平台支持通过 DashScope SDK 或 HTTP API 将**智能体应用**和**工作流应用**集成到业务系统中。开发者可以使用统一的 `Application.call` 接口完成应用调用，并支持多轮对话、自定义参数传递等高级功能。本文汇总了应用调用的核心流程、关键参数及注意事项。

## 支持的应用类型

百炼平台的应用调用主要涵盖两类应用：

- **智能体应用**：具备大模型推理能力，可关联插件工具，适用于对话、问答等场景。详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)。
- **工作流应用**：通过可视化编排节点实现复杂业务逻辑，已替代原有的智能体编排应用。详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。

> **注意**：工作流应用的文档明确标注"仅适用于中国大陆版（北京地域）"，而智能体应用文档未提及此限制。请根据实际部署地域确认可用性。

## 前提条件

无论调用哪种应用类型，都需要完成以下准备工作：

1. **获取 API Key**：在百炼控制台的[密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key)页面创建。
2. **配置 API Key 到环境变量**（推荐）：避免在代码中硬编码，SDK 会自动从 `DASHSCOPE_API_KEY` 环境变量读取。
3. **获取应用 ID（APP_ID）**：在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面的应用卡片上复制。
4. **安装 DashScope SDK**（若使用 SDK 调用）：
   - Python: `python3 -m pip install -U dashscope`
   - Java: 在 `pom.xml` 中添加 `com.alibaba:dashscope-sdk-java` 依赖（建议版本 >= 2.12.0）

## 调用方式

### 支持的语言与协议

两类应用均支持以下调用方式：**Python SDK**、**Java SDK**、**HTTP（curl / PHP / Node.js / C# / Go）**。

### API 端点

所有应用统一使用以下端点：

```
POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion
```

请求头需包含：
```
Authorization: Bearer $DASHSCOPE_API_KEY
Content-Type: application/json
```

### 基本调用示例（Python）

```python
import os
from http import HTTPStatus
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='你是谁？')

if response.status_code != HTTPStatus.OK:
    print(f'request_id={response.request_id}')
    print(f'code={response.status_code}')
    print(f'message={response.message}')
else:
    print(response.output.text)
```

智能体应用与工作流应用的基本调用方式完全一致，仅需替换对应的 `APP_ID`。

## 关键参数

| 参数 | 说明 | 适用场景 |
|------|------|----------|
| `app_id` | 应用 ID，从控制台获取 | 所有调用 |
| `prompt` | 用户输入的提示文本 | 单轮对话、基本调用 |
| `session_id` | 会话 ID，用于云端存储多轮对话历史 | 多轮对话（简单模式） |
| `messages` | 自行维护的对话历史数组 | 多轮对话（推荐模式） |
| `biz_params` | 业务参数，用于自定义插件参数传递 | 自定义插件调用 |

## 多轮对话

多轮对话支持两种方式：

- **`session_id` 模式**：系统自动从云端加载对话历史，实现简单，无需维护。有效期 1 小时，最多 50 轮。
- **`messages` 模式（推荐）**：自行维护对话历史数组，控制灵活。工作流应用使用此模式时，需在大模型节点配置提示词变量 `historyList` 并发布应用。

> **注意**：若请求中同时包含 `session_id` 和 `messages`，系统将优先使用 `messages`。

## 自定义参数传递

当应用中使用了自定义插件时，可通过 `biz_params` 中的 `user_defined_params` 字段传递插件参数。详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

### 关键步骤

1. **创建自定义插件**：在控制台创建插件，输入参数的**传参方式**必须选择**业务透传**。
2. **关联应用**：将插件关联到智能体应用，或在工作流应用中通过插件节点引用。
3. **API 调用时传递参数**：

```python
biz_params = {
    "user_defined_params": {
        "your_plugin_code": {    # 替换为实际的插件 ID
            "article_index": 2   # 替换为实际的插件参数
        }
    }
}

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='寝室公约内容',
    biz_params=biz_params)
```

HTTP 调用时，`biz_params` 置于 `input` 对象内：

```json
{
    "input": {
        "prompt": "寝室公约内容",
        "biz_params": {
            "user_defined_params": {
                "{your_plugin_code}": {
                    "article_index": 2
                }
            }
        }
    }
}
```

### 插件配置要点

- **插件描述**：使用自然语言描述插件用途，帮助大模型判断是否需要调用该插件。
- **工具描述**：描述工具功能和使用场景，尽量给出使用示例。
- **参数名称**：尽可能带有语义，帮助大模型理解需要识别的参数。
- **参数描述**：简练准确，帮助大模型理解取参方式。
- 插件工具只能与位于**相同业务空间**的智能体应用关联。

## 限制和注意事项

- `session_id` 有效期为 **1 小时**，最多支持 **50 轮**对话。
- 工作流应用文档标注仅适用于**中国大陆版（北京地域）**。
- 不建议在生产环境中将 API Key 硬编码到代码中，应通过环境变量配置。
- 插件 ID 可在百炼控制台的插件卡片上获取。
- 自定义插件如需鉴权，需在创建时打开**是否鉴权**开关并填写鉴权配置。
- 响应结构统一包含 `output.text`（回复文本）、`output.session_id`、`output.finish_reason` 以及 `usage`（token 用量）和 `request_id`。

## 来源文档

- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)

