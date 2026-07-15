# application evaluation

应用评测是百炼平台用于系统化评估智能体/工作流应用输出质量的核心能力，支持自动与手动两种评测范式。自动评测基于大模型与知识库自动生成评测集并完成端到端评分，适用于快速迭代与横向对比；手动评测则依赖人工构建评测集与标注，适用于高精度、强主观性或需深度归因的场景。两类评测均围绕评测集、评测任务、评估器与标签四大核心组件展开，形成可配置、可复用、可追溯的质量保障闭环。

## 支持的模型/功能

- **自动评测**：仅支持 `qwen-max` 和 `qwen-plus` 两种模型用于评测集生成与最终评分，不支持其他模型（如 `qwen-turbo` 或 `qwen2` 系列）[原文标题](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。该限制同样适用于评测规则配置阶段。
- **评估器类型**：新版评测体系支持 LLM 评估器（调用大模型进行语义评分）、Code 评估器（执行 Python 脚本进行规则校验）及基于历史评测任务自动生成的 LLM 评估器 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。LLM 评估器默认限时免费，但实际调用仍产生 Token 费用。
- **评测集类型**：当前存在两套并行体系：
  - 旧版仅支持 **对话分析**（`.xls`/`.xlsx`）和 **知识问答**（`.jsonl`）两类，分别用于手动评测与自动评测 [原文标题](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)；
  - 新版扩展为 **智能体**、**工作流** 和 **自定义** 三类，支持按应用出入参结构自动生成模板，并引入版本管理与表结构编辑能力 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。
> **注意**：文档 3 与文档 4 对评测集类型的定义存在明显差异——前者限定为“对话分析”和“知识问答”，后者升级为“智能体/工作流/自定义”。这反映平台已从单一 RAG 场景向通用应用评测演进，**旧版类型已逐步被新版覆盖，新建评测应优先采用新版评测集**。

## 关键参数

- **评测集字段映射**：所有评估器（尤其是预置模板）对输入字段有明确要求。例如，“问答相关性”评估器必需 `query` 和 `response` 字段；若评测集字段名为 `Prompt`/`Completion`，必须在参数映射中显式绑定 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **分类采样数**：自动评测中，需为每种任务类型（事实型、教程型等）单独设置采样数量，直接影响评测覆盖面与 Token 消耗 [原文标题](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **评估器评分范围与阈值**：LLM/Code 评估器均需配置 `评分范围`（如 `0-1` 或 `1-5`）和 `通过阈值`（如 `0.8` 或 `4`），二者共同决定 Pass/Fail 判定逻辑，且必须在 Prompt 中保持语义一致 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **标签类型约束**：标签创建时需指定类型（分类/布尔值/数字/文本），不同类型对应不同筛选条件与标注方式，影响后续指标统计维度 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

## 使用方式

1. **准备数据基础**：
   - 创建评测集：可选择自动生成（仅限知识问答类型，依赖知识库）或手动上传（支持 `.xls`/`.xlsx`/`.jsonl` 格式，单文件 ≤20MB）[原文标题](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)；
   - 发布评测集：草稿状态不可用于评测，必须点击“发布”使其生效；
   - （可选）创建标签与评估器：按业务需求定义多维标注体系与自动化评分规则。

2. **发起评测任务**：
   - **自动评测**：进入控制台自动评测页面 → 选择已发布且配置知识库的智能体应用 → 选择知识库 → 生成或选用评测集 → 设置采样数与评测模型 → 发起任务 [原文标题](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)；
   - **手动评测**：上传评测集 → 进入手动评测页 → 选择应用与已发布评测集 → 配置评测维度 → 开始评测 → 人工打标（较差/一般/较好 或 1–5 分）→ 提交结果；
   - **新版评测任务**：支持“不关联应用”（纯人工标注）、“智能体”或“工作流”关联模式，并可同时添加最多 10 个评估器与任意标签 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。

3. **分析与迭代**：
   - 查看报告：自动评测提供总正确率、BadCase 归因（模型理解/重排/检索/切片/未获取知识）、RAG 各类型得分；手动评测提供人工标注汇总；
   - 使用标签筛选 BadCase，结合评估器结果定位问题根因；
   - 基于归因建议优化 Prompt、知识库切分策略或检索配置，发布新版本后复用同一评测集验证效果。

## 限制和注意事项

- **权限与前提**：自动评测要求子账号具备 `管理员` 或 `应用评测-操作` 权限，且目标应用必须已发布、配置知识库、并加入应用观测列表 [原文标题](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **数量限制**：单次自动评测最多支持 8 个应用横向对比；单个评测任务最多添加 10 个评估器；单次上传评测集文件不超过 10 个，单文件 ≤20MB。
- **Token 消耗**：所有调用大模型的操作（评测集生成、自动评分、LLM 评估器）均产生 Token 费用，预估消耗仅为参考，实际以账单为准；试运行也会消耗少量 Token [原文标题](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **评测失败处理**：自动评测中失败用例不计入正确率计算；手动评测中未完成打标的条目不影响已完成部分的统计。
- **兼容性提示**：新版评测任务（文档 5/6/7）与旧版自动/手动评测（文档 1/2/3）共存，但二者数据模型与流程不互通。**新建项目应统一使用新版体系**，旧版功能仅维持兼容，不再新增特性。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


