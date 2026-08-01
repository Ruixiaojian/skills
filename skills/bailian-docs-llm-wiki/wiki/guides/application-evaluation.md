# application evaluation

application evaluation 是百炼平台用于系统化评估智能体/工作流应用输出质量的核心能力，支持自动与人工双路径评测机制。它通过结构化评测集驱动、多维度评估器打分、归因分析与人工标注协同，帮助开发者量化效果、定位瓶颈并闭环优化。评测结果可直接指导 Prompt 调优、知识库切片策略调整、检索重排配置等关键环节。

## 支持的模型/功能

- **自动评测**：基于大模型（当前仅支持 `qwen-max` 和 `qwen-plus`）自动生成评测集并执行端到端评分，适用于已发布且配置知识库的智能体应用，支持单应用深度评测与最多 8 个应用的横向对比 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **手动评测**：支持人工构建评测集（XLS/XLSX 格式），通过人工打标（如“较差/一般/较好”）产出定性报告，适用于需强业务语义判断的场景 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。  
- **新版评测体系**：引入统一评测任务模型，支持关联智能体、工作流或“不关联应用”的纯人工标注场景；支持混合使用 LLM 评估器（语义理解）与 Code 评估器（规则校验），每个任务最多添加 10 个评估器 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  
- **评测集类型扩展**：除传统知识问答（JSONL）和对话分析（XLS/XLSX）外，新版支持按应用类型（智能体/工作流）自动生成结构化表头，以及完全自定义字段的评测集 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。  
- **评估器与标签协同**：提供预置模板（如相关性、格式校验、幻觉检测）及自定义 LLM/Code 评估器；配合分类、布尔值、数字、文本四类标签，实现自动评分 + 人工补充标注的全维度覆盖 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)、[标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

> **注意**：文档 1（自动评测）中明确要求应用“已发布”且“配置知识库”，而文档 5（评测任务）中“选择应用”选项包含“不关联应用”这一纯人工场景，二者适用范围不同，无矛盾；但开发者需注意：**自动评测功能本身不支持未发布应用或无知识库应用**，该限制在文档 1 中已强调。

## 关键参数

| 参数类别 | 名称 | 说明 | 取值/约束 |
|----------|------|------|-----------|
| **评测集生成** | 任务类型 | 决定生成问题的语义类别 | 必选 2–8 种，如事实型、分析型、比较型、教程型；支持自定义 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md) |
| | 模型选择 | 生成评测集所用大模型 | 仅 `qwen-max`、`qwen-plus` [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md) |
| **评测执行** | 分类采样数 | 每类任务实际抽取的问题数量 | 各类型独立滑块调节，总样本量 = 各类采样数之和 |
| | 评测模型 | 执行最终评分的大模型 | 自动评测仅支持 `qwen-max`、`qwen-plus`；新版评测任务中 LLM 评估器可选其他模型（见文档 7） |
| **评估器** | 评分范围 | 评估器输出分数的有效区间 | 如 `0–1`、`1–5`、`0–100`，需与 Prompt 中描述一致 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md) |
| | 通过阈值 | 判定 Pass/Fail 的临界值 | ≥ 阈值为 Pass，建议设为评分范围中位数 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md) |
| **标签** | 标签类型 | 决定标注方式与筛选逻辑 | 分类（下拉多选）、布尔值（True/False）、数字（输入框）、文本（自由输入） [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md) |

## 使用方式

1. **准备评测数据**：  
   - 若用自动评测：确保应用已发布、配置知识库、开通应用观测；进入[评测集](https://bailian.console.aliyun.com/?&tab=app#/efm/app_evaluate/tabs?tab=group)页面，选择“自动生成”，指定知识库与任务类型。  
   - 若用手动评测：下载 XLS/XLSX 模板，填写 `Prompt`（用户输入）、`Completion`（参考答案）、`SessionId`（多轮标识），上传并发布 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。  
   - 若用新版体系：在[评测集](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=evalSet)页面选择“智能体/工作流/自定义”类型，系统自动生成字段或手动定义结构，再导入数据。

2. **创建评测任务**：  
   - 自动评测：在控制台“自动评测”页选择应用、知识库 → 设置评测集 → 配置采样数与模型 → 发起任务。  
   - 新版评测任务：在[评测任务](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=task)页选择评测集与应用类型 → 添加评估器（完成参数映射）→ （可选）添加标签 → 创建任务。

3. **执行与分析**：  
   - 自动评测：任务完成后查看总正确率、BadCase 归因（如“检索无效”“切片不完整”）及调优建议 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
   - 新版评测任务：在任务详情页切换“数据明细”（查看每条评估器评分与人工标签）与“指标统计”（综合得分、各评估器通过率柱状图）。

## 限制和注意事项

- **应用状态限制**：自动评测仅支持**已发布**的智能体应用，且必须关联至少一个知识库；未发布应用或无知识库应用无法发起 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **知识库一致性要求**：多应用横向评测时，所有被选应用必须拥有**至少一个公共知识库**，否则无法继续 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **评测集格式强约束**：知识问答类评测集必须为 `.jsonl` 格式，含 `query`、`referenceAnswer`、`fineKeywords`、`coarseKeywords`、`queryType` 字段；对话分析类必须为 `.xls`/`.xlsx`，含 `Prompt`、`Completion`、`SessionId` 字段 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。  
- **配置不可变性**：评测任务创建后，其关联的评测集、应用、评估器映射等核心配置**不可修改**；如需调整，必须新建任务 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  
- **Token 消耗提示**：自动评测中“预估平均消耗”仅为参考值，实际用量以账单为准；“预估最大消耗”是硬性成本上限，但实际消耗通常显著低于此值 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


