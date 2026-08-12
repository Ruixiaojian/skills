# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过标准化 API 快速调用千问（Qwen）及第三方模型。本文面向开发者，聚焦模型调用的核心路径：从环境准备、模型选择到实际请求，涵盖关键参数、地域与域名配置、限流机制等实操要点。所有内容均基于平台当前生产环境行为整理，不包含营销性描述。

## 支持的模型与功能

百炼提供覆盖文本、图像、音频、视频等多模态的模型服务，其中文本生成类模型是主流使用场景。核心推荐模型如下（以华北2北京地域为例）：

- **`qwen3.8-max`**：Qwen 系列效果最强模型，适合复杂多步骤任务；最新版推理能力全面超越前代，[原文标题](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)明确推荐选用。
- **`qwen3.7-plus`**：效果、速度与成本均衡，是多数场景的**推荐选择**。
- **`qwen3.7-flash`**：高性价比、低延迟，适合简单任务的快速响应。

除千问系列外，平台还集成 DeepSeek、Kimi、GLM 等第三方模型，但部分模型（如 DeepSeek）仅限特定地域（如北京）可用 [原文标题](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。所有模型均支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)、Anthropic 兼容接口及 DashScope 原生 SDK，无需修改核心逻辑即可切换。

> **注意**：文档 4 中列出的 `qwen3.7-flash` 等模型在文档 5 的限流表格中实际对应为 `qwen3.7-flash`（无版本后缀），而文档 5 中大量存在带日期后缀的快照模型（如 `qwen3.7-plus-2026-05-26`），其限流值显著低于主干版本（RPM 600 vs 30,000）。开发者应优先选用无后缀的稳定模型 ID，避免因限流过严导致服务不可用。

## 关键参数

调用模型需正确配置以下核心参数，缺一不可：

- **`DASHSCOPE_API_KEY`**：在 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建，**必须与所选地域和计费方案匹配**。不同地域的 API Key 不通用，跨地域使用将返回 401 错误 [原文标题](../../raw/model-user-guide/get-started-with-models/base-url.md)。
- **`base_url`**：模型服务接入地址，**必须与 API Key 所属计费方案一致**。推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），其具备更高并发、更低时延与业务空间级隔离；Dashscope 域名（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）为兼容方案，试用域名限流严格，不建议生产使用 [原文标题](../../raw/model-user-guide/get-started-with-models/base-url.md)。
- **`model`**：模型 ID，必须与 `base_url` 所属地域支持的模型列表一致。例如，新加坡地域不支持 `qwen3.8-max` 的全部功能，且其 TPM 限流档位（200w/500w/1000w）低于北京地域（500w/1000w/2000w）[原文标题](../../raw/model-user-guide/get-started-with-models/quota-management.md)。
- **`WorkspaceId`**：仅当使用业务空间专属域名时必需，在 [业务空间管理页面](https://modelstudio.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 查看。北京、新加坡、东京、法兰克福、弗吉尼亚五地均需此参数，但美国（弗吉尼亚）部分模型（如 `qwen-plus-us`）可限定境内推理。

## 使用方式

### 1. 环境准备
- **获取凭证**：注册阿里云账号 → 开通百炼服务 → 创建 API Key → 获取 WorkspaceId（若使用专属域名）。
- **配置 API Key**：强烈建议通过环境变量（如 `DASHSCOPE_API_KEY`）注入，避免硬编码。Linux/macOS 可写入 `~/.bashrc` 或 `~/.zshrc`；Windows 可通过系统属性或 PowerShell 设置 [原文标题](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。
- **安装 SDK**：推荐使用 `openai`（OpenAI 兼容）或 `dashscope`（原生 SDK）。安装命令：
  ```bash
  pip install -U openai  # 或 pip install -U dashscope
  ```

### 2. 发送请求（OpenAI 兼容示例）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId
)

response = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(response.choices[0].message.content)
```

### 3. 多语言支持
除 Python 外，Node.js、curl 等方式同样适用。Node.js 示例见 [原文标题](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)，curl 示例中需注意 `-H "Authorization: Bearer $DASHSCOPE_API_KEY"` 的变量引用语法。

## 限制和注意事项

### 限流机制
百炼按主账号维度对模型调用实施 RPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 消耗）双重限流，超出即返回 429 错误。关键规则：
- **账号级聚合**：主账号下所有子账号、业务空间、API Key 的调用量合并计算 [原文标题](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。
- **动态限流**：`qwen3.8-max` 等主力模型采用动态限流，TPM 阈值随百炼月消费金额分档调整（如北京地域：≤10w 档为 500w TPM），且实际可用值可能高于阈值（软限流）[原文标题](../../raw/model-user-guide/get-started-with-models/quota-management.md)。
- **静态限流**：其他模型（如 `qwen3.7-plus`）有固定限流值（北京地域 RPM 30,000 / TPM 5,000,000），可在控制台 [限流提额页面](https://bailian.console.aliyun.com/?tab=model#/efm/temp_limit_raise) 申请临时提升（30 天有效期）。

### 其他重要约束
- **地域隔离**：各地域 Endpoint、API Key、模型列表、功能支持（如批量推理仅北京/新加坡支持）完全独立，不可混用 [原文标题](../../raw/model-user-guide/get-started-with-models/regions.md)。
- **免费额度**：新用户享北京地域专属免费额度，用完后未认证用户将停服，已认证用户自动转按量付费；可开启“免费额度用完即停”避免意外扣费 [原文标题](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。
- **数据安全**：按量付费 API 和 [Token](../concepts/token.md) Plan 团队版承诺不使用客户数据训练模型；但 [Token](../concepts/token.md) Plan 个人版与 Coding Plan 不在此承诺范围内，详见服务协议 [原文标题](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 来源文档

- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


