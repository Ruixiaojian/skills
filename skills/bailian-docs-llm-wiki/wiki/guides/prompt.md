# prompt

阿里云百炼平台提供了一套完整的 Prompt 工程工具链，涵盖模板管理、自动优化、样例库引导和反馈优化等功能，帮助开发者高效构建、管理和迭代 Prompt。通过将 Prompt 的固定结构与动态变量分离，开发者可以实现 Prompt 的统一管理和复用，提升大模型应用的输出质量和稳定性。

> **注意**：以下功能仅适用于中国大陆版（北京地域）。

## 功能概览

百炼平台围绕 Prompt 提供四项核心能力：

| 功能 | 说明 | 适用场景 |
|------|------|----------|
| **Prompt 模板** | 创建可复用的结构化模板，支持变量填充 | Prompt 统一管理、团队协作、版本控制 |
| **Prompt 自动优化** | 大模型对原始 Prompt 进行结构重组和指令增强 | 快速提升已有 Prompt 的质量 |
| **Prompt 样例库** | 基于少样本学习，从预定义问答对中检索相关样例注入上下文 | 智能客服、领域知识问答、格式化内容生成 |
| **Prompt 反馈优化** | 基于用户提供的输入输出样例，多轮评估并自动生成优化 Prompt | 需要精确匹配业务预期的分类、抽取等任务 |

> **注意**：据 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 所述，Prompt 样例库功能**已不再维护**，推荐将样例库数据迁移到 RAG 表格库中。

## Prompt 模板

### 模板类型

Prompt 模板分为**预置模板**和**自定义模板**两类，详见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)：

- **预置模板**：由百炼平台提供，覆盖营销文案、摘要抽取、文案润色等通用场景，已经过优化，不支持修改。
- **自定义模板**：用户自行创建，适用于复杂或特定业务需求（如金融风控、医疗咨询），支持迭代修改。

### 模板工作流程

1. **创建模板**：通过控制台或 `CreatePromptTemplate` API 创建并保存，获取唯一 `promptTemplateId`。
2. **获取模板**：通过 `GetPromptTemplate` API 使用 `workspaceId` + `promptTemplateId` 拉取模板内容。
3. **生成 Prompt**：将业务数据填入模板变量，生成最终 Prompt。
4. **调用模型**：将生成的 Prompt 发送给目标模型获取结果。

### 创建自定义模板

自定义模板支持**文本生成**和**图片生成**两种类型，详见 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。

**文本生成模板**提供两种输入模式：

- **自定义创建**：直接输入已有 Prompt，可使用平台的"优化 Prompt"功能进行润色。
- **基于 Prompt 工程创建**：选择内置框架（ICIO / CRISPE / RASCEF）进行结构化设计。

| 框架 | 适用场景 |
|------|----------|
| ICIO（指令-背景-数据-输出格式） | 简单明确的任务：数据分析、内容生成、文本摘要 |
| CRISPE（角色-背景-任务-风格-范围） | 需要角色扮演的交互：客服、创意写作、面试模拟 |
| RASCEF（角色-行动-步骤-上下文-示例-格式） | 多步骤复杂业务流程：项目规划、战略分析 |

**图片生成模板**支持分别定义正向 Prompt（应包含的内容）和负向 Prompt（应排除的内容）。

### 使用模板的优势

相比在代码中直接拼接字符串，使用 `GetPromptTemplate` API 管理 Prompt 的优势包括：

- **逻辑与内容分离**：在控制台更新 Prompt 内容无需修改或重新部署代码。
- **集中管理与协作**：所有 Prompt 集中存储，便于团队协作和版本管理。
- **一致性保障**：确保不同服务间使用的 Prompt 版本一致。

## Prompt 自动优化

Prompt 自动优化利用大模型对用户提交的 Prompt 进行重构，优化策略包括：

- **结构重组**：调整整体结构使其更符合逻辑
- **角色扮演引导**：设定明确的专家角色
- **指令增强**：将模糊指令具体化、步骤化
- **安全与边界注入**：增加输出格式、内容限制等边界条件

操作路径：**应用开发 > 组件管理 > 提示词 > 自动优化**

优化结果可直接复制使用，也可保存为模板纳入提示词库。

> 该功能**不计费**。优化失败可能由输入内容过长、触发安全审核或网络问题导致。

## 基于样例的 Prompt 反馈优化

相较于上述自动优化仅对 Prompt 文本本身做改写，[基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md) 会结合用户提供的实际数据进行多轮评估和迭代，生成在具体业务场景中表现更优的 Prompt。

### 关键参数

| 参数 | 说明 | 建议 |
|------|------|------|
| 推理模型 | 用于多轮 Prompt 评测的模型 | 推荐选择 **千问-max** |
| 样例数据 | 自动添加到优化后 Prompt 中的高质量问答对 | 5~10 条，每种场景至少 1 条 |
| 评测数据 | 作为评估最优 Prompt 的标准 | 至少 20 条，越多效果越好 |
| 初始 Prompt | 需要优化的原始 Prompt | 只需描述任务目标 |

操作路径：**提示词 > 反馈优化 > 新增优化任务**

优化完成后，支持将结果**保存为 Prompt 模板**或直接**创建智能体应用**。

## Prompt 样例库（已停止维护）

> **注意**：该功能已不再维护，建议迁移至 RAG 表格库。

样例库通过少样本学习思路，从预定义的高质量问答对中检索相关样例注入模型上下文，引导生成更准确、风格一致的回复。

### 使用限制

| 限制项 | 值 |
|--------|-----|
| 单个样例库最大样例数 | 300 条 |
| 单个应用最多关联样例库数 | 5 个 |
| 单次请求最大召回片段数 | 10 个（默认 5，可配置） |
| 批量导入文件大小 | ≤ 20MB（Excel 格式） |
| 单次导入最大样例数 | 100 条 |

### 计费说明

样例库功能本身不收费，但启用后会增加大模型调用的 Token 消耗：

**总输入 Token ≈ 用户查询 Token + 所有召回样例的总 Token + 系统指令 Token**

## 关键 API 参数

使用 Prompt 相关 API 时需要的核心参数：

| 参数 | 说明 | 获取方式 |
|------|------|----------|
| `workspaceId` | 业务空间 ID | 控制台"获取 APP ID 和 Workspace ID" |
| `promptTemplateId` | Prompt 模板 ID | 创建模板后在模板卡片上获取 |
| `accessKeyId` / `accessKeySecret` | 阿里云访问凭证 | 阿里云 AccessKey 管理 |
| `has_thoughts` | 是否返回推理过程（应用 API） | 设为 `true` 可查看样例检索详情 |

## 错误处理

调用 Prompt 相关 API 失败时，请参见百炼平台错误码文档进行排查。常见失败原因包括输入内容超出 Token 限制、触发内容审核策略、网络问题等。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)

