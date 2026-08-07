# application evaluation

应用评测是百炼平台用于系统化评估智能体或工作流应用输出质量的核心能力，支持自动与手动两种评测范式。自动评测基于知识库自动生成评测集并调用大模型完成端到端评分与归因分析；手动评测则依赖人工构建评测集并结合人工标注与自动化评估器进行多维度评价。二者可独立使用，也可组合形成“自动初筛 + 人工复核 + 评估器固化”的闭环优化流程。

## 支持的模型/功能

- **自动评测**：仅支持 `qwen-max` 和 `qwen-plus` 模型用于评测集生成与最终评分，不支持其他模型 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。该限制适用于评测集生成阶段和评测规则配置阶段。
- **评估器（Grader）**：支持 LLM 评估器（可选 `qwen-max`、`qwen-plus` 等百炼托管模型）和 Code 评估器（无模型依赖，零 [Token](../concepts/token.md) 成本），且 LLM 评估器在创建时明确标注“评估模型限时免费” [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **评测集类型**：支持三类结构化评测集——**智能体**（适配智能体出入参）、**工作流**（适配工作流出入参）和**自定义**（任意字段定义），类型创建后不可修改 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。
- **评测任务模式**：支持关联智能体/工作流应用的自动推理评测，也支持“不关联应用”的纯人工标注场景，后者常用于历史数据回溯分析或专家评审 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。

> **注意**：文档 7 将评测集分为“对话分析”和“知识问答”两类，并限定知识问答仅用于自动评测、对话分析仅用于手动评测；但文档 3 明确支持“智能体”“工作流”“自定义”三类，且未绑定评测方式。实际平台中，**智能体类型评测集既可用于自动评测（如通过观测数据导入），也可用于手动评测（如上传 Excel）**，因此文档 7 的分类已过时，应以文档 3 的三类结构为准。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **评测集采样数** | 在自动评测中，按任务类型（事实型/分析型/比较型/教程型）分别设置采样数量，总评测数 = 各类型采样数之和 | 单类型最小为 0，最大未明示；总样本数影响 [Token](../concepts/token.md) 消耗与耗时 |
| **评估器参数映射** | 在评测任务中，必须将评估器声明的变量（如 `query`, `response`, `referenceAnswer`）1:1映射至评测集字段或应用输出字段 | 所有变量必须完成映射，否则无法保存任务 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md) |
| **标签类型** | 支持分类、布尔值、数字、文本四类，直接影响标注方式与筛选能力 | 分类标签最多 20 个选项；数字标签建议设为 `Double` 类型以兼容小数评分 |
| **评分范围与阈值** | LLM/Code 评估器均需配置评分范围（如 `0-1` 或 `1-5`）及通过阈值（如 `≥0.8` 判定为 Pass） | 范围需与 Prompt 中的指令严格一致，否则导致逻辑冲突 |

## 使用方式

1. **准备数据基础**  
   - 创建并**发布**评测集：支持手动上传（XLS/XLSX/JSONL）或从应用观测导入；草稿状态不可用于评测 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。  
   - （可选）创建自定义标签或评估器：标签用于人工维度标注，评估器用于自动评分，二者可在评测任务中同时启用 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)、[评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。

2. **发起评测任务**  
   - **自动评测**：选择已发布且配置知识库的智能体应用 → 生成或选用评测集 → 设置分类采样数与评测模型 → 发起任务 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
   - **手动评测**：选择已发布评测集 → 配置评测维度（内置或自定义模板）→ 启动推理 → 进入人工“打标”环节逐条对比并评分 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。  
   - **新版评测任务**：统一入口创建任务，灵活选择“智能体/工作流/不关联应用”，并叠加多个评估器与标签 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。

3. **分析与迭代**  
   - 查看自动评测报告中的 BadCase 归因（如“检索无效”“切片不完整”）并针对性优化知识库或 RAG 配置；  
   - 在手动/新版任务中，利用标签筛选（如 `错误类型 == "事实错误"`）快速定位共性问题；  
   - 基于高质量人工标注数据，使用“基于评测任务创建评估器”功能将专家经验转化为可复用的 LLM 评估器 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。

## 限制和注意事项

- **权限要求**：子账号需具备 `管理员` 或 `应用评测-操作` 权限方可使用自动评测功能 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **应用状态约束**：所有评测模式均**仅支持已发布的智能体应用**；未发布应用无法被选中，且自动评测强制要求应用已开通“应用观测”并加入观测列表。  
- **规模限制**：  
  - 自动评测最多支持 **8 个应用**参与横向对比；  
  - 单次评测集上传最多 **10 个文件**，单文件 ≤ 20 MB；  
  - 单评测任务最多添加 **10 个评估器**。  
- **[Token](../concepts/token.md) 消耗提示**：  
  - 自动评测中“预估平均消耗”仅为参考值，实际用量以账单为准；“预估最大消耗”是硬性成本上限，实际极少达到 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)；  
  - 手动评测与新版评测任务中，调用大模型产生的 Token 正常计费，独占资源部署模型除外 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  
- **版本与兼容性**：  
  - 新版评测任务（文档 4/5/6）与旧版自动评测（文档 1）并存，用户可通过页面左上角“返回旧版”切换；  
  - 旧版自动评测生成的评测集（JSONL 格式）可被新版任务直接引用，但新版创建的“智能体/工作流”类型评测集不向下兼容旧版界面。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)


