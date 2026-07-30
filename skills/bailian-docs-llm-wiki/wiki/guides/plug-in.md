# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）封装为可被大模型识别和调度的标准化单元，弥补其在实时信息获取、精确计算、代码执行、图像生成等场景下的固有局限。插件支持官方预置、三方市场接入及完全自定义三种形态，开发者可根据业务需求灵活选用或组合调用。所有插件均需经授权、配置与发布后方可集成至智能体或工作流应用中。

## 支持的模型/功能

当前插件能力已在以下模型上验证可用：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的调用稳定性与响应质量可能存在差异，**最新兼容性状态请以控制台实际执行结果为准** [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

插件按来源分为三类：
- **官方插件**：开箱即用，无需参数配置，包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）等 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：覆盖商业服务、图像视频、教育等领域，需在云市场开通后调用，无需额外配置输入/输出参数。
- **自定义插件**：支持通过控制台创建或从云市场导入，可对接任意 HTTP API，需明确定义工具路径、鉴权方式、输入/输出参数及高级调用示例 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档1中称“官方插件无需配置输入和输出参数”，而文档3明确要求自定义插件必须完整配置输入/输出参数（含类型、描述、传参方式等），且强调“出参与入参一样，需要尽可能精简和准确描述”。该差异非矛盾，而是因官方插件已由平台预置完整 Schema，而自定义插件需开发者自行定义——二者适用不同配置范式。

## 关键参数

- **工具ID**：唯一标识一个工具（如 `calculator`），API 调用时必需。可在插件详情页的工具卡片上悬停并点击复制图标获取 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **插件URL**（仅自定义插件）：工具所在服务的根域名，如 `https://example.com`；工具路径（如 `/query`）将拼接于此 URL 后构成完整请求地址 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **鉴权配置**（可选）：支持 `Header` 或 `Query` 方式传递，鉴权类型包括 `basic`、`bearer`、`appcode`；[Token](../concepts/token.md) 值需由 API 提供方分配。
- **输入参数**：必须指定 `参数名称`、`参数描述`、`类型`（Number/String/Object 等）、`传参方式`（`大模型识别` 或 `业务透传`）。Object 类型下子属性**不能为空**，需手动添加 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **输出参数**：所有参数均为必填，用于指导大模型解析 API 返回结果并构造最终回复；嵌套层级应尽量扁平。

## 使用方式

插件可通过以下三种方式集成：
1. **控制台添加至智能体应用**：在插件市场找到目标插件 → 单击“添加至智能体” → 选择工具与目标智能体 → 确认添加 → 在对话框中测试 → 发布应用。*注意：官方插件仅支持与同业务空间内的智能体关联* [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
2. **工作流应用节点**：将插件作为独立节点拖入工作流画布，按编排逻辑执行，不依赖大模型自主决策 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。
3. **Assistant API 调用**：在 `tools` 字段中传入工具定义（含 `type`, `function.name`, `function.description`, `function.parameters`），并在 `tool_choice` 中指定调用策略（`auto`/`required`/具体工具名）[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

对于自定义插件，还需额外完成：
- 创建插件并配置 URL 与鉴权；
- 为每个工具设置路径、方法（GET/POST）、提交方式（`application/json` 等）；
- 配置输入/输出参数，并通过“测试工具”验证连通性；
- **发布工具后才可被调用**（草稿状态不可用）[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 限制和注意事项

- **权限前提**：首次使用插件前，主账号或 RAM 用户需授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`；RAM 用户需额外授予 `ram:CreateServiceLinkedRole` 权限 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **调用上限**：单个智能体应用最多支持添加 10 个工具 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **功能限制**：
  - `code_interpreter` 不支持网络访问与本地文件上传，依赖库版本固定（如 `requests~=2.31.0`, `pandas`, `matplotlib` 等）；
  - `quark_search` 和 `github_search` 仅返回网页/项目标题、关键词、摘要，**不支持直接抓取网页正文或项目代码详情** [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)；
  - `text_to_image` 和 `quark_search` 为限时免费，需单独申请开通。
- **调试与发布强约束**：自定义插件的工具必须“测试成功”且“已发布”才能生效；编辑后需重新测试并发布，否则调用失败 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **错误处理**：发布工具时常见错误码 `130040`（参数描述缺失）、`130022`（Object 子属性为空或 GET 请求误配 Object 参数）需按提示修正 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


