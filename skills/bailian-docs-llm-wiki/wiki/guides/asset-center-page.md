# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台页面，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认持久化于平台存储（邀测期免费），支持按业务空间隔离展示。开发者可通过控制台开通并配置功能，也可在 API 中直接复用已有资产 ID，避免重复上传。

## 支持的模型/功能

资产中心当前支持以下模型生成的资产纳管：`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`z-image`、`wan2.7-image-pro`、`wan2.7-image`、`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。仅支持图片与视频两类资产，**不支持音频资产**。功能覆盖全生命周期操作：查看统计、多维筛选、收藏/删除/回收站管理、OSS 自动转存、以及通过 `asset_id` 在 API 中直接引用资产。详细支持范围请以 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 页面实时展示为准。

## 关键参数

- `asset_id`：全局唯一资产标识符，用于 API 输入参数（替代 `image_url` 或 `image_base64`），可在资产详情弹窗中获取；
- OSS 路径模板：默认为 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间标识；
- 转存策略：支持“全部资产”或“N 天前资产”，并可选是否释放平台存储副本（释放后资产不再显示于资产中心）；
- 回收站保留期：默认 30 天，到期自动清理，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

> **注意**：OSS 转存配置为全局设置，**不随业务空间切换而变化**；但资产列表严格按当前业务空间过滤——这一行为差异已在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 的“常见问题”中明确说明，需特别注意权限与数据可见性的边界。

## 使用方式

1. **开通与访问**：登录百炼控制台 → 左侧导航栏选择 **工作台 > 资产中心** → 点击 **立即开通**；
2. **OSS 绑定**：右上角点击 **绑定 OSS** → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择 Bucket、配置路径与转存策略；
3. **筛选与操作**：使用顶部筛选器（类型/模型/日期/提示词搜索）定位资产；悬停卡片执行收藏、删除；勾选后批量操作；
4. **API 集成**：调用生图/生视频模型时，在对应输入字段（如 `control_image`、`reference_video`）中传入 `"asset_id": "xxx"`，三选一（`asset_id` / `image_url` / `image_base64`）或二选一（`asset_id` / `url_or_base64`），具体格式参见各模型 API 文档。

## 限制和注意事项

- 平台存储当前免费，但正式商用后将按量计费；邀测阶段容量上限未公开，建议主动配置 OSS 转存规避超限风险；
- 删除操作仅移入回收站，**非永久删除**；永久删除需进入回收站手动触发；
- RAM 权限需显式授予：普通用户需 `AliyunBailianAssetCenterReader`，OSS 配置权限需 `AliyunBailianAssetCenterAdmin`；
- 所有资产元信息（提示词、参数、模型名、时间）仅在资产详情弹窗中完整呈现，列表页不展示参数细节；
- 若绑定 OSS 时选择“释放平台存储”，该资产将**立即从资产中心列表消失**，仅存在于 OSS 中，不可再通过控制台管理或 API 引用（除非重新上传）。此行为已在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 的“配置 OSS 转存”章节重点强调。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


