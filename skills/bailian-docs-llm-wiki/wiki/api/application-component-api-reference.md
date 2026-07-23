# application component api reference

本 API 参考文档面向开发者，系统性地描述了百炼平台 Application Component（应用组件）提供的核心 OpenAPI 能力，涵盖数据连接（应用数据）、知识库、[Prompt 工程](../concepts/prompt-engineering.md)及辅助功能等模块。所有接口均基于 `bailian/2023-12-29` 版本，采用 ROA 签名机制，支持多语言 SDK 封装调用。开发者需通过 RAM 子账号配合最小权限策略进行安全接入。

## 支持的模型/功能

Application Component 提供以下四类核心能力：

- **数据连接（原应用数据）**：管理非结构化文件与结构化表格。支持类目（Category）增删查、文件上传（`ApplyFileUploadLease` + `AddFile`）、OSS 批量导入（`AddFilesFromAuthorizedOss`）、解析器配置（`GetAvailableParserTypes`, `ChangeParseSetting`）及连接器管理（`AddConnector`, `GetConnector`）。注意：API 不支持直接操作数据表（如新增/删除表），该功能仅限控制台，详见 [AddTable - 添加表格](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addtable.md) 文档说明。
- **知识库（Knowledge Base）**：支持创建（`CreateIndex`）、更新（`UpdateIndex`）、删除（`DeleteIndex`）知识库；向知识库追加文档（`SubmitIndexAddDocumentsJob`）、检索（`Retrieve`）、查询文件列表（`ListIndexDocuments`）及删除知识库内文件（`DeleteIndexDocument`）。知识库类型包括文档/音视频（非结构化）和数据查询/图片问答（结构化）两类。
- **[Prompt 工程](../concepts/prompt-engineering.md)**：提供完整的 Prompt 模板生命周期管理，包括创建（`CreatePromptTemplate`）、获取（`GetPromptTemplate`）、更新（`UpdatePromptTemplate`）、删除（`DeletePromptTemplate`）及列表查询（`ListPromptTemplates`）。
- **辅助功能**：包含支付宝打赏状态查询（`GetAlipayTransferStatus`）、临时存储租约申请（`ApplyTempStorageLease`）等场景化能力。

> **注意**：文档 33 (`AddChunk`) 明确指出“目前尚不支持对音视频搜索类（multimedia）知识库进行相关操作”，而文档 34 (`CreateIndex`) 则将知识库类型划分为“基于文档或音视频的非结构化知识库”与“用于数据查询或图片问答的结构化知识库”。二者存在表述矛盾——实际能力以 `CreateIndex` 的分类为准，`AddChunk` 接口当前仅适用于 `document`、`table` 和 `image` 类型知识库，不支持 `multimedia` 类型。

## 关键参数

- **通用路径参数**：几乎所有接口均需 `WorkspaceId`（业务空间 ID），用于标识资源归属。其值可通过控制台或 `ListWorkspace` 接口获取。
- **身份认证**：所有请求必须携带有效的 AccessKey（建议使用 RAM 子账号并遵循最小权限原则），签名方式为 ROA。详细准备流程见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。
- **分页与幂等**：
  - 分页接口（如 `ListCategory`, `ListFile`, `ListPromptTemplates`）统一使用 `MaxResults`（每页最大条数）和 `NextToken`（下一页凭证）实现。
  - 幂等性接口（如 `ListCategory`, `DescribeFile`, `Retrieve`）可安全重试；非幂等接口（如 `AddCategory`, `ApplyFileUploadLease`）重复调用可能导致重复资源创建或失败。
- **关键业务参数**：
  - 文件操作：`CategoryId`（类目 ID）、`FileId`（文件 ID）、`LeaseId`（上传租约 ID）是串联 `ApplyFileUploadLease` → `AddFile` 流程的核心。
  - 知识库操作：`IndexId`（知识库 ID）、`JobId`（任务 ID）是关联 `CreateIndex` → `SubmitIndexJob` → `GetIndexJobStatus` 的关键。
  - 解析器：`Parser`（如 `DOCMIND`, `AUTO_SELECT`）在 `AddFile` 中指定；`FileType`（如 `pdf`, `docx`）在 `GetAvailableParserTypes` 中用于查询支持类型。

## 使用方式

1. **环境准备**：按 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 文档指引，创建 RAM 用户、配置 `AliyunBailianDataFullAccess` 或更细粒度策略，并加入目标业务空间。
2. **接入点选择**：根据部署地域选择对应服务接入点，例如华北2（北京）公网地址为 `bailian.cn-beijing.aliyuncs.com`，VPC 地址为 `bailian-vpc.cn-beijing.aliyuncs.com`，完整列表见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
3. **SDK 调用（推荐）**：下载并初始化最新版 [阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)，传入 `AccessKeyId`, `AccessKeySecret`, `RegionId`（如 `cn-beijing`）及 `WorkspaceId` 即可调用各接口方法，无需手动签名。
4. **自签名调用（备选）**：若需自定义签名，务必参考 ROA 机制文档，并强烈建议加入钉钉群（147535001692）获取技术支持，避免因签名错误导致调试周期过长。
5. **典型流程示例（文件导入知识库）**：
   - 调用 `ApplyFileUploadLease` 获取 `LeaseId`；
   - 使用 `LeaseId` 和 OSS URL 上传文件至临时存储；
   - 调用 `AddFile` 将文件导入应用数据，并指定 `Parser`；
   - 调用 `CreateIndex` 创建知识库；
   - 调用 `SubmitIndexAddDocumentsJob` 将已导入的文件追加至知识库；
   - 调用 `GetIndexJobStatus` 轮询任务状态，直至完成。

## 限制和注意事项

- **限流策略**：各接口有独立 QPS 限制，例如 `ListCategory`/`DeleteCategory` 为 5 次/秒，`ApplyFileUploadLease`/`AddFile` 为 10 次/秒，`Retrieve` 为 15 次/秒。超出限制将返回 HTTP 429，需实现退避重试逻辑。
- **权限隔离**：RAM 用户必须被显式授权（如 `sfm:ListCategory`）并加入业务空间后才能调用对应接口；主账号默认拥有全部权限。
- **数据一致性**：
  - `DeleteFile` 仅删除应用数据中的文件，不影响已构建的知识库内容；反之，`DeleteIndexDocument` 仅删除知识库索引，不影响应用数据源。
  - `AddFilesFromAuthorizedOss` 要求 OSS Bucket 与百炼同属一个阿里云主账号，并已完成跨服务授权。
- **版本兼容性**：API 入参与返回结构可能随版本变更，例如 `DescribeFile` 在 2026-01-15 发生返回结构变更，`CreateIndex` 在 2026-03-27 和 2026-03-30 均有入参变更。开发者应关注 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中的变更集，及时适配。

## 来源文档

- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [ListCategory - 类目列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listcategory.md)
- [DeleteCategory - 删除类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletecategory.md)
- [ApplyFileUploadLease - 申请文件上传租约](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-applyfileuploadlease.md)
- [AddFile - 添加文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfile.md)
- [AddFilesFromAuthorizedOss - 从已授权OSS Bucket中导入文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfilesfromauthorizedoss.md)
- [ListFile - 文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listfile.md)
- [DescribeFile - 查询文件状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-describefile.md)
- [UpdateFileTag - 更新文件标签](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updatefiletag.md)
- [BatchUpdateFileTag - 批量更新文档标签](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-batchupdatefiletag.md)
- [DeleteFile - 删除文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletefile.md)
- [DeleteFiles - 批量删除文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletefiles.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getavailableparsertypes.md)
- [GetParseSettings - 获取类目解析设置](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getparsesettings.md)
- [ChangeParseSetting - 修改类目解析设置](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-changeparsesetting.md)
- [UpdateTableFromAuthorizedOss - 从已授权OSS Bucket中选择文件更新表格](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updatetablefromauthorizedoss.md)
- [AddConnector - 新增连接器](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addconnector.md)
- [GetConnector - 获取连接器信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getconnector.md)
- [UpdateConnector - 编辑连接器](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updateconnector.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-createprompttemplate.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-getprompttemplate.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-updateprompttemplate.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-deleteprompttemplate.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-listprompttemplates.md)
- [AddCategory - 新增类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addcategory.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipaytransferstatus.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-applytempstoragelease.md)
- [AddTable - 添加表格](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addtable.md)
- [AddChunk - 新增切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-addchunk.md)
- [CreateIndex - 创建知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-createindex.md)
- [SubmitIndexAddDocumentsJob - 提交知识库追加任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexadddocumentsjob.md)
- [GetIndexJobStatus - 查询知识库创建任务状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexjobstatus.md)
- [Retrieve - 检索知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-retrieve.md)
- [ListIndexDocuments - 查询知识库下的文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexdocuments.md)
- [ListIndexFileDetails - 查询知识库下的文件详情](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexfiledetails.md)
- [UpdateIndex - 更新知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updateindex.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindexdocument.md)
- [DeleteIndex - 删除知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindex.md)
- [ListIndices - 查询知识库列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindices.md)
- [ListChunks - 查询索引下的分片列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listchunks.md)
- [UpdateChunk - 修改切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updatechunk.md)
- [DeleteChunk - 删除切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deletechunk.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexmonitor.md)
- [CreateMemory - 创建长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememory.md)
- [UpdateMemory - 更新长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememory.md)
- [GetMemory - 获取长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemory.md)
- [DeleteMemory - 删除长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememory.md)
- [ListMemories - 获取长期记忆体列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemories.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememorynode.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememorynode.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememorynode.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemorynodes.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexjob.md)
- [GetMemoryNode - 获取记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemorynode.md)


