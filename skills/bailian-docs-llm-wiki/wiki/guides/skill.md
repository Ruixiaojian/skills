# skill

Skill 是百炼平台提供的可插拔能力包，用于扩展智能体在对话中自动处理特定任务的能力（如文件解析、数据清洗等），无需额外编码或工具集成。开发者可通过官方 Skill 快速启用通用能力，或通过自定义 ZIP 包构建业务专属 Skill。所有 Skill 均由智能体基于 `description` 语义匹配自动调用，调用准确性高度依赖元信息描述质量。

## 支持的模型/功能

- **官方 Skill**：平台预置、开箱即用的通用能力，覆盖 `.xlsx`/`.csv`/`.tsv` 等文件处理、PDF 文本提取、图像 OCR 等场景，由平台统一维护和更新，已添加的智能体会自动升级至最新版本。  
- **自定义 Skill**：通过上传符合规范的 ZIP 包实现，适用于官方 Skill 未覆盖的垂直场景（如行业专用格式解析、私有 API 封装等）。ZIP 包必须包含根目录下的 `SKILL.md` 文件，并满足 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中定义的结构与字段要求。  
- 所有 Skill 均不依赖特定大模型，其调用逻辑由百炼底层调度引擎根据用户输入语义与 `description` 匹配决定，与所选推理模型无关。

## 关键参数

关键参数全部定义在 ZIP 包根目录的 `SKILL.md` 文件中，采用 YAML 格式：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 唯一标识符，仅允许小写字母、数字和连字符（如 `invoice-parser`），同一账号下不可重复；该字段也作为版本管理的命名依据。 |
| `description` | 是 | **决定 Skill 是否被正确调用的核心字段**。需明确说明适用输入类型、支持操作、典型触发关键词及明确排除的不适用场景。描述质量直接影响匹配准确率，详见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的编写建议与完整示例。 |

> **注意**：`description` 中若未声明“不适用场景”，可能导致误触发；例如 xlsx Skill 明确排除产出 Word 或 HTML 的场景，此约束在 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 的示例中有严格体现，实际编写时必须遵循。

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面查看并添加，无需配置。  
   - 自定义 Skill：按 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 要求准备 ZIP 包（含 `SKILL.md`，≤10 MB），在控制台 **组件 > Skill 管理 > 自定义 Skill** 中上传，系统约 2 分钟完成审查。

2. **添加到智能体**  
   - 方式一：在 Skill 详情页点击 **添加到智能体**，选择目标应用。  
   - 方式二：进入智能体 **应用配置 > 技能** 区域，点击对应 Skill 右侧加号添加。

3. **测试与验证**  
   在应用配置页右侧对话窗格中发送典型指令（如 `帮我清洗这份 CSV 数据，删除重复行并导出`），观察是否触发预期 Skill 并返回正确结果。

## 限制和注意事项

- ZIP 包大小上限为 **10 MB**，超限将导致上传失败。  
- `name` 字段全局唯一（同账号内），重名上传会拒绝，而非覆盖。  
- 自定义 Skill 版本更新需重新上传同名 ZIP 包，旧版本仍保留在历史记录中，但已添加该 Skill 的智能体会**自动切换至最新通过审查的版本**。  
- 官方 Skill 的 `description` 由平台维护，开发者不可修改；若发现官方 Skill 行为与文档描述不符，应以控制台实时展示的描述为准。  
- Skill 调用完全基于 `description` 的语义理解，**不支持正则匹配、硬编码关键词或条件分支逻辑**；复杂业务规则需在 Skill 内部代码中实现，而非依赖 `description` 控制流。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


