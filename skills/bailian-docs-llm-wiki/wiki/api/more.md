# more

`more` 是百炼平台面向高级用例提供的扩展能力集合，涵盖临时凭证管理、服务权限委托和知识库精细化检索三大核心方向。它不构成独立 API 服务，而是作为模型调用、工作流编排和 RAG 场景的支撑性机制，需结合具体功能模块（如 `Retrieve`、函数计算节点、安全存储空间等）协同使用。开发者应根据实际场景选择对应能力，并严格遵循权限最小化原则。

## 支持的模型/功能

`more` 本身不提供模型推理能力，但为以下关键功能提供底层支持：

- **临时 API Key 生成**：用于在浏览器、移动端等不可信环境安全调用模型服务（如 `qwen-max`、`qwen-plus` 等所有支持 DashScope 协议的模型），避免永久密钥泄露 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **服务关联角色（SLR）**：为百炼工作流、数据管理、安全存储空间、知识库、用量监控等模块自动创建并托管 RAM 角色，实现对 FC、OSS、ADB-PG、MNS、SLS 等云服务的安全访问授权 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **知识库 SearchFilters**：在 `Retrieve` 接口调用中对语义检索结果进行结构化过滤，支持单值、多值、范围、模糊及标签查询，显著提升结构化数据（如员工表、产品目录）的召回精度 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 2 中列出的 `AliyunServiceRoleForSFMAccessFC` 权限仅包含 `fc:ListFunctions` 和 `fc:InvokeFunction`，但实际工作流调用 FC 函数可能还需 `fc:GetFunction` 等元数据权限；建议以控制台实际授予策略为准，而非仅依赖文档描述。

## 关键参数

| 参数/字段 | 所属能力 | 类型 | 说明 | 示例 |
|-----------|----------|------|------|------|
| `expire_in_seconds` | 临时 API Key | integer | TTL 有效期，单位秒，取值范围 `[1, 1800]` | `1800`（30 分钟） |
| `searchFilters` | 知识库检索 | array of object | 过滤条件数组，每个元素为一个子分组（AND 语义），支持 `{"字段名": "值"}` 或高级语法如 `{"年龄": {"gte": 20, "lte": 30}}` | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| `token` | 临时 API Key 响应 | string | 生成的短期凭证，格式为 `st-***` | `st-9a8b7c6d...` |
| `expires_at` | 临时 API Key 响应 | number | UNIX 时间戳，表示过期时间 | `1744080369` |

## 使用方式

### 临时 API Key
1. 在后端服务中配置永久 `DASHSCOPE_API_KEY` 环境变量；
2. 向 `https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800` 发起 POST 请求（北京地域）或对应地域 Endpoint；
3. 将响应中的 `token` 作为 `Authorization: Bearer <token>` 用于后续模型调用。

### 服务关联角色
- **无需手动创建**：当首次在控制台启用对应功能（如添加函数计算节点、配置 OSS 数据源）时，系统自动创建 SLR；
- **权限验证**：可在 [RAM 控制台](https://ram.console.aliyun.com/) 查看角色及绑定策略；
- **删除前提**：必须先解除该角色所依赖的所有业务配置（如删除函数计算节点、断开 OSS 连接等），否则删除失败。

### SearchFilters
- 在 `RetrieveRequest` 请求体中直接传入 `searchFilters` 字段；
- 每个子分组内支持多种查询语法：
  - 单值：`{"姓名": "张三"}`
  - 范围：`{"年龄": {"gte": 25, "lte": 35}}`
  - 模糊：`{"岗位": {"like": "技%员"}}`
  - 多值（需 JSON 序列化）：`{"姓名": "[\"张三\",\"李四\"]"}`
- 注意：子分组间为 AND 关系，不可更改；标签查询仅适用于文档/音视频类知识库。

## 限制和注意事项

- **临时 API Key**：无法提前撤销，到期自动失效；继承父密钥全部权限，**不得用于高权限操作场景**；各地域 Endpoint 不互通，需按实际部署地域调用 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **服务关联角色**：删除前必须满足前置清理条件（如文档 2 中明确要求“删除所有已发布的工作流应用中的函数计算节点”），否则操作被拒绝；`AliyunServiceRoleForSFMAccessingMNS` 明确禁止用户修改或删除 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **SearchFilters**：仅对已索引字段生效，未在知识库配置中启用“参与检索”的字段无法过滤；多值查询需将数组 JSON 序列化为字符串传入（见文档 3 Python 示例）；模糊查询 `like` 仅支持 `%` 通配符，不支持正则表达式 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。
- **通用限制**：所有 `more` 相关能力均受百炼配额与计费规则约束，临时 Key 调用计入调用者配额；SLR 权限变更可能影响已有工作流执行，请在生产环境变更前充分测试。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


