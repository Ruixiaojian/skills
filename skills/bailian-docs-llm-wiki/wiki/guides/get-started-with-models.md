# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需自行部署或运维，只需配置 API Key 和 Base URL 即可发起首次请求。平台同时支持可视化应用构建与高代码开发模式，覆盖从快速验证到生产部署的完整链路。

## 支持的模型与功能

百炼提供[多模态](../concepts/multi-modal.md)、多场景的模型服务，核心包括：

- **千问（Qwen）系列**：按能力与成本分层，推荐选择 `qwen3.7-plus`（效果、速度、成本均衡），`qwen3.7-max`（复杂任务首选），`qwen3.7-flash`（低延迟简单任务）；[最新模型列表详见](../../raw/model-user-guide/get-started-with-models/models.md)。
- **第三方模型**：集成 DeepSeek、Kimi、GLM 等，其中 DeepSeek 仅支持华北2（北京）地域 [原文标题](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。
- **[多模态](../concepts/multi-modal.md)能力**：覆盖文本生成、视觉理解、图像/视频生成、语音识别与合成、嵌入向量等。
- **领域模型**：提供长文本处理、法律、意图理解、角色扮演等细分场景专用模型。

> **注意**：文档中 `qwen3.8-max-preview` 标注“仅 [Token](../concepts/token.md) Plan 可用”，但该模型未在限流文档（[原文标题](../../raw/model-user-guide/get-started-with-models/rate-limit.md)）中列出限流值，且其命名与当前主流 `qwen3.7-*` 系列不一致，建议优先使用已明确限流策略的 `qwen3.7-max` 或 `qwen3.7-plus`。

## 关键参数

### Base URL
必须与对应计费方案和地域的 API Key 配套使用，否则返回 401 错误。三类域名适用场景不同：
- **业务空间专属域名**（推荐生产环境）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，提供更高吞吐、更低时延与流量隔离；
- **Dashscope 域名**（兼容存量）：如 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）、`https://dashscope-us.aliyuncs.com/compatible-mode/v1`（美国）；
- **试用域名**（仅限快速验证）：`https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，RPM 限流为 1000，不建议用于生产 [原文标题](../../raw/model-user-guide/get-started-with-models/base-url.md)。

> **注意**：各地域 API Key 不通用，且 `WorkspaceId` 仅在华北2（北京）、新加坡、日本（东京）、德国（法兰克福）地域需显式填入；美国（弗吉尼亚）使用 `dashscope-us.aliyuncs.com`，无需 `WorkspaceId` [原文标题](../../raw/model-user-guide/get-started-with-models/regions.md)。

### API Key
- 通过 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建；
- 建议配置为环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露风险 [原文标题](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

## 使用方式

### 1. 环境准备
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，在控制台创建 API Key 并获取 `WorkspaceId`（如需）；
- 安装 SDK：`pip install -U openai`（OpenAI 兼容）或 `pip install -U dashscope`（DashScope SDK）。

### 2. 发起请求（OpenAI 兼容示例）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId
)
completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```

### 3. 多地域适配
- 北京：`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
- 新加坡：`{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
- 美国（弗吉尼亚）：`dashscope-us.aliyuncs.com`（无 WorkspaceId）
- 德国/日本：同理替换 `{region}`，详见 [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

## 限制和注意事项

### 限流规则
- **账号级聚合**：主账号下所有 RAM 子账号、业务空间、API Key 的调用量合并计算；
- **双维度限流**：每分钟请求数（RPM）与每分钟 [Token](../concepts/token.md) 消耗（TPM），任一超限即拒绝请求；
- **典型值**（华北2 北京）：
  - `qwen3.7-plus`：RPM 30,000 / TPM 5,000,000；
  - `qwen3.7-max-preview`：RPM 60 / TPM 500,000；
- **瞬时保护**：即使未达分钟上限，短时请求激增也可能触发 `Request rate increased too quickly` [原文标题](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

### 其他关键限制
- **地域隔离**：各地域模型、API Key、Base URL 互不通用，跨地域调用必失败；
- **功能差异**：批量推理、模型调优、应用开发等功能仅在华北2（北京）和新加坡地域支持，美国、德国、日本地域部分功能缺失 [原文标题](../../raw/model-user-guide/get-started-with-models/regions.md)；
- **费用控制**：模型推理与知识库（RAG）计费独立，前者按 [Token](../concepts/token.md) 用量，后者按规格时长，不支持通用节省计划抵扣 [原文标题](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)




