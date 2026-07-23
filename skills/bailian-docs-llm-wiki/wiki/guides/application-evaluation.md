# application evaluation

application evaluation 是百炼平台用于系统化评估智能体/工作流应用输出质量的核心能力，支持自动与手动两种评测范式。它通过结构化评测集、可配置的评估器与人工标签协同，实现从数据构建、任务执行到归因分析的完整闭环，适用于模型迭代、知识库更新、Prompt调优等关键研发场景。

## 支持的模型/功能

- **自动评测**：基于大模型（当前仅支持 `qwen-max` 和 `qwen-plus`）自动生成评测集并执行端到端评分，适用于已发布且配置知识库的智能体应用 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **手动评测**：支持人工构建评测集（`.xls`/`.xlsx` 格式），通过人工打标完成效果评估，适用于需强主观判断或无标准答案的业务场景 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。  
- **新版评测体系**：引入「智能体」「工作流」「自定义」三类评测集，并支持多评估器（LLM/Code）+ 多标签（分类/布尔/数字/文本）混合评测模式，覆盖更细粒度的质量维度 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  
- **评估器能力**：提供预置模板（如问答相关性、格式校验、文本相似度）及自定义 LLM/Code 评估器；LLM 评估器支持基于历史标注任务反向生成（即“评估器蒸馏”），但该方式不支持试运行 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。  
> **注意**：文档 4（新版评测集）与文档 3（旧版评测集）存在类型定义冲突——前者将评测集按应用形态（智能体/工作流/自定义）分类，后者按数据语义（对话分析/知识问答）分类。实际使用中，**新版体系已取代旧版**，旧版文档内容已过时，应以 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md) 为准。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **评测集类型** | 新版体系下必须在创建时选定：`智能体`（适配智能体出入参）、`工作流`（适配工作流出入参）、`自定义`（自由定义表结构） | 创建后不可修改 |
| **评估器映射** | 所有变量（如 `query`, `response`, `referenceAnswer`）必须完成字段映射，否则无法保存评测任务 | 映射错误将导致评分结果为空或失真 |
| **采样与规模** | 自动评测中，分类采样数（事实型/分析型等）决定最终评测用例总量；单次评测最多支持 8 个应用横向对比 | 多应用评测要求所有应用共享至少一个知识库 |
| **标签类型** | 分类（多选枚举）、布尔（True/False）、数字（0–100 等）、文本（自由输入）四类，影响后续筛选与统计逻辑 | 数字标签需明确评分范围与通过阈值 |

## 使用方式

1. **准备评测数据**：  
   - 新版推荐：在[评测集](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=evalSet)页面选择「智能体」类型 → 关联目标应用 → 下载模板 → 填写后上传；或直接从「应用观测」导入真实流量数据。  
   - 旧版兼容：仍支持上传 `.jsonl`（知识问答）或 `.xlsx`（对话分析）文件，但字段需严格匹配 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md) 规范。

2. **创建评测任务**：  
   - 在[评测任务](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=task)页面新建任务 → 选择已发布评测集及版本 → 关联「智能体」应用 → 添加 1–10 个评估器（需完成全部参数映射）→ 可选添加人工标签。

3. **执行与分析**：  
   - 任务发起后不可修改配置；支持「快速标注」模式逐条人工校验；  
   - 结果页分「数据明细」（含各评估器评分、人工标签）和「指标统计」（综合得分、通过率柱状图、数据分布）；  
   - BadCase 归因由自动评测模块提供（如「检索无效」「切片不完整」），但新版评测任务需依赖评估器组合实现类似分析能力。

## 限制和注意事项

- **权限与依赖**：自动评测要求子账号具备 `管理员` 或 `应用评测-操作` 权限，且目标应用必须已开通「应用观测」并加入观测列表 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **知识库强约束**：自动评测生成评测集及执行评估均依赖知识库内容，若知识库未配置或无公共交集，多应用评测将失败。  
- **[Token](../concepts/token.md) 消耗不可逆**：评测任务分步执行（如评测集生成、模型推理），任一成功步骤均产生 [Token](../concepts/token.md) 费用，即使后续步骤失败亦不退费 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **版本兼容性**：新版评测体系（文档 4/5/6/7）与旧版（文档 1/2/3）并存但不互通；旧版「自动评测」界面已标记为「返回旧版」入口，新项目应优先采用新版架构。  
- **评估器试运行限制**：基于历史评测任务创建的评估器**不支持试运行**，必须部署至评测任务中实测效果 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


