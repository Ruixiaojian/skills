# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（API）集成到模型推理链路中，弥补其在实时信息获取、精确计算、代码执行、图像生成等领域的固有局限。插件以“工具集合”形式组织，支持官方预置、三方市场及完全自定义三种类型，可被智能体应用、工作流应用或 Assistant API 主动调用或编排触发。所有插件均需经服务关联角色授权后方可使用。

## 支持的模型/功能

百炼插件当前支持以下模型：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的兼容性存在差异，实际调用效果请以控制台运行结果为准。[插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md) 中明确列出了模型标识符与对应关系。

插件按来源分为三类：
- **官方插件**：组件广场预置，开箱即用，无需配置参数。包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）等。详细说明见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：覆盖商业服务、图像视频、教育等领域，需在插件市场开通后调用。
- **自定义插件**：用户自主创建或从云市场导入，支持完整 API 配置（URL、路径、鉴权、输入/输出参数）。完整流程详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档1与文档2对 `quark_search` 的能力描述一致（仅返回标题、关键词、摘要），但文档2额外强调其与 `enable_search` 的区别——后者为模型级联网增强，不直接返回搜索结果；而夸克搜索插件返回结构化文本结果供模型直接使用。开发者应根据需求选择插件调用或启用全局联网开关。

## 关键参数

- **工具ID**：唯一标识插件下的具体工具（如 `calculator`），API 调用时必须显式指定。可通过插件详情页悬浮图标复制获取（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。
- **输入参数**：需配置参数名、描述、类型、传参方式（`大模型识别` 或 `业务透传`）。`大模型识别` 表示由模型从用户输入中抽取值；`业务透传` 需通过 `biz_params` 或 `user_defined_params` 由外部传入。
- **鉴权配置**：自定义插件支持 Header 或 Query 方式鉴权，类型包括 `basic`、`bearer`、`appcode`。[Token](../concepts/token.md) 值需准确填写，否则调用失败。
- **高级配置（示例）**：为提升模型调用准确性，建议为复杂入参提供 `Value` 示例（如 `{"city": "杭州", "date": "2025-04-25"}`），该能力在 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 中有详细配置指引。

## 使用方式

插件可通过三种方式接入：
1. **控制台集成**：在插件市场页面单击“添加至智能体”，选择工具并绑定到同业务空间的智能体应用；或在工作流中作为独立节点拖入编排。注意：官方插件仅支持与**同业务空间**的智能体关联。
2. **MCP 服务模式**：自定义插件需先发布为 MCP 服务，再在智能体编排页的“MCP”区块中添加。用户级/服务级鉴权需在对话前通过 UI 配置 [Token](../concepts/token.md)（[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。
3. **API 调用**：通过 Assistant API 的 `tools` 字段声明可用工具列表，并在 `tool_choice` 中控制调用策略；工作流/旧版智能体应用则通过 `biz_params` 传递透传参数或鉴权信息（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。

> **注意**：文档1称插件可通过“智能体应用、工作流应用以及 Assistant API”调用，而文档3明确指出自定义插件需转为 MCP 服务后才能被智能体使用——二者逻辑一致，但文档1未强调“自定义插件需 MCP 转换”这一前提，易引发误解。实际开发中，自定义插件**必须发布为 MCP 服务**方可被智能体识别。

## 限制和注意事项

- **权限要求**：首次使用插件需主账号或具备 `ram:CreateServiceLinkedRole` 权限的 RAM 用户授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。
- **数量限制**：单个智能体应用最多添加 10 个工具。
- **安全限制**：`code_interpreter` 插件禁止网络访问与本地文件上传，仅支持预装依赖（如 pandas、matplotlib、requests 等）。
- **调试要求**：自定义插件的工具必须经“测试工具”验证成功并**发布**后才可调用；草稿状态工具不可用。
- **兼容性风险**：修改插件 URL 或鉴权配置后，需重新测试并发布所有关联工具，否则调用将失败。
- **删除影响**：删除插件或工具会导致已关联的应用失效，且操作不可逆（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


