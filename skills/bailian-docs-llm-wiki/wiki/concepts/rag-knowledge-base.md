# RAG 检索增强生成

RAG（Retrieval-Augmented Generation，检索增强生成）通过先从外部数据源召回相关片段，再交由大模型基于这些片段生成回答，弥补模型在私有知识、时效信息和领域专业性上的不足。在百炼平台上，RAG 既以**托管知识库**的形态深度内置到智能体 / 工作流应用中，也可通过 SDK、OpenAPI 或主流开发框架（LlamaIndex、Spring AI Alibaba）在外部应用里消费。

## 在百炼平台的使用场景

### 托管知识库（推荐）

百炼知识库（Bailian Knowledge Base）将整套 RAG 链路托管在云端：**文件解析 → 切分 → 向量化 → 落入向量库 → 检索召回 → Rerank → 拼接到 Prompt**。开发者只需上传文档、配置索引参数，即可被智能体或工作流应用调用。

知识库类型在创建后不可更改，应按数据形态与业务场景选择：

- **文档搜索**（非结构化）：PDF/Word/Markdown/图片等。细分四种模式：
  - 基础文档问答（纯文本语义检索）
  - 图文并茂回复（抽取插图摘要，按需返回图片）
  - 视觉理解（使用 `qwen3-vl-embedding` 对整页做版面级理解）
  - 极速问答（低延迟，适合 FAQ）
- **数据查询（NL2SQL / Chatbot）**：结构化 Excel / RDS，要求多文件表头一致，可按列开关「参与检索 / 参与模型回复」。
- **图片问答**：数据表中需含 `image_url` 字段（公网可访问，单图 ≤ 3 MB）。
- **音视频搜索**：MP3/WAV/MP4/MOV，按时间轴对齐语音识别与视频帧。

### 智能体 / 工作流应用集成

- **智能体（Agent 2.0）**：知识库以「工具」形式挂载，由智能体自主规划是否检索；可按标签限定查询范围。
- **智能体（Agent 1.0）**：知识库先行检索，再决策是否调用其他工具，流程更固定。
- **工作流**：拖入「知识库」节点，输入变量绑定到 `query`，输出 `result` 变量供下游大模型节点拼装到提示词。支持「固定选择」或通过 `CodeList` 变量「动态引入」。

### 外部应用（SDK / OpenAPI）

通过百炼 SDK 调用知识库接口，完整链路：

```
ApplyFileUploadLease → AddFile → SubmitIndexJob → Retrieve
```

前置条件：子账号挂载 `AliyunBailianDataFullAccess`，并设置环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID`、`ALIBABA_CLOUD_ACCESS_KEY_SECRET`、`WORKSPACE_ID`。

### 开发框架集成

| 框架 | 语言 | 关键组件 / 类 |
| --- | --- | --- |
| LlamaIndex | Python ≥ 3.9 | `DashScopeParse`（解析）、`DashScopeCloudIndex`（云端索引）、`DashScopeRerank`（重排） |
| Spring AI Alibaba | Java，JDK 17+，Spring Boot 3.x | `DashScopeDocumentRetriever` + `DocumentRetrievalAdvisor` |

LlamaIndex 方案使用百炼默认的智能切分与官方向量模型，不支持自定义切分方式或自定义 Embedding；若需要更灵活的控制，可改用「本地知识库 + 通义千问 API」自建 RAG。

## 关键参数与配置

### 索引侧（创建知识库时配置，多数创建后不可改）

| 参数 | 说明 | 默认 / 推荐 |
| --- | --- | --- |
| 向量模型 | 文档/数据/音视频：`text-embedding-v4`（推荐）或 `text-embedding-v3`，均 512 维；图片问答：`multimodal-embedding-v1`（1024 维）；视觉理解：自动使用 `qwen3-vl-embedding` | v4 |
| 切片方式 | 智能切分 / 按长度（建议重叠 10–25%） / 按页 / 按标题 / 按正则 / 按符号；单切片上限 6000 Token | 智能切分 |
| 排序模型（Rerank） | `qwen3-rerank（hybrid）`（语义 + BM25）或 `qwen3-rerank`（仅语义）；图片问答不支持 Rerank，视觉理解 / 极速问答不支持排序模式配置 | hybrid |
| 排序模式 | 问答模式 / 相似模式 / 自定义高级（≤200 字自然语言指令） | 问答模式 |
| Meta 抽取 | 常量 / 变量（`file_name`、`cat_name`）/ 大模型 / 正则 / 关键词；可开启「参与检索 / 参与模型回复」 | 关闭 |
| 多轮对话改写 | 用轻量模型基于历史对话补全当前查询 | 关闭 |
| 相似度阈值 | 仅高于此值的切片被召回，应用侧可覆盖；视觉理解默认 0.20 | — |
| 最大召回数量 K | 排序后送入大模型的切片数，上限 20 | — |
| 向量存储 | 内置（免费）或 ADB-PG（需开启向量引擎优化，自购计费） | 内置 |

> 知识库创建后**仅名称、描述、相似度阈值可修改**，其余索引参数固化；类型、`image_url` 字段、向量模型等均不可变更。

### 应用侧 / 框架侧常用参数

LlamaIndex：

```python
Settings.llm = DashScope(model_name="qwen-max")  # 生成模型
similarity_top_k = 5       # 检索返回最大结果数
similarity_cutoff = 0.4    # 最低相似度阈值
top_n = 1                  # Rerank 后保留结果数
```

Spring AI Alibaba（YAML）：

```yaml
spring:
  ai:
    dashscope:
      api-key: ${AI_DASHSCOPE_API_KEY}
      # workspace-id: ${AI_DASHSCOPE_WORKSPACE_ID}  # 子业务空间需要
```

Java 关键代码：

```java
DocumentRetriever retriever = new DashScopeDocumentRetriever(dashscopeApi,
    DashScopeDocumentRetrieverOptions.builder().withIndexName(INDEX_NAME).build());

this.chatClient = builder
    .defaultAdvisors(new DocumentRetrievalAdvisor(retriever, retrievalSystemTemplate))
    .build();
```

### Rerank 开关位置（易踩坑）

Rerank 配置错位可能产生**非预期费用**，三种调用方式优先级不同：

- **旧版智能体 / 工作流**：在应用页知识库「调试」处设置「重排策略」开关；**应用内配置优先级高于知识库**。
- **新版智能体（Agent 2.0）**：在知识库卡片「命中测试」中将「选择排序模型」设为「不使用模型」即可走知识库自身配置。
- **OpenAPI**：可在控制台或命中测试页设置，亦可通过 `Retrieve` 接口参数覆盖；**API 参数优先级最高**。

## 命中测试与效果优化

- **命中测试**用于在不调用大模型的情况下模拟提问、验证召回质量并调优阈值。相同切片在不同排序模式下分数差异显著（同一切片可从问答模式 47% 到相似模式 69%）。
- 若召回不全或回答不准，按「RAG 效果优化」流程依次排查切片质量、向量模型、Rerank 开关、阈值、Meta 抽取与多轮改写等环节。
- 召回的文本切片会**占用模型上下文窗口并增加输入 Token**，结合模型上限与单切片 6000 Token 上限设计召回数量 K。

## 模型支持

知识库挂载到智能体 / 工作流应用后，与应用所选模型协同工作。预置可选包括千问 QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、千问 VL-Max/Plus/Flash/OCR、千问开源版（Qwen3/2.5/2），以及 DeepSeek-R1/V3.1、abab6.5s、Llama3.1、Yi-Large 等第三方模型；自定义调优模型支持千问 Plus/Turbo、千问 VL-Max/Plus、千问开源版。**最终可选清单以控制台为准**，会随版本动态更新。

## API Key 环境变量差异（注意）

不同框架对 API Key / WorkspaceId 的环境变量命名并不统一：

| 场景 | 推荐环境变量 |
| --- | --- |
| 外部 SDK 调用知识库接口 | `ALIBABA_CLOUD_ACCESS_KEY_ID` / `ALIBABA_CLOUD_ACCESS_KEY_SECRET` / `WORKSPACE_ID` |
| Spring AI Alibaba（知识库检索） | `AI_DASHSCOPE_API_KEY` / `AI_DASHSCOPE_WORKSPACE_ID` |
| Spring AI Alibaba（应用调用） | `DASHSCOPE_API_KEY` |
| LlamaIndex | 按「配置 API Key 到环境变量」文档设置 |

建议以各示例工程的 `application.yml` / 文档为准，混用容易导致鉴权失败。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [llm application](../guides/llm-application.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)
- [application component api reference](../api/application-component-api-reference.md)


