# 文本Embedding与多模态向量对比

## 概述

在构建语义搜索、推荐系统、内容理解等 AI 应用时，向量化（Embedding）是基础环节之一。百炼平台同时提供**通用文本向量**（General Text Embedding）和**多模态向量**（Multimodal Embedding）两类模型服务。前者专注于将纯文本转换为高维数值向量，后者则支持将文本、图像、视频等多种模态统一映射到同一语义空间。本文从输入输出格式、支持模型、接口规范、计费方式和典型场景等关键维度进行对比，帮助开发者根据业务需求做出合理的技术选型。

## 关键维度对比

| 对比维度 | 通用文本向量（Text Embedding） | 多模态向量（Multimodal Embedding） |
|---------|-------------------------------|----------------------------------|
| **输入格式** | 纯文本（字符串、字符串列表、文本文件） | 文本、图片（URL/Base64）、视频（URL）、多图列表，支持混合输入 |
| **输出格式** | 每条文本对应一个浮点向量（float 数组） | 每个输入对应独立向量，或所有输入融合为一个向量 |
| **向量类型** | 独立向量（一条文本 → 一个向量） | 独立向量 + 融合向量（多模态内容可融合为统一表征） |
| **向量维度** | 64–2048 维可选（v4）；v1/v2 固定 1536 维 | 64–2560 维可选（因模型而异）；部分旧模型固定维度 |
| **代表模型** | text-embedding-v4（Qwen3-Embedding）、text-embedding-v3/v2/v1 | qwen3-vl-embedding、qwen2.5-vl-embedding、tongyi-embedding-vision-plus/flash 系列 |
| **API 端点** | OpenAI 兼容：`https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings`；批处理：DashScope 异步接口 | DashScope 原生：`POST /api/v1/services/embeddings/multimodal-embedding/multimodal-embedding` |
| **接口协议** | 同步接口兼容 OpenAI SDK；批处理接口为 DashScope 异步协议 | DashScope 原生 HTTP 协议（非 OpenAI 兼容） |
| **单次最大输入** | 同步：10–25 行/次；批处理：100,000 行/次（≤200MB） | contents 数组（受模型文本 [Token](../concepts/token.md)、图片大小、视频大小限制） |
| **最大 [Token](../concepts/token.md)** | v3/v4：8,192 [Token](../concepts/token.md)/行；v1/v2：2,048 Token/行 | qwen3-vl / qwen2.5-vl：32K Token；tongyi 系列：1K Token；v1：512 Token |
| **图片/视频支持** | ❌ 不支持 | ✅ 图片 ≤5–10MB；视频 ≤10–50MB |
| **跨模态能力** | ❌ 仅文本语义空间 | ✅ 文本、图片、视频位于同一语义空间，可跨模态匹配 |
| **批处理模式** | ✅ 支持异步批处理（text-embedding-async-v1/v2），单次最多 10 万行 | ❌ 暂无独立批处理接口 |
| **免费额度** | 同步 v3/v4 各 100 万 Token；v1/v2 各 50 万 Token；批处理各 2000 万 Token（开通后 90 天） | 按模型定价，具体参见模型计费页面 |
| **计费方式** | 按 Token 数量计费 | 按 Token 数量（文本）+ 图片/视频用量综合计费 |
| **SDK 支持** | OpenAI Python/Java SDK、DashScope SDK、curl | DashScope SDK、curl |
| **语种支持** | v4：100+ 语种及编程语言；v3：50+ 语种；v1/v2：6–10 种语言 | 取决于具体模型，通常支持中英文等主流语种 |

## 适用场景建议

### 选择通用文本向量（Text Embedding）

| 场景 | 说明 |
|------|------|
| **纯文本语义搜索** | 文档检索、FAQ 匹配、知识库问答等仅涉及文本的检索场景 |
| **文本聚类与分类** | 对大量文本进行主题聚类、情感分类、意图识别 |
| **RAG 知识库构建** | 将文档切片后批量向量化存入向量数据库，配合 LLM 进行增强生成 |
| **大规模离线处理** | 利用批处理接口一次性处理数十万条文本，适合数据管线和 ETL 流程 |
| **多语种文本对齐** | 借助 v4 模型覆盖 100+ 语种的能力，实现跨语言语义匹配 |
| **成本敏感型项目** | 纯文本计费单价低，且提供较高免费额度 |

### 选择多模态向量（Multimodal Embedding）

| 场景 | 说明 |
|------|------|
| **以文搜图 / 以图搜文** | 用户输入文字查找匹配图片，或上传图片查找相关文本描述 |
| **以图搜图** | 在图片库中进行视觉相似度检索 |
| **视频语义检索** | 通过文本或图片检索相关视频片段 |
| **商品多模态表征** | 将商品图片 + 描述文本融合为统一向量，提升电商搜索和推荐效果 |
| **内容审核与打标** | 对图文混合内容进行语义分类和聚类分析 |
| **跨模态相似度计算** | 在统一语义空间内衡量不同模态内容之间的语义距离 |

## 技术选型参考

### 决策流程

```
是否涉及图片或视频？
├─ 否 → 选择 通用文本向量
│       ├─ 需要大规模批处理？ → text-embedding-async-v2（批处理接口）
│       ├─ 需要最优效果？ → text-embedding-v4（支持 2048 维）
│       └─ 需要兼容旧系统？ → text-embedding-v2/v1（固定 1536 维）
│
└─ 是 → 选择 多模态向量
        ├─ 需要融合向量？ → qwen3-vl-embedding（enable_fusion=true）或 qwen2.5-vl-embedding
        ├─ 需要独立向量 + 高维？ → tongyi-embedding-vision-plus-2026-03-06
        └─ 追求性价比？ → tongyi-embedding-vision-flash 系列
```

### 关键注意事项

1. **语义空间不互通**：文本向量模型和多模态向量模型产生的向量处于不同的语义空间，不可混合计算相似度。选型时需确保查询端和库端使用同一模型。

2. **维度一致性**：存入向量数据库的向量维度必须与查询时的维度一致。如果使用可变维度模型（如 text-embedding-v4 或 qwen3-vl-embedding），需在项目初期确定维度并保持统一。

3. **接口兼容性**：文本向量同步接口兼容 OpenAI SDK，迁移成本低；多模态向量仅支持 DashScope 原生接口，需使用专用调用方式。

4. **性能与成本权衡**：
   - 文本向量延迟低、吞吐高，适合实时在线服务
   - 多模态向量处理图片/视频时计算开销较大，建议对多媒体内容提前离线向量化

5. **query/document 区分**：文本向量在检索场景中建议区分 query 和 document 类型（通过 DashScope 原生接口或批处理接口的 `text_type` 参数）；多模态向量通过 `instruct` 参数可自定义任务说明以优化检索效果。

6. **模型演进**：text-embedding-v4 属于 Qwen3-Embedding 系列，qwen3-vl-embedding 属于 Qwen3 视觉系列，两者在各自领域均代表最新一代能力，建议新项目优先选用。

## 总结

| 需求特征 | 推荐方案 |
|---------|---------|
| 纯文本、大规模、低成本 | 通用文本向量（text-embedding-v4 / 批处理接口） |
| 涉及图片/视频、跨模态检索 | 多模态向量（qwen3-vl-embedding / tongyi-embedding-vision 系列） |
| 图文融合统一表征 | 多模态向量（启用融合模式） |
| OpenAI SDK 兼容、快速集成 | 通用文本向量（同步接口） |

根据实际业务中涉及的数据模态、检索模式和性能要求，选择合适的向量化方案，可以在效果与成本之间取得最佳平衡。

## 被对比主题页

- [general text embedding](../api/general-text-embedding.md)
- [multimodal vector](../api/multimodal-vector.md)

