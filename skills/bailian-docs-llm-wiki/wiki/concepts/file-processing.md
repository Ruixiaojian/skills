# 文件处理

文件处理是百炼平台中对非结构化与半结构化数据（如 PDF、Word、Excel、CSV、JPG、PNG 等）进行上传、解析、引用、转换与输出的核心能力集合，贯穿模型调用、智能体执行、知识库构建与数据连接等关键链路。它不直接参与模型推理，而是为大模型和业务逻辑提供安全、标准化的文件输入通道与结果交付载体。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用场景**：通过 `file management API` 上传文件获取 `file_id`，在 `chat/completions` 或[多模态](multi-modal.md)请求（如 `qwen-vl-plus`）中以 `file_id` 或 `oss://` URL 引用；需注意 `purpose` 参数（`assistants` / `vision`）决定文件是否可用于文本理解或视觉模型。
- **智能体（Agent）场景**：用户上传附件后，系统自动识别 MIME 类型与内容特征，结合 Skill 的 `description` 语义匹配，触发 `pdf`、`xlsx` 等官方 Skill 执行解析、格式转换或表格生成，并以新文件形式返回结果。
- **RAG 与知识库场景**：通过应用支持模块上传 `.pdf`/`.docx` 等文档，平台调用文档理解能力完成切片、向量化与索引构建；文件作为知识源参与检索增强，不直接参与对话流但影响生成质量。
- **数据连接场景**：文件连接器（File Connector）将本地或 OSS 中的静态文档批量导入平台，经统一解析后形成可检索的知识集；表格连接器则处理 Excel/CSV，支持 `image_url` 字段用于[多模态](multi-modal.md)向量构建。
- **异步任务与临时资源场景**：调用图像/视频生成等异步模型时，需先通过 `getPolicy` 接口获取临时 OSS 上传策略，生成 `oss://` URL 并在请求头中显式启用 `X-DashScope-OssResourceResolve: enable`，该 URL 48 小时后自动失效。

## 关键参数和配置

| 参数 | 所属模块 | 说明 | 注意事项 |
|------|----------|------|----------|
| `file_id` | File Management API | 文件唯一标识符，上传成功后返回，全局唯一且不可复用 | 删除后所有关联调用立即失效；不可修改 purpose |
| `purpose` | File Management API | 取值 `assistants`（默认，适用于文本类模型）或 `vision`（仅限[多模态](multi-modal.md)模型如 `qwen-vl`） | 同一文件若需双用途，必须分别上传两次并指定不同 purpose |
| `expire_in_seconds` | More about Models | 临时 API Key 有效期（1–1800 秒） | 用于前端直传等不可信环境，到期自动作废 |
| `X-DashScope-OssResourceResolve: enable` | Model Calling (Multi-modal) | 使用 `oss://` URL 时必需的请求头 | 缺失将导致模型拒绝访问文件资源 |
| `MD5` | Application Support | 文件上传完整性校验字段 | 必填，用于服务端比对防止传输损坏 |
| `bailian-connector-access` / `bailian-datahub-access` | Data Connection | OSS Bucket 标签，区分连接器类型权限 | 前者用于文件/表格连接器（值 `ReadAndWrite`），后者用于数据枢纽型 OSS 连接（值 `read`），不可混用 |

> ⚠️ 共同限制：单文件 ≤ 512 MB；禁止 `.exe`、`.zip`、`.jar` 等可执行/压缩格式；PDF 后缀必须为小写 `pdf`；文件默认永久保留，需显式 DELETE 清理。

## 面向开发者，简洁实用

- ✅ **首选路径**：生产环境优先使用 `file management API` 上传 + `file_id` 引用，避免临时 URL 的 48 小时生命周期约束；
- ✅ **多模态必做**：调用 `qwen-vl-*` 模型前，务必确认 `purpose=vision`，否则图像无法被识别；
- ✅ **Skill 开发提示**：自定义 Skill ZIP 包 ≤ 10 MB，运行于沙箱，禁止外网访问；输出文件需通过标准返回协议（如 `{"file": "result.xlsx"}`）交付；
- ✅ **调试建议**：文件未生效？检查 `file_id` 是否有效、`purpose` 是否匹配模型、请求头是否缺失 `X-DashScope-OssResourceResolve`、OSS Bucket 标签是否正确；
- ❌ **禁止行为**：不要重复上传同名文件期望复用 `file_id`（每次生成新 ID）；不要在 Skill 中尝试写数据库或调用外部 API（沙箱限制）；不要将临时 `oss://` URL 用于长期存储或压测（QPS 限 100，且非生产级设计）。

## 关联主题页

- [file management api](../api/file-management-api.md)
- [data connection overview](../guides/data-connection-overview.md)
- [skill](../guides/skill.md)
- [more about models](../api/more-about-models.md)
- [application support](../guides/application-support.md)


