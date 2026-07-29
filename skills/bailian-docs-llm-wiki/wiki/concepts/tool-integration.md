# 工具集成

工具集成是百炼平台中将外部能力（如 API、脚本、服务）安全、标准化地接入大模型推理流程的核心机制，使模型能按需调用真实世界功能（如搜索、计算、代码执行、文件处理、天气查询等），从而突破纯语言生成的局限，构建具备行动力的智能体。

## 在百炼平台的不同场景中，这个概念如何使用

工具集成不是单一技术方案，而是覆盖多层抽象、适配不同开发范式的统一能力体系，具体体现为以下三类主流模式：

- **插件（Plug-in）**：面向快速集成与开箱即用。官方插件（如 `calculator`、`quark_search`）无需配置即可在智能体或工作流中启用；自定义插件需定义 URL、鉴权方式、输入/输出 Schema，并**必须发布为 MCP 服务后才能被智能体识别和调用**。适用于明确输入结构、结果可结构化返回的 RESTful 场景。

- **Skill**：面向文件与本地任务自动化。以 ZIP 包形式封装 Python 脚本及依赖，通过 `SKILL.md` 中的 `description` 字段驱动语义匹配（如“把 PDF 表格转成 Excel”）。不依赖模型能力，由智能体调度引擎直接触发，适合格式解析、数据清洗等确定性任务。

- **MCP（Model Context Protocol）服务**：面向标准化、可扩展的工具生态。基于开源 MCP 协议（Streamable HTTP），支持官方服务（如高德地图）、AI 网关封装的 API 或 OpenAPI 自动发布。智能体自动发现工具并生成调用参数；工作流中则作为显式节点编排。**是当前推荐的、统一的工具接入标准**，尤其适用于需要多工具协同、长链路调用的复杂场景。

此外，在 **Managed Agents** 运行时中，工具集成体现为内置沙箱能力（如 `bash`、`read`、`download_file`）与外部 MCP/Skill 的混合调用——模型可在同一会话中交替使用云端工具与本地命令，实现“思考-执行-验证”闭环。

> ✅ 关键区别：  
> - 插件侧重 *模型主动决策调用*，依赖模型理解输入参数；  
> - Skill 侧重 *意图精准匹配*，依赖 `description` 编写质量；  
> - MCP 侧重 *协议统一与生态互通*，支持自动发现与跨平台集成。

## 关键参数和配置

工具集成的配置分散在服务定义与应用绑定两个层面，开发者需关注以下核心项：

### 通用必填项（所有类型）
- **工具标识（ID / name）**：唯一字符串，用于在 `tools` 列表中声明或在工作流节点中引用（如 `"calculator"`、`"maps_weather"`）。控制台详情页可一键复制。
- **描述（description）**：对工具能力的自然语言说明。插件和 MCP 中用于模型理解用途；Skill 中此字段决定是否被触发，**必须包含适用场景 + 典型关键词 + 明确排除项**（如“不处理图像内容”）。

### 鉴权与安全
- **仅支持 `Authorization` header 透传**：自定义插件/MCP 调用时，其他自定义 header 将被平台忽略。建议使用 `bearer` 或 `appcode` 类型，并通过环境变量（如 `MCP_ENV_API_KEY`）注入敏感凭据，**禁止硬编码**。
- **服务关联角色授权**：首次使用插件或 MCP 服务前，需主账号或具备 `ram:CreateServiceLinkedRole` 权限的 RAM 用户授权角色 `AliyunServiceRoleForSFMAccessCloudAPI`。

### 输入与参数
- **输入 Schema（inputSchema）**：JSON Schema 格式，定义参数名、类型、是否必需、示例值（如 `{"city": "杭州", "date": "2025-04-25"}`）。工作流节点和模型调用均据此校验与填充。
- **参数传递方式**：
  - `大模型识别`：由模型从用户输入中抽取（适用于插件/MCP）；
  - `业务透传`：通过 `biz_params`（旧版智能体）、`user_defined_params`（Assistant API）或工作流字段引用（如 `{{ upstream.city }}`）显式传入。

### 协议与部署（MCP 专属）
- `type`: 必须为 `"streamableHttp"`（对应 `/mcp` 端点），旧版 `"sse"` 已弃用。
- `env`: 环境变量列表，用于注入 API Key、Endpoint 等，配合 KMS 加密管理。
- 超时控制：`MCP_INIT_TIMEOUT`（初始化超时，默认 30s）、`MCP_REQUEST_TIMEOUT`（单次请求超时，默认 60s），错误码 `11200058` 多因 `type` 不匹配或超时导致。

## 面向开发者，简洁实用

- ✅ **首选 MCP**：新项目统一使用 MCP 接入工具。它兼容官方/三方/自定义服务，支持自动发现、版本管理与跨平台 SDK（Python/Cherry Studio/Cursor），长期维护成本最低。
- ✅ **插件用于轻量 API**：若已有简单 REST 接口且无需复杂编排，用自定义插件最快上线；但务必记得：**发布为 MCP 服务后才可在智能体中生效**。
- ✅ **Skill 用于文件处理**：当任务本质是“读一个 PDF → 提取表格 → 生成图表 → 输出 Excel”，优先选 Skill，避免模型幻觉与网络调用开销。
- ⚠️ **避坑提示**：
  - 修改工具 URL 或鉴权配置后，必须重新测试并**发布**，否则调用失败；
  - 单个智能体最多添加 10 个工具（插件限制），MCP 服务最多选 5 个（智能体配置页限制）；
  - `code_interpreter` 沙箱禁止网络访问与文件上传，仅支持预装库（pandas/matplotlib/requests 等）；
  - 文件上传请确保 PDF 后缀为小写 `pdf`，否则报错 `140010`。

工具集成不是“连上就行”，而是模型能力延伸的接口设计。清晰定义 `description`、严格校验 `inputSchema`、安全管理 `env` 凭据——这三步做好，90% 的集成问题可提前规避。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [skill](../guides/skill.md)
- [model context protocol](../guides/model-context-protocol.md)
- [managed agents api](../api/managed-agents-api.md)
- [managed agents](../guides/managed-agents.md)
- [application support](../guides/application-support.md)


