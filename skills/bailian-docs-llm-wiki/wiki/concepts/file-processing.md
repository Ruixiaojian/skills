# 文件处理

文件处理是百炼平台中统一抽象的、面向非结构化与半结构化数据（如文本、表格、图像）的接入、解析、操作与协同能力，贯穿模型调用、智能体运行、知识库构建及技能执行等多个核心场景。它不指代单一 API，而是由文件管理、数据连接、Managed Agents 和 Skill 等模块协同提供的端到端能力集合，核心目标是让大模型和智能体能安全、可控、语义化地“理解并操作文件”。

## 在百炼平台的不同场景中，这个概念如何使用

- **文件管理 API（基础层）**：提供文件的上传、查询、列举与删除等全生命周期元数据与二进制操作。上传后获得全局唯一的 `file_id`，该 ID 可在后续任意支持文件引用的接口（如 `chat/completions`、Managed Agents 会话、Skill 调用）中复用。注意：此层仅托管文件，**不执行解析或嵌入生成**，纯属资源中枢。

- **Managed Agents（运行时层）**：在沙箱环境中支持对已挂载文件的实时读写、编辑、执行命令（如 `bash`, `grep`, `edit`）。文件通过 `resources` 参数挂载至 `/mnt/session/uploads/` 下，单文件 ≤10 MB；Agent 可基于上下文自主调用工具完成清洗、转换、分析等操作，状态跨事件持久化，但 Session 终止即销毁。

- **数据连接（知识层）**：通过「文件连接器」或「表格连接器」将 PDF/Word/Excel/CSV 等文件批量导入平台，触发后台文档理解服务（如 Qwen-VL [多模态](multi-modal.md)解析），构建可检索的知识库。此过程为异步、批处理式，生成独立副本，适用于 RAG 场景；不支持 JSON/YAML 直接导入，需转为 XLSX/XLS。

- **Skill（能力封装层）**：以预置或自定义 ZIP 包形式封装专业文件处理逻辑（如发票识别、Excel 表格生成、PDF 文本提取）。Skill 由模型根据用户指令语义 + 附件类型自动匹配调用，输出结果以新文件形式返回（如 `.xlsx`），运行于沙箱，禁止外网访问与系统命令。

- **Application Support（应用集成层）**：在 RAG 应用中直接上传 `.pdf`（小写）、`.docx` 等格式文档作为知识源；文件格式与命名（如 `.pdf` 必须小写）直接影响解析成功率。此层强调易用性，但底层仍依赖文件管理 API 上传 + 数据连接解析流水线。

> ⚠️ 关键区分：  
> - `file_id` 是跨模块复用的统一标识符，但**用途受 `purpose` 参数约束**（`assistants` vs `vision`）；  
> - 文件解析（OCR、结构提取、向量化）由 `document_parse` 或数据连接后台异步完成，**不可通过文件管理 API 同步触发**；  
> - 所有文件操作均默认**无自动清理策略**，需开发者主动调用 DELETE 或通过配额管理控制。

## 关键参数和配置

| 模块 | 参数/配置项 | 说明 | 典型值/限制 |
|------|-------------|------|-------------|
| **文件管理 API** | `purpose` | 决定文件在下游模型中的可用范围 | `assistants`（默认，用于文本模型）、`vision`（用于 Qwen-VL 等[多模态](multi-modal.md)模型） |
| | `file_id` | 上传成功后返回的全局唯一 ID，用于所有引用场景 | 字符串，不可修改、不可重用 |
| | 单文件大小 | 上传硬限制 | ≤ 512 MB（超出返回 `413`） |
| **Managed Agents** | `resources` | 挂载文件列表，含 `resource_id`（即 `file_id`）与 `mount_path` | 路径固定为 `/mnt/session/uploads/{filename}`，单文件 ≤10 MB |
| | `tools` | 控制是否启用内置文件工具（`read`/`write`/`edit` 等） | 默认全启用，暂不支持细粒度开关 |
| **数据连接（文件/表格）** | 存储位置 | 决定数据副本归属 | 平台存储（免费额度：200,000 文件 + 1 TB）或自有 OSS（需打 `bailian-connector-access: ReadAndWrite` 标签） |
| | 解析方式 | 影响内容提取质量 | 默认（平台优化策略）或自定义（指定 OCR/版面模型） |
| **Skill** | `description`（SKILL.md） | Skill 是否被触发的核心语义依据 | 必须明确声明支持的输入类型（如 `"PDF 发票"`）、操作（如 `"提取金额与日期"`）及不适用场景 |
| | ZIP 包大小 | 自定义 Skill 上传限制 | ≤ 10 MB（超限直接拒绝） |

## 面向开发者，简洁实用

- ✅ **统一 ID，分场景复用**：一次上传（`POST /v1/files`），获取 `file_id`，即可在 Agents 会话、Skill 调用、RAG 知识库、`chat/completions` 中引用——但务必确认 `purpose` 匹配目标模型能力。
- ✅ **按需选择处理层级**：
  - 快速托管+引用 → 用 **文件管理 API**；
  - 需沙箱内交互式操作（如改 Excel、跑脚本）→ 用 **Managed Agents**；
  - 批量导入+构建知识库 → 用 **数据连接（文件连接器）**；
  - 封装专业逻辑（如合同比对）→ 开发 **Skill**。
- ✅ **避坑清单**：
  - 图像文件若要用于 `qwen-vl`，上传时必须设 `purpose=vision`，否则无法引用；
  - 文件连接器不支持 `.json`/`.csv` 直传，需转 `.xlsx`；
  - Managed Agents 挂载文件路径固定为 `/mnt/session/uploads/...`，勿硬编码其他路径；
  - Skill 的 `description` 必须覆盖典型触发词+文件类型，否则模型大概率漏触发；
  - 所有删除操作（DELETE `/v1/files/{id}`）**不可逆**，且立即使关联调用失效。

文件处理不是黑盒，而是百炼平台能力分层设计的体现：底层管资源，中层管执行，上层管语义。掌握各层边界与协作方式，即可高效构建稳健的文件智能应用。

## 关联主题页

- [file management api](../api/file-management-api.md)
- [managed agents](../guides/managed-agents.md)
- [data connection overview](../guides/data-connection-overview.md)
- [skill](../guides/skill.md)
- [application support](../guides/application-support.md)


