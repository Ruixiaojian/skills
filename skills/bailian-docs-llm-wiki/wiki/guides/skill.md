# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，支持无需编码即可为智能体赋予文件处理、数据分析等专业功能。通过自然语言描述触发条件与能力边界，智能体可在对话中自动识别任务并调用匹配的 Skill 执行。Skill 分为平台预置的官方 Skill 和用户自主构建的自定义 Skill 两类，均通过 `SKILL.md` 元信息驱动语义理解与调度逻辑。

## 支持的模型/功能

- **官方 Skill**：由百炼统一维护，覆盖常见文件处理场景（如 `.xlsx`、`.csv`、PDF 解析、图像 OCR 等），添加后即刻可用，版本更新自动同步至已绑定的智能体应用。最新列表请参考 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面。
- **自定义 Skill**：用户通过上传符合规范的 ZIP 包创建，适用于行业定制场景（如特定格式发票解析、内部数据清洗流水线）。其行为完全由 ZIP 包根目录下的 `SKILL.md` 定义，不依赖特定模型或推理框架——调用执行由平台底层运行时保障，与所选大模型无关。详情见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 关键参数

所有 Skill 的核心行为由 `SKILL.md` 中的两个必填字段控制：

- `name`：全局唯一标识符，仅允许小写字母、数字和连字符（如 `invoice-parser-v2`），同一账号下不可重复；
- `description`：**最关键参数**，直接影响智能体是否准确触发该 Skill。必须清晰说明：  
  - 输入类型（如 “`.pdf` 文件” 或 “JSON 格式日志”）；  
  - 支持操作（如 “提取表格”、“转换为 Markdown”）；  
  - 典型触发关键词（如 “转成 Excel”、“识别发票金额”）；  
  - 明确排除场景（如 “不处理扫描件模糊的 PDF”、“不生成代码”）。  
  描述质量不足将导致误调用或漏调用，强烈建议参照 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中 xlsx Skill 的完整示例编写。

## 使用方式

1. **创建 Skill**：
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击“添加到智能体”；
   - 自定义 Skill：打包含合规 `SKILL.md` 的 ZIP（≤10 MB），在“组件 > Skill 管理 > 自定义 Skill”中上传，系统约 2 分钟完成审查。
2. **绑定智能体**：支持两种路径——  
   - 从 Skill 详情页点击“添加到智能体”，选择目标应用；  
   - 在智能体的“应用配置 > 技能”区域，点击加号从列表选取。  
3. **验证效果**：在应用配置页右侧对话窗格中输入典型用户指令（如 `把附件里的销售数据按季度汇总成图表`），观察是否自动调用对应 Skill 并返回预期结果。测试逻辑详见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 限制和注意事项

- ZIP 包大小上限为 10 MB，超限将导致上传失败；
- `name` 字段在账号维度全局唯一，重名上传会拒绝，而非覆盖；
- 自定义 Skill 更新需重新上传 ZIP 包（同名即覆盖旧版本），已绑定智能体**自动生效新版本**，无需手动刷新；
- > **注意**：文档中提及“官方 Skill 由平台统一维护”，但未明确说明其是否支持回滚至历史版本。实际使用中，若新版官方 Skill 引发兼容性问题，当前控制台暂不提供版本回退入口，建议关键业务场景优先使用自定义 Skill 并自行管控版本；
- `description` 中若未明确排除不适用场景（例如未声明“不处理加密 PDF”），可能导致 Skill 在无效输入下被错误调用并失败，此类问题需通过迭代优化 `description` 修复。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


