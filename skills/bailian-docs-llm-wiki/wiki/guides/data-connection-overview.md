# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的数据接入入口。通过创建不同类型的连接器，开发者可将企业自有数据库、文档系统、对象存储等数据源接入百炼，支撑对话式应用实时检索与引用结构化/非结构化数据。所有连接器均支持在智能体（Agent）或 API 调用中作为知识源使用，无需自行维护数据同步逻辑。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：**平台托管型**（文件、表格）和**流处理型**（MySQL、PostgreSQL、PolarDB-X 2.0、语雀、OSS）。  
- **平台托管型**：数据导入百炼平台或自有 OSS 后，经解析生成向量索引，供 RAG 场景调用（如 `searchFile`、`searchTable` 工具）；支持文档智能解析、大模型文档解析（含图表理解）、音视频多模态解析等 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。  
- **流处理型**：数据保留在原系统，运行时直连查询；其中 MySQL、PostgreSQL、PolarDB-X 2.0 连接器**仅当通过 DMS 导入数据源方式创建时**才支持执行 SQL 查询（即 `executeSQL` 工具），自定义数据源方式创建的实例不支持该能力 —— 此限制在 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中有明确说明。  
- **语雀与 OSS 连接器**：分别对接语雀知识库（需公网 [Token](../concepts/token.md)）和 OSS Bucket（需开通向量检索服务并打标 `bailian-datahub-access:read`），用于实时拉取文档元信息及内容片段。

> **注意**：原始文档中对 OSS Bucket 标签值的描述存在不一致：文件/表格连接器要求标签为 `bailian-connector-access:ReadAndWrite`，而 OSS 连接器明确要求 `bailian-datahub-access:read`。实际配置请以 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中“OSS连接器”章节为准，避免权限拒绝。

## 关键参数

| 参数类别         | 必填项                                                                 | 说明                                                                 |
|------------------|------------------------------------------------------------------------|----------------------------------------------------------------------|
| **通用**         | 连接器名称、描述                                                       | 描述建议明确数据内容与用途，直接影响智能体检索准确率                 |
| **文件/表格**    | 存储位置（平台存储 or 自有 OSS）                                       | 平台存储免费额度：文件连接器限 200,000 文件/1 TB；表格连接器限 1 TB |
| **MySQL/PG/PX**  | 数据库地址、端口、用户名、密码、dbName（PG/PX 必填）、网络类型（公网/私网） | 公网需加白名单；私网需指定地域；PG 需 `wal_level=logical`            |
| **语雀**         | Tenant access token                                                    | 仅支持公网语雀，[Token](../concepts/token.md) 需从 [语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取 |
| **OSS**          | Bucket 名称、`bailian-datahub-access:read` 标签                         | 不支持归档/冷归档存储类型；开启 Referer 防盗链需放行 `*.console.aliyun.com` |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击「创建连接器」→ 选择类型 → 填写参数 → 完成授权与连通性检测。  
2. **导入数据（仅平台托管型）**：  
   - 文件连接器：在详情页选择类目 → 「导入数据」→ 本地上传 PDF/Word/Excel 等 → 选择解析方式（推荐「大模型文档解析」以支持图表理解）→ 配置标签（可选，用于 API 调用时过滤）。  
   - 表格连接器：在详情页新建数据表 → 上传 CSV/Excel 或自定义表头（列名、类型、描述必填；`image_url` 类型需确保 URL 公开可访问）→ 提交导入。  
3. **调用连接器**：在智能体工具配置或 API 请求中，通过预置工具（如 `searchFile`、`executeSQL`、`searchOSSFile`）传入连接器 ID 及查询参数即可触发数据访问。

## 限制和注意事项

- **容量与时效**：平台托管文件仅保留最近 90 天的导入记录（不可查看但未删除）；文件解析在高并发时可能超时，建议错峰操作。  
- **网络与权限**：  
  - MySQL/PostgreSQL 公网连接需将百炼服务 IP 段加入数据库白名单；  
  - PolarDB-X 2.0 **仅支持私网**，且必须与百炼所在地域一致；  
  - 所有自有 OSS Bucket 必须添加对应标签（`bailian-connector-access` 或 `bailian-datahub-access`），否则授权失败。  
- **功能边界**：  
  - 文件连接器不支持直接导入 JSON/YAML，需转为 XLSX/XLS；  
  - 表格连接器一旦建表，结构（列名、类型）不可修改；  
  - OSS 连接器若未开通向量检索服务，则 `searchOSSFile` 和 `searchOSSFileByFileName` 工具不可用 —— 该依赖关系详见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


