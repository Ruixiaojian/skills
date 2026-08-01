# 文件输入与管理

文件输入与管理是百炼平台统一处理用户上传文件的核心能力，指通过标准化接口完成文件的上传、标识、引用与生命周期管理，并在模型调用、知识库构建、智能体执行等场景中安全、高效地传递原始文件或其平台生成的逻辑引用（`file_id`）。该能力不依赖具体模型，而是作为平台级基础设施，为多模态推理、RAG、工具调用等提供一致的文件抽象层。

## 在百炼平台的不同场景中如何使用

- **模型 API 调用（如 Qwen-VL、Qwen3）**：上传文件后获取 `file_id`，在 `messages` 中以 `"file_id": "file-xxx"` 形式传入；需根据模型类型显式指定 `purpose=vision`（视觉模型）或 `purpose=assistants`（文本/助手类模型），否则调用失败。
- **知识库构建**：支持直接上传 PDF/Word/CSV 等文件，平台自动解析并切片索引；也可通过数据连接器接入 OSS 或本地文件，由知识库服务统一托管和向量化；上传文件即触发索引任务，无需额外 API 调用。
- **智能体应用（Application Call）**：仅新版智能体支持文件输入，需在应用配置中启用“全文引用”或“切片检索”，并在 `input` 字段中传入 `{"input_file": [{"file_id": "file-xxx"}]}` 结构。
- **Managed Agents（托管智能体）**：上传文件会自动挂载至沙箱路径 `/mnt/session/uploads/`，Agent 可通过 `read`/`glob` 等内置工具直接读取；单次上传上限 10 MB，挂载后路径固定且会话间隔离。
- **数据连接器（Data Connection）**：文件类连接器（如 PDF/Excel 连接器）支持批量导入平台存储或自有 OSS；上传后平台自动解析并构建向量索引，后续可通过 `searchFile` 工具按语义检索内容。

## 关键参数和配置

| 参数 | 说明 | 必填性 | 注意事项 |
|------|------|--------|----------|
| `file`（form-data） | 二进制文件流 | 是 | 支持格式：`text/plain`, `application/pdf`, `text/csv`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`, `image/*` 等 |
| `purpose`（form-data） | 文件用途标识 | 否（默认 `assistants`） | 必须设为 `vision` 才能被 Qwen-VL 等多模态模型识别；设为 `batch` 用于异步批处理任务 |
| `file_id` | 平台返回的唯一标识符 | — | 由 `/v1/files` 接口返回，所有下游引用（模型调用、知识库、智能体）均依赖此 ID |
| `limit` / `after`（query） | 分页参数 | 否 | `limit` 默认 20；`after` 为上一页最后一个 `file_id`，用于游标分页 |
| 单文件大小上限 | — | — | **512 MB**（文件管理 API）；**10 MB**（Managed Agents 挂载）；知识库与数据连接器无单独限制，但受项目总配额约束 |
| 项目文件总数上限 | — | — | **10,000 个文件**；超出后上传失败，需主动清理 |

> ⚠️ 重要提醒：  
> - 平台**不执行 OCR、文本提取或格式转换**——PDF/Word 等文件内容由下游模型或服务自行解析；  
> - 删除文件（`DELETE /v1/files/{file_id}`）立即生效且不可恢复，请确认无活跃任务正在引用；  
> - 未被任何模型或服务引用的文件将在 **30 天后自动清理**，建议业务侧主动管理生命周期。  

## 面向开发者：快速上手要点

- ✅ **统一入口**：所有文件操作均通过 `POST /v1/files`（上传）及配套 REST 接口完成，无需区分模型或场景；  
- ✅ **一次上传，多处复用**：同一 `file_id` 可同时用于知识库索引、智能体挂载和模型调用；  
- ✅ **权限最小化**：只需 `AliyunBailianDataFullAccess` 或自定义策略含 `bailian:CreateFile` 等动作；  
- ❌ **避免硬编码路径**：勿使用已废弃的 `/v1/files/upload`；始终以 `/v1/files` 为准；  
- ❌ **勿跳过 `purpose` 设置**：视觉模型调用失败的最常见原因是遗漏 `purpose=vision`；  
- 📌 **调试建议**：上传后立即调用 `GET /v1/files/{file_id}` 验证元信息；结合 SLS 日志查看 `file_id` 在各服务中的流转记录。

## 关联主题页

- [file management api](../api/file-management-api.md)
- [application call](../api/application-call.md)
- [knowledge base](../guides/knowledge-base.md)
- [data connection overview](../guides/data-connection-overview.md)
- [managed agents](../guides/managed-agents.md)


