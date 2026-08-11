# application publishing and sharing

百炼平台支持将智能体应用（Agent 1.0）和工作流应用以多种方式发布与共享，包括 UI 应用、钉钉/微信机器人、可复用组件及音视频实时互动等形态，便于集成至业务系统或面向终端用户交付。所有发布行为均需在已发布的应用基础上操作，且受 Agent 版本、业务空间归属、API Key 权限等约束。本文档汇总核心能力、参数配置、使用路径及关键限制，供开发者快速落地。

## 支持的模型/功能

- **Agent 版本兼容性**：仅 **Agent 1.0** 智能体应用支持魔笔 UI、钉钉、微信、组件发布及音视频互动；**Agent 2.0 应用不支持任何 UI 或渠道发布功能，仅可通过 API 调用**（见 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)）。
- **支持的应用类型**：
  - 智能体应用（Agent 1.0）
  - 工作流应用（含任务型与对话型）
  - *注意*：UI 设计器本身不生成 AI 模型，但可集成已发布的智能体或工作流应用作为后端服务（见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)）。
- **发布形态**：
  - UI 应用（基于魔笔低代码平台，支持 PC/H5）
  - 钉钉机器人（需配置 Client ID/Secret、模板 ID 及权限 `Card.Streaming.Write` 等）
  - 微信公众号客服（需 AppID 授权及凭证绑定）
  - 可复用组件（供其他智能体或工作流引用）
  - 音视频实时互动（H5/APP 扫码体验或 SDK 集成，仅支持图文类应用）

> **注意**：文档 1 明确指出音视频实时互动“仅支持百炼的图文对话类应用（含智能体应用和工作流应用）”，而文档 3 在“快速开始”示例中未限定应用类型，但未提供非图文类（如纯文件处理）的适配说明。实际使用应以文档 1 的限制为准。

## 关键参数

| 参数类别 | 参数名 | 说明 | 必填性 | 备注 |
|----------|--------|------|--------|------|
| **通用认证** | API Key | 调用百炼服务的身份凭证 | 是 | 必须与应用、UI 设计器处于**同一业务空间**（见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)）；未配置时 UI/钉钉/微信等渠道均无法创建 |
| **钉钉配置** | 钉钉 Client ID / Client Secret / 模板 ID | 用于对接钉钉开放平台 | 是 | 模板 ID 必须关联已申请 `Card.Streaming.Write` 和 `Card.Instance.Write` 权限的应用（见 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)） |
| **微信配置** | 开发者ID（AppID） | 微信公众号唯一标识 | 是 | 需在[微信公众号后台](https://mp.weixin.qq.com/) > 设置与开发 > 基本配置中获取 |
| **组件参数** | `query`（系统预设） | 用户输入文本主参数 | 是（默认） | 别名可自定义（如 `userQuery`），传参方式支持“业务透传”或“模型识别” |
| | `imageList`（系统预设） | 图像公网地址数组 | 否 | 仅当组件使用视觉模型时有效；可通过“是否可见”设为隐藏 |
| | 是否必填 / 是否可见 / 传参方式 | 控制参数暴露与填充逻辑 | 按需 | “模型识别”在工作流中**无效**，必须通过上游节点显式传参（见 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)） |

## 使用方式

1. **前提条件**  
   - 应用已完成构建并**已发布**（非草稿状态）；
   - 所有依赖资源（API Key、智能体、工作流）位于**同一业务空间**；
   - 钉钉/微信首次接入需完成 SLR 授权及 AppFlow 服务授权（见 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)）。

2. **操作入口**  
   - 统一入口：百炼控制台 > **应用管理** > 目标应用卡片 > **发布**；
   - 各渠道入口：
     - UI 应用：发布页签 > **UI 应用** > 创建 → 进入 [UI设计器](https://bailian.console.aliyun.com/?tab=app#/app-ui) 编辑与部署；
     - 钉钉/微信：发布页签 > 对应卡片 > **创建**；
     - 组件：发布页签 > **组件** > **+ 创建**，或通过 [组件管理](https://bailian.console.aliyun.com/?tab=app#/component-manage) 统一维护；
     - 音视频互动：AI 实时互动页签 > **语音互动/视频互动** > **去配置**。

3. **典型流程**  
   - **UI 应用**：创建 → 自动填充基础信息（可选模板）→ 编辑界面 → 发布至**开发环境**（24 小时有效期）或**生产环境**（需订阅套餐）；
   - **组件发布与引用**：配置组件名称/描述/参数 → 发布 → 在新智能体的“技能”中选择，或在工作流画布中拖入“组件节点”并绑定；
   - **钉钉/微信**：完成三方平台应用创建与权限配置 → 回填百炼发布面板所需凭证 → 获取回调地址（钉钉）或二维码（微信）→ 分享给目标用户。

## 限制和注意事项

- **版本限制**：Agent 2.0 应用**完全不支持**除 API 调用外的任何发布渠道（UI、钉钉、微信、组件、音视频），该限制在文档 1 中明确强调，开发者需确认应用版本再操作。
- **环境与计费**：
  - UI 应用开发环境免费但链接**24 小时失效**；生产环境需订阅团队版及以上套餐并绑定自定义域名（见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)）；
  - 所有分享链接产生的模型调用费用均由**应用创建者 UID 账号承担**（见 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)）。
- **组件调用风险**：
  - **禁止嵌套调用**（A→B→A）：导致无限循环，功能不可用；
  - **慎用多级调用**（A→B→C）：受最长运行时间限制，易超时；
  - **工作流中“模型识别”无效**：即使参数设置为该模式，也必须由上游节点显式传值（见 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)）。
- **权限与访问**：
  - UI 应用默认仅限阿里云用户访问；如需匿名访问，需在 UI 设计器中开启“允许匿名访问”并配置权限组；
  - 钉钉/微信机器人回调地址、UI 应用地址等链接无内置访问控制，需通过业务空间隔离或后续权限策略管控。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)


