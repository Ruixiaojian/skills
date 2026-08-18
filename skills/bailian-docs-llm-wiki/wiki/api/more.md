# more

`more` 是百炼平台中一组面向高级用例的扩展能力集合，涵盖服务权限治理（服务关联角色）、安全凭证管理（临时 API Key）和知识库精准检索（SearchFilters）三大核心方向。这些功能不直接参与模型推理，但为生产级应用提供关键支撑：确保最小权限访问云资源、防止密钥泄露风险、提升结构化知识检索准确率。开发者需根据具体场景按需启用并严格遵循权限收敛原则。

## 支持的模型/功能

`more` 不对应具体模型，而是提供三类平台级功能支持：

- **服务关联角色（SLR）**：为百炼子系统（如工作流、数据管理、安全存储空间等）自动创建并托管对其他阿里云服务（FC、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、内容安全、DTS、CPFS）的最小权限访问能力。详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：用于在不可信前端环境（如浏览器、移动 App）中安全调用模型服务，通过后端服务动态签发、短时有效（1–1800 秒）的凭证，继承源 API Key 的全部权限范围。
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级精确过滤（如 `{"姓名": "张三"}`），显著减少无关噪声，特别适用于结构化表格数据场景。该能力依赖知识库索引配置中已声明的字段类型（string/double/long）。

> **注意**：文档 3 中 Python 示例代码内硬编码了 `bailian.cn-beijing.aliyuncs.com` Endpoint，但文档 2 明确指出“各地域的 API Key 不同”，且百炼控制台实际支持北京、新加坡、弗吉尼亚三地。开发者必须根据所用 API Key 所属地域（而非知识库部署地域）选择匹配的 Endpoint，否则将返回 `InvalidApiKey` 错误。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 来源 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | integer | 否（默认 60） | TTL，单位秒，取值范围 `[1, 1800]` | [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) |
| SearchFilters | `searchFilters` | array of object | 否 | 检索过滤条件数组，每个元素为一个子分组（AND 语义），支持单值、多值、范围（`gte`/`lte`）、模糊（`like`）、标签（`tags`）查询 | [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) |
| SearchFilters（范围查询） | `gte`, `lte`, `gt`, `lt`, `eq`, `neq` | number/string | 否 | 字段比较操作符，`gte`/`lte` 仅支持数值类型字段 | [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) |

## 使用方式

- **服务关联角色**：无需手动创建。当您首次在控制台启用某项依赖外部云服务的功能（例如在工作流中添加函数计算节点、在安全存储空间中绑定 OSS Bucket）时，百炼会自动为您创建对应 SLR。角色名称与策略均以 `AliyunServiceRoleFor*` 前缀标识，权限严格限定于该功能必需的最小动作集。
- **临时 API Key**：通过 `POST /api/v1/tokens` 接口调用，使用您的永久 API Key 在 `Authorization: Bearer` 头中鉴权，并可选传入 `expire_in_seconds` 查询参数。响应返回 `token`（临时密钥）和 `expires_at`（Unix 时间戳）。**注意：临时 Key 无法主动撤销，仅能等待过期**。
- **SearchFilters**：在调用 `Retrieve` 接口时，将 `searchFilters` 字段作为 JSON 对象嵌入请求体。每个子分组为 `{ "字段名": "值" }` 或 `{ "字段名": { "操作符": "值" } }` 形式（如 `{"年龄": {"gte": 20, "lte": 30}}`）。多值查询需对数组 `json.dumps` 编码；模糊查询需构造 `{"like": "前缀%"} `对象并 `json.dumps`。

## 限制和注意事项

- **服务关联角色删除风险极高**：删除任一 SLR（如 `AliyunServiceRoleForSFMAccessFC`）将导致其关联功能完全不可用（如工作流无法调用 FC 函数），且删除前必须先解除所有业务绑定（如删除函数计算节点、断开 OSS 连接、停止数据导入任务）。操作前务必阅读对应文档中的 **警告** 部分。
- **临时 API Key 权限继承无隔离**：临时 Key 完全继承签发它的永久 API Key 的所有权限（包括模型访问、知识库读写等），**不能用于权限降级或细粒度控制**。如需更精细的权限管控，应使用 RAM 子账号 + 自定义策略。
- **SearchFilters 依赖知识库索引配置**：仅对在知识库创建时明确设置为“参与检索”的字段生效；字段类型（string/double/long）必须与查询语法匹配（如 `gte` 不可用于 string 字段）；标签（`tags`）查询仅支持文档搜索、音视频搜索类知识库。
- **SLR 策略更新滞后风险**：文档 1 中 `AliyunServiceRoleForSFMTelemetry` 的策略 JSON 片段被截断（末尾缺失 `]` 和 `}`），实际策略可能包含更多 ARM/SLS 权限。请以控制台 RAM 角色详情页显示的最新策略为准，勿直接依赖文档片段。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


