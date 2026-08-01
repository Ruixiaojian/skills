# Prompt 工程

Prompt 工程是指在百炼平台上，通过系统化设计、迭代与优化提示词（Prompt），以精准引导大语言模型行为、提升输出质量、可控性与业务适配性的工程实践。它不是一次性编写文本，而是涵盖模板构建、上下文注入、自动增强、反馈调优与效果验证的闭环方法论。

## 在百炼平台的不同场景中，这个概念如何使用

Prompt 工程在百炼平台中并非孤立能力，而是贯穿于多个核心场景的底层支撑能力：

- **Prompt 模板管理**：作为最基础的工程载体，支持预置模板（开箱即用）和自定义模板（`text-generation` / `image-generation` 类型）。开发者通过控制台或 API 创建模板，利用占位符（如 `{{topic}}`）实现动态渲染，确保提示词可复用、可版本化、可跨应用共享。

- **智能体（Agent 2.0）构建**：系统提示词（System Prompt）是智能体的“行为契约”，直接影响其角色设定、工具调用逻辑与思考链生成。工程重点在于明确指令边界（如“仅回答事实，不虚构”）、注入领域约束（如“输出必须为 JSON Schema 格式”），并配合 `enable_thinking` 参数可视化推理过程。

- **工作流（Workflow）节点编排**：在大模型节点中，Prompt 是连接上游变量（如 `${sys.query}`、`${node1.output}`）与下游处理的关键接口。工程实践强调结构化输入（如将多轮历史拼接为 `<user>...<assistant>...` 格式）与显式格式要求（如 `请用 Markdown 表格返回结果`），保障流程确定性。

- **RAG 应用优化**：Prompt 与检索结果协同工作——需设计能理解 RAG 片段语义的指令（如“基于以下参考内容回答，未提及信息请回答‘暂无依据’”），避免幻觉；同时通过评测反馈（见下文）持续优化提示词对召回片段的利用效率。

- **模型/应用评测闭环**：Prompt 工程的成效需被量化验证。在 `application evaluation` 和 `model evaluation` 中，高质量 Prompt 是评测基准的前提；而评测结果（如幻觉率、格式错误率）又直接驱动 Prompt 迭代——例如，若评测发现“数字提取不准”，可针对性增强 Prompt 中的格式约束与示例。

> ⚠️ 注意：已弃用的 Prompt 样例库（Few-shot）功能不再维护，新项目应统一采用 **RAG 表格库 + 结构化 Prompt 设计** 或 **反馈优化（Prompt Feedback Optimization）** 作为少样本增强替代方案。

## 关键参数和配置

| 参数 | 说明 | 使用建议 |
|------|------|----------|
| `workspaceId` | 业务空间 ID，所有 Prompt 相关 API（如 `GetPromptTemplate`）必需 | 从控制台或 OpenAPI 文档获取，华北2（北京）地域专属，不可跨域复用 |
| `promptTemplateId` | 模板唯一标识符 | 控制台模板卡片右上角「复制 ID」，用于程序化加载与渲染 |
| `variables` | 模板中自动解析的占位符列表（如 `["topic", "platform"]`） | 运行时传入 JSON 对象填充，无需手动声明；确保变量名与模板内 `{{xxx}}` 严格一致 |
| `temperature` | 控制输出随机性（0.0–1.0） | 确定性任务（如结构化提取）设为 `0.0`；创意生成可设 `0.7–0.9`；智能体默认 `0.3` 平衡稳定性与灵活性 |
| `enable_thinking` | 开启模型推理链输出（Thinking step） | 仅 Agent 2.0 及支持思考模式的模型（如 `qwen-max`）有效；调试阶段开启，生产环境可关闭以节省 Token |
| `ReAct 最大轮次`（1–50） | 限制单次会话中工具调用总次数 | 防止死循环，推荐初设 `5–10`，根据实际工具复杂度调整 |

## 面向开发者，简洁实用

- **起步最快路径**：  
  1. 控制台 → [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) → 选一个预置模板（如“会议纪要生成”）→ 点击「创建应用」一键填充；  
  2. 在智能体应用中，将该模板粘贴至「系统提示词」框，替换占位符后发布测试；  
  3. 调用 SDK 时，用 `GetPromptTemplate` 获取模板内容，再 `render()` 填充变量，最后传给 `chat.completions.create()`。

- **进阶提效技巧**：  
  - ✅ **用反馈优化代替人工调参**：准备 5–10 条真实 query-answer 样例 + ≥20 条评测数据，在控制台启动「反馈优化」任务，自动生成更贴合业务的 Prompt；  
  - ✅ **结构化优于自由发挥**：文本 Prompt 推荐「角色+任务+约束+示例」四段式（如 `你是一名电商客服，请将用户问题分类为【售后】【物流】【咨询】三类，仅输出类别名，不要解释。示例：……`）；图像/视频 Prompt 必须遵循官方公式（主体+场景+运动+风格）；  
  - ✅ **成本敏感配置**：启用 `prompt_extend=false`（文生图）或 `stream=true`（长文本）减少冗余 Token；避免在 Prompt 中重复注入知识库内容，改用 RAG 检索片段动态注入；  
  - ❌ **规避已弃用路径**：勿依赖样例库（`has_thoughts=true` 等参数已失效），勿在非北京地域尝试 Prompt 功能（全域报错）。

- **调试黄金法则**：  
  > 所有 Prompt 修改后，务必用 **同一组测试用例** 对比输出差异；结合 `application evaluation` 的「幻觉检测」「格式校验」评估器定位问题；优化目标始终是「降低人工修正率」，而非单纯提升模型得分。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [application evaluation](../guides/application-evaluation.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)
- [use cases](../guides/use-cases.md)


