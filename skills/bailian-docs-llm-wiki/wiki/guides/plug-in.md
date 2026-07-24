# plug in

[插件](../concepts/plugin.md)是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如计算、搜索、图像生成等 API）集成到模型推理流程中，弥补大模型在实时信息获取、精确计算、确定性执行等方面的固有局限。开发者可选用官方[插件](../concepts/plugin.md)、三方[插件](../concepts/plugin.md)或自定义插件，按需增强应用功能。插件调用由模型自主规划（智能体/Assistant API）或显式编排（工作流）驱动，无需修改模型本身。

## 支持的模型/功能

当前插件能力已在以下模型上验证可用：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的兼容性可能存在差异，**最新兼容性状态请以控制台实际执行结果为准** [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。  
插件功能分为三类：  
- **官方插件**：开箱即用，含 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）等，详见[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；  
- **三方插件**：覆盖商业服务、图像视频、教育等领域，需开通后使用；  
- **自定义插件**：支持通过控制台创建或从云市场导入，可对接任意符合规范的 HTTP API [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档1与文档2均列出 `quark_search` 插件说明，但文档2额外强调“夸克搜索和联网搜索（`enable_search`）的区别”——前者返回结构化搜索结果供模型直接引用，后者仅辅助内容生成且不返回原始结果。该差异在文档1中未体现，应以文档2为准。

## 关键参数

- **工具ID**：唯一标识插件下的具体工具（如 `calculator`），API 调用时必须传入，可通过插件详情页复制获取 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；  
- **输入参数**：配置时需明确 `参数名称`、`参数描述`、`类型`、`传参方式`（`大模型识别` 或 `业务透传`）。`大模型识别` 参数由模型从用户输入中抽取，`业务透传` 参数需通过 `biz_params` 显式传入；  
- **输出参数**：定义 API 返回数据中哪些字段会被模型提取并用于生成最终回复，所有出参均为必填项，嵌套层级应尽量扁平；  
- **鉴权配置**：自定义插件支持 Header 或 Query 方式鉴权，支持 `basic`/`bearer`/`appcode` 类型，[Token](../concepts/token.md) 需由 API 提供方发放 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 使用方式

1. **权限准备**：主账号或 RAM 子账号首次使用插件前，需授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。RAM 用户需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（策略条件中 `ram:ServiceName` 应为 `"cloundapi-access.sfm.aliyuncs.com"`）[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；  
2. **插件接入**：  
   - *官方/三方插件*：在插件市场页面单击 **添加至智能体**，选择目标智能体应用（官方插件需与应用同业务空间），最多支持添加 10 个工具；  
   - *自定义插件*：需先发布为 MCP 服务，再在智能体编排页的 **MCP 区块** 中添加；  
3. **调用触发**：  
   - 智能体应用/Assistant API：模型根据用户输入、工具名称及描述自主决定是否调用，调用后自动合并结果并生成回复；  
   - 工作流应用：将插件作为独立节点手动编排执行顺序；  
4. **调试与发布**：所有自定义工具必须完成在线测试（**测试工具**）并点击 **发布** 后方可被应用调用，草稿状态不可用 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 限制和注意事项

- **调用限制**：单个智能体应用最多关联 10 个工具；自定义插件的 `Object` 类型参数子属性不能为空，且 GET 请求不支持 `Object` 类型入参；  
- **能力边界**：`code_interpreter` 不支持网络访问及本地文件上传，依赖库版本固定（如 `matplotlib`、`pandas` 等）；`quark_search` 和 `github_search` 仅返回摘要、标题、链接，不支持访问网页或仓库详情；  
- **安全要求**：自定义插件 URL 必须为 HTTPS；若启用鉴权，需确保 [Token](../concepts/token.md) 安全传递，避免硬编码；  
- **错误处理**：发布工具失败常见原因包括参数描述缺失（错误码 130040）、Object 子属性为空（130022）等，需按提示修正 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)；  
- **计费说明**：官方插件中 `text_to_image` 和 `quark_search` 为限时免费且需申请开通，其余多数免费；三方插件按所选套餐计费。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


