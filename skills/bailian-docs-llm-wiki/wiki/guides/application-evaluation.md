# application evaluation

应用评测是百炼平台用于系统化评估智能体（或工作流）应用输出质量的核心能力，支持从自动评分到人工标注的全链路质量验证。它既可通过大模型自动生成评测集并完成端到端打分（自动评测），也支持基于人工构建的评测集进行多维度标注与分析（手动评测）。评测结果可直接驱动 Prompt 优化、知识库切片调整及 RAG 配置迭代，形成“评测—归因—优化—再评测”的闭环。

## 支持的模型与功能

- **自动评测**：依赖 `qwen-max` 和 `qwen-plus` 模型生成评测集并执行评分，不支持其他模型 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)；该能力仅面向已发布且配置知识库的智能体应用，并要求开通「应用观测」功能。
- **手动评测**：不依赖特定模型，由人工对应用输出进行打标（如“较差/一般/较好”或1–5分），适用于需主观判断的场景 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **新版评测体系**：引入「评估器（Grader）」和「标签（Label）」两大核心组件，支持 LLM 与 Code 双模评估器、四类标签类型（分类/布尔/数字/文本），并兼容智能体、工作流与自定义应用类型 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。

> **注意**：文档 4（新版评测集）与文档 3（旧版评测集）在评测集类型定义上存在差异——前者将评测集划分为「智能体」「工作流」「自定义」三类，后者则按数据语义划分为「对话分析」与「知识问答」两类。实际使用中，新版体系已逐步替代旧版，但旧版自动评测仍依赖「知识问答」格式的 `.jsonl` 评测集，二者不兼容。建议新项目统一采用新版评测任务流程。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **评测集类型** | 决定数据结构与适用场景：`智能体`/`工作流`/`自定义`（新版）；或 `对话分析`（`.xls`/`.xlsx`）与 `知识问答`（`.jsonl`）（旧版） | 创建后不可修改类型；旧版自动评测仅支持 `知识问答` 类型 |
| **评估器参数映射** | 将评估器中声明的变量（如 `query`, `response`, `referenceAnswer`）绑定至评测集字段或应用输出字段 | 所有变量必须完成映射，否则无法保存评测任务 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md) |
| **标签类型** | 分类（多选枚举）、布尔（True/False）、数字（0–100等）、文本（自由输入） | 影响标注方式与筛选逻辑，需根据评测目标预设 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md) |
| **采样数与权重** | 自动评测中可为各任务类型（事实型/分析型等）设置采样数；新版评测任务支持为每个评估器配置权重 | 旧版自动评测中分类采样数总和即为评测总数；新版权重影响指标统计中的综合得分计算 |

## 使用方式

1. **准备评测数据**  
   - 自动评测：通过知识库自动生成 `.jsonl` 格式评测集，需确保知识库已配置且内容覆盖业务场景 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
   - 手动评测：下载模板填写 `.xls`/`.xlsx` 文件，上传后发布为「对话分析」评测集 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。  
   - 新版评测：可手动上传 Excel 模板，或从「应用观测」中导入真实调用数据，支持增量导入与版本管理 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。

2. **创建评测任务**  
   - 旧版：在「自动评测」或「手动评测」页面依次完成「选择应用→设置评测集→配置规则→发起评测」四步流程。  
   - 新版：在「评测任务」页面选择评测集、关联应用（智能体/工作流/不关联）、添加评估器（最多10个）与标签，完成参数映射后创建 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。

3. **执行与分析**  
   - 自动评测：系统自动运行，生成含总正确率、BadCase 归因（如“检索无效”“切片不完整”）、RAG 各环节得分的报告。  
   - 手动/新版评测：进入「数据明细」页逐条标注，或启用「快速标注」模式批量操作；「指标统计」页提供综合得分仪表盘、各评估器通过率柱状图及标签分布分析。

## 限制和注意事项

- **应用状态限制**：自动评测仅支持已发布的智能体应用，且必须关联至少一个知识库；未发布或无知识库的应用无法参与 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **并发与规模限制**：单次自动评测最多支持 8 个应用横向对比；评测集生成与执行均为离线任务，排队期间进度显示为 0%，属正常现象。
- **权限要求**：子账号需具备 `管理员` 或 `应用评测-操作` 权限，否则无法访问评测功能 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **费用说明**：自动评测、新版评测任务调用大模型产生的 [Token](../concepts/token.md) 按实际用量计费；Code 评估器无额外费用；手动评测中若启用公共资源部署模型，也会产生 [Token](../concepts/token.md) 费用 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。
- **评测集一致性**：复用已有评测集时，必须确保其参考答案能在当前指定知识库中召回，否则自动评测结果失真 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


