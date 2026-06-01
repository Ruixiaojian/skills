# get started with models

阿里云百炼提供兼容 OpenAI 的大模型调用服务，集成千问（Qwen）全系列及 DeepSeek、Kimi、GLM 等第三方模型。开发者只需获取 API Key、选择模型和地域，即可通过几行代码完成模型调用。本文汇总模型接入的核心信息，帮助您快速上手。

## 支持的模型与能力

百炼覆盖多种模态和任务类型，详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)：

| 能力类别 | 代表模型 | 说明 |
|---------|---------|------|
| **文本生成** | qwen3.7-max、qwen3.6-plus、qwen3.6-flash | Max 效果最强，Plus 均衡推荐，Flash 低延迟高性价比 |
| **文本生成（第三方）** | deepseek-v4-pro、kimi-k2.6、glm-5.1 | API 格式与千问一致，DeepSeek 仅支持北京地域 |
| **视觉理解** | qwen3.6-plus、qwen3.5-omni-plus | 分析图片/视频内容，返回文本或结构化结果 |
| **图像/视频生成** | wan2.7-image-pro、happyhorse-1.0-t2v | 文生图、图生视频、视频编辑等 |
| **语音识别与合成** | cosyvoice-v3.5-plus、fun-asr-realtime | TTS、ASR、端到端语音对话 |
| **向量与重排序** | text-embedding-v4、qwen3-rerank | 文本/图文向量化，检索增强 |

千问旗舰模型选型建议：
- **qwen3.7-max**：推理能力最强，适合复杂多步骤任务
- **qwen3.6-plus**：效果、速度和成本均衡，多数场景推荐
- **qwen3.6-flash**：高性价比低延迟，适合简单任务快速响应

## 接入准备

### 1. 获取 API Key

1. 注册阿里云账号并完成实名认证
2. 前往 [百炼控制台](https://bailian.console.aliyun.com/?tab=model#/model-market) 开通服务
3. 在 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建密钥

### 2. 配置环境变量

建议将 API Key 存入环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露风险。完整的各平台（Linux/macOS/Windows）配置步骤请参见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

```bash
# Linux / macOS 永久生效
echo 'export DASHSCOPE_API_KEY="sk-xxx"' >> ~/.bashrc
source ~/.bashrc
```

```cmd
# Windows CMD 永久生效
setx DASHSCOPE_API_KEY "sk-xxx"
```

### 3. 选择地域

每个地域有独立的 Base URL、API Key 和模型列表，**不可跨地域混用**。详见 [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)。

| 地域 | Base URL（OpenAI 兼容） | 典型场景 |
|------|------------------------|---------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 数据不出中国内地 |
| 新加坡 | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` | 数据不经过中国内地 |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` | 全球推理或限定美国境内 |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` | 全球推理或限定欧盟境内 |

> **注意**：弗吉尼亚地域要限定美国境内推理，需使用 `-us` 后缀模型名（如 `qwen-plus-us`）；法兰克福需先创建业务空间获取 WorkspaceId。

## 调用方式

百炼兼容 OpenAI 接口规范，支持 OpenAI SDK、DashScope SDK 和 curl 三种方式。以下为 OpenAI SDK 示例：

### Python

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.6-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"}
    ]
)
print(completion.choices[0].message.content)
```

### Node.js

```javascript
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
});

const completion = await openai.chat.completions.create({
    model: "qwen3.6-plus",
    messages: [{ role: "user", content: "你是谁？" }],
});
console.log(completion.choices[0].message.content);
```

### curl

```bash
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.6-plus",
    "messages": [{"role": "user", "content": "你是谁？"}]
  }'
```

> **注意**：文档 1（平台概述）和文档 2（首次调用）中的示例代码使用了不同的默认模型名称（分别为 `qwen3.6-plus` 和 `qwen-plus`），两者均可用。`qwen3.6-plus` 为更新版本，建议优先使用。

## 限流与配额

百炼按**主账号维度**对模型调用进行限流，账号下所有 RAM 子账号、业务空间和 API Key 的调用量合并计算。不同模型的限流额度相互独立。详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

### 典型限流额度（中国内地/北京）

| 模型 | RPM（每分钟请求数） | TPM（每分钟 Token 数） |
|------|------|------|
| qwen3.7-max | 30,000 | 5,000,000 |
| qwen3.6-plus | 30,000 | 5,000,000 |
| qwen3.6-flash | 30,000 | 10,000,000 |

### 常见限流错误

| 错误信息 | 原因 | 建议 |
|---------|------|------|
| `Requests rate limit exceeded` | 超出 RPM | 降低调用频率 |
| `Allocated quota exceeded` | 超出 TPM | 缩短输入或限制输出长度 |
| `Request rate increased too quickly` | 瞬时请求激增 | 采用匀速调度或指数退避 |

### 缓解限流的策略

1. **优先选用稳定版模型**（如 `qwen-plus`），限流额度通常高于带日期的快照版本
2. **添加备选模型**：主模型触发限流时自动切换到备用模型
3. **使用批量推理**（Batch API）：无实时性要求时不受实时限流约束
4. **提升临时额度**：在控制台 [限流提额](https://bailian.console.aliyun.com/?tab=model#/efm/temp_limit_raise) 页面申请，提交后立即生效，有效期 30 天

## 各地域功能差异

| 功能 | 北京 | 新加坡 | 弗吉尼亚 | 法兰克福 |
|------|:----:|:------:|:--------:|:--------:|
| 实时推理 | ✅ | ✅ | ✅ | ✅ |
| 批量推理 | ✅ | ✅ | ❌ | ❌ |
| 模型调优 | ✅ | ❌ | ❌ | ❌ |
| 模型告警 | ✅ | ✅ | ❌ | ❌ |

## 计费概要

- 开通百炼**不收费**，调用模型时按量付费（按分钟出账）
- 新用户可获得北京地域专属免费额度，用完后自动转为按量付费
- 可开启「免费额度用完即停」避免意外扣费
- 删除所有 API Key 可从源头阻断调用，防止产生费用

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)

