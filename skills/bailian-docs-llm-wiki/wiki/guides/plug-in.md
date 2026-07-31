# plug in

插件是百炼平台扩展大模型能力的核心机制，通过将外部工具（如代码执行、网络搜索、图像生成等）以标准化方式接入，弥补大模型在实时信息获取、精确计算、多模态输出等方面的固有局限。开发者可直接调用官方插件、开通三方插件，或创建自定义插件，实现任务自动化与能力增强。所有插件均需通过服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI` 授权访问云资源，主账号与RAM用户权限配置存在差异。

## 支持的模型/功能

百炼插件支持以下模型调用（兼容性以控制台实际执行为准）：  
- `qwen-turbo`、`qwen-plus`、`qwen-max`（文本模型）  
- `qwen-vl-max`、`qwen-vl-plus`（多模态模型）  

> **注意**：文档 2 中列出的 `qwen-vl-plus` 在文档 1 的插件说明示例中未体现其对 `text_to_image` 等视觉类插件的特殊适配逻辑，实际使用时请以 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md) 中的模型列表为基准，并在控制台验证调用效果。

官方插件提供开箱即用能力，无需配置参数：
- `code_interpreter`：执行 Python 代码（支持 pandas、matplotlib、sympy 等依赖，[原文标题](../../raw/application-user-guide/plug-in/plugins.md)）
- `calculator`：高精度数学计算
- `text_to_image`：文生图（限时免费，需申请开通）
- `quark_search`：实时网络搜索（返回标题、关键词、摘要，不支持网页详情访问）
- `generate_qrcode`：URL 转二维码
- `github_search`：GitHub 项目检索（返回标题、链接、摘要，不支持项目详情）

三方插件覆盖商业服务、图像视频、教育等领域，需在插件市场开通后使用；自定义插件支持通过 API 接入任意业务系统，详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 关键参数

插件调用依赖以下核心参数：

- **工具 ID（tool_id）**：唯一标识插件下的具体工具（如 `calculator`），API 调用时必需。可通过插件详情页的“插件工具”区域或悬浮图标复制获取。
- **输入参数（input parameters）**：
  - `传参方式`：`大模型识别`（从用户输入中抽取）或 `业务透传`（由外部传入，需通过 `biz_params` 或 `user_defined_params` 传递）；
  - `类型`：支持 `String`、`Number`、`Object`（子属性必填，否则发布失败）；
  - `参数描述`：必须填写，用于引导大模型准确提取值（缺失将导致错误码 `130040`）。
- **鉴权配置**（自定义插件）：
  - `是否鉴权`：启用后需配置 `Header` 或 `Query` 位置、`Type`（`basic`/`bearer`/`appcode`）及 `Token`；
  - `服务级鉴权` 使用固定 [Token](../concepts/token.md)；`用户级鉴权` 需每次对话前手动配置 [Token](../concepts/token.md)（控制台通过 ![icon](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1891396371/p905403.png) 输入）。

## 使用方式

插件可通过三种方式集成：

1. **控制台集成（智能体应用）**：
   - 官方/三方插件：在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 页面单击 **添加至智能体**，选择目标智能体（注意：官方插件仅支持与同业务空间的智能体关联）；
   - 自定义插件：需先发布为 MCP 服务（插件卡片 → **发布为MCP服务**），再在智能体编排页的 **MCP 区块** 中添加；
   - 最多支持单个智能体关联 10 个工具。

2. **工作流应用**：
   - 将插件作为独立节点拖入画布，按流程编排执行顺序，不依赖大模型自主决策（[原文标题](../../raw/application-user-guide/plug-in/plug-in-overview.md)）。

3. **API 调用**：
   - Assistant API：在请求 `tools` 字段中声明工具 ID 及描述，模型自动规划调用；
   - 工作流/旧版智能体 API：通过 `biz_params` 透传鉴权信息或业务参数（[原文标题](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。

## 限制和注意事项

- **权限限制**：主账号可直接授权 `AliyunServiceRoleForSFMAccessCloudAPI`；RAM 用户需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（策略条件中 `ram:ServiceName` 必须为 `cloundapi-access.sfm.aliyuncs.com`），否则无法进入插件页面或导入云市场插件。
- **功能限制**：
  - `code_interpreter` 禁止网络访问与本地文件上传；
  - `quark_search` 和 `github_search` 均仅返回摘要信息，不支持跳转或解析原始网页/仓库内容；
  - GET 请求不支持 `Object` 类型输入参数（否则触发错误码 `130022`）；
  - 自定义插件工具名称长度上限为 20 字符（超长将阻断发布）。
- **调试与发布**：所有自定义工具必须完成 **在线调试成功** 并 **发布** 后才可在应用中调用；草稿状态工具不可用。
- **兼容性风险**：模型对插件的调用成功率受工具描述准确性、输入参数设计质量影响显著，建议在高级配置中添加调用示例以降低漏召/误召率。

## 来源文档

- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


