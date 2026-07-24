# skill

Skill 是百炼平台提供的可插拔能力包，用于赋予智能体自动处理特定任务（如文件解析、数据清洗、格式转换等）的能力，无需开发者编写集成代码或调用外部 API。官方 Skill 开箱即用，自定义 Skill 支持通过 ZIP 包扩展业务专属能力。其核心机制依赖 `SKILL.md` 中的语义描述驱动智能体在对话中自主识别并调用匹配 Skill，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **适用模型**：Skill 与百炼平台所有支持智能体编排的模型兼容（如 Qwen-Max、Qwen-Plus），不依赖特定模型权重，调用逻辑由平台运行时统一调度。
- **核心功能**：
  - 自动触发：基于用户输入语义与 `SKILL.md.description` 的语义匹配，动态决定是否调用；
  - [文件处理](../concepts/file-processing.md)：官方 Skill 覆盖 `.xlsx`, `.csv`, `.pdf`, `.docx`, `.txt` 等主流格式的读取、生成、编辑与转换；
  - 数据操作：支持结构化数据清洗、列计算、表合并、格式标准化等；
  - 输出约束：Skill 必须明确声明输出类型（如“必须返回 .xlsx 文件”），避免歧义调用 —— 此规则在 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 的示例中被严格体现。

> **注意**：文档中未说明 Skill 是否支持流式响应或大文件分块处理。实际使用中，单次 Skill 执行受平台默认超时（60 秒）和内存限制（2 GB）约束，超出需拆分为多步任务，该限制未在 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中明确定义，开发者应以控制台实际报错为准。

## 关键参数

所有 Skill 行为由 `SKILL.md` 中的两个必填字段驱动：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 全局唯一标识符，仅限小写字母、数字、连字符；同一账号下不可重名。 |
| `description` | 是 | **最关键字段**：决定 Skill 是否被触发。必须包含输入类型、支持操作、典型触发词、明确排除场景（如“不适用于生成 HTML 报告”）。描述越精确，误触发率越低。 |

- `description` 长度建议 200–500 字，需覆盖正向触发条件与负向过滤边界，参考官方 xlsx Skill 的完整示例（见原文）。

## 使用方式

1. **添加 Skill**：
   - 方式一：在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击 Skill 卡片 → **添加到智能体**；
   - 方式二：进入目标智能体的**应用配置** → **技能**区域 → 点击 `+` 选择 Skill。

2. **创建自定义 Skill**：
   - 编写符合规范的 `SKILL.md`（YAML 格式，含 `name` 和 `description`）；
   - 将 `SKILL.md` 及其依赖代码/资源打包为 ZIP（≤10 MB）；
   - 在 Skill 管理页点击**自定义 Skill** → 上传 ZIP → 等待约 2 分钟自动审查。

3. **更新自定义 Skill**：
   - 修改 ZIP 内 `SKILL.md`（尤其 `description`）后重新上传同名包，系统自动发布新版本，已接入的应用即时生效。

## 限制和注意事项

- **大小限制**：ZIP 包总大小 ≤ 10 MB，超限将导致审查失败；
- **命名冲突**：同一账号下 `name` 值全局唯一，重复上传会报错而非覆盖；
- **审查机制**：仅校验 `SKILL.md` 存在性、YAML 格式及字段完整性，**不执行代码安全扫描**，自定义 Skill 的逻辑安全性由开发者自行保障；
- **版本管理**：官方 Skill 自动更新，自定义 Skill 需手动上传新 ZIP 触发版本迭代；
- **调试建议**：若 Skill 未被触发，优先检查 `description` 是否遗漏关键触发词或未明确排除干扰场景 —— 这是 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中强调的核心实践。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


