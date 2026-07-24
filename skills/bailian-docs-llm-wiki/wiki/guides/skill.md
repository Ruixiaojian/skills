# skill

Skill 是百炼平台提供的可插拔能力包，用于扩展智能体在对话中自动处理特定任务的能力（如文件解析、数据清洗等），无需开发者编写集成代码。官方 Skill 开箱即用，自定义 Skill 支持通过 ZIP 包上传实现业务定制。其核心机制依赖 `SKILL.md` 中的语义描述驱动智能体自动识别与调用 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **官方 Skill**：平台预置、统一维护的通用能力，覆盖 `.xlsx`/`.csv`/`.tsv` 等常见文件格式的读写、编辑、转换与清洗，无需配置即可添加使用。最新列表请参考控制台 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。
- **自定义 Skill**：通过上传符合规范的 ZIP 包创建，适用于行业专属格式解析、定制化数据处理等场景。ZIP 包必须包含根目录下的 `SKILL.md` 文件，并满足命名唯一性、10 MB 大小限制等要求 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 关键参数

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 唯一标识符，仅支持小写字母、数字和连字符（如 `invoice-parser`）；同一账号下不可重名。 |
| `description` | 是 | 决定智能体调用准确性的核心字段，需明确说明：① 输入类型（如 `.pdf` 文本提取）、② 支持操作（如“提取表格”“OCR 识别”）、③ 触发关键词（如“转成 Excel”“识别发票”）、④ 不适用场景（如“不处理扫描件以外的图片”）。 |

> **注意**：`description` 的表述质量直接影响调用召回率与误触发率，建议严格按示例结构编写，避免模糊或过度泛化描述。

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面选择添加。  
   - 自定义 Skill：打包含 `SKILL.md` 的 ZIP 文件，在控制台 **组件 > Skill 管理 > 自定义 Skill** 中上传，审查通过后即可使用。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击 **添加到智能体**，选择目标应用。  
   - 方式二：进入智能体 **应用配置 > 技能** 区域，点击对应 Skill 右侧加号添加。

3. **测试与验证**  
   在应用配置页右侧对话窗格输入典型触发语句（如 `把附件里的 CSV 按销售额排序并导出为 Excel`），观察是否自动调用 Skill 并返回预期结果。

## 限制和注意事项

- ZIP 包总大小 ≤ 10 MB，且 `SKILL.md` 必须位于根目录。
- 自定义 Skill 名称全局唯一，重复上传同名包将创建新版本，已绑定该 Skill 的智能体会自动升级至最新版。
- 官方 Skill 版本由平台自动更新，用户无法手动回滚；自定义 Skill 版本需通过重新上传 ZIP 包更新。
- `description` 中若未明确排除不适用场景（如“不处理加密 PDF”），可能导致误调用——务必在描述中显式声明限制条件。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


