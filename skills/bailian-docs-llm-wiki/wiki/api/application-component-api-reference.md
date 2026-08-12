# application component api reference

本 API 参考文档面向开发者，涵盖百炼平台中应用组件（Application Component）的核心能力，包括数据连接（原应用数据）、知识库（RAG Index）、Prompt 模板及配套管理接口。所有接口均基于 `bailian/2023-12-29` 版本，采用 ROA 签名机制，支持多语言 SDK 封装，推荐优先使用 SDK 调用以规避签名复杂性 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

## 支持的模型/功能

API 主要支撑三类核心能力：

- **数据连接（Data Connection）**：提供类目（Category）、文件（File）、连接器（Connector）、表格（Table）的全生命周期管理，支持从本地、OSS 导入文件与结构化数据。例如 `AddCategory` 用于创建分类体系，`AddFilesFromAuthorizedOss` 支持批量导入已授权 OSS 文件 [AddFilesFromAuthorizedOss](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfilesfromauthorizedoss.md)。
- **知识库（Index / RAG）**：覆盖非结构化（文档/音视频）与结构化（数据查询/图片问答）两类知识库的创建、更新、监控与内容管理。关键流程为：`CreateIndex` → `SubmitIndexJob` → `ListIndexDocuments` → `Retrieve`；支持细粒度操作如 `UpdateChunk`（修改文本切片）、`DeleteIndexDocument`（删除知识库内文件），但注意该操作不影响原始应用数据 [DeleteIndexDocument](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindexdocument.md)。
- **Prompt 工程**：提供 `CreatePromptTemplate` 和 `GetPromptTemplate` 接口，支持模板的创建、获取与变量注入，当前不支持文生图类 Prompt 模板。

> **注意**：文档 37（`AddChunk`）声明支持 document/table/image 三类知识库，但文档 36（`UpdateChunk`）明确限定仅支持 document 类型；且文档 37 的权限描述错误地引用了 `sfm:ChunkList`（应为 `sfm:AddChunk`）。实际开发中请以 `UpdateChunk` 的限制为准，并确认目标知识库类型。

## 关键参数

- **WorkspaceId（业务空间 ID）**：几乎所有接口的路径参数，标识资源归属空间，需通过控制台或 `ListIndices` 等接口获取。
- **CategoryId / FileId / IndexId / ConnectorId**：各资源的唯一标识符，通常由上游接口（如 `AddCategory`、`AddFile`、`CreateIndex`）返回，不可自行构造。
- **Parser（解析器类型）**：在 `AddFile` 中指定，影响文档解析质量，可选值包括 `DOCMIND`、`DOCMIND_LLM_VERSION`、`AUTO_SELECT` 等，具体支持列表需结合 `GetAvailableParserTypes` 动态查询。
- **Time Range（时间范围）**：`GetIndexMonitor` 接口要求 `StartTimestamp` 和 `EndTimestamp` 均为秒级 Unix 时间戳，且时间跨度不得超过 30 天。
- **Chunk-level Fields**：`AddChunk` 和 `ListChunks` 中的 `Fields` 参数用于过滤元数据字段；`AddChunk` 的 `field` 对象结构因知识库类型而异：document 类固定为 `content`/`title`/`image_urls`，table/image 类则映射至源 Excel 表头。

## 使用方式

1. **准备环境**：
   - 创建 RAM 用户并授予最小权限策略（如 `AliyunBailianDataFullAccess`），避免使用主账号 AK [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。
   - 获取 AccessKey 并配置 SDK 或客户端工具。
   - 根据地域选择服务接入点（如 `bailian.cn-beijing.aliyuncs.com`）[服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。

2. **典型流程示例（知识库构建）**：
   ```bash
   # 1. 创建类目
   POST /{WorkspaceId}/datacenter/category/
   # 2. 申请上传租约
   POST /{WorkspaceId}/datacenter/category/{CategoryId}
   # 3. 上传并解析文件
   PUT /{WorkspaceId}/datacenter/file
   # 4. 创建知识库
   POST /{WorkspaceId}/index/create
   # 5. 提交构建任务
   POST /{WorkspaceId}/index/submit_index_job
   # 6. 查询状态直至完成
   GET /{WorkspaceId}/index/job/status?JobId=xxx
   ```

3. **调试与开发**：
   - 所有接口均支持在 [OpenAPI Explorer](https://api.aliyun.com) 直接调试，自动生成 SDK 示例代码。
   - 推荐使用官方 SDK（版本 `2023-12-29`），避免手动签名。

## 限制和注意事项

- **限流策略**：多数接口有严格 QPS 限制（如 `AddCategory`/`DeleteCategory` 为 5 次/秒，`AddFile`/`ApplyFileUploadLease` 为 10 次/秒），超限将返回 429 错误，需实现退避重试。
- **幂等性**：`DeleteCategory`、`ListCategory`、`DescribeFile` 等读/删操作具备幂等性；`AddCategory`、`AddFile` 等创建操作不具备幂等性，重复调用可能产生冗余资源。
- **资源依赖与约束**：
  - `DeleteIndexDocument` 仅支持状态为 `FINISH` 或 `INSERT_ERROR` 的文件，且不删除原始应用数据。
  - `UpdateChunk` 仅适用于 `document` 类知识库，对 `table`/`image` 类无效。
  - `AddTable`/`UpdateTableFromAuthorizedOss` 仅支持结构化数据连接器，不适用于非结构化知识库。
- **安全要求**：OSS Bucket 必须与百炼同属一阿里云账号，且 Referer 白名单需包含 `*.console.aliyun.com`；RAM 策略应遵循最小权限原则，禁止授予 `*` 全资源权限。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [AddCategory - 新增类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addcategory.md)
- [DeleteCategory - 删除类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletecategory.md)
- [ListCategory - 类目列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listcategory.md)
- [ApplyFileUploadLease - 申请文件上传租约](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-applyfileuploadlease.md)
- [AddFile - 添加文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfile.md)
- [AddFilesFromAuthorizedOss - 从已授权OSS Bucket中导入文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfilesfromauthorizedoss.md)
- [ListFile - 文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listfile.md)
- [UpdateFileTag - 更新文件标签](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updatefiletag.md)
- [DescribeFile - 查询文件状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-describefile.md)
- [DeleteFile - 删除文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletefile.md)
- [DeleteFiles - 批量删除文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletefiles.md)
- [BatchUpdateFileTag - 批量更新文档标签](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-batchupdatefiletag.md)
- [GetParseSettings - 获取类目解析设置](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getparsesettings.md)
- [ChangeParseSetting - 修改类目解析设置](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-changeparsesetting.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getavailableparsertypes.md)
- [UpdateTableFromAuthorizedOss - 从已授权OSS Bucket中选择文件更新表格](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updatetablefromauthorizedoss.md)
- [AddTable - 添加表格](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addtable.md)
- [GetConnector - 获取连接器信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getconnector.md)
- [AddConnector - 新增连接器](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addconnector.md)
- [UpdateConnector - 编辑连接器](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updateconnector.md)
- [CreateIndex - 创建知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-createindex.md)
- [GetIndexJobStatus - 查询知识库创建任务状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexjobstatus.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexjob.md)
- [SubmitIndexAddDocumentsJob - 提交知识库追加任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexadddocumentsjob.md)
- [ListIndexFileDetails - 查询知识库下的文件详情](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexfiledetails.md)
- [ListIndexDocuments - 查询知识库下的文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexdocuments.md)
- [UpdateIndex - 更新知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updateindex.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindexdocument.md)
- [ListIndices - 查询知识库列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindices.md)
- [ListChunks - 查询索引下的分片列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listchunks.md)
- [DeleteIndex - 删除知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindex.md)
- [UpdateChunk - 修改切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updatechunk.md)
- [AddChunk - 新增切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-addchunk.md)
- [DeleteChunk - 删除切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deletechunk.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-createprompttemplate.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexmonitor.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-getprompttemplate.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-updateprompttemplate.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-deleteprompttemplate.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-listprompttemplates.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipaytransferstatus.md)
- [CreateMemory - 创建长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememory.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-applytempstoragelease.md)
- [GetMemory - 获取长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemory.md)
- [UpdateMemory - 更新长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememory.md)
- [DeleteMemory - 删除长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememory.md)
- [ListMemories - 获取长期记忆体列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemories.md)
- [Retrieve - 检索知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-retrieve.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememorynode.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememorynode.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemorynodes.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememorynode.md)
- [GetMemoryNode - 获取记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemorynode.md)


