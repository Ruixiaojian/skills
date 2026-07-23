# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过 OpenAI 兼容 API、DashScope SDK 等方式快速调用千问（Qwen）及第三方模型。开发者无需部署运维，只需获取 API Key、配置 Base URL 并指定模型 ID 即可发起首次推理请求。本文聚焦核心接入路径，涵盖模型选择、参数配置、调用方式及关键约束。

## 支持的模型与功能

百炼提供覆盖文本、[多模态](../concepts/multi-modal.md)及领域专用的全系列模型，其中千问（Qwen）为核心自研模型：

- **主力推荐模型**：`qwen3.7-plus`（效果、速度、成本均衡），`qwen3.7-max`（复杂任务首选），`qwen3.6-flash`（高并发低延迟场景）[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)  
- **模型可用性差异**：不同地域支持的模型集合不同。例如 `qwen3.7-max-preview` 仅限 [Token](../concepts/token.md) Plan 用户且仅在北京地域可用；DeepSeek 模型目前仅支持华北2（北京）地域 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)  
- **功能覆盖**：除基础文本生成外，还支持视觉理解、图像生成、语音合成、嵌入向量、长文本处理、法律/意图/角色扮演等细分领域模型 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)

> **注意**：文档 3 中列出的 `qwen3.8-max-preview` 在文档 5 的限流表格中未出现，且文档 5 明确标注该模型“仅 [Token](../concepts/token.md) Plan 可用”，而文档 2 未提及此限制。实际使用前请以控制台实时模型列表为准。

## 关键参数

### API Key
- 必须通过[阿里云百炼控制台 → API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)创建，**不可跨地域复用**  
- 建议配置为环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露风险 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)

### Base URL
- **业务空间专属域名（生产推荐）**：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，需先在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)获取 WorkspaceId  
- **DashScope 共享域名（兼容存量）**：如 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）、`https://dashscope-us.aliyuncs.com/compatible-mode/v1`（美国）  
- **试用域名（非生产）**：`https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，RPM 限流严格（1000）  
- 各域名鉴权范围不同：业务空间专属域名仅允许对应 Workspace 的 API Key 调用，而 DashScope 域名支持跨 Workspace [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)

### 模型 ID
- 必须与所选地域和 Base URL 匹配。例如 `qwen3.7-plus-us` 仅适用于美国（弗吉尼亚）地域的 DashScope 域名，而 `qwen3.7-plus` 在北京地域需配合业务空间专属域名使用  
- 部分模型带时间后缀（如 `qwen-plus-2025-07-28`），其限流额度显著低于稳定版（见下文限制部分）

## 使用方式

### 基础调用流程
1. **开通服务**：使用阿里云主账号登录[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/model-market)，同意协议开通服务  
2. **获取凭证**：创建 API Key，并在业务空间管理页获取 WorkspaceId（若使用专属域名）  
3. **配置环境**：将 `DASHSCOPE_API_KEY` 设为环境变量（Linux/macOS/Windows 均有详细指南）[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)  
4. **发起请求**：使用 OpenAI SDK 或 DashScope SDK，示例（OpenAI 兼容）：
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   )
   response = client.chat.completions.create(
       model="qwen3.7-plus",
       messages=[{"role": "user", "content": "你是谁？"}]
   )
   ```

### 多语言支持
- 官方提供 Python、Node.js 示例，curl 命令亦可直接验证 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)  
- 所有 OpenAI 兼容客户端（如 LangChain、LlamaIndex）均可通过调整 `base_url` 和 `api_key` 迁移使用  

## 限制和注意事项

### 限流策略
- **账号级聚合限流**：主账号下所有子账号、业务空间、API Key 的调用量合并计算 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)  
- **双维度限制**：每分钟请求数（RPM）和每分钟 [Token](../concepts/token.md) 消耗（TPM）任一超限即触发 429 错误  
- **典型额度对比**（北京地域）：
  - `qwen3.7-plus`：RPM 30,000 / TPM 5,000,000  
  - `qwen-plus-2025-07-28`：RPM 60 / TPM 1,000,000  
  - `qwen-long-2025-01-25`：RPM 3 / TPM 7,500  
- **临时提额**：可在控制台[限流提额页面](https://bailian.console.aliyun.com/?tab=model#/efm/temp_limit_raise)申请提升 TPM，有效期 30 天 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)

### 地域与域名约束
- **地域隔离**：API Key、Base URL、模型列表均按地域独立，混用导致 401 错误 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)  
- **域名适配**：业务空间专属域名要求 API Key 必须属于该 Workspace；DashScope 域名支持跨 Workspace，但不提供业务级流量隔离 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)  
- **功能差异**：批量推理（Batch API）仅在北京、新加坡地域支持；模型调优、应用开发等功能在北京地域独有 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)

### 其他关键约束
- **免费额度**：新用户在北京地域享有专属免费额度，用尽后认证用户自动转按量付费，未认证用户需完成实名认证 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)  
- **数据合规**：若要求数据不出中国内地，必须选择华北2（北京）地域 + “中国内地”服务部署范围；国际业务推荐新加坡（国际）或美国（全球） [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)  
- **Token Plan 限制**：Token Plan 专属 API Key 仅限 Claude Code 等交互式工具使用，**不可用于后端服务调用** [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)

## 来源文档

- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


