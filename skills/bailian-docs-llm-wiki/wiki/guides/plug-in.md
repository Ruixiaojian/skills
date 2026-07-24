# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（API）集成到推理链路中，弥补大模型在实时信息获取、精确计算、代码执行、图像生成等场景下的固有局限。插件以“工具集合”形式组织，支持官方预置、三方市场及完全自定义三类来源，由大模型自主规划调用或在工作流中显式编排。其设计目标是提升任务完成准确率与实用性，而非替代模型本身。

## 支持的模型/功能

当前插件能力已覆盖以下通义千问系列模型：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的兼容性存在差异，**实际可用性请以控制台运行结果为准**，不建议依赖文档静态列表做兼容性判断 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

插件按来源分为三类：
- **官方插件**：开箱即用，无需配置参数。包括 `code_interpreter`（Python执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub项目检索）等 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：来自阿里云云市场，覆盖商业服务、教育、音视频等领域，需开通后使用。
- **自定义插件**：用户通过定义插件URL、工具路径、输入/输出参数及鉴权方式，将自有API接入。支持从云市场导入或手动创建，完整流程见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档1与文档2均列出 `quark_search` 插件说明，但文档2额外强调其“目前支持检索出网页标题、关键词和摘要，但不支持直接访问网页详情”，而文档1仅简述为“不支持直接访问网页详情”。此处以文档2的表述为准，因其更具体且与常见问题部分一致。

## 关键参数

插件调用依赖两类核心参数：

- **工具ID（tool_id）**：唯一标识一个工具，如 `calculator`、`text_to_image`。必须在API请求或应用配置中显式指定，可通过插件详情页悬浮图标复制 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **输入参数（input parameters）**：由大模型从用户输入中提取（传参方式设为“大模型识别”）或由业务系统透传（设为“业务透传”，通过 `biz_params` 传递）。参数需明确定义名称、类型、描述及是否必填；Object类型参数的子属性**不能为空**，否则发布失败 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

此外，自定义插件需配置：
- **插件URL**：工具所在服务的根域名（如 `https://example.com`）；
- **工具路径**：相对于插件URL的路径（如 `/query`），拼接后构成完整API地址；
- **鉴权配置**：支持 Header 或 Query 方式，Type 可选 `basic`/`bearer`/`appcode`，[Token](../concepts/token.md) 由API提供方发放。

## 使用方式

插件可通过三种方式集成：

1. **智能体应用（Agent）**：在控制台插件市场中选择工具 → “添加至智能体”，或在智能体编排页面通过MCP区块引入。官方插件仅支持与**同业务空间**内的智能体关联 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
2. **工作流应用（Workflow）**：将插件作为独立节点拖入画布，按需编排执行顺序，不依赖大模型自主决策。
3. **Assistant API**：在 `tools` 字段中声明工具列表（含 `tool_id` 和 `description`），并在 `messages` 中触发调用。详细格式参考 Assistant API 文档中的 `tools` 关键字说明 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

> **注意**：自定义插件必须先发布为MCP服务，再通过MCP区块添加至智能体；直接添加插件卡片的方式仅适用于官方及三方插件 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 限制和注意事项

- **权限要求**：首次使用插件需授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。主账号可直接授权；RAM子账号需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（含特定 `Condition` 约束），否则授权失败 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **数量限制**：单个智能体应用最多支持添加10个工具 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **安全限制**：`code_interpreter` 插件**禁止网络访问与本地文件上传**，仅支持预装依赖（如 `pandas`, `matplotlib`, `requests` 等）[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **调试要求**：自定义插件的工具必须经在线调试成功并**发布**后才可调用；草稿状态或调试失败的工具无法生效 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **错误处理**：发布自定义工具时常见错误包括参数描述缺失（错误码 `130040`）或 Object 类型子属性为空（错误码 `130022`），需按提示补全 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


