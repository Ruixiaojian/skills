# plug in

插件（Plug-in）是百炼平台扩展大模型能力的核心机制，支持通过官方插件、三方插件和自定义插件三种方式，为大模型注入联网搜索、代码执行、图像生成、API调用等外部能力。插件以工具（Tool）为最小可调用单元，通过标准化的输入/输出参数定义与大模型协同工作，适用于智能体应用、工作流及 Assistant API 等多种调用场景。所有插件均需完成服务关联角色授权后方可使用，详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 支持的模型/功能

- **适用模型**：插件能力与底层大模型解耦，所有百炼支持的模型（包括 Qwen 系列、第三方模型等）均可在启用插件后调用，无需模型侧适配。
- **功能类型**：
  - **官方插件**：开箱即用，无需配置参数，覆盖通用能力，如 `code_interpreter`（Python 执行）、`calculator`（高精度计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）。
  - **三方插件**：来自阿里云市场，经效果验证，涵盖商业服务、图像视频、教育等领域，开通后即可调用。
  - **自定义插件**：支持用户自主接入任意 HTTP API，通过定义插件 URL、工具路径、鉴权方式及结构化 I/O 参数实现深度定制，详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 中称“官方插件只能与位于相同的业务空间里的智能体应用关联”，而文档 2 在“使用插件”章节未限定业务空间约束，且明确支持通过 MCP 服务跨空间复用。实际行为以控制台最新逻辑为准——**官方插件在默认业务空间可直接使用；子业务空间需显式授权后方可调用**，该限制仍有效。

## 关键参数

| 参数类别 | 字段名 | 说明 | 示例 |
|----------|--------|------|------|
| **插件级** | `plugin_url` | 插件根域名，所有工具路径以此为基础拼接 | `https://myapi.example.com` |
| | `is_auth_required` / `auth_type` / `auth_location` / `auth_token` | 鉴权配置，支持 `bearer`/`basic`/`appcode` 类型，位置可选 `Header` 或 `Query` | `{"type": "bearer", "location": "Header", "token": "xxx"}` |
| **工具级** | `tool_path` | 相对路径，以 `/` 开头，与 `plugin_url` 拼接为完整 API 地址 | `/weather/query` |
| | `method` | HTTP 方法 | `GET` 或 `POST` |
| | `content_type` | 提交方式 | `application/json` 或 `application/x-www-form-urlencoded` |
| | `input_params` | 定义入参：`name`（如 `city`）、`description`（如“城市名称，中文”）、`type`（`String`/`Number`/`Object`）、`in`（`Body`/`Query`/`Header`）、`required`、`pass_through_mode`（`model_recognition` 或 `biz_pass_through`） | `{ "name": "city", "type": "String", "required": true }` |
| | `output_params` | 定义出参：`name`、`description`、`type`，用于指导模型解析响应并构造最终答案 | `{ "name": "temperature", "type": "Number", "description": "当前温度，单位摄氏度" }` |

> **注意**：文档 1 未提及 `Object` 类型参数的嵌套约束，而文档 2 明确强调：“**Object类型下的子属性不能为空**”，且需通过 UI 图标手动添加子属性；若忽略此规则将导致发布失败（错误码 `130022`）。开发者必须严格遵循此要求。

## 使用方式

1. **前置授权**：主账号或 RAM 子账号首次使用插件前，必须创建服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。RAM 用户需先由主账号授予 `ram:CreateServiceLinkedRole` 权限（策略条件中 `ram:ServiceName` 值应为 `cloundapi-access.sfm.aliyuncs.com`），否则无法完成授权 —— 此流程在 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 中均被强调。
2. **控制台集成**：
   - **官方/三方插件**：进入 [插件市场](https://bailian.console.aliyun.com/#/plugin-market)，点击“添加至智能体”，选择目标应用（最多 10 个工具），发布后生效。
   - **自定义插件**：创建并发布工具后，需先“发布为 MCP 服务”，再在智能体编排页的 **MCP 区块** 中添加该服务。
3. **API 调用**：
   - Assistant API：在 `tools` 数组中传入工具定义（含 `function.name`、`function.description`、`function.parameters`），并在 `tool_choice` 中指定策略。
   - 工作流/旧版智能体 API：通过 `biz_params` 传递业务透传参数或用户级鉴权 [Token](../concepts/token.md)。

## 限制和注意事项

- **权限限制**：RAM 用户无默认创建服务关联角色权限，必须由主账号预先授予 `ram:CreateServiceLinkedRole` 权限（策略条件 `ram:ServiceName` 必须精确匹配 `cloundapi-access.sfm.aliyuncs.com`），否则所有插件入口（市场、导入、MCP 发布）均会失败。
- **功能限制**：
  - `code_interpreter` 不支持网络访问、本地文件上传，依赖库版本固定（见文档 1 列表）。
  - `quark_search` 和 `github_search` 仅返回网页/项目摘要、标题、链接，**不支持访问原始网页内容或 GitHub 仓库详情页**。
  - 自定义插件的 `Object` 类型入参在 `GET` 请求下不被支持（错误码 `130022`）。
- **发布约束**：
  - 工具名称长度 ≤ 20 字符（超长将红色提示 `22/20`）。
  - 所有输入/输出参数的 `description` 字段为必填（缺失触发错误码 `130040`）。
- **安全提醒**：开启 `biz_pass_through` 模式时，外部调用方需确保 `biz_params` 内容可信；用户级鉴权 [Token](../concepts/token.md) 应通过安全渠道传入，避免硬编码。

## 来源文档

- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


