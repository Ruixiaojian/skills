# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）及第三方模型。开发者无需自行部署或运维，只需配置 API Key 和 Base URL 即可发起首次请求。本文档面向开发者，聚焦模型调用的核心路径与关键约束。

## 支持的模型与功能

百炼提供多系列千问模型（如 `qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`）及 DeepSeek、Kimi、GLM 等第三方模型，覆盖文本生成、多模态理解与生成、嵌入向量等能力 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。模型按能力、速度与成本分层：  
- **qwen3.7-max**：效果最优，适合复杂多步任务；  
- **qwen3.7-plus**：效果、延迟与成本均衡，为多数场景的**推荐选择**；  
- **qwen3.6-flash**：高性价比、低延迟，适用于简单高频任务。  

除标准文本生成外，平台还支持可视化智能体构建、工作流编排、RAG 知识库接入、[插件](../concepts/plugin.md)调用及模型微调等高级功能 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

> **注意**：文档 3（`models.md`）中列出的 `qwen3.6-flash` 模型 ID 与文档 1 中推荐的 `qwen3.7-plus` 存在版本不一致；实际生产应以控制台最新模型市场为准，`qwen3.7-plus` 是当前主力推荐版本，而非 `qwen3.6-flash`。

## 关键参数

### 地域与 Base URL
- **地域决定数据驻留位置与接入点**：华北2（北京）、新加坡、美国（弗吉尼亚）、德国（法兰克福）、日本（东京）五地独立运营，API Key 不通用，Base URL 亦不互通 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。  
- **Base URL 类型**：  
  - **业务空间专属域名**（推荐）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，提供更高并发、更低时延与流量隔离；  
  - **Dashscope 域名**（兼容）：如 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）、`https://dashscope-us.aliyuncs.com/compatible-mode/v1`（美国），适用于存量迁移；  
  - **试用域名**：`https://trial.{region}.maas.aliyuncs.com/compatible-mode/v1`，限流严格，仅用于快速验证 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。  

### API Key 与鉴权
- API Key 需在对应地域的 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建，且必须与 Base URL 所属地域匹配；  
- 业务空间专属域名仅接受该业务空间创建的 API Key，而 Dashscope 域名支持跨业务空间调用；  
- 强烈建议将 `DASHSCOPE_API_KEY` 配置为环境变量，避免硬编码泄露 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

## 使用方式

### 1. 环境准备
- 安装 Python ≥3.8，并推荐使用虚拟环境隔离依赖；  
- 安装 SDK：`pip install -U openai`（OpenAI 兼容）或 `pip install -U dashscope`（DashScope 原生）；  
- 配置环境变量 `DASHSCOPE_API_KEY`（Linux/macOS：`~/.bashrc` 或 `~/.zshrc`；Windows：系统属性或 PowerShell）[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 2. 发起请求（OpenAI SDK 示例）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换 {WorkspaceId}
)
completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```

> **注意**：文档 2 中示例代码使用 `qwen-plus`，但文档 1 明确推荐 `qwen3.7-plus` 为当前主力版本；请优先采用 `qwen3.7-plus` 或控制台模型市场最新稳定版 ID。

### 3. 多语言支持
除 Python 外，Node.js、curl 均有完整示例，核心逻辑一致：设置 `Authorization: Bearer $DASHSCOPE_API_KEY` + 正确 Base URL + JSON 请求体 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 限制和注意事项

### 限流策略
- **账号级聚合限流**：主账号下所有 RAM 子账号、业务空间、API Key 的调用量合并计算；  
- **双维度限流**：每分钟请求数（RPM）与每分钟 [Token](../concepts/token.md) 消耗（TPM，含输入+输出）任一超限即拒绝请求；  
- **典型限流值（华北2 北京）**：`qwen3.7-plus` 为 RPM=30,000 / TPM=5,000,000；快照版（如 `qwen-plus-2025-07-28`）仅为 RPM=60 / TPM=1,000,000 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；  
- **恢复时间**：通常 60 秒内自动恢复；瞬时激增可能触发 `Request rate increased too quickly`，需平滑请求速率。

### 其他关键约束
- **免费额度**：新用户仅华北2（北京）地域享新人免费额度，用完后已认证用户自动转按量付费，未认证用户需完成实名认证并充值 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)；  
- **费用控制**：限流不等于费用控制；如需防超额支出，须主动设置消费限额、开启“免费额度用完即停”或订阅 Coding Plan [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；  
- **域名与 Key 绑定**：Dashscope 域名、业务空间专属域名、Coding Plan 域名三者 API Key 互不通用，混用将返回 401 错误 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


