# more

`more` 是百炼平台中一组面向高级用例与底层能力的扩展功能集合，涵盖服务权限治理（如服务关联角色）、安全凭证管理（如临时 API Key）以及知识库精细化检索（如 SearchFilters）。这些功能不直接参与模型推理主链路，但对生产环境的安全性、可观测性与数据精准性至关重要。开发者需按需启用并严格遵循最小权限原则。

## 支持的模型/功能

`more` 不对应具体模型，而是提供三类关键支撑能力：

- **服务关联角色（SLR）**：为百炼子系统（如工作流、数据管理、安全存储空间等）自动申请访问其他云服务（FC、OSS、ADB-PG、MNS、SLS 等）所需的最小化权限。例如 `AliyunServiceRoleForSFMAccessFC` 用于函数计算节点调用，`AliyunServiceRoleForSFMAccessADB` 用于知识库向量检索对接 ADB-PG [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：用于在不可信前端环境（如浏览器、App）中安全调用百炼 API，避免永久密钥泄露。其权限继承自生成它的主 API Key [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级后过滤（如 `{"姓名": "张三"}`），显著提升结构化数据场景下的召回精度 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMTelemetry` 的权限策略示例被截断（末尾缺失 `}` 和完整 `xtrace` 权限列表），实际部署应以控制台或最新 OpenAPI 返回的完整策略为准；该问题已在 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 中体现。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|------|--------|------|------|------|-----------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | 指定临时 [Token](../concepts/token.md) 有效期（TTL） | `[1, 1800]` 秒，默认 `60` |
| SearchFilters | `searchFilters` | array of object | 否 | 过滤条件数组，每个元素为一个子分组（AND 语义） | 子分组内支持单值、多值、范围（`gte`/`lte`）、模糊（`like`）、标签（`tags`）查询 |

## 使用方式

- **服务关联角色**：首次启用对应功能（如发布含 FC 节点的工作流）时，系统自动创建 SLR；无需手动调用 API。角色名称与策略已预置，详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：通过 `POST https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800` 请求生成，需在 Header 中携带 `Authorization: Bearer <主APIKey>`。响应返回 `token`（如 `st-****`）和 `expires_at`（UNIX 时间戳）[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **SearchFilters**：在 `RetrieveRequest` 请求体中直接嵌入 `searchFilters` 字段，格式为 JSON 数组。例如：`{"searchFilters": [{"姓名": "张三"}, {"岗位": "技术员"}]}`。需确保知识库字段类型与查询语法匹配（如 `age` 字段为 `double` 才支持 `{"age": {"gte": 20, "lte": 30}}`）[知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **SLR 删除风险高**：删除任一 SLR（如 `AliyunServiceRoleForSFMAccessFC`）将导致依赖该角色的功能完全失效（如工作流无法调用 FC），且必须先清理所有关联资源（如删除函数计算节点、断开 OSS/ADB 连接）才能删除 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 不可撤销**：一旦生成，只能等待自然过期（最长 30 分钟），无法主动吊销。务必严格控制 `expire_in_seconds` 值，并仅在必要场景使用。
- **SearchFilters 依赖知识库配置**：仅当知识库索引中已包含对应字段（如 `姓名`、`年龄`），且字段类型正确（string/double/long）时，过滤才生效；未索引字段或类型不匹配将静默忽略该条件。
- **地域隔离**：临时 API Key 的 Endpoint 与主 API Key 所属地域强绑定（北京/新加坡/弗吉尼亚），跨地域调用会失败 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


