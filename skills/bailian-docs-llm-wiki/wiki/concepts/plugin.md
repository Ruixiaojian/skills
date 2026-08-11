# 插件

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如计算、搜索、图像生成、API 服务等）以标准化方式接入，弥补大模型在实时信息获取、精确计算、[多模态](multi-modal.md)生成和确定性执行等方面的固有局限。所有插件均通过智能体应用、工作流应用或 Assistant API 统一调度，由大模型自主规划调用（智能体/Assistant 模式）或显式编排调用（工作流模式）。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体应用（Agent）**：插件作为“可调用工具”被自动发现与触发。大模型基于用户指令和对话上下文，自主判断是否需要调用插件、调用哪个插件、传入哪些参数。例如：“帮我算一下 127 × 89 的结果”，模型会自动选择 `calculator` 插件并传参；“生成一张赛博朋克风格的猫”，则调用 `text_to_image` 插件。官方/三方插件可一键添加至智能体；自定义插件需先发布为 MCP 服务，再在智能体的“MCP”区块中启用。

- **工作流应用（Workflow）**：插件以独立节点形式显式编排。开发者拖入插件节点（如 `quark_search` 或自定义 MCP 工具），手动配置输入参数（可引用前置节点输出）、超时时间、错误处理逻辑，并连接上下游节点。适用于流程确定、步骤清晰的任务，如“先搜索最新政策 → 再提取关键条款 → 最后生成摘要”。

- **Assistant API / DashScope SDK 调用**：在 `tools` 字段中声明插件工具 ID 及其描述（`function.name` + `function.description` + `function.parameters`），平台自动注入工具调用能力。此时插件行为与智能体模式一致——由模型自主决策是否调用及如何调用。注意：纯千问 API（如 `dashscope.ChatCompletion.create`）**不支持插件调用**，必须通过百炼平台容器（智能体/工作流）或 Assistant API 接口。

- **与 Skill、MCP 的关系说明**：
  - **插件 ≠ Skill**：Skill 是面向文件/文档处理的语义化能力包（如 PDF OCR、Excel 表格解析），由 `SKILL.md` 驱动，无需参数配置，通过自然语言触发；插件是通用工具接口，强调结构化输入/输出与外部系统集成。
  - **插件 ≈ MCP 服务**：当前百炼平台中，“插件”在技术实现上已全面基于 **Model Context Protocol（MCP）** 协议。官方插件、三方插件、自定义插件均以 MCP 服务形态注册、发布和调用。MCP 是插件的底层通信标准，而“插件”是面向用户的功能抽象层。

## 关键参数和配置

- **工具 ID（`tool_id`）**：插件内具体工具的唯一标识符，API 调用和工作流节点配置时必需。可在控制台插件详情页的“插件工具”列表中复制。

- **输入参数（Input Schema）**：必须使用 JSON Schema 明确定义，包括参数名、类型（`string`/`number`/`object` 等）、是否必填、默认值。特别注意：
  - `object` 类型的子属性**不可为空**（即不能省略字段），否则发布失败；
  - 建议为复杂参数提供映射示例（如 `"查询杭州明天天气"` → `{"city": "杭州", "date": "2025-04-25"}`），显著提升模型参数提取准确率。

- **鉴权配置**：支持三种方式，均需与后端 API 严格一致：
  - `basic`：Base64 编码的 `username:password`；
  - `bearer`：[Token](token.md) 值（平台自动添加前缀 `Bearer `）；
  - `appcode`：阿里云 AppCode（常用于云市场 API）；
  - 传参位置可选 `Header`（推荐）或 `Query`。

- **高级配置（可选）**：
  - `enable_search`（布尔值）：仅适用于部分模型（如 `qwen-turbo`），开启后激活模型内置联网搜索增强，**与 `quark_search` 插件无关**——后者是独立工具调用，返回结构化结果；前者是模型内部能力，不暴露原始搜索内容。
  - `biz_params`（对象）：用于透传业务参数（如用户 ID、租户上下文）或动态鉴权 [Token](token.md)，需在 API 请求体中显式传入，不参与模型推理。

## 面向开发者，简洁实用

- ✅ **快速起步**：优先使用官方插件（如 `code_interpreter`, `calculator`, `text_to_image`），无需配置，控制台一键添加即可验证。
- ✅ **自定义开发**：  
  1. 将你的 HTTP 服务封装为符合 [MCP Streamable HTTP 协议](https://help.aliyun.com/zh/model-studio/user-guide/model-context-protocol-mcp) 的服务（端点 `/mcp`，POST 请求）；  
  2. 在控制台「MCP 广场」→「自定义服务」→「AI 网关导入」或「OpenAPI 导入」完成注册；  
  3. 发布后，在智能体或工作流中添加该 MCP 服务即可调用。
- ⚠️ **必做检查项**：  
  - 主账号或 RAM 子账号首次使用前，确保已授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`；  
  - 自定义插件必须通过「测试工具」验证成功并**发布**，编辑后需重新测试+发布才生效；  
  - 单个智能体最多关联 10 个插件工具；  
  - `code_interpreter` 插件沙箱**禁止外网访问和本地文件上传**，依赖库版本固定（如 `pandas`, `matplotlib`），请勿假设可安装新包。
- 🚫 **避坑提示**：  
  - 不要依赖文档静态列出的模型兼容性（如 `qwen-vl-plus` 支持插件），实际可用性以控制台运行结果为准；  
  - `quark_search` 和 `enable_search` 是两类完全不同的能力，切勿混用；  
  - 使用 `biz_params` 传递敏感信息（如 [Token](token.md)）时，务必通过 KMS 加密环境变量方式管理，避免硬编码。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [model context protocol](../guides/model-context-protocol.md)
- [skill](../guides/skill.md)
- [more](../api/more.md)
- [application call](../api/application-call.md)
- [managed agents api](../api/managed-agents-api.md)


