# application publishing and sharing

百炼平台支持将智能体应用（Agent 1.0）和工作流应用以多种方式发布与共享，包括 UI 应用、钉钉/微信渠道、可复用组件及音视频实时互动等形态，便于集成至业务系统或面向终端用户分发。所有发布行为均需基于已创建并发布的应用，且不同渠道对 Agent 版本、权限模型和参数配置有明确约束。开发者应根据目标场景选择适配的发布路径，并严格遵循各渠道的前置条件与配置规范。

## 支持的模型/功能

- **Agent 版本限制**：魔笔分享渠道、钉钉、微信、UI 应用、组件发布及音视频实时互动等功能**仅支持 Agent 1.0 智能体应用**；Agent 2.0 应用仅支持 API 调用，不支持上述任何 UI 或渠道类发布方式 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **UI 应用**：基于魔笔低代码平台构建，支持拖放式界面开发，可集成智能体、工作流、数据库、HTTP 服务等资源，提供开发/生产双环境部署能力 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件化能力**：智能体或工作流应用可发布为标准化组件，供其他智能体（作为工具）或工作流（作为节点）引用，支持 `query` 和 `imageList` 等预设系统参数，并自动随源应用更新 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **音视频实时互动**：仅支持图文对话类应用（含智能体与工作流），通过 SDK 集成或 H5/APP 扫码方式提供语音/视频交互能力，依赖 AICallKit SDK 和临时 [Token](../concepts/token.md) 验证。

## 关键参数

| 参数 | 说明 | 使用约束 |
|------|------|----------|
| `API KEY` | 调用百炼服务的身份凭证，必须与应用、UI 设计器处于**同一业务空间** | 所有发布渠道（钉钉、微信、UI、音视频）均需显式选择；未配置时需先创建 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) |
| `query`（系统参数） | 默认字符串型入参，用于传递用户原始输入文本 | 组件配置中不可删除，可通过“是否可见”控制暴露；在智能体中启用“模型识别”时由大模型自动填充 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| `imageList`（系统参数） | 默认 `Array<String>` 型入参，用于传递图像公网 URL 列表 | 仅当组件使用视觉模型时生效；非视觉场景建议设为“不可见” |
| `biz_param`（API 调用） | 用于透传业务参数的 JSON 字段，适用于含“业务透传”参数的组件调用 | 仅在 API 调用时生效，UI/钉钉/微信等渠道不支持该字段 |

> **注意**：文档 1 中称“钉钉/微信配置需授权计算巢 AppFlow”，而文档 3 在 UI 设计器准备工作中强调“API Key 与应用必须同业务空间”，但未提 AppFlow 授权；实际操作中若跨空间配置 API KEY 将导致 UI 或渠道发布失败，此时必须补全 AppFlow 授权步骤，否则无法完成回调地址注册或服务集成。

## 使用方式

1. **UI 应用发布**  
   - 进入应用「发布渠道」页签 → 选择「UI 应用」→ 「创建」→ 自动填充基础信息（API KEY、智能体、图标等）→ 编辑 UI 后发布至开发环境（24 小时有效）或生产环境（需订阅套餐）[UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。  
   - 开发环境链接可直接分享，生产环境支持自定义域名绑定。

2. **钉钉/微信发布**  
   - 首次需授权计算巢 AppFlow（SLR + API-KEY 加密传输）；  
   - 钉钉：需在钉钉开放平台创建应用、获取 Client ID/Secret、创建 AI 卡片模板并申请 `Card.Streaming.Write` 权限，再填入百炼发布面板；  
   - 微信：需在微信公众号后台获取 AppID 并完成授权；  
   - 发布后生成回调地址（钉钉）或客服二维码（微信），供下游配置机器人或扫码接入。

3. **组件发布与引用**  
   - 在应用「发布渠道」页签 → 「组件」→ 「创建」→ 配置名称、描述、参数（别名/是否必填/传参方式等）→ 「确定发布」；  
   - 引用时：智能体中作为技能添加，工作流中作为节点拖入；  
   - 注意：工作流中即使参数设为“模型识别”，也**必须显式连接上游节点传值**，不支持自动推断 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

4. **音视频实时互动**  
   - 进入应用「AI 实时互动」页签 → 选择语音/视频 → 配置 API KEY → 生成 24 小时临时体验二维码或链接；  
   - 正式发布需开通智能媒体服务、完成 SLR 授权，并选择 H5/APP 分享或 SDK 集成（含 UI / 无 UI 方案）。

## 限制和注意事项

- **Agent 版本硬性隔离**：Agent 2.0 应用完全不支持 UI、钉钉、微信、组件、音视频等发布渠道，仅开放 RESTful API 接口；迁移前须确认版本兼容性 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **组件调用风险**：  
  - 禁止嵌套调用（A→B→A），会导致无限循环；  
  - 多级调用（A→B→C）易触发最长运行时间限制（默认 60 秒），建议单链深度 ≤2；  
  - 组件发布后自动随源应用更新，无需手动同步。
- **环境与权限约束**：  
  - UI 应用开发环境链接 24 小时失效，生产环境需团队版及以上套餐；  
  - 所有分享链接默认仅限阿里云用户访问，如需匿名访问需在 UI 设计器中单独配置权限组；  
  - 计费主体为应用创建者 UID，所有通过分享链接产生的模型调用、文件存储、数据库等费用均由其承担。
- **参数配置陷阱**：  
  - 工作流中引用组件时，“模型识别”传参方式**无效**，必须使用“业务透传”并显式连线；  
  - UI 应用若含文件上传参数，需在 UI 设计器中手动映射变量（如 `{{{file_name:files[0]}}}`），否则无法传递文件。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


