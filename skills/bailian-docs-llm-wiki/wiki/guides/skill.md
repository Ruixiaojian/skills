# skill

Skill 是百炼平台提供的可插拔能力包，用于扩展智能体在对话中自动处理特定任务（如文件解析、数据清洗等）的能力，无需额外编码或工具集成。开发者可通过官方 Skill 快速启用通用功能，或通过自定义 ZIP 包构建业务专属能力。Skill 的调用由智能体基于 `SKILL.md` 中的 `description` 自动决策，其准确性高度依赖描述的完整性与精确性。

## 支持的模型/功能

- **官方 Skill**：平台预置、开箱即用的通用能力，覆盖 `.xlsx`, `.csv`, `.pdf`, `.docx` 等常见格式的读取、编辑、转换与清洗任务，由百炼统一维护和更新。最新列表请参考 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面。  
- **自定义 Skill**：通过上传符合规范的 ZIP 包实现，适用于行业特有格式（如医疗 DICOM 元数据提取）、私有协议解析或定制化数据处理逻辑等场景。详细要求见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 关键参数

所有 Skill 的核心元信息均定义在 ZIP 包根目录下的 `SKILL.md` 文件中，采用 YAML 格式，**必填字段**为：
- `name`：唯一标识符，仅支持小写字母、数字和连字符（如 `invoice-parser`），不可与当前账号下已有 Skill 重名；
- `description`：决定 Skill 是否被调用的关键字段，需明确说明适用输入类型、支持操作、典型触发关键词及**不适用场景**（避免误触发）。该字段质量直接影响调用准确率，编写规范详见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

> **注意**：`description` 中未明确排除的边界场景（如“产出 HTML 报告”）可能导致 Skill 被错误调用；务必按文档示例完整覆盖正反例，否则调试成本显著升高。

## 使用方式

1. **创建**：  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面添加；  
   - 自定义 Skill：打包含 `SKILL.md` 的 ZIP（≤10 MB），在控制台 **组件 > Skill 管理 > 自定义 Skill** 中上传，审查通过后即可使用（审查约需 2 分钟）。  

2. **集成到智能体**：  
   - 方式一：从 Skill 详情页点击 **添加到智能体**；  
   - 方式二：在目标应用的 **应用配置 > 技能** 区域点击加号选择 Skill。  
   添加后，智能体在对话中自动匹配并调用，无需修改应用代码。具体操作流程参见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

3. **测试**：在应用配置页右侧对话窗格发送典型用户指令（如“清洗附件中的 CSV 数据”），观察是否触发 Skill 并返回预期结果（如下载清洗后的文件）。

## 限制和注意事项

- ZIP 包总大小严格限制为 **≤10 MB**，超限将导致上传失败；  
- `name` 字段全局唯一，重复名称会导致上传拒绝，且历史版本无法回滚至旧版 `description`；  
- 官方 Skill 版本自动同步，但自定义 Skill 更新需重新上传 ZIP 包，已添加的应用**立即生效新版本**（无灰度机制）；  
- Skill 不支持运行时依赖安装（如 `pip install`），所有逻辑必须打包进 ZIP；Python 运行环境限定为百炼托管的 Python 3.9 基础镜像；  
- 当前 Skill 仅支持文件类输入（用户上传或系统生成的二进制文件），**不支持纯文本流式输入或 API 调用链路嵌入**。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


