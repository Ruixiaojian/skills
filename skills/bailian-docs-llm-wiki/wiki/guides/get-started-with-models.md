# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需自行部署或运维模型，只需配置 API Key、Base URL 和模型 ID 即可发起首次请求。平台同时支持可视化应用构建、微调、部署与评测等全链路能力，适用于从快速验证到生产落地的各类场景。

## 支持的模型与功能

百炼提供覆盖文本、图像、音频、视频等多模态的模型服务，核心文本生成模型包括：

- **Qwen 系列旗舰模型**：`qwen3.8-max`（效果最优，推荐用于复杂任务）、`qwen3.7-plus`（效果/速度/成本均衡，多数场景首选）、`qwen3.7-flash`（高性价比、低延迟，适合简单高频任务）；
- **第三方模型**：DeepSeek、Kimi、GLM 等，部分模型（如 `deepseek-v4-pro-0813`）仅限特定地域（如华北2北京）可用；
- **领域专用模型**：支持长文本处理、法律、意图理解、角色扮演等细分场景。

所有模型均支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)、Anthropic 兼容接口及 DashScope 原生 API 三种调用方式。详细模型列表及各模型在不同地域的支持情况，请参见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

> **注意**：文档 6 中列出的 `qwen3.7-plus-2025-07-28` 等带日期后缀的快照模型（RPM/TPM 限流仅为 60/1,000,000），与文档 1 中明确推荐的 `qwen3.8-max` 及 `qwen3.7-plus`（RPM/TPM 为 30,000/5,000,000）存在显著性能与限流差异。生产环境应优先选用无日期后缀的稳定版模型 ID，避免因限流过严导致服务不稳定。

## 关键参数

调用模型必需的三个核心参数为：

- **`model`**：模型 ID，如 `"qwen3.8-max"`，必须与所选地域实际支持的模型一致；
- **`base_url`**：接入域名，**必须与地域和计费方案严格匹配**。例如：
  - 华北2（北京）按量付费 → `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
  - 新加坡按量付费 → `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
  - Token Plan（仅限交互式工具）→ `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
  - Coding Plan → `https://coding.dashscope.aliyuncs.com/v1`
  
  业务空间专属域名（推荐生产使用）需替换 `{WorkspaceId}`；DashScope 域名（如 `dashscope.aliyuncs.com`）仍可用但不推荐新项目使用。详见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。

- **`api_key`**：必须使用与 `base_url` 所属地域和计费方案配套的 API Key。各地域 API Key 相互独立，不可混用；Token Plan 和 Coding Plan 的 Key 仅限其专属域名使用。

## 使用方式

1. **开通与准备**：  
   - 注册阿里云账号并完成实名认证；  
   - 开通百炼服务，在[控制台](https://bailian.console.aliyun.com/)选择目标地域；  
   - 在[API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)创建 Key，并记录 `DASHSCOPE_API_KEY`；  
   - 在[业务空间管理页面](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)获取 `WorkspaceId`（业务空间ID，用于构造 Base URL）。

2. **配置开发环境**：  
   - 将 `DASHSCOPE_API_KEY` 配置为环境变量（Linux/macOS：`export DASHSCOPE_API_KEY="sk-xxx"`；Windows：系统属性或 PowerShell 设置）；  
   - 安装 SDK：`pip install -U openai`（推荐）或 `pip install -U dashscope`。

3. **发起请求**（以 OpenAI SDK 为例）：  
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   )
   response = client.chat.completions.create(
       model="qwen3.8-max",
       messages=[{"role": "user", "content": "你是谁？"}]
   )
   print(response.choices[0].message.content)
   ```
   完整示例与调试指南请参考 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

## 限制和注意事项

- **地域隔离**：各地域（北京、新加坡、美国弗吉尼亚、德国法兰克福、日本东京）的 Base URL、API Key、模型列表、计费规则完全独立，**严禁跨地域混用**。例如，北京地域的 Key 无法调用新加坡地域的模型。
- **动态限流**：`qwen3.8-max` 等主力模型采用动态 TPM 限流机制，额度按主账号月消费金额分档（如北京地域 ≤10w 档为 500万 TPM），每月 15 日自动更新。该机制为“软限流”，实际可用吞吐可能高于档位值。详情见 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)。
- **硬性限流**：除动态限流外，所有模型均有默认 RPM/TPM 上限（如 `qwen3.8-max` 北京地域为 30,000 RPM / 5,000,000 TPM）。超出时返回 `429 Too Many Requests`。可通过控制台申请临时提额，或采用备选模型降级策略规避。
- **免费额度**：新用户享有北京地域专属免费额度，用完后已认证用户自动转为按量付费；未认证用户需完成认证并充值。建议开启“免费额度用完即停”开关防止意外扣费。
- **数据安全**：按量付费 API 和 Token Plan 团队版承诺**不使用客户数据训练模型**；但 Token Plan 个人版与 Coding Plan 的数据使用条款不同，详见相关协议。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


