# plug in

[插件](../concepts/plugin.md)是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如计算、搜索、图像生成等 API）以标准化方式接入，弥补大模型在实时信息获取、精确计算、[多模态](../concepts/multi-modal.md)生成等方面的固有局限。开发者可直接调用官方/三方[插件](../concepts/plugin.md)，或基于业务需求创建自定义[插件](../concepts/plugin.md)，所有插件均通过智能体应用、工作流应用或 Assistant API 统一调度。插件调用由大模型自主规划（智能体/Assistant 模式）或显式编排（工作流模式）。

## 支持的模型/功能

百炼插件当前支持以下模型：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的兼容性存在差异，**实际可用性请以控制台运行结果为准**，不建议依赖文档静态列表做兼容性断言 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

插件按来源分为三类：
- **官方插件**：预置于组件广场，开箱即用，无需配置参数。包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）等 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：覆盖商业服务、图像视频、教育等领域，需在云市场开通后调用。
- **自定义插件**：支持开发者导入云市场 API 或完全自建 HTTP 服务，通过定义插件 URL、工具路径、输入/输出参数及鉴权方式实现深度集成 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 和文档 2 均列出 `quark_search` 插件说明，但文档 2 明确指出“夸克搜索和联网搜索（`enable_search`）有本质区别”，而文档 1 未提及 `enable_search`。实际开发中应以文档 2 的区分逻辑为准：`quark_search` 是独立工具调用，返回结构化搜索结果；`enable_search` 是模型内部增强机制，不暴露原始搜索内容。

## 关键参数

- **工具 ID（`tool_id`）**：唯一标识插件下的具体工具，API 调用时必需。可在插件详情页的“插件工具”区域或工具名称旁的图标处复制 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **输入参数**：需明确定义参数名、类型（String/Number/Object 等）、传参方式（`大模型识别` 或 `业务透传`）。Object 类型子属性**不能为空**，否则发布失败 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **鉴权配置**：支持 Header 或 Query 方式，鉴权类型包括 `basic`、`bearer`、`appcode`。[Token](../concepts/token.md) 需与 API 提供方一致，且 `bearer` 类型会自动添加前缀 `Bearer ` [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **高级配置（示例）**：为提升大模型参数提取准确率，可配置用户 Query 与期望入参的映射示例（如 `"查询杭州明天的天气"` → `{"city": "杭州", "date": "2025-04-25"}`），尤其适用于复杂 Object 参数场景 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 使用方式

1. **权限准备**：主账号或 RAM 子账号首次使用插件前，必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。RAM 用户需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（策略中 `ram:ServiceName` 必须为 `cloundapi-access.sfm.aliyuncs.com`）[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
2. **插件接入**：
   - **官方/三方插件**：在插件市场页面单击“添加至智能体”，选择工具并绑定到同业务空间的智能体应用；或在工作流中作为节点手动添加。
   - **自定义插件**：需先发布为 MCP 服务，再在智能体应用的“MCP”区块中添加；若含 `业务透传` 参数或用户级鉴权，需通过对话前的 `biz_params` 配置传入 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
3. **API 调用**：通过 Assistant API 时，在 `tools` 字段中声明工具 ID 及描述；通过 DashScope SDK 或 HTTP 接口时，`biz_params` 用于传递透传参数或鉴权 [Token](../concepts/token.md) [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 限制和注意事项

- **数量限制**：单个智能体应用最多关联 10 个工具 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **网络与文件限制**：`code_interpreter` 插件**不支持对外网络访问及本地文件上传**，仅限沙箱内执行，依赖库版本固定（如 `requests~=2.31.0`, `pandas`, `matplotlib` 等）[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件开通**：需在云市场完成购买/试用，开通后状态显示为“已开通”，方可调用 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **自定义插件调试**：工具必须经“测试工具”验证成功并**发布**后才可被应用调用；编辑后需重新测试+发布，否则变更不生效 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **删除风险**：删除插件或工具会导致所有关联应用失效，且操作不可逆 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


