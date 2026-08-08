# skill

Skill 是百炼平台提供的可插拔能力包，用于扩展智能体在对话中自动处理特定任务的能力（如文件解析、数据清洗等），无需开发者编写额外代码或集成外部服务。它分为官方预置 Skill 和用户自定义 ZIP 技能包两类，通过自然语言描述驱动智能体自动识别并调用。详细背景见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **官方 Skill**：由平台统一维护，覆盖常见[文件处理](../concepts/file-processing.md)场景（如 `xlsx`、`pdf`、`csv` 等），开箱即用，无需配置。最新列表请参考控制台 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面。
- **自定义 Skill**：用户通过上传符合规范的 ZIP 包创建，适用于行业定制需求（如专有格式解析、业务规则校验）。ZIP 包必须包含根目录下的 `SKILL.md` 文件，且整体大小 ≤ 10 MB。具体结构要求详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

> **注意**：官方 Skill 不支持用户修改其 `description` 或行为逻辑；所有更新均由平台发布，已添加的智能体会自动生效。而自定义 Skill 的版本更新需重新上传 ZIP 包，旧版本不会被覆盖，仅新部署或重启后生效。

## 关键参数

自定义 Skill 的核心元信息定义在 `SKILL.md`（YAML 格式）中，必填字段如下：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 唯一标识符，仅允许小写字母、数字和连字符（如 `invoice-parser`），不可与当前账号下已有 Skill 重名。 |
| `description` | 是 | 决定智能体是否调用该 Skill 的关键依据。需明确说明：① 支持的输入类型（如 `.xlsx`, `.pdf`）；② 可执行操作（如“读取表格”“生成图表”）；③ 触发关键词（如“帮我整理销售表”）；④ **不适用场景**（如“不处理 Word 文档”），避免误触发。示例详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的 xlsx Skill 描述。 |

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面选择添加。  
   - 自定义 Skill：打包含 `SKILL.md` 的 ZIP 文件，在控制台 **组件 > Skill 管理 > 自定义 Skill > 上传**，系统约 2 分钟完成审查。

2. **添加到智能体**  
   - 方式一：在 Skill 详情页点击 **添加到智能体**，选择目标应用。  
   - 方式二：进入智能体的 **应用配置 > 技能** 区域，点击对应 Skill 右侧 `+` 添加。

3. **测试调用**  
   在应用配置页右侧对话窗格中发送符合 `description` 触发条件的请求（如 `把这份 CSV 按销售额排序并导出为 Excel`），观察是否自动调用并返回预期结果。

## 限制和注意事项

- ZIP 包总大小上限为 **10 MB**，超限将导致上传失败。
- `name` 字段在账号维度全局唯一，重复名称上传会报错，需修改后再试。
- `description` 质量直接影响调用准确率：模糊、缺失“不适用场景”或未明确输入类型，易导致误触发或漏触发。
- 自定义 Skill 审查失败时，需根据错误提示（如 YAML 格式错误、`description` 缺失）修正 `SKILL.md` 后重新上传。
- 官方 Skill 版本由平台统一升级，用户无法回滚；自定义 Skill 版本需手动上传更新，历史版本保留在详情页的 **更新记录** 中供追溯。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


