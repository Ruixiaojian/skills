# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）以标准化方式接入，弥补大模型在实时信息获取、精确计算、代码执行、图像生成等方面的固有局限。开发者可选用官方插件、三方插件或自定义插件，在智能体应用、工作流应用或 Assistant API 中按需调用。插件调用由大模型自主规划（智能体/Assistant 模式）或显式编排（工作流模式）驱动。

## 支持的模型与功能

百炼当前支持以下模型调用插件：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的实际兼容性可能存在差异，[插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)明确指出“最新的兼容性状态，请以控制台实际执行结果为准”。

官方插件提供开箱即用能力，包括：
- `code_interpreter`：执行 Python 代码（支持 matplotlib、pandas、sympy 等依赖，**不支持网络访问与本地文件上传**）  
- `calculator`：复杂数学运算  
- `text_to_image`：文生图（限时免费，需申请开通）  
- `quark_search`：实时网络搜索（返回标题、关键词、摘要，**不支持直接访问网页详情**）  
- `generate_qrcode`：URL 转二维码  
- `github_search`：GitHub 项目检索（返回标题、链接、摘要，**不支持访问项目详情**）  

三方插件覆盖商业服务、图像视频、教育等场景，需在云市场开通后使用；自定义插件支持通过 REST API 接入任意业务系统，详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 文档。

> **注意**：文档 1 和文档 2 均列出 `quark_search` 插件限制为“不支持直接访问网页详情”，但文档 2 在“常见问题”中额外说明“联网搜索（`enable_search`）也是基于夸克搜索”，暗示二者底层一致而行为不同——`enable_search` 是模型级增强策略，非插件调用，不可混用。实际开发中应严格区分插件调用与模型配置开关。

## 关键参数

- **工具 ID**：唯一标识插件下的具体工具（如 `calculator`），API 调用时必需。可通过插件详情页悬浮图标复制，见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。  
- **输入参数**：需明确定义名称、类型、描述及传参方式（`大模型识别` 或 `业务透传`）。`大模型识别` 参数由模型从用户输入中抽取；`业务透传` 参数需通过 `biz_params` 或 `user_defined_params` 显式传入。  
- **鉴权配置**：自定义插件支持 Header 或 Query 方式鉴权，支持 `basic`/`bearer`/`appcode` 类型。[Token](../concepts/token.md) 需按规范拼接（如 `Bearer <TOKEN>`），且 RAM 子账号需提前授予 `ram:CreateServiceLinkedRole` 权限方可完成授权，该要求在 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 和 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 中一致强调。  
- **高级配置（示例）**：对复杂入参，建议配置 `Value` 字段提供调用样例（如 `{"city": "杭州", "date": "2025-04-25"}`），显著提升模型参数构造准确率。

## 使用方式

1. **权限准备**：主账号或 RAM 子账号首次使用插件前，必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。RAM 子账号需主账号预先授予 `ram:CreateServiceLinkedRole` 权限，否则授权失败（详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。  
2. **插件接入**：  
   - *官方/三方插件*：在插件市场页面单击“添加至智能体”，选择目标智能体应用（**官方插件仅支持同业务空间内关联**），最多添加 10 个工具。  
   - *自定义插件*：需先创建插件 → 添加并调试工具 → 发布工具 → **发布为 MCP 服务** → 在智能体编排页的“MCP”区块中添加该服务。  
3. **调用入口**：  
   - 智能体应用：模型根据用户输入、工具名及描述自动决策是否调用；  
   - 工作流应用：插件作为独立节点手动编排；  
   - Assistant API：在 `tools` 参数中声明工具列表，由 SDK 自动处理调用循环。  

## 限制和注意事项

- **业务空间隔离**：官方插件仅能与**同一子业务空间**内的智能体应用关联，跨空间需重新授权（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。  
- **工具数量上限**：单个智能体应用最多绑定 10 个插件工具。  
- **自定义插件调试要求**：所有工具必须“测试成功”且“已发布”状态才可调用；Object 类型参数的子属性**不能为空**，否则发布失败（错误码 `130022`）。  
- **安全限制**：`code_interpreter` 插件明确禁止网络访问与本地文件上传，依赖列表以文档 2 为准。  
- **RAM 子账号权限**：创建服务关联角色权限（`ram:CreateServiceLinkedRole`）是使用插件的前置硬性条件，未授权将无法进入插件市场或导入云市场 API。  
- **计费提示**：`text_to_image` 和 `quark_search` 为“限时免费，需申请开通”，开通状态需在控制台确认，非默认可用。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


