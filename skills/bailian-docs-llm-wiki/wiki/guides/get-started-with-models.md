# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过标准化 API 快速集成千问（Qwen）及第三方模型。开发者只需完成账号开通、API Key 配置和 Base URL 设置，即可调用文本生成、[多模态](../concepts/multimodal.md)等能力。本文档聚焦首次调用的核心路径，涵盖模型选择、参数配置、调用方式及关键限制。

## 支持的模型/功能

百炼提供覆盖[多模态](../concepts/multimodal.md)的模型服务，包括文本生成、视觉理解、图像生成、语音识别与合成、嵌入向量等。文本生成类模型以千问（Qwen）系列为主，当前主力推荐如下：

- **`qwen3.8-max`**：旗舰模型，适合复杂、多步骤任务，推理能力全面超越前代；
- **`qwen3.7-plus`**：效果、速度与成本均衡，是多数生产场景的**推荐选择**；
- **`qwen3.7-flash`**：高性价比、低延迟，适合简单任务与高频响应场景。

除千问外，平台还支持 DeepSeek、Kimi、GLM 等主流第三方模型。所有模型均按地域独立部署，不同地域支持的模型列表存在差异，例如 DeepSeek 仅在华北2（北京）地域可用 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。完整模型清单及上下文长度等规格，请参见[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

> **注意**：文档 3 中列出的 `qwen3.7-flash` 模型在“美国（弗吉尼亚）”地域的 Base URL 格式与其他地域不一致（使用 `dashscope-us.aliyuncs.com` 而非 `{WorkspaceId}.us-east-1.maas.aliyuncs.com`），且未明确要求 WorkspaceId；而文档 6 和文档 7 均指出美国地域需使用业务空间专属域名（含 WorkspaceId）。该矛盾表明美国地域的 `qwen3.7-flash` 在文档 3 中的 URL 示例可能已过时，实际调用应以[选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)为准。

## 关键参数

调用模型必需以下三个核心参数，缺一不可：

- **API Key**：用于身份鉴权，需在[阿里云百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)创建。建议配置为环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露风险 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。
- **Base URL**：模型服务入口地址，**必须与 API Key 所属地域严格匹配**。各地域提供三种域名类型：
  - *业务空间专属域名*（推荐）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，需先在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)中获取 WorkspaceId；
  - *Dashscope 域名*（兼容）：如 `https://dashscope.aliyuncs.com/compatible-mode/v1`，适用于存量迁移；
  - *试用域名*：如 `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，限流严格，仅限验证。
- **Model ID**：字符串形式的模型标识符，如 `"qwen3.8-max"`。模型 ID 与 Base URL 的地域和服务部署范围强绑定，跨地域使用将返回 401 错误。

## 使用方式

### 1. 环境准备
- 完成阿里云账号注册、实名认证及百炼服务开通；
- 创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`（Linux/macOS 推荐写入 `~/.bashrc` 或 `~/.zshrc`；Windows 推荐通过系统属性设置）；
- 确认 Python 版本 ≥ 3.8，并安装 SDK：`pip install -U openai`（OpenAI 兼容）或 `pip install -U dashscope`（DashScope SDK）。

### 2. 发起调用（OpenAI SDK 示例）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://llm-xxx.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId 和地域
)

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```

支持语言不限于 Python，Node.js、curl 等方式同样可用，详见[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

### 3. 域名迁移建议
新项目应直接使用**业务空间专属域名**，其具备更高并发承载能力、网络隔离性及 SLA 保障（99.9%）。从 Dashscope 域名迁移仅需替换 Base URL，无需修改业务逻辑代码 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

## 限制和注意事项

- **地域隔离**：API Key、Base URL、模型列表三者严格绑定地域，**不可跨地域混用**。例如华北2（北京）的 Key 无法调用新加坡地域的模型。
- **动态限流**：部分模型（如 `qwen3.8-max`）采用动态限流机制，TPM 限流值按账号月消费金额分档调整（如北京地域 ≤10w 档为 500w TPM），且实际可用值不低于档位值 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)。
- **静态限流**：非动态限流模型遵循固定 RPM/TPM 阈值（如 `qwen3.8-max` 在北京地域为 30,000 RPM / 5,000,000 TPM），超限返回 429 错误。RPM/TPM 按主账号维度合并计算，子账号、所有业务空间和 API Key 共享同一配额 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。
- **免费额度与计费**：新用户享有北京地域专属免费额度，用完后可自动转为按量付费（已认证用户）或需手动充值（未认证用户）。务必开启“免费额度用完即停”开关以防意外扣费 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。
- **[Token](../concepts/token.md) Plan/Coding Plan 数据条款**：使用 [Token](../concepts/token.md) Plan 个人版或 Coding Plan 时，输入及输出内容将用于服务改进，**不适用“数据不用于训练”的隐私承诺**，请务必审阅对应服务协议 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 来源文档

- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)


