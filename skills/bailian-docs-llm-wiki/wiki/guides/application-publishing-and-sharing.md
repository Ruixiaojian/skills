# application publishing and sharing

百炼平台支持将已发布的智能体应用（Agent 1.0）或工作流应用以多种方式对外发布与共享，包括 UI 应用、钉钉/微信机器人、可复用组件及音视频实时互动渠道。所有发布行为均需基于已发布的应用实例，并受 Agent 版本、业务空间隔离和权限模型约束。发布后的调用流量与资源消耗统一由应用创建者 UID 账号承担。

## 支持的模型/功能

- **仅限 Agent 1.0**：魔笔 UI 应用、钉钉机器人、微信公众号机器人、组件化发布、音视频实时互动等功能**均不支持 Agent 2.0** 应用 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。Agent 2.0 应用仅可通过 API 调用接入。
- **UI 应用**：依托魔笔低代码平台，支持拖拽式界面构建，集成智能体/工作流、数据库、HTTP 服务等资源 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件化能力**：智能体或工作流应用可发布为标准化组件，供其他智能体（作为工具）或工作流（作为节点）引用，支持 `query` 和 `imageList` 等预设系统参数 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **音视频实时互动**：仅支持图文类智能体/工作流应用，提供 H5/APP 扫码体验与 SDK 集成两种交付方式，需开通智能媒体服务并完成 SLR 授权。

> **注意**：文档 1 中称“音视频实时互动仅支持百炼的图文对话类应用（含智能体应用和工作流应用）”，而文档 3 的 UI 设计器说明中未提及音视频能力；二者无直接冲突，但需明确音视频发布入口在智能体/工作流的 **AI实时互动** 页签，而非 UI 设计器内。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `API KEY` | 所有外部渠道（钉钉、微信、音视频、UI）均需绑定同一业务空间下的有效 API KEY。未授权或跨空间将导致配置失败 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。 | 必填；需提前在[我的API-KEY](https://bailian.console.aliyun.com/?tab=app#/api-key)中创建并授权。 |
| `query` / `imageList` | 组件预设系统参数，不可删除。`query` 类型为 `String`，默认必填；`imageList` 类型为 `Array<String>`，默认非必填 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。 | 在组件配置中通过“是否可见”控制透出，通过“传参方式”区分模型识别或业务透传。 |
| 钉钉 `Client ID` / `Client Secret` / `模板 ID` | 钉钉机器人必需凭证，需在钉钉开放平台创建应用后获取，并申请 `Card.Streaming.Write` 和 `Card.Instance.Write` 权限 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。 | 缺一不可；模板 ID 必须关联对应钉钉应用且已发布。 |
| 微信 `AppID` | 微信公众号机器人必需凭证，需从[微信公众号后台](https://mp.weixin.qq.com/) > 设置与开发 > 开发接口管理中获取。 | 仅支持服务号或认证订阅号；需完成微信侧开发者资质审核。 |

## 使用方式

1. **前置条件**：确保目标应用已**发布**（非仅保存），且与 API KEY、UI 设计器、钉钉/微信配置处于**同一业务空间** [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
2. **入口路径**：
   - UI 应用：应用详情页 → **发布渠道** → **UI应用** → 创建；或直接进入 [UI设计器](https://bailian.console.aliyun.com/?tab=app#/app-ui) → “从已有应用发布”。
   - 钉钉/微信：应用详情页 → **发布平台** 页签 → 对应卡片 → **创建** → 完成授权与凭证配置。
   - 组件：应用详情页 → **发布渠道** → **组件** → **+ 创建**；或通过 [组件管理](https://bailian.console.aliyun.com/?tab=app#/component-manage) 统一操作。
   - 音视频：应用详情页 → **AI实时互动** 页签 → 选择语音/视频 → 配置 API KEY → 发布。
3. **引用组件**：
   - 在智能体中：编辑智能体 → **技能** → 添加组件 → 大模型根据组件描述与上下文自动触发（`模型识别`传参）或由用户/API 提供 `biz_param`（`业务透传`）。
   - 在工作流中：拖入 **组件节点** → 选择组件 → 显式连接上游节点输出至组件输入参数（工作流中 `模型识别` 不生效，必须 `业务透传`）。

## 限制和注意事项

- **Agent 版本锁定**：Agent 2.0 应用无法使用除 API 外的任何发布渠道，升级后原有分享链接/机器人将失效 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **嵌套与多级调用禁止**：组件 A 调用 B、B 又调用 A 将导致死循环；A→B→C 等三级以上调用易超时，应避免 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **环境时效性**：UI 应用开发环境链接有效期为 **24 小时**，需重新发布；生产环境需订阅付费套餐并绑定自定义域名 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **权限与计费归属**：所有分享链接、回调地址、二维码生成的调用均计入**应用创建者 UID 账号**费用；RAM 用户仅能操作其被授权的应用，无法变更计费主体。
- **文件参数映射**：若工作流应用含文件类自定义参数，需在 UI 设计器中显式配置变量如 `{{{file_name:files[0]}}`（`file_name` 替换为实际参数名），否则上传文件无法传递至后端 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


