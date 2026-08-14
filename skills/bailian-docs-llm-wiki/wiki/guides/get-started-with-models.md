# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过 OpenAI 兼容 API、DashScope SDK 等方式快速调用千问（Qwen）全系列及主流第三方模型。开发者无需部署和运维模型，只需配置 API Key 和 Base URL 即可发起首次推理请求。平台同时覆盖文本、多模态、领域专用等多样化能力，适用于从原型验证到生产部署的全场景。

## 支持的模型与功能

百炼提供自研千问（Qwen）全系模型及 DeepSeek、Kimi、GLM 等第三方模型，按能力分层：

- **旗舰模型**：`qwen3.8-max`（效果最优，适合复杂多步任务）、`qwen3.7-plus`（效果/速度/成本均衡，**推荐首选**）、`qwen3.7-flash`（低延迟、高性价比，适合简单响应）  
- **多模态能力**：涵盖视觉理解、图像生成、语音识别与合成、嵌入向量等  
- **领域模型**：支持长文本处理、法律、意图理解、角色扮演、数据挖掘等垂直场景  

> **注意**：文档中 `qwen3.8-max` 被多次标注为“最新推荐”，但[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)文档未列出该模型在德国（法兰克福）、日本（东京）地域的可用性，而[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)明确指出其支持全部五大地域。实际调用前请以[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)页面控制台实时列表为准。

除直接调用外，平台还支持：
- 可视化智能体（Agent 1.0）与工作流应用构建  
- RAG 知识库接入与[插件](../concepts/plugin.md)/MCP 外部服务集成  
- 模型微调（SFT/CPT/DPO）、专属部署与自动评测  

## 关键参数

### Base URL
Base URL 是模型 API 的核心接入地址，必须与配套 API Key 同地域、同计费方案使用，否则返回 401 错误。三类域名适用场景不同：

| 类型 | 域名格式（示例：北京） | 适用场景 | 鉴权范围 | SLA |
|------|------------------------|----------|-----------|-----|
| **业务空间专属域名**（推荐） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 生产环境，高并发、低延迟、流量隔离 | 仅当前业务空间 | 99.9% |
| **DashScope 域名** | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 存量兼容，快速迁移 | 所有业务空间 | 99.9% |
| **试用域名** | `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 临时测试与验证 | 所有业务空间 | 不提供 |

> **注意**：[Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)文档指出美国（弗吉尼亚）地域的 DashScope 域名已不支持（表格中标注“不支持”），但[选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)文档仍将其列为有效选项。生产环境请优先使用业务空间专属域名，并确认控制台地域页的实际可用域名。

### API Key 与 WorkspaceId
- **API Key**：需在对应地域的[API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)创建，不同地域 Key 不通用  
- **WorkspaceId**：仅业务空间专属域名必需，可在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)页面查看  

## 使用方式

### 1. 环境准备
- 注册阿里云账号并完成实名认证  
- 开通百炼服务，在目标地域创建 API Key  
- 将 `DASHSCOPE_API_KEY` 配置为系统环境变量（避免硬编码）  
- 安装 SDK：`pip install -U openai`（OpenAI 兼容）或 `pip install -U dashscope`

### 2. 发起调用（OpenAI 兼容示例）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId
)

completion = client.chat.completions.create(
    model="qwen3.7-plus",  # 推荐首选
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```

完整代码与 Node.js/curl 示例见[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 3. 地域与部署范围选择
- **地域**：决定数据存储位置与接入点，就近选择降低延迟（如国内用户选华北2（北京））  
- **服务部署范围**：决定推理执行位置（如德国（法兰克福）支持“欧盟”或“全球”），有合规要求时需显式指定  
- **接入域名**：生产环境务必使用业务空间专属域名，迁移仅需替换 Base URL 中的域名部分，无需改业务逻辑  

## 限制和注意事项

### 限流策略
- **账号级聚合限流**：主账号下所有子账号、业务空间、API Key 的调用量合并计算  
- **RPM/TPM 双维度限制**：超出任一阈值即返回 `429 Too Many Requests`  
- **动态限流**：`qwen3.8-max` 等模型采用基于月消费档位的软限流（如北京地域消费 50w 对应 TPM 1000w），实际可用值 ≥ 限流值  
- **固定限流**：多数模型有明确 RPM/TPM 上限（如北京 `qwen3.7-plus`：RPM 30,000 / TPM 5,000,000），详见[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)文档表格  

### 关键注意事项
- **免费额度**：新用户享北京地域专属额度，用完后已认证用户自动转按量付费；可开启“免费额度用完即停”避免意外扣费  
- **数据隐私**：按量付费 API 和 [Token](../concepts/token.md) Plan 团队版**不使用用户数据训练模型**；[Token](../concepts/token.md) Plan 个人版与 Coding Plan 除外，具体条款见[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)  
- **模型响应速度**：与是否付费无关，取决于模型类型（`flash` > `plus` > `max`）、输出长度及服务器负载  
- **错误处理**：`429` 表示速率超限（需退避重试），`403` 表示配额耗尽（需充值或提额），详见[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) FAQ  
- **批量推理**：Batch API 不受实时 RPM/TPM 限制，适合非实时场景，但需额外排队等待  

> **注意**：[动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)文档强调限流按“自然月账单周期”测算，每月 15 日生效；而[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)文档未提及此周期性机制，仅描述静态阈值。开发者应以动态限流文档为准管理长期容量规划。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


