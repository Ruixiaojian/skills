# 向量嵌入

向量嵌入（Vector Embedding）是将原始数据（如文本、图像、视频帧等）映射到高维连续向量空间的数学表示过程，其核心目标是让语义相似的内容在向量空间中距离更近（通常用余弦相似度衡量）。它是百炼平台实现语义搜索、RAG、跨模态检索等能力的基础技术底座。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG 与知识库**：知识库构建时，文档内容（文本、PDF、图片、音视频）被自动切片并调用向量模型生成嵌入，存入向量索引；检索阶段，用户 Query 被向量化后与索引中向量比对，完成语义召回。  
- **语义搜索与多模态检索**：通过 `vector and sort` 功能，支持纯文本、图文混合、视频帧序列等多种输入形式的统一向量化，所有模态向量位于同一语义空间，可直接跨模态计算相似度（如“描述一只金毛犬” → 检索匹配图片）。  
- **框架集成（LlamaIndex / Spring AI Alibaba）**：当使用 LlamaIndex 构建 RAG 或 Spring AI Alibaba 调用知识库时，底层向量化由百炼托管完成，开发者无需自行部署或调用嵌入模型——但可通过参数控制维度、融合策略等行为。  
- **自定义应用开发**：开发者可直接调用 `/api/v1/services/embeddings/text-embedding` 或 [OpenAI 兼容接口](openai-compatible-interface.md) `/compatible-mode/v1/embeddings`，对任意文本或 multimodal content 手动生成向量，用于构建私有检索系统、聚类分析、去重等任务。  
- **模型训练数据准备（非直接使用，但强相关）**：在千问 VL 多模态训练集中，图像/视频帧需经预处理（如 `resized_width`/`fps` 控制）后送入视觉编码器，该过程本质也是嵌入生成，但属于模型内部流程，不对外暴露向量输出。

## 关键参数和配置

| 参数名 | 适用模型 | 说明 | 注意事项 |
|--------|----------|------|----------|
| `model` | 必填 | 指定向量模型名称，例如 `"text-embedding-v4"`、`"qwen3-vl-embedding"`、`"tongyi-embedding-vision-plus-2026-03-06"` | 名称必须严格匹配官方列表，大小写敏感；不同模型支持的输入类型（text/image/video）、是否支持融合、是否支持 `dimensions` 等能力差异显著 |
| `input` / `contents` | 按模型而异 | 文本向量：接受 `string` 或 `string[]`；多模态向量：必须为 `array` of `content` 对象（含 `type` 和 `data` 字段） | `qwen3-vl-embedding` 支持 `enable_fusion=true` 将多个模态融合为单向量；`tongyi-embedding-vision-plus-2026-03-06` 等模型则通过单个 `content` 内混合 text/image/video 实现融合，无需 `enable_fusion` |
| `dimensions` | 可选 | 指定输出向量维度（如 `512`、`1024`），仅部分模型支持（见下表） | 不支持该参数的模型（如 `text-embedding-v2`）将返回固定维度向量；设置过小可能损失语义表达力，过大增加存储与计算开销 |
| `encoding_format` | 文本向量同步模型 | 当前仅支持 `"float"`（默认），暂不支持 base64 编码 | 若需压缩传输，建议客户端自行做 float32 → float16 转换 |
| `enable_fusion` | 仅 `qwen3-vl-embedding` | `true`：将 `contents` 中所有模态融合为一个向量；`false`（默认）：为每个模态生成独立向量 | 其他融合型模型（如 `tongyi-embedding-vision-plus-2026-03-06`）不支持此参数，融合逻辑内置于模型设计中 |

✅ **支持 `dimensions` 的主流模型**：  
`qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`, `tongyi-embedding-vision-flash-2026-03-06`

❌ **不支持 `dimensions` 的模型**：  
`text-embedding-v2/v1`, `tongyi-embedding-vision-plus`（非快照版）, `tongyi-embedding-vision-flash`（非快照版）, `text-embedding-async-v1/v2`

## 面向开发者，简洁实用

- ✅ **优先选新模型**：生产环境推荐使用 `text-embedding-v4`（文本）或 `qwen3-vl-embedding`（多模态），它们支持 `dimensions`、更高 [Token](token.md) 上限（128K）、更优语义一致性。  
- ✅ **[多模态输入](multimodal-input.md)格式要规范**：  
  ```json
  {
    "model": "qwen3-vl-embedding",
    "input": {
      "contents": [
        {"type": "text", "data": "一只奔跑的黑猫"},
        {"type": "image", "data": "base64_encoded_image_data"}
      ]
    },
    "enable_fusion": true
  }
  ```
- ✅ **批量处理大文本？用异步模型**：`text-embedding-async-v2` 支持单次 10 万行、每行 ≤2048 [Token](token.md)，适合离线构建知识库索引。  
- ⚠️ **注意地域限制**：向量服务仅在华北2（北京）可用，调用时确保 `workspaceId` 和 API Key 对应正确地域。  
- ⚠️ **相似度阈值慎设**：知识库检索中，`similarity_threshold` 过高（>0.85）易漏召，建议从 `0.4~0.6` 起调，结合业务效果验证。  
- 📦 **SDK 提示**：DashScope SDK 中，文本嵌入调用 `dashscope.TextEmbedding.call()`，多模态嵌入调用 `dashscope.MultimodalEmbedding.call()`，参数结构与 REST API 一致。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [knowledge](../api/knowledge.md)
- [model data overview](../guides/model-data-overview.md)


