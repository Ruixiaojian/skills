# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP 接口，将已发布的百炼智能体应用（Agent 1.0）或工作流应用集成至第三方业务系统的能力。调用过程以 `app_id` 为唯一标识，支持同步文本生成、插件参数透传及基础调试能力，适用于轻量级 AI 能力嵌入场景。所有调用均需有效 API Key 和已发布应用 ID。

## 支持的模型/功能

- **核心模型**：调用本身不直接指定底层模型，而是由应用在百炼控制台中绑定的推理模型（如 `qwen-max`、`qwen-plus` 等）决定，见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)。
- **应用类型支持**：
  - 智能体应用（Agent 1.0）：支持 [prompt](prompt.md) 直接输入与 `biz_params` 参数透传；
  - 工作流应用（原“智能体编排应用”）：自 v2024.06 起替代旧版编排应用，同样支持 `biz_params`，但需注意其节点配置逻辑与智能体应用不同；详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。
- **扩展能力**：
  - 自定义插件参数透传（通过 `biz_params.user_defined_params.{plugin_code}` 结构）；
  - 调试信息返回（启用 `debug: {}` 可获取中间步骤日志，仅限调试环境）；
  - [Token](../concepts/token.md) 使用统计（响应中 `usage.models` 字段包含 `input_tokens`/`output_tokens` 及 `model_id`）。

> **注意**：文档 2 中称“智能体编排应用已被工作流应用替代”，但文档 1 未提及该术语变更，且当前控制台仍存在“智能体编排应用”入口。实际开发中请以控制台最新应用类型分类为准，避免混淆。建议优先使用 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) 中明确支持的工作流应用。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✓ | 百炼控制台应用管理页获取的唯一 ID，非模型 ID |
| `prompt` | string | ✓ | 用户输入的原始提示词，作为应用入口输入 |
| `biz_params` | object | ✗ | 用于透传业务参数，结构为 `{ "user_defined_params": { "{plugin_code}": { ... } } }`，仅对含自定义插件的应用生效 |
| `parameters` | object | ✗ | 当前暂无公开可用参数，保留字段，传空对象 `{}` 即可 |
| `debug` | object | ✗ | 启用调试模式，传 `{}` 即可获取 `debug_info` 字段（含工具调用链、中间结果等），生产环境请勿启用 |

> **注意**：`biz_params` 的结构和语义在两篇文档中一致，但文档 2 的 Java 示例中使用了 `JsonUtils.parse()` 解析字符串，而文档 1 的 Java 示例未体现该参数——这表明 SDK 对 `biz_params` 的支持依赖于较新版本（≥1.14.0）。请务必参考 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 中的 SDK 版本要求，并在实际项目中验证 `ApplicationParam.builder().bizParams(...)` 是否可用。

## 使用方式

### 1. 准备工作
- 获取 API Key：前往 [密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并复制；
- 获取 `app_id`：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 中复制目标应用卡片上的 ID；
- （推荐）配置环境变量：`export DASHSCOPE_API_KEY=sk-xxx`，避免代码硬编码。

### 2. SDK 调用（Python 示例）
```python
from dashscope import Application
import os

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？",
    biz_params={  # 仅当应用含插件时需设置
        "user_defined_params": {
            "plugin_abc123": {"article_index": 2}
        }
    }
)
if response.status_code == 200:
    print(response.output.text)
```

### 3. HTTP 调用（curl 示例）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "input": {
            "prompt": "你是谁？",
            "biz_params": {
                "user_defined_params": {
                    "plugin_abc123": {"article_index": 2}
                }
            }
        },
        "parameters": {},
        "debug": {}
      }'
```

完整语言支持见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)，包括 Java、Node.js、PHP、C#、Go。

## 限制和注意事项

- **调用频率与配额**：受百炼平台账户级 QPS 和 [Token](../concepts/token.md) 总量配额限制，超出将返回 `429 Too Many Requests`，具体阈值需在控制台查看；
- **超时时间**：HTTP 接口默认超时为 60 秒，SDK 默认行为一致，长流程应用建议自行设置 `timeout` 参数；
- **安全要求**：
  - 禁止在客户端（如浏览器 JS）直接暴露 `DASHSCOPE_API_KEY`；
  - 生产环境必须通过服务端代理调用，或使用阿里云 RAM 角色临时凭证（文档未覆盖，需另行查阅权限文档）；
- **错误处理**：
  - 所有失败响应均含 `request_id`，用于问题定位；
  - 错误码含义统一参考 [开发者参考错误码](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)；
- **插件参数约束**：
  - `user_defined_params` 中的 `plugin_code` 必须与控制台插件卡片显示的 ID 完全一致（区分大小写）；
  - 插件输入参数必须已在插件配置中声明为“业务透传”（Business Pass-through），否则会被忽略；
  - 多插件场景下，`user_defined_params` 可包含多个插件键值对。

如遇参数不生效、插件未触发等问题，请首先确认应用已重新发布，并检查 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) 中的插件配置步骤是否完整执行。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


