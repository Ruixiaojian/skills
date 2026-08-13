# skill

Skill 是百炼平台提供的可插拔能力包，用于扩展智能体在对话中自动处理特定任务的能力（如文件解析、数据清洗等），无需开发者编写集成代码。官方 Skill 开箱即用，自定义 Skill 支持通过 ZIP 包上传实现业务定制。其核心机制依赖 `SKILL.md` 中的语义描述驱动智能体自动识别与调用 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **官方 Skill**：平台预置、统一维护的通用能力，覆盖 `.xlsx`, `.csv`, `.pdf`, `.docx` 等常见格式的读写、转换、清洗等操作，无需配置即可添加使用。最新列表请参考控制台 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。
- **自定义 Skill**：通过 ZIP 包上传实现，适用于行业专属逻辑（如医疗报告结构化解析、金融报表校验）。ZIP 包必须包含根目录下的 `SKILL.md` 文件，并满足 10 MB 大小限制与名称唯一性要求 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 关键参数

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 唯一标识符，仅支持小写字母、数字和连字符（如 `invoice-parser`）；同一账号下不可重名。 |
| `description` | 是 | 决定智能体调用准确性的核心字段，需明确说明：① 支持的输入类型（如 `.xlsx`, `.csv`）；② 可执行操作（如“计算公式”“修复表头”）；③ 触发关键词（如“生成表格”“清洗数据”）；④ **不适用场景**（如“不输出 HTML 报告”），避免误触发。 |

> **注意**：`description` 的完整性直接影响调用效果，示例中 xlsx Skill 的描述长达 200+ 字，明确排除了 Word、Python 脚本等非目标产出物——实践中若描述过于简略（如仅写“处理 Excel”），将导致高误触发率。

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击添加。  
   - 自定义 Skill：打包含 `SKILL.md` 的 ZIP 文件，在控制台 **组件 > Skill 管理 > 自定义 Skill** 中上传，审查通过后即可使用（约 2 分钟）。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击 **添加到智能体**，选择目标应用。  
   - 方式二：进入智能体 **应用配置 > 技能** 区域，点击 Skill 右侧 `+` 号添加。

3. **更新与版本管理**  
   - 官方 Skill：自动更新至最新版本，已添加的应用即时生效。  
   - 自定义 Skill：重新上传同名 ZIP 包即创建新版本，已添加的应用自动切换至最新版。

## 限制和注意事项

- ZIP 包总大小 ≤ 10 MB，且 `SKILL.md` 必须位于 ZIP 根目录。
- `name` 字段全局唯一（同一阿里云账号内），重复上传将被拒绝。
- 自定义 Skill 审查失败时，需根据错误提示修改 `SKILL.md` 后重传，常见原因包括 YAML 格式错误、`description` 缺失或为空。
- 智能体调用 Skill 依赖 `description` 的语义匹配，**不支持显式指令调用**（如 `/use xlsx`），也不支持运行时传参控制行为。
- 当前所有 Skill 均以异步方式执行，返回结果为文件下载链接或结构化数据，不支持流式响应。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


