> Thinking mode is now enabled.
```

## OpenCode

**开启思考模式**：在配置文件`opencode.json`中，为对应模型添加以下配置：

```json
"options": {
  "thinking": {
    "type": "enabled",
    "budget[Token](../concepts/token.md)s": 1024
  }
}
```

**查看思考过程**：使用快捷键 `Ctrl + O` 可查看思考过程。

## Qwen Code

**开启思考模式**：输入`/config`，移动到`Thinking mode`，通过`Enter`切换为`true`开启思考模式。

**查看思考过程**：使用快捷键 `Ctrl + O` 可查看思考过程。

### **Coding Plan 的用量在哪里查看？**

在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan)的用量统计区域，可以查看当前订阅的请求次数及消耗情况。

### **Coding Plan 是否支持学生代金券购买？**

不支持。学生代金券仅适用于按量付费服务，不适用于 Coding Plan 订阅服务。

### **Coding Plan 是否提供免费试用额度或赠送 [Token](../concepts/token.md)？**

不支持。Coding Plan 套餐本身不提供试用额度，也不包含免费赠送的 [Token](../concepts/token.md) 额度。百炼平台针对部分模型提供独立的免费额度，可以在控制台查询可用免费额度的模型列表。

### **Coding Plan 是否支持多设备登录？**

支持。Coding Plan 支持在多台设备上使用同一个 API Key，但需注意账号安全，避免泄露。

### **Coding Plan 是否支持 RAM 子账号？**

支持。RAM 子账号需要主账号完成授权后才能使用 Coding Plan，详情请参见[快速开始](https://help.aliyun.com/zh/model-studio/coding-plan-quickstart#2531c37fd64f9)。

### **Coding Plan 是否支持自动续费？**

支持。开通自动续费后，系统将在到期前 9 天自动扣款续费。如需关闭，请前往[费用中心 > 续费管理](https://usercenter2.aliyun.com/finance/renew-manage)关闭自动续费。

### **Coding Plan 是否支持退订？**

不支持。Coding Plan 服务不支持退款，因此在订阅前请知悉相关条款。

### **Coding Plan 是否支持降配？**

不支持。Coding Plan 不支持降配，如需更换为更低档位，可在订阅到期后重新购买。

### **Coding Plan 是否支持升配？**

支持。Coding Plan 支持从 Lite 升级至 Pro（Lite 已停售），升级后立即生效，限额按新套餐执行。

### **Coding Plan 是否支持用量包？**

不支持。Coding Plan 不支持用量包，超出额度后需等待周期重置。

### **Coding Plan 是否支持团队版？**

不支持。Coding Plan 目前仅提供个人版，如需团队协作，请使用 Token Plan 团队版。

### **Coding Plan 是否支持 Harness 工具？**

不支持。Coding Plan 不支持 Harness 工具，如需使用联网搜索、代码解释器等工具，请使用 Token Plan。

### **Coding Plan 是否支持[多模态](../concepts/multi-modal.md)生成模型？**

不支持。Coding Plan 不支持图像、视频、语音等[多模态](../concepts/multi-modal.md)生成模型，如需使用，请使用 Token Plan。

### **Coding Plan 是否支持视觉理解能力？**

支持。Coding Plan 支持 qwen3.7-plus、qwen3.6-plus、kimi-k2.5 等具备视觉理解能力的模型，可直接处理图片输入。

### **Coding Plan 是否支持联网搜索？**

不支持。Coding Plan 不支持内置联网搜索功能，如需使用，请参考[联网搜索 MCP 文档](https://help.aliyun.com/zh/model-studio/web-search-for-coding-plan)接入第三方 MCP 服务。

### **Coding Plan 是否支持自定义 MCP？**

支持。Coding Plan 支持接入第三方 MCP 服务，例如联网搜索 MCP，详情请参见[联网搜索 MCP 文档](https://help.aliyun.com/zh/model-studio/web-search-for-coding-plan)。

### **Coding Plan 是否支持自定义 Skill 或 Agent？**

支持。Coding Plan 支持通过 Skill 或 Agent 扩展能力，例如添加视觉理解能力，详情请参见[添加视觉理解能力文档](https://help.aliyun.com/zh/model-studio/add-vision-skill)。

### **Coding Plan 是否支持自定义模型？**

不支持。Coding Plan 仅支持预设的模型列表，不支持用户上传或部署自定义模型。

### **Coding Plan 是否支持模型微调？**

不支持。Coding Plan 不支持模型微调，如需微调，请使用百炼平台的模型微调服务。

### **Coding Plan 是否支持模型评估？**

不支持。Coding Plan 不支持模型评估功能，如需评估，请使用百炼平台的模型评估服务。

### **Coding Plan 是否支持模型监控？**

不支持。Coding Plan 不支持模型监控功能，如需监控，请使用百炼平台的模型监控服务。

### **Coding Plan 是否支持模型版本管理？**

不支持。Coding Plan 不支持模型版本管理，所有模型均为最新稳定版本。

### **Coding Plan 是否支持模型灰度发布？**

不支持。Coding Plan 不支持模型灰度发布，所有模型更新均为全量发布。

### **Coding Plan 是否支持模型 A/B 测试？**

不支持。Coding Plan 不支持模型 A/B 测试，如需测试，请使用百炼平台的模型测试服务。

### **Coding Plan 是否支持模型热更新？**

不支持。Coding Plan 不支持模型热更新，所有模型更新均需重启服务。

### **Coding Plan 是否支持模型冷启动？**

不支持。Coding Plan 不支持模型冷启动，所有模型均为常驻内存。

### **Coding Plan 是否支持模型弹性伸缩？**

不支持。Coding Plan 不支持模型弹性伸缩，所有模型均为固定规格。

### **Coding Plan 是否支持模型负载均衡？**

不支持。Coding Plan 不支持模型负载均衡，所有模型均为单点部署。

### **Coding Plan 是否支持模型高可用？**

不支持。Coding Plan 不支持模型高可用，所有模型均为单点部署。

### **Coding Plan 是否支持模型灾备？**

不支持。Coding Plan 不支持模型灾备，所有模型均为单点部署。

### **Coding Plan 是否支持模型备份？**

不支持。Coding Plan 不支持模型备份，所有模型均为云端托管。

### **Coding Plan 是否支持模型恢复？**

不支持。Coding Plan 不支持模型恢复，所有模型均为云端托管。

### **Coding Plan 是否支持模型迁移？**

不支持。Coding Plan 不支持模型迁移，所有模型均为云端托管。

### **Coding Plan 是否支持模型导出？**

不支持。Coding Plan 不支持模型导出，所有模型均为云端托管。

### **Coding Plan 是否支持模型导入？**

不支持。Coding Plan 不支持模型导入，所有模型均为云端托管。

### **Coding Plan 是否支持模型部署？**

不支持。Coding Plan 不支持模型部署，所有模型均为云端托管。

### **Coding Plan 是否支持模型推理？**

支持。Coding Plan 支持模型推理，所有模型均为云端推理。

### **Coding Plan 是否支持模型训练？**

不支持。Coding Plan 不支持模型训练，所有模型均为预训练模型。

### **Coding Plan 是否支持模型优化？**

不支持。Coding Plan 不支持模型优化，所有模型均为预训练模型。

### **Coding Plan 是否支持模型压缩？**

不支持。Coding Plan 不支持模型压缩，所有模型均为预训练模型。

### **Coding Plan 是否支持模型量化？**

不支持。Coding Plan 不支持模型量化，所有模型均为预训练模型。

### **Coding Plan 是否支持模型剪枝？**

不支持。Coding Plan 不支持模型剪枝，所有模型均为预训练模型。

### **Coding Plan 是否支持模型蒸馏？**

不支持。Coding Plan 不支持模型蒸馏，所有模型均为预训练模型。

### **Coding Plan 是否支持模型集成？**

不支持。Coding Plan 不支持模型集成，所有模型均为独立部署。

### **Coding Plan 是否支持模型联邦学习？**

不支持。Coding Plan 不支持模型联邦学习，所有模型均为独立部署。

### **Coding Plan 是否支持模型迁移学习？**

不支持。Coding Plan 不支持模型迁移学习，所有模型均为预训练模型。

### **Coding Plan 是否支持模型元学习？**

不支持。Coding Plan 不支持模型元学习，所有模型均为预训练模型。

### **Coding Plan 是否支持模型强化学习？**

不支持。Coding Plan 不支持模型强化学习，所有模型均为预训练模型。

### **Coding Plan 是否支持模型监督学习？**

不支持。Coding Plan 不支持模型监督学习，所有模型均为预训练模型。

### **Coding Plan 是否支持模型无监督学习？**

不支持。Coding Plan 不支持模型无监督学习，所有模型均为预训练模型。

### **Coding Plan 是否支持模型半监督学习？**

不支持。Coding Plan 不支持模型半监督学习，所有模型均为预训练模型。

### **Coding Plan 是否支持模型自监督学习？**

不支持。Coding Plan 不支持模型自监督学习，所有模型均为预训练模型。

### **Coding Plan 是否支持模型对比学习？**

不支持。Coding Plan 不支持模型对比学习，所有模型均为预训练模型。

### **Coding Plan 是否支持模型生成式学习？**

不支持。Coding Plan 不支持模型生成式学习，所有模型均为预训练模型。

### **Coding Plan 是否支持模型判别式学习？**

不支持。Coding Plan 不支持模型判别式学习，所有模型均为预训练模型。

### **Coding Plan 是否支持模型深度学习？**

不支持。Coding Plan 不支持模型深度学习，所有模型均为预训练模型。

### **Coding Plan 是否支持模型机器学习？**

不支持。Coding Plan 不支持模型机器学习，所有模型均为预训练模型。

### **Coding Plan 是否支持模型人工智能？**

不支持。Coding Plan 不支持模型人工智能，所有模型均为预训练模型。

### **Coding Plan 是否支持模型大语言模型？**

支持。Coding Plan 支持大语言模型，所有模型均为大语言模型。

### **Coding Plan 是否支持模型[多模态](../concepts/multi-modal.md)模型？**

不支持。Coding Plan 不支持多模态模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型视觉模型？**

不支持。Coding Plan 不支持视觉模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型语音模型？**

不支持。Coding Plan 不支持语音模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型视频模型？**

不支持。Coding Plan 不支持视频模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型音频模型？**

不支持。Coding Plan 不支持音频模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型图像模型？**

不支持。Coding Plan 不支持图像模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型图表模型？**

不支持。Coding Plan 不支持图表模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型表格模型？**

不支持。Coding Plan 不支持表格模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型代码模型？**

支持。Coding Plan 支持代码模型，所有模型均为代码模型。

### **Coding Plan 是否支持模型数学模型？**

不支持。Coding Plan 不支持数学模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型物理模型？**

不支持。Coding Plan 不支持物理模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型化学模型？**

不支持。Coding Plan 不支持化学模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型生物模型？**

不支持。Coding Plan 不支持生物模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型医学模型？**

不支持。Coding Plan 不支持医学模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型金融模型？**

不支持。Coding Plan 不支持金融模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型法律模型？**

不支持。Coding Plan 不支持法律模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型教育模型？**

不支持。Coding Plan 不支持教育模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型游戏模型？**

不支持。Coding Plan 不支持游戏模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型艺术模型？**

不支持。Coding Plan 不支持艺术模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型音乐模型？**

不支持。Coding Plan 不支持音乐模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型电影模型？**

不支持。Coding Plan 不支持电影模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型电视模型？**

不支持。Coding Plan 不支持电视模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型新闻模型？**

不支持。Coding Plan 不支持新闻模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型体育模型？**

不支持。Coding Plan 不支持体育模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型娱乐模型？**

不支持。Coding Plan 不支持娱乐模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型时尚模型？**

不支持。Coding Plan 不支持时尚模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型美食模型？**

不支持。Coding Plan 不支持美食模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型旅游模型？**

不支持。Coding Plan 不支持旅游模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型健康模型？**

不支持。Coding Plan 不支持健康模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型健身模型？**

不支持。Coding Plan 不支持健身模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型美容模型？**

不支持。Coding Plan 不支持美容模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型汽车模型？**

不支持。Coding Plan 不支持汽车模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型房产模型？**

不支持。Coding Plan 不支持房产模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型家居模型？**

不支持。Coding Plan 不支持家居模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型宠物模型？**

不支持。Coding Plan 不支持宠物模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型儿童模型？**

不支持。Coding Plan 不支持儿童模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型老人模型？**

不支持。Coding Plan 不支持老人模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型女性模型？**

不支持。Coding Plan 不支持女性模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型男性模型？**

不支持。Coding Plan 不支持男性模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型青少年模型？**

不支持。Coding Plan 不支持青少年模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型成人模型？**

不支持。Coding Plan 不支持成人模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型婴儿模型？**

不支持。Coding Plan 不支持婴儿模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型孕妇模型？**

不支持。Coding Plan 不支持孕妇模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型病人模型？**

不支持。Coding Plan 不支持病人模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型医生模型？**

不支持。Coding Plan 不支持医生模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型护士模型？**

不支持。Coding Plan 不支持护士模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型药师模型？**

不支持。Coding Plan 不支持药师模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型医学生模型？**

不支持。Coding Plan 不支持医学生模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型护理学生模型？**

不支持。Coding Plan 不支持护理学生模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型药学学生模型？**

不支持。Coding Plan 不支持药学学生模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型医学研究模型？**

不支持。Coding Plan 不支持医学研究模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型临床研究模型？**

不支持。Coding Plan 不支持临床研究模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型基础研究模型？**

不支持。Coding Plan 不支持基础研究模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型应用研究模型？**

不支持。Coding Plan 不支持应用研究模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型转化研究模型？**

不支持。Coding Plan 不支持转化研究模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型精准医疗模型？**

不支持。Coding Plan 不支持精准医疗模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型个性化医疗模型？**

不支持。Coding Plan 不支持个性化医疗模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型远程医疗模型？**

不支持。Coding Plan 不支持远程医疗模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型移动医疗模型？**

不支持。Coding Plan 不支持移动医疗模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型智慧医疗模型？**

不支持。Coding Plan 不支持智慧医疗模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型数字医疗模型？**

不支持。Coding Plan 不支持数字医疗模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型虚拟医疗模型？**

不支持。Coding Plan 不支持虚拟医疗模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型增强现实医疗模型？**

不支持。Coding Plan 不支持增强现实医疗模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型虚拟现实医疗模型？**

不支持。Coding Plan 不支持虚拟现实医疗模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型混合现实医疗模型？**

不支持。Coding Plan 不支持混合现实医疗模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型人工智能医疗模型？**

不支持。Coding Plan 不支持人工智能医疗模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型机器学习医疗模型？**

不支持。Coding Plan 不支持机器学习医疗模型，所有模型均为文本模型。

### **Coding Plan 是否支持模型深度学习医疗模型？**

不支持。Coding Plan 不支持深度学习医疗模型，所有

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-for-coding-plan.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)


