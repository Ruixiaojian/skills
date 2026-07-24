# 文件处理

文件处理是百炼平台中统一支撑[多模态](multi-modal.md)输入与资源管理的核心横切能力，指对用户上传的原始文件（如 PDF、Word、CSV、图像等）进行托管、解析、索引及安全引用的全生命周期操作。该能力不绑定具体模型，而是作为平台级基础设施，为智能体、RAG、微调、图像/视频/3D 生成等各类 AI 任务提供标准化的文件接入方式。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体与应用调用**：在 `application call` 中，文件通过 `input` 字段以 `input_file` 类型传入（需提前上传至平台），并由智能体配置“全文引用”或“切片检索”策略，实现文档问答、摘要、表格分析等能力。
- **知识库构建**：文件管理 API 是知识库数据注入的唯一入口；上传时指定 `purpose=assistants` 的文件可被自动解析为向量片段，供 RAG 检索使用。
- **图像/视频/3D 生成**：所有支持图像输入的模型（如 `qwen-image-3.0-pro`、`wan2.7-i2v`、`Tripo/Tripo-H3.1`）均要求图像资源为公网可访问 URL；开发者需先调用文件管理 API 上传图像，再将返回的 `file_id` 转换为直链（通过 `GET /v1/files/{file_id}` 获取 `url` 字段），填入对应模型的 `input.media.url` 或 `input.image` 参数。
- **微调任务**：上传训练数据集时需设置 `purpose=fine-tune`，该用途文件仅允许被 `fine-tuning` 相关 API 引用，与其他用途隔离，保障数据权限安全。
- **批量推理与异步任务**：`batch` 用途文件专用于批量 API（如 `batch/completions`），支持一次提交多条请求，提升吞吐效率。

> ✅ 关键共识：**所有模型均不直接接收二进制文件流**；必须先通过 `/v1/files` 上传获取 `file_id`，再转换为可公开访问的 `url` 或在支持 `file_ids` 的接口中直接引用 `file_id`。

## 关键参数和配置

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data body | binary | 是 | 原始文件流（非 base64），支持格式包括 `text/plain`, `application/pdf`, `text/csv`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`, `text/markdown`, `image/jpeg`, `image/png` 等（完整列表见 API 参考 v2.3） |
| `purpose` | form-data body | string | 否 | 文件用途，决定后续调用权限：<br>• `assistants`（默认）：可用于智能体、RAG、`chat/completions`；<br>• `fine-tune`：仅限微调任务；<br>• `batch`：仅限批量推理；<br>• `vision`：预留，当前未启用 |
| `file_id` | path / body | string | 是（查询/删除/引用时） | 平台分配的全局唯一标识符（如 `file_abc123xyz`），上传成功后返回，用于后续所有引用 |
| `url` | response body | string | — | 上传成功响应中返回的直链地址，有效期 2 小时，适用于图像/视频/3D 等需 URL 输入的模型 |

- **大小限制**：免费版单文件 ≤ 512 MB；企业版 ≤ 2 GB。
- **保留策略**：文件默认永久保留，但若连续 90 天未被任何 API 引用（如未出现在 `messages.file_ids`、`input.media.url`、`fine_tuning.job.file_id` 等字段中），可能被系统自动清理。
- **安全性**：`file_id` 本身不暴露文件内容，仅作为授权凭证；直链 `url` 带签名且短期有效，防止未授权访问。

## 面向开发者，简洁实用

- ✅ **第一步永远是上传**：不要尝试在图像/视频/3D 接口里直接传 `file` 字段——先调 `POST /v1/files`。
- ✅ **用途选对才可用**：`purpose=assistants` ≠ `purpose=fine-tune`，混用必报 `400 Invalid file purpose`。
- ✅ **URL 要及时用**：`url` 字段有效期仅 2 小时，建议上传后立即提取并传入下游模型，勿缓存复用。
- ✅ **查状态用 `file_id`**：调试时可通过 `GET /v1/files/{file_id}` 确认文件是否上传成功、解析是否完成（`status: "processed"` 表示已就绪用于 RAG）。
- ✅ **删前必确认**：`DELETE /v1/files/{file_id}` 不可逆，删除后所有引用失效，可能导致智能体或任务失败。

> 提示：本地开发推荐使用 DashScope SDK 的 `File.upload()` 方法，自动处理重试、分块上传与 MIME 类型推断，比 raw cURL 更健壮。

## 关联主题页

- [file management api](../api/file-management-api.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [application call](../api/application-call.md)


