# application component api reference

本 API 参考文档面向开发者，系统性地描述了百炼平台 Application Component（应用组件）层提供的核心 OpenAPI 能力，覆盖数据连接（原应用数据）、知识库、Prompt 模板等关键功能模块。所有接口均基于 `bailian/2023-12-29` 版本，采用 ROA 签名机制，推荐通过官方 SDK 调用以简化鉴权与请求构造。详细接入方式与安全要求请参见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

## 支持的模型/功能

Application Component API 主要提供三类能力：

- **数据连接管理**：支持类目（Category）、文件（File）、表格（Table）、连接器（Connector）的全生命周期操作，包括创建、查询、更新、删除及解析设置管理。例如，`AddCategory` 用于构建分类体系，`ApplyFileUploadLease` + `AddFile` 组合实现文件上传与入库，`ChangeParseSetting` 可为不同文件类型（如 `.pdf`, `.jpg`）指定专用解析器（如 `DOCMIND_LLM_VERSION`, `DASH_QWEN_VL_PARSER`）。具体支持的解析器类型可通过 `GetAvailableParserTypes` 接口动态查询，详见 [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getavailableparsertypes.md)。
- **知识库（RAG Index）管理**：覆盖知识库的创建（`CreateIndex`）、提交构建（`SubmitIndexJob`）、追加文档（`SubmitIndexAddDocumentsJob`）、检索（`Retrieve`）、查询（`ListIndices`, `ListIndexDocuments`）、更新（`UpdateIndex`）及删除（`DeleteIndex`）全流程。同时支持细粒度操作，如切片（Chunk）的增删改查（`ListChunks`, `UpdateChunk`, `DeleteChunk`）和监控（`GetIndexMonitor`）。
- **Prompt 工程支持**：提供 Prompt 模板的创建（`CreatePromptTemplate`）与获取（`GetPromptTemplate`）能力，支持变量占位符（如 `${theme}`），便于在应用中复用标准化提示词。

> **注意**：`CreateIndex` 接口仅初始化作业，必须调用 `SubmitIndexJob` 才能真正触发知识库构建；而 `Retrieve` 接口的响应延迟较高，需合理配置客户端超时与重试策略。

## 关键参数

- **通用路径参数**：几乎所有接口均需 `WorkspaceId`（业务空间 ID），用于隔离资源。其值可在控制台业务空间详情页获取，或通过 `ListIndices` 等接口返回结果中提取。
- **身份认证参数**：所有请求必须携带有效的 AccessKey ID/Secret，并按 ROA 规范签名。强烈建议使用 [阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29) 自动处理，避免手动签名错误。相关安全准备细节见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。
- **核心业务参数**：
  - 类目/文件操作：`CategoryId`（来自 `AddCategory` 返回）、`FileId`（来自 `AddFile` 返回）、`ConnectorId`（来自 `AddConnector` 返回）。
  - 知识库操作：`IndexId`（来自 `CreateIndex` 返回）、`JobId`（来自 `SubmitIndexJob` 返回）、`PipelineId`（同 `IndexId`，用于切片操作）。
  - 文件解析：`Parser`（在 `AddFile` 中指定，如 `AUTO_SELECT` 或 `DOCMIND_LLM_VERSION`）。
  - 分页与过滤：`MaxResults`/`NextToken`（列表接口）、`DocumentStatus`（知识库文件状态过滤）、`IndexName`（知识库名称模糊查询）。

## 使用方式

1. **环境准备**：确保已创建具备最小权限的 RAM 用户，并授予 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略。具体授权模型详见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。
2. **服务接入**：根据地域选择对应接入点，例如华北2（北京）的公网地址为 `bailian.cn-beijing.aliyuncs.com`，VPC 地址为 `bailian-vpc.cn-beijing.aliyuncs.com`。完整列表见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
3. **典型流程示例（构建知识库）**：
   - 调用 `AddCategory` 创建类目；
   - 调用 `ApplyFileUploadLease` 获取租约；
   - 将文件上传至租约地址；
   - 调用 `AddFile` 导入文件至该类目；
   - 调用 `CreateIndex` 初始化知识库；
   - 调用 `SubmitIndexJob` 启动构建；
   - 调用 `GetIndexJobStatus` 轮询任务状态直至完成；
   - 调用 `Retrieve` 进行检索。

## 限制和注意事项

- **限流规则**：各接口有独立 QPS 限制，例如 `AddCategory`/`ListCategory`/`DeleteCategory` 为 5 次/秒，`ApplyFileUploadLease`/`AddFile`/`DescribeFile` 为 10 次/秒，`ListIndexDocuments` 为 15 次/秒。超出将返回 429 错误，需实现退避重试逻辑。
- **幂等性**：`ListCategory`, `DescribeFile`, `ListFile`, `GetIndexJobStatus`, `Retrieve`, `DeleteIndex`, `UpdateChunk`, `DeleteChunk` 等接口具有幂等性；而 `AddCategory`, `AddFile`, `CreateIndex`, `SubmitIndexJob` 等不具备，重复调用可能产生冗余资源。
- **功能边界**：
  - 数据表（Table）的创建与删除不支持 API，必须通过控制台操作（见 `AddTable` 和 `DeleteFile` 文档说明）。
  - `DeleteFile` 仅删除应用数据中的文件，不影响已构建的知识库；反之，`DeleteIndexDocument` 仅删除知识库中的索引，不影响原始文件。
  - `UpdateIndex` 的 `PipelineCommercialCu` 参数仅对旗舰版（`enterprise`）知识库生效，标准版（`standard`）传入将被忽略。
- **版本兼容性**：API 行为可能随版本变更，例如 `DescribeFile` 在 2026-01-15 发生了返回结构变更，`CreateIndex` 在 2026-03-27 和 2026-03-30 均有入参调整。开发者应关注 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 并及时适配。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [AddCategory - 新增类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addcategory.md)
- [ListCategory - 类目列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listcategory.md)
- [ApplyFileUploadLease - 申请文件上传租约](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-applyfileuploadlease.md)
- [AddFile - 添加文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfile.md)
- [DeleteCategory - 删除类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletecategory.md)
- [DescribeFile - 查询文件状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-describefile.md)
- [ListFile - 文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listfile.md)
- [AddFilesFromAuthorizedOss - 从已授权OSS Bucket中导入文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfilesfromauthorizedoss.md)
- [DeleteFile - 删除文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletefile.md)
- [BatchUpdateFileTag - 批量更新文档标签](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-batchupdatefiletag.md)
- [UpdateFileTag - 更新文件标签](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updatefiletag.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getavailableparsertypes.md)
- [GetParseSettings - 获取类目解析设置](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getparsesettings.md)
- [DeleteFiles - 批量删除文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletefiles.md)
- [ChangeParseSetting - 修改类目解析设置](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-changeparsesetting.md)
- [UpdateTableFromAuthorizedOss - 从已授权OSS Bucket中选择文件更新表格](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updatetablefromauthorizedoss.md)
- [AddTable - 添加表格](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addtable.md)
- [AddConnector - 新增连接器](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addconnector.md)
- [GetConnector - 获取连接器信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getconnector.md)
- [UpdateConnector - 编辑连接器](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updateconnector.md)
- [CreateIndex - 创建知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-createindex.md)
- [GetIndexJobStatus - 查询知识库创建任务状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexjobstatus.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexjob.md)
- [SubmitIndexAddDocumentsJob - 提交知识库追加任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexadddocumentsjob.md)
- [Retrieve - 检索知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-retrieve.md)
- [ListIndexDocuments - 查询知识库下的文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexdocuments.md)
- [UpdateIndex - 更新知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updateindex.md)
- [ListIndexFileDetails - 查询知识库下的文件详情](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexfiledetails.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindexdocument.md)
- [DeleteIndex - 删除知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindex.md)
- [ListIndices - 查询知识库列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindices.md)
- [UpdateChunk - 修改切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updatechunk.md)
- [ListChunks - 查询索引下的分片列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listchunks.md)
- [DeleteChunk - 删除切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deletechunk.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-createprompttemplate.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexmonitor.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-getprompttemplate.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-updateprompttemplate.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-deleteprompttemplate.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-listprompttemplates.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-applytempstoragelease.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipaytransferstatus.md)
- [CreateMemory - 创建长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememory.md)
- [GetMemory - 获取长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemory.md)
- [UpdateMemory - 更新长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememory.md)
- [DeleteMemory - 删除长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememory.md)
- [ListMemories - 获取长期记忆体列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemories.md)
- [GetMemoryNode - 获取记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemorynode.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememorynode.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememorynode.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememorynode.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemorynodes.md)


