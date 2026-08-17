# 文件处理

文件处理是百炼平台中对非结构化与半结构化数据（如 PDF、Word、CSV、JSON、TXT 等）进行上传、托管、解析、挂载与语义化利用的一系列核心能力的统称。它不是单一 API 或功能模块，而是贯穿文件管理、数据连接、知识库、托管智能体及应用支持等多个场景的横切能力，为 RAG、智能体工具调用、文档理解等上层 AI 任务提供可靠的数据输入基础。

## 在百炼平台的不同场景中，这个概念如何使用

- **文件管理 API**：提供最底层的文件生命周期操作（上传/查询/列举/删除），不参与推理，仅用于资源纳管；上传后生成 `file_id`，作为后续所有文件引用的唯一凭证。
- **数据连接（平台托管型）**：将文件导入平台或自有 OSS，触发文档智能解析（含 Qwen VL、大模型文档解析等），生成可检索的文本切片或结构化表数据，支撑语义搜索与实时查询。
- **知识库（RAG）**：文件是知识库的核心数据源；上传后经向量化（`text-embedding-v4` 等）、分块（默认≤6000字符）、元信息抽取（如 `filename`、`date`）和标签标注，最终参与多路召回与重排。
- **托管智能体（Managed Agents）**：支持将文件挂载至沙箱会话路径 `/mnt/session/uploads/`，并配合内置工具（`read`/`write`/`edit`/`bash`）实现运行时动态读写、解析与转换，适用于数据分析、报告生成等有状态任务。
- **应用支持（RAG 集成）**：在低代码应用编排中，文件可通过知识库节点或插件方式接入；上传时需校验 MD5，且仅接受 `.pdf`（小写）、`.doc`、`.docx` 等明确支持格式，确保端到端一致性。

## 关键参数和配置

| 场景 | 关键参数 | 说明 |
|------|----------|------|
| **文件管理 API** | `purpose`（form-data） | 当前仅支持 `"assistants"`，为预留字段，不可硬编码其他值；<br>`limit` / `after`（query）：分页控制，`limit` 默认 20，最大 100 |
| **数据连接（文件类）** | 存储位置、OSS Bucket 标签（`bailian-connector-access`）、解析方式 | 平台存储上限 200,000 文件 / 1 TB；自有 OSS 必须添加指定标签并完成 RAM 授权 |
| **知识库** | 相似度阈值（0.01–1.0）、初步 TopK（1–100）、最大召回数（1–20）、标签过滤（单文件 ≤32 个） | 影响召回精度与成本；标签可用于前置过滤，提升检索效率 |
| **托管智能体** | `resources`（挂载列表）、`mount_path`（固定为 `/mnt/session/uploads/xxx`） | 单次挂载文件 ≤10 MB；路径需在 `system_prompt` 中显式声明，否则智能体无法定位 |
| **通用限制** | 单文件大小上限 512 MB、账号总存储配额默认 10 GB、文件不自动解析（需显式触发） | 超限将返回 `400` 错误；已删除文件不可恢复，`file_id` 不可复用 |

## 面向开发者，简洁实用

- ✅ **统一标识**：所有场景均以 `file_id`（UUID）为文件唯一身份，跨服务复用（如上传后传给知识库或智能体）。
- ✅ **格式明确**：首选 MIME 类型包括 `application/pdf`, `text/csv`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`, `text/plain`, `application/json`；避免大小写混用（如 `.PDF` → 用 `.pdf`）。
- ✅ **解析非自动**：上传 ≠ 可检索。需显式创建知识库、配置数据连接或调用 `Retrieve` API 才能触发向量化与索引。
- ✅ **路径即契约**：在托管智能体中，挂载路径固定为 `/mnt/session/uploads/{filename}`，务必在系统提示词中写明完整路径（如 `"请读取 /mnt/session/uploads/report.pdf"`）。
- ⚠️ **注意配额**：文件管理 API 的 10 GB 总配额、知识库的 1 TB 平台存储、托管智能体的 10 MB 单次挂载限制，三者独立计费与管控，需分别监控。
- 📌 **调试建议**：遇到文件不可见/解析失败，优先检查：① `file_id` 是否正确传递；② 是否遗漏 `purpose=assistants`（API 上传）；③ OSS Bucket 是否添加了 `bailian-connector-access` 标签；④ 控制台是否完成“开始检测”连通性验证。

## 关联主题页

- [file management api](../api/file-management-api.md)
- [data connection overview](../guides/data-connection-overview.md)
- [knowledge base](../guides/knowledge-base.md)
- [managed agents](../guides/managed-agents.md)
- [application support](../guides/application-support.md)


