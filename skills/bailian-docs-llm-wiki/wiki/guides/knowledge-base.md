# knowledge base

知识库是阿里云百炼平台基于 RAG（检索增强生成）技术为大模型补充私有数据和最新信息的核心组件。大模型在生成回答前会先从知识库中检索相关内容，从而提升特定领域问答的准确性。知识库支持通过控制台、工作流和 API 三种方式集成到业务应用中。

## 工作原理

知识库的 RAG 流程分为三个核心阶段：

1. **建立索引**：对文件进行解析、切片与向量化处理
2. **检索召回**：根据用户查询，从向量存储中匹配并召回相关知识片段
3. **生成答案**：大模型根据召回的知识片段和用户查询生成最终回答

知识库支持语义检索，即使查询关键词与实际答案完全不同，也能找到语义相关的内容。

## 支持的模型

根据 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) 文档，以下模型支持使用知识库：

**预置模型：**
- 千问系列：QwQ / Long / Max / Plus / Turbo / Coder / Deep-Research
- 千问VL：Max / Plus / Flash / OCR
- 千问开源版：Qwen3、Qwen2.5、Qwen2 等
- 第三方模型：DeepSeek-R1、DeepSeek-V3.1、Llama3.1、Yi-Large 等

**自定义模型（调优后）：**
- 千问 Plus / Turbo
- 千问VL Max / Plus
- 千问开源版（Qwen3、Qwen2.5、Qwen2 等）

> **注意**：支持的模型列表随时可能更新，请以控制台应用管理页面实际可选的模型为准。

## 知识库类型与使用场景

创建知识库时需选择类型（创建后不可更改）：

| 类型 | 适用场景 |
|------|---------|
| **文档搜索 - 基础文档问答** | 纯文本文档的语义检索 |
| **文档搜索 - 图文并茂回复** | 需要返回图文混排内容 |
| **文档搜索 - 视觉理解** | 含复杂排版、图表、公式的 PDF/图片文档，自动使用 qwen3 多模态向量模型 |
| **文档搜索 - 极速问答** | 高度结构化或简单文档（FAQ、参数表），低延迟优化，仅支持文本查询 |
| **数据查询** | 结构化数据（xlsx/xls） |
| **图片问答** | 图片类知识库 |
| **音视频搜索** | 音视频文件的语音识别与内容理解 |

## 知识库规格

根据 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)，知识库分为两种规格：

| 规格 | 最高并发 | 存储空间 | 价格 |
|------|---------|---------|------|
| **标准版** | 1 QPS（固定） | ≤ 100 GB | 0.03 元/知识库/小时 |
| **旗舰版** | 50–10,000 QPS（1–200 RCU） | ≤ 9,999 GB | 0.2 元/RCU/小时 |

- **RCU**（Retrieval Compute Unit）：1 RCU ≈ 最高 50 QPS
- 所需 RCU = 向上取整（峰值 QPS ÷ 50）
- 免费额度：所有用户一次性 720 小时（仅限标准版），新用户 30 天内有效

## 关键参数

### 索引配置（创建时设定，不可更改）

- **切片方式**：推荐使用「智能切分」，基于语义相关性自适应切分；也可选择「按长度切分」
- **向量模型**：文档搜索类支持 text-embedding-v4 / v3（512 维）；图片问答类使用 multimodal-embedding-v1（1024 维）
- **Meta 信息抽取**：为文本切片附加元数据（常量、变量、大模型提取、正则、关键词），提升检索精度
- **多轮对话改写**：根据历史对话自动补全用户查询，创建后不可追加开启

> **注意**：切片方式和 Meta 信息抽取在知识库创建后均**无法更改**，请在创建时慎重配置。

### 检索参数（可动态调整）

| 参数 | 说明 |
|------|------|
| **相似度阈值** | 仅语义相似度高于此阈值的文本才会被召回，设置过高会丢弃相关内容 |
| **召回片段数（TopK）** | 最终返回的切片数量，上限 20。增大可提升回答完整性，但增加 Token 消耗 |
| **权重** | 多知识库场景下按重要程度分配，仅在同类型知识库之间生效 |
| **标签过滤** | 通过文件标签在向量检索前筛选目标文件 |

## 文件格式与上传限制

根据 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)：

| 格式 | 限制 |
|------|------|
| PDF / DOCX / DOC / PPTX 等 | ≤ 100 MB，≤ 1,000 页 |
| TXT / Markdown / HTML | ≤ 10 MB |
| XLSX / XLS | ≤ 10 MB，≤ 10 万行 |
| PNG / JPG / BMP / GIF | ≤ 20 MB |
| 音视频（MP4、MP3 等） | ≤ 512 MB |

其他配额：
- 每个业务空间最多 100,000 个文件、500 个类目、1,000 个数据表
- 单个文件最多 32 个标签
- 单个文本切片上限 6,000 Token

## 集成方式

### 控制台集成

- **智能体应用**：在应用配置中通过「文档知识库」添加已创建的知识库
- **工作流应用**：在画布中添加「知识库」节点，支持固定选择或动态引入知识库

### API 集成

通过阿里云百炼 SDK 调用知识库 API，主要流程：

1. 安装百炼 SDK，配置 AccessKey 和业务空间 ID
2. 上传文件（申请租约 → 上传 → 添加到类目）
3. 创建知识库（CreateIndex）并提交索引任务（SubmitIndexJob）
4. 调用检索接口（Retrieve）获取结果

> **注意**：根据 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)，API 当前仅适用于**文档搜索类**知识库。子账号需获取 `AliyunBailianDataFullAccess` 策略权限。

## 费用构成

知识库总费用 = **规格费用**（运行时长）+ **模型调用费用**（向量化 + 排序）

- **模型调用费用**独立计费，按输入 Token 量计算
- 多个知识库检索时，Token 消耗按知识库数量倍增
- 排序（Rerank）是检索费用的主要部分，费用取决于初步召回的切片总量，而非最终返回数量
- 可通过关闭排序或调低初步召回 TopK 来优化成本
- 欠费后知识库暂停服务；平台存储 15 天未补缴、自购 ADB-PG 8 天未补缴将永久删除数据

## RAG 效果优化

当出现知识召回不完整或不准确时，可按以下方向排查：

| 问题类型 | 优化方向 |
|---------|---------|
| 检索无效（无相关知识） | 补充知识、优化源文件排版、统一实体名称、启用多轮对话改写 |
| 召回不相关 | 添加文件标签进行过滤、配置 Meta 元数据进行结构化搜索 |
| 切片不完整 | 使用智能切分、人工检查并编辑文本切片 |
| 重排不佳 | 调低相似度阈值、增大召回片段数 |
| 模型理解有误 | 更换更大参数或专业领域模型、优化提示词模板 |

建议在优化前通过自动评测功能建立至少 100 组问题的评测基线，以量化衡量改进效果。

## 日志与监控

知识库的检索调用日志通过日志服务（SLS）投递，支持调用审计、问题排查和用量统计。在知识库列表页点击「监控配置」开通后，日志实时投递到 SLS LogStore。

关键日志字段包括：`request_id`（请求 ID）、`pipeline_id`（知识库 ID）、`latency`（耗时毫秒）、`response_code`（业务响应码）、`request_body` / `response_body`（请求/响应体）。

建议搭建的监控：
- 调用量趋势（按小时/天）
- 业务错误率（`response_code != Success`）
- HTTP 5xx 错误率
- TopN 知识库调用排名

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)

