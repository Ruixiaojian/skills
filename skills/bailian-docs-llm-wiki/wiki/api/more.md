# more

`more` 是百炼平台中一组面向高级用例的扩展能力集合，涵盖服务权限管理、安全认证机制与知识库精细化检索等功能。它不构成独立 API 服务，而是以配套机制形式支撑工作流编排、安全存储、模型监控、RAG 等核心场景。开发者需结合具体功能模块（如知识库、工作流、安全存储）按需启用和配置。

## 支持的模型/功能

`more` 本身不提供模型，而是为以下功能提供底层支撑能力：

- **服务关联角色（SLR）**：自动创建并绑定 RAM 角色，使百炼可安全访问外部云资源（如 FC、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、DTS、CPFS、内容安全）。例如，工作流调用函数计算节点依赖 `AliyunServiceRoleForSFMAccessFC`，知识库对接 ADB-PG 依赖 `AliyunServiceRoleForSFMAccessADB` [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **临时 API Key 生成**：用于在不可信前端环境（如浏览器、App）中安全调用模型服务，避免永久密钥泄露。该能力通过 `/api/v1/tokens` 接口提供，由后端服务代理调用 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级、范围级、模糊级或标签级二次过滤，显著提升 RAG 结果精准度 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中列出的 `AliyunServiceRoleForSFMTelemetry` 权限策略截断（末尾缺失），实际策略应包含完整 `xtrace:*` 动作；请以控制台或最新 OpenAPI 返回的实际策略为准。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | TTL（秒），取值范围 `[1, 1800]`，默认 `60` | `?expire_in_seconds=1800` |
| SearchFilters | `searchFilters` | array of object | 否 | 每个 object 为一个 AND 分组，支持单值、多值、范围（`gte`/`lt`等）、模糊（`like`）、标签（`tags`）查询 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（范围查询） | 字段值格式 | string (JSON) | 是（范围查询时） | 需 JSON 序列化，如 `{"gte": 20, "lte": 27}` | `"年龄": "{\"gte\":20,\"lte\":27}"` |

## 使用方式

- **服务关联角色**：首次开通对应功能（如工作流中添加 FC 节点、安全存储接入 OSS 或 ADB-PG）时，系统自动创建 SLR；无需手动创建，但需确保 RAM 权限允许创建 SLR（如 `ram:CreateServiceLinkedRole`）。查看与管理请前往 [RAM 控制台](https://ram.console.aliyun.com/) → 角色管理。  
- **临时 API Key**：后端服务使用永久 API Key（`DASHSCOPE_API_KEY`）向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起 POST 请求，携带 `expire_in_seconds` 查询参数；响应返回 `token`（即临时 Key）与 `expires_at`（Unix 时间戳）。  
- **SearchFilters**：在 `RetrieveRequest` 请求体中直接嵌入 `searchFilters` 字段（非 query string），SDK 调用示例见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 中的 Python/Java 完整代码；注意字段名须与知识库索引时定义的字段名严格一致（区分大小写）。

## 限制和注意事项

- **SLR 删除风险高**：删除任一 SLR（如 `AliyunServiceRoleForSFMAccessFC`）将导致依赖该角色的功能立即失效（如工作流无法调用 FC 函数），且删除前必须先清理所有关联资源（如删除函数计算节点、断开 OSS/ADB-PG 连接、停止数据导入任务）[服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **临时 API Key 不可撤销**：生命周期固定，到期自动失效，不支持手动删除或提前吊销；务必严格控制 `expire_in_seconds` 时长，避免过长 TTL 增加泄露风险 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **SearchFilters 兼容性约束**：仅适用于知识库类型为“数据查询”的结构化知识库；非结构化文档知识库（如 PDF 文本切片）不支持字段级过滤；多值查询需确保字段类型为纯字符串或纯数值数组，且值需 JSON 序列化后传入 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。  
- **地域隔离**：临时 API Key 的 Endpoint 与永久 API Key 所属地域强绑定（北京/新加坡/弗吉尼亚），跨地域调用将返回 `InvalidApiKey` 错误。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


