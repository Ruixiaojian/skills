# Prompt 工程

Prompt 工程是系统性设计、验证与优化大语言模型输入指令（Prompt）的方法论与技术实践，其目标是提升模型输出的准确性、一致性、可控性与业务适配度。在百炼平台中，它不是静态文本编写，而是融合模板化管理、结构化框架、自动增强与效果闭环评估的一整套工程能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）与工作流应用**：Prompt 是应用的“大脑指令”，通过控制台或 API 配置系统提示词（system [prompt](../guides/prompt.md)），支持变量插值（如 `${user_intent}`）、结构化框架（如 CRISPE、RASCEF）和角色设定；新版 Agent 2.0 更将 Prompt 与 `enable_thinking`、工具调用链路深度耦合，实现可解释的推理过程。
  
- **Prompt 模板服务**：提供开箱即用的预置模板（如营销文案、摘要抽取）和可复用的自定义模板，适用于华北2（北京）地域。模板支持正/负向提示词分离（尤其用于文生图）、多变量注入及跨应用共享，是团队协作与 Prompt 复用的核心载体。

- **Prompt 自动优化**：无需人工标注，基于大模型对原始 Prompt 进行指令强化、边界注入与结构重组，实时生成更鲁棒的版本；该能力免费、不训练、不存储用户数据，适合快速迭代初期 Prompt。

- **Prompt 反馈优化（推荐用于关键业务）**：结合 5–10 条高质量输入-输出样例 + ≥20 条评测数据，在 `qwen-max` 上多轮反思并生成带 few-shot 的优化 Prompt，效果显著优于通用自动优化，是上线前质量加固的关键步骤。

- **应用评测闭环**：Prompt 工程与 [application evaluation](../guides/application-evaluation.md) 深度联动——评测任务可针对特定 Prompt 版本执行，通过 LLM 评估器或人工标签量化其在事实性、格式合规、风格一致性等维度的表现，并直接驱动下一轮 Prompt 迭代。

> ⚠️ 注意：Prompt 样例库（Few-shot 样例库）功能已停止维护，新项目请勿依赖；RAG 表格库是其语义更强、可检索的知识注入替代方案。

## 关键参数和配置

| 参数 | 说明 | 使用建议 |
|------|------|----------|
| `workspaceId` | 业务空间 ID，所有 Prompt 相关 API 的必需路径参数 | 仅华北2（北京）有效，需通过控制台或 RAM 接口获取 |
| `promptTemplateId` | 模板唯一标识符 | 通过 `GetPromptTemplate` 获取，用于运行时加载与渲染 |
| `variables` | 模板中声明的变量名列表（如 `["topic", "tone"]`） | 运行时必须完整填充，缺失变量将导致渲染失败 |
| `content`（模板内容） | 支持 ICIO/CRISPE 等结构化框架，最大 6144 字符 | 控制台编辑框有硬限制；超长 Prompt 建议拆分为 system + user 分层传递 |
| `negative_prompt`（文生图场景） | 显式排除不期望元素（如 `"blurry, text, watermark"`） | 与正向 [prompt](../guides/prompt.md) 同等重要，建议始终显式配置 |
| `has_thoughts=true`（历史遗留） | 曾用于展示样例检索过程，但因样例库停用，**当前无实际作用** | 新项目请忽略此参数 |

## 面向开发者，简洁实用

- ✅ **起步最快方式**：控制台 → [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) → “基于 Prompt 工程创建” → 选模板 → 编辑变量 → 一键插入智能体配置页。
- ✅ **生产级推荐流程**：  
  1. 用预置模板快速启动；  
  2. 通过 `GetPromptTemplate` + SDK 渲染变量生成最终 Prompt；  
  3. 将其作为 `system` 消息传入 `ChatCompletion` 或智能体 `/chat` 接口；  
  4. 发布后立即关联 [application evaluation](../guides/application-evaluation.md)，用真实评测集验证效果；  
  5. 若效果未达预期，启用 **Prompt 反馈优化**，输入典型 BadCase 进行定向增强。
- ✅ **避坑要点**：  
  - 所有 Prompt 操作仅支持 **华北2（北京）**，跨地域调用必失败；  
  - 预置模板不可编辑，需点击“复制模板”生成自定义副本；  
  - 含大量 few-shot 的 Prompt 会显著增加输入 [Token](token.md)，请在效果与成本间权衡；  
  - 不要手动拼接 Prompt 字符串——务必通过 `GetPromptTemplate` 解析 `variables` 并严格按占位符规则替换（如 `${topic}`），避免语法错误。

Prompt 工程的本质，是把“让模型听懂人话”这件事，从经验直觉变为可测量、可版本化、可协同的软件工程实践。在百炼，它已不是起点，而是贯穿模型调用、应用构建与质量保障的基础设施。

## 关联主题页

- [prompt](../guides/prompt.md)
- [application component api reference](../api/application-component-api-reference.md)
- [application evaluation](../guides/application-evaluation.md)
- [use cases](../guides/use-cases.md)
- [llm application](../guides/llm-application.md)


