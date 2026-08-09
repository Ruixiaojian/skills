# 插件

插件是百炼平台用于扩展大模型能力的核心机制，通过标准化方式将外部工具（如代码执行、实时搜索、图像生成等）接入大模型工作流，弥补其在实时信息获取、精确计算、[多模态](multimodal.md)生成等方面的固有局限。

## 在百炼平台的不同场景中如何使用

插件在百炼平台中并非单一抽象，而是以三种互补形态落地，适用于不同开发需求与控制粒度：

- **官方/三方插件（Plugin）**：面向开箱即用场景，如 `code_interpreter`、`quark_search`、`text_to_image` 等。由平台预置或第三方发布，通过控制台「插件市场」一键添加至智能体应用；支持在 Assistant API 的 `tools` 字段中声明调用，由大模型自主决策触发（需模型支持，如 `qwen-max`、`qwen-vl-plus` 等）。  
- **MCP 服务（Model Context Protocol）**：作为标准化工具协议层，屏蔽底层实现差异。适用于需要统一接入多类异构服务（如地图、天气、网页抓取）的场景。MCP 服务必须通过智能体或工作流应用集成（**不可直接用于千问原始 API 调用**），支持自动决策调用（智能体）或显式编排调用（工作流节点）。  
- **Skill（可插拔能力包）**：面向文件处理、格式解析等任务型能力封装。不依赖特定模型，调用完全由 `SKILL.md` 中的 `description` 语义驱动，无需参数配置。适用于“用户说‘把PDF转成Excel’”这类自然语言触发的端到端任务，开发者只需上传符合规范的 ZIP 包即可扩展能力。

> ✅ 关键区别：  
> - **Plugin**：强模型耦合，依赖大模型理解参数结构，适合通用工具调用；  
> - **MCP**：协议标准化，支持复杂工具链与外部 IDE 集成，适合企业级工具治理；  
> - **Skill**：零参数、纯语义匹配，适合确定性任务封装，对模型无感知。

## 关键参数和配置

| 类别 | 参数 | 说明 | 开发提示 |
|------|------|------|----------|
| **通用标识** | `tool_id` / `name` | 工具唯一标识符（如 `calculator`、`invoice-parser`）。官方插件 ID 固定；自定义插件/Skill 需全局唯一，仅支持小写字母、数字、连字符。 | 控制台悬停复制，API 中必须严格一致。 |
| **输入控制** | `传参方式`（Plugin）<br>`description`（Skill） | Plugin：设为 `大模型识别`（自动抽取）或 `业务透传`（需 `biz_params` 传入）；<br>Skill：`description` 是唯一调度依据，必须明确输入类型、支持操作、触发词及**排除场景**。 | 模糊的 `description` 导致误触发；遗漏排除条件是 Skill 调试失败主因。 |
| **网络与鉴权** | `plugin_url` + `path`（Plugin）<br>`type` + `url`（MCP）<br>`DASHSCOPE_API_KEY`（MCP） | Plugin 自定义需拼接完整地址；MCP 必须匹配 `type`（`streamableHttp` → `/mcp`）；所有外部调用均需 `DASHSCOPE_API_KEY` 鉴权。 | MCP 配置错误常见报错：`11200058`（HTTP 405）、`11200049`（HTTP 401）。 |
| **安全约束** | `AliyunServiceRoleForSFMAccessCloudAPI`（Plugin/MCP）<br>`KMS 凭据`（MCP 敏感参数） | 首次使用插件/MCP 必须授权该服务关联角色；自定义工具的密钥（如 `AMAP_MAPS_API_KEY`）必须通过 KMS 加密存储。 | RAM 子账号需主账号授予 `ram:CreateServiceLinkedRole` 权限，否则报错 `140052`。 |

## 面向开发者：简洁实用指南

- **快速起步**：  
  1. 控制台 → [插件市场](https://bailian.console.aliyun.com/#/plugin-market) → 添加官方插件 → 绑定智能体；  
  2. 或使用 Assistant API：在 `tools` 数组中填入工具定义（如 `{"type": "function", "function": {"name": "calculator", ...}}`），确保模型支持且已授权角色。  

- **调试必查项**：  
  - ✅ 插件/MCP 是否已**发布成功**（草稿状态不可用）；  
  - ✅ `plugin_ids` 或 `tools` 是否在 API 请求/应用配置中**显式声明**；  
  - ✅ `biz_params` 是否正确传递透传参数（Plugin）；  
  - ✅ `description` 是否覆盖典型触发句式+明确排除干扰场景（Skill）；  
  - ✅ KMS 加密凭据是否已配置且未过期（MCP）。  

- **避坑提醒**：  
  - `code_interpreter` 禁止网络访问、文件上传、系统命令；  
  - `quark_search`/`github_search` 仅返回摘要，无法获取网页正文；  
  - 单个智能体最多添加 **10 个插件**，MCP 最多配置 **5 个服务**；  
  - 自定义插件/Skill 上传后需约 2 分钟审核，失败时按错误码修正（如 `130040` = `description` 缺失）。  

> 💡 提示：优先使用官方插件验证流程；复杂业务逻辑建议用 MCP 封装；高频文件处理任务首选 Skill —— 三者可共存于同一智能体，按需组合。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [skill](../guides/skill.md)
- [model context protocol](../guides/model-context-protocol.md)
- [application support](../guides/application-support.md)
- [managed agents](../guides/managed-agents.md)


