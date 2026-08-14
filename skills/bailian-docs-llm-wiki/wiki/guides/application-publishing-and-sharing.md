# application publishing and sharing

百炼平台支持将智能体（Agent 1.0）或工作流应用以多种方式发布与共享，包括生成可访问的 UI 应用、集成至钉钉/微信等第三方平台、封装为可复用组件、以及接入音视频实时互动场景。所有发布行为均需基于已创建并发布的应用，且不同渠道对应用类型、参数配置和权限模型有明确约束。开发者应根据目标使用场景选择适配的发布方式，并注意版本兼容性与运行时限制。

## 支持的模型/功能

- **仅限 Agent 1.0**：魔笔 UI 应用、钉钉机器人、微信公众号、组件化发布、音视频实时互动等功能**全部仅支持 Agent 1.0 智能体应用**；Agent 2.0 应用不支持上述任何分享渠道，仅可通过 API 调用 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **工作流应用支持范围**：工作流应用可发布为组件（见 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)），也可用于 UI 设计器集成及音视频实时互动（图文类应用），但**不支持钉钉/微信机器人发布**。
- **UI 应用能力**：UI 设计器支持集成智能体或工作流应用，并提供低代码页面搭建、数据库映射、权限配置及多环境部署能力，详见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

> **注意**：文档 1 明确指出“Agent 2.0 仅支持通过 API 调用”，而文档 3 在“准备工作”中要求“百炼应用、API Key 和 UI 设计需归属于同一业务空间”，但未限定应用版本；实际实践中，UI 设计器**无法选择 Agent 2.0 应用**作为后端服务，该限制隐含在控制台交互逻辑中，应以文档 1 的版本声明为准。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `query`（系统预设） | 用户输入文本主参数，类型为 `String`，默认必填 | 不可删除；若无需暴露，须设为“是否可见=否” |
| `imageList`（系统预设） | 图像公网地址列表，类型为 `Array<String>`，默认非必填 | 仅当组件使用视觉模型时生效；否则建议隐藏 |
| `biz_param`（API 调用） | 用于透传业务参数的字段，格式为 JSON 对象 | 仅在调用含“业务透传”参数的组件时必需，如测试时需手动填入入参变量配置 |
| 回调地址 / [Token](../concepts/token.md) 有效时间 / 分享 ID | 钉钉/微信/音视频渠道的核心交付物 | 回调地址需配置到第三方平台；[Token](../concepts/token.md) 有效期影响 H5/APP 体验链接时效；分享 ID 用于 SDK 快速集成 |

## 使用方式

1. **UI 应用发布**  
   进入应用「发布渠道」页签 → 选择「UI 应用」→ 「创建」→ 自动填充基础信息（API Key、智能体、图标等）→ 发布至开发/生产环境 → 获取应用地址分享。开发环境链接**24 小时失效**，生产环境需订阅付费套餐 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

2. **钉钉/微信发布**  
   - 均需先完成计算巢 AppFlow 授权（SLR + API-KEY 加密传输）；  
   - 钉钉需在开放平台创建应用、获取 Client ID/Secret、创建 AI 卡片模板并申请 `Card.Streaming.Write` 权限；  
   - 微信需在公众号后台获取 AppID 并完成授权；  
   - 配置完成后，复制回调地址（钉钉）或生成客服二维码（微信）交付终端用户。

3. **组件化发布**  
   - 在应用编辑页点击「发布应用」→ 勾选「发布应用组件」，或进入「组件管理」→ 「创建组件」；  
   - 必填「组件名称」「组件描述」，配置 `query`/`imageList` 等参数的别名、是否可见、传参方式（`业务透传` 或 `模型识别`）；  
   - 在智能体中作为技能引用，在工作流中作为节点拖入并绑定上游输出 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

4. **音视频实时互动**  
   仅支持图文类应用（智能体/工作流）；需配置 API Key → 生成临时体验二维码（24 小时）→ 发布后开通智能媒体服务并授权 SLR → 选择 H5/APP 扫码或 SDK 集成（含快速集成与开发集成两种模式）。

## 限制和注意事项

- **版本锁定**：所有非 API 类发布渠道（UI、钉钉、微信、组件、音视频）**严格限定为 Agent 1.0**，Agent 2.0 应用不可选 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **嵌套与多级调用禁止**：组件 A 调用 B、B 又调用 A 将导致死循环；A→B→C 多级链路易触发超时，应尽量扁平化设计 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **传参方式差异**：`模型识别` 在智能体中由大模型自动填充参数，但在工作流中**无效**——必须通过上游节点显式传入值，否则运行失败。
- **环境与权限隔离**：UI 设计器、API Key、智能体应用必须位于**同一业务空间**，否则无法关联 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **计费责任归属**：所有通过分享链接产生的模型调用、存储、带宽等费用，均由应用创建者 UID 账号承担，与访问者身份无关。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


