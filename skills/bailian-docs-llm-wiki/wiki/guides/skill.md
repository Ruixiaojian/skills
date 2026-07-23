# skill

Skill 是百炼平台提供的可插拔能力包，用于扩展智能体在对话中自动处理特定任务的能力（如文件解析、数据清洗等），无需开发者编写集成代码。官方 Skill 由平台预置并维护，自定义 Skill 则通过符合规范的 ZIP 包上传实现。Skill 的调用完全由智能体根据 `SKILL.md` 中的 `description` 描述自主决策，因此描述质量直接影响匹配准确率 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **官方 Skill**：覆盖常见文件处理场景（如 `xlsx`、`pdf`、`csv` 等），开箱即用，无需配置，版本由平台统一更新 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。  
- **自定义 Skill**：支持用户上传 ZIP 包实现业务定制能力，例如行业专属格式解析、私有 API 封装等。ZIP 包必须包含根目录下的 `SKILL.md` 文件，且整体大小 ≤ 10 MB [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。  
- 当前所有 Skill 均不依赖特定大模型底座，而是作为独立能力模块被智能体调度；调用过程对底层模型透明。

## 关键参数

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 唯一标识符，需全账号唯一，建议使用小写英文+连字符（如 `invoice-parser`） |
| `description` | 是 | 决定 Skill 是否被调用的核心字段。必须明确说明：适用输入类型、支持操作、典型触发关键词、**不适用场景**（避免误触发） |

> **注意**：`description` 不是 UI 展示文案，而是供智能体推理的语义指令。模糊或缺失“不适用场景”将显著增加误调用概率——该要求在 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中被多次强调，但部分早期示例未严格遵循。

## 使用方式

1. **创建**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面添加。  
   - 自定义 Skill：按规范编写 `SKILL.md` → 打包 ZIP → 控制台「组件 > Skill 管理 > 自定义 Skill」上传。审查约 2 分钟，通过后即可使用。

2. **绑定到智能体**  
   - 方式一：从 Skill 详情页点击「添加到智能体」，选择目标应用。  
   - 方式二：进入智能体「应用配置」→「技能」区域 → 点击对应 Skill 右侧 `+` 添加。

3. **测试**  
   在应用配置页右侧对话窗格输入典型用户指令（如 `帮我清洗这个 CSV 中的重复行`），观察是否触发 Skill 并返回预期结果（如下载清洗后的文件）。

## 限制和注意事项

- 自定义 Skill ZIP 包内禁止包含可执行二进制文件（`.exe`, `.so`, `.dll` 等），仅允许文本、脚本（Python）、配置及静态资源。  
- 同名 Skill 重新上传会创建新版本，已绑定该 Skill 的智能体**自动升级至最新版**（官方 Skill 同理）。  
- `description` 中若未明确排除冲突场景（例如“产出 Word 报告时不触发 xlsx Skill”），可能导致 Skill 被错误调用——这是当前最常见的配置失误，详见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的完整示例对比。  
- Skill 无状态设计：每次调用均为独立上下文，不共享内存或临时文件。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


