# application publishing and sharing

百炼平台支持将已发布的智能体应用（Agent 1.0）或工作流应用以多种方式对外共享与集成，包括生成可访问的 UI 应用、发布为跨平台机器人（钉钉/微信）、封装为可复用组件、以及接入音视频实时互动场景。所有发布行为均需基于已上线的应用，并受 Agent 版本、权限空间和计费模型约束。

## 支持的模型/功能

- **仅限 Agent 1.0**：魔笔分享渠道、钉钉机器人、微信公众号、组件发布、音视频实时互动等功能**全部仅支持 Agent 1.0 智能体应用**；Agent 2.0 应用不支持上述任何发布渠道，仅可通过 API 调用 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **UI 应用支持范围更广**：UI 设计器支持集成**智能体应用（Agent 1.0/2.0）和工作流应用**，但前提是二者与 UI 所属业务空间一致 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件来源多样**：智能体应用和工作流应用均可发布为组件，且组件可在智能体或工作流中被引用 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

> **注意**：文档 1 明确限定“分享渠道均为 Agent 1.0 功能”，而文档 3 在“准备工作”中指出 UI 设计器支持“智能体应用或工作流应用”，未限定 Agent 版本；结合控制台实际能力，UI 集成对 Agent 2.0 的支持是例外情形，但组件发布、钉钉/微信等渠道严格不兼容 Agent 2.0。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `API Key` | 用于身份认证与调用鉴权，必须与应用、UI 同属一个业务空间 | 缺失时需在发布流程中创建或管理；钉钉/微信/音视频配置均依赖此密钥 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |
| `query` / `imageList` | 组件预设系统参数：`query`（String，必填）传递用户文本输入；`imageList`（Array<String>，非必填）传递图像公网地址 | 预设参数不可删除，无需显式定义；若组件不处理图像，应将 `imageList` 设置为“是否可见 = 否” [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| `传参方式`（业务透传 / 模型识别） | 决定参数值由调用方提供（业务透传）还是由大模型从上下文推断（模型识别） | **工作流中模型识别无效**：即使配置为“模型识别”，仍需上游节点明确传入值 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |

## 使用方式

1. **UI 应用发布**  
   进入应用「发布渠道」页签 → 选择「UI 应用」→ 创建后跳转至 UI 设计器 → 编辑并发布至开发/生产环境。开发环境链接有效期 24 小时，生产环境需订阅付费套餐并绑定域名 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

2. **钉钉/微信机器人**  
   - 钉钉：需在钉钉开放平台创建应用，获取 `Client ID`/`Client Secret` 和 AI 卡片 `Template ID`，并在百炼配置回调地址；授权 SLR 及 API-KEY 传输为必要前置步骤 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。  
   - 微信：需在微信公众号后台获取 `AppID`，完成开发者授权；发布后生成客服二维码供扫码体验。

3. **组件发布与引用**  
   - 发布：在应用「发布渠道」→「组件」→ 填写名称、描述、参数别名及传参方式 → 确定发布。  
   - 引用：智能体中作为技能添加；工作流中拖入「组件节点」并绑定输入（如 `系统变量/query`）→ 输出可直接接入下游节点 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

4. **音视频实时互动**  
   仅支持图文类应用（智能体/工作流），需配置 API Key → 生成临时体验二维码（24 小时有效）→ 发布后开通智能媒体服务并授权 SLR → 可选 H5/APP 扫码或 SDK 集成 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 限制和注意事项

- **Agent 版本硬性限制**：除 UI 集成外，所有发布渠道（魔笔、钉钉、微信、组件、音视频）均**不支持 Agent 2.0**；尝试对 Agent 2.0 应用执行相关操作将失败或无响应。
- **嵌套与多级调用风险**：组件间禁止 A→B→A 的循环调用（导致死循环），也应避免 A→B→C 的三级以上链式调用（易超时） [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **环境与权限隔离**：UI 应用、API Key、智能体/工作流必须归属同一业务空间，否则无法关联或发布 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **计费责任归属**：所有通过分享链接产生的模型调用、存储、带宽等费用，均由应用创建者 UID 账号承担，与访问者无关 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **生产环境成本**：UI 应用发布至生产环境需订阅团队版及以上套餐；开发环境免费但链接 24 小时失效 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


