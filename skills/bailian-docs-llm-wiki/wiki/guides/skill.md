# skill

Skill 是百炼平台提供的可插拔能力包，用于扩展智能体在对话中自动处理特定任务（如文件解析、数据清洗等）的能力，无需额外编码或[工具集成](../concepts/tool-integration.md)。开发者可通过官方 Skill 快速启用通用功能，或通过自定义 ZIP 包构建业务专属能力。所有 Skill 均由智能体基于 `description` 语义匹配触发，调用过程对用户透明。

## 支持的模型/功能

- **官方 Skill**：平台预置、开箱即用的通用能力，覆盖 `.xlsx`/`.csv`/`.pdf` 等常见格式的读写、转换与清洗，由百炼统一维护和更新，详见 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面。  
- **自定义 Skill**：通过上传符合规范的 ZIP 包实现，适用于行业定制场景（如医疗报告解析、金融票据识别）。ZIP 包必须包含根目录下的 `SKILL.md` 文件，且整体大小 ≤10 MB —— 具体要求参见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。  
- 所有 Skill 均不依赖特定大模型底座，其调用逻辑由百炼运行时统一调度，与底层模型解耦。> **注意**：文档中未明确说明 Skill 是否支持[流式输出](../concepts/streaming-output.md)或长上下文输入，实际使用中需以 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中描述的触发行为为准，避免假设非声明能力。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` YAML 字段 | 是 | Skill 唯一标识符，仅限小写字母、数字和连字符（如 `invoice-parser`），同一账号下不可重复 —— 该约束在 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中明确要求。 |
| `description` | `SKILL.md` YAML 字段 | 是 | 决定 Skill 调用准确性的核心字段，需清晰描述适用输入类型、支持操作、触发关键词及**不适用场景**（如“勿用于生成 HTML 报告”）。描述质量直接影响语义匹配效果。 |
| 版本号 | 控制台 Skill 详情页 | 自动生成 | 官方 Skill 版本由平台自动升级；自定义 Skill 每次重新上传同名 ZIP 即生成新版本，已绑定应用将自动切换至最新版。 |

## 使用方式

1. **添加 Skill**：  
   - 方式一：在 [Skill 管理](../../raw/application-user-guide/skill/introduction-to-skill.md) 页面点击目标 Skill 卡片 → “添加到智能体” → 选择应用；  
   - 方式二：进入目标智能体的“应用配置” → “技能”区域 → 点击 `+` → 从列表选取。  

2. **测试效果**：在应用配置页右侧对话窗格中发送典型触发语句（如“把附件里的销售数据转成 Excel 并按季度汇总”），观察是否自动调用并返回预期结果（如 `.xlsx` 文件下载链接）。  

3. **更新自定义 Skill**：修改本地 ZIP 包（尤其 `SKILL.md` 的 `description`）后，重新上传同名包即可发布新版本，无需手动更新已绑定应用。

## 限制和注意事项

- ZIP 包大小上限为 **10 MB**，超限将导致审查失败；  
- `name` 字段全局唯一（同一阿里云账号内），重名上传会报错；  
- `description` 中若未明确排除不适用场景（如“勿用于数据库同步”），可能导致误触发 —— 这是 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 强调的关键实践；  
- 官方 Skill 不支持修改 `description` 或元信息，仅能通过平台更新获得新版本；  
- 自定义 Skill 审查耗时约 2 分钟，失败时需根据控制台提示修正 `SKILL.md` 后重试。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


