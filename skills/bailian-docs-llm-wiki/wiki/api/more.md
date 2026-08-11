# more

`more` 是百炼平台中一组面向高级用例与安全治理的扩展能力集合，涵盖服务关联角色（SLR）管理、临时认证凭据生成、以及知识库语义检索增强等功能。这些能力不直接参与模型推理主流程，但对工作流编排、权限隔离、数据过滤和可信调用等关键场景至关重要。开发者需结合具体业务需求按需启用，并严格遵循最小权限原则配置。

## 支持的模型/功能

- **服务关联角色（SLR）**：百炼通过预定义 SLR 自动获取对 FC、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、内容安全、DTS、CPFS 等云服务的受控访问权限，支撑工作流[函数调用](../concepts/function-calling.md)、OSS 数据导入、安全存储空间、知识库向量化、用量监控等核心功能。详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 生成**：提供 `/tokens` 接口，允许后端服务基于永久 API Key 签发短期有效的临时凭证（TTL 1–1800 秒），适用于浏览器或移动端等不可信环境的安全调用。
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，支持单值、多值、范围、模糊及标签查询，实现对语义检索结果的精准后置过滤，显著提升结构化数据场景下的召回准确率。该能力仅适用于已启用「数据查询」类型的知识库，详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 关键参数

| 参数 | 位置 | 类型 | 说明 | 示例 |
|------|------|------|------|------|
| `expire_in_seconds` | Query String | Integer | 临时 API Key 有效期（秒），取值范围 `[1, 1800]`，默认 `60` | `?expire_in_seconds=1800` |
| `searchFilters` | Request Body (`RetrieveRequest`) | Array of Objects | 检索过滤规则数组，每个对象为一个 AND 分组；支持 `{"字段": "值"}`（单值）、`{"字段": "[\"v1\",\"v2\"]"}`（多值）、`{"字段": "{\"gte\":20,\"lte\":27}\"}`（范围）、`{"字段": "{\"like\":\"技%员\"}"}`（模糊）等格式 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| `indexId` | Request Body (`RetrieveRequest`) | String | 必填，目标知识库 ID | `"o73yjlxxxx"` |
| `query` | Request Body (`RetrieveRequest`) | String | 必填，用户原始查询语句 | `"公司中姓名为张三的员工"` |

> **注意**：文档 3 中 Python 示例代码内 `multi_query()` 方法使用 `json.dumps(names)` 构造多值字符串，但实际 API 要求该字段值为 JSON 字符串（即双序列化），而 `range_query()` 和 `wildcard_query()` 同样采用 `json.dumps(...)` 包裹，该写法易引发格式错误；正确做法应确保 `search_filters` 中每个值已是合法 JSON 字符串（如 `"['张三','李四']"` 或 `'{"gte":20,"lte":27}'`），而非 Python 对象。请以 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 中的语法说明为准，避免直接复用示例中的 `json.dumps` 嵌套逻辑。

## 使用方式

- **服务关联角色**：首次启用对应功能（如添加函数计算节点、配置 OSS 数据源）时，系统自动创建 SLR；无需手动调用 API。角色名称与策略权限已在控制台和文档中明确定义，可通过 RAM 控制台统一审计。
- **生成临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起 `POST` 请求，携带 `Authorization: Bearer <PERMANENT_API_KEY>` 及可选 `expire_in_seconds` 查询参数。响应返回 `token`（临时密钥）与 `expires_at`（Unix 时间戳）。详见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **使用 SearchFilters**：在调用 `bailian20231229.Retrieve` 接口时，将 `searchFilters` 字段作为 `RetrieveRequest` 的成员传入。注意字段名须与知识库索引时定义的元数据字段名完全一致（区分大小写），且目标字段需已配置为可检索属性。

## 限制和注意事项

- **SLR 删除风险高**：删除任一 SLR（如 `AliyunServiceRoleForSFMAccessFC`）将导致依赖该角色的功能立即失效（如工作流无法调用 FC 函数），且删除前必须先解除所有业务绑定（如删除函数计算节点、断开 OSS/ADB 连接等）。操作前务必阅读对应文档的【删除服务关联角色】警告章节。
- **临时 API Key 不可撤销**：其生命周期由 `expire_in_seconds` 决定，到期自动失效，**不支持主动吊销或提前删除**。若发生泄露，应立即轮换其父级永久 API Key。
- **SearchFilters 兼容性约束**：
  - 仅对「数据查询」类型知识库生效；
  - 多值查询要求字段值为纯字符串或纯数值数组，不支持混合类型；
  - 范围查询（`gt`/`gte`/`lt`/`lte`）仅支持 `long` 或 `double` 类型字段；
  - 模糊查询（`like`）仅支持 `string` 类型字段，且 `%` 为通配符；
  - 标签查询（`tags`）仅适用于文档搜索、音视频搜索类知识库。
- **地域隔离**：临时 API Key 的 Endpoint 与生成所用 API Key 所属地域强绑定（北京/新加坡/弗吉尼亚），跨地域调用将失败。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


