# use cases

百炼平台提供了丰富的使用案例，涵盖 Prompt 工程、多模态内容生成、第三方模型集成、RAG 应用构建、模型调优以及生产环境最佳实践等方面。本页面按功能类别梳理了各使用案例的核心内容和适用场景，帮助开发者快速定位所需文档。

## Prompt 工程指南

百炼提供了针对不同模态的 Prompt 编写指南，是上手各类生成任务的基础。

### 文生文 Prompt

[文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md) 介绍了面向大语言模型（LLM）的 Prompt 设计方法，核心要点包括：

- **构建清晰明确的 Prompt**：任务描述越具体，模型输出越符合预期。
- **使用 Prompt 框架**：按"背景 → 目的 → 风格 → 语气 → 受众 → 输出"六要素组织 Prompt，系统化地引导模型生成高质量结果。
- **Prompt 优化工具**：百炼控制台提供自动优化功能，可对 Prompt 进行扩写和细节添加（会消耗 Token）。

### 文生图 Prompt

[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md) 适用于万相文生图 V1/V2 模型，关键参数：

| 参数 | 说明 |
|------|------|
| `prompt` | 正向提示词，支持中英文 |
| `negative_prompt` | 反向提示词，描述不希望出现的内容 |
| `prompt_extend` | （仅 V2）是否启用大模型智能改写，默认 `true` |

提示词公式分两级：
- **基础公式**：主体 + 场景 + 风格
- **进阶公式**：主体描述 + 场景描述 + 定义风格 + 镜头语言 + 氛围词 + 细节修饰

文档还提供了景别、视角、镜头类型、风格、光线等维度的提示词词典。

### 文生视频 / 图生视频 Prompt

[文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md) 适用于万相系列视频模型，提供了多种公式：

- **基础公式**：主体 + 场景 + 运动
- **进阶公式**：主体描述 + 场景描述 + 运动描述 + 美学控制 + 风格化
- **图生视频公式**：运动 + 运镜（图像已确定主体和风格）
- **声音公式**（wan2.7/2.6/2.5）：增加人声、音效、背景音乐描述
- **多镜头公式**（wan2.7/2.6）：总体描述 + 镜头序号 + 时间戳 + 分镜内容
- **参考生视频公式**（wan2.7/2.6）：支持通过"图n"/"视频n"指代参考素材

> **注意**：wan2.7 模型不再支持 `shot_type` 参数指定单镜头/多镜头，改为由模型结合提示词自动判断。如需控制一镜到底，需在 prompt 中写明"生成单镜头"。

### Vidu 视频生成 Prompt

Vidu 模型的提示词公式为"主体/场景 + 场景描述 + 环境描述 + 艺术风格/媒介"，支持通过特定关键词触发动态控制（如"大动态"）、运镜控制（如"镜头推进"）、画面风格（如"2D动漫风格"）和特效（如"爆炸特效"）。

## 第三方模型集成

百炼平台通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)和 DashScope SDK 统一接入多家第三方模型，调用方式高度一致。

### 支持的模型

| 模型系列 | 供应商 | 代表模型 | 地域限制 |
|---------|--------|---------|---------|
| DeepSeek | 百炼 / 硅基流动 / 快手万擎 | `deepseek-v4-pro`、`siliconflow/deepseek-v3.2`、`vanchin/deepseek-v4-pro` | 华北2（北京） |
| Kimi | 百炼 / 月之暗面 | `kimi-k2-thinking`、`kimi/kimi-k2.6` | 华北2（北京）、美国（弗吉尼亚）、德国（法兰克福） |
| GLM | 百炼 / 智谱 | `glm-5.1`、`ZHIPU/GLM-5.1` | 华北2（北京） |
| MiniMax | 百炼 / 稀宇科技 | `MiniMax-M2.5`、`MiniMax/MiniMax-M2.7` | 中国内地 |
| MiMo | 小米 | `xiaomi/mimo-v2.5-pro` | 华北2（北京） |
| Step | 阶跃星辰 | `stepfun/step-3.7-flash` | 华北2（北京） |

> **注意**：同一模型系列不同供应商的差异需关注——例如 DeepSeek 的硅基流动供应商支持更长上下文，百炼供应商限流更宽松且支持联网搜索和上下文缓存；GLM 的智谱供应商支持更长回复长度，百炼供应商提供免费额度和阶梯计费。

### 统一调用方式

所有第三方模型均通过以下方式调用：

- **Base URL**：`https://dashscope.aliyuncs.com/compatible-mode/v1`
- **认证**：使用百炼 API Key
- **思考模式**：通过 `enable_thinking` 参数控制（Python SDK 使用 `extra_body` 传入，Node.js SDK 作为顶层参数传入）
- **推理深度**：部分模型支持 `reasoning_effort` 参数（`low`/`medium`/`high`）

### 前提条件

1. 获取 API Key 并配置到环境变量
2. 安装 OpenAI 或 DashScope SDK
3. 部分第三方直供模型需在百炼控制台搜索并单独开通

## 应用开发

### 基于 LlamaIndex 构建 RAG 应用

通过 `llama-index-indices-managed-dashscope` 包接入百炼知识库服务，核心流程：

1. **文档解析**：使用 `DashScopeParse` 解析 .doc/.docx/.pdf 文件（单文件 ≤100MB、≤1000 页）
2. **创建知识库**：`DashScopeCloudIndex.from_documents()` 自动创建
3. **检索与查询**：通过 `index.as_retriever()` 获取 retriever，或 `index.as_query_engine()` 获取 query engine

环境要求：Python ≥3.8 且 ≤3.12。

### 借助大模型将文档转换为视频

整体流程分四步：文档切片 → 生成演示文稿 → 生成讲解语音与字幕 → 合成视频。依赖 FFmpeg 和 Marp 工具，提供完整代码包。

## 模型调优与部署

百炼支持基于通用模型创建自定义模型，流程为：

1. **训练数据准备**：收集业务数据并编排为"Prompt-Completion"格式，建议至少 500 条
2. **模型调优**：配置超参数（学习率、迭代次数等），平台自动训练
3. **模型部署**：部署到独占实例后方可调用和评测
4. **模型评测**：支持自动化评测，不满意可调整策略迭代

> **注意**：完成调优的模型**必须部署后**才能调用和评测，部署会产生持续计费。

## 生产环境最佳实践

### 限流应对

百炼 API 按主账号维度、模型独立计算限流，触发后通常 1 分钟内恢复。三种限流规则：

- **分钟级配额**（RPM/TPM）
- **瞬时频率**（RPS/TPS）
- **增速限制**（Traffic Burst）

应对方案按改动成本从低到高：

| 层级 | 方案 | 适用场景 |
|------|------|---------|
| 平台配置 | 服务端排队等待（`X-DashScope-Wait-Timeout` 请求头） | Traffic Burst，推荐首选 |
| 平台配置 | 提升限流额度、PTU、Batch API | 持续高吞吐需求 |
| 客户端 | 重试 → 令牌桶 → 平滑限速器 → 自适应拥塞控制 | 需要精细流控 |
| 架构兜底 | 模型降级（Fallback）、消息队列削峰填谷 | 高可用架构 |

### 显式缓存

通过在请求中添加 `cache_control` 标记实现 100% 确定性命中缓存，首次写入额外开销为标准价格的 25%，后续命中可节省 90% 成本。适用场景：

- 高频复用相同 Prompt
- Agent 长上下文管理
- 需要稳定命中缓存的业务

Claude Code、Open Code、OpenClaw、Hermes 等工具通过 Anthropic 协议接入百炼时原生支持显式缓存，无需额外配置。

## 限制和注意事项

- 第三方直供模型（如硅基流动 DeepSeek、月之暗面 Kimi、智谱 GLM 等）通常仅适用于华北2（北京）或中国内地地域，需使用对应地域的 API Key。
- `enable_thinking` 是非 OpenAI 标准参数，不同 SDK 传入方式不同。
- 文档解析器 `DashScopeParse` 仅支持在线解析 .doc/.docx/.pdf，单文件 ≤100MB 且 ≤1000 页。
- 自定义模型的 PTU 部署为预留资源，未满负荷使用也持续计费，需根据实际峰值评估规格。

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

