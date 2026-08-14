# 向量嵌入

向量嵌入（Vector Embedding）是将原始数据（如文本、图像、视频等）映射到高维连续向量空间的数学表示方法，其核心目标是让语义相似的内容在向量空间中距离更近。该表示可被用于语义搜索、相似度计算、聚类、RAG 检索等下游任务。

## 在百炼平台的不同场景中如何使用

- **语义检索与 RAG**：知识库构建时，文档内容经自动切片后由嵌入模型（如 `qwen3.7-text-embedding` 或 `qwen3-vl-embedding`）生成向量，并存入向量索引；用户查询时，查询文本也被向量化，通过向量相似度（如余弦相似度）召回最相关片段。
- **多模态理解**：`qwen3-vl-embedding` 等多模态嵌入模型支持统一处理文本、图像、视频输入；可通过 `enable_fusion=true` 生成跨模态融合向量，实现图搜文、文搜图等跨模态检索。
- **批量预处理**：对海量文档（如 10 万行文本或 ≤200MB 文件），使用异步批处理接口（如 `text-embedding-async-v2`）高效生成向量，适用于离线建库、定期更新等场景。
- **框架集成**：LlamaIndex 和 Spring AI Alibaba 等框架通过 `DashScopeCloudIndex` 或 `DashScopeDocumentRetriever` 底层调用百炼嵌入服务，无需自行部署模型或管理向量存储。

## 关键参数和配置

| 参数 | 说明 | 是否必选 | 适用模型示例 |
|------|------|----------|--------------|
| `model` | 指定嵌入模型名称 | 必选 | `qwen3.7-text-embedding`, `qwen3-vl-embedding`, `text-embedding-v4` |
| `input` | 输入数据，支持 `string`、`array<string>`、`file` 或含 `text`/`image`/`video` 字段的对象 | 必选 | 所有嵌入模型 |
| `dimensions` | 指定向量维度（如 `1024`），仅部分新模型支持 | 可选 | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding` |
| `encoding_format` | 输出格式：`"float"`（默认）或 `"base64"`（节省带宽） | 可选 | 同步文本嵌入模型 |
| `enable_fusion` | 多模态输入时是否融合为单一向量（`true`）或独立生成（`false`，默认） | 可选 | `qwen3-vl-embedding` |

> ⚠️ 注意：  
> - `text-embedding-v2/v1` 等旧版模型不支持 `dimensions` 参数；  
> - 多模态嵌入必须按规范构造 `input` 对象（如 `{ "text": "...", "image": "data:image/png;base64,..." }`）；  
> - 异步批处理需通过 `task_id` 轮询获取结果，不支持实时返回。

## 面向开发者的小贴士

- **选型建议**：实时低延迟场景用同步模型（如 `qwen3.7-text-embedding`）；大批量建库优先用异步接口（`text-embedding-async-v2`）；图文混合内容务必选用 `qwen3-vl-embedding` 并显式设置 `enable_fusion`。
- **性能优化**：向量维度越低（如 `512`），存储与检索开销越小，但可能损失细微语义区分力；建议在业务效果与成本间做 A/B 测试。
- **调试技巧**：使用控制台「知识库命中测试」或直接调用 `/v1/embeddings` 接口验证输入输出，注意检查 `status_code=200` 与 `data[0].embedding` 长度是否符合预期维度。
- **计费提示**：所有嵌入调用按实际输入 [Token](token.md) 计费，多模态输入中图像/视频会按帧或分辨率折算 [Token](token.md)，详见各模型文档。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [data connection overview](../guides/data-connection-overview.md)


