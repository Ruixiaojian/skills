# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过标准化 API 快速调用千问（Qwen）全系列及第三方模型。开发者无需部署和运维模型，只需配置 API Key、选择合适地域与 Base URL，并传入标准参数即可发起推理请求。本文档汇总了模型接入的核心路径、关键约束与最佳实践。

## 支持的模型与功能

百炼当前提供文本生成、[多模态](../concepts/multi-modal.md)理解与生成、嵌入向量等能力，主力模型为千问（Qwen）系列，按能力与成本分为三档：

- **qwen3.7-max**：效果最强，适合复杂多步任务；[文档明确指出其为“Qwen 系列效果最好的模型”](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)  
- **qwen3.7-plus**：效果、速度与成本均衡，是多数场景的**推荐选择**；[该模型在华北2（北京）、新加坡、日本（东京）、德国（法兰克福）、美国（弗吉尼亚）等多地可用](../../raw/model-user-guide/get-started-with-models/models.md)  
- **qwen3.7-flash**：高性价比、低延迟，适用于简单、高频响应任务  

此外，平台还支持 DeepSeek、Kimi、GLM 等第三方模型（部分仅限特定地域，如 DeepSeek 仅支持华北2（北京））。所有模型均兼容 OpenAI、Anthropic 及 DashScope 三种协议，同一模型 ID 在不同协议下行为一致。

> **注意**：文档 2 中列出的 `qwen3.8-max-preview` 标注为“仅 [Token](../concepts/token.md) Plan 可用”，但文档 6 的限流表格中未包含该模型，且文档 3 明确推荐使用 `qwen3.7-max`。建议以 [限流文档](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 中实际列出的稳定模型为准，避免依赖预览版。

## 关键参数

调用模型必需以下参数，缺一不可：

- **API Key**：通过 [阿里云百炼控制台 → API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建，需与所选 Base URL 所属地域及计费方案匹配。  
- **Base URL**：决定请求接入点，必须与 API Key 的计费方案（按量付费 / [Token](../concepts/token.md) Plan / Coding Plan）及地域严格对应。例如：
  - 华北2（北京）按量付费 + 业务空间专属域名：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`  
  - 美国（弗吉尼亚）按量付费 + Dashscope 域名：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`  
  - [Token](../concepts/token.md) Plan 专用：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`  
  详见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。  
- **model**：字符串形式的模型 ID，如 `"qwen3.7-plus"`，必须与所选地域支持的模型列表一致。  
- **messages**：符合 OpenAI Chat Completions 格式的对话数组，至少包含一个 `user` 角色消息。  

> **注意**：文档 1 和文档 3 均强调 `base_url` 中的 `{WorkspaceId}` 需替换为真实业务空间 ID（可在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 页面获取），而文档 4 的试用域名（如 `trial.cn-beijing.maas.aliyuncs.com`）虽无需 WorkspaceId，但限流严格（RPM=1000），**不适用于生产环境**。

## 使用方式

### 1. 环境准备
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，在控制台创建业务空间（如需专属域名）；
- 获取 API Key 并**配置为环境变量 `DASHSCOPE_API_KEY`**，避免硬编码泄露风险；[详细配置方法见首次调用千问API文档](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 2. SDK 调用示例（OpenAI 兼容）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为实际 WorkspaceId
)

response = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(response.choices[0].message.content)
```

### 3. curl 调用（调试用）
```bash
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "qwen3.7-plus",
        "messages": [{"role": "user", "content": "你是谁？"}]
      }'
```

## 限制和注意事项

- **地域隔离**：各地域（华北2、新加坡、德国、日本、美国）的 API Key、Base URL、模型列表、限流策略均独立，**不可跨地域混用**。  
- **限流策略**：按主账号维度合并计算所有子账号、业务空间和 API Key 的调用量。核心限制为：
  - **RPM（每分钟请求数）**：如 `qwen3.7-plus` 在华北2（北京）为 30,000 RPM；  
  - **TPM（每分钟 Token 消耗）**：含输入与输出 Token，同模型在不同地域额度差异显著（如新加坡版 `qwen3.7-plus` TPM 为 5,000,000，而德国版为 30,000）；  
  - **瞬时保护**：即使未超 RPM/TPM，短时请求激增也可能触发 `Request rate increased too quickly` 错误。  
  详情参见 [限流文档](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。  
- **Token Plan 与 Coding Plan 限制**：仅限 AI 工具（如 Claude Code）交互式使用，**不可用于后端服务调用**；其 Base URL 和 API Key 与按量付费体系完全隔离。  
- **安全与合规**：用户数据不会被用于模型训练，传输全程加密；但需自行选择符合数据合规要求的服务部署范围（如欧盟客户应选德国（法兰克福）+ 欧盟部署范围）。

## 来源文档

- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)


