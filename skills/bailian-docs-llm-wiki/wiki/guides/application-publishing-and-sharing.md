# application publishing and sharing

百炼平台支持将已发布的智能体应用（Agent 1.0）或工作流应用以多种方式对外发布与共享，包括 UI 应用、钉钉/微信机器人、可复用组件及音视频实时互动等形态。所有发布行为均需基于已上线的应用实例，并受 Agent 版本、业务空间隔离和权限模型约束。发布后的调用流量统一由应用创建者 UID 承担计费责任。

## 支持的模型/功能

- **仅限 Agent 1.0**：魔笔 UI 应用、钉钉机器人、微信公众号机器人、组件化发布、音视频实时互动等功能**均不支持 Agent 2.0 应用**，后者仅可通过 API 调用接入 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **UI 应用**：依托魔笔低代码能力，支持拖拽式界面构建，集成智能体/工作流、数据库、HTTP 服务等资源，可发布至开发环境（24 小时有效期）或生产环境（需订阅套餐）[原文标题](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件化能力**：智能体或工作流应用均可发布为组件，供其他智能体（作为工具）或工作流（作为节点）引用，支持 `query` 和 `imageList` 等预设系统参数 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **音视频实时互动**：仅支持图文类智能体/工作流应用，提供 H5/APP 扫码体验与 SDK 集成两种交付方式，需完成 SLR 授权与智能媒体服务开通。

> **注意**：文档 1 中“通过 UI 应用分享应用”章节描述的“开发环境显示已发布、生产环境显示未发布”与文档 3 中“开发环境 24 小时后失效、生产环境长期有效”的表述存在逻辑冲突——实际应以文档 3 的环境定义为准：开发环境发布即生效但时效有限；生产环境需显式发布且长期有效。文档 1 的状态描述易引发误解，建议以 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 为准。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `API Key` | 所有发布渠道（钉钉、微信、音视频、UI）均需绑定同一业务空间下的有效 API Key | 不同业务空间的 API Key 不可跨空间使用；未授权时需先完成计算巢 AppFlow SLR 关联 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |
| `query` / `imageList` | 组件预设系统参数，不可删除；`query` 类型为 `String` 且必填，`imageList` 类型为 `Array<String>` 且非必填 | 若组件不处理图像，须将 `imageList` 的“是否可见”设为否 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| 传参方式（`业务透传` / `模型识别`） | 决定参数值由调用方显式传入，还是由大模型从上下文推断 | 在工作流中引用组件时，即使设为 `模型识别`，也**必须**由上游节点显式传参，否则运行失败 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |

## 使用方式

1. **前置条件**：确保目标应用已发布，且与所需 API Key、UI 设计器、钉钉/微信凭证处于**同一业务空间** [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
2. **入口路径**：
   - UI 应用：应用管理 → 发布渠道 → UI 应用 → 创建 → 进入 UI 设计器编辑并发布；
   - 钉钉/微信：应用管理 → 发布平台 → 对应渠道 → 授权 → 配置凭证（Client ID/Secret、模板 ID、AppID）→ 获取回调地址或二维码；
   - 组件：应用管理 → 发布渠道 → 组件 → 创建 → 填写名称、描述、参数映射 → 确定发布；
   - 音视频：应用管理 → AI 实时互动 → 配置 → 生成体验链接或 SDK 集成。
3. **引用组件**：
   - 智能体中：在“技能”中选择已发布组件，大模型根据组件描述与上下文自动触发；
   - 工作流中：拖入“组件节点”，手动连接上游输入（如 `系统变量/query`），不可依赖模型识别填充。

## 限制和注意事项

- **版本限制**：Agent 2.0 应用完全不支持除 API 外的任何发布渠道，该限制贯穿所有发布流程 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **嵌套与多级调用**：禁止 A→B→A 的循环调用；A→B→C 的三级及以上调用易触发超时，建议控制在两层以内 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **环境与权限**：UI 应用默认仅限阿里云用户访问；如需匿名访问，须在 UI 设计器中显式开启“允许匿名访问”并配置权限组 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **计费归属**：所有通过分享链接、回调地址、SDK 或二维码触发的调用，产生的模型 Token、存储、带宽等费用均由应用创建者 UID 账户承担，与访问者身份无关。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


