# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需自行部署或运维模型，只需配置 API Key 和 Base URL 即可发起首次请求。平台同时支持可视化应用构建、微调与部署等进阶能力，覆盖从快速验证到生产落地的完整链路。

## 支持的模型与功能

百炼提供多模态、多场景的模型服务，核心包括：

- **千问（Qwen）旗舰系列**：`qwen3.8-max`（效果最优，推荐复杂任务）、`qwen3.7-plus`（效果/速度/成本均衡，**多数场景的推荐选择**）、`qwen3.7-flash`（高性价比、低延迟，适合简单高频任务）[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)；
- **第三方模型**：DeepSeek、Kimi、GLM 等，部分模型（如 DeepSeek）仅限华北2（北京）地域使用 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)；
- **多模态能力**：文本生成、视觉理解、图像/视频生成、语音识别与合成、嵌入向量等；
- **领域模型**：长文本处理、法律、意图理解、角色扮演、数据挖掘等细分方向专用模型。

> **注意**：文档 3（`models.md`）中列出的 `qwen3.7-plus` 和 `qwen3.7-flash` 模型 ID 与文档 1 中明确推荐的 `qwen3.8-max` 存在版本不一致；根据文档 1 的权威说明，“最新的 qwen3.8-max 推理能力全面超越前代，推荐选用”，因此应以 `qwen3.8-max` 为当前首选模型，`qwen3.7-*` 系列为历史版本，实际调用时请优先参考控制台模型广场最新可用模型列表。

## 关键参数

调用模型需正确配置以下核心参数：

- **API Key**：在[API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)创建，**按地域独立**，不可跨地域复用；
- **Base URL**：必须与 API Key 所属地域和计费方案严格匹配，否则返回 401 错误。推荐使用**业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），其具备更高吞吐、更低时延与业务空间级隔离 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；
- **WorkspaceId（业务空间ID）**：使用华北2（北京）、新加坡、日本（东京）、德国（法兰克福）地域时必需，在[业务空间管理](https://modelstudio.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)页面获取；
- **模型名称（model）**：如 `"qwen3.8-max"`，需与所选 Base URL 支持的模型一致，不同地域支持的模型可能不同。

## 使用方式

### 1. 环境准备
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`（避免硬编码）[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)；
- 安装 SDK：`pip install -U openai`（OpenAI 兼容）或 `pip install -U dashscope`（DashScope SDK）。

### 2. 发起调用（OpenAI 兼容示例）
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

> **注意**：文档 5（`base-url.md`）指出 Dashscope 域名（如 `dashscope.aliyuncs.com`）为“原有中心化共享域名，当前可继续使用，**建议迁移至业务空间专属域名**”；而文档 1 的代码示例直接使用了业务空间专属域名，且强调其为生产推荐方案。因此，新项目应直接采用业务空间专属域名，而非 Dashscope 域名。

### 3. 多地域支持
- **华北2（北京）**、**新加坡**、**日本（东京）**、**德国（法兰克福）**：使用 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/...` 格式；
- **美国（弗吉尼亚）**：使用 `https://dashscope-us.aliyuncs.com/compatible-mode/v1`（无 WorkspaceId）；
- 各地域接入点、模型列表、功能支持均独立，详见[地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

## 限制和注意事项

- **动态限流**：对 `qwen3.8-max` 等主力模型，TPM 限流值按账号月消费金额分档动态调整（如北京地域 ≤10w 档为 500w TPM），实际可用值不低于该档位，且每月 15 日生效 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)；
- **固定限流**：非动态限流模型（如部分快照版 `qwen3.7-max-2026-06-08`）有明确 RPM/TPM 上限（如 RPM=600, TPM=1,000,000），超出即触发 429 错误 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；
- **域名与 Key 绑定**：Base URL 必须与同一地域、同一计费方案（按量/[Token](../concepts/token.md) Plan/Coding Plan）的 API Key 配套使用；
- **试用域名限制**：`trial.*` 域名 RPM 仅为 1000，且不提供 SLA，**严禁用于生产环境** [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)；
- **费用控制**：新用户享有北京地域免费额度，额度用尽后已认证用户自动转为按量付费；可通过开启“[免费额度用完即停](https://help.aliyun.com/zh/model-studio/new-free-quota#d1cb80ac11i92)”开关实现额度耗尽即停服 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


