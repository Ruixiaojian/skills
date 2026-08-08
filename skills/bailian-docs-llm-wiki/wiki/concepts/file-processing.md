# 文件处理

文件处理是百炼平台中对非结构化文档（如 PDF、Word、CSV、TXT 等）进行上传、解析、索引、引用与调用的一整套能力抽象，贯穿数据准备、知识增强、智能体执行和应用集成等关键环节。它不依赖特定大模型，而是作为平台级基础设施，统一支撑知识库构建、RAG 检索、智能体工具调用及自定义 Skill 执行等场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **文件管理 API（独立服务）**：提供文件全生命周期控制（上传/查询/列举/删除），是所有文件处理的起点。上传后的 `file_id` 是后续各场景中唯一标识该文件的凭证，适用于预置资源、批量导入知识库或为高代码应用准备输入素材。

- **LLM Application（智能体/工作流/高代码）**：
  - *智能体（Agent 2.0）*：支持两种模式——**全文引用**（将文件内容直接拼入 [prompt](../guides/prompt.md)，适用于小文件+精准问答）和**切片检索**（通过向量检索召回相关片段，适用于长文档+成本敏感场景）；文件需先通过 API 上传并传入 `file_id`，或在对话中临时上传（单会话 ≤10 个、≤10MB）。
  - *工作流*：通过 `searchFile` 等内置工具节点调用已上传文件，支持跨节点变量传递（如 `${session.file_ids}`），常用于自动化报告生成、合同比对等流程。
  - *高代码应用*：开发者可直接在 Python 代码中调用文件管理 API 获取文件内容，或结合 `bailian-sdk` 解析 `file_id` 对应的原始二进制/文本数据，实现定制化处理逻辑。

- **数据连接（Data Connection）**：针对文件类数据源，提供“平台托管型”接入方式——将本地或 OSS 中的 PDF/Word/Excel 等文件导入百炼，自动完成解析、分块与向量化，构建可被 RAG 检索的知识库。注意：JSON/CSV/YAML 需转为 Excel 格式后方可导入。

- **Skill（能力插件）**：官方 Skill（如 `pdf-parser`、`xlsx-reader`）封装了常见格式的解析逻辑，智能体可根据用户指令自动识别并调用；自定义 Skill 可扩展专有格式处理能力，其 `description` 必须明确声明支持的文件类型与操作边界，以确保精准触发。

## 关键参数和配置

| 场景 | 参数/配置项 | 说明 |
|------|-------------|------|
| **文件管理 API** | `file`（form-data） | 必填，二进制文件内容；支持 MIME 类型：`text/plain`, `application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`, `text/csv`, `application/json`；**不支持图像格式**。 |
| | `purpose`（form-data） | 可选，默认 `"assistants"`；当前仅此值有效，其他值被忽略。 |
| | `file_id`（path） | 平台生成的 24 位十六进制字符串，全局唯一，用于后续所有引用。 |
| | `limit` / `after`（query） | 列举接口分页参数：`limit`（1–100，默认 20），`after`（上一页 `last_file_id`）。 |
| **LLM Application** | `单文件最大解析长度`（token） | 全文引用模式下，控制截断位置（末尾截断），直接影响输入 [Token](token.md) 消耗。 |
| | `召回片段数` / `最大拼装长度`（token） | 切片检索模式核心参数：前者决定返回多少片段，后者限制总 token 数，系统按相关性丢弃低分片段。 |
| | `session_file_id`（API 请求 input） | 推荐替代公网 URL 的文件引用方式，避免超时与权限问题；值为文件管理 API 返回的 `file_id`。 |
| **Skill** | `name`（`SKILL.md`） | 自定义 Skill 唯一标识，仅允许小写字母、数字、连字符；账号维度全局唯一。 |
| | `description`（`SKILL.md`） | 必填且关键：必须明确说明支持的文件扩展名、可执行操作、典型触发语句，并**显式声明不适用场景**（如“不处理 .doc 文件”），否则易误触发。 |

## 注意事项（面向开发者）

- ✅ **优先使用 `file_id`**：所有场景下，推荐先调用 `/v1/files` 上传文件获取 `file_id`，再在智能体、工作流或高代码中引用，而非直接传 URL 或 base64。
- ⚠️ **大小限制分层**：  
  - 文件管理 API：单文件 ≤ 512 MB；  
  - LLM Application 会话上传：单文件 ≤ 10 MB，单会话 ≤ 10 个；  
  - 自定义 Skill ZIP 包：≤ 10 MB。
- ⚠️ **不可逆操作**：`DELETE /v1/files/{file_id}` 会永久删除文件及所有关联（如知识库引用、Skill 调用上下文），请谨慎执行。
- 🔒 **权限与网络**：OSS 连接器需 Bucket 添加标签 `bailian-datahub-access: read`；MySQL/PostgreSQL 公网访问需白名单百炼 IP 段；PolarDB-X 2.0 仅支持私网。
- 📊 **计费影响**：文件内容解析后的文本计入模型输入 [Token](token.md)；知识库召回片段、记忆体内容、Skill 输出均参与计费，请合理设置 `最大拼装长度` 和 `召回片段数`。

## 关联主题页

- [file management api](../api/file-management-api.md)
- [llm application](../guides/llm-application.md)
- [data connection overview](../guides/data-connection-overview.md)
- [skill](../guides/skill.md)


