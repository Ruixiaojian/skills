# more

`more` 是百炼平台中一组面向高级用例的扩展能力集合，涵盖服务权限管理、临时凭证生成和知识库精细化检索等核心功能。这些能力不直接参与模型推理主流程，但对构建安全、可控、可观察的企业级AI应用至关重要。开发者需根据具体场景选择并正确配置对应能力。

## 支持的模型/功能

`more` 并非模型名称或推理接口，而是百炼平台提供的**扩展功能模块集合**，当前包含以下三类关键能力：

- **服务关联角色（SLR）管理**：为百炼各子服务（如工作流、数据管理、安全存储空间等）自动申请并托管对其他云服务（FC、OSS、ADB-PG、MNS、SLS 等）的最小必要访问权限。详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 生成**：用于在不可信前端环境（如浏览器、App）中安全调用百炼 API，避免永久密钥泄露。该能力继承源 API Key 的全部权限范围。
- **知识库 `searchFilters` 检索过滤**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级精准筛选，显著提升结构化数据查询准确率。详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中列出的 `AliyunServiceRoleForSFMTelemetry` 权限策略片段被截断（末尾缺失 `}`），实际使用时请以控制台或最新版 RAM 策略文档为准；其完整策略应包含 `xtrace` 相关读取权限及 `ram:DeleteServiceLinkedRole` 条件授权。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|------|--------|------|------|------|----------|
| 临时 API Key | `expire_in_seconds` | Integer | 否 | 临时 [Token](../concepts/token.md) 有效期（秒） | `[1, 1800]`，默认 `60` |
| `searchFilters` | `searchFilters` | Array of Object | 否 | 检索过滤条件数组，每个元素为一个子分组（AND 语义） | — |
| `searchFilters` 子分组内 | 字段名（如 `"姓名"`） | String | 是 | 知识库文档元数据字段名 | 需与知识库索引字段定义一致 |
| `searchFilters` 子分组内 | 字段值 | String / Number / Array / Object | 是 | 支持单值、多值（JSON 数组）、范围（`{"gte":18,"lte":25}`）、模糊（`{"like":"技%员"}`）、标签（`["A大学","学生会主席"]`） | 见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 语法说明 |

## 使用方式

- **服务关联角色**：无需主动创建。当您首次在控制台启用依赖外部云服务的功能（如添加函数计算节点、配置 OSS 数据源、接入 ADB-PG 知识库）时，系统自动为您创建对应 SLR。角色名称与权限策略已预置，不可修改。详情参见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：通过 `POST https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=N` 调用，需在 `Authorization` Header 中携带有效的永久 `Bearer` API Key。响应返回 `token`（即临时 Key）和 `expires_at`（Unix 时间戳）。**重要**：临时 Key 继承源 Key 的全部权限，包括模型/知识库访问限制。
- **`searchFilters`**：在调用 `Retrieve` 接口（如 `/api/v1/retrieve`）的 JSON 请求体中，与 `indexId`、`query` 同级传入 `searchFilters` 字段。支持嵌套多层逻辑（子分组间 AND，子分组内字段间 AND），不支持 OR 或 NOT 逻辑。示例见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **SLR 删除风险**：删除任一服务关联角色（如 `AliyunServiceRoleForSFMAccessFC`）将导致对应功能（如工作流中的函数计算节点）立即失效。删除前必须先解除所有依赖该角色的资源绑定（如删除函数节点、断开 OSS/ADB 连接、停止数据导入任务），否则操作将失败。
- **临时 API Key 不可撤销**：临时 Key 生命周期固定，到期自动失效，**无法手动删除或提前吊销**。务必严格控制 `expire_in_seconds` 时长，并确保调用方环境安全。
- **`searchFilters` 兼容性**：仅对**数据查询型知识库**（Data Query）生效；文档搜索、音视频搜索类知识库仅支持 `tags` 字段过滤。字段类型（string/long/double）必须与知识库索引定义严格匹配，否则过滤无效。
- **权限继承原则**：所有 `more` 功能均受制于调用者所持凭证（API Key 或 AccessKey）的 RAM 权限。例如，若子账号未被授予 `AliyunBailianDataFullAccess` 策略，则无法使用 `searchFilters` 调用 `Retrieve` 接口。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


