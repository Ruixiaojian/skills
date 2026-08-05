# data connection overview

[数据连接](../concepts/data-connection.md)是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的数据接入入口。通过创建不同类型的连接器，开发者可将非结构化文档、结构化表格或实时数据库等数据源接入百炼，支撑知识检索、SQL查询、多模态解析等下游能力。所有连接器均遵循最小权限原则，支持平台托管与自有存储双模式。

## 支持的模型/功能

[数据连接](../concepts/data-connection.md)器按数据访问模式分为**平台托管**（文件、表格）和**流处理**（MySQL、PostgreSQL、PolarDB-X 2.0、语雀、OSS）两类，对应不同数据形态与使用场景：

- **平台托管类**：适用于静态内容管理。  
  - `文件`：支持 PDF、Word、Markdown 等非结构化文档，提供电子文档解析、文档智能解析、大模型文档解析（含 Qwen-VL）、音视频解析等多种解析方式，详见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中“导入文件”章节。  
  - `表格`：支持 CSV、Excel 等结构化数据，支持自定义表头与字段类型（如 `image_url`），但表结构一旦创建不可修改。

- **流处理类**：适用于实时数据访问。  
  - `MySQL` / `PostgreSQL` / `PolarDB-X 2.0`：仅通过 **DMS 导入数据源** 方式创建的连接器支持执行 SQL 查询；自定义方式创建的连接器仅支持元数据同步，不支持运行时 SQL 执行。该限制在 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 的各数据库小节中多次强调。  
  - `语雀`：仅支持公网版语雀，需提供 Tenant access token。  
  - `OSS`：支持私有 Bucket 和内容加密 Bucket，但需开通向量检索服务才能使用 `searchOSSFile` 和 `searchOSSFileByFileName` 工具——此前提条件明确记载于 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 的 OSS 小节末尾。

> **注意**：原始文档中“文件连接器”说明称“文件将作为独立副本存储在平台提供的免费空间中，当前无容量限制”，但同一文档“前置条件”部分明确指出平台存储额度为“1 TB 存储额度”。二者存在矛盾，以实际控制台配额提示及计费策略为准，建议通过配额管理页面确认可用额度。

## 关键参数

| 连接器类型 | 必填参数 | 特殊要求 | 检测机制 |
|------------|----------|----------|----------|
| 文件 / 表格 | 连接器名称、描述、存储位置（平台/OSS） | OSS Bucket 需添加 `bailian-connector-access` 标签（值 `ReadAndWrite`） | 无主动连通性检测，依赖上传/导入结果反馈 |
| MySQL | 数据库地址、端口、用户名、密码；若为 RDS 则需实例 ID | 公网需加白名单；`wal_level` 无要求；仅 DMS 方式支持 SQL | EventBridge 连通性检测 |
| PostgreSQL | 主机地址、端口、dbName、用户名、密码 | `wal_level=logical`；自建实例需配置 `listen_addresses` 允许 `100.64.0.0/16` | DTS 连通性检测 |
| PolarDB-X 2.0 | 数据库地址、端口、用户名、密码；仅支持私网 | 必须完成 DTS + PolarDB-X SLR 授权；仅支持阿里云实例 | EventBridge 检测（同 MySQL） |
| 语雀 | Tenant access token | 仅公网语雀；[Token](../concepts/token.md) 需具备知识库读取权限 | [Token](../concepts/token.md) 校验接口调用 |
| OSS | Bucket 名称 | Bucket 需添加 `bailian-datahub-access` 标签（值 `read`）；必须开通向量检索服务 | 授权后自动校验 Bucket 权限 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击“创建连接器” → 选择类型 → 填写基本信息与连接参数 → （可选）点击“开始检测”或“连接检测”验证 → 单击“确认”。  
2. **导入数据**（仅平台托管类）：  
   - 文件：进入连接器详情页 → 选择类目 → “导入数据” → 本地上传 → 选择解析方式（推荐默认设置，复杂图表需选“大模型文档解析”）→ 配置标签（可选）→ 确认。  
   - 表格：进入连接器详情页 → “数据表管理” → 新建数据表 → 选择“直接上传Excel”或“自定义表头” → 上传文件 → 确认。  
3. **在应用中调用**：连接器创建并导入/配置完成后，可在智能体（Agent 1.0）或 API 调用中通过 `knowledge_retrieval` 或 `sql_query` 工具引用，具体工具名与参数格式请参考对应模型的 SDK 文档。

## 限制和注意事项

- **类目与数据表上限**：每个业务空间最多 500 个类目（文件）、无限数据表（表格），但单次导入文件数受并发与资源限制，高峰时段可能延迟数小时。  
- **文件生命周期**：仅支持查看最近 **90 天内**导入的文件，超期后不可见（但数据未删除）。  
- **存储类型限制**：OSS 连接器**不支持归档、冷归档、深度冷归档**存储类型的 Bucket。  
- **Referer 防盗链**：若 OSS Bucket 开启 Referer 防盗链，必须将 `*.console.aliyun.com` 加入白名单。  
- **权限依赖**：所有连接器均需主账号或已授权 RAM 用户操作；首次使用 OSS、DMS、PolarDB-X 等服务时，需完成对应 SLR 角色授权（如 `AliyunServiceRoleForSFMConnectorAccessDTS`）。  
- **模型兼容性**：大模型文档解析与 Qwen-VL 解析需搭配支持多模态的模型（如 Qwen-VL、Qwen2-VL），普通文本模型无法调用图像理解能力。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


