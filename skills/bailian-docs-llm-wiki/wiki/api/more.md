# more

`more` 是百炼平台中一组面向高级用例与扩展能力的辅助功能集合，涵盖服务权限管理、安全鉴权机制和知识库精准检索等核心能力。它不直接提供模型推理接口，而是为工作流编排、数据接入、监控观测及RAG应用构建提供底层支撑。开发者需结合具体场景按需启用，并严格遵循权限最小化原则。

## 支持的模型/功能

`more` 本身不对应独立模型，而是支撑以下关键功能模块：

- **服务关联角色（SLR）**：为百炼各子系统（如工作流、数据管理、安全存储、知识库、模型监控等）自动创建并托管对其他云服务的访问权限，包括 FC、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、内容安全、DTS 和 CPFS 等 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 生成**：用于在不可信前端环境（如浏览器、App）中安全调用后端模型服务，避免永久密钥泄露。
- **知识库 `searchFilters` 检索过滤**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级精确筛选，显著提升 RAG 输出相关性 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档中提及的 `AliyunServiceRoleForSFMAccessFC` 权限仅包含 `fc:ListFunctions` 和 `fc:InvokeFunction`，但实际工作流调用函数计算可能还需 `fc:GetFunction` 等元信息权限；建议以控制台实际授予策略为准，而非仅依赖文档示例策略 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | TTL（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| `searchFilters` | `searchFilters` | array of object | 否 | 检索过滤规则数组，每个对象为一个 AND 子分组，支持单值、多值、范围、模糊、标签查询 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| `searchFilters`（范围查询） | `gte`, `lte`, `gt`, `lt`, `eq`, `neq` | number/string | 否 | 字段比较操作符，需嵌套在字段值中（JSON string 化） | `{"年龄": "{\"gte\":20,\"lte\":30}\"}` |

## 使用方式

- **服务关联角色**：首次启用对应功能（如添加函数计算节点、配置 OSS 数据源）时由系统自动创建，无需手动部署；角色名称与策略已预定义，不可修改 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：通过 `POST /api/v1/tokens` 接口调用，需在 `Authorization: Bearer <permanent_api_key>` 中携带永久密钥，并可选传 `expire_in_seconds` 查询参数。
- **`searchFilters`**：作为 `RetrieveRequest` 的字段直接传入，需确保知识库字段已正确映射为可检索属性（如 `姓名`、`年龄` 字段类型需与查询方式匹配），且子账号已获 `AliyunBailianDataFullAccess` 权限及业务空间加入授权 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **SLR 删除风险高**：删除任一服务关联角色将导致其关联功能完全失效（如删 `AliyunServiceRoleForSFMAccessFC` 后无法调用 FC 节点），且必须先清理所有依赖资源（如发布态工作流、OSS 导入任务、ADB 连接等）才能删除。
- **临时 API Key 不可撤销**：生命周期固定，到期自动失效，不支持主动吊销或提前回收；应严格控制 TTL 时长，避免过度宽松。
- **`searchFilters` 语法约束**：
  - 子分组间为强制 `AND` 逻辑，不可配置 `OR`；
  - 多值查询需使用 `json.dumps(["val1","val2"])` 格式传递字符串；
  - 模糊查询 `like` 值中 `%` 为通配符，`_` 不被支持；
  - 标签（`tags`）查询中多个标签在同一数组内为 `OR` 关系，跨子分组为 `AND` 关系。
- **地域隔离**：临时 API Key 的 Endpoint 与永久 API Key 所属地域强绑定（北京/新加坡/弗吉尼亚），跨地域调用将失败 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


