# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心界面，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认持久化于平台存储（当前邀测阶段免费），支持按业务空间隔离展示，并可通过配置实现自动同步至用户自有 OSS Bucket。详细功能与行为规范请参考 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

资产中心当前支持以下模型生成的图片与视频资产入库与管理：  
`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`z-image`、`wan2.7-image-pro`、`wan2.7-image`、`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。  
> **注意**：仅支持图片与视频两类资产，**不支持音频资产**，该限制在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中明确声明。

核心功能包括：
- 多维筛选（类型、模型、时间范围、提示词关键词）；
- 收藏/取消收藏、批量删除、回收站（保留 30 天）；
- OSS 全局转存配置（含路径模板、转存范围、是否释放平台副本）；
- 资产详情查看（含完整生成参数与 `asset_id`）；
- 在生图/生视频 API 中直接通过 `asset_id` 引用已有资产，替代 `image_url` 或 `image_base64`。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `asset_id` | 资产唯一标识符，用于 API 输入引用；在资产详情弹窗右侧字段中获取 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}` | OSS 默认路径模板，其中 `{workspace}` 为当前业务空间标识 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| `AliyunBailianAssetCenterReader` / `AliyunBailianAssetCenterAdmin` | RAM 权限策略，分别控制只读与含 OSS 配置的管理权限 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |

## 使用方式

1. **开通入口**：登录百炼控制台 → 左侧导航栏 **工作台 > 资产中心** → 点击 **立即开通**；  
2. **OSS 绑定（可选但推荐）**：右上角点击 **绑定 OSS** → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择地域/Bucket/目录 → 配置路径模板与转存策略（如“仅转存 30 天前资产”并勾选“释放平台存储”）；  
3. **资产操作**：在列表页悬停卡片执行收藏/删除；勾选后使用顶部批量操作栏；点击卡片查看详情及 `asset_id`；  
4. **API 集成**：调用 `qwen-image-*` 或 `wan2.7-*` 模型时，在对应输入字段（如 `control_image`、`first_frame`）中传入 `"asset_id": "xxx"`，无需再提供 URL 或 Base64。

## 限制和注意事项

- OSS 转存配置为**全局生效**，不随业务空间切换而变化；但资产列表始终仅显示**当前业务空间**下的生成内容；  
- 若 OSS 转存时选择“释放平台存储”，该资产将**不再出现在资产中心列表中**，仅保留在 OSS 中；  
- 回收站资产默认保留 30 天，到期自动清理，期间可手动执行永久删除；  
- 平台存储当前免费，但正式商用后将按量计费，容量明细可在页面顶部“平台存储”信息图标中查看；  
- > **注意**：文档中“首次使用前需开通”的操作路径与实际控制台 UI 可能存在版本偏差——部分新版环境已默认启用资产中心，若未见开通按钮，请确认账号权限及邀测白名单状态（参见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) “重要”提示）。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


