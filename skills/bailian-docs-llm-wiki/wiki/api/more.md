# more

`more` 是百炼平台面向开发者提供的扩展能力集合，涵盖服务权限管理、安全认证机制与高级检索控制三大方向。它不直接提供模型推理能力，而是支撑工作流编排、知识库精准检索、跨云服务集成等关键场景的底层基础设施。开发者需结合具体业务需求，按需启用对应功能模块，并严格遵循权限最小化原则配置服务关联角色与临时凭证。

## 支持的模型/功能

`more` 本身**不提供独立模型**，而是为以下核心功能提供支撑能力：

- **服务集成能力**：通过预置的服务关联角色（SLR），实现百炼与函数计算（FC）、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、内容安全、DTS、CPFS 等阿里云服务的安全对接。例如，`AliyunServiceRoleForSFMAccessFC` 支持工作流中调用 FC 函数，`AliyunServiceRoleForSFMAccessADB` 支持知识库向 ADB-PG 写入向量数据 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **安全访问控制**：提供生成临时 API Key 的能力，用于在不可信前端环境（如浏览器、App）中安全调用百炼 API，避免永久密钥泄露 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **知识库高级检索**：支持在 `Retrieve` 接口请求中传入 `searchFilters`，对语义检索结果进行结构化字段过滤（如单值、多值、范围、模糊、标签查询），显著提升 RAG 场景下结果的相关性 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中列出的 `AliyunServiceRoleForSFMTelemetry` 权限策略在末尾被截断（`"xtrace:Read*","xtrace:Get*"` 后无闭合），实际策略应以控制台或最新 SDK 返回为准；该问题已在 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 中体现，使用前请务必验证策略完整性。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | TTL（秒），取值范围 `[1, 1800]`，默认 `60` | `?expire_in_seconds=300` |
| 知识库检索 | `searchFilters` | array of object | 否 | 过滤条件数组，每个元素为一个子分组（AND 语义），支持 `{"字段": "值"}` 或 `{"字段": {"eq": "值"}}` 等结构 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| 知识库检索 | 字段操作符 | string | 否 | 在 `searchFilters` 子分组内使用，如 `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `like` | `{"年龄": {"gte": 25, "lt": 35}}` |

## 使用方式

### 1. 服务关联角色（SLR）
- **自动创建**：首次在控制台启用对应功能（如添加 FC 节点、配置 OSS 数据源）时，系统自动创建所需 SLR。
- **手动管理**：可在 RAM 控制台 > 角色管理 > 服务关联角色中查看、删除（删除前须按文档要求清理依赖资源）。
- **权限验证**：各 SLR 绑定的系统策略（如 `AliyunServiceRolePolicyForSFMAccessFC`）已明确限定最小必要权限，禁止手动修改策略内容。

### 2. 临时 API Key
- **调用方式**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起 `POST` 请求，`Authorization` 头携带主账号或子账号的永久 API Key。
- **地域隔离**：北京、新加坡、弗吉尼亚地域的 Endpoint 和 API Key **不互通**，需按实际部署地域选择对应 Endpoint [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

### 3. SearchFilters
- **请求位置**：作为 `RetrieveRequest` 的字段，与 `query`、`indexId` 同级传入。
- **语法约束**：
  - 子分组间为 AND 关系，不可更改；
  - 单值查询直接写 `{"字段": "值"}`；
  - 范围/模糊查询需嵌套对象：`{"字段": {"gte": 20, "lte": 30}}` 或 `{"字段": {"like": "技%员"}}`；
  - 多值查询需 `json.dumps(["值1", "值2"])`（Python）或等效序列化。

## 限制和注意事项

- **SLR 删除风险**：删除任一 SLR（如 `AliyunServiceRoleForAccessOSS`）将导致对应功能（安全存储空间访问 OSS）**立即失效**，且无法回滚。删除前必须按 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 文档要求完成前置清理（如断开连接、删除任务）。
- **临时 API Key 不可撤销**：其生命周期由 `expire_in_seconds` 决定，到期自动失效，**不支持主动吊销或提前删除** [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **SearchFilters 兼容性**：仅对「数据查询」类型的知识库生效；「文档搜索」「音视频搜索」类知识库仅支持 `tags` 字段的标签查询 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。
- **权限继承警告**：临时 API Key **完全继承**其签发者的全部权限（含模型访问、知识库读写、业务空间操作等），切勿用高权限主账号 Key 签发前端可用 [Token](../concepts/token.md)。
- **字段类型校验**：`searchFilters` 中字段值类型必须与知识库索引时定义的类型一致（如 `年龄` 字段为 `double`，则 `{"年龄": "25"}`（字符串）将被忽略），类型不匹配会导致过滤失效。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


