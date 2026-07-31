# application publishing and sharing

百炼平台支持将已发布的智能体应用（Agent 1.0）或工作流应用以多种方式对外共享与集成，包括 UI 应用、钉钉/微信机器人、可复用组件及音视频实时互动渠道。所有发布行为均需基于已发布的应用，并受 Agent 版本、业务空间归属和权限配置约束。开发者应根据目标场景选择合适渠道，并注意参数传递逻辑与运行时限制。

## 支持的模型/功能

- **仅限 Agent 1.0**：魔笔 UI 应用、钉钉机器人、微信公众号、组件化发布、音视频实时互动等功能**全部仅支持 Agent 1.0 智能体应用**；Agent 2.0 应用不支持上述任何分享渠道，仅可通过 API 调用接入 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **组件来源广泛**：智能体应用与工作流应用均可发布为组件，供其他智能体或工作流引用 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **UI 设计器兼容性**：UI 应用可集成 Agent 1.0 或工作流应用，但要求 UI、API Key 和目标应用必须归属于**同一业务空间** [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **音视频互动限定类型**：仅支持图文对话类应用（含智能体与工作流），不支持纯[工具调用](../concepts/tool-use.md)型或非对话型工作流。

> **注意**：文档 1 明确指出“Agent 2.0 仅支持通过 API 调用”，而文档 2 和文档 3 均未提及 Agent 2.0 的组件或 UI 集成能力，三者一致确认 Agent 2.0 不参与本主题所述任何发布流程。

## 关键参数

| 参数 | 说明 | 约束与注意事项 |
|------|------|----------------|
| `query`（系统预设） | 用户输入文本主参数，类型为 `String`，默认必填 | 无法删除；在智能体中启用“模型识别”时，大模型据此自动填充；工作流中必须显式传入 |
| `imageList`（系统预设） | 图像公网地址列表，类型为 `Array<String>`，默认非必填 | 仅当组件使用视觉模型时生效；如无需图像输入，应设为“是否可见=否” |
| `biz_param`（API 调用） | 用于透传业务参数的顶层字段，格式为 JSON 对象 | 仅在 API 调用时生效，用于传递 `query` 等系统参数之外的业务变量 |
| 回调地址 / [Token](../concepts/token.md) / 分享链接 | 各渠道对外暴露的访问入口 | 钉钉/微信回调地址需在第三方平台配置；UI 开发环境链接有效期为 24 小时；音视频体验二维码有效期同为 24 小时 |

## 使用方式

### 1. UI 应用（魔笔渠道）
- 进入应用「发布渠道」页签 → 选择「UI 应用」→ 「创建」→ 自动填充基础信息（API Key、智能体、图标等）→ 发布至开发/生产环境  
- 开发环境免费、链接 24 小时失效；生产环境需订阅套餐并绑定自定义域名 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)

### 2. 钉钉/微信机器人
- **前提**：完成计算巢 AppFlow 授权（SLR + API Key 加密传输）  
- **钉钉**：获取钉钉 Client ID/Secret、AI 卡片模板 ID，配置权限 `Card.Streaming.Write` 和 `Card.Instance.Write`，再填入百炼发布面板  
- **微信**：需已有微信公众号开发者凭据（AppID），授权后生成客服二维码供扫码体验  
- 两者均需在第三方平台完成机器人配置与版本发布 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)

### 3. 组件化发布
- 在应用「发布渠道」页签 → 「组件」→ 「创建」→ 配置组件名称、描述、参数别名、传参方式（业务透传 / 模型识别）  
- **关键区别**：  
  - 智能体中“模型识别”可自动推断参数；  
  - 工作流中无论传参方式如何，**必须由上游节点显式提供输入值** [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)  
- 发布后可在智能体「技能」或工作流画布中拖入「组件节点」引用

### 4. 音视频实时互动
- 进入应用「AI 实时互动」页签 → 配置 API Key → 生成临时体验二维码（24 小时）→ 正式发布后开通智能媒体服务并授权 SLR  
- 支持 H5/APP 扫码体验与 SDK 集成（含 UI / 无 UI 方案）  
- 注意：消息接收模式必须选 **HTTP 模式**（Stream 模式不兼容） [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)

## 限制和注意事项

- **Agent 版本硬限制**：所有 UI、钉钉、微信、组件、音视频渠道均**不支持 Agent 2.0**，仅限 Agent 1.0 应用使用。
- **嵌套与多级调用风险**：  
  - A 调用 B 且 B 调用 A → 触发无限循环，导致功能不可用；  
  - A→B→C 多级链路 → 易因总运行时间超限（默认 120 秒）而失败 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **工作流中组件参数逻辑特殊**：即使设置“模型识别”，工作流仍强制要求上游节点显式传参，此行为与智能体不同，需特别注意 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **业务空间强一致性**：UI 设计器、API Key、目标应用三者必须位于同一业务空间，否则无法关联或选择 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **计费责任归属**：所有通过分享链接产生的模型调用费用，均由应用创建者 UID 账号承担；UI 生产环境发布需订阅付费套餐。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


