# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及第三方主流模型。开发者无需部署和运维，只需配置 API Key 和 Base URL 即可发起首次推理请求。本文档聚焦模型调用的核心路径，涵盖模型选择、参数配置、接入方式及关键约束。

## 支持的模型与功能

百炼提供文本生成、多模态理解与生成、嵌入向量、领域专用模型（如法律、意图识别）等能力。主力文本模型按性能与成本分层：

- **qwen3.8-max**：旗舰模型，适用于复杂多步任务；[原文标题](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)明确指出其“推理能力全面超越前代，推荐选用”。
- **qwen3.7-plus**：效果、速度与成本均衡，是多数场景的**推荐选择**。
- **qwen3.7-flash**：高性价比、低延迟，适合简单高频任务。

除千问系列外，还支持 DeepSeek、Kimi、GLM 等第三方模型（DeepSeek 仅限北京地域）。模型覆盖地域包括华北2（北京）、新加坡、美国（弗吉尼亚）、德国（法兰克福）、日本（东京），但各地区支持的模型和功能存在差异——例如德国/日本地域不支持模型调优与应用开发，美国地域不支持批量推理 [原文标题](../../raw/model-user-guide/get-started-with-models/regions.md)。

> **注意**：文档 3（`models.md`）中列出的 `qwen3.7-plus` 在多个地域均标注为支持，但文档 6（`regions.md`）的“各地域功能支持”表格显示新加坡地域**不支持模型调优**，而文档 1（`what-is-model-studio.md`）称“支持有监督微调（SFT）”——该能力实际仅在北京地域可用。请以[原文标题](../../raw/model-user-guide/get-started-with-models/regions.md)的地域功能矩阵为准。

## 关键参数

调用模型需正确配置以下核心参数：

- **API Key**：在[API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)创建，不同地域的 Key 不通用。
- **Base URL**：必须与 API Key 所属地域及计费方案严格匹配：
  - **业务空间专属域名**（推荐生产环境）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，其中 `{WorkspaceId}` 需从[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)获取；
  - **DashScope 域名**（兼容存量）：如 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）、`https://dashscope-us.aliyuncs.com/compatible-mode/v1`（美国）；
  - **试用域名**：`https://trial.{region}.maas.aliyuncs.com/compatible-mode/v1`，限流严格，仅用于验证。
- **Model ID**：如 `qwen3.8-max`，需与所选地域实际支持的模型一致（参见[原文标题](../../raw/model-user-guide/get-started-with-models/models.md)）。

## 使用方式

### 1. 环境准备
- 完成阿里云账号注册与实名认证；
- 开通百炼服务，在控制台创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`；
- 获取业务空间 ID（北京/新加坡/东京/法兰克福地域必需）。

### 2. 发起调用（OpenAI SDK 示例）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId
)

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```

> 注意：Node.js、curl 等其他语言/工具的调用方式详见[原文标题](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

### 3. 备选策略
为应对限流，建议实现自动降级逻辑：主模型触发 `429` 错误时，切换至同地域限流更宽松的备选模型（如 `qwen3.7-plus`），示例代码见[原文标题](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

## 限制和注意事项

- **地域隔离**：各地域的 API Key、Base URL、模型列表、监控数据完全独立，**不可跨地域混用**。
- **动态限流**：`qwen3.8-max` 等模型采用动态 TPM 限流，额度按账号月消费金额分档（如北京地域 ≤10万元档为 500w TPM），每月 15 日生效 [原文标题](../../raw/model-user-guide/get-started-with-models/quota-management.md)。
- **静态限流**：非动态限流模型（如快照版 `qwen3.7-max-2026-06-08`）有固定 RPM/TPM 上限（北京地域 RPM=600, TPM=1,000,000），超出即拒绝请求。
- **协议与超时**：业务空间专属域名支持 WebSocket/WebRTC/AOQ，超时 3600 秒；DashScope 域名仅支持 HTTP/SSE，超时 600 秒 [原文标题](../../raw/model-user-guide/get-started-with-models/regions.md)。
- **费用控制**：模型推理与知识库（RAG）计费相互独立；新用户可开启“免费额度用完即停”避免意外扣费 [原文标题](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)


