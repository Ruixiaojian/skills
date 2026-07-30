# 文件处理

文件处理是百炼平台中对用户上传或引用的各类文件（文本、表格、PDF、图像等）进行解析、读写、编辑、转换与结构化输出的核心能力集合。它并非单一接口，而是贯穿于智能体运行、Skill 扩展、数据连接和模型调用等多个场景的横切能力，统一由平台托管的沙箱环境、文件管理服务与语义驱动调度机制协同支撑。

## 在百炼平台的不同场景中，这个概念如何使用

- **Managed Agents（托管智能体）**：文件作为会话上下文的一部分被挂载至沙箱路径 `/mnt/session/uploads/`，Agent 可通过内置工具（如 `read`、`write`、`edit`、`download_file`、`glob`）直接操作；单文件 ≤10 MB，挂载后生命周期与 Session 绑定，Session 结束即销毁。
- **File Management API（文件管理 API）**：提供文件全生命周期管理（上传/查询/列举/删除），生成全局唯一 `file_id`，供后续模型调用（如 `chat/completions`）或 Skill 引用；支持最大 512 MB 单文件，`purpose` 参数决定其在[多模态](multi-modal.md)模型中的可用性（`assistants` 或 `vision`）。
- **Skill（可复用能力包）**：官方 Skill（如 `pdf`、`xlsx`）封装了专业级文件解析逻辑（如 PDF 表格抽取、Excel 公式计算），自动识别用户意图与附件类型并触发；输出结果以新文件形式返回，全部运行于安全沙箱内，禁止外网访问或系统命令执行。
- **Data Connection（数据连接）**：文件连接器将本地或 OSS 中的文档批量导入平台，经文档理解服务解析为向量与结构化文本，用于 RAG 检索；表格连接器则将 CSV/Excel 映射为可 SQL 查询的数据表，支持 `image_url` 字段构建[多模态](multi-modal.md)索引。

## 关键参数和配置

| 场景 | 关键参数 | 说明 |
|------|----------|------|
| **Managed Agents** | `resources`（挂载列表） | 数组，含 `resource_id`（对应 `file_id`）与 `mount_path`（固定为 `/mnt/session/uploads/...`）；挂载后路径不可自定义。 |
| **File Management API** | `purpose`（上传时） | 必填字段，默认 `"assistants"`；若需在视觉模型（如 `qwen-vl`）中使用图像，必须设为 `"vision"`。 |
| **Skill** | `description`（SKILL.md） | 决定 Skill 是否被触发的关键语义描述，须明确支持的文件类型（如 `"支持 .pdf 和 .docx 格式发票"`）、操作（如 `"提取金额、日期、供应商名称"`）及不适用边界。 |
| **Data Connection（文件类）** | 存储位置 + 解析方式 | 平台存储或自有 OSS（需打 `bailian-connector-access: ReadAndWrite` 标签）；解析方式影响结构化质量，默认启用文档理解，支持自定义规则。 |

> ⚠️ 注意：所有场景均强制隔离——文件内容不会跨沙箱共享；`file_id` 是跨服务引用的唯一凭证，但不同 `purpose` 值的同名文件视为不同资源；删除 `file_id` 后，所有依赖该 ID 的调用（包括已启动的 Agent Session 或 Skill）将立即失败。

## 面向开发者，简洁实用

- ✅ **首选实践**：大文件（>10 MB）先用 File Management API 上传获取 `file_id`，再传给 Managed Agents 或 Skill；小文件（≤10 MB）可直接在 Agent 创建时挂载。
- ✅ **调试技巧**：在 Managed Agents 中，用 `bash ls -la /mnt/session/uploads/` 确认挂载；在 Skill 中，用 `print()` 输出中间结果（需配合日志审计权限查看）。
- ❌ **避免踩坑**：不要在 Skill ZIP 包中硬编码路径或依赖外部网络；不要重复上传同名文件期望复用 `file_id`（每次上传必生成新 ID）；不要在数据库连接器中尝试导入 JSON/CSV 原生格式（需转为 XLSX）。
- 🔧 **性能提示**：PDF/Excel 解析耗时较长，建议在 Skill 或数据连接中启用异步预处理；高频小文件操作优先走 Agent 沙箱内 `read`/`write`，避免反复 API 调用。

## 关联主题页

- [managed agents](../guides/managed-agents.md)
- [file management api](../api/file-management-api.md)
- [skill](../guides/skill.md)
- [data connection overview](../guides/data-connection-overview.md)


