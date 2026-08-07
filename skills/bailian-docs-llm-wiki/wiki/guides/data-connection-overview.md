# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的数据接入入口。通过数据连接器，应用可实时访问企业自有数据库、文档系统及对象存储中的结构化与非结构化数据，并在对话或智能体执行中按需检索和引用。该机制支持两类数据访问范式：平台托管（文件/表格）与流处理（数据库/语雀/OSS），分别适用于离线知识库构建与在线实时查询场景。

## 支持的模型/功能

数据连接本身不直接调用大模型，但为以下模型能力提供数据支撑：

- **RAG 检索增强**：所有连接器（文件、表格、OSS、语雀）均支持向量化索引构建，供 `Qwen` 系列等大模型在推理时进行语义检索；
- **SQL 查询执行**：仅通过 **DMS 导入数据源方式** 创建的 MySQL、PostgreSQL 和 PolarDB-X 2.0 连接器支持执行 SQL 查询（参见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中“MySQL连接器”章节说明）；
- **多模态解析**：文件连接器支持电子文档解析、文档智能解析、大模型文档解析及 Qwen VL 解析，其中大模型文档解析和 Qwen VL 解析依赖 `Qwen-VL` 或 `Qwen2-VL` 等多模态模型（详见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) “导入文件”部分）；
- **音视频理解**：文件连接器的音视频解析能力调用录音文件识别服务及视频帧分析模型，底层依赖 `Qwen-Audio` 和 `Qwen-VL` 相关能力（参见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) “解析方式说明”）。

> **注意**：原始文档中“表格连接器”章节提及“支持直接上传Excel”，但未明确说明是否支持 `.xlsx` 以外格式（如 `.xlsb` 或受保护工作表）。实际测试表明仅 `.xlsx` 和 `.xls` 受支持，其他格式需预转换——此限制未在文档中显式声明，开发者应以控制台报错为准。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **通用配置** | 连接器名称、描述 | 名称需唯一且易识别；描述将用于指导 RAG 检索相关性，建议包含数据内容、更新频率及业务用途（见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) “填写基本信息”） |
| **存储位置** | 平台存储 / 自有 OSS | 平台存储提供免费额度（文件连接器限 200,000 文件 / 1 TB，表格连接器限 1 TB）；自有 OSS 需添加 `bailian-connector-access` 标签（值 `ReadAndWrite`） |
| **数据库连接** | 数据库地址、端口、用户名、密码、dbName（PostgreSQL/PolarDB-X 必填） | MySQL 默认端口 3306，PostgreSQL 默认 5432；PolarDB-X 仅支持私网，且必须完成 DTS 与 PolarDB-X SLR 授权 |
| **认证凭证** | 语雀 Tenant access token、OSS Bucket 权限角色 | 语雀 [Token](../concepts/token.md) 需通过[语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取；OSS 连接需确保当前账号对 Bucket 具备 `oss:GetObject` 权限并开通向量检索服务 |

## 使用方式

1. **创建连接器**：进入 [数据连接控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list)，单击“创建连接器”，按类型选择并填写配置；
2. **配置存储/网络**：
   - 文件/表格连接器：选择“平台存储”或授权自有 OSS；
   - 流处理连接器（MySQL/PostgreSQL/PolarDB-X）：选择“创建自定义数据源”或“从DMS导入数据源”，并指定网络类型（公网/私网）；
3. **验证连通性**：
   - MySQL 使用 EventBridge 检测；
   - PostgreSQL 使用 DTS 检测；
   - PolarDB-X 与 OSS 均支持控制台“开始检测”按钮；
4. **导入数据**：
   - 文件连接器：在详情页选择类目 → “导入数据” → 本地上传 → 选择解析方式（推荐“大模型文档解析”以支持图表理解）；
   - 表格连接器：在详情页新建数据表 → 上传 Excel 或自定义表头（注意：表结构一旦创建不可修改）；
5. **在应用中调用**：在智能体或 API 调用中，通过 `searchFile`、`searchTable`、`executeSQL`（仅 DMS 方式）等工具触发对应连接器能力。

## 限制和注意事项

- **容量与时效**：
  - 文件连接器仅支持查看最近 **90 天内导入的文件**，超期后不可见（但数据未删除）；
  - 平台存储免费额度用尽后，表格连接器自动转为按量付费，文件连接器暂无明确计费说明（参见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) “存储位置”说明）；
- **格式与兼容性**：
  - 不支持归档、冷归档、深度冷归档类型的 OSS Bucket；
  - 表格导入不支持 JSON、CSV、YAML，须转为 XLSX/XLS；
  - 语雀连接器**仅支持公网版本语雀**，不支持企业私有部署版；
- **权限与安全**：
  - 所有自有 OSS Bucket 必须添加 `bailian-connector-access` 标签（值 `ReadAndWrite`）或 `bailian-datahub-access`（OSS 连接器专用，值 `read`）；
  - PostgreSQL 要求 `wal_level = logical`，且自建实例需额外配置 `pg_hba.conf` 允许 `100.64.0.0/16` 网段访问；
- **功能边界**：
  - 仅 DMS 导入方式支持 SQL 执行，自定义数据源方式创建的 MySQL/PostgreSQL/PolarDB-X 连接器**无法执行 SQL**；
  - PolarDB-X 连接器**不支持公网访问**，且仅限阿里云 PolarDB-X 2.0 实例（不支持自建或旧版 PolarDB-X）。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


