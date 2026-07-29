# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需自行部署或运维，只需配置 API Key 和 Base URL 即可发起首次请求。平台同时支持可视化应用构建与高代码开发模式，覆盖从快速验证到生产部署的全生命周期需求。

## 支持的模型与功能

百炼提供文本生成、多模态理解与生成、嵌入向量、领域专用模型（如法律、意图识别、长文本处理）等能力。核心模型包括：

- **千问系列**：`qwen3.7-max`（复杂任务首选）、`qwen3.7-plus`（效果/速度/成本均衡，[推荐选择](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）、`qwen3.7-flash`（低延迟、高性价比）；
- **第三方模型**：DeepSeek、Kimi、GLM 等（部分模型地域受限，例如 DeepSeek 仅支持华北2（北京）地域）；
- **特殊用途模型**：`qwen-long`（超长上下文）、`qwq-plus`（推理增强）、`qwen-turbo`（轻量级）等。

所有模型均按地域独立提供，不同地域支持的模型列表、服务部署范围及计费策略存在差异，详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 文档。

> **注意**：文档 1 中称 “DeepSeek 仅支持北京地域”，而文档 4 的模型详情页未明确标注地域限制，但实际调用时若在非北京地域使用 `deepseek-v3.2-exp` 等模型将返回 404 或 401 错误。请以控制台模型市场实时可用列表为准。

## 关键参数

### Base URL
必须与对应计费方案和地域的 API Key 配套使用，否则返回 401 错误。推荐使用**业务空间专属域名**（更高吞吐、更低时延、流量隔离），格式为：
```
https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1
```
其中 `{WorkspaceId}` 需从 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 页面获取；`{region}` 如 `cn-beijing`、`ap-southeast-1` 等。Dashscope 域名（如 `dashscope.aliyuncs.com`）仍可用，但建议迁移至专属域名 —— 具体迁移步骤见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。

### API Key
需通过 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建，并配置为环境变量 `DASHSCOPE_API_KEY` 以避免硬编码泄露风险。不同地域的 API Key **不通用**，且与 Base URL 绑定。

### 模型 ID
直接使用文档中公布的模型名称（如 `qwen3.7-plus`），无需额外注册。部分快照版本（如 `qwen3.7-plus-2026-05-26`）限流更严格，稳定性低于 `qwen3.7-plus` 等无日期后缀的稳定版。

## 使用方式

### 1. 环境准备
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，在控制台创建业务空间（非北京/新加坡/东京/法兰克福地域需显式创建）；
- 获取 API Key 并配置为环境变量（[详细配置指南](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)）。

### 2. 发起调用（OpenAI SDK 示例）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId
)
response = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(response.choices[0].message.content)
```

支持 Python、Node.js、curl 等多种调用方式，完整示例见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 3. 生产增强实践
- **限流应对**：主用模型触发 `429` 时自动降级至备用模型（如 `qwen3.7-plus` → `qwen3.7-flash`），参考 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 中的重试示例；
- **批量处理**：对非实时场景，优先使用 Batch API（不受 RPM/TPM 限流约束）；
- **监控与告警**：调用后约 1 小时可在 [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 查看 [Token](../concepts/token.md) 消耗、成功率等指标。

## 限制和注意事项

- **地域隔离**：各地域 Endpoint、API Key、模型列表、限流策略、计费标准完全独立，**严禁跨地域混用**。例如北京地域的 Key 无法调用新加坡 Base URL。
- **限流规则**：按主账号维度聚合所有子账号、业务空间和 Key 的调用量。常见限流类型包括：
  - `Requests rate limit exceeded`（RPM 超限）；
  - `Allocated quota exceeded`（TPM 超限，含输入+输出 [Token](../concepts/token.md)）；
  - `Request rate increased too quickly`（瞬时爆发触发保护）。  
  各模型 RPM/TPM 阈值差异显著（如 `qwen3.7-max` 北京地域为 30,000 RPM / 5,000,000 TPM，而 `qwen3.7-max-preview` 仅为 60 RPM / 500,000 TPM），详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 表格。
- **免费额度**：新用户仅在北京地域享有新人免费额度，额度耗尽后：
  - 已认证用户自动转为按量付费；
  - 未认证用户需完成认证并充值方可继续使用；
  - 可开启“免费额度用完即停”开关防止意外扣费。
- **安全与合规**：所有传输数据加密，阿里云**不会使用客户数据训练模型**；数据存储位置由所选地域决定，服务部署范围（如“欧盟”、“美国”）控制推理节点物理位置，满足 GDPR 等合规要求。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


