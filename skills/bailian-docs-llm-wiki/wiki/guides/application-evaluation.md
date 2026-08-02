# application evaluation

application evaluation 是阿里云百炼平台用于系统化评估智能体、工作流等应用输出质量的核心能力，支持自动与手动两种评测范式。它通过评测集（dataset）、评估器（grader）、标签（label）和评测任务（task）四大组件构成可扩展的评测体系，覆盖从数据准备、规则定义、自动打分到人工标注的全链路。开发者可根据业务需求选择轻量级自动评测或高精度人工评测，并借助归因分析定位 RAG 流程瓶颈。

## 支持的模型/功能

- **自动评测**：基于[知识库](../concepts/knowledge-base.md)自动生成评测集，调用 `qwen-max` 或 `qwen-plus` 模型完成端到端评分与归因分析，适用于单应用深度诊断或多应用横向对比（最多 8 个）[原文标题](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **手动评测**：支持人工构建 `.xls`/`.xlsx` 格式对话分析评测集，通过人工打标（如“较差/一般/较好”）产出定性报告 [原文标题](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。  
- **新版评测体系**：引入结构化评测集类型（智能体/工作流/自定义）、可组合评估器（LLM + Code）及多类型标签（分类/布尔/数字/文本），支持混合自动评分与人工标注的精细化评测 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  
- **评估器**：提供预置模板（如问答相关性、格式校验）及自定义 LLM/Code 评估器，支持字段映射、试运行验证与基于历史标注任务的自动化建模 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。  

> **注意**：文档 1 和文档 4–6 描述的“新版评测体系”与文档 1 中的“自动评测”存在功能重叠但架构不兼容——前者要求显式配置评估器与标签，后者为开箱即用的黑盒流程；实际使用中需根据控制台版本（旧版 `/efm/app_evaluate/tabs` vs 新版 `/efm/app_evaluate/tabs?activeKey=...`）选择对应路径，二者不互通。

## 关键参数

| 参数类别 | 名称 | 说明 | 约束 |
|----------|------|------|------|
| **评测集** | `queryType` | 问题分类标签（如 `"事实型"`、`"比较型"`），影响自动评测的任务类型采样 | 仅知识问答类 `.jsonl` 评测集必需；对话分析类 `.xlsx` 不支持 [原文标题](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md) |
| **评测规则** | 分类采样数 | 每类任务类型抽取的问题数量（如事实型=2，分析型=1） | 总采样数决定 Token 消耗上限，实际评测数 ≤ 采样数 × 类型数 |
| **评估器** | 评分范围 | 定义打分尺度（如 `0-1`、`1-5`、`0-100`） | 必须与 Prompt 中的评分指令严格一致，否则导致逻辑冲突 |
| **标签** | 类型 | 分类/布尔/数字/文本四类，决定标注方式与筛选条件 | 布尔值标签仅支持 `True`/`False`，不可自定义选项 |

## 使用方式

1. **准备评测数据**：  
   - 自动评测：确保应用已发布、关联[知识库](../concepts/knowledge-base.md)且开通应用观测，再通过控制台自动生成 `.jsonl` 知识问答评测集；  
   - 手动评测：下载 `.xlsx` 模板填写 `Prompt`/`Completion`/`SessionId`，上传后发布为评测集；  
   - 新版体系：创建智能体/工作流类型评测集，系统自动生成字段结构，或使用自定义类型灵活定义表结构。  

2. **配置评测任务**：  
   - 旧版自动评测：在“创建评测任务”中依次选择应用→[知识库](../concepts/knowledge-base.md)→生成评测集→设置采样数→选择 `qwen-max`/`qwen-plus` 评测模型→发起任务；  
   - 新版评测任务：选择已发布评测集→关联智能体/工作流应用→添加 3–5 个评估器（如 LLM 相关性评估器 + Code 格式校验器）→配置字段映射→启用标签进行人工补充标注。  

3. **执行与分析**：  
   - 自动评测结果包含总正确率、BadCase 归因（如“检索无效”“切片不完整”）及调优建议；  
   - 新版任务支持在“数据明细”页切换普通/快速标注模式，对每条结果进行多维度标注，并在“指标统计”页查看各评估器通过率与标签分布。  

## 限制和注意事项

- **应用约束**：自动评测仅支持已发布的智能体应用，且多应用横向评测要求所有应用必须关联至少一个**相同的知识库**；工作流应用仅在新版评测体系中支持 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  
- **文件限制**：评测集上传支持 `.xls`/`.xlsx`（≤20MB/个，单次≤10个）和 `.jsonl`（同规格），草稿状态评测集不可用于评测任务 [原文标题](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。  
- **权限要求**：子账号需具备 `管理员` 或 `应用评测-操作` 权限，且必须开通 `应用观测` 功能，否则无法启动评测 [原文标题](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **Token 消耗**：自动评测中“预估平均消耗”仅为参考值，实际用量以账单为准；“预估最大消耗”是硬性成本上限，但评测失败步骤仍计费 [原文标题](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **版本兼容性**：新版评测体系（含评估器、标签）与旧版自动评测互不兼容，控制台页面存在明确“返回旧版”入口，迁移需重建评测集与任务。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)


