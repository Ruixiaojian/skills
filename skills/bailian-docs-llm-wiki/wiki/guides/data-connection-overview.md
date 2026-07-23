# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的实时数据访问入口。它支持结构化与非结构化数据源的接入，并通过向量化索引与流式查询两种机制支撑知识检索与动态 SQL 执行。所有连接器均需在业务空间内创建并绑定权限，其行为受底层服务（如 DMS、DTS、OSS）和网络策略共同约束。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：

- **平台托管型**：适用于静态文件与表格数据，包括  
  - `文件`：支持 PDF、Word、Markdown 等非结构化文档，依赖[文档理解](https://help.aliyun.com/zh/document-mind/product-overview/overview-of-document-understanding#9a4f5fb91fpps)能力进行切分与向量化；  
  - `表格`：支持 CSV、Excel 等结构化数据，自动识别表头或允许自定义 schema，字段类型（如 `image_url`）直接影响向量索引生成逻辑。

- **流处理型**：适用于实时数据库与在线知识库，包括  
  - `MySQL` / `PostgreSQL` / `PolarDB-X 2.0`：仅通过 **从 DMS 导入数据源** 方式创建的连接器支持执行 SQL 查询（详见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)）；  
  - `语雀`：对接公网语雀知识库，依赖个人访问 Token 鉴权；  
  - `OSS`：访问对象存储中的原始文件，需开通[向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/)方可使用 `searchOSSFile` 等工具（参见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)）。

> **注意**：`MySQL` 和 `PostgreSQL` 连接器均明确要求“仅 DMS 导入方式支持 SQL 执行”，但文档中未说明该限制是否适用于所有 API 调用场景；实际开发中应以控制台创建路径为准，避免依赖自定义数据源方式实现查询逻辑 —— 此矛盾点已在 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中多次强调，需严格遵循。

## 关键参数

| 参数 | 说明 | 约束条件 |
|------|------|----------|
| `连接器名称` & `描述` | 必填；描述将参与智能体调用时的意图识别，建议包含数据内容与用途 | 名称需唯一，描述长度 ≤ 500 字符 |
| `存储位置`（文件/表格） | 平台存储（免费额度）或自有 OSS Bucket | OSS Bucket 必须添加 `bailian-connector-access` 标签（值为 `ReadAndWrite`） |
| `数据库地址` / `端口` / `用户名` / `密码`（MySQL/PostgreSQL/PolarDB-X） | 连接凭据；部分字段由 SLR 授权自动填充 | PostgreSQL 必须设置 `wal_level=logical`；PolarDB-X 仅支持私网且需显式授权 `AliyunServiceRoleForSFMAccessPolarDBX` 等角色 |
| `Tenant access token`（语雀） | 公网语雀个人访问 Token | 仅支持语雀开放 API v1，不兼容企业版或私有部署实例 |
| `Bucket 名称`（OSS） | 下拉选择已授权的 OSS Bucket | Bucket 不得为归档/冷归档类型；若启用 Referer 防盗链，须将 `*.console.aliyun.com` 加入白名单 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击 **创建连接器** → 选择类型 → 填写基本信息与连接参数 → （可选）点击 **开始检测** 或 **连接检测** 验证连通性 → 单击 **确认**。
2. **导入数据**：
   - 文件连接器：进入详情页 → 选择类目 → **导入数据** → 本地上传 → 配置解析方式（默认/文档智能/大模型/Qwen VL/音视频）→ 设置标签 → 提交；
   - 表格连接器：进入详情页 → 新建或选择数据表 → 上传 Excel 或自定义表头 → 确保列名与类型严格匹配 → 提交；
   - 流处理连接器：无需导入，直接在应用中调用对应工具（如 `queryMySQL`、`searchYuqueDoc`）。
3. **调用集成**：在智能体或 API 应用中，通过预置工具（如 `searchFile`、`queryPostgreSQL`）传入参数调用，具体参数格式参考各连接器文档。

## 限制和注意事项

- **容量与时效**：平台托管文件仅保留最近 90 天导入记录（不可查看但未删除）；平台存储免费额度为 1 TB（表格）或 200,000 文件 + 1 TB（文件），超限后转为按量计费。
- **网络与权限**：
  - MySQL 公网连接需将百炼服务 IP 段加入 RDS 白名单；
  - PolarDB-X 仅支持私网，且必须与连接器所在地域一致；
  - 所有连接器均需主账号或具备 `AliyunBailianDataConnectorFullAccess` 权限的 RAM 用户操作。
- **功能边界**：
  - 文件连接器不支持直接导入 JSON/CSV/YAML，须先转为 XLSX/XLS；
  - 表格连接器一旦建表，schema（列名、类型、描述）不可修改；
  - OSS 连接器若未开通向量检索服务，则 `searchOSSFile` 和 `searchOSSFileByFileName` 工具不可用（依据 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)）；
  - 语雀连接器仅支持公网版本，不兼容语雀企业版或私有化部署实例。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


