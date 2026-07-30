# application evaluation

application evaluation 是百炼平台用于系统化评估智能体/工作流应用输出质量的核心能力，支持自动与手动两种评测范式。它通过评测集驱动、多维度评估器协同、人工标签补充的闭环机制，帮助开发者量化效果、定位问题并持续优化 RAG 或推理链路。评测结果可直接关联归因分析与调优建议，支撑从开发到上线的全周期质量保障。

## 支持的模型/功能

- **自动评测**：基于知识库自动生成评测集，支持单应用深度诊断与最多 8 个应用的横向对比，依赖 `qwen-max` 或 `qwen-plus` 模型生成评测集及执行评分 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **手动评测**：支持人工构建 `.xls`/`.xlsx` 格式对话分析评测集，或 `.jsonl` 格式知识问答评测集，通过人工打标产出报告 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **新版评测体系**：引入“智能体”“工作流”“自定义”三类评测集类型，支持从应用观测导入真实数据，并提供版本管理能力 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。
- **评估器（Grader）**：提供预置模板（如相关性、格式校验）及自定义 LLM/Code 评估器，支持最多 10 个评估器组合使用，实现多维度自动评分 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **标签管理**：支持分类、布尔值、数字、文本四类标签，用于人工标注与指标统计，可与应用观测联动实现线上数据质量回溯 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

> **注意**：文档 3 和文档 4 对评测集类型的描述存在差异——文档 3 仅提及“对话分析”和“知识问答”两类，而文档 4 明确扩展为“智能体”“工作流”“自定义”三类。当前控制台实际支持以文档 4 为准，旧版“知识问答/对话分析”逻辑已整合进新类型中。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **评测集类型** | 决定字段结构与适用场景：`智能体`（按出入参自动生成模板）、`工作流`、`自定义`（自由定义表结构） | 创建后不可修改 |
| **任务类型（自动评测）** | 生成评测集时需选择 2–8 种，如 `事实型`、`分析型`、`比较型`、`教程型`，支持自定义 | 影响评测集覆盖能力 |
| **采样数（自动评测）** | 每类任务下随机抽取的问题数量，通过滑块配置；总评测数 = 各类采样数之和 | 单任务最大样本量受系统限制 |
| **评估器参数映射** | 必须将评估器变量（如 `query`, `response`, `referenceAnswer`）精确映射至评测集字段或应用输出 | 所有变量未映射完成则无法保存任务 |
| **评分范围 & 通过阈值** | LLM/Code 评估器均需配置（如 `0–1`、`1–5`、`0–100`），阈值决定 Pass/Fail 判定 | 需与 Prompt 中的评分指令严格一致 |

## 使用方式

1. **准备评测集**  
   - 自动评测：在[自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)流程中，基于已配置知识库生成 `.jsonl` 格式知识问答评测集；  
   - 手动/新版评测：上传 `.xls`/`.xlsx`（对话分析）或 `.jsonl`（知识问答），或选择“智能体”类型后自动拉取应用出入参生成模板。

2. **创建评测任务**  
   - 旧版：在[自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)或[手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)页面发起，绑定应用+评测集；  
   - 新版：在[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)页面创建，支持“不关联应用”（纯人工标注）、“智能体”、“工作流”三种模式，并可添加多个评估器与标签。

3. **执行与分析**  
   - 自动评测任务启动后，系统自动调用模型运行并生成含 BadCase 归因、RAG 环节诊断、调优建议的报告；  
   - 新版评测任务支持“快速标注”模式逐条人工打标，指标统计页聚合评估器得分与标签分布；  
   - 所有评测结果均可导出，[Token](../concepts/token.md) 消耗明细在任务列表页可查。

## 限制和注意事项

- **应用前提**：自动评测仅支持**已发布**且**已配置知识库**的智能体应用，并需开通 `应用观测` 功能 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **权限要求**：子账号需具备 `管理员` 或 `应用评测-操作` 权限方可使用 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **并发与规模**：单次自动评测最多支持 8 个应用；评测集生成与执行均为离线任务，排队期间进度显示为 0%；大模型 [Token](../concepts/token.md) 消耗以实际账单为准，预估平均消耗仅为参考值 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **评测集一致性**：若复用已有评测集进行自动评测，必须确保其 `referenceAnswer` 能在当前指定知识库中被召回，否则导致评分失真 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。
- **配置不可变性**：评测任务创建后，应用、评测集、评估器等核心配置不可修改；如需调整，必须新建任务 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


