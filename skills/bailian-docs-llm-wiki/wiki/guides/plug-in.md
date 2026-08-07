# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）集成到智能体或工作流中，弥补大模型在实时信息获取、精确计算、代码执行、图像生成等方面的固有局限。插件以“工具”为最小可调用单元，支持官方预置、三方市场及完全自定义三种形态，开发者可根据业务需求灵活选用或组合。

## 支持的模型/功能

当前插件能力已覆盖通义千问全系列主流模型：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max` 和 `qwen-vl-plus`。各模型对插件的调用支持度一致，但实际兼容性请以控制台运行结果为准 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。  
插件功能按来源分为三类：
- **官方插件**：开箱即用，无需配置参数，包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）等；
- **三方插件**：来自阿里云云市场，覆盖商业服务、图像视频、教育等领域，需开通后使用；
- **自定义插件**：支持开发者接入任意 HTTP API，通过定义插件 URL、工具路径、输入/输出参数及鉴权方式实现深度定制 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 和文档 2 均列出 `quark_search` 插件说明，但文档 2 补充了关键对比：“夸克搜索插件”与“联网搜索（`enable_search`）”本质不同——前者直接返回结构化搜索结果供模型引用；后者仅作为辅助信息源，不保证结果显式返回或结构化呈现 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 关键参数

- **工具 ID**：唯一标识一个工具（如 `calculator`），API 调用时必须准确传递，可通过插件详情页悬浮图标复制 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
- **输入参数**：支持 `Number`、`String`、`Object` 等类型；`传参方式` 分为 `大模型识别`（从用户输入中抽取）和 `业务透传`（由外部系统主动注入，需通过 `biz_params` 传递）；
- **输出参数**：所有字段必填，定义越精简准确，模型对返回结果的解析与重组越可靠；
- **鉴权配置**：自定义插件支持 Header 或 Query 方式鉴权，`Type` 可选 `basic`/`bearer`/`appcode`，[Token](../concepts/token.md) 由 API 提供方发放；云市场导入插件自动携带 AppKey/AppSecret/AppCode。

## 使用方式

1. **权限准备**：首次使用前，主账号或 RAM 子账号需授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`，否则无法访问插件市场 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
2. **插件接入**：
   - *智能体应用*：在插件市场选择工具 → “添加至智能体”，最多支持 10 个工具；官方插件仅限同业务空间内关联；
   - *工作流应用*：将插件作为独立节点编排，由人工而非模型决策触发；
   - *Assistant API*：在请求 `tools` 字段中声明工具列表，模型自动规划调用逻辑；
3. **自定义插件发布流程**：创建插件 → 添加工具（配置路径、参数、鉴权）→ 在线调试 → 发布；发布后需转为 MCP 服务，再在智能体中添加 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 限制和注意事项

- 官方插件中，`code_interpreter` 不支持网络访问与本地文件上传，可用依赖版本固定（如 `requests~=2.31.0`、`pandas`、`matplotlib` 等）；
- `quark_search` 和 `github_search` 均仅返回摘要级结果（标题、关键词、链接、摘要），**不支持访问网页或仓库详情页**；
- 自定义插件的 `Object` 类型输入参数在 `GET` 请求下不被支持，且子属性不能为空，否则发布失败（错误码 `130022`）；
- 删除插件或工具将导致所有关联应用失效，操作不可逆；
- 三方插件开通后需手动授权至目标子业务空间，而默认业务空间无需额外授权。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


