# application publishing and sharing

百炼平台支持将智能体应用（Agent 1.0）和工作流应用以多种方式发布与共享，包括 UI 应用、钉钉/微信机器人、可复用组件及音视频实时互动渠道。该能力面向开发者提供标准化集成路径，适用于业务嵌入、跨平台分发和模块化复用场景。**注意：Agent 2.0 应用仅支持 API 调用，不支持除 API 外的任何发布渠道** [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 支持的模型/功能

- **适用应用类型**：  
  - ✅ Agent 1.0 智能体应用（支持全部发布渠道）  
  - ✅ 工作流应用（支持 UI 应用、音视频实时互动、组件发布）  
  - ❌ Agent 2.0 智能体应用（**仅支持 API 调用**，不支持魔笔、钉钉、微信、UI 设计器或音视频互动等渠道）[分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)  
- **核心发布能力**：  
  - UI 应用（基于魔笔低代码平台，支持 PC/H5 端）[UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)  
  - 第三方平台机器人（钉钉、微信公众号）  
  - 可复用组件（供其他智能体或工作流引用）  
  - 音视频实时互动（H5/APP 扫码体验 + SDK 集成）  
  - 组件自动更新（应用重新发布后，已发布的组件同步生效）[使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)

> **注意**：文档 1 与文档 2 均明确指出“Agent 2.0 不支持非 API 发布渠道”，但文档 3 的 UI 设计器章节未提及 Agent 版本限制。实际使用中，**UI 设计器仅支持绑定已发布的 Agent 1.0 或工作流应用**；尝试绑定 Agent 2.0 应用将失败，此为隐含限制，需以文档 1 的版本说明为准。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `API KEY` | 用于调用百炼服务的身份凭证，必须与应用、UI 设计器处于同一业务空间 | 必填；跨业务空间不可见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) |
| `query`（系统预设） | 用户输入文本的默认入参，类型 `String`，必填 | 组件配置中不可删除，仅可通过“是否可见”控制透出 |
| `imageList`（系统预设） | 图像公网地址列表，类型 `Array<String>`，非必填 | 仅当组件使用视觉模型时有效；否则建议设为“不可见” [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| 传参方式（`业务透传` / `模型识别`） | 决定参数由调用方显式传入，还是由大模型从上下文推断 | 工作流中**不支持 `模型识别`**，即使配置也为无效；必须通过上游节点显式传入 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |

## 使用方式

1. **入口统一**：所有发布操作均从百炼控制台 **[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)** 页面的目标应用卡片进入 → 点击 **发布**。  
2. **渠道选择**：  
   - **UI 应用**：在“发布渠道”页签点击 **UI 应用** → “创建”，或从 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 页面直接创建并绑定已有应用。开发环境链接 24 小时失效，生产环境需订阅套餐。  
   - **钉钉/微信**：在“发布平台”页签完成授权（SLR + API KEY）→ 配置平台凭证（Client ID/Secret、模板 ID、AppID）→ 获取回调地址或二维码。  
   - **组件**：在“发布渠道”页签点击 **组件** → “创建”，填写名称、描述、参数别名/是否可见/传参方式等 → 发布后可在其他智能体（技能栏）或工作流（组件节点）中引用。  
   - **音视频实时互动**：在“AI 实时互动”页签配置 API KEY → 生成临时体验二维码（24 小时）→ 发布后开通智能媒体服务并完成 SLR 授权。  
3. **组件引用差异**：  
   - 智能体中引用：大模型根据组件描述+上下文自动决策是否调用；`模型识别` 参数可被自动填充。  
   - 工作流中引用：必须手动拖入组件节点，并通过变量（如 `系统变量/query`）显式连接输入；`模型识别` 配置被忽略。

## 限制和注意事项

- **版本兼容性**：Agent 2.0 应用**完全不支持**魔笔、钉钉、微信、UI 设计器、音视频互动等发布渠道，仅开放 API 接口 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。  
- **组件调用风险**：  
  - ❌ 禁止嵌套调用（A → B → A），会导致无限循环；  
  - ⚠️ 多级调用（A → B → C）易触发超时（最长运行时间限制），应尽量扁平化设计 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。  
- **权限与计费**：  
  - UI 应用默认仅限阿里云用户访问；如需匿名访问，须在 UI 设计器中配置权限组 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)；  
  - 所有分享链接产生的模型调用费用均由应用创建者 UID 承担；  
  - 生产环境 UI 发布需订阅付费套餐，开发环境免费但链接 24 小时过期。  
- **业务空间隔离**：API KEY、智能体应用、UI 设计器三者**必须归属同一业务空间**，否则无法关联 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


