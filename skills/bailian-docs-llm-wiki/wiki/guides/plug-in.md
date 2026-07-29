# plug in

插件是百炼平台用于扩展大模型能力的关键机制，通过集成外部工具（如计算器、搜索、代码执行等），弥补大模型在实时信息获取、精确计算、多模态生成等方面的固有局限。插件以工具（Tool）为最小单元，支持官方预置、三方认证及用户自定义三类来源，调用过程由模型自主规划或工作流显式编排。所有插件均需通过服务关联角色授权后方可使用。

## 支持的模型与功能

百炼当前支持以下模型调用插件：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的兼容性存在差异，**实际可用性请以控制台运行结果为准**，而非静态列表 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。  
插件功能分为三类：
- **官方插件**：开箱即用，无需配置参数，包括 `code_interpreter`（Python代码执行）、`calculator`（复杂数学计算）、`text_to_image`（文生图）、`quark_search`（实时网络搜索）、`generate_qrcode`（URL转二维码）、`github_search`（GitHub项目检索）；
- **三方插件**：覆盖商业服务、图像视频、教育等领域，需开通后使用，详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
- **自定义插件**：支持用户按 OpenAPI 规范定义并注册，实现业务专属能力集成。

> **注意**：文档 1 中称“官方插件无需配置输入输出参数”，而文档 2 在“Python代码解释器”小节明确列出其依赖库清单及网络/文件访问限制，表明**参数约束与运行环境限制实际存在，不可忽略**。开发者应以 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 中的运行时说明为准。

## 关键参数

插件调用的核心参数为 `tool_id`（如 `calculator`），用于标识具体工具。通过 API 调用时必须准确传递该 ID。  
工具输入参数由插件定义，例如：
- `calculator` 接收 `payload__input__text` 字段（如 `"12313x13232"`）；
- `quark_search` 接收查询文本，返回结构化摘要（标题、关键词、摘要），**不返回原始网页内容**；
- `code_interpreter` 仅支持指定依赖（如 `pandas`, `matplotlib`, `sympy`），且**禁止网络访问与本地文件上传**，详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 使用方式

插件可通过三种方式集成：
1. **智能体应用**：在插件市场页面选择工具 → “添加至智能体” → 绑定同业务空间内的智能体应用（最多 10 个工具）；
2. **工作流应用**：将插件作为独立节点拖入流程，由用户显式编排执行顺序，不依赖模型自动决策；
3. **Assistant API**：在请求体中传入 `tools` 数组（含 `tool_id` 和 `description`），模型根据 `user_message` 自主选择调用；详细用法见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

> **注意**：官方插件仅支持与**同一子业务空间**内的智能体关联；跨空间调用需先完成插件授权操作，具体步骤见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 限制和注意事项

- **权限前提**：首次使用插件前，主账号或 RAM 子账号必须授权 `AliyunServiceRoleForSFMAccessCloudAPI` 服务关联角色，否则无法访问插件市场；
- **RAM 子账号特殊处理**：子账号需额外授予 `ram:CreateServiceLinkedRole` 权限（含 `Condition` 限定 `cloundapi-access.sfm.aliyuncs.com`），否则授权失败（错误码 140052）；
- **组合调用**：支持单次请求中调用多个插件（如 `quark_search` + `text_to_image` + `generate_qrcode`），但需确保各工具语义可协同；
- **计费说明**：`code_interpreter`、`calculator`、`generate_qrcode`、`github_search` 免费；`text_to_image` 与 `quark_search` 为限时免费，需单独申请开通；
- **能力边界**：`quark_search` 仅返回摘要，不支持跳转原文；`github_search` 仅返回项目元信息（标题、链接、摘要），不支持克隆或读取代码库详情。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)


