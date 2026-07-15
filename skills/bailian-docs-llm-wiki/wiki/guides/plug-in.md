# plug in

[插件](../concepts/plugin.md)是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（API）集成到推理链路中，弥补大模型在实时信息获取、精确计算、代码执行、图像生成等方面的固有局限。[插件](../concepts/plugin.md)以“工具”为最小可调用单元，支持官方预置、三方市场及完全自定义三种来源，由大模型根据用户输入自主规划调用，或在工作流中显式编排执行。

## 支持的模型/功能

当前[插件](../concepts/plugin.md)能力仅对部分模型开放，**必须使用以下模型标识符之一**才能启用插件调用：

- `qwen-turbo`（通义千问-Turbo）  
- `qwen-plus`（通义千问-Plus）  
- `qwen-max`（通义千问-Max）  
- `qwen-vl-max`（通义千问VL-Max）  
- `qwen-vl-plus`（通义千问VL-Plus）  

> **注意**：文档 1 中称“各模型对插件的兼容性可能有差异”，但未明确列出不支持的模型；而文档 2 和 3 均未重复说明兼容性范围。实际开发中请以控制台运行结果为准，建议优先选用 `qwen-plus` 或 `qwen-max` 进行插件集成验证。该兼容性说明详见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

插件按来源分为三类，功能边界如下：

- **官方插件**：开箱即用，无需配置参数。包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）等。详细功能与限制见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：来自阿里云云市场，覆盖商业服务、教育、图像视频等领域，需开通后使用，同样免配置。
- **自定义插件**：支持通过控制台创建或从云市场导入，可对接任意 HTTP API。需明确定义工具路径、鉴权方式、输入/输出参数结构，并完成调试与发布。完整流程参见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 关键参数

插件调用依赖以下核心参数，尤其在 API 集成场景中必须准确传递：

- **工具 ID（tool_id）**：唯一标识一个工具，如 `calculator`、`quark_search`。可在插件详情页的“插件工具”区域直接复制，[获取工具ID](../../raw/application-user-guide/plug-in/plugins.md) 有详细指引。
- **输入参数（input parameters）**：
  - `传参方式` 必须明确设为 `大模型识别`（由 LLM 从用户 query 中抽取）或 `业务透传`（由上游系统主动注入，通过 `biz_params` 传递）；
  - 参数类型（String/Number/Object）及嵌套结构需严格匹配 API 接口契约，Object 类型子属性**不能为空**（见文档 3 错误码 130022）；
  - 鉴权参数（如 `api_key`）若置于 Query，需在插件配置中指定 `参数名`；若置于 Header，则 `Type`（如 `bearer`）决定前缀格式。
- **输出参数（output parameters）**：所有字段均为必填，描述需精简准确，便于大模型从 API 响应中提取关键字段并组织最终回复。

## 使用方式

插件可通过三种方式接入应用：

1. **智能体应用（Agent）**：在控制台应用编排页 → “MCP” 区块 → 添加已发布的插件（或其转换的 MCP 服务）。官方插件仅支持与**同业务空间**内的智能体关联；自定义插件需先发布为 MCP 服务。详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 的“调用插件”章节。
2. **工作流应用（Workflow）**：将插件作为独立节点拖入画布，显式编排执行顺序，不依赖大模型自动决策。
3. **Assistant API**：在请求 payload 的 `tools` 字段中声明工具列表（含 `type`、`function` 及 `function.name`），并在 `tool_choice` 中控制调用策略。具体格式参考 [Assistant API 文档](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api) 中 `tools` 关键字说明。

> **注意**：首次使用插件前，主账号或 RAM 子账号**必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`**，否则无法访问插件市场或调用云市场 API。RAM 用户需额外授予 `ram:CreateServiceLinkedRole` 权限，操作细节见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 限制和注意事项

- **调用上限**：单次对话最多调用 10 个工具（含同一插件下的多个工具），且工具总调用次数受应用配额约束。
- **安全限制**：
  - `code_interpreter` 插件**禁止网络访问**（`requests` 等库不可用）及**本地文件上传**，仅支持内置依赖（如 `pandas`, `matplotlib`, `sympy`）；
  - `quark_search` 和 `github_search` 仅返回网页标题、关键词/摘要、项目链接等元信息，**不支持抓取网页正文或项目源码**（见文档 1 和 2 的明确说明）。
- **自定义插件部署要求**：
  - 插件 URL 必须为 HTTPS 协议，且响应头需包含 `Access-Control-Allow-Origin: *` 或明确允许百炼域名；
  - 工具路径必须以 `/` 开头，且拼接后构成合法 URL（如插件 URL `https://example.com` + 工具路径 `/query` → `https://example.com/query`）；
  - 发布前必须通过在线调试验证连通性，未发布状态的工具无法被应用调用。
- **权限与生命周期**：删除插件将**级联删除其下所有工具**，且已关联该插件的应用立即失效；编辑插件 URL 或鉴权配置后，必须重新测试并发布所有相关工具。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


