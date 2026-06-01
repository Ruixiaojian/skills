# get started with models

阿里云百炼是一站式大模型开发与应用平台，提供兼容 OpenAI 的 API 接口，集成千问（Qwen）全系列及 DeepSeek、Kimi、GLM 等第三方模型。开发者只需几行代码即可完成模型调用，支持 Python、Node.js、curl 等多种方式接入。

## 支持的模型与能力

百炼提供开箱即用的模型服务，覆盖多种模态和场景。详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

### 文本生成

| 层级 | 代表模型 | 适用场景 |
|------|----------|----------|
| 旗舰 | qwen3.7-max | 复杂、多步骤任务，推理能力最强 |
| 均衡 | qwen3.6-plus | 效果、速度、成本均衡，多数场景推荐 |
| 高性价比 | qwen3.6-flash | 快速响应的简单任务 |
| 第三方 | deepseek-v4-pro、kimi-k2.6、glm-5.1 等 | API 格式与千问一致 |

### 其他模态

- **视觉理解**：qwen3.6-plus、qwen3.5-omni-plus
- **图像/视频生成**：wan2.7-image-pro、happyhorse-1.0-t2v
- **语音识别与合成**：cosyvoice-v3.5-plus、fun-asr-realtime
- **向量与重排序**：text-embedding-v4、qwen3-rerank
- **全模态**：qwen3.5-omni-plus-realtime

## 地域与接入信息

调用前需选择地域，不同地域的 Base URL、API Key 和模型列表**不能跨地域混用**。详见 [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)。

| 地域 | Base URL（OpenAI 兼容） | 数据合规 |
|------|------------------------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 数据不出中国内地 |
| 新加坡 | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` | 数据不经过中国内地 |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` | 全球/限美国境内 |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` | 全球/限欧盟境内 |

> **注意**：德国（法兰克福）地域需先创建业务空间并获取 WorkspaceId，替换 Base URL 中的占位符。

## 快速开始

完整的首次调用流程请参考 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 1. 获取 API Key

前往 [API Key 管理页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建 Key，并配置到环境变量：

```bash
# Linux/macOS
export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"

# Windows CMD
setx DASHSCOPE_API_KEY "YOUR_DASHSCOPE_API_KEY"
```

### 2. 调用模型

百炼兼容 OpenAI 接口规范，只需调整 `api_key`、`base_url` 和模型名称即可迁移现有代码。

**Python 示例：**

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
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'}
    ]
)
print(completion.choices[0].message.content)
```

**curl 示例：**

```bash
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.6-plus",
    "messages": [{"role": "user", "content": "你是谁？"}]
}'
```

### SDK 选择

| SDK | 安装命令 |
|-----|---------|
| OpenAI Python SDK | `pip install -U openai` |
| DashScope Python SDK | `pip install -U dashscope` |
| OpenAI Node.js SDK | `npm install openai` |

## 限流与配额

百炼按**主账号维度**对模型调用设置限流（RPM/TPM），账号下所有 RAM 子账号和 API Key 的调用量合并计算。详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

### 主要限流指标

- **RPM**（Requests Per Minute）：每分钟请求数
- **TPM**（Tokens Per Minute）：每分钟消耗 Token 数（含输入与输出）

典型限流额度（中国内地）：

| 模型 | RPM | TPM |
|------|-----|-----|
| qwen3.7-max | 30,000 | 5,000,000 |
| qwen3.6-plus | 30,000 | 5,000,000 |
| qwen3.6-flash | 30,000 | 10,000,000 |

> **注意**：限流策略可能按秒级 RPS（RPM/60）与 TPS（TPM/60）执行，短时间内的请求爆发即使未达分钟总量也可能触发限流。

### 触发限流后的处理

1. 通常一分钟内自动恢复
2. 降低调用频率或减少 Token 消耗
3. 添加备选模型进行自动切换
4. 使用批量推理（Batch API）替代实时调用
5. 在控制台 [限流提额](https://bailian.console.aliyun.com/?tab=model#/efm/temp_limit_raise) 页面提升临时 TPM 额度（提交即生效，有效期 30 天）

## 注意事项

- **环境变量优先**：避免在代码中硬编码 API Key，建议通过环境变量 `DASHSCOPE_API_KEY` 传入
- **地域隔离**：不同地域的 API Key、Base URL 和可用模型列表不通用
- **功能差异**：模型调优仅华北2（北京）支持；批量推理仅北京和新加坡支持
- **计费方式**：开通免费，调用按量付费；新用户有北京地域专属免费额度
- **数据安全**：用户数据不用于模型训练，传输全程加密

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)

