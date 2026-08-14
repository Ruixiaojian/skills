# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，支持无需编码即可为智能体赋予文件处理、数据分析等专业功能。它通过语义匹配自动触发，开发者可选用平台预置的官方 Skill，或基于 ZIP 包定义自定义 Skill。所有 Skill 均需通过 `SKILL.md` 描述其能力边界，该描述直接影响智能体调用的准确性 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **官方 Skill**：由平台统一维护，覆盖常见文件处理场景（如 `.xlsx`、`.csv` 解析与生成），开箱即用，无需配置；版本更新后已添加的应用将自动升级 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。  
- **自定义 Skill**：通过上传符合规范的 ZIP 包创建，适用于行业定制需求（如特定格式发票解析、内部数据清洗逻辑）。其行为完全由 `SKILL.md` 中的 `description` 字段驱动，不依赖代码逻辑或模型选型——当前所有 Skill 均运行于统一推理调度层，**不绑定具体大模型实例**。  
> **注意**：原始文档未明确说明 Skill 是否支持多模型路由或模型级参数控制；实际调用中 Skill 本身无模型选择项，其执行依赖智能体所配置的基础模型，因此“支持的模型”实为智能体层级配置项，非 Skill 自身属性。

## 关键参数

唯一需显式声明的关键参数均位于 ZIP 包根目录的 `SKILL.md` 文件中，采用 YAML 格式：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 全局唯一标识符，仅限小写字母、数字和连字符（如 `pdf-summarizer`）；同一账号下不可重名。 |
| `description` | 是 | **核心字段**：决定智能体是否触发该 Skill。必须包含适用输入类型、支持操作、典型触发关键词及明确的不适用场景，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的完整示例。 |

ZIP 包本身无其他运行时参数；`description` 的表述质量直接关联调用准确率，建议避免模糊表述（如“处理文档”），而应具体到文件格式、动作动词和否定约束。

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面直接查看并添加。  
   - 自定义 Skill：准备含 `SKILL.md` 的 ZIP 包（≤10 MB），在控制台 **组件 > Skill 管理 > 自定义 Skill > 上传**，系统约 2 分钟完成审查。  

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击 **添加到智能体**，选择目标应用；  
   - 方式二：进入智能体 **应用配置 > 技能** 区域，点击 Skill 右侧 `+` 号添加。  

3. **验证效果**  
   在应用配置页右侧对话窗格中发送符合 `description` 触发条件的请求（如 `把附件里的销售数据转成带图表的 Excel`），观察是否自动调用并返回预期文件。

## 限制和注意事项

- **大小限制**：ZIP 包总大小 ≤10 MB，超限将导致上传失败。  
- **命名冲突**：同账号下 `name` 字段全局唯一，重复上传同名包将创建新版本，旧版本仍保留在历史记录中。  
- **描述敏感性**：`description` 中缺失“不适用场景”易引发误触发（如将 PDF 转 Word 任务错误调用 xlsx Skill）；务必按规范覆盖否定条件。  
- **版本生效机制**：官方 Skill 更新后自动生效；自定义 Skill 需重新上传 ZIP 才能更新，且**已添加的应用立即切换至新版本**，无灰度或回滚界面。  
> **注意**：原始文档称“审查未通过请根据提示修改后重新上传”，但未说明提示内容的具体位置（控制台无内联错误定位），实践中需结合审查失败日志与 `SKILL.md` 格式校验工具排查。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


