# application component api reference

本 API 参考文档面向开发者，系统性地描述了百炼平台 Application Component（应用组件）层提供的核心 OpenAPI 能力，涵盖数据连接（应用数据）、知识库、[Prompt 工程](../concepts/prompt-engineering.md)三大功能域。所有接口均基于 `bailian/2023-12-29` 版本，采用 ROA 签名机制，支持通过官方 SDK 或自签名方式调用。开发者需预先配置 RAM 权限与业务空间成员身份方可使用。

## 支持的模型/功能

Application Component API 主要提供三类能力：

- **数据连接（应用数据）**：管理非结构化文件与结构化表格。支持类目（Category）的增删查（`AddCategory`、`ListCategory`、`DeleteCategory`）、文件上传与元数据管理（`ApplyFileUploadLease`、`AddFile`、`ListFile`、`DescribeFile`）、OSS 批量导入（`AddFilesFromAuthorizedOss`）、解析器配置（`GetAvailableParserTypes`、`ChangeParseSetting`）及连接器管理（`AddConnector`、`UpdateConnector`）。注意：[API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 明确指出“不支持通过 API 新增或删除数据表”，相关操作需通过控制台完成。

- **知识库（Index）**：支持全生命周期管理。包括创建（`CreateIndex`）、提交构建任务（`SubmitIndexJob`）、追加文档（`SubmitIndexAddDocumentsJob`）、检索（`Retrieve`）、查询列表与详情（`ListIndices`、`ListIndexDocuments`、`ListIndexFileDetails`）、更新配置（`UpdateIndex`）、监控（`GetIndexMonitor`）及删除（`DeleteIndex`）。对于文档类知识库，还支持细粒度切片操作（`AddChunk`、`UpdateChunk`、`DeleteChunk`）。> **注意**：`AddChunk` 文档 [AddChunk - 新增切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-addchunk.md) 与 `UpdateChunk` 文档 [UpdateChunk - 修改切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updatechunk.md) 在支持的知识库类型上存在矛盾：前者声明支持 `document`/`table`/`image` 三类，后者明确限定“仅支持文档搜索类知识库”。实际开发中，请以 `UpdateChunk` 的限制为准，避免在非文档类知识库上误用。

- **[Prompt 工程](../concepts/prompt-engineering.md)**：提供 Prompt 模板的 CRUD 操作，包括创建（`CreatePromptTemplate`）、更新（`UpdatePromptTemplate`）、删除（`DeletePromptTemplate`）和列表查询（`ListPromptTemplates`）。[CreatePromptTemplate - 创建Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-createprompttemplate.md) 明确说明“暂不支持文生图 Prompt 模板的创建”。

## 关键参数

- **通用路径参数**：几乎所有接口均需 `WorkspaceId`（业务空间 ID），用于隔离资源。获取方式请参见 [如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。
- **鉴权参数**：所有请求必须携带有效的 `AccessKey ID` 和 `AccessKey Secret` 进行 ROA 签名。强烈建议遵循最小权限原则，为 RAM 用户配置精确的权限策略，而非直接使用主账号密钥。
- **核心业务参数**：
  - 类目操作：`CategoryId`（由 `AddCategory` 返回）。
  - 文件操作：`FileId`（由 `AddFile` 返回）、`LeaseId`（由 `ApplyFileUploadLease` 返回）。
  - 知识库操作：`IndexId`（由 `CreateIndex` 返回）、`JobId`（由 `SubmitIndexJob` 返回）。
  - 切片操作：`ChunkId`（由 `ListChunks` 返回的 `Node.Metadata._id` 字段）。
  - Prompt 操作：`promptTemplateId`（由 `CreatePromptTemplate` 返回）。
- **分页参数**：`List*` 类接口普遍支持 `MaxResults`/`PageSize` 与 `NextToken`/`nextToken` 实现分页，首次请求只需设置 `MaxResults`，后续请求需传入前次响应中的 `NextToken`。

## 使用方式

1. **准备环境**：创建具备 `AliyunBailianDataFullAccess`（或更细粒度策略）权限的 RAM 用户，并将其加入目标业务空间。
2. **选择接入方式**：
   - **推荐**：使用官方 SDK（如 Python、Java 版），它已封装签名逻辑与错误处理。SDK 下载地址见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。
   - **自定义**：若需自签名，务必参考 [ROA 机制文档](https://help.aliyun.com/zh/sdk/product-overview/roa-mechanism) 并加入服务钉钉群（147535001692）获取专家指导，因自签名复杂度高且易出错。
3. **确定接入点**：根据部署地域选择对应的服务接入地址，例如华北2（北京）为 `bailian.cn-beijing.aliyuncs.com`，详见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
4. **调用流程示例（知识库）**：
   - 调用 `CreateIndex` 初始化知识库。
   - 调用 `SubmitIndexJob` 提交构建任务。
   - 调用 `GetIndexJobStatus` 轮询任务状态直至完成。
   - 调用 `Retrieve` 进行检索。

## 限制和注意事项

- **限流策略**：各接口均有严格 QPS 限制，常见值为 5~10 次/秒。超出将返回限流错误，需实现退避重试逻辑。具体数值请查阅各接口文档的“限流说明”章节。
- **幂等性**：`List*`、`Describe*`、`Get*` 及部分 `Delete*` 接口（如 `DeleteCategory`、`DeleteFile`）具有幂等性；而 `Add*`、`Create*`、`Submit*` 等创建类接口不具备幂等性，重复调用可能产生冗余资源。
- **状态依赖**：知识库相关操作（如 `SubmitIndexAddDocumentsJob`、`DeleteIndexDocument`）要求知识库处于 `FINISH` 状态；文件操作（如 `DeleteFile`）要求文件状态为 `PARSE_SUCCESS` 或 `PARSE_FAILED`。务必先通过 `DescribeFile` 或 `ListIndexDocuments` 查询状态。
- **安全与权限**：RAM 权限策略需精确到 `Action`（如 `sfm:ListCategory`），并遵循最小权限原则。主账号密钥泄露风险极高，严禁在客户端代码中硬编码。
- **数据一致性**：`DeleteFile` 仅删除应用数据中的文件，不影响已构建的知识库；反之，`DeleteIndexDocument` 仅删除知识库索引，不影响原始应用数据。两者互不影响。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [AddCategory - 新增类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addcategory.md)
- [ListCategory - 类目列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listcategory.md)
- [DeleteCategory - 删除类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletecategory.md)
- [ApplyFileUploadLease - 申请文件上传租约](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-applyfileuploadlease.md)
- [AddFile - 添加文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfile.md)
- [AddFilesFromAuthorizedOss - 从已授权OSS Bucket中导入文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfilesfromauthorizedoss.md)
- [ListFile - 文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listfile.md)
- [DescribeFile - 查询文件状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-describefile.md)
- [UpdateFileTag - 更新文件标签](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updatefiletag.md)
- [DeleteFile - 删除文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletefile.md)
- [BatchUpdateFileTag - 批量更新文档标签](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-batchupdatefiletag.md)
- [GetParseSettings - 获取类目解析设置](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getparsesettings.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getavailableparsertypes.md)
- [DeleteFiles - 批量删除文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletefiles.md)
- [UpdateTableFromAuthorizedOss - 从已授权OSS Bucket中选择文件更新表格](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updatetablefromauthorizedoss.md)
- [AddTable - 添加表格](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addtable.md)
- [ChangeParseSetting - 修改类目解析设置](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-changeparsesetting.md)
- [AddConnector - 新增连接器](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addconnector.md)
- [UpdateConnector - 编辑连接器](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updateconnector.md)
- [CreateIndex - 创建知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-createindex.md)
- [GetIndexJobStatus - 查询知识库创建任务状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexjobstatus.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexjob.md)
- [SubmitIndexAddDocumentsJob - 提交知识库追加任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexadddocumentsjob.md)
- [Retrieve - 检索知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-retrieve.md)
- [ListIndexDocuments - 查询知识库下的文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexdocuments.md)
- [ListIndexFileDetails - 查询知识库下的文件详情](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexfiledetails.md)
- [UpdateIndex - 更新知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updateindex.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindexdocument.md)
- [ListIndices - 查询知识库列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindices.md)
- [DeleteIndex - 删除知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindex.md)
- [AddChunk - 新增切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-addchunk.md)
- [UpdateChunk - 修改切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updatechunk.md)
- [DeleteChunk - 删除切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deletechunk.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexmonitor.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-createprompttemplate.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-updateprompttemplate.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-deleteprompttemplate.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-listprompttemplates.md)
- [CreateMemory - 创建长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememory.md)
- [GetMemory - 获取长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemory.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [UpdateMemory - 更新长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememory.md)
- [DeleteMemory - 删除长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememory.md)
- [ListMemories - 获取长期记忆体列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemories.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememorynode.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememorynode.md)
- [GetMemoryNode - 获取记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemorynode.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememorynode.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemorynodes.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-applytempstoragelease.md)


