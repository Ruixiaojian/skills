# llm application

`llm application` 是阿里云百炼平台面向大模型落地的核心能力抽象，提供三种互补的构建范式：以自主决策为特征的智能体（Agent）、以流程确定性为优势的工作流（Workflow），以及以代码完全可控为特点的高代码应用。开发者可根据业务复杂度、可控性要求和团队技术栈，在零代码、低代码与专业编码之间灵活选型，快速构建具备知识增强、工具调用与多步规划能力的生产级 AI 应用。

## 支持的模型/功能

- **模型支持**：所有应用类型均支持千问系列主流模型（如 `qwen-max`、`qwen-plus-latest`、`qwen-vl-plus`），部分能力对模型有特定要求：
  - 新版智能体（Agent 2.0）推荐使用 `千问-Max` 系列等具备强工具调用能力的模型，以保障多步规划效果 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)；
  - 文件问答场景中，视觉理解任务需选用 `千问VL` 系列模型，而文本长文档处理则可搭配 `千问Long` 或 `千问3` 开源模型 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)；
  - 工作流节点（如大模型节点、意图分类节点）默认支持 `千问-Plus-latest`，但实际可用模型以控制台实时列表为准 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。

- **核心功能矩阵**：
  | 功能                | 智能体（Agent） | 工作流（Workflow） | 高代码应用 |
  |---------------------|----------------|----------------------|------------|
  | 知识库（RAG）       | ✅ 统一为工具，由模型自主调用 | ✅ 可在大模型节点中显式配置知识库输入 | ✅ 通过 MCP 协议一键接入 |
  | 外部工具（MCP/[插件](../concepts/plugin.md)）| ✅ 自主规划调用顺序与时机 | ❌ 不支持直接调用；需封装为子智能体或通过 API 节点间接集成 | ✅ 一站式 MCP 工具接入 |
  | [多模态](../concepts/multi-modal.md)文件处理      | ✅ 支持全文引用、切片检索、自定义处理三种模式 | ❌ 仅支持文本输入；图片/音视频需预处理为文本后传入 | ✅ 依赖代码实现，灵活性最高 |
  | 可视化编排          | ❌ 提示词驱动，无节点图 | ✅ 基于画布拖拽节点，支持条件分支、循环、变量传递 | ❌ 纯代码定义逻辑 |
  | 自定义前端          | ❌ 控制台内置对话界面 | ❌ 同上 | ✅ 支持直接体验、交互卡片、完整 WebUI（基于 Spark Design） |

> **注意**：文档 3（[智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)）将“[插件](../concepts/plugin.md)”作为独立能力描述，而文档 2（[新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)）明确指出“[插件](../concepts/plugin.md)已支持一键转换为 MCP 服务”，且新版统一使用 MCP 协议调度所有外部能力。因此，**插件是旧版概念，新版智能体应统一使用 MCP**；若需兼容旧插件，须通过 MCP 封装。

## 关键参数

- **通用参数**：
  - `temperature`：控制生成随机性，范围通常为 0.0–1.0，值越高输出越发散；
  - `max_tokens`（最长回复长度）：限制模型输出 token 数，不包含提示词；
  - `enable_thinking`：仅对支持思考模式的模型（如 `qwen-max`）有效，开启后可展示推理链路。

- **智能体特有参数**：
  - `ReAct 最大轮次`（1–50）：限制单次会话中工具调用总次数，超限则终止调用并生成最终回复；
  - `短期记忆轮数`（0–30）：控制多轮对话上下文保留数量，0 表示无记忆；
  - `预解析文件`开关：决定上传文件是否由系统自动解析为文本（关闭时仅传递 URL，由模型自主决策是否调用工具解析）。

- **工作流特有参数**：
  - `会话变量`（如 `query`, `historyList`, `imageList`）：全局共享变量，支持跨节点引用；
  - `记忆`配置（自定义缓存 / 本节点缓存）：影响大模型节点对历史对话的感知范围；
  - `召回片段数` & `最大拼装长度`：仅在启用知识库或切片检索时生效，用于控制 RAG 输入规模。

- **高代码应用特有参数**：
  - 部署方式（Serverless Function / K8s）、规格方案（vCPU/内存）、最小实例数、并发度：直接影响性能与成本；
  - 环境变量与触发器配置：用于注入密钥、连接外部服务。

## 使用方式

- **创建与配置**：
  - 智能体：控制台 → 应用中心 → 创建应用 → 选择“智能体应用” → 优先选用 **Agent 2.0** 版本 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)；
  - 工作流：控制台 → 应用中心 → 创建应用 → 选择“工作流应用” → 拖拽节点（开始/大模型/意图分类/结束等）并连线配置；
  - 高代码应用：控制台 → 应用中心 → 创建应用 → 选择“高代码应用” → 选择模板或上传 `.whl` 包部署。

- **文件处理模式（智能体专属）**：
  - `全文引用`：适合短文档总结，需关注 token 截断风险；
  - `切片检索`：适合长文档问答，支持混合检索上传文件 + 知识库；
  - `自定义处理`：适合需调用 MCP 工具的场景（如图片风格转换），千问VL模型支持“模型处理+规划”双模式。

- **发布与调用**：
  - 所有应用**必须发布后才能被调用**（API/SDK/第三方平台）；
  - API 调用入口统一位于应用详情页的 **发布渠道 > API调用** 标签页；
  - 文件问答的 API 调用需严格遵循应用内配置的处理模式，**无法在请求时动态切换** [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 限制和注意事项

- **功能限制**：
  - 智能体暂不支持[长期记忆](../concepts/long-term-memory.md)（文档 2 明确说明“该功能计划在未来的迭代中支持”）；
  - 工作流不支持原生[多模态](../concepts/multi-modal.md)输入，图片/音视频需先经外部服务转为文本再接入；
  - 高代码应用的 `.whl` 包仅支持 Python 项目，不支持其他语言运行时。

- **计费关键点**：
  - 模型调用费用 = 输入 [Token](../concepts/token.md) × 输入单价 + 输出 [Token](../concepts/token.md) × 输出单价；
  - 知识库检索内容计入输入 [Token](../concepts/token.md)，`切片检索` 模式通常比 `全文引用` 更省成本；
  - MCP 工具调用可能产生额外费用（如文生图按次计费），第三方 API 费用由对应服务商收取。

- **重要注意事项**：
  - **版本不可互转**：Agent 1.0 与 Agent 2.0 架构不兼容，无法升级或降级，需重新创建 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)；
  - **文件有效期**：聊天窗口上传的文件仅在当前会话有效；通过 `session_file_id` 上传的文件有效期为 24 小时；
  - **API 限流**：每个智能体应用默认限流 100 次/分钟，该配额被所有 API 请求共享（含文件问答、普通对话等）；
  - **权限要求**：发布应用前，RAM 子账号需具备 `ram:CreateServiceLinkedRole` 权限，否则发布失败 [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


