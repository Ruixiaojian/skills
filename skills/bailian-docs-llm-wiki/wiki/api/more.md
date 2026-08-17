# more

`more` 是百炼平台中一组面向高级用例与安全治理的扩展能力集合，涵盖服务权限委托（服务关联角色）、临时凭证分发（临时 API Key）和语义检索增强（SearchFilters）。这些功能不直接参与模型推理，但对工作流编排、多租户隔离、数据安全与检索精度至关重要，适用于需要精细化权限控制、前端直连调用或结构化知识过滤的开发者场景。

## 支持的模型/功能

`more` 不对应具体模型，而是提供三类基础设施级能力：

- **服务关联角色（SLR）**：为百炼子系统（如工作流、数据管理、安全存储空间等）自动申请并托管对其他云服务（FC、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、内容安全、DTS、CPFS）的最小权限访问。详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：基于永久 API Key 签发的短期有效凭证，用于在不可信客户端（如浏览器、App）中安全调用模型服务，避免长期密钥泄露风险。
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，支持单值、多值、范围、模糊及标签查询，显著提升 RAG 场景下语义检索结果的相关性与准确性。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例值 |
|------|--------|------|------|------|--------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | 有效期（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters | `searchFilters` | array of object | 否 | 过滤条件数组，每个元素为一个 key-value 对象；子分组间为 AND 逻辑 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |

> **注意**：文档 3 中 Python 示例代码使用 `json.dumps()` 序列化 `searchFilters` 字段值（如 `{"年龄": json.dumps(age_range.to_dict())}`），但实际 API 要求该字段为原生 JSON 对象（非字符串）。SDK 层应自动序列化，**开发者不应手动调用 `json.dumps()`**，否则将导致 `400 Bad Request`。此为文档示例错误，以 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 的接口定义为准。

## 使用方式

- **服务关联角色**：无需主动创建。当您首次启用依赖外部服务的功能（如在工作流中添加函数计算节点、在安全存储空间中绑定 OSS 或 ADB-PG）时，百炼会自动为您创建对应 SLR。角色名称与策略已预置，权限严格限定于对应功能所需最小集。
- **临时 API Key**：通过 `POST /api/v1/tokens` 接口调用，需在 `Authorization: Bearer <permanent_api_key>` 头中携带您的永久 API Key，并可选传入 `expire_in_seconds` 查询参数。响应返回 `token`（临时密钥）与 `expires_at`（UNIX 时间戳）。
- **SearchFilters**：在调用知识库 `Retrieve` 接口时，于请求体中添加 `searchFilters` 字段。支持嵌套结构（如 `{"年龄": {"gte": 20, "lte": 27}}`）和复合条件（多个子分组），详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **SLR 删除风险高**：删除任一服务关联角色（如 `AliyunServiceRoleForSFMAccessFC`）将导致对应功能完全失效（如工作流无法调用 FC 函数）。删除前必须先解除所有业务依赖（如删除函数计算节点、断开 OSS/ADB-PG 连接、停止数据导入任务），否则操作将被拒绝或引发运行时错误。
- **临时 API Key 不可撤销**：其生命周期由 `expire_in_seconds` 决定，到期自动失效，**不支持手动删除或提前吊销**。请严格控制 TTL 时长，避免在长连接场景中设置过长有效期。
- **SearchFilters 兼容性要求**：仅对「数据查询」类型知识库生效；字段类型（string/long/double）必须与知识库索引配置一致，否则过滤无效；多值查询需确保字段值为纯数组（如 `["张三","李四"]`），而非字符串形式的 JSON 数组。
- **地域隔离**：临时 API Key 的 Endpoint 与永久 API Key 所属地域强绑定（北京、新加坡、弗吉尼亚），跨地域调用将返回 `InvalidApiKey` 错误。请确保请求 URL 与密钥创建地域一致。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


