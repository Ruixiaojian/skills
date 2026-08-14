# application evaluation

application evaluation 是阿里云百炼平台用于系统化评估智能体（Agent）与工作流应用输出质量的核心能力，支持自动评测、手动评测及新一代可扩展评测框架。它通过评测集驱动、多维度评估器协同、人工标签补充的方式，帮助开发者量化应用表现、定位 RAG 流程瓶颈并闭环优化。该能力深度依赖应用观测数据，并与知识库、Prompt、模型选型等配置强耦合。

## 支持的模型/功能

- **自动评测**：基于知识库自动生成评测集，支持单应用深度诊断与最多 8 个应用的横向对比，依赖 `qwen-max` 或 `qwen-plus` 模型生成评测集及执行评分 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **手动评测**：支持人工构建 `.xls`/`.xlsx` 格式对话分析评测集，通过人工打标（如“较差/一般/较好”）产出报告，适用于需主观判断的业务场景 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **新版评测框架**：提供统一评测任务入口，支持关联智能体、工作流或自定义应用；集成预置与自定义评估器（LLM/Code）、多类型标签（分类/布尔/数字/文本），实现自动评分与人工标注融合 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。
- **评估器**：支持 LLM 语义评估（如相关性、幻觉检测）与 Code 规则评估（如 JSON 校验、字符串匹配），可基于历史人工标注任务反向生成 LLM 评估器 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **评测集类型**：明确区分「知识问答」（`.jsonl`，用于自动评测）与「对话分析」（`.xls`/`.xlsx`，用于手动评测），新版还支持「智能体」「工作流」「自定义」三类结构化评测集 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。

> **注意**：文档 4（新版评测集）与文档 3（评测集）对评测集类型的定义存在不一致——前者将评测集按应用类型（智能体/工作流/自定义）分类，后者按数据语义（知识问答/对话分析）分类。实际使用中，**评测集类型由创建时选择的模板决定，且创建后不可修改**；知识问答类评测集仅可用于自动评测流程，而对话分析类仅用于手动评测或新版框架中的人工标注场景。

## 关键参数

- **评测集字段**：  
  - 知识问答类必需字段：`query`（用户问题）、`referenceAnswer`（标准答案）、`coarseKeywords`（粗粒度主题词）、`fineKeywords`（细粒度信息点嵌套数组）、`queryType`（如“事实型”）；  
  - 对话分析类必需字段：`Prompt`（用户输入）、`Completion`（参考答案）、`SessionId`（多轮会话标识）。
- **采样与权重**：自动评测中，可通过滑块为各 `queryType`（事实型/分析型/比较型/教程型）设置分类采样数，总评测数 = 各类采样数之和；新版评测任务支持为每个评估器独立配置权重。
- **评估器参数映射**：所有变量（如 `query`, `response`, `reference`）必须完成字段映射，否则无法保存评测任务；映射错误将导致评分结果失真。
- **标签类型约束**：分类标签最多支持 20 个筛选项；数字标签支持 Double 类型；文本标签上限 200 字符；布尔值标签固定为 `True`/`False`。

## 使用方式

1. **准备数据基础**：  
   - 确保目标智能体已发布、配置知识库、并开通「应用观测」功能 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)；  
   - 创建评测集：可自动生成（仅知识问答类）或手动上传（支持 `.jsonl`/`.xls`/`.xlsx`）；新版支持从应用观测真实流量导入 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)；  
   - （可选）预先创建标签与评估器，用于后续任务配置 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)、[评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。

2. **发起评测**：  
   - **自动评测**：在控制台选择应用→指定知识库→生成评测集→配置采样规则→选择 `qwen-max`/`qwen-plus` 作为评测模型→发起任务；  
   - **手动评测**：上传并发布对话分析评测集→创建评测任务→人工逐条打标→提交生成报告；  
   - **新版评测任务**：选择评测集与应用→添加评估器并完成参数映射→配置标签→启动任务；支持“不关联应用”模式用于纯人工标注。

3. **分析与迭代**：  
   - 查看自动评测报告中的「BadCase 归因分析」（如“检索无效”“切片不完整”），结合调优建议修改知识库切分策略或 Prompt；  
   - 在新版任务详情页，通过「指标统计」查看各评估器通过率，用「数据明细」筛选特定标签组合定位问题样本；  
   - 建议在知识库更新、Prompt 调整、模型切换或定期回归时触发评测，形成持续优化闭环 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

## 限制和注意事项

- **权限与状态约束**：子账号需具备 `管理员` 或 `应用评测-操作` 权限；仅已发布的智能体应用可参与自动评测；评测集必须「已发布」才可用于任务 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **数量限制**：自动评测最多支持 8 个应用横向对比；单次上传评测集文件不超过 10 个，单个 ≤ 20MB；每个评测任务最多添加 10 个评估器。
- **模型与计费**：自动评测的评测集生成与执行阶段均调用 `qwen-max`/`qwen-plus`，产生 [Token](../concepts/token.md) 费用；新版框架中 LLM 评估器调用同样计费，Code 评估器无额外费用 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **不可变配置**：评测任务创建后，关联的评测集、应用、评估器映射关系不可修改；若需调整，必须新建任务。
- **数据一致性风险**：手动评测中，若所选评测集的参考答案无法在当前知识库中召回，将导致评测结果失真；新版框架中，评估器参数映射错误会直接导致评分失效 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


