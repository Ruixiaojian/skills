# more

`more` 是百炼平台面向高级用例提供的扩展能力集合，涵盖临时凭证生成、服务关联角色管理、知识库检索过滤等关键功能。这些能力主要用于增强安全性、实现跨云服务集成、提升结构化数据检索精度，适用于工作流编排、安全存储、RAG 应用等生产场景。开发者需结合具体业务需求按需启用，并严格遵循权限最小化原则。

## 支持的模型/功能

`more` 并非单一模型，而是平台级能力模块，当前包含以下核心功能：

- **临时 API Key 生成**：为浏览器、移动端等不可信环境提供短期访问凭证，避免永久密钥泄露风险 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)  
- **服务关联角色（SLR）**：自动创建并托管 RAM 角色，用于百炼访问函数计算（FC）、OSS、ADB-PG、MNS、OpenTelemetry 等阿里云服务资源 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)  
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级精确过滤，显著降低噪声 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)

> **注意**：文档 2 中 `AliyunServiceRoleForSFMAccessingMNS` 的策略示例末尾被截断（`"xtrace:Describe*"` 后缺失闭合括号与完整 JSON），实际使用请以控制台或最新 SDK 返回的策略为准；该问题已在 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 文档中体现。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例值 |
|------|--------|------|------|------|--------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | TTL（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters | `searchFilters` | array of object | 否 | 检索过滤子分组列表，各子分组内支持单值、多值、范围、模糊、标签查询 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（范围查询） | `gte`, `lte`, `gt`, `lt`, `eq`, `neq` | number/string | 否 | 字段比较操作符，需嵌套在字段值中（如 `{"年龄": "{\"gte\":20,\"lte\":27}\"}`） | `{"age": "{\"gte\":25}"}` |

## 使用方式

- **临时 API Key**：通过后端服务向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起 `POST` 请求，携带 `Authorization: Bearer <永久APIKey>`，响应返回 `token` 和 `expires_at` 时间戳。客户端后续请求直接使用该 `token` 替代永久密钥。  
- **服务关联角色**：首次启用对应功能（如工作流中添加 FC 节点、安全存储空间绑定 OSS）时，系统自动创建 SLR；无需手动调用 API，但需确保主账号具备 `ram:CreateServiceLinkedRole` 权限。  
- **SearchFilters**：在 `RetrieveRequest` 请求体中直接设置 `searchFilters` 字段，支持 JSON 格式嵌套；SDK 调用时需按语言规范序列化（如 Python 中需 `json.dumps` 后赋值），详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 中的完整代码示例。

## 限制和注意事项

- 临时 API Key **不可主动撤销**，仅能等待过期（最长 1800 秒），且继承生成者密钥的全部权限，包括模型访问与知识库读写限制 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- 所有服务关联角色均受 **RAM 权限管控**，删除前必须先解除其依赖资源（如删除 FC 节点、断开 OSS 连接、停止 MNS 订阅等），否则将导致对应功能异常 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- `SearchFilters` 仅作用于 **已成功索引的结构化字段**（如知识库配置中明确指定为 `string`/`double` 类型的列），未索引字段或类型不匹配的字段过滤无效；多值查询需确保字段值为纯数组（如 `["张三","李四"]`），字符串形式数组（如 `"[\"张三\",\"李四\"]"`）将被忽略。  
- 各地域 Endpoint 独立（北京、新加坡、弗吉尼亚），临时 [Token](../concepts/token.md) 接口与模型调用接口需使用**同一地域**的域名，混用将返回 `InvalidApiKey` 错误 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


