# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有、结构化或非结构化的领域知识，提升回答的准确性与专业性。其本质是将用户上传的文档、表格、音视频等数据解析、切片、向量化后构建可语义检索的索引，并在模型生成前动态召回相关片段作为上下文。该功能仅在中国站华北2（北京）地域可用。

## 支持的模型/功能

知识库支持广泛的预置与自定义模型，包括千问全系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、开源版 Qwen3/Qwen2.5/Qwen2）、以及第三方模型如 DeepSeek-R1、Llama3.1、Yi-Large 等 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。除基础文档问答外，还支持多模态场景：**视觉理解**（PDF/图片版面保留）、**极速问答**（低延迟结构化检索）和**音视频搜索**（语音识别+帧提取+剧情解析）。

知识库可集成至三类应用：**智能体应用**（通过“文档知识库”节点配置）、**工作流应用**（拖入“知识库”节点并连接大模型节点）、以及**外部应用**（通过 SDK 或 REST API 调用）[知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。此外，平台提供独立的 **知识问答服务**（支持拒答、防泄漏、引用溯源）和 **知识检索服务**（支持多库联合、混排、路由），二者均支持最多 15 个知识库绑定 [知识问答 (raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。

> **注意**：文档 1 中列出的“千问-开源版（Qwen3、Qwen2.5、Qwen2等）”在文档 7 的知识问答服务模型列表中仅体现为 `qwen3.6-plus`、`qwen3.7-plus` 等具体版本，且未提及 Qwen2 系列。实际可用模型请以控制台创建时下拉菜单为准，避免依赖过时的泛称列表。

## 关键参数

| 参数类别 | 参数名 | 说明 | 取值范围/默认值 |
|----------|--------|------|-----------------|
| **检索控制** | 相似度阈值 | 过滤排序后低于该分数的切片，过高易漏召 | 0.01–1.0，默认 0.43（文档 1 示例） |
| | TopK（初步向量/关键词） | 向量/关键词阶段召回的切片数，影响 Rerank 费用 | 1–100，默认各 50（文档 7/8） |
| | 最大召回数量 | 排序后最终返回给下游的切片数 | 1–20，默认 5（文档 7/8） |
| **高级能力** | Query 改写 | 开启后优化用户输入，提升检索效果 | 开/关（文档 7/8） |
| | 知识库权重 | 多库场景下，决定同分切片的优先级 | 数值越大越优先（文档 1） |
| | 标签过滤 / 元数据过滤 | 基于文件标签或预设元数据（如 `author`, `date`）进行前置筛选 | 支持字符串匹配（文档 2/7/8） |
| **性能与成本** | RCU（旗舰版） | 检索并发能力单位，1 RCU ≈ 50 QPS | 1–200（文档 9） |

## 使用方式

1. **创建知识库**：进入 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 页面，选择**标准版**（0.03 元/小时）或**旗舰版**（0.2 元/RCU/小时），按三步完成：填写名称/描述 → 选择类型（文档搜索/数据查询/图片问答/音视频搜索）→ 配置数据源（本地上传/OSS/连接器）与索引参数（如启用“多轮对话改写”、“Meta信息抽取”）。
2. **数据同步**：对 OSS、飞书、钉钉等外部源，可通过**数据连接器**创建定时同步规则（周期：1分钟/1小时/1天），实现增量更新 [知识库定时数据同步指南 (raw/application-user-guide/knowledge-base/data-sync-guide.md)](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)。
3. **集成应用**：
   - *智能体应用*：在应用配置页点击“文档知识库”右侧 `+`，添加知识库并设置相似度阈值、权重。
   - *工作流应用*：拖入“知识库”节点，配置 `content` 输入为 `query`，选择知识库（固定或动态），设置 TopK；再连接大模型节点，在提示词中插入 `{知识库1/result}`。
   - *API 调用*：使用 `bailian20231229` SDK，流程为：申请租约 → 上传文件 → 添加文件 → 创建索引 → 提交索引任务 [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。
4. **调试与监控**：通过控制台“命中测试”验证召回效果；开通 SLS 日志服务，分析 `request_id`、`latency`、`response_code` 等字段排查问题 [知识库日志与监控 (raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 限制和注意事项

- **地域限制**：知识库功能**仅限华北2（北京）地域**，新加坡、法兰克福等其他地域不支持 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **配额限制**：单账号知识库数量无硬上限（RDS 数据源除外），但单个知识库文件数无限制，而单次控制台导入上限为 50 个文件；文本切片长度上限为 6000 [Token](../concepts/token.md) [知识库配额与限制 (raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **元数据与标签**：知识库创建后**无法再配置 Meta 信息抽取**，必须在创建时设定；标签可在上传时或数据管理页编辑，用于运行时过滤 [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。
- **计费要点**：费用 = **规格费**（按小时，标准版/旗舰版） + **模型调用费**（向量化、Rerank、路由、问答生成）。其中 Rerank 费用取决于**初步召回总切片数**（TopK之和），而非最终返回数；多知识库会线性增加 [Token](../concepts/token.md) 消耗 [知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。
- **文件处理**：PDF/DOCX 建议先转 Markdown 再导入；避免合并单元格表头；音视频解析耗时与文件时长正相关（30分钟音频约需 5–15 分钟）[RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)


