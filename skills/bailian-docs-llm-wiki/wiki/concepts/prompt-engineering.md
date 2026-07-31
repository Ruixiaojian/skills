# Prompt 工程

Prompt 工程是百炼平台中系统化设计、管理与优化大语言模型输入指令（Prompt）的方法论与工程实践，旨在通过结构化框架、模板化复用和数据驱动迭代，显著提升模型输出的准确性、一致性、可控性与业务适配度。

## 在百炼平台的不同场景中，这个概念如何使用

- **基础文本生成应用**：直接在控制台或 API 中编写 `system`/`user` 消息级 Prompt，配合变量插值（如 `${topic}`）实现动态内容注入；推荐使用预置或自定义 Prompt 模板，分离逻辑与数据。
- **智能体（Agent 2.0）应用**：Prompt 工程体现为“系统提示词（System Prompt）”配置——它定义智能体的角色、能力边界、[工具调用](tool-use.md)规范及思考范式（如启用 `enable_thinking` 时需匹配 ReAct 结构），直接影响规划质量与工具调度合理性。
- **工作流（Workflow）应用**：每个“大模型节点”均支持独立配置 Prompt 模板，支持跨节点变量传递（如 `historyList`、`imageList`），实现多步骤任务中上下文精准延续与角色状态保持。
- **图片/视频生成（万相系列）**：采用正向 Prompt + 负向 Prompt 双通道输入，需遵循视觉模型语义表达规律（如实体+属性+风格+构图），平台提供专用模板与结构化框架（如 CRISPE）辅助构建。
- **RAG 增强场景**：虽 RAG 主体由知识库与检索器承担，但最终生成阶段的 Prompt 工程至关重要——需显式指令模型“仅依据以下召回片段作答”“拒绝推测未提及信息”，并合理组织检索结果格式（如 JSON 片段列表），避免幻觉。

> ✅ 提示：所有场景下，Prompt 均需通过 `GetPromptTemplate` 渲染后，作为标准消息字段传入模型推理 API（如 `ChatCompletion`），不建议硬编码拼接。

## 关键参数和配置

| 参数 | 说明 | 开发者须知 |
|------|------|------------|
| `promptTemplateId` | 模板唯一标识符，用于 API 获取与调用 | 必填；在控制台模板详情页或 `ListPromptTemplates` 响应中获取 |
| `workspaceId` | 业务空间 ID，用于资源隔离与鉴权 | 必填；仅华北2（北京）地域有效，跨地域调用将失败 |
| `variables` | 模板声明的变量名数组（如 `["query", "context"]`） | 由 `GetPromptTemplate` 接口返回，运行时需按此键名填充，不可自行增删 |
| `temperature` / `top_p` 等模型参数 | 控制生成随机性与多样性 | 属于模型推理层参数，与 Prompt 工程正交；但高确定性任务（如结构化提取）建议设 `temperature=0.1–0.3` 配合强约束 Prompt |
| 结构化框架标识（非 API 参数） | 如 `ICIO`（Input-Context-Instruction-Output）、`CRISPE`（Capacity-Role-Insight-Statement-Personality-Experiment）等 | 在控制台“自动优化”或模板编辑器中可选择启用，用于引导 Prompt 逻辑完整性，不参与 API 传输 |

⚠️ 注意：已弃用的 `has_thoughts`、`召回片段数` 等参数仅关联已下线的 Prompt 样例库功能，新项目严禁使用；请统一迁移至 RAG 表格库或反馈优化流程。

## 面向开发者，简洁实用

- **起步最快方式**：控制台 → [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) → 使用“预置模板”或点击“新建模板”，粘贴你的原始 Prompt，启用“自动优化”一键增强。
- **生产级推荐路径**：  
  1. 定义清晰任务目标（如“从合同中提取甲方名称、签约日期、违约金比例，JSON 格式”）；  
  2. 在控制台创建模板，使用 `${variable}` 占位符（如 `${contract_text}`）；  
  3. 对关键模板启动“反馈优化”：上传 5–10 条高质量输入-输出样例 + ≥20 条评测数据，平台自动多轮迭代；  
  4. SDK 调用 `GetPromptTemplate` 渲染后，注入 `ChatCompletion` 请求的 `messages` 字段。
- **调试技巧**：  
  - 检查变量填充后总 [Token](token.md) 数（含用户输入），确保 ≤ 所选模型上下文上限（如 `qwen-max` 为 128K）；  
  - 图片生成类 Prompt 避免抽象形容词（如“beautiful”），改用具象描述（如“photorealistic, 8k, studio lighting, shallow depth of field”）；  
  - 所有 Prompt 数据经自动优化服务处理时**不存储、不训练、不共享**，符合隐私合规要求。

> 📌 最后提醒：Prompt 工程不是“一次写好”，而是“持续验证—量化评估—迭代优化”的闭环。百炼平台的反馈优化能力，正是为此而生——用你的真实业务数据，驱动 Prompt 进化。

## 关联主题页

- [prompt](../guides/prompt.md)
- [application component api reference](../api/application-component-api-reference.md)
- [llm application](../guides/llm-application.md)
- [model experience](../guides/model-experience.md)
- [frameworks](../api/frameworks.md)


