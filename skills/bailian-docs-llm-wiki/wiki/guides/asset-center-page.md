# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心入口，支持筛选、收藏、删除、OSS 转存及 API 直接引用等关键能力。所有资产默认持久化于平台存储（邀测期免费），用户可通过控制台开通并配置全局 OSS 同步策略。资产与业务空间强绑定，但 OSS 配置为账号级全局设置，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

资产中心当前支持以下模型生成的**图片与视频资产**管理（不支持音频）：  
`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`z-image`、`wan2.7-image-pro`、`wan2.7-image`、`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。  

核心功能包括：  
- 多维筛选（类型、模型、时间范围、提示词关键词）；  
- 收藏/取消收藏、批量删除与回收站管理（保留 30 天）；  
- 资产详情查看（含完整生成参数、提示词、模型名、时间戳）；  
- 通过 `asset_id` 在生图/生视频 API 中直接引用资产，替代 `image_url` 或 `image_base64` —— 具体字段兼容性请参考 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中“在 API 中使用资产”章节。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `asset_id` | 资产唯一标识符，可在资产详情弹窗中获取，用于 API 输入参数（如 `reference_image.asset_id`） | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}` | OSS 默认路径模板，其中 `{workspace}` 为当前业务空间 ID | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| 转存范围策略 | 支持“全部资产”或“N 天前资产”，并可选是否释放平台存储副本（释放后资产不再显示于资产中心） | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |

> **注意**：路径模板中的 `{workspace}` 实际取值为业务空间的 **ID 字符串**（非名称），需在控制台「工作空间管理」中确认，避免因误填导致 OSS 写入失败。

## 使用方式

1. **开通与访问**：登录 [阿里云百炼控制台](https://bailian.console.aliyun.com/) → 左侧导航栏 **工作台 > 资产中心** → 点击 **立即开通**。  
2. **OSS 绑定（可选但推荐）**：点击右上角 **绑定 OSS** → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择地域/Bucket/目录 → 配置路径模板与转存策略。  
3. **资产操作**：  
   - 筛选：顶部筛选栏按类型、模型、日期、提示词搜索；  
   - 管理：悬停卡片操作（收藏/删除），或勾选后批量操作；  
   - 查看详情：点击卡片 → 弹窗中复制 `asset_id`；  
4. **API 集成**：在调用 `qwen-image-*` 或 `wan2.7-*` 模型时，将 `asset_id` 填入对应输入字段（如 `control_image.asset_id`），无需额外传 URL/Base64。

## 限制和注意事项

- **存储生命周期**：平台存储免费期仅限邀测阶段，正式商用后将按量计费；当前容量显示格式为 `已用 / 免费额度`（如 `0.00 / 5 GB`）。  
- **OSS 配置全局性**：绑定后对账号下所有业务空间生效，切换空间不影响已配置的 Bucket 和路径规则。  
- **释放平台存储的风险**：若 OSS 转存配置中启用“释放平台存储”，资产将**立即从资产中心列表消失且不可恢复**（不进入回收站），仅保留在 OSS 中。  
- **权限隔离**：资产列表仅展示当前业务空间资产；子账号需被授予 `AliyunBailianAssetCenterReader`（只读+删除）或 `AliyunBailianAssetCenterAdmin`（含 OSS 配置）策略方可操作。  
- **API 兼容性边界**：`asset_id` 仅支持同账号、同 Region 下的模型调用，跨账号或跨 Region 引用会返回 `404` 错误。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


