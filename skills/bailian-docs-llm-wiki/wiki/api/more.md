# more

`more` 是百炼平台中一组面向高级用例的扩展能力集合，涵盖服务权限管理、安全鉴权机制与知识库精准检索等核心功能。它不提供独立 API 接口，而是作为底层支撑能力嵌入工作流编排、数据接入、模型调用及 RAG 等关键链路中。开发者需结合具体场景按需启用，并严格遵循权限最小化与生命周期管理原则。

## 支持的模型/功能

`more` 本身不对应具体模型，而是支撑以下平台级功能的基础设施：
- **服务关联角色（SLR）**：为百炼访问外部云服务（如 FC、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、内容安全、DTS、CPFS）提供受控权限，由系统在首次启用对应功能时自动创建 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)；
- **临时 API Key 生成**：用于不可信前端环境的安全调用，继承源密钥全部权限，支持 TTL 自定义；
- **知识库 `searchFilters` 检索过滤**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级精确筛选，显著提升 RAG 输出相关性。

## 关键参数

| 参数 | 位置 | 类型 | 说明 | 示例 |
|------|------|------|------|------|
| `expire_in_seconds` | Query String | Integer | 临时 API Key 有效期（秒），取值范围 `[1, 1800]` | `?expire_in_seconds=1800` |
| `searchFilters` | Request Body (`RetrieveRequest`) | Array of Objects | 知识库检索过滤规则，支持单值、多值、范围、模糊、标签查询；子分组间为 AND 逻辑 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| `token` | Response Body | String | 生成的临时 API Key，前缀为 `st-` | `st-abc123...` |
| `expires_at` | Response Body | Number | UNIX 时间戳（秒），表示过期时间 | `1744080369` |

> **注意**：文档 3 中 `searchFilters` 的 `multi_query` 示例代码使用 `json.dumps(names)` 传递数组，但实际 SDK（如 `alibabacloud_bailian20231229`）要求直接传入 Python list 或 Java List 对象，`json.dumps` 会导致类型错误。请以 [SDK 文档](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29) 为准，避免手动序列化。

## 使用方式

### 服务关联角色
- **自动创建**：当您在控制台首次启用「函数计算节点」「OSS 数据导入」「安全存储空间」「知识库 ADB-PG 接入」等功能时，百炼自动创建对应 SLR（如 `AliyunServiceRoleForSFMAccessFC`）；
- **手动管理**：可在 RAM 控制台查看、审计或删除（需先解除依赖资源）[服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)；
- **权限验证**：各 SLR 绑定的系统策略（如 `AliyunServiceRolePolicyForAccessOSS`）已明确限定操作范围与资源条件，禁止修改。

### 临时 API Key
- **调用方式**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发送带 `Authorization: Bearer <永久APIKey>` 的 POST 请求；
- **地域隔离**：北京、新加坡、弗吉尼亚地域 endpoint 不互通，API Key 需匹配对应地域 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)；
- **生命周期**：仅可设置 TTL，不可主动撤销，到期自动失效。

### `searchFilters` 使用
- **前提**：知识库需配置为「数据查询」类型，且字段已声明类型（string/double/long）；
- **语法**：`searchFilters` 是 JSON 数组，每个元素为一个键值对对象（单值）或含 `eq`/`gte`/`like` 等操作符的对象（高级查询）；
- **示例**（年龄区间 + 岗位精确匹配）：
  ```json
  "searchFilters": [
    {"岗位": "技术员"},
    {"年龄": {"gte": 20, "lte": 27}}
  ]
  ```
- **完整实现参考**：[知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 提供了 Python/Java 多种查询模式的可运行代码。

## 限制和注意事项

- **SLR 删除风险**：删除任一服务关联角色将导致对应功能完全不可用（如删除 `AliyunServiceRoleForSFMAccessFC` 后，工作流中所有函数计算节点失效），且删除前必须清空所有依赖资源；
- **临时 API Key 权限继承**：其权限范围严格等于生成所用的永久 API Key，若后者被限制访问某知识库，则临时 Key 也无法访问；
- **`searchFilters` 兼容性**：仅适用于「数据查询」类知识库；文档搜索、音视频搜索类知识库仅支持 `tags` 字段过滤；
- **OSS 权限隔离**：不同 SLR 对 OSS 的访问受 Bucket Tag 严格约束（如 `bailian-datahub-access: read`），不得跨场景复用同一 Bucket；
- **MNS 队列命名约束**：`AliyunServiceRoleForSFMAccessingMNS` 仅允许操作以 `bailian-oss-event*` 开头的队列，禁止手动创建或修改其他队列权限。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


