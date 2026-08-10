# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）及第三方模型。开发者无需部署或运维模型，只需配置 API Key 和 Base URL 即可开始推理。平台同时支持可视化应用构建、微调与部署等全链路能力，适用于从快速验证到生产级落地的各类场景。

## 支持的模型与功能

百炼提供[多模态](../concepts/multi-modal.md)、多系列的预置模型，覆盖文本生成、视觉理解、语音合成、嵌入向量等能力。核心文本模型包括：

- **Qwen 系列旗舰模型**：`qwen3.8-max`（效果最优，推荐用于复杂任务）、`qwen3.7-plus`（效果/速度/成本均衡，[多数场景的推荐选择](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）、`qwen3.7-flash`（低延迟、高性价比，适合简单任务）。
- **第三方模型**：DeepSeek、Kimi、GLM 等，部分模型（如 DeepSeek）仅限华北2（北京）地域使用 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。
- **领域专用模型**：长文本处理、法律、意图理解、角色扮演等细分场景模型，详情见[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

> **注意**：文档中 `qwen3.8-max` 与 `qwen3.7-plus` 的版本命名存在不一致（如文档1称“qwen3.8-max”，文档3和6中出现“qwen3.7-plus”），实际以控制台[模型广场](https://bailian.console.aliyun.com/?tab=model#/model-market)最新列表为准；建议优先选用无日期后缀的稳定版模型（如 `qwen3.8-max`），其限流额度更高且不受快照版本限制 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

## 关键参数

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `API Key` | 调用鉴权凭证，需在[API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)创建 | 各地域 API Key **不通用**，必须与 Base URL 所属地域匹配；建议配置为环境变量 `DASHSCOPE_API_KEY` 避免硬编码 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) |
| `Base URL` | 模型服务接入地址，格式为 `{domain}/compatible-mode/v1` | 必须与 API Key 计费方案配套：<br>- **业务空间专属域名**（推荐生产环境）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`<br>- **Dashscope 域名**（兼容存量）：`https://dashscope.aliyuncs.com/compatible-mode/v1`<br>- **试用域名**（非生产）：`https://trial.{region}.maas.aliyuncs.com/compatible-mode/v1` [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md) |
| `model` | 模型 ID，如 `"qwen3.8-max"` | 不同地域支持的模型不同，例如 DeepSeek 仅支持北京地域；美国（弗吉尼亚）地域需使用带 `-us` 后缀的模型名（如 `qwen3.7-plus-us`）限定境内推理 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) |
| `messages` | 对话历史，含 `role`（`system`/`user`/`assistant`）和 `content` | 输入输出 [Token](../concepts/token.md) 总和计入 TPM 限流，长对话需注意 [Token](../concepts/token.md) 消耗 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) |

## 使用方式

### 1. 环境准备
- 完成[实名认证](https://help.aliyun.com/zh/account/verify-your-identity-individual-account)，开通百炼服务；
- 在[API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)创建 Key，并配置为环境变量 `DASHSCOPE_API_KEY`；
- 若使用业务空间专属域名，需在[业务空间管理](https://modelstudio.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)页面获取 `WorkspaceId`。

### 2. 发起调用（OpenAI SDK 示例）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 华北2（北京）业务空间专属域名示例（请替换 {WorkspaceId}）
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```

> **注意**：文档1、文档2和文档7对 Base URL 的协议路径描述一致（`/compatible-mode/v1`），但文档5中提及美国（弗吉尼亚）地域的 Dashscope 域名为 `dashscope-us.aliyuncs.com`，而文档7明确列出其 OpenAI 兼容路径为 `https://dashscope-us.aliyuncs.com/compatible-mode/v1`，二者无矛盾；所有地域均支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，无需额外适配 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

### 3. 多语言支持
除 Python 外，也支持 Node.js、curl 等方式调用，详见[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)中的完整示例。

## 限制和注意事项

- **地域隔离**：各地域（北京、新加坡、美国、德国、日本）的 API Key、Base URL、模型列表相互独立，**不可跨地域混用**；建议就近选择地域以降低延迟 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。
- **限流机制**：
  - 默认按主账号维度进行 RPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 数）限流，不同模型额度独立；
  - `qwen3.8-max` 等主力模型采用[动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)，TPM 额度随月消费金额分档提升（如北京地域 ≤10w 档为 500w TPM）；
  - 触发限流时返回 `429` 错误，通常 1 分钟内自动恢复；可通过[提升临时限流额度](https://bailian.console.aliyun.com/?tab=model#/efm/temp_limit_raise)或添加备选模型缓解 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。
- **计费与安全**：
  - 模型推理按 Token 用量计费，知识库（RAG）为独立计费项，两者不互通 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)；
  - 数据全程加密传输，阿里云承诺**不会将用户数据用于模型训练**，符合隐私合规要求 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)；
  - 新用户享有北京地域免费额度，用完后可开启“免费额度用完即停”避免意外扣费 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)


