# 文件处理与引用

文件处理与引用是百炼平台中统一管理、解析与接入非结构化数据的核心横切能力，指将本地或外部文件（如 PDF、Word、Excel、Markdown 等）上传至平台，生成唯一标识（`file_id`），并在模型调用、知识库构建、智能体执行、工作流节点等场景中按需引用其内容或元数据的行为。该能力不绑定具体模型，而是作为基础设施层提供标准化的文件生命周期管理与上下文注入机制。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型直调（File ID 引用）**：通过文件管理 API 上传文件后，获取 `file_id`，在 `messages.content` 中以 `{"type": "file", "file_id": "file-xxx"}` 形式嵌入请求体。模型（如 Qwen3、Qwen-VL、Yi-Large 等）将自动解析并理解文件语义，适用于单次问答、多轮对话中的文档参考。
  
- **知识库构建**：文件可作为知识源导入知识库（支持平台托管或 OSS 连接器）。上传后需显式触发索引任务；平台对内容进行分块、向量化与语义索引，后续检索时返回带溯源信息的切片（含 `file_id`、页码、段落位置等），供 RAG 流程使用。

- **数据连接器集成**：文件类连接器（如“本地文件”“OSS 文件”）支持批量上传与标签化管理。上传时可指定 `tags`，调用 `searchFile` 工具时通过 `tags` 参数精准过滤；表格类连接器还支持自动 Schema 推导与字段类型定义，供 SQL 或自然语言查询使用。

- **Skill 调用**：官方或自定义 Skill（如 `pdf-parser`、`xlsx-converter`）可直接接收 `file_id` 或文件 URL 作为输入，在隔离环境中执行格式转换、结构提取、内容清洗等操作，并返回新文件或结构化数据，无需开发者编写解析逻辑。

- **应用调用（Application Call）**：智能体应用支持在 `input` 字段中以 `{"input_file": {"file_id": "file-xxx"}}` 方式传入文件；应用内可配置为“全文引用”（整份内容送入 LLM）或“切片检索”（先经知识库检索再合成回答），实现端到端文件驱动的业务流程。

## 关键参数和配置

| 参数 | 所属模块 | 类型 | 说明 |
|------|----------|------|------|
| `file_id` | 全局 | string | 文件唯一标识符，由 `/v1/files` 上传接口返回，是所有引用行为的基础凭证。 |
| `purpose` | 文件管理 API | string | 上传时指定用途：`assistants`（默认，用于智能体/应用）、`batch`（批量推理）、`fine-tune`（微调），影响平台内部资源调度策略。 |
| `tags` | 文件管理 / 数据连接器 / 知识库 API | string array | 用户定义的字符串标签（如 `["invoice", "2024Q3"]`），用于跨场景过滤与精准召回，支持在 `searchFile`、知识库检索、API 请求中传递。 |
| `metadata_filter` | 知识库 API | object | 结构化元信息过滤条件（如 `{"source_type": "contract", "signed_date": {"gte": "2024-01-01"}}`），需在知识库创建时启用 Meta 抽取并预设字段。 |
| `input_file` | Application Call（OpenAI 协议） | object | [OpenAI 兼容接口](openai-compatible-api.md)中用于传递文件的字段，结构为 `{"file_id": "file-xxx"}`，仅智能体应用支持。 |

> ⚠️ 注意：`file_id` 仅在文件未被删除且未超出存储配额（默认 10,000 文件）时有效；删除后不可恢复，已关联运行中任务（如 `batch` 作业）的文件将阻塞删除直至任务完成。

## 面向开发者，简洁实用

- ✅ **首选路径**：上传 → 获取 `file_id` → 在任意支持文件输入的 API（模型调用、知识库、应用、Skill）中直接引用。
- ✅ **批量/自动化场景**：结合 `tags` + `metadata_filter` 实现文件分组管理与条件检索，避免硬编码 `file_id`。
- ✅ **安全与成本意识**：文件默认私有；单文件上限 512 MB；知识库初步召回 TopK 直接影响费用，建议从 `5` 起调优。
- ❌ **避免误区**：文件上传 ≠ 自动索引（知识库需手动建索引）；`file_id` 引用 ≠ 支持所有模型（需确认模型文档是否声明支持 `file` 类型 content）；JSON/CSV 不支持直接上传，须转为 XLSX。
- 🔧 **调试技巧**：使用 `HEAD /v1/files/supported-types` 探测当前环境支持的 MIME 类型；通过控制台「文件管理」页面快速验证 `file_id` 状态与元信息。

## 关联主题页

- [file management api](../api/file-management-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [data connection overview](../guides/data-connection-overview.md)
- [skill](../guides/skill.md)
- [application call](../api/application-call.md)


