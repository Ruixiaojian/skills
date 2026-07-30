# skill

Skill 是百炼平台提供的可插拔能力包，用于扩展智能体在对话中自动处理特定任务的能力（如文件解析、数据清洗等），无需开发者编写集成代码。官方 Skill 由平台预置并维护，自定义 Skill 则通过符合规范的 ZIP 包上传实现。其核心机制依赖 `SKILL.md` 中的语义描述驱动智能体自动识别与调用，因此描述质量直接影响调用准确率 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **官方 Skill**：覆盖常见文件处理场景（如 `.xlsx`, `.csv`, `.pdf`, `.docx` 等格式的读写、转换、清洗），由平台统一维护，添加后即用，且已接入智能体的自动路由系统 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。  
- **自定义 Skill**：支持 ZIP 包形式上传，适用于行业专属逻辑（如医疗报告结构化解析、金融票据 OCR 后处理）。必须包含 `SKILL.md`，且仅支持同步执行、无状态的单次任务处理，不支持长时运行或流式响应。  
- > **注意**：当前 Skill 不支持调用外部 API 或访问私有网络资源；所有逻辑需封装在 ZIP 包内本地执行。该限制在 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中未明确说明，但实测验证确认。

## 关键参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 唯一标识符，仅允许小写字母、数字、连字符（`-`），长度 ≤ 64 字符；同一账号下不可重名。 |
| `description` | 是 | 决定智能体是否触发该 Skill 的核心字段。需清晰声明输入类型、支持操作、典型触发词及**明确排除场景**（如“不适用于生成 HTML 报告”）[原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。 |
| ZIP 包大小 | — | ≤ 10 MB，超限将被拒绝上传。 |

## 使用方式

1. **创建**：  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面选择启用。  
   - 自定义 Skill：按规范编写 `SKILL.md`，打包为 ZIP，通过控制台「组件 > Skill 管理 > 自定义 Skill」上传。  

2. **添加到智能体**：  
   - 方式一：从 Skill 详情页点击「添加到智能体」，选择目标应用；  
   - 方式二：进入智能体「应用配置」→「技能」区域，点击加号选择 Skill。  

3. **更新**：重新上传同名 ZIP 包即创建新版本；已添加该 Skill 的智能体会自动切换至最新版（官方 Skill 同理）。

## 限制和注意事项

- **调用触发依赖 description 语义匹配**：若 `description` 未覆盖用户实际表达（如遗漏口语化触发词“那个表格”），Skill 可能无法被调用。强烈建议参考 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中 xlsx Skill 的完整示例编写。  
- **无状态执行**：Skill 运行环境每次调用均为干净上下文，无法跨请求共享内存或临时文件。  
- **调试建议**：使用应用配置页右侧对话窗格测试，输入贴近真实用户表达的句子（含文件名、动作动词、输出要求），观察是否触发及返回结果是否符合预期。  
- **审查耗时**：自定义 Skill 上传后需约 2 分钟自动审查，失败时需根据错误提示修改 `SKILL.md` 后重试。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


