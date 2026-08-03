# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可复用能力包，支持在不编写代码的前提下，让智能体自动识别并执行文件处理、数据分析等专业任务。Skill 分为平台预置的官方 Skill 和用户自主开发的自定义 Skill 两类，均通过语义描述驱动调用决策。其核心机制依赖于 `SKILL.md` 中的 `description` 字段对触发条件与能力边界的精准刻画，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **适用模型**：Skill 当前仅支持接入基于百炼大模型（如 Qwen 系列）构建的智能体应用，不适用于纯规则引擎或非百炼托管的推理服务。
- **核心功能**：
  - 自动识别用户意图与输入文件/数据特征，匹配最相关的 Skill；
  - 执行文件解析（如 PDF、XLSX、CSV）、格式转换、结构化清洗、表格生成等操作；
  - 输出结果以文件形式返回（如 `.xlsx`, `.pdf`, `.json`），不支持流式响应或中间状态交互；
  - 官方 Skill（如 `xlsx`、`pdf-reader`）由平台统一维护，功能稳定且持续迭代；自定义 Skill 的行为完全由 ZIP 包内代码与 `SKILL.md` 描述共同决定。

> **注意**：原始文档中未明确说明 Skill 是否支持多模态输入（如图像+文本混合指令），但根据 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中所有示例均为文本+文件组合，当前版本暂不支持纯图像输入触发 Skill，该限制需在开发自定义 Skill 时主动规避。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` 根级字段 | 是 | Skill 唯一标识符，须全小写、仅含字母/数字/连字符（如 `invoice-parser`），同一账号下不可重复。 |
| `description` | `SKILL.md` 根级字段 | 是 | **最关键参数**：决定智能体是否调用该 Skill。必须清晰声明适用输入类型、支持操作、典型触发关键词及明确排除场景。质量直接影响召回率与误触发率。参考 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中 xlsx 示例的完整结构。 |
| ZIP 包大小 | 上传时校验 | — | ≤ 10 MB，超限将被拒绝。 |

## 使用方式

1. **创建 Skill**：
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面查看并添加；
   - 自定义 Skill：准备符合规范的 ZIP 包（含 `SKILL.md` 及可执行逻辑），在控制台 **组件 > Skill 管理 > 自定义 Skill** 中上传。

2. **添加到智能体**：
   - 方式一：从 Skill 详情页点击 **添加到智能体**，选择目标应用；
   - 方式二：进入智能体 **应用配置 > 技能** 区域，点击 `+` 号选择 Skill。

3. **测试验证**：
   - 在应用配置页右侧对话窗格中发送典型指令（如 `帮我把附件里的 CSV 按销售额排序并导出为 Excel`），观察是否触发对应 Skill 并正确返回文件。

## 限制和注意事项

- **版本更新行为差异**：官方 Skill 更新后，已添加的应用**自动生效最新版本**；而自定义 Skill 需重新上传同名 ZIP 包才生成新版本，且已添加的应用**立即切换至新版本**（无灰度期），请确保向后兼容。
- **description 误写风险高**：若 `description` 中遗漏“不适用场景”或触发关键词覆盖不足，将导致 Skill 被错误调用或完全不触发。强烈建议按文档示例组织描述，避免模糊表述（如“处理数据”应改为“清洗含缺失值和重复行的 CSV 表格，并输出去重后的 .xlsx”）。
- **调试支持有限**：当前平台不提供 Skill 运行时日志或中间变量查看能力，排查失败需依赖 `description` 语义合理性验证与 ZIP 内代码本地测试。
- **安全约束**：自定义 Skill 运行于沙箱环境，禁止访问外网、读写宿主机文件系统、执行系统命令；ZIP 包中不得包含二进制可执行文件（`.exe`, `.so` 等），仅支持 Python 脚本及依赖（需满足 `requirements.txt` 规范）。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


