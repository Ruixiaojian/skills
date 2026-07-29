# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，支持无需编码即可让智能体自动识别并执行文件处理、数据分析等专业任务。它分为官方预置 Skill 和用户自定义 ZIP 技能包两类，通过语义描述驱动调用，适用于对话场景中的自动化任务分发。详细背景见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **官方 Skill**：平台统一维护的通用能力，覆盖 `.xlsx`、`.csv`、`.pdf`、`.docx` 等常见格式的读取、编辑、转换与清洗，开箱即用，无需配置。最新列表请参考控制台 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面。
- **自定义 Skill**：用户通过上传符合规范的 ZIP 包实现定制化能力，例如行业专用数据解析、私有协议文件处理等。ZIP 包必须包含根目录下的 `SKILL.md` 文件，且整体大小 ≤ 10 MB。具体要求详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

> **注意**：官方 Skill 不支持用户修改其 `description` 或行为逻辑；所有更新由平台后台统一推送，已添加的应用将自动生效。而自定义 Skill 的版本更新需重新上传 ZIP 包，旧版本不会被自动删除，但已绑定该 Skill 的智能体会立即切换至最新通过审查的版本。

## 关键参数

自定义 Skill 的核心元信息全部定义在 `SKILL.md`（YAML 格式）中，必需字段如下：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 唯一标识符，仅限小写字母、数字和连字符（如 `invoice-parser`），不可与当前账号下已有 Skill 名重复。 |
| `description` | 是 | 决定智能体是否调用该 Skill 的关键依据。需明确说明：① 支持的输入类型（如 `.xlsx`, JSON 表格）；② 可执行操作（如“清洗缺失值”“生成透视表”）；③ 典型触发关键词（如“整理表格”“导出为 CSV”）；④ 明确排除的不适用场景（如“不处理图片内嵌表格”）。描述质量直接影响调用准确率，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的完整示例。 |

## 使用方式

1. **添加 Skill 到智能体**：
   - 方式一：进入 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill)，点击目标 Skill 卡片 → **添加到智能体** → 选择应用；
   - 方式二：在目标智能体的**应用配置**页 → 左侧**技能**区域 → 点击 Skill 右侧 `+` → 从列表中勾选。

2. **测试效果**：在应用配置页右侧对话窗格中发送典型指令（如 `把附件里的销售数据按季度汇总成表格`），观察智能体是否正确调用 Skill 并返回预期结果（如生成 `.xlsx` 文件）。

3. **更新自定义 Skill**：修改本地 ZIP 包（含更新后的 `SKILL.md`）→ 在**自定义 Skill** 标签页重新上传同名包 → 审查通过后，所有已绑定该 Skill 的智能体自动升级。

## 限制和注意事项

- ZIP 包总大小上限为 **10 MB**，超限将导致上传失败；
- `name` 字段全局唯一（同一账号下），重名上传会拒绝，需先删除旧版或改名；
- `description` 中若未明确排除歧义场景（如“不处理扫描件 PDF”），可能导致误触发 —— 强烈建议按规范包含“不适用场景”说明；
- 官方 Skill 的 `description` 不可编辑，其语义匹配逻辑由平台模型统一优化，用户无法干预；
- 自定义 Skill 审查耗时约 2 分钟，失败时需根据错误提示（如 YAML 格式错误、`description` 缺失）修正后重传。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


