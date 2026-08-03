# application publishing and sharing

百炼平台支持将已构建的智能体应用（Agent 1.0）或工作流应用以多种方式对外发布与共享，包括 UI 应用、钉钉/微信机器人、可复用组件及音视频实时互动等渠道。所有发布行为均需基于已发布的应用实例，并受 Agent 版本、业务空间隔离和权限模型约束。开发者应根据目标场景选择合适发布方式，并注意各渠道对模型能力、参数传递和运行时限制的差异化要求。

## 支持的模型/功能

- **仅限 Agent 1.0**：魔笔 UI 应用、钉钉机器人、微信公众号、组件化发布、音视频实时互动等功能**全部仅支持 Agent 1.0 智能体应用**；Agent 2.0 应用不支持上述任何分享渠道，仅可通过 API 调用接入 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **UI 应用支持更广**：UI 设计器不仅支持集成 Agent 1.0，也支持工作流应用（含任务型与对话型），但需确保应用、API Key 与 UI 所属**业务空间完全一致** [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件来源灵活**：智能体应用和工作流应用均可发布为组件，且组件可被其他智能体或工作流引用 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

> **注意**：文档 1 明确指出“Agent 2.0 仅支持通过 API 调用”，而文档 3 在“准备工作”中强调“智能体应用或工作流应用”均可集成至 UI，未限定 Agent 版本。但结合文档 1 的权威性及上下文一致性，**Agent 2.0 不支持 UI 集成**，该能力实际仍受限于 Agent 1.0。UI 设计器文档中“工作流应用”的表述无矛盾，但“智能体应用”应理解为 Agent 1.0。

## 关键参数

| 参数类别 | 参数名 | 说明 | 来源依据 |
|----------|--------|------|----------|
| **通用系统参数** | `query` | 必填 String 类型，用于传递用户原始文本输入（如“查询杭州天气”） | [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| | `imageList` | 非必填 Array<String> 类型，用于传递图像公网 URL 列表，仅在启用视觉模型时生效 | 同上 |
| **组件配置参数** | 别名 | 调用方可见的参数名称，用于避免命名冲突；不可修改原始参数名（如 `query`） | [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 中“发布应用为组件”章节 |
| | 传参方式 | 分 `业务透传`（由调用方显式提供）与 `模型识别`（仅智能体中由大模型自动填充，工作流中无效） | 同上文档及 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| **UI 应用参数** | 百炼 API-KEY、百炼智能体 | 必填，且必须与 UI 所属业务空间一致；不匹配将导致创建失败 | [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) |

## 使用方式

1. **UI 应用发布**  
   - 进入应用管理 → 目标应用 → **发布渠道** → 选择 **UI 应用** → 创建 → 自动跳转至 UI 设计器编辑界面；或直接访问 [UI设计器](https://bailian.console.aliyun.com/?tab=app#/app-ui) → **创建UI** → 选择模板并绑定已发布应用与 API Key。  
   - 发布后，开发环境链接**24 小时失效**，生产环境需订阅付费套餐并绑定自定义域名 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

2. **第三方平台发布（钉钉/微信）**  
   - 均需先完成**计算巢 AppFlow 授权**（SLR + API-KEY 加密传输），再分别配置平台凭证（钉钉：Client ID/Secret + 卡片模板 ID；微信：AppID）。  
   - 钉钉需额外在开放平台申请 `Card.Streaming.Write` 和 `Card.Instance.Write` 权限；微信生成二维码供扫码体验 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

3. **组件化发布与引用**  
   - 发布：在应用发布页勾选“发布应用组件”，或进入 [组件管理](https://bailian.console.aliyun.com/?tab=app#/component-manage) → **创建组件** → 配置名称、描述、参数（含别名、是否可见、传参方式等）。  
   - 引用：  
     - *智能体中*：在技能配置中选择组件，大模型根据描述与上下文自动触发（`模型识别`）或依赖手动/`biz_param` 传参（`业务透传`）；  
     - *工作流中*：拖入“组件节点”，**必须**通过上游节点显式传入参数（即使设为 `模型识别` 也无效） [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

4. **音视频实时互动**  
   - 仅支持图文类应用（智能体/工作流），需配置 API Key → 生成临时二维码（24 小时）→ 正式发布后开通智能媒体服务并授权 SLR → 选择 H5/APP 扫码或 SDK 集成 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 限制和注意事项

- **版本限制**：Agent 2.0 应用**完全不支持**除 API 调用外的任何发布渠道，包括 UI、钉钉、微信、组件、音视频互动 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **嵌套与多级调用禁止**：组件 A 调用 B、B 又调用 A（嵌套）会导致死循环；A→B→C（三级）易因超时失败，应尽量扁平化设计 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 与 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **工作流中组件参数约束**：`传参方式` 设为 `模型识别` 时，工作流**不会自动推断**参数值，必须由上游节点明确传入；此行为与智能体不同，需特别注意 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **业务空间隔离**：UI 设计器、API Key、目标应用三者必须归属同一业务空间，否则无法关联或创建失败 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **计费责任**：所有通过分享链接产生的模型调用、存储、带宽等费用，均由应用创建者 UID 账号承担 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


