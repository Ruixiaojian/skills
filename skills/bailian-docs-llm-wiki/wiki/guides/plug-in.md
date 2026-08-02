# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如计算、搜索、图像生成等）以标准化方式接入，弥补大模型在实时信息获取、精确计算、多模态生成等方面的固有局限。开发者可选用官方插件、三方插件或自定义插件，按需增强应用功能。插件调用由大模型自主规划（智能体/Assistant API）或显式编排（工作流）驱动，无需修改模型本身。

## 支持的模型/功能

当前插件能力已在以下模型上验证可用：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的兼容性可能存在差异，**最新兼容性状态请以控制台实际执行结果为准** [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。  
插件按来源分为三类：
- **官方插件**：预置于组件广场，开箱即用，无需配置参数。包括 `code_interpreter`（Python执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub项目检索）等 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：覆盖商业服务、图像视频、教育等领域，经效果测试，开通后即可调用。
- **自定义插件**：支持开发者通过定义插件URL、工具路径、输入/输出参数及鉴权方式，集成任意HTTP API [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档1中称“官方插件无需配置输入和输出参数”，而文档3明确要求自定义插件必须完整配置入参/出参且“所有参数均为必填项”。该差异合理——官方插件已由平台预置完整Schema，自定义插件需用户自行定义，二者适用场景不同，无实质矛盾。

## 关键参数

- **工具ID**：唯一标识插件下的具体工具（如 `calculator`），API调用时必需。可通过插件详情页悬浮工具名称图标复制获取 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **插件URL**（自定义插件）：工具所在服务的根域名，如 `https://example.com`；工具路径（如 `/query`）将拼接其后构成完整请求地址 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **输入参数配置**：
  - `传参方式`：`大模型识别`（从用户Query中抽取）或 `业务透传`（由外部系统通过 `biz_params` 传入）；
  - `类型`：支持 `String`、`Number`、`Object` 等，`Object` 类型下子属性**不能为空**，需手动添加 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **鉴权配置**（自定义插件）：支持 `Header` 或 `Query` 方式，`Type` 可选 `basic`/`bearer`/`appcode`，Token 值需与API提供方一致。

## 使用方式

1. **权限准备**：主账号或RAM子账号首次使用插件前，需授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。RAM子账号需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（含特定 `Condition`）[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
2. **插件开通与授权**：
   - 官方插件：默认可用；子业务空间需单独授权 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
   - 三方插件：在插件市场购买/试用后开通。
   - 自定义插件：通过控制台创建或从云市场导入，完成调试并发布 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
3. **集成到应用**：
   - **智能体应用**：在编排页面的“MCP”区块添加插件（或MCP服务），最多支持10个工具 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
   - **工作流应用**：将插件作为独立节点拖入流程，按需配置输入输出。
   - **Assistant API**：在 `tools` 参数中声明工具列表，由模型自主触发调用 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。
4. **调用验证**：发布前务必通过控制台“测试工具”验证API连通性及参数解析准确性。

## 限制和注意事项

- **功能限制**：`code_interpreter` 插件**不支持网络访问及本地文件上传**，仅限沙箱内执行，依赖库版本固定（如 `requests~=2.31.0`、`pandas` 等）[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **搜索类插件能力边界**：`quark_search` 和 `github_search` 均**仅返回网页/项目标题、摘要、链接，不支持访问详情页内容** [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。
- **自定义插件发布强约束**：工具名称长度≤20字符；`Object` 类型参数必须定义子属性；GET请求不支持 `Object` 类型入参 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **安全与运维**：删除插件或工具将导致关联应用**立即失效且不可恢复**；修改插件URL或鉴权配置后，必须重新测试并发布工具 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


