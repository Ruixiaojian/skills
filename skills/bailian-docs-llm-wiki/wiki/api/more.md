# more

`more` 是百炼平台为高级功能和扩展能力提供的统一入口，涵盖服务权限管理、安全认证机制与知识库精准检索等关键能力。开发者可通过服务关联角色（SLR）授权百炼访问外部云资源；使用临时 API Key 实现前端安全调用；并通过 `searchFilters` 对知识库语义检索结果进行结构化过滤。所有能力均需配合对应业务场景的权限配置与参数设置。

## 支持的模型/功能

`more` 不直接对应某类模型，而是支撑以下三类核心功能：

- **服务关联角色（SLR）**：用于百炼各子模块访问外部云服务，如函数计算（FC）、OSS、ADB-PG、MNS、OpenTelemetry 等。例如，工作流应用调用 FC 函数需 `AliyunServiceRoleForSFMAccessFC`，安全存储空间接入 OSS 需 `AliyunServiceRoleForAccessOSS` [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 生成**：面向不可信客户端（如浏览器、App）的安全鉴权方案，通过后端调用 `/api/v1/tokens` 接口签发短期有效凭证。
- **知识库检索过滤（SearchFilters）**：在 `Retrieve` 接口请求中传入结构化过滤条件，支持单值、多值、范围、模糊及标签查询，显著提升 RAG 场景下结果相关性 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档中提及的 `AliyunServiceRoleForSFMTelemetry` 权限策略在原文末尾被截断（缺少 `xtrace` 权限的完整 JSON），实际部署时请以控制台或最新 SDK 返回的策略为准；该问题已在 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 中明确标注。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | TTL（秒），取值范围 `[1, 1800]`，默认 `60` | `?expire_in_seconds=1800` |
| SearchFilters | `searchFilters` | array of object | 否 | 检索过滤子分组数组，子分组间为 AND 逻辑 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（范围查询） | `gte` / `lte` / `gt` / `lt` / `eq` / `neq` | number/string | 否 | 字段比较操作符，仅数值字段支持区间，字符串支持等值 | `{"年龄": {"gte": 20, "lte": 27}}` |
| SearchFilters（模糊查询） | `like` | string | 否 | 字符串字段支持 `%` 通配符（如 `"技%员"`） | `{"岗位": {"like": "技%员"}}` |

## 使用方式

- **服务关联角色**：首次启用对应功能（如创建函数计算节点、导入 OSS 数据）时，系统自动创建 SLR；无需手动创建，但需确保 RAM 权限允许 `ram:CreateServiceLinkedRole`。角色详情与删除指引见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：后端服务使用永久 API Key（`DASHSCOPE_API_KEY`）向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起 POST 请求，响应返回 `token` 与 `expires_at`（UNIX 时间戳）。**不可手动删除**，到期自动失效 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **SearchFilters**：在 `RetrieveRequest` 请求体中直接嵌入 `searchFilters` 字段，支持嵌套多组条件。需确保知识库字段已正确映射为可检索类型（如 `string`、`double`），且子账号已授予 `AliyunBailianDataFullAccess` 策略 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **SLR 删除风险**：删除任一 SLR 将导致其关联功能完全不可用（如删除 `AliyunServiceRoleForSFMAccessFC` 后，工作流无法调用 FC 节点），且删除前必须清理依赖资源（如已发布的流程、OSS 连接等）。
- **临时 API Key 权限继承**：生成的临时 token 完全继承源 API Key 的权限范围（含模型访问、知识库读写等），**不得在前端硬编码或持久化存储**。
- **SearchFilters 兼容性**：仅对「数据查询」型知识库生效；「文档搜索」「音视频搜索」类知识库仅支持 `tags` 字段的标签查询；多值查询需使用 `json.dumps` 序列化数组（如 Python SDK 示例所示）。
- **地域隔离**：临时 API Key 的 Endpoint 与 API Key 所属地域强绑定（北京/新加坡/弗吉尼亚），跨地域调用将返回 `InvalidApiKey` 错误 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


