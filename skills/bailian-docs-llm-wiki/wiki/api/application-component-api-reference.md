# application component api reference

百炼平台应用组件 API（`bailian/2023-12-29`）采用 ROA 签名风格，提供数据连接、知识库、Prompt 工程等核心功能的程序化管理能力。开发者可通过官方 SDK 或自签名方式调用这些接口，实现文件管理、知识库构建与检索、Prompt 模板管理等操作。本文档汇总了各 API 的分类、关键参数、使用方式及限制约束。

## 接入准备

### 身份认证

调用 API 前需准备阿里云访问密钥（AccessKey）。建议创建 RAM 用户并遵循最小权限原则配置策略，避免使用主账号 AccessKey。百炼的 RAM 代码为 `sfm`，授权粒度为操作级。详见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。

### 服务接入点

| 地域 | 地域 ID | 公网地址 | VPC 地址 |
|------|---------|---------|----------|
| 华北2（北京） | cn-beijing | bailian.cn-beijing.aliyuncs.com | bailian-vpc.cn-beijing.aliyuncs.com |
| 新加坡 | ap-southeast-1 | bailian.ap-southeast-1.aliyuncs.com | bailian-vpc.ap-southeast-1.aliyuncs.com |

### SDK 与签名

推荐使用官方 SDK 调用，支持多种编程语言。自签名对接较为复杂（约需 5 个工作日），建议加入服务钉钉群（147535001692）获取指导。详见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

## API 分类

### 数据连接（原应用数据）

管理业务空间中的文件类目、文件上传/导入、标签、解析设置及连接器。

| API | 功能 | HTTP 方法 | 限流 |
|-----|------|-----------|------|
| AddCategory | 新增类目（最多 500 个/空间） | POST | 5 次/秒 |
| ListCategory | 获取类目列表 | POST | 5 次/秒 |
| DeleteCategory | 删除类目 | DELETE | 5 次/秒 |
| ApplyFileUploadLease | 申请文件上传租约 | POST | 10 次/秒 |
| AddFile | 添加文件到数据连接 | PUT | 10 次/秒 |
| AddFilesFromAuthorizedOss | 从已授权 OSS 导入文件 | POST | 5 次/秒 |
| ListFile | 查询文件列表 | GET | 5 次/秒 |
| DescribeFile | 查询文件状态 | GET | 10 次/秒 |
| UpdateFileTag | 更新文件标签 | PUT | 5 次/秒 |
| BatchUpdateFileTag | 批量更新文档标签 | PUT | - |
| DeleteFile | 删除文件 | DELETE | 10 次/秒 |
| GetParseSettings | 获取类目解析设置 | GET | 10 次/秒 |
| GetAvailableParserTypes | 获取支持的解析器类型 | GET | 10 次/秒 |
| ChangeParseSetting | 修改类目解析设置 | PUT | 10 次/秒 |
| AddTable | 添加表格 | POST | 10 次/秒 |
| UpdateTableFromAuthorizedOss | 从 OSS 更新表格 | PUT | 5 次/秒 |
| AddConnector | 新增连接器 | POST | 5 次/秒 |
| GetConnector | 获取连接器信息 | GET | 5 次/秒 |

### 知识库

管理知识库的完整生命周期：创建、提交任务、追加文档、检索、更新和删除。

| API | 功能 | HTTP 方法 | 限流 |
|-----|------|-----------|------|
| CreateIndex | 创建知识库 | POST | 10 次/秒 |
| SubmitIndexJob | 提交知识库创建任务 | POST | 10 次/秒 |
| SubmitIndexAddDocumentsJob | 追加文件到知识库 | POST | 10 次/秒 |
| GetIndexJobStatus | 查询任务状态 | GET | - |
| Retrieve | 检索知识库 | POST | - |
| ListIndices | 查询知识库列表 | GET | 10 次/秒 |
| ListIndexDocuments | 查询知识库文件列表 | GET | 15 次/秒 |
| ListIndexFileDetails | 查询知识库文件详情 | POST | - |
| UpdateIndex | 更新知识库配置 | POST | - |
| DeleteIndex | 删除知识库 | POST | 10 次/秒 |
| DeleteIndexDocument | 删除知识库文件 | POST | 10 次/秒 |
| ListChunks | 查询切片列表 | POST | 10 次/秒 |
| UpdateChunk | 修改切片 | POST | 10 次/秒 |
| DeleteChunk | 删除切片 | POST | 10 次/秒 |
| GetIndexMonitor | 获取知识库监控数据 | GET | - |

### Prompt 工程

管理 Prompt 模板的 CRUD 操作。

| API | 功能 | HTTP 方法 |
|-----|------|-----------|
| CreatePromptTemplate | 创建模板（不支持文生图） | POST |
| GetPromptTemplate | 获取模板 | GET |
| UpdatePromptTemplate | 增量更新模板 | PATCH |
| DeletePromptTemplate | 删除模板 | DELETE |
| ListPromptTemplates | 获取模板列表 | GET |

## 关键参数说明

### 通用路径参数

- **WorkspaceId**（string，必填）：业务空间 ID，所有 API 均需要在路径中指定。
- **IndexId**（string）：知识库 ID，由 `CreateIndex` 返回。
- **FileId**（string）：文件 ID，由 `AddFile` 返回。
- **CategoryId**（string）：类目 ID，由 `AddCategory` 返回。

### 分页参数

列表类接口支持分页，典型参数：
- `MaxResults`：每页返回的条目数
- `NextToken`：下一页查询凭证（为空表示无更多结果）
- 部分接口使用 `PageNumber` + `PageSize` 分页模式

### 文件解析器类型

`AddFile` 接口中 `Parser` 参数支持：
- `DOCMIND`：智能文档解析
- `DOCMIND_DIGITAL`：电子文档解析
- `DOCMIND_LLM_VERSION`：大模型文档解析
- `DASH_QWEN_VL_PARSER`：Qwen VL 解析
- `DOCMIND_LLM_VERSION_MEDIA`：音视频解析
- `AUTO_SELECT`：自动选择解析器

## 知识库使用流程

1. **上传文件**：`ApplyFileUploadLease` → 上传文件 → `AddFile`
2. **创建知识库**：`CreateIndex` → `SubmitIndexJob`（必须提交才能完成创建）
3. **追加文件**：`SubmitIndexAddDocumentsJob`
4. **查询状态**：`GetIndexJobStatus`（建议间隔 ≥5 秒）
5. **检索**：`Retrieve`

详细代码示例参见 [CreateIndex - 创建知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-createindex.md)。

## 权限要求

- RAM 用户需先获取百炼 API 权限策略：
  - `AliyunBailianDataFullAccess`：数据完全访问（覆盖绝大部分接口）
  - `AliyunBailianDataReadOnlyAccess`：只读访问（仅适用于 DescribeFile、GetParseSettings 等查询接口）
- RAM 用户需加入目标业务空间
- 阿里云主账号可直接调用无须额外授权

## 限制和注意事项

- **限流**：各接口有不同的 QPS 限制（通常 5~15 次/秒），遇到限流请稍后重试。
- **幂等性**：部分接口具有幂等性（如 `DeleteCategory`、`ListFile`、`Retrieve` 等），部分不具备（如 `AddCategory`、`AddFile`、`CreateIndex`）。调用前请查阅各接口说明。
- **不支持 API 操作的功能**：新增数据表、删除数据表需通过控制台操作；`SubmitIndexAddDocumentsJob` 不支持数据查询/图片问答类知识库。
- **删除操作不可逆**：`DeleteIndex`、`DeleteIndexDocument`、`DeleteChunk` 等删除操作为硬删除，无法恢复。
- **知识库创建后必须提交**：调用 `CreateIndex` 后若不调用 `SubmitIndexJob`，将得到空知识库。
- **OSS 导入要求**：OSS Bucket 需与百炼同属一个主账号，不支持归档/冷归档/深度冷归档存储类型。
- **文件状态约束**：`DeleteFile` 仅能删除状态为 `PARSE_FAILED` 或 `PARSE_SUCCESS` 的文件。
- **监控数据查询**：`GetIndexMonitor` 查询时间范围最大支持 30 天。

> **注意**：`DeleteFile` 接口删除的是应用数据中的文件，不会影响已构建的知识库。若需删除知识库中的文件，应使用 `DeleteIndexDocument` 接口。

> **注意**：版本说明中 `CreateIndex` 接口入参在 2026-03-27 和 2026-03-30 均发生变更，请确保使用最新版 SDK 以避免参数不兼容问题。详见 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)。

> **注意**：`UpdateChunk` 仅支持文档搜索类知识库，不支持数据查询和图片问答类知识库。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [AddCategory - 新增类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addcategory.md)
- [ListCategory - 类目列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listcategory.md)
- [DeleteCategory - 删除类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletecategory.md)
- [ApplyFileUploadLease - 申请文件上传租约](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-applyfileuploadlease.md)
- [ListFile - 文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listfile.md)
- [AddFilesFromAuthorizedOss - 从已授权OSS Bucket中导入文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfilesfromauthorizedoss.md)
- [AddFile - 添加文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfile.md)
- [DescribeFile - 查询文件状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-describefile.md)
- [UpdateFileTag - 更新文件标签](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updatefiletag.md)
- [DeleteFile - 删除文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletefile.md)
- [BatchUpdateFileTag - 批量更新文档标签](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-batchupdatefiletag.md)
- [GetParseSettings - 获取类目解析设置](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getparsesettings.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getavailableparsertypes.md)
- [ChangeParseSetting - 修改类目解析设置](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-changeparsesetting.md)
- [AddTable - 添加表格](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addtable.md)
- [UpdateTableFromAuthorizedOss - 从已授权OSS Bucket中选择文件更新表格](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updatetablefromauthorizedoss.md)
- [AddConnector - 新增连接器](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addconnector.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-createprompttemplate.md)
- [GetConnector - 获取连接器信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getconnector.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-getprompttemplate.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-updateprompttemplate.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-deleteprompttemplate.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-listprompttemplates.md)
- [CreateIndex - 创建知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-createindex.md)
- [GetIndexJobStatus - 查询知识库创建任务状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexjobstatus.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexjob.md)
- [SubmitIndexAddDocumentsJob - 提交知识库追加任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexadddocumentsjob.md)
- [Retrieve - 检索知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-retrieve.md)
- [ListIndexDocuments - 查询知识库下的文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexdocuments.md)
- [ListIndexFileDetails - 查询知识库下的文件详情](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexfiledetails.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindexdocument.md)
- [UpdateIndex - 更新知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updateindex.md)
- [ListIndices - 查询知识库列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindices.md)
- [DeleteIndex - 删除知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindex.md)
- [ListChunks - 查询索引下的分片列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listchunks.md)
- [DeleteChunk - 删除切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deletechunk.md)
- [UpdateChunk - 修改切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updatechunk.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexmonitor.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipaytransferstatus.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-applytempstoragelease.md)
- [GetMemory - 获取长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemory.md)
- [CreateMemory - 创建长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememory.md)
- [UpdateMemory - 更新长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememory.md)
- [DeleteMemory - 删除长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememory.md)
- [ListMemories - 获取长期记忆体列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemories.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememorynode.md)
- [GetMemoryNode - 获取记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemorynode.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememorynode.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememorynode.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemorynodes.md)

