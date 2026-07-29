# application evaluation

应用评测是百炼平台用于系统化评估智能体或工作流应用输出质量的核心能力，支持自动评分与人工标注双轨并行。它通过评测集提供标准化输入数据，结合评估器（LLM 或 Code）实现多维度自动打分，并允许开发者配置标签进行主观判断与深度归因分析，最终生成可量化的评测报告与调优建议。

## 支持的模型/功能

- **评测类型**：当前支持三类评测集——**智能体**、**工作流**和**自定义**，分别适配不同应用形态的出入参结构 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)；同时保留传统分类：**对话分析**（用于人工评测）和**知识问答**（用于自动评测）[评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。
  
- **评估器类型**：支持预置模板（如“问答相关性”“格式校验”）及自定义创建，包括：
  - **LLM评估器**：基于 `qwen-max` 或 `qwen-plus` 等大模型进行语义评分，适用于相关性、幻觉、有害性等复杂判断；
  - **Code评估器**：通过 Python 脚本执行精确规则匹配（如 JSON 校验、关键词存在性），零 [Token](../concepts/token.md) 成本；
  - **基于评测任务的评估器**：从已完成人工标注的历史任务中自动提炼评分逻辑 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。

- **评测模式**：
  - **自动评测**：面向已发布且配置知识库的智能体应用，支持单应用深度诊断与最多 8 个应用的横向对比 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)；
  - **手动评测**：依赖人工构建 `.xls`/`.xlsx` 评测集，通过“打标”完成人工评分，适用于高专业性场景；
  - **新版评测任务**：统一入口，支持“不关联应用”（纯人工标注）、智能体或工作流调用，并可混合使用多个评估器与标签 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。

> **注意**：文档 1 和文档 4 对评测集类型的定义存在差异——文档 1 仅提“对话分析”与“知识问答”，而文档 4 明确扩展为“智能体/工作流/自定义”三类。实际平台以文档 4 的新版分类为准，旧分类（如“对话分析”）属于“智能体”类型下的具体数据结构变体，非独立类型。

## 关键参数

- **评测集字段要求**：
  - 智能体类评测集：必含 `Prompt`（用户输入）与 `Completion`（参考答案）字段；若含多轮对话，需 `SessionId` 字段对齐会话上下文；
  - 知识问答类（`.jsonl`）：必含 `query`、`referenceAnswer`、`coarseKeywords`、`fineKeywords`；
  - 自定义评测集：字段完全由用户定义，但需在评估器参数映射时确保字段名一致。

- **评估器配置核心项**：
  - `评分范围`（如 `0-1`、`1-5`、`0-100`）：决定输出粒度，影响阈值敏感性；
  - `通过阈值`：默认设为范围中值（如 `0-1` 时阈值为 `0.5`），用于 Pass/Fail 判定；
  - `参数映射`：必须将评估器 Prompt 中引用的变量（如 `query`, `response`, `reference`）一一映射至评测集字段或应用输出，**未完成映射则无法保存评测任务**。

- **评测规则控制**：
  - 分类采样数：在自动评测中，可为“事实型”“分析型”等任务类型分别设置采样数量；
  - 模型选择：生成评测集与执行评测均限选 `qwen-max` 或 `qwen-plus`；
  - 标签类型：支持分类、布尔值、数字、文本四类，用于人工标注维度 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

## 使用方式

1. **准备数据**：
   - 创建评测集：可手动上传 `.xls`/`.xlsx`（对话分析）或 `.jsonl`（知识问答），或使用新版“智能体/工作流”类型自动生成模板；亦支持从应用观测导入真实流量数据 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。
   - 发布评测集：草稿状态不可用于评测，必须点击“发布”后方可选用。

2. **配置评测任务**：
   - 进入[评测任务](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=task)页面，选择评测集版本与目标应用（智能体/工作流/不关联）；
   - 添加评估器（最多 10 个），严格完成所有参数映射；
   - 可选添加标签（如“回答完整性”“是否存在幻觉”），用于人工补充判断。

3. **执行与分析**：
   - 启动评测后，状态变为“评测中”，完成后可在“数据明细”页查看每条样本的评估器评分与人工标签；
   - “指标统计”页提供综合得分仪表盘、各评估器通过率柱状图及 BadCase 分布；
   - 自动评测额外提供归因分析（如“检索无效”“切片不完整”），并给出对应优化建议 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

## 限制和注意事项

- **权限与前提**：
  - 子账号需具备 `管理员` 或 `应用评测-操作` 权限；
  - 自动评测要求应用已发布、配置知识库、且开通“应用观测”功能；
  - 多应用横向评测时，所有被选应用必须共享至少一个知识库。

- **技术限制**：
  - 评测集单文件 ≤ 20 MB，单次上传 ≤ 10 个文件；
  - 评测任务创建后**不可修改**应用、评测集或评估器配置，仅支持新增标签 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)；
  - 基于评测任务创建的评估器**不支持试运行**，需在真实任务中验证效果 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。

- **计费与消耗**：
  - LLM评估器调用产生 [Token](../concepts/token.md) 费用，Code评估器无额外成本；
  - 预估 [Token](../concepts/token.md) 消耗为参考值，实际用量以账单为准；“预估最大消耗”为硬性上限，实际极少达到 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

- **数据一致性**：
  - 若选用已有评测集进行自动评测，需确保其 `referenceAnswer` 和 `keywords` 内容均可在当前指定知识库中检索到，否则评测结果失真；
  - 新版评测任务中，“不关联应用”选项适用于纯人工标注场景，此时系统不会触发任何模型调用。

## 来源文档

- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


