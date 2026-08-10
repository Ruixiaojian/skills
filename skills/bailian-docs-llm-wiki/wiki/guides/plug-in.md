# plug in

插件是百炼平台扩展大模型能力的核心机制，通过将外部工具（如代码执行、实时搜索、图像生成等）以标准化方式接入，弥补大模型在计算精度、时效性、[多模态](../concepts/multi-modal.md)输出等方面的固有局限。开发者可直接使用官方插件、开通三方插件，或基于自有 API 创建自定义插件。所有插件均需通过服务关联角色授权后方可调用，且最终由大模型根据输入语义自主决策是否触发。

## 支持的模型/功能

百炼当前支持插件调用的模型包括：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max` 和 `qwen-vl-plus`。各模型对插件的兼容性以控制台实际执行结果为准，[插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md) 文档明确指出“最新的兼容性状态，请以控制台实际执行结果为准”。

插件按来源分为三类：
- **官方插件**：预置于组件广场，开箱即用，无需配置参数。包括 `code_interpreter`（Python 代码执行）、`calculator`（高精度计算）、`text_to_image`（文生图）、`quark_search`（实时网页搜索）、`generate_qrcode`（URL 转二维码）、`github_search`（GitHub 项目检索）。
- **三方插件**：来自阿里云云市场，覆盖商业服务、图像视频、教育等场景，开通后即可调用，详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **自定义插件**：支持开发者导入云市场 API 或自行开发 HTTP 接口，通过定义插件 URL、工具路径、输入/输出参数完成集成，完整流程见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 与文档 2 均列出 `quark_search` 插件说明，但文档 1 明确标注“不支持直接访问网页详情”，而文档 2 仅复述该描述，未新增限制；二者一致，无矛盾。但文档 1 中“夸克搜索和联网搜索（enable_search）有什么区别？”一节指出“联网搜索（enable_search）也是基于夸克搜索”，该表述与当前插件架构中 `enable_search` 作为独立开关（非插件）的实现存在潜在歧义，实际使用中应以控制台启用插件而非设置 `enable_search` 参数为准。

## 关键参数

- **工具 ID（tool_id）**：唯一标识插件下的具体工具，API 调用时必需。可在插件详情页的“插件工具”区域或工具名称旁悬浮图标处复制获取。
- **输入参数（input parameters）**：
  - `传参方式` 必须明确设为 `大模型识别`（从用户输入提取）或 `业务透传`（由外部 SDK/HTTP 请求透传）；
  - `参数类型` 支持 `String`、`Number`、`Object` 等，`Object` 类型下子属性**不能为空**，需手动添加；
  - `参数描述` 需自然语言撰写，直接影响大模型参数提取准确率。
- **鉴权配置**（自定义插件）：
  - 支持 `Header` 或 `Query` 位置；
  - `Type` 可选 `basic` / `bearer` / `appcode`，决定 Authorization 字段前缀；
  - `Token` 为服务级鉴权凭证，用户级鉴权需通过 `biz_params` 在 API 调用时动态传入。
- **高级配置（可选）**：提供 `Value` 示例（如 `{"city": "杭州", "date": "2025-04-25"}`），显著提升复杂参数场景下的召回准确率。

## 使用方式

插件可通过三种方式集成：
1. **控制台智能体应用**：在插件市场页面单击“添加至智能体”，选择目标智能体；或在智能体编排页的 **MCP 区块** 添加已发布的 MCP 服务（自定义插件需先发布为 MCP）。
2. **工作流应用**：将插件作为独立节点拖入画布，按编排逻辑执行，不依赖大模型自主规划。
3. **Assistant API**：在请求 `tools` 数组中传入工具定义（含 `tool_id`、`description`、`parameters`），由 SDK 自动处理调用与结果注入。具体格式参考 [Assistant API 文档](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api) 中 `tools` 关键字章节。

> **注意**：官方插件在**默认业务空间**内可直接调用；若在**子业务空间**使用，必须先在插件详情页完成空间级授权——此要求在 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 中明确强调，遗漏将导致调用失败。

## 限制和注意事项

- **权限前提**：主账号或 RAM 子账号首次使用插件前，必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。RAM 用户需额外授予 `ram:CreateServiceLinkedRole` 权限（策略脚本见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)），否则授权失败。
- **调用上限**：单个智能体应用最多关联 **10 个工具**（含不同插件下的工具）。
- **功能边界**：
  - `code_interpreter` 不支持网络访问与本地文件上传，依赖库版本固定（如 `pandas`、`matplotlib` 等）；
  - `quark_search` 与 `github_search` 仅返回网页/项目标题、关键词、摘要，**不支持抓取正文或仓库代码内容**；
  - `text_to_image` 为限时免费，需单独申请开通。
- **自定义插件发布要求**：工具必须处于 **已发布** 且 **调试成功** 状态；编辑后需重新测试并发布才生效；删除插件将导致所有关联应用失效，操作不可逆。
- **错误处理**：发布工具常见错误码如 `130040`（参数描述缺失）、`130022`（Object 子属性为空或 GET 请求误配 Object 参数），需按 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 中错误码表逐一修复。

## 来源文档

- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


