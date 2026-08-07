# application evaluation

应用评测是阿里云百炼平台中用于系统化评估智能体、工作流等应用输出质量的核心能力，支持自动与手动两种评测范式。通过评测集驱动、多维度评估器组合及人工标签协同，开发者可量化验证应用效果、定位 RAG 流程瓶颈，并构建持续优化闭环。该能力深度集成于应用观测体系，要求前置开通相关功能并配置必要权限。

## 支持的模型/功能

- **自动评测**：基于知识库自动生成评测集，支持单应用深度诊断与最多 8 个应用的横向对比，依赖 `qwen-max` 或 `qwen-plus` 模型生成评测集与执行评分 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **手动评测**：支持人工构建评测集（XLS/XLSX 格式），通过人工打标完成效果评估，适用于需主观判断或无标准答案的场景 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **新版评测体系**：引入“智能体”“工作流”“自定义”三类评测集类型，支持从应用观测导入真实数据，并提供版本管理能力 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。
- **评估器（Grader）**：提供预置模板（如问答相关性、格式校验）及自定义 LLM/Code 评估器，支持多评估器组合评测，每个任务最多添加 10 个 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **标签管理**：支持分类、布尔值、数字、文本四类标签，用于人工标注与多维统计分析，可复用于评测任务与应用观测 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

> **注意**：文档 3 与文档 4 对评测集类型的定义存在差异——文档 3 仅区分“对话分析”和“知识问答”两类，而文档 4 明确支持“智能体”“工作流”“自定义”三类。实际控制台以文档 4 的新版分类为准，旧版“知识问答”对应新版“智能体”类型评测集。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **评测集** | `queryType`、`referenceAnswer`、`fineKeywords`、`coarseKeywords` | 知识问答型必备字段，用于大模型自动评分；`fineKeywords` 必须为嵌套数组格式 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md) |
| **评测规则** | 分类采样数（事实型/教程型/比较型/分析型）、评测模型（`qwen-max`/`qwen-plus`） | 控制评测覆盖广度与精度，影响 [Token](../concepts/token.md) 消耗；采样数为每类问题抽取数量，非总数 |
| **评估器** | `评分范围`（如 0–1、1–5）、`通过阈值`、`参数映射`（如 `query`→`Prompt`） | 决定评分粒度与判定逻辑；所有变量必须完成映射方可保存任务 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md) |
| **标签** | 类型（分类/布尔值/数字/文本）、筛选项（分类标签最多 20 项） | 影响标注方式与统计维度；布尔值标签固定为 `True`/`False`，数字标签支持浮点数 |

## 使用方式

1. **准备数据**：  
   - 自动评测：确保目标智能体已发布、关联知识库、开通应用观测；  
   - 手动评测：下载模板，按 `.xls`/`.xlsx` 格式填充 `Prompt`/`Completion`/`SessionId`；  
   - 新版评测：在[评测集](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=evalSet)页面选择类型（智能体/工作流/自定义），上传或从观测导入。

2. **创建任务**：  
   - 自动评测：在[自动评测](https://bailian.console.aliyun.com/?&tab=app#/efm/app_evaluate/tabs)界面依次完成“创建任务→设置评测集→配置规则→发起评测”；  
   - 新版评测任务：在[评测任务](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=task)页面选择评测集、关联应用（智能体/工作流/不关联）、添加评估器与标签。

3. **执行与分析**：  
   - 自动评测：查看总正确率、BadCase 归因（模型理解有误/重排不佳/检索无效/切片不完整/未获取知识）及调优建议；  
   - 手动/新版评测：进入任务详情页，在“数据明细”中逐条标注，或使用“快速标注”模式批量操作；在“指标统计”页查看综合得分、各评估器通过率及标签分布。

## 限制和注意事项

- **权限与依赖**：子账号需具备 `管理员` 或 `应用评测-操作` 权限；自动评测强制要求开通 `应用观测` 功能且目标应用已加入观测列表 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **数量限制**：单次自动评测最多支持 8 个应用；单个评测集文件 ≤ 20 MB，单次上传 ≤ 10 个文件；每个评测任务最多添加 10 个评估器。
- **格式强约束**：知识问答型评测集必须为 `.jsonl` 格式，`fineKeywords` 字段需严格采用 `...` 嵌套数组结构；对话分析型仅支持 `.xls`/`.xlsx`，且 `SessionId` 相同的行视为多轮对话。
- **不可逆操作**：评测任务创建后无法修改应用、评测集或评估器配置；评测集发布后类型不可更改；已发布的评测集若被引用则无法删除。
- **[Token](../concepts/token.md) 消耗提示**：预估平均消耗仅为参考值，实际账单以最终用量为准；预估最大消耗为硬性成本上限，但评测失败步骤仍计费 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


