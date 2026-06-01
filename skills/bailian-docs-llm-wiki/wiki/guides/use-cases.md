# use cases

百炼平台提供了丰富的模型使用场景（Use Cases），涵盖文本生成、图像生成、视频生成、RAG 构建、模型调优与部署，以及多种第三方模型集成等实践。本页面汇总各使用场景的核心要点，帮助开发者快速定位适合自身业务的方案。

## 内容创作类

### 文生文（Prompt 工程）

百炼平台支持通过精心设计的 Prompt 来充分发挥大语言模型能力。关键技巧包括：

- **构建清晰明确的 Prompt**：任务描述越具体、无歧义，模型表现越符合预期
- **使用 Prompt 框架**：包含背景、目的、风格、语气、受众、输出六个维度，系统化引导模型输出
- **Prompt 优化工具**：百炼控制台提供自动优化功能，可对 Prompt 进行扩写和细节添加

详见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。

### 文生图

适用模型：万相-文生图V2、万相-文生图V1。核心参数：

| 参数 | 说明 |
|------|------|
| `prompt` | 正向提示词，支持中英文 |
| `negative_prompt` | 反向提示词，描述不希望出现的内容 |
| `prompt_extend` | （仅V2）是否开启大模型智能改写，默认 true |

提示词公式分为两个层级：
- **基础公式**：主体 + 场景 + 风格
- **进阶公式**：主体描述 + 场景描述 + 定义风格 + 镜头语言 + 氛围词 + 细节修饰

详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。

### 文生视频/图生视频

适用模型：万相系列（wan2.7/wan2.6/wan2.5）及 Vidu。提示词公式：

- **基础公式**：主体 + 场景 + 运动
- **进阶公式**：主体描述 + 场景描述 + 运动描述 + 美学控制 + 风格化
- **图生视频公式**：运动 + 运镜
- **声音公式**（wan2.7/wan2.6/wan2.5）：主体 + 场景 + 运动 + 声音描述
- **多镜头公式**（wan2.7/wan2.6）：总体描述 + 镜头序号 + 时间戳 + 分镜内容
- **参考生视频公式**（wan2.7/wan2.6）：参考指代 + 动作 + 场景 + 台词 + 背景音乐

详见 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。

### 文档转视频

利用大语言模型和多模态技术，将文档自动转换为包含图文、语音、字幕的完整视频。流程包括：文档切片 → 生成演示文稿 → 生成讲解语音与字幕 → 合成视频。依赖工具包括 FFmpeg 和 Marp。

## 第三方模型集成

百炼平台通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)和 DashScope SDK 统一接入多家第三方模型，调用方式一致：

### 支持的模型

| 供应商 | 模型示例 | 特殊说明 |
|--------|----------|----------|
| DeepSeek | deepseek-v4-pro | 支持思考模式，百炼供应商支持联网搜索与上下文缓存 |
| DeepSeek-硅基流动 | siliconflow/deepseek-v3.2 | 支持更长上下文 |
| DeepSeek-快手万擎 | vanchin/deepseek-v4-pro | 仅适用于华北2（北京）地域 |
| Kimi-月之暗面 | kimi/kimi-k2.6 | 支持文本、图像、视频输入 |
| Kimi（百炼部署） | kimi-k2-thinking | 支持华北2、美国、德国多地域 |
| GLM-智谱 | ZHIPU/GLM-5.1 | 智谱供应商支持更长回复长度 |
| GLM（百炼部署） | glm-5.1 | 每个模型各有100万免费Token |
| MiniMax | MiniMax-M2.5, MiniMax/MiniMax-M2.7 | 仅适用于中国内地地域 |
| MiMo-小米 | xiaomi/mimo-v2.5-pro | 默认开启思考模式 |
| Stepfun-阶跃星辰 | stepfun/step-3.7-flash | 默认关闭思考模式，支持 `reasoning_effort` 控制推理深度 |

### 通用调用方式

所有第三方模型均通过统一的 `base_url` 接入：

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="<模型名称>",
    messages=[{"role": "user", "content": "你好"}],
    extra_body={"enable_thinking": True},  # 可选：开启思考模式
    stream=True,
)
```

### 关键参数

| 参数 | 说明 |
|------|------|
| `enable_thinking` | 开启/关闭思考模式。Python SDK 通过 `extra_body` 传入，Node.js SDK 作为顶层参数传入 |
| `reasoning_effort` | 控制推理深度，可选值：`low`、`medium`、`high`（部分模型支持） |
| `reasoning_content` | 返回字段，包含模型的推理过程 |

> **注意**：不同供应商提供的同名模型可能存在功能差异。例如 DeepSeek 模型中，硅基流动供应商支持更长上下文，而阿里云百炼供应商限流更宽松且支持联网搜索与上下文缓存功能。GLM 模型中，智谱供应商支持更长回复长度，百炼供应商提供免费额度。

## RAG 应用构建

通过 LlamaIndex 集成百炼知识库服务，支持文档解析、知识库创建、检索和问答。核心流程：

1. 使用 `DashScopeParse` 解析文档（支持 .doc/.docx/.pdf，单文件 100M/1000 页以内）
2. 通过 `DashScopeCloudIndex.from_documents()` 创建知识库
3. 获取 retriever 或 query engine 进行检索和问答

Python 版本要求：>=3.8 且 <=3.12。

## 模型调优与部署

创建自定义模型涉及三个主要步骤：

1. **模型调优**：准备训练数据（建议至少 500 条），配置训练超参数
2. **模型部署**：部署至独占实例后方可调用和评测
3. **模型评测**：评估效果，不满意可调整策略重复迭代

训练数据需编排为"Prompt-Completion"格式。详见 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

## 性能优化与运维

### 显式缓存

通过在请求中添加 `cache_control` 标记，确保相同输入确定性命中缓存。适用场景：

- 高频复用相同 Prompt（命中可节省 90% 成本）
- 工业级 Agent 长上下文管理
- 支持 Claude Code、Open Code、OpenClaw、Hermes 等工具原生接入

接入端点根据套餐不同：
- 按量计费：`https://dashscope.aliyuncs.com/apps/anthropic`
- Token Plan 团队版：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
- Coding Plan：`https://coding.dashscope.aliyuncs.com/apps/anthropic`

### 限流应对

百炼 API 按主账号维度、模型独立计算限流，包括三种规则：

- **RPM/TPM**：每分钟最大请求数/Token 用量
- **RPS/TPS**：每秒瞬时频率限制
- **Traffic Burst**：短时间流量激增触发

应对方案按改动成本递进：

1. **平台配置**（推荐首选）：服务端排队等待（`X-DashScope-Wait-Timeout` 请求头）、提升限流额度、PTU 预留算力、Batch API 异步处理
2. **客户端流控**：基础重试 → 令牌桶 → 平滑限速器 → 自适应拥塞控制
3. **架构兜底**：模型降级 Fallback、基于消息队列的削峰填谷

## 限制和注意事项

- 第三方模型大多仅适用于**华北2（北京）**地域，需使用对应地域的 API Key
- 使用第三方供应商模型前需在百炼控制台完成**服务开通**和授权
- `enable_thinking` 为非 OpenAI 标准参数，Python SDK 需通过 `extra_body` 传入
- DashScopeParse 解析器仅支持在线解析 .doc/.docx/.pdf 文件，单文件大小 100M 以内、页数 1000 以内
- 自定义模型完成调优后**必须部署才能调用和评测**
- 显式缓存的排队等待功能仅适用于增速/突发限流（Throttling.BurstRate），不适用于 RPM/TPM 绝对值限流

> **注意**：部分文档中 Kimi 模型存在两个来源——月之暗面直供（模型名带 `kimi/` 前缀，如 `kimi/kimi-k2.6`）和百炼部署（直接使用模型名，如 `kimi-k2-thinking`），两者支持的地域和功能有所不同，请根据实际需求选择。

## 来源文档

- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-best-practice.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [DeepSeek大语言模型](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)

