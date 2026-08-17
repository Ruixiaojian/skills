# more

`more` 是百炼平台中一组面向高级用例与安全治理的扩展能力集合，涵盖服务关联角色（SLR）管理、临时 API Key 生成、知识库检索过滤（SearchFilters）等核心功能。这些能力不直接参与模型推理调用，但对权限隔离、客户端安全接入、结构化数据精准召回等关键场景起决定性作用。开发者需按需启用并严格遵循最小权限原则。

## 支持的模型/功能

- **服务关联角色（SLR）**：百炼通过预定义 SLR 自动获取对 FC、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、内容安全、DTS、CPFS 等云服务的受控访问权限，支撑工作流编排、数据导入、安全存储、模型监控、用量分析等模块运行。详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：用于在不可信前端环境（如浏览器、移动 App）中安全调用模型服务，避免永久密钥泄露。其权限继承自签发用的永久 API Key，并支持 TTL 自定义（1–1800 秒）。
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级后置过滤，显著提升结构化数据（如员工表、产品目录）的召回精度。该能力仅适用于已配置为“数据查询”类型的知识库。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | integer | 否（默认 60） | 临时 [Token](../concepts/token.md) 有效期，单位秒，取值范围 `[1, 1800]` | `1800` |
| SearchFilters | `searchFilters` | array of object | 否 | 过滤条件数组，每个元素为一个子分组（AND 语义），支持单值、多值、范围、模糊、标签查询 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（范围查询） | `gte`, `lte`, `gt`, `lt`, `eq`, `neq` | number/string | 否 | 字段比较操作符，需嵌套在字段值中（JSON 字符串化） | `{"年龄": "{\"gte\":20,\"lte\":27}\"}` |

> **注意**：文档 3 中 `multi_query` 示例使用 `json.dumps(names)` 构造多值，而 `range_query` 和 `wildcard_query` 同样要求将结构体 `json.dumps()` 后作为字符串传入字段值；但文档未明确说明所有复杂查询均需此序列化步骤，实际调用时若未序列化将导致过滤失效。请以 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 中的完整代码示例为准。

## 使用方式

- **服务关联角色**：首次启用对应功能（如添加函数计算节点、配置 OSS 数据源）时，系统自动创建 SLR；无需手动调用 API。角色策略已固化，禁止修改。
- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <permanent_key>` 的 POST 请求，可选附加 `?expire_in_seconds=N`。响应返回 `token`（前缀 `st-`）与 `expires_at`（UNIX 时间戳）。
- **SearchFilters**：在 `RetrieveRequest` 请求体中设置 `searchFilters` 字段，格式为 JSON 数组。每个子分组内支持混合字段类型查询（如 `{"姓名": "张三", "性别": "男"}`），子分组间为 AND 关系。务必确保知识库字段类型与查询语法匹配（如数值字段不可用 `like`）。

## 限制和注意事项

- **SLR 删除风险高**：删除任一 SLR（如 `AliyunServiceRoleForSFMAccessFC`）将导致依赖该角色的功能完全不可用（如工作流无法调用 FC），且删除前必须清空所有关联资源（如已发布的应用、OSS 导入任务、ADB 连接）。详情见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 不可撤销**：生命周期固定，到期自动失效，**不支持手动删除或提前吊销**。应严格控制 `expire_in_seconds` 时长，避免过度宽松。
- **SearchFilters 兼容性约束**：仅对“数据查询”类型知识库生效；普通文档类知识库不支持字段过滤。多值、范围、模糊查询必须将条件对象 `json.dumps()` 后作为字符串传入字段值，否则服务端解析失败，等效于无过滤。
- **地域隔离**：临时 API Key 的 Endpoint 与永久 API Key 所属地域强绑定（北京/新加坡/弗吉尼亚），跨地域调用将返回 `InvalidApiKey` 错误。参见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


