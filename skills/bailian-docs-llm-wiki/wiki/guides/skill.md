# skill

Skill 是百炼平台提供的可插拔能力包，用于扩展智能体在对话中自动处理特定任务的能力（如文件解析、数据清洗等），无需额外编码或工具集成。开发者可通过官方 Skill 快速启用通用能力，或通过自定义 ZIP 包构建业务专属 Skill。其核心机制依赖 `SKILL.md` 中的语义描述驱动智能体自动识别与调用，[原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 详细说明了该机制的设计逻辑。

## 支持的模型/功能

- **官方 Skill**：由平台预置并维护，覆盖常见文件处理场景（如 `.xlsx`、`.csv` 解析与生成），开箱即用，无需配置。最新列表请参考控制台 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面，[原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 明确指出其持续更新特性。
- **自定义 Skill**：通过上传符合规范的 ZIP 包实现，适用于行业特有格式（如医疗 DICOM 元数据提取）、私有协议解析等官方未覆盖场景。所有自定义 Skill 均需包含 `SKILL.md` 文件，且必须满足命名唯一性、10 MB 大小限制等要求，详见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 关键参数

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 唯一标识符，仅支持小写字母、数字和连字符（如 `invoice-parser`）；同一账号下不可重复。 |
| `description` | 是 | 决定智能体是否调用该 Skill 的核心依据。必须明确说明：① 支持的输入类型（如 `.pdf`, JSON 数据流）；② 支持的操作（如“提取表格”“转为 Markdown”）；③ 触发关键词（如“帮我导出为 Excel”）；④ **不适用场景**（如“不处理扫描件 OCR”），否则易导致误调用。 |

> **注意**：`description` 的质量直接影响调用准确率，[原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 提供的 xlsx Skill 示例是当前唯一权威参考，其结构（含触发条件、输入输出约束、排除场景）应严格遵循。

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面选择添加。  
   - 自定义 Skill：准备 ZIP 包（含 `SKILL.md` + 可执行代码/配置），在控制台 **组件 > Skill 管理 > 自定义 Skill** 中上传；审查约 2 分钟，通过后即可使用。

2. **添加到智能体**  
   - 方式一：在 Skill 详情页点击 **添加到智能体**，选择目标应用。  
   - 方式二：进入智能体 **应用配置 > 技能** 区域，点击对应 Skill 右侧加号添加。

3. **测试与验证**  
   在应用配置页右侧对话窗格发送典型用户指令（如 `把附件里的销售数据按季度汇总成表格`），观察是否触发 Skill 并返回预期结果（如 `.xlsx` 文件下载链接）。

## 限制和注意事项

- ZIP 包总大小 ≤ 10 MB，超限将被拒绝上传。  
- `name` 字段在账号维度全局唯一，重名上传会失败。  
- 自定义 Skill 更新需重新上传同名 ZIP 包，系统自动创建新版本；已添加该 Skill 的智能体会**自动切换至最新版本**（无需手动刷新配置）。  
- 官方 Skill 版本由平台统一升级，用户无法回滚或修改其 `description`。  
- 当前 Skill 仅支持同步执行（即阻塞式调用），不支持长时异步任务（如小时级数据训练）；此类需求需通过外部服务 + Callback 实现，不在 Skill 范畴内。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


