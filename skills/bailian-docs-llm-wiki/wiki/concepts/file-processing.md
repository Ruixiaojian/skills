# 文件处理

文件处理是百炼平台中对非结构化数据（如 PDF、Word、Excel、图像、音视频等）进行上传、托管、解析与集成调用的核心能力。它并非单一接口，而是贯穿文件管理、多模态模型推理、智能体应用及数据连接四大场景的横切能力，为 RAG、文档问答、视觉理解、语音识别等上层业务提供统一的数据输入基础。

## 在百炼平台的不同场景中，这个概念如何使用

- **文件管理 API 场景**：作为文件生命周期的起点，所有需被平台其他服务引用的文件必须先通过 `/v1/files` 接口上传，获得唯一 `file_id`。该 ID 是后续查询、删除或在其他 API 中引用该文件的凭证。此层仅做“托管”，不涉及内容解析。

- **多模态模型调用场景**（如 `qwen-vl-plus`、`paraformer-16k-1`）：文件需先转换为临时可访问的 URL（`oss://...`），再作为 `input.image_url` 或 `input.audio_url` 传入模型请求。调用时必须显式添加请求头 `X-DashScope-OssResourceResolve: enable`，否则模型无法加载资源。临时 URL 有效期为 48 小时，适用于开发调试；生产环境应使用自有 OSS + 鉴权 URL。

- **智能体（Agent）与工作流应用调用场景**：支持直接上传文件（如用户对话中发送 PDF），并在配置中选择「全文引用」或「切片检索」模式。平台自动触发文档解析与向量化，使文件内容可参与 RAG 检索。文件输入通过 `input` 字段中的 `input_file` 对象传递，格式为 `{ "file_id": "file-xxx" }` 或 `{ "url": "https://..." }`（需确保可公开访问）。

- **数据连接场景**：文件类连接器（如“文件连接器”）支持批量导入本地或 OSS 中的文档，经平台内置解析引擎（含大模型文档解析）提取文本、表格、图表等内容，并构建向量索引。导入后，智能体可通过 `searchFile` 工具按标签、关键词实时检索片段，实现企业知识库问答。

## 关键参数和配置

| 参数/配置项 | 所属场景 | 说明 | 注意事项 |
|-------------|----------|------|----------|
| `file_id` | 文件管理、应用调用 | 文件唯一标识符，由上传接口返回，格式为 `file-xxx` | 仅在所属 `project_id` 或 `workspace_id` 内有效；不可跨项目复用 |
| `file`（binary） | 文件管理 API 上传 | `multipart/form-data` 中的二进制文件流 | `Content-Type` 必须与实际文件类型一致；单文件 ≤ 2 GB |
| `expire_in_seconds`（临时 URL） | 多模态模型调用 | 控制临时 OSS URL 有效期（默认 60 秒，最大 1800 秒） | 仅影响 URL 生效时长，不影响文件本身存储 |
| `X-DashScope-OssResourceResolve: enable` | 多模态模型调用 | 强制启用平台对 OSS URL 的资源解析 | **必须显式设置**，否则模型返回 400 错误 |
| `bailian-datahub-access:read`（OSS 标签） | 数据连接（OSS 连接器） | OSS Bucket 必须绑定的访问标签 | 用于授权百炼读取权限；与文件连接器的 `bailian-connector-access` 标签不同，不可混用 |
| 解析方式（“大模型文档解析”） | 数据连接、应用文件问答 | 启用通义千问模型进行深度解析，支持图文混合、表格重建、公式识别 | 相比传统 OCR 更准确，但耗时略长；建议高价值文档优先启用 |

## 面向开发者：实用建议

- ✅ **生产环境文件路径**：避免依赖临时 URL；推荐将文件预存至自有 OSS，配置好 `bailian-datahub-access:read` 标签后，直接在应用或数据连接中使用带鉴权的长期 URL。
- ✅ **大文件处理**：单文件超 2 GB 时，请先分片或压缩；若需处理超大规模文档集，优先使用「数据连接 → 文件连接器」批量导入 + 向量索引，而非逐个上传 `file_id`。
- ✅ **安全与权限**：`file_id` 本身不携带权限信息，其访问受 `project_id` / `workspace_id` 和调用方 API Key 权限双重控制；删除前务必确认无活跃任务正在引用该文件。
- ⚠️ **不要重复解析**：同一份文件若已在数据连接中完成解析并建索引，无需再通过文档解析 API 单独调用——直接复用连接器 ID 即可调用 `searchFile` 工具。
- 📌 **调试技巧**：上传后立即调用 `GET /v1/files/{file_id}` 确认状态为 `processed`（非 `uploading` 或 `failed`）；多模态调用失败时，优先检查请求头是否遗漏 `X-DashScope-OssResourceResolve`。

## 关联主题页

- [file management api](../api/file-management-api.md)
- [more about models](../api/more-about-models.md)
- [application call](../api/application-call.md)
- [data connection overview](../guides/data-connection-overview.md)


