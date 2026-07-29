# 文件输入

文件输入是百炼平台中将本地或托管的结构化/非结构化文件（如 PDF、DOCX、CSV、TXT 等）作为模型推理上下文或知识源引入的关键机制。它不直接参与模型权重计算，而是通过预处理、向量化、切片检索或全文注入等方式，为大模型提供可引用的外部信息支撑。

## 在百炼平台的不同场景中，这个概念如何使用

文件输入并非单一接口能力，而是贯穿多个核心能力层的横切能力，具体使用方式取决于业务目标：

- **文件管理 API（基础层）**：用于统一上传、查询和生命周期管理文件。上传后获得 `file_id`，该 ID 可在后续 `/v1/chat/completions` 或 `/v1/embeddings` 等模型调用中作为 `file` 参数传入（需配合 `purpose=assistants` 等语义标识）。这是所有文件输入的源头入口，适用于 RAG 预置、微调数据准备或通用文档解析。

- **智能体应用调用（应用层）**：在 `Application.call()` 中，通过 `input` 字段的 `input_file` 子类型传入文件（支持单文件或多文件数组），要求应用已配置“全文引用”或“切片检索”模式。此时文件可被智能体动态解析、路由至知识库或工具节点，无需预先上传至文件管理 API（SDK 会自动完成托管与引用）。

- **知识库（RAG 层）**：文件作为知识源导入知识库后，经自动切分、向量化和索引，成为可检索的语义单元。用户提问时，系统不直接传入原始文件，而是通过语义匹配召回相关切片，并将内容拼接进模型 [prompt](../guides/prompt.md)。文件输入在此场景下是离线构建知识底座的必要前置动作。

- **数据连接（集成层）**：支持将 OSS Bucket 或平台托管的文件/表格类数据源注册为连接器。文件不作为单次请求参数传入，而是以“连接器+标签”形式在工作流中按需检索（如 `searchOSSFile(tags=["report_2024"])`），实现动态、安全、可复用的数据接入。

- **多模态模型调用（模型层）**：对 `qwen-vl-plus` 等视觉语言模型，文件输入特指图像类文件（`.jpg`, `.png` 等），需先调用 `/api/v1/uploads` 获取 `oss://` 临时 URL，并在模型请求中通过 `input.image_url` 字段传入——**此时必须携带 `X-DashScope-OssResourceResolve: enable` 请求头**，否则服务无法解析资源。

> ⚠️ 注意：同一文件在不同场景下不可混用 `file_id`、`input_file`、`oss://` URL 等引用方式；各路径独立鉴权、独立计费、独立状态管理。

## 关键参数和配置

| 场景 | 关键参数 | 类型 | 必填 | 说明 |
|------|----------|------|------|------|
| **文件管理 API** | `file` | multipart/form-data | 是 | 二进制文件流，支持 `.txt`, `.pdf`, `.docx`, `.xlsx`, `.csv`, `.json`, `.md` |
| | `purpose` | string | 否（默认 `"assistants"`） | 决定文件用途及元数据校验逻辑：`"assistants"`（智能体/RAG）、`"batch"`（批量任务）、`"fine-tune"`（微调数据） |
| | `filename` | string | 否 | 显式指定文件名（尤其流式上传时建议设置，避免 MIME 推断失败） |
| **智能体应用调用** | `input.input_file` | object/array | 是（当需文件输入时） | 包含 `file_id`（已上传）或 `file_bytes`（SDK 自动托管）；支持多文件，每文件可带 `name` 和 `type`（如 `"application/pdf"`） |
| **知识库** | — | — | — | 无运行时参数；文件上传通过控制台或 SDK `KnowledgeBase.upload_files()` 完成，配置项在知识库创建时设定（如切片大小、解析策略） |
| **数据连接（文件类）** | `connector_id` + `tags` | string | 是（调用时） | 在工作流工具节点中指定连接器 ID，并通过 `tags` 过滤目标文件（如 `["quarterly", "finance"]`） |
| **多模态模型（VL）** | `input.image_url` | string | 是（图像输入时） | `oss://` 格式临时 URL；**必须添加请求头 `X-DashScope-OssResourceResolve: enable`** |
| | `expire_in_seconds` | integer | 否（默认 60） | 临时 URL 有效期，范围 60–1800 秒 |

## 面向开发者，简洁实用

- ✅ **首选托管路径**：生产环境优先使用 **文件管理 API** 上传 → 获取 `file_id` → 在模型/应用调用中复用。避免临时 URL 的 48 小时有效期与 QPS 限制。
- ✅ **智能体开发快捷方式**：Python SDK 中直接传 `input_file=bytes` 或 `input_file=open("a.pdf","rb")`，SDK 自动完成上传与引用，适合原型验证。
- ✅ **知识库文件处理**：上传前确保文档格式规范（PDF 文字可选中、Word 无复杂嵌套表格），大文件（>50 MB）建议预拆分，提升解析成功率。
- ❌ **禁止跨场景混用**：`file_id` 不能用于 `image_url`；`oss://` URL 不能用于 `input_file`；知识库中的文件 ID 与文件管理 API 的 `file_id` 不互通。
- ⚙️ **状态检查必做**：文件上传后，务必轮询 `/v1/files/{file_id}` 检查 `status == "processed"` 再调用，否则返回 `invalid_file` 错误。
- 📦 **大小与格式守则**：单文件 ≤ 512 MB；PDF/DOCX 建议 ≤ 100 MB；不支持 ZIP、EXE、加密 PDF；JSON/CSV 需为 UTF-8 编码且无 BOM。

## 关联主题页

- [file management api](../api/file-management-api.md)
- [application call](../api/application-call.md)
- [knowledge base](../guides/knowledge-base.md)
- [data connection overview](../guides/data-connection-overview.md)
- [more about models](../api/more-about-models.md)


