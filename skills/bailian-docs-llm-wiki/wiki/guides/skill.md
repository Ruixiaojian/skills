# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可复用能力包，支持在不编写代码的前提下，让智能体自动识别并执行[文件处理](../concepts/file-processing.md)、数据分析等专业任务。Skill 分为平台预置的官方 Skill 和用户自主开发的自定义 Skill 两类，均通过语义描述驱动调用决策。其核心机制依赖于 `SKILL.md` 中的 `description` 字段对触发条件与能力边界的精准刻画，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **适用模型**：Skill 当前仅支持接入基于百炼大模型（如 Qwen 系列）构建的智能体应用，不适用于纯规则引擎或非百炼托管的推理服务。
- **核心功能**：
  - 自动识别用户意图与输入文件/数据特征，匹配最相关的 Skill；
  - 执行文件解析（如 PDF、Excel、CSV）、结构化数据清洗、格式转换、表格生成等操作；
  - 输出结果以文件形式返回（如 `.xlsx`、`.pdf`），不支持直接返回数据库写入、API 调用或外部系统状态变更；
  - 官方 Skill（如 `xlsx`、`pdf-parser`）由平台统一维护，[Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中列出了当前覆盖的常见场景。

> **注意**：原始文档未明确说明 Skill 是否支持流式响应或长时任务（如小时级数据处理）。实际使用中，所有 Skill 执行受单次调用超时限制（默认 120 秒），超出将中断并报错——该限制未在 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中体现，需开发者自行验证。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` 根字段 | 是 | Skill 唯一标识符，须全小写+连字符（如 `invoice-parser`），同一账号下不可重复。 |
| `description` | `SKILL.md` 根字段 | 是 | **决定调用准确性的关键字段**。必须包含适用输入类型、支持操作、典型触发关键词、明确的不适用场景四要素；描述模糊将导致误调或漏调。 |
| ZIP 包大小 | 上传时校验 | — | ≤ 10 MB，超限拒绝上传。 |

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面启用，无需配置。  
   - 自定义 Skill：按规范编写 `SKILL.md`，打包为 ZIP（根目录含该文件），通过控制台「组件 > Skill 管理 > 自定义 Skill」上传。审查约 2 分钟，通过后即可使用。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击「添加到智能体」，选择目标应用；  
   - 方式二：在智能体「应用配置 > 技能」区域点击 `+`，勾选所需 Skill。

3. **测试与验证**  
   在应用配置页右侧对话窗格中发送典型指令（如 `把附件里的 CSV 按销售额排序并导出为 Excel`），观察是否触发对应 Skill 并正确返回文件。

## 限制和注意事项

- **版本更新行为差异**：官方 Skill 更新后，已添加的应用**自动生效最新版**；自定义 Skill 更新需重新上传同名 ZIP，且**已添加的应用立即切换至新版本**（无灰度或回滚机制）。
- **description 无语法校验**：`SKILL.md` 中 `description` 字段内容不经过 NLP 模型预检，仅作为提示词输入给大模型。若描述存在歧义、矛盾或缺失否定场景（如未声明“不处理图片”），将显著增加误调用概率。
- **文件输入约束**：Skill 仅能处理用户显式上传的文件或对话中引用的附件，**无法主动访问用户本地磁盘、云存储路径或数据库连接**；路径引用（如“下载目录中的 report.xlsx”）仅在用户已上传该文件前提下有效。
- **输出强制为文件**：所有 Skill 的最终交付物必须是生成的文件（如 `.xlsx`, `.pdf`），不支持纯文本摘要、JSON 结构化数据或嵌入式图表渲染——此限制在原始文档中隐含但未明示。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


