# more

本分类涵盖百炼平台的辅助功能与高级配置，包括服务关联角色管理、临时 API Key 生成以及知识库检索过滤等。这些功能为开发者在安全管控、权限管理和数据检索精度优化方面提供支撑。

## 服务关联角色（SLR）

百炼通过服务关联角色获取对其他阿里云服务的访问权限。首次授权开通相关功能时，系统自动创建对应角色，无需手动操作。详细信息参见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。

### 角色列表概览

| 角色名称 | 用途 | 关联服务 |
|---------|------|---------|
| AliyunServiceRoleForSFMAccessFC | 工作流应用/流程编排访问函数计算 | FC |
| AliyunServiceRoleForSFMDataHubOSSImport | 数据管理导入 OSS 数据 | OSS |
| AliyunServiceRoleForAccessOSS | 安全存储空间访问 OSS | OSS |
| AliyunServiceRoleForSFMAccessADB | 知识库/安全存储访问 ADB-PG | ADB-PG |
| AliyunServiceRoleForSFMAccessingMNS | 数据管理监听 OSS 变更消息 | MNS |
| AliyunServiceRoleForSFMTelemetry | 用量监控与性能分析 | OpenTelemetry |
| AliyunServiceRoleForSFMAccessingCIP | 应用访问内容安全服务 | 内容安全 |
| AliyunServiceRoleForSFMAccessSLS | 模型监控访问日志服务 | SLS |
| AliyunServiceRoleForSFMAccessCMS | 模型监控访问云监控 | CMS |
| AliyunServiceRoleForAccessCusOss | 平台托管操作用户 OSS 文件 | OSS |
| AliyunServiceRoleForSFMConnectorAccessDTS | 通过 DTS 接入外部数据源 | DTS |
| AliyunServiceRoleForSFMFineTuning | 模型调优访问 CPFS/OSS | CPFS, OSS |

### 删除注意事项

- 删除 SLR 前需先移除依赖该角色的资源或配置（如断开安全存储空间连接、删除函数计算节点等）
- 删除操作参见 RAM 控制台的[服务关联角色](https://help.aliyun.com/zh/ram/user-guide/service-linked-roles#section-b9f-8dv-b5q)文档
- 删除后相关功能将不可用，请谨慎操作

## 临时 API Key

在浏览器、移动 App 等不可信环境中，应使用临时 API Key 代替永久 API Key 以防止泄露。详见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

### 关键参数

| 参数 | 说明 |
|------|------|
| `expire_in_seconds` | 有效期，范围 [1, 1800] 秒，默认 60 秒 |

### 请求方式

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 响应结构

成功时返回：

```json
{
  "token": "st-****",
  "expires_at": 1744080369
}
```

- `token`：临时 API Key，以 `st-` 开头
- `expires_at`：过期时间（UNIX 时间戳，秒）

### 限制与注意事项

- 临时 API Key 继承生成它的永久 API Key 的全部权限（含模型和知识库访问限制）
- 无法手动删除，到期后自动失效
- 各地域 Endpoint 不同，北京使用 `dashscope.aliyuncs.com`，新加坡和弗吉尼亚使用对应地域 Endpoint

## 知识库 SearchFilters

在调用知识库 Retrieve 接口时，可通过 `searchFilters` 参数对语义检索结果进行结构化过滤，减少干扰信息。该功能尤其适合结构化数据场景。完整用法参见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

### 语法结构

```json
{
  "searchFilters": [
    { "字段A": "值1", "字段B": "值2" },
    { "字段C": "值3" }
  ]
}
```

- 子分组之间为 **AND** 语义，不可更改
- 同一子分组内的多个键值对也为 AND 关系

### 支持的查询类型

| 查询类型 | 字段类型 | 示例 |
|---------|---------|------|
| 单值查询 | 数值（long/double）、字符串 | `{"姓名": "张三"}` |
| 多值查询 | 纯数值或纯字符串数组 | `{"姓名": "[\"张三\",\"李四\"]"}` |
| 范围查询（等值） | 数值、字符串 | `eq`、`neq` |
| 范围查询（区间） | 数值 | `gt`、`gte`、`lt`、`lte` |
| 模糊查询 | 字符串 | `{"like": "技%员"}`（`%` 匹配任意字符） |
| 标签查询 | 仅文档搜索/音视频搜索知识库 | `{"tags": "[\"标签1\",\"标签2\"]"}`（多标签为 OR 关系） |

### 前置条件

- 子账号需获取 `AliyunBailianDataFullAccess` 策略并加入业务空间
- 需安装阿里云百炼 SDK 并配置 AccessKey 环境变量
- 知识库需已创建且字段参与检索

### 使用示例（Python）

```python
retrieve_request.query = '公司中叫张三的员工'
retrieve_request.index_id = '<知识库ID>'
retrieve_request.search_filters = [
    {"姓名": "张三"},
    {"性别": "女"}
]
resp = client.retrieve('<业务空间ID>', retrieve_request)
```

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)

