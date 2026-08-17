# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需自行部署或运维模型，只需配置 API Key 和 Base URL 即可发起首次请求。本文档聚焦模型调用的核心路径，涵盖模型选择、参数配置、接入方式及关键限制。

## 支持的模型与功能

百炼提供覆盖[多模态](../concepts/multi-modal.md)与多场景的模型服务，包括文本生成、视觉理解、图像/视频生成、语音处理及嵌入向量等能力。主力文本模型按定位分为三档：

- **qwen3.8-max**：旗舰模型，适合复杂多步骤任务，推理能力全面超越前代，推荐用于高要求场景；  
- **qwen3.7-plus**（含 `qwen-plus` 等别名）：效果、速度与成本均衡，是多数生产场景的**默认推荐选择**；  
- **qwen3.7-flash**（含 `qwen-flash` 等别名）：高性价比、低延迟，适用于简单任务与高频响应场景。  

此外，平台还支持 DeepSeek、Kimi、GLM 等第三方模型（如 `deepseek-v4-pro-0813`），但部分模型地域受限（例如 DeepSeek 仅支持华北2（北京）地域）[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。模型列表与地域支持情况详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)，不同地域的可用模型、上下文长度及计费策略存在差异。

> **注意**：文档 6（`rate-limit.md`）中列出的 `qwen3.7-plus-2026-05-26` 等带日期后缀的快照模型，在文档 4（`models.md`）的模型市场展示中未出现，且文档 6 明确指出“稳定版或最新版比带日期的快照版本限流更宽松”。建议优先使用无日期后缀的通用模型 ID（如 `qwen3.7-plus`），避免因快照模型限流严苛或下线导致服务中断。

## 关键参数

调用模型需正确配置以下核心参数：

- **API Key**：必须通过[阿里云百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)创建，并按计费方案（按量付费、[Token](../concepts/token.md) Plan 或 Coding Plan）选用对应 Key。Key 与地域绑定，**不可跨地域复用**；  
- **Base URL**：决定请求接入点与服务保障等级。推荐使用**业务空间专属域名**（格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`），其具备更高并发、更低时延与业务空间级隔离；Dashscope 域名（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）适用于存量兼容，试用域名（如 `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）仅限临时验证 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；  
- **WorkspaceId**：使用业务空间专属域名时必需，可在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)页面获取；  
- **Model ID**：必须与所选地域实际支持的模型一致（例如 `qwen3.8-max` 在新加坡地域可用，但在德国法兰克福地域未列于文档 7 的模型列表中）；  
- **超时设置**：业务空间专属域名默认超时 3600 秒，Dashscope/试用域名为 600 秒，需在客户端显式配置以避免意外中断。

## 使用方式

### 1. 环境准备
- 完成[实名认证](https://help.aliyun.com/zh/account/verify-your-identity-individual-account)并开通百炼服务；  
- 创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`（Linux/macOS 推荐写入 `~/.bashrc` 或 `~/.zshrc`；Windows 推荐通过系统属性设置）[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)；  
- 确认 Python ≥ 3.8，安装 SDK：`pip install -U openai`（OpenAI 兼容）或 `pip install -U dashscope`（DashScope 原生）。

### 2. 发起请求（OpenAI 兼容示例）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId 和地域
)
completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}],
    temperature=0.8,
    max_tokens=512
)
print(completion.choices[0].message.content)
```

### 3. 地域与部署范围选择
- **地域**：影响数据存储位置与网络延迟，建议就近选择（如中国用户选华北2（北京），东南亚用户选新加坡）；  
- **服务部署范围**：决定推理节点物理位置（如全球、美国、欧盟），有数据合规要求时需指定（例如德国法兰克福地域需在业务空间中选择“欧盟”范围）[选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)；  
- **协议支持**：业务空间专属域名支持 HTTP/SSE/WebSocket/WebRTC/AOQ，Dashscope 域名仅支持 HTTP/SSE。

## 限制和注意事项

- **限流机制**：  
  - 默认采用账号级 RPM/TPM 限流（如 `qwen3.8-max` 在北京地域为 30,000 RPM / 5,000,000 TPM），超出返回 `429 Too Many Requests`；  
  - 部分模型（如 `qwen3.8-max`）启用[动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)，TPM 基线随月消费金额分档提升（≤10w/ (10w,100w]/ >100w 档位对应 500万/1000万/2000万 TPM），且为软限流（实际可用值 ≥ 基线）；  
  - 试用域名 RPM 严格限制为 1000，不建议用于压测或生产。

- **关键约束**：  
  - API Key、Base URL、模型 ID 必须同地域匹配，混用将导致 `401 Unauthorized`；  
  - 免费额度耗尽后，若未开启“免费额度用完即停”，将自动转为按量付费；开启后则返回 `403 Forbidden`；  
  - [Token](../concepts/token.md) Plan 与 Coding Plan 的 API Key 和 Base URL **专用且不可混用**（如 Coding Plan 必须用 `https://coding.dashscope.aliyuncs.com/v1`），且仅限交互式工具（如 Claude Code），**禁止用于后端服务**；  
  - 批量推理（Batch API）不受实时 RPM/TPM 限流约束，但需额外排队等待。

- **调试与监控**：  
  - 调用失败时，依据错误码区分：`Requests rate limit exceeded`（RPM 触发）、`Allocated quota exceeded`（TPM 触发）、`Request rate increased too quickly`（瞬时激增保护）；  
  - 调用量数据约 **1 小时后** 可在[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)查看，非实时；  
  - 生产环境务必使用业务空间专属域名，并通过[限流提额](https://bailian.console.aliyun.com/?tab=model#/efm/temp_limit_raise)申请临时 TPM 提升（30 天有效期）。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


