# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如计算、搜索、图像生成等）以标准化方式接入，弥补大模型在实时信息获取、精确计算、多模态生成等方面的固有局限。开发者可直接选用官方/三方插件，或基于自有 API 创建自定义插件，所有插件均通过统一的工具调用协议与模型协同工作。插件能力需配合支持工具调用的模型及正确配置的权限方可生效。

## 支持的模型/功能

百炼插件功能仅在以下模型上可用，且需确保模型版本为最新稳定版（控制台实际执行结果为准）：

| 模型名称         | 模型标识符     |
|------------------|----------------|
| 通义千问-Turbo   | `qwen-turbo`   |
| 通义千问-Plus    | `qwen-plus`    |
| 通义千问-Max     | `qwen-max`     |
| 通义千问VL-Max   | `qwen-vl-max`  |
| 通义千问VL-Plus  | `qwen-vl-plus` |

插件按来源分为三类：
- **官方插件**：预置于组件广场，开箱即用，无需配置参数。包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）等。详情见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：来自阿里云云市场，覆盖商业服务、教育、音视频等领域，开通后即可调用，无需额外配置。
- **自定义插件**：开发者可自行创建，支持从零构建或从云市场导入 API，并完整定义工具路径、鉴权方式、输入/输出参数及高级调用示例。完整流程详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 3 中“插件效果示例”提到 calculator 插件输入参数为 `payload__input__text`，但该字段名未在文档 1 和文档 2 的任何工具配置界面或 API 文档中出现；实际调用时应以控制台调试器生成的请求体结构或 Assistant API `tools` 参数定义为准。此字段属于过时或内部实现细节，开发者不应硬编码依赖。

## 关键参数

插件调用依赖以下核心参数，其中部分由平台自动注入，部分需开发者显式配置：

- **工具 ID（`tool_id`）**：全局唯一标识符，用于在 API 请求中指定目标工具。例如 `calculator`、`code_interpreter`。获取方式见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **输入参数（`input_parameters`）**：
  - `传参方式` 决定参数来源：`大模型识别`（从用户 query 中抽取）、`业务透传`（由外部系统通过 `biz_params` 或 `user_defined_params` 注入）。
  - 类型支持 `String`、`Number`、`Boolean`、`Object`（Object 子属性**必须非空**，否则发布失败）。
- **鉴权配置**（仅自定义插件）：
  - `是否鉴权`：启用后需配置 `Header列表` 或 `Query参数`。
  - `鉴权类型`：支持 `basic`、`bearer`、`appcode`，决定 Authorization 头格式（如 `Bearer <TOKEN>`）。
- **高级配置（可选）**：提供 `Value` 字段填写典型用户输入与期望构造参数的映射示例（如 `"查询杭州明天天气" → {"city": "杭州", "date": "2025-04-25"}`），显著提升模型参数提取准确率。

## 使用方式

插件可通过三种方式集成到应用中：

1. **控制台集成（智能体应用）**：
   - 在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 页面，对官方/三方插件点击 **添加至智能体**，选择目标应用（注意：官方插件仅支持与**同业务空间**的应用关联）。
   - 对自定义插件，需先发布为 MCP 服务（点击插件卡片上的 **发布为MCP服务**），再进入智能体编排页，在 **MCP 区块** 中添加该服务。
   - 鉴权或业务透传参数需在对话前通过界面图标手动配置一次。

2. **工作流应用节点**：
   - 在工作流编排页，将插件作为独立节点拖入画布，按需配置输入参数与上下文依赖，执行逻辑由工作流引擎严格编排，**不由模型自主决策**。

3. **API 调用**：
   - 通过 [Assistant API](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api) 的 `tools` 字段传入工具定义（含 `tool_id`、`function` 描述等），模型返回 `tool_calls` 后，客户端需自行执行 HTTP 请求并回填 `tool_outputs`。
   - 若含业务透传或用户级鉴权参数，须通过 `biz_params` 字段传递（参考 [工作流与旧版智能体应用 API](https://help.aliyun.com/zh/model-studio/agent-and-workflow-application-api-reference)）。

## 限制和注意事项

- **权限前提**：首次使用插件（含官方、三方、自定义）**必须**授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。主账号可直接授权；RAM 子账号需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（策略条件中 `ram:ServiceName` 应为 `cloundapi-access.sfm.aliyuncs.com`）。详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **数量限制**：单个智能体应用最多关联 10 个工具（插件实例）。
- **网络与安全**：
  - `code_interpreter` 插件**禁止访问外网**、**禁止上传本地文件**，仅支持预装依赖（如 `pandas`, `matplotlib`, `requests~=2.31.0` 等）。
  - `quark_search` 和 `github_search` 均**仅返回网页标题、关键词、摘要**，不支持抓取或渲染网页正文。
- **发布要求**：自定义插件下的工具必须处于 **已发布** 且 **调试成功** 状态才可被调用；编辑后需重新测试并发布，否则变更不生效。
- **错误处理**：发布工具时常见错误如 `130040`（参数描述缺失）、`130022`（Object 子属性为空或 GET 方法误配 Object 入参），需按提示修正。详细错误码见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 来源文档

- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)
- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)


