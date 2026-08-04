# application publishing and sharing

百炼平台支持将智能体应用（Agent 1.0）和工作流应用以多种方式发布与共享，包括 UI 应用、钉钉/微信机器人、可复用组件及音视频实时互动渠道。所有发布行为均需基于已创建并发布的应用，且不同渠道对 Agent 版本、模型能力及配置权限有明确约束。开发者应根据目标场景选择适配的发布路径，并严格遵循参数配置规范与调用限制。

## 支持的模型/功能

- **Agent 版本兼容性**：魔笔分享渠道、钉钉、微信、组件、音视频实时互动等全部发布方式**仅支持 Agent 1.0 智能体应用**；Agent 2.0 应用**不支持上述任何 UI 或集成渠道**，仅可通过 API 调用 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **UI 应用**：依托魔笔低代码平台，支持拖放式界面搭建，可集成智能体、工作流、大模型、HTTP 服务及数据库，适用于 PC/H5 多端部署 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件化能力**：智能体或工作流应用均可发布为组件，供其他智能体（作为工具）或工作流（作为节点）引用，实现功能复用 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **音视频实时互动**：仅支持图文类智能体/工作流应用（不含纯语音/视频模型），提供 H5/APP 扫码体验与 SDK 集成两种接入方式。

> **注意**：文档 1 明确指出“音视频实时互动仅支持图文对话类应用”，而文档 3 中 UI 设计器支持“企业AI知识库Lite”等含文件上传的模板，但未说明其是否兼容音视频互动。二者功能边界不同，不可混用——UI 设计器用于构建前端界面，音视频互动用于构建实时音视频会话通道，属正交能力。

## 关键参数

| 参数类别 | 参数名 | 说明 | 约束 |
|----------|--------|------|------|
| **通用认证** | API Key | 所有发布渠道（钉钉、微信、音视频、UI）均需绑定同一业务空间下的有效 API Key | 必填；需提前在[同一业务空间](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)创建 |
| **钉钉配置** | 钉钉 Client ID / Client Secret / 模板 ID | 用于对接钉钉开放平台；模板 ID 必须关联已申请 `Card.Streaming.Write` 和 `Card.Instance.Write` 权限的应用 | 缺失任一将导致发布失败 |
| **微信配置** | 开发者ID（AppID） | 微信公众号后台「基本配置」页获取；需完成微信侧授权流程 | 仅支持公众号类型，暂不支持小程序或企业微信（文档未提及） |
| **组件参数** | `query`（String, 必填）、`imageList`（Array<String>, 可选） | 预设系统参数，不可删除；`query` 传递用户文本输入，`imageList` 传递图像公网地址列表 | `imageList` 仅在组件使用视觉模型时生效；非视觉模型应设为“是否可见=否” |
| **UI 应用** | 数据库表映射名（如 `kb_chat_list`） | 模板自带固定结构表，若复用已有表，必须确保字段类型、名称、主键完全一致 | 结构不一致将导致运行时错误 |

## 使用方式

1. **前置准备**  
   - 确保智能体/工作流应用已**发布成功**（非仅“保存”）；
   - 确认 API Key、应用、UI 设计器三者处于**同一业务空间** [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)；
   - Agent 2.0 应用请直接跳过 UI/钉钉/微信/组件等渠道，仅使用 API 调用。

2. **发布操作路径**  
   - **UI 应用**：进入应用「发布渠道」页签 → 选择「UI 应用」→「创建」→ 自动填充基础信息 → 编辑 UI → 发布至开发/生产环境；
   - **钉钉/微信**：进入「发布平台」页签 → 授权计算巢 AppFlow（首次需 SLR + API-KEY 加密授权）→ 配置对应平台凭证 → 获取回调地址/二维码；
   - **组件**：在「发布渠道」页签 → 「组件」→「创建」→ 填写组件名称、描述、参数（含别名、传参方式、是否可见）→ 确定发布；
   - **音视频互动**：进入「AI实时互动」页签 → 配置 API Key → 生成临时体验二维码（24小时）→ 正式发布后开通智能媒体服务并授权 SLR。

3. **引用组件**  
   - **在智能体中**：创建新智能体 → 「技能」中选择已发布组件 → 大模型根据组件描述与上下文自动触发调用（`模型识别`传参）或由用户/API 提供 `biz_param`（`业务透传`）；
   - **在工作流中**：拖入「组件节点」→ 选择组件 → 手动连接上游节点输出至组件输入（**工作流不支持 `模型识别` 自动填参，必须显式传值**） [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

## 限制和注意事项

- **版本限制**：Agent 2.0 应用**完全不支持**魔笔、钉钉、微信、组件、音视频等所有可视化/集成发布渠道，仅开放 API 接口 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **嵌套与多级调用禁止**：组件 A 调用 B、B 再调用 A 将导致无限循环；A→B→C 的三级调用易超时，建议单层调用或合并逻辑 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **环境时效性**：UI 应用开发环境链接**24 小时后失效**，需重新发布；生产环境需订阅付费套餐并绑定自定义域名 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **权限与计费归属**：所有通过分享链接产生的模型调用费用，均由**应用创建者 UID 账号承担**；匿名访问 UI 需单独配置权限组，不影响后台管理权限。
- **参数传参差异**：`模型识别` 方式在智能体中有效，在工作流中**无效**——工作流必须通过上游节点显式传入参数值，否则报错 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


