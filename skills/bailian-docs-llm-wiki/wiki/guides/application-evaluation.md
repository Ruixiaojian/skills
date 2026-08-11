# application evaluation

应用评测是百炼平台提供的核心质量保障能力，用于系统化评估智能体、工作流等应用的输出效果。它支持人工打标与自动评分双模式，覆盖从评测集构建、任务执行到归因分析与调优建议的完整闭环。评测既可面向单应用深度诊断，也支持多应用横向对比，适用于上线前验证、迭代回归及线上观测数据回溯等典型研发运维场景。

## 支持的模型/功能

- **评测模式**：支持**手动评测**（基于人工构建评测集+人工打标）和**自动评测**（基于知识库自动生成评测集+大模型自动评分）两种范式；新版评测体系进一步引入**评估器（Grader）驱动的混合评测**，支持 LLM 与 Code 类型评估器组合使用，实现语义理解与规则校验的协同 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **应用类型支持**：手动评测仅支持已发布的**智能体应用**；自动评测同样限定于已发布且配置了知识库的智能体应用；而新版评测任务（[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)）已扩展支持**智能体**、**工作流**及**不关联应用**（纯人工标注）三种模式。
- **评测集类型**：当前支持三类评测集：**对话分析**（`.xls`/`.xlsx`，用于多轮/单轮人工评测）、**知识问答**（`.jsonl`，用于自动评测）以及新版统一的**智能体/工作流/自定义**类型评测集，后者通过动态表结构适配不同应用的出入参形式 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。

> **注意**：文档 1（手动评测）与文档 4（新版评测集）在评测集类型定义上存在差异——前者仅明确区分“对话分析”与“知识问答”，后者则按应用形态划分为“智能体/工作流/自定义”。实际使用中，应以新版控制台界面为准，旧版文档中的类型划分已逐步被新模型抽象所覆盖。

## 关键参数

- **评测集字段**：
  - 对话分析需包含 `Prompt`（用户输入）、`Completion`（参考答案）、`SessionId`（会话标识）；
  - 知识问答需包含 `query`、`referenceAnswer`、`coarseKeywords`、`fineKeywords`、`queryType`；
  - 新版评测集支持自定义字段结构，但预置模板会根据所选应用自动推导字段（如 `input`、`output`），详见 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。
- **评估器参数映射**：所有变量（如 `query`, `response`, `context`）必须完成字段映射才能保存评测任务；映射错误将直接导致评估器失效 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **评分配置**：
  - LLM 评估器需设置**评分范围**（如 `0-1`、`1-5`、`0-100`）与**通过阈值**（默认常设为范围中值）；
  - 自动评测报告中，“总正确率”定义为得分 ≥4 分的回答数 / 总回答数 × 100% [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

## 使用方式

1. **准备评测数据**：  
   - 手动构建：下载 Excel 模板填写 `Prompt`/`Completion`，或按 JSONL 格式编写知识问答数据；  
   - 自动生成：在自动评测流程中，基于知识库选择任务类型（事实型/分析型等），由 `qwen-max` 或 `qwen-plus` 模型生成评测集；  
   - 新版推荐：通过“从应用观测导入”复用真实线上请求数据，提升评测代表性。

2. **创建并发布评测集**：  
   - 上传后必须点击**发布**，草稿状态无法用于评测任务；  
   - 新版支持版本管理，每次发布生成新版本，创建任务时可指定使用特定版本。

3. **配置评测任务**：  
   - 选择评测集与目标应用（智能体/工作流）；  
   - 添加评估器（最多 10 个），严格完成所有参数映射；  
   - 可选添加人工标签（分类/布尔/数字/文本四类），用于主观维度补充 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)；  
   - 任务创建后配置不可修改，如需调整须新建任务。

4. **执行与分析**：  
   - 启动后查看进度，支持中途终止；  
   - 完成后在“数据明细”页查看每条结果的评估器评分与人工标签；  
   - “指标统计”页提供综合得分、通过率柱状图及数据分布；  
   - 自动评测额外提供 BadCase 归因（如“检索无效”“切片不完整”）与调优建议。

## 限制和注意事项

- **权限与依赖**：自动评测要求子账号具备 `管理员` 或 `应用评测-操作` 权限，且目标应用必须已开通 `应用观测` 并加入观测列表 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **文件与规模限制**：  
  - 评测集上传：单文件 ≤20 MB，单次 ≤10 个；  
  - 多应用横向评测：最多支持 8 个应用；  
  - 评测样本量：自动评测中各任务类型采样数通过滑块调节，总评测数受 [Token](../concepts/token.md) 预算约束。
- **计费说明**：  
  - 所有调用大模型的环节（评测集生成、自动评分、LLM 评估器运行）均按实际消耗 [Token](../concepts/token.md)s 计费；  
  - Code 评估器无额外费用；  
  - 预估 [Token](../concepts/token.md) 消耗仅为参考值，实际以账单为准 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。
- **关键约束**：  
  - 手动评测中，未发布的智能体应用不可选；  
  - 自动评测要求知识库非空，且多应用评测时所有应用必须共享至少一个知识库；  
  - 新版评测任务中，“不关联应用”选项仅用于纯人工标注，不触发任何模型调用。

## 来源文档

- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


