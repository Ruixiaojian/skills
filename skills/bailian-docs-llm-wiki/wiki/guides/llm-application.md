# llm application

`llm application` 是阿里云百炼平台提供的面向大语言模型（LLM）的三类核心应用构建范式之一，用于突破模型在私有知识访问、实时信息获取、复杂任务规划等方面的原生局限。它通过零代码/低代码方式将 LLM 与知识库、MCP 工具、记忆等能力深度集成，支持从简单问答到多步自主决策的智能任务执行。开发者可根据业务需求，在智能体（Agent）、工作流（Workflow）和高代码应用三种模式中选型，其中智能体应用强调 AI 自主推理与动态工具调度，是处理开放式、意图不确定任务的首选方案 [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)。

## 支持的模型与功能

- **核心模型要求**：推荐选用具备强工具调用与多步规划能力的模型，如 `千问-Max` 系列；`千问-VL` 系列模型因具备[多模态](../concepts/multi-modal.md)能力，可直接解析图片/视频，即使关闭预解析亦能生效 [新版智能体应用 (raw/application-user-guide/llm-application/new-single-agent-application.md)](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **[文件处理](../concepts/file-processing.md)模式**：支持三种模式——**全文引用**（适合总结/翻译）、**切片检索（RAG）**（适合长文档精准问答）、**自定义处理**（依赖配置的 MCP 或插件完成图像风格转换、音视频分析等复杂操作）[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
- **内置能力**：  
  - **知识库（RAG）**：作为可被智能体自主规划调用的“工具”，支持标签过滤以提升检索精度；检索结果占用输入 [Token](../concepts/token.md)，需注意上下文窗口限制 [新版智能体应用 (raw/application-user-guide/llm-application/new-single-agent-application.md)](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
  - **MCP 工具**：所有外部服务（含官方 MCP 广场及自定义服务）均以 MCP 协议接入，支持非固定顺序、多轮动态调用。  
  - **内置沙箱工具**：`bash`、`write`、`read`、`edit`、`glob`、`grep`、`download_file`，全部默认关闭，按需启用。  
  - **技能（Skill）**：可复用的能力包，自动识别任务并触发对应逻辑，无需编码。  
  - **记忆**：仅支持短期记忆（0–30 轮上下文），[长期记忆](../concepts/long-term-memory.md)暂未上线。

> **注意**：文档 3（`single-agent-application.md`）仍提及“插件”概念，而文档 1（`new-single-agent-application.md`）已明确统一为“MCP 协议接入”。当前平台已全面迁移至 MCP 架构，旧版插件接口已不推荐使用，应优先通过 MCP 集成外部能力。

## 关键参数

| 参数 | 说明 | 取值范围/示例 | 备注 |
|------|------|----------------|------|
| `enable_thinking` | 是否开启模型思考模式（用于展示推理链路） | `true` / `false` | 仅对支持该能力的模型（如 `千问-Max`）生效；不支持时参数不可见 [新版智能体应用 (raw/application-user-guide/llm-application/new-single-agent-application.md)](../../raw/application-user-guide/llm-application/new-single-agent-application.md) |
| `ReAct 最大轮次` | 单次会话中工具调用的最大次数 | 1–50 | 超限后强制终止工具链并生成最终回复 |
| `最长回复长度` | 模型生成内容的 token 上限（不含提示词） | 正整数 | 影响输出完整性，需结合模型上下文窗口设置 |
| `温度系数（temperature）` | 控制输出随机性与多样性 | 0.0–2.0 | 值越高越随机，建议问答场景设为 0.1–0.6 |
| `单文件最大解析长度（token）` | 全文引用模式下单个文件提取上限 | 正整数 | 超出部分从文件末尾截断 |
| `召回片段数` | 切片检索模式下返回的相关文本片段数量 | 正整数 | 影响答案覆盖广度与精度平衡 |

## 使用方式

1. **创建与配置**：  
   - 访问控制台 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择 **智能体应用 > Agent 2.0** 创建；  
   - 在模型选择器中选定模型（如 `千问-Plus-Latest`），并通过参数配置器调整 `temperature`、`enable_thinking` 等；  
   - 配置系统提示词（支持嵌入自定义变量 `/var_name`），并按需开启知识库、MCP、内置工具等能力。

2. **文件交互**：  
   - 在调试窗口上传文件后，根据所选处理模式（全文引用/切片检索/自定义处理）进行对话；  
   - 若启用自定义处理，需提前挂载对应 MCP（如人物重绘）或插件，并确保模型能理解调用意图。

3. **发布与调用**：  
   - **必须先发布**应用，才能通过 API 或第三方渠道调用；  
   - 发布后，在 **发布渠道 > API 调用** 中获取 endpoint 与鉴权方式；  
   - API 调用时，文件需通过 `file_list`（通用文件 URL）、`image_list`（图片 URL）或 `session_file_id`（上传 API 返回 ID）传递，**无法在请求中动态切换[文件处理](../concepts/file-processing.md)模式** [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 限制和注意事项

- **版本兼容性**：Agent 1.0 与 Agent 2.0 架构不兼容，**不支持升级或降级**，需重新创建应用 [新版智能体应用 (raw/application-user-guide/llm-application/new-single-agent-application.md)](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **文件时效性**：聊天窗口上传的文件**仅在当前会话有效**，刷新或关闭页面即失效；生产环境强烈推荐使用 `session_file_id` 方式上传 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
- **计费要点**：  
  - 模型调用费用 = 输入 [Token](../concepts/token.md)（含知识库召回内容、文件解析文本） + 输出 [Token](../concepts/token.md)；  
  - 全文引用模式 Token 消耗显著高于切片检索；  
  - MCP 工具调用可能产生第三方费用，百炼平台不代收。  
- **缓存机制**：仅支持**隐式缓存**（自动识别公共前缀并按 20% 计费），暂不支持显式缓存配置 [新版智能体应用 (raw/application-user-guide/llm-application/new-single-agent-application.md)](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **超时限制**：自定义 MCP 服务调用超时为 **5 秒**，需确保服务响应在此时限内 [智能体应用 (raw/application-user-guide/llm-application/single-agent-application.md)](../../raw/application-user-guide/llm-application/single-agent-application.md)。

## 来源文档

- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


