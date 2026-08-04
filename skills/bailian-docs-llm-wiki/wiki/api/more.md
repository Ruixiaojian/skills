# more

`more` 是百炼平台中一组支撑性能力的统称，涵盖临时凭证管理、服务关联角色（SLR）授权、以及知识库高级检索过滤等功能。这些能力不直接参与模型推理，但为安全调用、跨云服务集成和精准语义检索提供关键基础设施支持。开发者需根据具体场景选择并正确配置对应组件。

## 支持的模型/功能

`more` 不代表具体模型，而是指代以下三类核心支撑功能：

- **临时 API Key 生成**：用于在前端或不可信环境（如浏览器、移动 App）中安全调用模型服务，避免永久密钥泄露；  
- **服务关联角色（SLR）**：百炼自动创建的 RAM 角色，用于访问 FC、OSS、ADB-PG、MNS、SLS 等阿里云服务资源；  
- **知识库 `searchFilters`**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级精确筛选，提升 RAG 结果相关性 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 2 中列出的 `AliyunServiceRoleForSFMAccessFC` 权限策略仅包含 `fc:ListFunctions` 和 `fc:InvokeFunction`，但实际工作流应用可能还需 `fc:GetFunction` 等元信息权限以完成节点校验——该差异已在最新控制台行为中修复，建议以 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 文档中声明的策略为准。

## 关键参数

| 功能 | 参数名 | 类型 | 说明 | 取值范围/示例 |
|------|--------|------|------|----------------|
| 临时 API Key | `expire_in_seconds` | integer | 临时 [Token](../concepts/token.md) 有效期（TTL） | `[1, 1800]` 秒，默认 `60`；示例：`?expire_in_seconds=1800` [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) |
| `searchFilters` | `searchFilters` | array of object | 检索过滤条件数组，每个对象为一个 AND 分组 | `[{"姓名": "张三"}, {"岗位": "技术员"}]`；支持单值、多值、范围（`gte`/`lt`）、模糊（`{"岗位": {"like": "技%员"}}`）、标签查询 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) |
| `searchFilters`（范围查询） | `gte`, `lte`, `gt`, `lt`, `eq`, `neq` | number/string | 字段比较操作符 | `"年龄": {"gte": 20, "lte": 27}`；`"姓名": {"eq": "张三"}` |

## 使用方式

### 临时 API Key
1. 后端服务需预先配置永久 `DASHSCOPE_API_KEY` 环境变量；  
2. 向对应地域 Endpoint 发起 POST 请求（如新加坡：`https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800`）；  
3. 使用响应中的 `token` 替换原 `Authorization: Bearer <permanent-key>`，有效期由 `expires_at` 时间戳标识。

### 服务关联角色
- **自动创建**：首次启用对应功能（如函数计算节点、OSS 数据导入、ADB-PG 知识库存储）时，百炼自动创建 SLR；  
- **手动管理**：可在 [RAM 控制台](https://ram.console.aliyun.com/) 查看、删除（需先解除业务依赖）；  
- **权限验证**：各 SLR 策略已明确限定最小必要权限（如 `AliyunServiceRoleForAccessOSS` 仅允许访问带特定 Bucket Tag 的 OSS 资源）[服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。

### `searchFilters`（知识库检索）
- 在 `RetrieveRequest` 中设置 `search_filters` 字段（SDK 中为 `search_filters` 或 `searchFilters`，依语言 SDK 命名而定）；  
- 支持嵌套 JSON 结构表达复杂条件（如 `{"年龄": {"gte": 25, "lt": 30}}`）；  
- 多值查询需对数组 `json.dumps`（Python）或等效序列化（Java/Go）后传入字符串字段值。

## 限制和注意事项

- **临时 API Key**：  
  - 不可手动删除，到期自动失效；  
  - 继承生成密钥的全部权限（含模型访问限制与知识库白名单），**不支持降权**；  
  - 各地域 Endpoint 独立，北京/新加坡/弗吉尼亚密钥不可混用 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  

- **服务关联角色**：  
  - 删除前必须解除所有业务依赖（如断开 OSS 连接、删除函数计算节点、停止数据同步任务），否则功能异常；  
  - `AliyunServiceRoleForSFMAccessingMNS` 明确禁止手动修改或授予权限给非 SLR 身份；  
  - 所有 SLR 的 `ram:DeleteServiceLinkedRole` 权限均受 `Condition` 保护，仅允许百炼服务自身调用删除。  

- **`searchFilters`**：  
  - 仅作用于 `Retrieve` 接口，不影响向量索引构建过程；  
  - 字段名须与知识库创建时定义的**原始列名完全一致**（区分大小写）；  
  - 模糊查询（`like`）和标签查询（`tags`）仅支持 string 类型字段，数值字段不支持 `like`；  
  - 子分组间为强制 `AND` 逻辑，不可配置 `OR` 或 `NOT`。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


