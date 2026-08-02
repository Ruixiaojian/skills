# more

`more` 是百炼平台中一组面向高级用例的扩展能力集合，涵盖服务权限管理、临时凭证生成和[知识库](../concepts/knowledge-base.md)精细化检索等功能。这些能力不直接参与模型推理主链路，但对构建安全、可控、可观察的企业级AI应用至关重要。开发者需根据具体场景按需启用，并严格遵循最小权限原则配置相关资源。

## 支持的模型/功能

`more` 不对应特定模型，而是提供三类关键支撑能力：

- **服务关联角色（SLR）管理**：为百炼与外部云服务（如 FC、OSS、ADB-PG、MNS、SLS 等）的安全集成提供托管式权限委托机制，覆盖工作流编排、数据导入、安全存储、[知识库](../concepts/knowledge-base.md)向量化、监控分析等场景 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)；
- **临时 API Key 生成**：用于在不可信前端环境（如浏览器、移动端）安全调用百炼 API，避免永久密钥泄露；
- **[知识库](../concepts/knowledge-base.md) `searchFilters` 检索过滤**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，对语义检索结果进行字段级精准裁剪，显著提升 RAG 输出相关性 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中列出的 `AliyunServiceRoleForSFMTelemetry` 权限策略存在截断（末尾 JSON 不完整），实际策略应以控制台或最新 SDK 返回为准；其依赖的 `xtrace:Read*` 等权限在当前公开文档中未完整展开，建议通过 RAM 控制台查看实时策略内容。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|------|--------|------|------|------|----------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | 有效期（TTL） | `[1, 1800]` 秒，默认 `60` |
| `searchFilters` | `searchFilters` | array of object | 否 | 检索过滤条件数组，每个元素为一个子分组（AND 语义） | 最多支持 10 个子分组；每个子分组内 Key-Value 对数量无硬限制，但总请求体大小 ≤ 1 MB |
| `searchFilters` 子项 | 字段名（如 `"姓名"`） | string | 是 | 知识库文档 metadata 中定义的字段名 | 必须与知识库索引字段完全一致（区分大小写） |
| `searchFilters` 子项 | 字段值 | string / number / object | 是 | 支持单值、多值（JSON 数组）、范围（`{"gte": 20, "lte": 27}`）、模糊（`{"like": "技%员"}`）、标签（`["A大学", "学生会主席"]`） | 字符串值需 UTF-8 编码；数值类型必须匹配索引定义（如 `age` 字段为 `double`，则传 `25.0` 而非 `"25"`） |

## 使用方式

### 服务关联角色
- **自动创建**：首次在控制台启用对应功能（如函数计算节点、OSS 数据导入）时，系统自动创建 SLR，无需手动操作；
- **手动管理**：可在 [RAM 控制台](https://ram.console.aliyun.com/) > 角色管理 > 服务关联角色 页面查看、删除（删除前须按文档要求清理依赖资源）；
- **权限验证**：SLR 绑定的系统策略（如 `AliyunServiceRolePolicyForSFMAccessFC`）已预设最小必要权限，禁止修改或解绑。

### 临时 API Key
- **调用方式**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发送 `POST` 请求，`Authorization: Bearer <永久APIKey>`；
- **地域适配**：Endpoint 需与永久 API Key 所属地域一致（北京、新加坡、弗吉尼亚），[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 文档明确指出各 Endpoint 差异；
- **使用限制**：临时 Token 仅可用于 `dashscope.aliyuncs.com` 域名下的 API，不可用于其他阿里云服务。

### `searchFilters`
- **请求位置**：作为 `RetrieveRequest` 的顶层字段传入，与 `query`、`indexId` 同级；
- **语法结构**：
  ```json
  {
    "indexId": "o73yjlxxxx",
    "query": "公司中姓名为张三的员工",
    "searchFilters": [
      {"姓名": "张三"},
      {"岗位": "技术员", "性别": "男"}
    ]
  }
  ```
- **字段类型约束**：必须与知识库创建时定义的字段类型严格匹配（例如 `age` 字段为 `double`，则 `{"age": 25}` 合法，`{"age": "25"}` 将被忽略）。

## 限制和注意事项

- **SLR 删除风险**：删除任一 SLR 将导致对应功能立即失效（如删除 `AliyunServiceRoleForSFMAccessFC` 后，所有工作流中的函数计算节点无法调用），且恢复需重新授权并发布应用 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)；
- **临时 API Key 不可撤销**：生命周期内无法主动吊销，仅能等待过期；建议设置最短必要 TTL（如前端单次请求设为 `60` 秒），避免长期暴露；
- **`searchFilters` 适用范围**：仅作用于 `Retrieve` 接口返回的 `nodes` 列表，**不影响语义相似度计算过程**，即过滤发生在检索后而非检索中；
- **权限最小化原则**：SLR 策略已按功能隔离（如 `AliyunServiceRoleForAccessOSS` 仅允许访问打标 `bailian-safe-workspace-oss-access: ReadAndWrite` 的 Bucket），切勿通过自定义策略扩大权限；
- **知识库字段一致性**：`searchFilters` 中的字段名必须与知识库元数据（metadata）字段名完全一致，且该字段需在创建知识库时已声明为“参与检索”；
- **错误处理**：临时 Token 请求失败时，需捕获 `code`（如 `InvalidApiKey`）并触发密钥轮换流程；`searchFilters` 语法错误将导致整个请求失败（HTTP 400），错误信息中会明确指出非法字段或格式。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


