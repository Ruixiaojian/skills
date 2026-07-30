# more

`more` 是百炼平台为高级功能和扩展能力提供的统一入口，涵盖服务权限管理（如服务关联角色）、[知识库](../concepts/knowledge-base.md)检索增强（如 `SearchFilters`）以及安全认证机制（如临时 API Key）。这些能力面向需要精细化控制、结构化数据过滤或客户端安全调用的开发者场景，不直接参与模型推理主流程，但对生产级应用构建至关重要。

## 支持的模型/功能

`more` 不对应具体模型，而是支撑以下核心功能模块：
- **服务关联角色（SLR）**：为百炼子系统（如工作流、[知识库](../concepts/knowledge-base.md)、安全存储、用量监控等）自动申请并托管对其他云服务（FC、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、内容安全、DTS、CPFS）的最小必要访问权限 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)；
- **[知识库](../concepts/knowledge-base.md)检索过滤（SearchFilters）**：在 `Retrieve` 接口请求中传入结构化过滤条件，支持单值、多值、范围、模糊及标签查询，显著提升语义检索结果的相关性 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)；
- **临时 API Key 生成**：通过后端服务调用 `/api/v1/tokens` 接口，基于永久 API Key 签发短期有效的凭证，适用于浏览器或移动端等不可信环境 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

> **注意**：文档 1 中列出的 `AliyunServiceRoleForSFMAccessFC` 权限仅包含 `fc:ListFunctions` 和 `fc:InvokeFunction`，但实际工作流调用 FC 可能还需 `fc:GetFunction` 等元信息权限；建议以 RAM 控制台中该角色绑定的最新系统策略为准，而非仅依赖文档示例。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | TTL（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters | `searchFilters` | array of object | 否 | 检索过滤条件数组，每个对象为一个 AND 分组，支持 `eq`/`neq`/`gt`/`gte`/`lt`/`lte`/`like` 等操作符 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（范围查询） | 字段值 | string (JSON) | — | 范围查询需序列化为 JSON 字符串，如 `{"gte": 20, "lte": 27}` | `{"age": "{\"gte\": 20, \"lte\": 27}\"}` |

## 使用方式

- **服务关联角色**：无需手动创建。当首次启用对应功能（如在工作流中添加函数计算节点、在安全存储空间中绑定 OSS Bucket）时，百炼自动创建所需 SLR。开发者只需确保主账号具备 `AliyunRAMFullAccess` 或等效权限以允许 SLR 创建 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)；
- **SearchFilters**：在 `RetrieveRequest` 请求体中直接嵌入 `searchFilters` 字段，字段名需与知识库建模时定义的列名完全一致（区分大小写），且目标字段必须已配置为可检索字段 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)；
- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <PERMANENT_API_KEY>` 的 POST 请求，地域 Endpoint 需与永久 API Key 所属地域一致（北京、新加坡或弗吉尼亚） [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

## 限制和注意事项

- **服务关联角色删除风险高**：删除任一 SLR（如 `AliyunServiceRoleForSFMAccessFC`）将导致对应功能完全不可用（如工作流无法调用 FC），且删除前必须先清理所有依赖资源（如已发布的应用、OSS 连接、ADB-PG 连接等） [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)；
- **SearchFilters 语法约束严格**：子分组间为强制 AND 逻辑，不支持 OR 或 NOT；多值查询需使用 `json.dumps(["val1","val2"])` 序列化；模糊查询 `like` 值中 `%` 为通配符，`_` 不被支持；标签查询中同一分组内多个 tag 为 OR 关系，不同分组间仍为 AND [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)；
- **临时 API Key 不可撤销**：一旦签发，只能等待其自然过期（最长 30 分钟），无法主动吊销。因此 `expire_in_seconds` 应按实际业务会话时长谨慎设置，避免过度宽松；
- **权限继承原则**：临时 API Key 继承签发者（永久 API Key）的全部权限，包括模型访问白名单、知识库读写范围等，**不会缩小原始权限** [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)


