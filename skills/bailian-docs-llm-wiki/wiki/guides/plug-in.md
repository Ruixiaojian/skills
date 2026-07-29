# plug in

[插件](../concepts/plugin.md)是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（API）集成到大模型应用中，弥补其在实时信息获取、精确计算、代码执行、图像生成等场景下的固有局限。[插件](../concepts/plugin.md)以“工具集合”形式组织，支持官方预置、三方市场及完全自定义三种类型，可被智能体、工作流或 Assistant API 主动调用或编排执行。所有[插件](../concepts/plugin.md)均需显式授权与配置后方可使用。

## 支持的模型/功能

当前插件能力仅在以下模型上可用：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max` 和 `qwen-vl-plus`。各模型对插件的兼容性存在差异，实际调用效果请以控制台运行结果为准 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。  
插件按来源分为三类：
- **官方插件**：组件广场预置，开箱即用，无需参数配置，包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）等 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：来自阿里云云市场，覆盖商业服务、教育、图像视频等领域，需开通后使用。
- **自定义插件**：用户自主创建或从云市场导入，支持完整 API 接入、鉴权（Header/Query，含 basic/bearer/appcode 类型）、输入输出参数定义及高级示例配置 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 与文档 2 均列出 `quark_search` 插件，但文档 2 明确指出其“目前支持检索出网页标题、关键词和摘要，但不支持直接访问网页详情”，而文档 1 仅简述为“查找公开的网络知识和信息”。应以文档 2 的限定说明为准，避免误判插件能力边界。

## 关键参数

- **工具 ID**：唯一标识插件下的具体工具（如 `calculator`），API 调用时必需。可通过插件详情页悬浮图标复制 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **插件 URL 与工具路径**：自定义插件中，`插件URL`（如 `https://example.com`）为域名根地址，`工具路径`（如 `/query`）为其相对路径，二者拼接构成完整调用地址 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **输入参数配置**：
  - `传参方式` 必须明确设为 `大模型识别`（从用户输入提取）或 `业务透传`（由外部传入，通过 `biz_params` 或 `user_defined_params`）；
  - `参数类型` 支持 Number/String/Object 等，Object 类型子属性**不能为空**，需手动添加 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **鉴权配置**：自定义插件可启用 Header 或 Query 鉴权，`Token` 值需按 `Type`（basic/bearer/appcode）格式注入请求头或 URL。

## 使用方式

1. **权限准备**：主账号或 RAM 子账号首次使用插件前，必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`；RAM 用户需额外授予 `ram:CreateServiceLinkedRole` 权限（策略条件中 `ram:ServiceName` 应为 `cloundapi-access.sfm.aliyuncs.com`）[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
2. **插件接入**：
   - 官方/三方插件：在插件市场页面单击“添加至智能体”，选择目标智能体应用（同一业务空间），最多支持 10 个工具 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
   - 自定义插件：需先发布为 MCP 服务，再于智能体编排页的“MCP”区块中添加 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)；
   - 工作流应用：将插件作为独立节点拖入流程，手动编排执行顺序；
   - Assistant API：在 `tools` 字段中声明工具列表，由模型自主决策调用时机与参数 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。
3. **调试与发布**：所有自定义工具必须通过“测试工具”验证连通性，并点击“发布”后才可在应用中生效；草稿状态工具不可调用。

## 限制和注意事项

- **调用限制**：智能体应用中最多添加 10 个工具；自定义插件的 `工具名称` 不得超过 20 字符 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **功能限制**：
  - `code_interpreter` 不支持网络访问与本地文件上传，依赖库版本固定（如 `requests~=2.31.0`、`pandas` 等）；
  - `quark_search` 和 `github_search` 均仅返回摘要信息，不支持访问原始网页或 GitHub 仓库详情页；
  - GET 请求方法下，输入参数**不支持 Object 类型**（错误码 130022）[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **安全与维护**：
  - 删除插件或工具将导致所有关联应用失效，且操作不可逆；
  - 修改插件 URL 或鉴权配置后，必须重新测试并发布所有下属工具；
  - 通过 API 调用含业务透传参数或用户级鉴权的插件时，必须通过 `biz_params` 传递对应值。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


