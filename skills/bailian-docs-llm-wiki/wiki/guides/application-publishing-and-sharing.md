# application publishing and sharing

百炼平台支持将智能体应用（Agent 1.0）和工作流应用以多种方式发布与共享，包括 UI 应用、钉钉/微信机器人、可复用组件及音视频实时互动渠道。该能力面向业务集成与跨平台分发场景，适用于快速落地 AI 能力。**注意：Agent 2.0 应用仅支持 API 调用，不支持 UI、钉钉、微信等分享渠道**，详见[分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 支持的模型/功能

- **适用应用类型**：  
  - ✅ Agent 1.0 智能体应用（支持全部发布渠道）  
  - ✅ 工作流应用（支持 UI 应用、音视频实时互动、组件发布）  
  - ❌ Agent 2.0 智能体应用（**仅支持 API 调用**，不支持魔笔、钉钉、微信、组件、音视频等发布方式）  

- **发布渠道与能力**：  
  | 渠道 | 支持应用类型 | 关键能力 |  
  |---|---|---|  
  | UI 应用（魔笔） | Agent 1.0、工作流 | 可视化拖拽构建 H5/PC 界面，支持权限控制、数据库集成、匿名访问配置；开发环境链接有效期为 24 小时 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) |  
  | 钉钉机器人 | Agent 1.0 | 需配置钉钉 Client ID/Secret、卡片模板 ID 及 `Card.Streaming.Write` 权限；回调地址需在钉钉机器人 HTTP 模式中配置 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |  
  | 微信公众号 | Agent 1.0 | 依赖微信 AppID 授权，生成客服二维码供扫码接入；不支持公众号消息模板以外的交互形式 |  
  | 组件（Reusable Component） | Agent 1.0、工作流 | 发布后可在其他智能体或工作流中作为节点调用；预设系统参数 `query`（String，必填）和 `imageList`（Array<String>，非必填） [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |  
  | 音视频实时互动 | Agent 1.0、工作流（图文类） | 支持 H5/APP 扫码体验（24 小时临时链接）及 SDK 集成（AICallKit），需开通智能媒体服务并完成 SLR 授权 |  

> **注意**：文档 1 中称“音视频实时互动仅支持图文对话类应用”，而文档 3 的 UI 设计器说明中未限定应用类型，但实际发布入口仅对智能体/工作流开放，且不支持纯语音/视频模型直连。此处以文档 1 的明确限制为准。

## 关键参数

| 参数 | 位置 | 说明 |  
|---|---|---|  
| `API Key` | 所有渠道（UI、钉钉、微信、音视频） | 必须与目标应用、UI 设计器处于**同一业务空间**；未授权时需先创建并绑定 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) |  
| `query` / `imageList` | 组件发布页 | 预设系统参数，不可删除；`query` 默认必填，用于传递用户文本输入；`imageList` 仅在启用[多模态](../concepts/multi-modal.md)模型时生效 |  
| `传参方式`（业务透传 / 模型识别） | 组件参数配置 | 在智能体中引用时，“模型识别”由大模型自动填充；在工作流中引用时，**无论设置为何种方式，均需上游节点显式传入值**，否则报错 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |  
| `回调地址` | 钉钉/微信发布页 | 用于钉钉机器人 HTTP 模式接收消息；微信侧不暴露该地址，仅生成二维码 |  
| `Token 有效时间` | 音视频 H5 分享页 | 控制扫码链接有效期（单位：小时），默认 24 小时，最长支持 72 小时 |  

## 使用方式

1. **统一入口**：进入百炼控制台 → [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → 打开目标应用 → 切换至 **发布渠道** 页签（或 **AI 实时互动** 页签）。  
2. **按渠道操作**：  
   - **UI 应用**：点击「UI 应用」→「创建」→ 自动填充或手动配置 API Key、智能体、图标等 → 「立即创建」→ 进入 UI 设计器编辑 → 右上角「发布」至开发/生产环境。  
   - **钉钉/微信**：点击对应卡片「创建」→ 完成 API Key 选择 → 填写平台凭证（Client ID/Secret/AppID/模板 ID）→ 获取回调地址或二维码。  
   - **组件**：点击「组件」→「+ 创建」→ 设置组件名称、描述、参数别名/可见性/传参方式/默认值 → 「确定发布」→ 在其他应用的技能区（智能体）或节点区（工作流）中引用。  
   - **音视频**：进入「AI 实时互动」页签 → 「去配置」→ 选 API Key → 生成临时二维码或配置 H5/SDK → 「发布」后开通智能媒体服务。  
3. **验证**：  
   - UI：复制「应用地址」在浏览器打开；  
   - 钉钉：在群聊中 @ 机器人提问；  
   - 微信：扫码体验客服；  
   - 组件：在测试对话框输入触发语句，观察是否被调用；  
   - 音视频：扫码或集成 SDK 后发起语音/视频会话。

## 限制和注意事项

- **Agent 版本限制**：Agent 2.0 应用**完全不支持**除 API 外的任何发布渠道，此为硬性限制，与文档 1 一致。  
- **组件调用风险**：  
  - ❌ 禁止嵌套调用（A→B→A），会导致无限循环；  
  - ⚠️ 多级调用（A→B→C）易超时，建议单链深度 ≤2；  
  - ⚠️ 组件更新后自动同步，但工作流中引用的组件若含“模型识别”参数，仍需人工补全上游输入 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。  
- **环境与计费**：  
  - UI 开发环境链接 24 小时失效，生产环境需订阅付费套餐并绑定自定义域名；  
  - 所有分享链接产生的模型调用费用，均由应用创建者 UID 账号承担；  
  - 钉钉/微信首次授权需同意计算巢 AppFlow 的 SLR 及 API-KEY 加密传输条款。  
- **权限一致性**：UI 设计器、API Key、目标应用**必须归属同一业务空间**，否则无法关联资源（如百炼智能体、数据库表）。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


