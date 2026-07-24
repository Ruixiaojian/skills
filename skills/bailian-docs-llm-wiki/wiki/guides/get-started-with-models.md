# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过 API 快速调用千问（Qwen）及第三方模型。本文面向开发者，聚焦模型接入的核心路径：从环境准备、模型选择到实际调用，涵盖关键参数、地域与域名配置、限流约束等实操要点。所有操作均基于标准 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope SDK，无需自行部署模型。

## 支持的模型与功能

百炼提供覆盖文本、多模态及领域场景的模型服务：

- **千问系列主力模型**（按能力与成本平衡推荐）：
  - `qwen3.7-max`：效果最强，适合复杂多步任务（[详见模型文档](https://help.aliyun.com/zh/model-studio/models)）；
  - `qwen3.7-plus`：效果、速度与成本均衡，为多数生产场景的**默认推荐**；
  - `qwen3.6-flash`：高性价比、低延迟，适用于简单快速响应任务。

- **第三方模型**：支持 DeepSeek、Kimi、GLM 等，具体可用模型因地域而异，需在[模型广场](https://bailian.console.aliyun.com/?tab=model#/model-market)中确认。

- **多模态能力**：除文本生成外，还支持视觉理解、图像生成、语音识别与合成、嵌入向量等（见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）。

> **注意**：文档 1 中示例使用 `qwen-plus`，而文档 3 和 6 明确推荐 `qwen3.7-plus` 作为当前主力版本；`qwen-plus`（无版本号）已属旧版，其限流额度（RPM 15,000）低于 `qwen3.7-plus`（RPM 30,000），且部分地域不再默认提供。请优先选用带 `3.7` 版本号的模型。

## 关键参数

调用模型必需配置以下参数，缺一不可：

- **API Key**：在 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建，用于身份鉴权。  
- **Base URL**：模型服务接入地址，**必须与 API Key 所属地域和计费方案严格匹配**（见下文“使用方式”）。  
- **Model ID**：如 `qwen3.7-plus`，需与所选地域支持的模型列表一致（参见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)）。  
- **WorkspaceId（业务空间ID）**：仅华北2（北京）、新加坡、日本（东京）、德国（法兰克福）地域的**业务空间专属域名**需要，可在 [业务空间管理](https://modelstudio.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 页面获取。美国（弗吉尼亚）地域使用 `dashscope-us.aliyuncs.com` 域名，**无需 WorkspaceId**。  

> **注意**：文档 1 中要求“使用华北2（北京）、新加坡、日本（东京）或德国（法兰克福）地域的模型时，需在 Base URL 中填入 WorkspaceId”，但文档 5 明确指出美国（弗吉尼亚）地域**不支持业务空间专属域名**，仅提供 `dashscope-us.aliyuncs.com`；同时，文档 4 表明德国/日本地域的 Dashscope 域名已“不支持”，即必须使用 WorkspaceId。因此，WorkspaceId 并非“四地通用”，而是**业务空间专属域名的强制参数，与地域强绑定**。

## 使用方式

### 1. 环境准备
- **获取凭证**：注册阿里云账号 → 开通百炼服务 → 在 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建 Key。
- **配置环境变量**（推荐）：将 `DASHSCOPE_API_KEY` 写入系统环境变量，避免硬编码（详细步骤见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)）。
- **安装 SDK**：任选其一：
  - OpenAI Python SDK：`pip install -U openai`
  - DashScope Python SDK：`pip install -U dashscope`

### 2. 构造请求
- **Base URL 选择原则**：
  - **生产环境**：务必使用**业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），具备更高并发与 SLA 保障（99.9%）；
  - **快速验证**：可临时使用试用域名（如 `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），但 RPM 限流仅为 1000；
  - **存量迁移**：Dashscope 域名（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）仍可用，但建议按 [迁移指南](https://help.aliyun.com/zh/model-studio/base-url#section-migrate-domain) 升级（见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)）。

- **代码示例（OpenAI SDK）**：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://llm-xxx.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为你的 WorkspaceId + 地域域名
  )
  response = client.chat.completions.create(
      model="qwen3.7-plus",
      messages=[{"role": "user", "content": "你是谁？"}]
  )
  ```

## 限制和注意事项

- **地域隔离**：API Key、Base URL、模型列表均**不可跨地域混用**。例如，北京地域的 Key 无法调用新加坡地域的模型（见 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)）。
- **限流策略**：
  - 按主账号维度合并计算所有子账号、业务空间和 Key 的调用量；
  - 分 RPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 数）双重限制，超出任一即返回 `429`；
  - 稳定版模型（如 `qwen3.7-plus`）限流额度显著高于快照版（如 `qwen-plus-2025-07-28`），后者 RPM 仅 60（见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)）；
  - 批量推理（Batch API）不受实时限流约束，适合离线任务。
- **费用控制**：
  - 新用户享有北京地域免费额度，用完后认证用户自动转按量付费，未认证用户将停止服务；
  - 可开启“免费额度用完即停”开关，或设置消费告警，避免意外扣费（见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）；
  - 模型推理与知识库（RAG）**独立计费**，前者按 [Token](../concepts/token.md)，后者按规格时长，不支持通用节省计划抵扣。

## 来源文档

- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)


