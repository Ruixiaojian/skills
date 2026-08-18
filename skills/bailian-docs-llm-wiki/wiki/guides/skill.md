# skill

Skill 是百炼平台提供的可插拔能力包，用于赋予智能体自动处理特定任务（如文件解析、数据清洗、格式转换等）的能力，无需开发者编写集成代码。通过声明式描述（`SKILL.md`）定义触发条件与行为边界，智能体可在对话中自主识别并调用匹配的 Skill。官方 Skill 开箱即用，自定义 Skill 支持 ZIP 包上传扩展业务场景。

## 支持的模型/功能

- **官方 Skill**：由平台预置并统一维护，覆盖常见文件处理场景（如 `xlsx`、`pdf`、`csv` 等），无需配置即可添加使用。最新列表请见 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面，其更新策略详见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。
- **自定义 Skill**：通过上传符合规范的 ZIP 包创建，适用于官方 Skill 未覆盖的垂直场景（如行业专用报表生成、私有协议解析）。ZIP 包必须包含根目录下的 `SKILL.md` 文件，且整体大小 ≤10 MB —— 具体要求参见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。
- 所有 Skill 均不依赖特定大模型，而是作为独立执行单元被智能体调度；调用逻辑基于 `description` 的语义匹配，与底层模型无关。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` YAML 字段 | 是 | Skill 唯一标识符，仅支持小写字母、数字和连字符（如 `invoice-parser`），同一账号下不可重复。 |
| `description` | `SKILL.md` YAML 字段 | 是 | **决定 Skill 是否被调用的核心字段**。需明确说明适用输入类型、支持操作、典型触发关键词及明确排除的不适用场景。质量直接影响调用准确率，编写建议详见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。 |
| 版本号 | 平台自动生成 | 否 | 官方 Skill 版本由平台管理；自定义 Skill 每次同名 ZIP 上传即生成新版本，历史版本可在详情页「概览」标签中切换查看。 |

> **注意**：`description` 中若未明确排除“产出非文件类结果”（如生成 Python 脚本或调用外部 API），可能导致误触发。务必按示例严格声明不适用场景，否则智能体会因语义模糊而错误调用。

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击添加。  
   - 自定义 Skill：准备含 `SKILL.md` 的 ZIP 包 → 控制台 **组件 > Skill 管理 > 自定义 Skill** → 上传 → 等待约 2 分钟审查（失败时按提示修改重传）。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击 **添加到智能体**，选择目标应用。  
   - 方式二：进入智能体 **应用配置 > 技能** 区域，点击对应 Skill 右侧 `+` 号添加。

3. **测试效果**  
   在应用配置页右侧对话窗格中输入典型用户指令（如 `帮我把这份 PDF 表格转成 Excel`），观察是否自动调用并返回预期结果（如 `.xlsx` 文件下载链接）。

## 限制和注意事项

- **大小限制**：自定义 Skill ZIP 包总大小 ≤10 MB，超限将导致上传失败。
- **命名冲突**：同一阿里云账号下，`name` 字段值全局唯一；重复上传同名包会创建新版本，但不会覆盖旧版。
- **调用可靠性**：Skill 调用完全依赖 `description` 的语义匹配精度。若描述过于宽泛（如仅写“处理表格”），易与其他 Skill 冲突或误触发；务必参考 `xlsx` Skill 的完整示例进行编写。
- **版本生效**：官方 Skill 更新后，已添加的应用**自动生效最新版本**；自定义 Skill 更新需重新上传，且已添加的应用**立即使用新版本**（无缓存延迟）。
- **调试支持**：当前不提供 Skill 运行时日志或中间状态输出，调试主要依赖 `description` 优化与对话测试验证。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


