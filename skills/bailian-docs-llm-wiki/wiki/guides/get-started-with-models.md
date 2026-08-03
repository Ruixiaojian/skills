# get started with models

阿里云百炼提供开箱即用的大模型 API 服务，支持通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)、DashScope SDK 等方式快速调用千问（Qwen）及第三方模型。本文面向开发者，聚焦模型调用的起点：从环境准备、模型选择到首次请求的完整链路，不涉及应用构建或可视化界面操作。所有步骤均基于生产就绪实践提炼。

## 支持的模型与功能

百炼当前提供覆盖文本、多模态及领域专用的全系列模型，核心推荐如下（以华北2北京地域为准）：

- **qwen3.8-max**：效果最优，适合复杂推理任务；[原文标题](../../raw/model-user-guide/get-started-with-models/models.md) 中明确标注其为“Qwen 系列效果最好的模型”。
- **qwen3.7-plus**：效果、速度与成本均衡，是多数场景的**推荐选择**；该结论在 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 中被反复强调。
- **qwen3.7-flash**：高性价比、低延迟，适用于简单任务的高频调用。

除千问外，平台还支持 DeepSeek、Kimi、GLM 等第三方模型（部分仅限北京地域）。所有模型均提供 OpenAI 兼容、Anthropic 兼容及 DashScope 原生三种接入协议，且覆盖文本生成、嵌入向量、视觉理解等能力。

> **注意**：文档 3（`models.md`）中列出的 `qwen3.7-plus` 在多个地域的 Base URL 格式一致，但文档 2（`what-is-model-studio.md`）示例代码中使用了 `qwen3.7-plus`，而文档 6（`rate-limit.md`）表格中大量出现的是 `qwen-plus`（无版本号）及其带日期后缀的变体（如 `qwen-plus-2025-07-28`）。实际调用时应以控制台[模型广场](https://bailian.console.aliyun.com/?tab=model#/model-market)或 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 文档中最新发布的模型 ID 为准，避免使用已下线的快照版本。

## 关键参数

调用模型必需的三个核心参数为：

- **API Key**：在 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key) 页面创建，需配置为环境变量 `DASHSCOPE_API_KEY`（推荐永久配置，详见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)）。
- **Base URL**：必须与 API Key 所属地域和计费方案严格匹配。生产环境**强烈推荐使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），而非 DashScope 共享域名（如 `dashscope.aliyuncs.com`），因其提供更高吞吐与流量隔离。
- **Model ID**：必须与所选 Base URL 的地域和服务部署范围兼容。例如，美国弗吉尼亚地域的 `qwen3.7-plus-us` 不可在新加坡 Base URL 下调用。

## 使用方式

### 1. 环境准备
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，在控制台获取 API Key 和业务空间 ID（WorkspaceId）；
- 将 `DASHSCOPE_API_KEY` 配置为系统环境变量（Linux/macOS 推荐写入 `~/.bashrc` 或 `~/.zshrc`；Windows 推荐通过系统属性设置）。

### 2. SDK 选择与安装
- **OpenAI Python SDK**（推荐）：`pip install -U openai`，兼容性好，迁移成本低；
- **DashScope Python SDK**：`pip install -U dashscope`，提供更底层的控制能力。

### 3. 发起请求（OpenAI SDK 示例）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为实际 WorkspaceId
)

response = client.chat.completions.create(
    model="qwen3.7-plus",  # 必须与 Base URL 地域匹配
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(response.choices[0].message.content)
```

其他语言（Node.js、curl）及 Anthropic/DashScope 协议的调用方式，详见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 限制和注意事项

- **地域隔离**：API Key、Base URL、模型列表三者严格绑定地域，**不可跨地域混用**。例如，北京地域的 Key 无法调用新加坡 Base URL。
- **限流机制**：
  - 默认按主账号维度进行 RPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 数）限流，不同模型额度独立；
  - 部分旗舰模型（如 `qwen3.8-max`）采用[动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)，其 TPM 基线随月消费金额自动提升；
  - 试用域名（`trial.*`）RPM 仅为 1000，**严禁用于生产环境**。
- **安全与合规**：所有传输数据加密，阿里云**不会将您的输入数据用于模型训练**（见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）。
- **费用控制**：新用户享有北京地域免费额度；额度耗尽后可开启“免费额度用完即停”开关，或设置费用告警，避免意外扣费。

## 来源文档

- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


