# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心界面，支持筛选、收藏、删除、OSS 转存及 API 直接引用等关键操作。所有资产默认保存在平台存储中，当前处于邀测阶段，平台存储免费开放。详细功能说明请参见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

资产中心当前支持以下模型生成的图片与视频资产：`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`z-image`、`wan2.7-image-pro`、`wan2.7-image`、`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。  
> **注意**：仅支持图片和视频资产，**不支持音频资产**（详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)）。  
核心功能包括：按类型/模型/时间/提示词筛选、收藏与“只看收藏”视图、批量删除与回收站管理（保留30天）、资产详情查看（含完整生成参数），以及通过 `asset_id` 在 API 中直接复用资产。

## 关键参数

- `asset_id`：每个资产唯一标识符，可在资产详情弹窗中获取，用于 API 输入（替代 `image_url` 或 `image_base64`）；  
- OSS 路径模板：默认为 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间标识；  
- 转存范围策略：支持“全部资产”或“N天前资产”，并可选是否释放平台存储副本（若释放，则资产不再显示于资产中心）；  
- 平台存储容量显示格式为 `已用容量 / 免费额度`（如 `0.00 / 5 GB`），该信息位于页面顶部统计栏。  
完整参数语义与约束请参考 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 使用方式

1. **开通入口**：登录百炼控制台 → 左侧导航栏选择 **工作台 > 资产中心** → 点击 **立即开通**；  
2. **OSS 绑定**：点击右上角 **绑定 OSS**，依次完成 SLR 授权（`AliyunServiceRoleForBailianAssetForward`）、Bucket 与路径配置、转存范围设置；  
3. **资产操作**：  
   - 筛选：使用顶部筛选器按类型、模型、日期、提示词搜索；  
   - 收藏/删除：悬停卡片操作，支持单选与批量；  
   - 查看详情：点击卡片弹出完整元数据（含提示词、模型名、生成时间等）；  
4. **API 集成**：在生图/生视频请求中，将 `asset_id` 作为输入字段（如 `reference_image.asset_id`），与 URL/Base64 互斥。  

## 限制和注意事项

- OSS 转存配置为**全局设置**，不随业务空间切换而变化（[资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 明确说明）；  
- 若绑定 OSS 时选择“释放平台存储副本”，则资产**不会出现在资产中心列表中**，仅存在于 OSS；  
- 回收站资产默认保留 30 天，到期自动清理，也可手动执行永久删除；  
- 权限需通过 RAM 策略显式授予：`AliyunBailianAssetCenterReader`（读/删）或 `AliyunBailianAssetCenterAdmin`（含 OSS 配置权限）；  
- > **注意**：文档中“平台存储免费开放”仅适用于邀测期，正式商用后将按量计费——该计费策略变更未在当前文档中明确生效时间，开发者应关注后续公告。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


