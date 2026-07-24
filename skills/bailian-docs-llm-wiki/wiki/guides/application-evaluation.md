# application evaluation

应用评测是百炼平台用于系统化评估智能体/工作流应用输出质量的核心能力，支持自动与手动两种评测范式。自动评测基于大模型与知识库自动生成评测集并完成端到端评分，适用于快速迭代与横向对比；手动评测则依赖人工构建评测集与标注，适用于高精度、强业务语义的场景。二者均可结合评估器（LLM/Code）与标签体系实现多维度、可复用的质量分析。

## 支持的模型/功能

- **自动评测**：仅支持 `qwen-max` 和 `qwen-plus` 模型用于评测集生成与最终评分，不支持其他模型 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **手动评测**：无固定模型限制，实际调用模型由被评测应用自身配置决定，评测过程本身不强制指定模型。  
- **新版评测任务**：支持灵活组合多种评估器（LLM 或 Code 类型），每个任务最多添加 10 个评估器，覆盖相关性、正确性、格式校验、工具调用等维度 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  
- **评测集类型**：当前支持三类——**智能体**（适配智能体出入参）、**工作流**（适配工作流结构）、**自定义**（任意表结构），取代旧版仅区分“对话分析”与“知识问答”的二分法 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。  
> **注意**：文档 3 中定义的“知识问答（.jsonl）”与“对话分析（.xls/.xlsx）”仍为有效数据格式，但其语义已纳入新版“智能体”或“自定义”评测集类型下管理；旧格式未废弃，但新建评测集推荐使用新版类型体系。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **评测集** | `queryType`, `referenceAnswer`, `fineKeywords`, `coarseKeywords` | 仅知识问答类评测集必需，用于自动归因与细粒度评分 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md) |
| **评测规则** | 分类采样数（事实型/分析型/比较型/教程型） | 控制各任务类型抽样数量，直接影响评测覆盖率与 [Token](../concepts/token.md) 消耗 |
| **评估器** | `评分范围`（如 0–1、1–5）、`通过阈值`、`字段映射`（如 `query` → 评测集 `Prompt` 字段） | 决定评分尺度、Pass/Fail 判定逻辑及数据源绑定准确性，所有变量必须完成映射方可保存任务 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md) |
| **标签** | 类型（分类/布尔值/数字/文本）、筛选项、标注方式 | 用于人工补充维度，支持快速标注与基于标签的统计分析 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md) |

## 使用方式

1. **准备数据**：  
   - 自动评测：确保目标智能体**已发布**、**已配置知识库**、**已开通应用观测**；知识库内容需覆盖预期评测范围。  
   - 手动评测：按模板准备 `.xls`/`.xlsx`（对话分析）或 `.jsonl`（知识问答）文件，上传后**必须发布**才可用于评测任务。  
   - 新版评测集：推荐使用“智能体”类型，系统自动根据所选应用版本生成匹配字段结构。

2. **创建任务**：  
   - 自动评测：在控制台依次完成「选择应用→选择知识库→生成/选择评测集→配置采样与模型→发起评测」四步流程。  
   - 手动评测：在「手动评测」页选择已发布应用与已发布评测集，配置评测维度后启动，随后进入人工打标环节。  
   - 新版评测任务：选择「智能体」或「工作流」关联方式，绑定评测集与应用，并**至少添加一个评估器**（可选加标签），配置字段映射后创建。

3. **执行与分析**：  
   - 自动评测结果含总正确率、BadCase 归因（模型理解/重排/检索/切片/未获取知识）及调优建议。  
   - 新版任务支持「数据明细」查看每条评估器评分与人工标签、「指标统计」查看综合得分与各评估器通过率。  
   - 所有评测任务均支持导出结果，[Token](../concepts/token.md) 消耗可在任务列表页直接查看。

## 限制和注意事项

- **权限与状态限制**：自动评测要求子账号具备 `管理员` 或 `应用评测-操作` 权限；且仅支持**已发布**的智能体应用，草稿或未配置知识库的应用不可选 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **数量上限**：单次自动评测最多支持 8 个应用横向对比；单次评测任务最多添加 10 个评估器；单个评测集上传文件不超过 10 个，单文件 ≤20MB。  
- **不可修改性**：评测任务创建后，其关联的评测集、应用、评估器配置均**不可修改**；如需调整，必须新建任务 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  
- **费用与消耗**：自动评测与新版评测任务中调用 LLM 评估器均产生 [Token](../concepts/token.md) 费用，预估消耗仅为参考，以实际账单为准；Code 评估器无额外调用成本。  
- **兼容性提示**：新版评测任务（含评估器、标签、智能体评测集）与旧版自动/手动评测并存，但二者数据不互通；控制台提供「返回旧版」入口，迁移前请确认业务适配性。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


