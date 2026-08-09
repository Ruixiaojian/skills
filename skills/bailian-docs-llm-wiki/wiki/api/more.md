# more

`more` 是百炼平台中一组面向高级用例的扩展能力集合，涵盖服务权限管理、安全鉴权机制与知识库精准检索三大方向。它不提供独立模型服务，而是作为核心功能（如工作流编排、知识库检索、监控分析）的支撑组件存在。开发者需结合具体业务场景按需启用，并严格遵循各能力的权限约束与调用规范。

## 支持的模型/功能

`more` 本身不提供模型推理能力，但为以下关键功能提供底层支持：

- **服务关联角色（SLR）**：为百炼与外部云服务（如 FC、OSS、ADB-PG、MNS、OpenTelemetry 等）的安全集成提供最小化权限委托。例如，`AliyunServiceRoleForSFMAccessFC` 使工作流应用能调用函数计算节点；`AliyunServiceRoleForSFMAccessADB` 支持知识库对接 AnalyticDB for PostgreSQL 向量库 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **临时 API Key 生成**：用于在不可信前端环境（如浏览器、App）中安全调用百炼 API，避免永久密钥泄露。该能力继承源 API Key 的全部权限范围，包括模型访问控制与知识库读写限制 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，对语义检索结果进行字段级精确筛选（如 `{"姓名": "张三"}`），显著提升 RAG 场景下结构化数据的召回准确率 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中列出的 `AliyunServiceRoleForSFMTelemetry` 权限策略在末尾被截断（`"xtrace:Read*","xtrace:Get*","xtrace:Describe*"` 后缺失完整 JSON 结构），实际部署时请以控制台或最新 SDK 返回的策略为准，避免因权限缺失导致 OpenTelemetry 数据采集失败。

## 关键参数

| 能力 | 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|------|--------|------|------|------|----------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | 指定 [Token](../concepts/token.md) 有效期（TTL） | `[1, 1800]` 秒，默认 `60` |
| SearchFilters | `searchFilters` | array of object | 否 | 检索过滤条件数组，每个对象为一个 AND 分组 | 最多支持 10 个分组；单个分组内支持单值、多值、范围（`gte`/`lte`）、模糊（`like`）及标签（`tags`）查询 |

## 使用方式

- **服务关联角色**：首次启用对应功能（如创建函数计算节点、配置 OSS 数据导入）时，系统自动创建所需 SLR；无需手动调用 API。角色名称与权限策略已固化，不可修改。详情见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **临时 API Key**：通过 `POST https://dashscope.aliyuncs.com/api/v1/tokens` 接口生成，需在 `Authorization` Header 中携带有效的永久 API Key（`Bearer $DASHSCOPE_API_KEY`）。生成后直接用于后续模型或知识库 API 请求的鉴权。  
- **SearchFilters**：在 `RetrieveRequest` 请求体中以 JSON 数组形式传入，字段名需与知识库索引时定义的元数据字段名完全一致（区分大小写）。示例：`{"searchFilters": [{"岗位": "技术员", "年龄": {"gte": 20, "lte": 30}}]}`。

## 限制和注意事项

- **SLR 删除风险**：删除任一服务关联角色将导致其关联功能完全失效（如删除 `AliyunServiceRoleForSFMAccessFC` 后，所有工作流中的函数计算节点无法调用）。删除前必须先解除依赖（如删除节点、断开 OSS/ADB 连接等），否则操作会被拒绝 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **临时 API Key 不可撤销**：[Token](../concepts/token.md) 生命周期固定，到期自动失效，**不支持主动吊销或提前删除**。应严格控制 TTL 时长，避免在长生命周期前端会话中复用。  
- **SearchFilters 字段类型约束**：范围查询（`gt`/`gte`/`lt`/`lte`）仅支持数值型字段（`long`/`double`）；模糊查询（`like`）仅支持字符串型字段；多值查询需确保数组元素类型统一（全为 string 或全为 number）。非匹配类型将导致过滤失效或返回空结果 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。  
- **地域隔离**：临时 API Key 的生成 Endpoint 与目标模型服务地域强绑定（如新加坡地域需使用 `modelstudio.console.aliyun.com` 管理密钥，并调用对应地域的 `/api/v1/tokens`），跨地域调用将返回 `InvalidApiKey` 错误 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


