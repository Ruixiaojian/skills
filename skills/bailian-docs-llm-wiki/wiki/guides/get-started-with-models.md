# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过 OpenAI 兼容 API、DashScope SDK 等方式快速调用千问（Qwen）及第三方模型。本文面向开发者，聚焦模型接入的核心路径：从环境准备、模型选择到实际调用，涵盖关键参数、地域与域名约束、限流机制等生产必需信息。所有操作均基于真实控制台逻辑和最新接口规范。

## 支持的模型与功能

百炼提供覆盖文本、[多模态](../concepts/multi-modal.md)、领域专用的全系列模型，核心推荐如下（以华北2北京地域为准）：

- **`qwen3.8-max`**：Qwen 系列效果最强模型，适合复杂多步骤任务；[原文标题](../../raw/model-user-guide/get-started-with-models/models.md) 明确其为“推理能力全面超越前代，推荐选用”。
- **`qwen3.7-plus`**：效果、速度与成本均衡，是多数场景的**推荐选择**。
- **`qwen3.7-flash`**：高性价比、低延迟，适合简单高频任务。

除千问外，还支持 DeepSeek、Kimi、GLM 等第三方模型（部分仅限北京地域）。模型能力覆盖文本生成、视觉理解、图像/视频生成、语音识别与合成、嵌入向量等。细分领域模型（如法律、意图理解、长文本处理）亦可直接调用。

> **注意**：文档 3 中列出的 `qwen3.7-flash` 在文档 7 的限流表中实际对应 `qwen3.7-flash`（RPM 30,000 / TPM 5,000,000），但文档 7 同时存在 `qwen3.7-flash-2026-07-15` 等快照版本（限流更严格）。开发者应优先使用无日期后缀的稳定版模型 ID，避免因快照版本限流骤降导致服务不稳定。

## 关键参数

调用模型必需配置以下参数，缺一不可：

- **`DASHSCOPE_API_KEY`**：在 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key) 页面创建，**按地域独立**，不可跨地域复用。
- **`base_url`**：模型服务接入地址，**必须与 API Key 所属地域及计费方案严格匹配**。常见组合：
  - **业务空间专属域名（推荐生产使用）**：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，其中 `{WorkspaceId}` 需从 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取。
  - **DashScope 域名（兼容存量）**：`https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）、`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`（新加坡）等。
  - **试用域名（仅限验证）**：`https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，TPM 限流极低。
- **`model`**：模型 ID，如 `"qwen3.8-max"`，需与所选地域支持的模型列表一致（参见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)）。
- **`messages`**：符合 OpenAI Chat Completions 格式的对话数组，`role` 为 `"system"`/`"user"`/`"assistant"`，`content` 为字符串。

## 使用方式

### 1. 环境准备
- **注册与开通**：使用阿里云主账号注册并开通百炼服务，完成实名认证 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。
- **获取凭证**：在控制台获取 `DASHSCOPE_API_KEY` 和 `WorkspaceId`（若使用业务空间专属域名）。
- **配置 API Key**：强烈建议将 `DASHSCOPE_API_KEY` 设为环境变量（如 `export DASHSCOPE_API_KEY="sk-xxx"`），避免硬编码 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 2. SDK 选择与调用
支持 OpenAI Python SDK 和 DashScope Python SDK：

```python
# OpenAI SDK 示例（推荐）
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId
)

response = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(response.choices[0].message.content)
```

> **注意**：文档 2 中 Node.js 示例的 `baseURL` 写法为 `new OpenAI({ apiKey, baseURL })`，而文档 1 的 Python 示例使用 `OpenAI(api_key=..., base_url=...)`。两者语法正确，但需确保 SDK 版本兼容（OpenAI >= 1.0）。旧版 `openai==0.28` 不支持 `base_url` 参数，必须升级。

### 3. 多语言与 curl
除 Python 外，Node.js、Java、Go 等均有官方或社区 SDK 支持。`curl` 调用示例如下：
```bash
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3.8-max","messages":[{"role":"user","content":"你是谁？"}]}'
```

## 限制和注意事项

- **地域隔离**：API Key、`base_url`、模型列表均按地域独立。北京、新加坡、德国法兰克福、日本东京、美国弗吉尼亚五地**不能混用**。例如，北京地域的 Key 无法调用新加坡的模型 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。
- **限流机制**：
  - **账号级聚合**：限流按主账号维度计算，RAM 子账号、所有业务空间和 API Key 的调用量合并计入 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。
  - **RPM/TPM 双重限制**：每分钟调用次数（RPM）和每分钟 [Token](../concepts/token.md) 消耗（TPM）任一超限即触发 429 错误。`qwen3.8-max`（北京）默认为 RPM 30,000 / TPM 5,000,000 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。
  - **动态限流**：对 `qwen3.8-max` 等模型，TPM 限流值随百炼月消费金额分档调整（如北京地域 ≤10w 档为 500w TPM），每月 15 日生效 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)。
- **生产建议**：
  - **域名选择**：生产环境务必使用**业务空间专属域名**，其 SLA 99.9%、超时 3600 秒、支持 WebSocket/WebRTC，远优于 DashScope 域名（600 秒超时）和试用域名（无 SLA） [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。
  - **错误处理**：捕获 `APIStatusError` 并检查 `status_code == 429` 实现自动降级（如切换备用模型） [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。
  - **费用控制**：新用户可启用“免费额度用完即停”，避免意外扣费；长期运行需设置费用告警 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 来源文档

- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)


