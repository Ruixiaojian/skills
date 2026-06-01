# 文本Embedding与多模态向量对比

## 概述

在构建语义搜索、推荐系统、RAG（检索增强生成）等 AI 应用时，开发者常需要将非结构化数据转换为向量表示。百炼平台提供了两类向量化能力：**通用文本向量（General Text Embedding）** 和 **多模态向量（Multimodal Embedding）**。两者均可生成高维数值向量用于下游任务，但在输入模态、模型架构、API 设计和适用场景上存在显著差异。

本文旨在帮助开发者理解两类方案的核心区别，以便根据业务需求快速完成技术选型。

---

## 关键维度对比

| 对比维度 | 文本Embedding | 多模态向量 |
|---------|--------------|-----------|
| **输入格式** | 纯文本（字符串、字符串列表或文本文件） | 文本、图片（URL/Base64）、视频（URL）、多图列表，支持混合输入 |
| **输出格式** | 每条文本返回一个浮点数向量（`float` 数组） | 每个输入项返回独立向量，或将所有输入融合为一个向量 |
| **向量维度** | 64–2048 可选（v4），64–1024 可选（v3），1536 固定（v1/v2） | 因模型而异：最高 2560（qwen3-vl-embedding），部分模型支持维度缩减，部分固定维度 |
| **代表模型** | text-embedding-v4（Qwen3-Embedding）、v3、v2、v1；批处理：async-v2、async-v1 | qwen3-vl-embedding、qwen2.5-vl-embedding、tongyi-embedding-vision-plus/flash 系列、multimodal-embedding-v1 |
| **API 端点** | 同步：`https://dashscope.aliyuncs.com/compatible-mode/v1`（OpenAI 兼容）；批处理：DashScope 异步任务接口 | `POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`（DashScope 原生接口） |
| **SDK 兼容性** | 同步接口兼容 OpenAI SDK（Python/Java/curl）；批处理使用 DashScope SDK | DashScope SDK / HTTP 直接调用 |
| **单次最大输入量** | 同步：10–25 行/次；批处理：100,000 行/次（≤200MB） | 按 `contents` 数组传入，受单请求体大小和模型限制约束 |
| **单条最大 Token** | v3/v4：8,192 Token；v1/v2：2,048 Token | qwen3/2.5-vl-embedding：32K Token；tongyi 系列：1K Token；v1：512 Token |
| **语种支持** | v4：100+ 语种及编程语言；v3：50+；v1/v2：6–10 种 | 依模型而定，主要面向中英文及视觉内容 |
| **融合向量能力** | 不支持（仅产出每条文本的独立向量） | 支持。qwen3-vl-embedding 通过 `enable_fusion=true` 开启；qwen2.5-vl-embedding 始终融合；tongyi 2026-03-06 版本通过同一 content 对象融合 |
| **视频处理** | 不支持 | 支持视频 URL 输入，可配置帧采样率（`fps`）和最大采样帧数（`max_video_frames`） |
| **计费方式** | 按 Token 数计费；同步 v3/v4 免费额度各 100 万 Token，v1/v2 各 50 万 Token；批处理各 2000 万 Token（开通后 90 天内有效） | 按 Token/图片张数/视频时长等多维度计费（具体费率参见各模型计费说明） |
| **批处理能力** | 原生支持异步批处理接口（async-v1/v2），单次最多 10 万行 | 无专用批处理接口，需自行在应用层编排并发请求 |
| **特殊参数** | `text_type`（query/document，仅批处理和 DashScope 原生接口可用）；`dimensions`（v3/v4） | `enable_fusion`、`fps`、`instruct`（自定义任务说明）、`res_level`（分辨率档位）、`max_video_frames` |

---

## 适用场景建议

### 推荐使用文本Embedding的场景

| 场景 | 说明 |
|------|------|
| **纯文本语义搜索** | 文档检索、FAQ 匹配、知识库问答等以文搜文场景，text-embedding-v4 提供高质量文本向量 |
| **RAG 向量知识库构建** | 大规模文档切片后批量向量化入库，可使用批处理接口（单次 10 万行）高效完成 |
| **文本聚类与分类** | 新闻分类、舆情聚类、文本去重等基于文本语义相似度的任务 |
| **多语种文本处理** | v4 支持 100+ 语种，适合跨语言检索和多语种内容理解 |
| **对 OpenAI 接口兼容有要求** | 同步接口完全兼容 OpenAI SDK，便于存量项目迁移 |
| **大规模离线处理** | 批处理接口支持 10 万行/次、200MB 文件，适合 ETL 流水线和离线数据加工 |

### 推荐使用多模态向量的场景

| 场景 | 说明 |
|------|------|
| **跨模态检索** | 以文搜图、以图搜视频、以图搜图等需要不同模态间语义匹配的场景 |
| **图文融合理解** | 电商商品的图片+描述文本融合为统一向量，实现综合语义检索 |
| **视频内容检索** | 基于视频内容生成语义向量，支持视频库搜索和相似视频推荐 |
| **多模态内容审核与分类** | 将图片/视频内容映射到统一语义空间，进行智能分类与打标 |
| **图文混合知识库** | 构建包含图片、文本、视频等多种内容形式的向量知识库 |

---

## 技术选型参考

### 选型决策流程

```
你的输入数据是否包含图片或视频？
├── 否 → 选择 文本Embedding
│       ├── 需要批量处理（>千条）？ → 批处理接口（async-v2）
│       ├── 需要高质量 + 多语种？ → text-embedding-v4
│       └── 存量 OpenAI 项目迁移？ → 同步接口 + OpenAI SDK
└── 是 → 选择 多模态向量
        ├── 需要图文融合表征？ → qwen3-vl-embedding（enable_fusion=true）
        ├── 需要视频理解？ → qwen3-vl-embedding 或 tongyi-vision 系列
        └── 仅需以文搜图/以图搜图？ → tongyi-embedding-vision-plus/flash
```

### 关键选型因素

| 因素 | 建议 |
|------|------|
| **仅处理文本** | 使用文本Embedding，模型更成熟、调用更简单、成本更低 |
| **需要跨模态能力** | 使用多模态向量，确保所有模态的向量在同一语义空间 |
| **向量维度敏感** | 文本Embedding v4 支持 8 档维度（64–2048）灵活选择；多模态中 qwen3-vl-embedding 支持 7 档维度 |
| **超长文本** | 多模态中 qwen3/2.5-vl-embedding 支持 32K Token，优于文本Embedding 的 8K Token 上限 |
| **大规模离线处理** | 文本Embedding 的批处理接口有明确的大规模支持（10 万行/次），多模态需自行编排 |
| **接口兼容性** | 文本Embedding 兼容 OpenAI SDK；多模态仅支持 DashScope 原生接口 |
| **融合表征** | 仅多模态向量支持将多种模态融合为单一向量 |

### 可以组合使用的场景

在实际项目中，两类向量服务并非互斥。例如：

- **混合知识库**：文本文档使用文本Embedding 向量化入库，图片/视频内容使用多模态向量入库，检索时根据 query 类型分别调用对应服务。
- **多级检索管线**：先用文本Embedding 在大规模文本库中粗筛，再用多模态向量对候选结果中的图文内容精排。

> **注意**：文本Embedding 和多模态向量生成的向量**不在同一语义空间**，不能直接进行跨服务的向量相似度比较。如需跨模态匹配，必须统一使用多模态向量模型。

---

## 总结

| 维度 | 文本Embedding | 多模态向量 |
|------|--------------|-----------|
| 核心优势 | 纯文本处理成熟稳定，支持批处理，兼容 OpenAI SDK | 跨模态统一语义空间，支持图文视频融合 |
| 局限性 | 仅支持文本输入 | 无原生批处理接口，API 仅支持 DashScope 格式 |
| 推荐首选模型 | text-embedding-v4 | qwen3-vl-embedding |

根据业务中是否涉及图片、视频等非文本模态来决定技术路线：纯文本场景优先选择文本

## 被对比主题页

- [general text embedding](../api/general-text-embedding.md)
- [multimodal vector](../api/multimodal-vector.md)

