# 文件处理

文件处理是百炼平台中对非结构化或半结构化数据（如 PDF、Word、CSV、JSON、纯文本等）进行上传、托管、解析、索引与调用的统一能力抽象。它不直接参与模型推理，而是作为数据准备层，为知识库构建、智能体技能执行、多模态模型输入等下游场景提供可靠、可配置的文件生命周期管理支持。

## 在百炼平台的不同场景中，这个概念如何使用

文件处理能力贯穿多个核心模块，但职责与实现方式各异：

- **文件管理 API**：提供最底层的文件托管服务。开发者通过 `POST /v1/files` 上传文件，获得唯一 `file_id`；后续可查询、列举或删除。该层**不解析内容**，仅存储原始二进制与元信息（如 `filename`, `size`, `created_at`），适用于预置训练/评估数据、构建知识库前的素材归集等场景。

- **知识库（RAG）**：文件需先经文件管理 API 上传（`purpose="assistants"`），再通过知识库控制台或 API 关联至具体知识库实例。此时平台自动触发**文档智能解析**（含文本提取、段落切分、表格识别、OCR 等），并基于向量模型完成嵌入与索引。文件处理在此场景中表现为“上传 → 解析 → 向量化 → 可检索”的端到端流水线。

- **数据连接（文件/表格类）**：支持将本地文件或 OSS 中的文件批量导入平台托管知识库，或配置**定时同步规则**（如每小时拉取钉钉新文档）。该模式复用文件管理 API 的上传能力，但封装了来源发现、增量检测与自动触发逻辑，适合企业级知识持续更新。

- **Skill（技能）**：官方 Skill（如 `pdf-reader`, `csv-analyzer`）在运行时自动调用平台内置文件解析引擎，对用户对话中提及的附件或 URL 进行即时读取与结构化转换。此处的文件处理是**按需、轻量、无状态**的，不持久化文件，仅返回解析结果供智能体下一步决策。

- **多模态模型调用（如 `qwen-vl-plus`）**：通过 `GET /api/v1/uploads` 获取临时 OSS 上传凭证，将图像/视频/音频文件上传后得到 `oss://` URL，并在模型请求中携带该 URL 及 `X-DashScope-OssResourceResolve: enable` 头。此路径属于“临时文件处理”，强调低延迟与 URL 时效性，不进入长期文件管理系统。

## 关键参数和配置

| 场景 | 关键参数 | 说明 | 注意事项 |
|------|----------|------|----------|
| **文件管理 API 上传** | `file`（form-data） | 二进制文件流 | 必填；支持 MIME 类型见下文 |
| | `purpose` | 用途标识 | 当前仅 `"assistants"` 有效（用于知识库），其他值被忽略；建议始终显式传入 |
| | `file_id` | 路径参数 | 查询/删除时必需；由上传成功响应返回的 `id` 字段提供 |
| | `limit`, `after` | 查询分页参数 | `limit` 默认 20，最大 100；`after` 值为上一页响应中的 `last_id` |
| **知识库关联** | `chunk_size`, `chunk_overlap` | 切分粒度 | 控制文本分块大小与重叠，影响召回精度与上下文长度；可在知识库创建时配置 |
| | `embedding_model` | 向量模型 | 如 `text-embedding-v4`，决定语义表示质量；需与知识库类型匹配 |
| **多模态输入** | `model_name`（上传时） | 绑定模型名 | 必须与后续模型调用一致（如 `qwen-vl-plus`），否则调用失败 |
| | `X-DashScope-OssResourceResolve: enable` | 请求头 | 使用 `oss://` URL 时**必须添加**，否则模型返回 400 错误 |
| **Skill 触发** | `description`（SKILL.md） | 技能描述 | 必须明确包含“支持格式”（如 `.pdf`, `.xlsx`）和“支持操作”（如 “提取表格”、“读取文字”），否则无法准确触发 |

**支持的文件格式（通用）**：  
- 文本类：`text/plain`, `application/json`, `text/csv`  
- 文档类：`application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`（.docx）, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`（.xlsx）  
- 其他：部分 Skill 和多模态模型支持图片（`image/*`）、音频（`audio/*`）、视频（`video/*`）——具体以对应模型文档为准  

**硬性限制**：  
- 单文件上限：**100 MB**（文件管理 API）；临时上传 URL 无此限，但 OSS 存储策略需自行配置  
- 每项目文件数上限：**10,000 个**（文件管理 API）  
- 自定义 Skill ZIP 包：≤ 10 MB，且必须包含合法 `SKILL.md`  

## 面向开发者，简洁实用

- ✅ **优先使用文件管理 API 上传**：若需长期托管、复用或纳入知识库，务必通过 `/v1/files` 上传并保存 `file_id`，而非直接传二进制到模型接口。  
- ✅ **知识库文件必须走 `purpose="assistants"`**：即使上传成功，未指定该 purpose 或未关联知识库，文件不会被自动解析或索引。  
- ✅ **多模态输入请用临时 URL 流程**：避免直接传大文件；获取 `oss://` URL 后，务必加 `X-DashScope-OssResourceResolve: enable` 头。  
- ✅ **Skill 描述要精准**：`description` 中写明“支持 .pdf 表格提取”，智能体才会在用户说“把这份PDF里的表格转成Excel”时调用；模糊描述（如“处理文档”）将导致不可靠触发。  
- ⚠️ **文件不自动解析**：上传 ≠ 可检索。文件管理 API 本身不解析；知识库、Skill、多模态模型各自触发解析，逻辑相互独立。  
- ⚠️ **删除不可逆**：`DELETE /v1/files/{file_id}` 后文件彻底丢失，`file_id` 不可复用；生产环境建议先 `GET` 确认再删。  
- 📌 **调试技巧**：遇到 `415 Unsupported Media Type`，检查 MIME 类型是否在支持列表内；遇到 `413 Payload Too Large`，确认文件是否超 100 MB；遇到模型调用失败且含 `oss://`，首先检查是否遗漏 `X-DashScope-OssResourceResolve` 头。

## 关联主题页

- [file management api](../api/file-management-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [data connection overview](../guides/data-connection-overview.md)
- [skill](../guides/skill.md)
- [more about models](../api/more-about-models.md)


