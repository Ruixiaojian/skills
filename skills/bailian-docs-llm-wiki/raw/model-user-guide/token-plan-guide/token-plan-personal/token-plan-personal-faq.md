# 常见问题

Token Plan 个人版的额度、购买、订阅和接入常见问题。

## **额度与限额**

### 5 小时/7 天限额是什么意思？

Token Plan 个人版采用每 5 小时滚动窗口和每 7 天固定窗口双重限额，限额单位为 Credits。任一窗口累计消耗达到限额后暂停服务，需等待对应窗口结束后额度重置。窗口期内未用完的额度不结转至下一周期。**其中每 5 小时限额当前限时取消，暂不限制。**

例如：Standard 套餐的 7 天限额为 10,000 Credits。您在 7 月 20 日首次调用，系统开启窗口（7 月 20 日 ~ 7 月 27 日）。7 月 20 日消耗 4,000 Credits，7 月 22 日消耗 6,000 Credits，累计 10,000 Credits 触顶暂停。需等到 7 月 27 日窗口结束，额度重置为 10,000 Credits，服务恢复。

各档位限额如下：

**档位**

**5 小时限额**

**7 天限额**

Lite 套餐

700 Credits  
限时 **无限制**  

2,500 Credits

Standard 套餐

3,000 Credits  
限时 **无限制**  

10,000 Credits

Pro 套餐

12,000 Credits  
限时 **无限制**  

40,000 Credits

### 7 天限额是固定日期重置吗？

不是。7 天限额采用固定窗口机制，自首次调用起计时 7 天，到期后额度重置。重置时间取决于您首次调用的时间，而非固定的日历日期（如每周一）。

### 额度用完了怎么办？

限额用完后调用会被阻断，不会按量计费。恢复方式：

-   等待额度释放。
    
-   升级套餐。
    
-   购买用量包，获得不受限额约束的额外额度。
    

### 开通 Token Plan 后为什么仍产生按量扣费？

开通 Token Plan 后仍看到按量扣费，通常是以下原因导致：

-   **生效前调用**：开通 Token Plan 之前发生的调用属于独立计费，无法被套餐抵扣。
    
-   **配置错误**：未使用 Token Plan 专属 API Key 和 Base URL（例如误用百炼通用 dashscope.aliyuncs.com 或 Coding Plan 的 Key），导致请求走按量计费通道。
    
-   **模型不支持**：调用了 Token Plan 白名单之外的模型（如 Qwen3-VL-Plus 及部分子型号）。
    

已产生的按量费用无法通过 Credits 事后抵扣或退款。请立即检查并更正 API Key 和 Base URL 配置，确保后续调用正常抵扣。

### 用量包和套餐是什么关系？需要先买套餐吗？

用量包是套餐的补充，提供不受套餐限额约束的额外 Credits，需先订阅有效套餐后才能购买，最多同时持有 5 个。

### 用量包的额度有窗口限制吗？

没有。用量包额度不受套餐的 5 小时和 7 天窗口限额约束，购买后即可使用。

### 用量包有效期多久？

用量包有效期为 1 个月，到期后未使用的额度自动作废，不支持退款。

### Token Plan 的用量在哪里查看？

在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/token-plan)的 **Token Plan > 我的订阅** 页面查看当前订阅的 Credits 额度及消耗情况。

### 为什么账单/插件统计的 Credits 消耗与预期不一致？

Credits 消耗与账单或插件统计出现差异，常见原因：

-   **上下文缓存命中**：命中缓存时抵扣系数较低，未命中时抵扣系数较高。
    
-   **模型系列差异**：不同模型（如 Qwen 系列与 GLM 系列）的 Credits 抵扣系数不同。
    
-   **功能模式影响**：频繁切换工具调用或思考模式可能影响计费。
    

验证方法：对比具体时间段内的抵扣记录，通过“抵扣 Credits ÷ 消耗 Token”计算实际系数进行核实。

### Credits 的换算规则、消耗延迟和缓存命中统计是怎样的？

-   **Credits 与 Token 换算规则**：Token Plan 的 Credits 与 Token 目前没有固定的公开换算系数，不同模型（如 Qwen3.7-Max 与 `DeepSeek-V4-Flash`）的计费倍数由模型判定，具体消耗量请以账单页面展示为准。
    
-   **额度消耗延迟与心跳设置**：控制台额度统计存在数据同步延迟，未操作时看到的额度变化，可能是之前操作产生的消耗稍后同步显示的结果；将心跳参数设置为 `heartbeat=0` 可以减少额度消耗，但可能仍会有其他定时任务产生少量消耗。
    
-   **缓存命中统计**：当前 Token Plan 控制台界面暂不提供缓存命中统计功能。
    

### Token Plan 的 Credits 消耗是如何计算的？

计算公式：消耗 Credits = 调用模型目录价 × 100，目录价由输入、输出及缓存 Token 分别乘以对应官方定价累加得出。实际消耗没有固定倍率，取决于模型类型、Token 用量、思考模式及工具调用等因素。

额度消耗过快的常见原因：第三方工具多轮隐式调用、长上下文输入 Token 消耗大、缓存命中等。相比按量付费，Token Plan 有折扣优惠且可叠加免费额度。

### Token Plan 是否提供免费试用额度或赠送 Token？

Token Plan 套餐本身不提供试用额度，也不包含免费赠送的 Token 额度。百炼平台针对部分模型提供独立的免费额度，可以在控制台查询可用免费额度的模型列表。

### 如何减少 Token Plan 的 Credits 消耗？

-   压缩历史消息或新开对话窗口，避免长上下文累积消耗。
    
-   关闭思考模式（Thinking Mode）以降低推理开销。
    
-   非复杂任务场景下切换至轻量模型（如 qwen3.6-plus 替代 qwen3.7-max）。
    
-   利用缓存机制，缓存命中的 Token 计费价格低于正常 Input Token。
    
-   通过**用量分析**页面监控消耗明细，及时调整使用策略。
    

### Token Plan Credits 消耗明细是否支持导出下载？

目前不支持直接下载 Credits 消耗明细，需使用主账号登录百炼控制台查看。若需获取团队成员用量统计或账单数据，可前往阿里云费用中心的**账单明细**页面查询并导出 CSV 文件。

### 是否支持通过 API 查询 Token Plan 剩余额度或用量？

目前暂未开放查询 Token Plan 剩余额度的 OpenAPI 接口（出于安全考虑，防止盗刷）。可以登录百炼控制台 **Token Plan** 页面查看套餐及用量包详情，或在**用量分析**页面查看消耗明细。

### 为什么第三方工具（如 Claude Code）显示的 Token 用量与百炼控制台统计不一致？

-   **统计口径不同**：第三方工具仅显示模型层面的输入输出 Token；百炼控制台统计包含完整消耗项。
    
-   **隐藏消耗项**：系统提示词、工具定义（Schema）、用户配置、项目约定、多轮对话历史累积、工具调用参数与返回结果、模型内部推理内容（reasoning）等，均会计入 Credits 消耗但不在第三方工具中显示。
    
-   **模型单价影响**：Credits 消耗与模型抵扣系数相关，高价模型（如 qwen3.7-max）会导致相同 Token 数下 Credits 消耗更高。
    
-   **优化建议**：通过百炼控制台 Token Plan 订阅页的**用量分析**查看官方统计；使用 `/compact` 压缩历史消息或 `/clear` 新开对话以减少上下文累积。
    

### 模型监控是否支持查看 Token Plan 用量？

不支持。当前模型监控功能仅支持监控按量付费产生的模型调用记录，暂不支持监控 Token Plan（资源包）的用量。如需查看 Token Plan 消耗情况，请前往费用与成本控制台查询。

### 服务器关机是否能避免 Token Plan 额度消耗？

可以。Token Plan 仅在发生实际模型调用时才会扣除 Credits，不使用服务时将服务器关机可以完全避免 API 调用，从而避免额度消耗。

### Credits 配额用尽时如何区分是免费额度还是 Token Plan 额度耗尽？

在百炼控制台**我的订阅**页面可查看 Token Plan 额度使用情况。若提示 Credits 配额用尽但 Token Plan 仍有剩余，通常是因为当前使用的是免费试用额度；请确认当前调用使用的是 Token Plan 专属 API Key，而非普通 API Key。

### 如何查看 Token Plan 的详细用量及排查配额消耗异常？

-   **查看路径一**：登录 Token Plan 控制台 > **我的订阅** > **Token Plan** 标签页，查看总配额使用量。
    
-   **查看路径二**：登录费用与成本控制台 > Token Plan 页面，查看总 Credits、剩余余额、过期倒计时及基于时间的详细使用情况。
    
-   **异常排查**：若发现配额飙升且无法追踪，请结合上述两个页面的明细数据进行比对分析。
    

## **接入报错**

### 常见报错及解决方案

**报错信息**

**可能原因**

**解决方案**

401 InvalidApiKey: No API-key provided.

请求头中未携带 API Key

生成 API Key 并在工具中完成配置

401 InvalidApiKey: Invalid API-key provided.

误用了按量计费的 API Key 或 Coding Plan 的 Key；订阅过期；Key 复制不完整

确认使用 Token Plan 个人版 API Key，确保完整且无空格

404 model 'xxx' not found or not supported

模型名称拼写错误或不在支持列表

确认模型名称区分大小写，与套餐支持的模型 ID 一致。

401 invalid access token or token expired

误用了 Coding Plan 或其他计费模式的 Base URL

使用 Token Plan 个人版 Base URL

401 Incorrect API key provided

误用了百炼通用 Base URL（dashscope.aliyuncs.com）

使用 Token Plan 个人版 Base URL

429 Requests rate limit exceeded

短时间内请求过于密集

等待一分钟后重试，降低请求频率

429 Allocated quota exceeded

5 小时或 7 天限额用尽

等待窗口释放额度

502 Bad Gateway（错误码 4028）

纯文本模型无法处理图像请求，或模型内部异常

切换支持的模型重试，并确认请求内容与模型能力匹配

页面提示“服务不可用，请求已过期”

控制台会话超时，或订阅过期后 Key 失效

刷新页面或重新登录；若曾过期中断后重新订阅，需重新获取并替换 API Key

### 第三方工具接入/测试报错如何排查？

**Q1：第三方工具无法接入 Token Plan 怎么办？**

1.  确认使用 Token Plan 专属 Base URL 与 API Key（参见「快速开始」），未误用百炼通用或 Coding Plan 的 Key/Base URL。
    
2.  部分第三方工具可能未对百炼 Token Plan 进行兼容优化，建议咨询工具服务方确认兼容性。
    
3.  对于支持自定义 Anthropic 兼容端点的工具，可使用 `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` 自定义接入。
    
4.  若工具不兼容，建议更换已支持的 AI 工具（如 Cursor、Claude Code、Qwen Code 等）。
    

**Q2：第三方工具的连接测试不通过，但实际调用似乎正常，怎么办？**

部分第三方工具自带的模型连接测试功能可能不准确，测试不通过不代表服务不可用，请以实际调用返回结果为准。若调用异常，可按以下顺序排查：

1.  确认使用 Token Plan 专属 API Key 与 Base URL（个人版专属地址），未误用百炼通用 dashscope.aliyuncs.com 或 Coding Plan 的 Key/Base URL。
    
2.  检查服务器能否访问 Token Plan 接入域名 `token-plan.cn-beijing.maas.aliyuncs.com`。
    
3.  重启客户端或服务以排除临时故障后重试。
    

**Q3：为什么后台健康检查/测试按钮报错，但实际客户端可用？**

后台测试脚本发送固定参数的极简请求，部分模型对参数校验严格，可能报 400 错误，但不代表服务不可用。验证方法：直接在实际客户端（如 Cursor、`ChatBox`、Cherry Studio 等）配置 API Key 并发送真实消息测试，能正常回复即说明渠道正常，可忽略测试报错。

### Token Plan 用量显示为 0 或调用仍扣费/欠费怎么办？

-   用量显示为 0 通常是因为尚未产生实际消耗，或使用了非 Token Plan 专属 API Key。
    
-   调用仍扣余额或产生欠费，是因为配置了普通 API Key 而非套餐专属 Key。
    
-   解决方法：进入控制台**我的订阅**页面获取专属 API Key，确保在工具配置中使用该专属 Key 发起调用。
    

## **并发与性能**

### 最多支持多少个 Agent 并发？

并发能力与套餐档位相关：

**档位**

**建议并发**

Lite 套餐

可同时支持 1-2 个 Agent 并发运行

Standard 套餐

可同时支持 3-4 个 Agent 并发运行

Pro 套餐

可同时支持 6-8 个 Agent 并发运行

### 高峰期响应会变慢吗？

高峰期可能出现排队等待。如需更稳定的吞吐，可升级到更高档位或使用团队版。

### Token Plan 的限流阈值（TPM/RPM）是多少？能否提升？

官方未公开具体的 TPM/TPS/RPM 数值，限流阈值会根据整体负载动态调整以保障服务稳定性。套餐限流额度不支持提升。

优化建议：精简上下文、降低任务复杂度以减少单次输入 Token 数量；遇到限流时等待约 1 分钟后重试。

## **使用规则**

### "禁止 API 生产自动化调用"具体是什么意思？

Token Plan 个人版仅供个人通过官方指定工具（如 Cursor、Claude Code、Windsurf 等）进行交互式开发。不允许将 API Key 用于生产环境的自动化服务、批量脚本或后台定时任务等非交互场景。

### 多人共用一个账号可以吗？

不可以。Token Plan 个人版限单人使用，不允许多人共用同一账号或 API Key。如需多人协作，请使用 Token Plan 团队版。

### 可以在多台设备上使用同一个 API Key 吗？

可以。Token Plan 个人版每个订阅对应一个专属 API Key，生成后请立即复制并妥善保存。您可以将同一个 API Key 配置到多台设备（如家庭电脑和公司电脑）上使用，无需为每台设备重新生成。

**重要**

重置 API Key 会使旧 Key 立即失效，届时需在所有设备上更新为新 Key。建议仅在 Key 泄露时才重置。

### Token Plan 与 AI 通用型节省计划、Coding Plan 有什么区别？

-   **计费模式**：Token Plan 为预付费订阅，以 Credits 统一计量抵扣；AI 通用型节省计划是承诺月消费金额换取按量账单折扣；Coding Plan 仅支持特定名单模型且已停止新购/续费。
    
-   **适用场景**：Token Plan 适合团队交互及主流 AI 编程工具（如 Claude Code、Cursor）使用；节省计划适合 API 调用及应用开发，灵活性最高；Coding Plan 仅限 IDEA 等特定环境。
    
-   **配置差异**：Token Plan 需使用专属 API Key 和 Base URL，无法与节省计划叠加抵扣（Key 互斥）；节省计划使用通用 Key 自动抵扣。
    
-   **模型支持**：Token Plan 支持广泛的文本/图像生成模型；节省计划适用于百炼平台所有按量计费模型；Coding Plan 仅支持 qwen3.7-plus、glm-5 等指定模型。
    

### Token Plan 与其他计费方式或产品有什么区别？

-   **Token Plan vs 阿里云账号充值（节省计划）**：Token Plan 为包月制，使用专属 Base URL 和 API Key，适合重度/团队用户；节省计划为按量付费承诺消费折扣，使用通用 URL 和 API Key，适合轻度/个人用户。
    
-   **名称说明**：`ModelStudio Token Plan`、Token Plan 团队版、`ModelStudio Standard` 仅为自定义显示名称，计费方式相同，可通过配置链接是否以 token plan 开头确认。
    
-   **算法备案**：Token Plan 作为订阅模式无需备案，仅应用上架需备案。
    
-   **记忆系统**：Token Plan 仅提供额度，不包含员工工作记忆，记忆数据归属于智能体应用。
    

### Token Plan 与私网连接（`PrivateLink`）、通义灵码是什么关系？

-   **与 `PrivateLink`**：两者独立计费，无直接依赖关系；`PrivateLink` 是网络产品，用于私网访问百炼服务，不直接使用 Token Plan。
    
-   **与通义灵码**：通义灵码仅限 IDEA 等 IDE 使用，而 Token Plan 支持 Claude Code、Cursor、`OpenClaw` 等多种调用方式；两者为独立产品，需分别购买。
    

### Token Plan 何时更新支持新模型？

Token Plan 支持的模型会不定期更新，最新模型列表请参见控制台**模型列表**页面或**模型广场**。

## **购买与订阅**

### RAM 用户可以使用 Token Plan 吗？

可以，需由主账号完成以下授权：

1.  在 [RAM 控制台](https://ram.console.aliyun.com/)为该 RAM 用户授予 `AliyunTokenPlanReadOnlyAccess`（只读）或 `AliyunTokenPlanFullAccess`（管理）系统策略，同时授予 `AliyunBSSReadOnlyAccess` 系统策略。
    
2.  在百炼控制台[账号管理](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/uac-admin/organization/members/list)页面，为该 RAM 用户分配管理员或订阅套餐权限。
    

### 可以升配吗？升配后额度怎么算？

支持从低档位升级到更高档位。升级按剩余时长补缴差价，升级后限额立即提升至新档位对应额度。

### 可以降配吗？

不支持降配。如需更换为更低档位，可在订阅到期后重新购买。

### 自动续费怎么取消？

登录[百炼控制台 Token Plan](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/token-plan) 页面，在订阅管理中关闭自动续费。

### Token Plan 如何升级、退订或变更订阅周期？退款金额如何计算？

-   **周期变更**：不支持月包直接变更为年包，需先退订当前月包（退还剩余金额），待实例释放后重新购买年包。
    
-   **升级规则**：升级费用按原订单剩余时间按比例折算成额度下发，支付金额相应减少。
    
-   **退订退款**：退款金额 =（额度剩余量 ÷ 总量）× 实付金额，或由系统根据实例剩余价值核算；退订需在到期前办理，费用约 2 个工作日内退回原支付账户。
    
-   **特殊场景**：自助退订入口不可用时需提交工单处理；续费订单生效前的消耗仍计入上一周期。
    

### Token Plan 套餐用完或退订后如何切换为按量付费模式？

-   套餐额度用完后，可购买用量包补充额度继续使用，或等待窗口期重置。
    
-   如需切换为按量付费，可退订原 Token Plan 套餐，退订生效后该实例抵扣的产品将自动切换为按量付费模式。
    
-   也可选择购买节省计划，或直接使用按量付费 API Key 调用。
    

### 如何查看 Token Plan 套餐的生效时间和剩余天数？

-   **生效时间查看路径**：登录[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/token-plan)的 **Token Plan** 页面查看套餐生效时间。
    
-   **剩余天数显示逻辑**：控制台显示的剩余天数为向下取整后的完整 24 小时周期数，实际有效期以具体结束时间戳为准（例如剩余 22 天 20 小时会显示为 22 天），属正常显示逻辑。
    

### Token Plan 已使用的额度支持退款吗？

不支持。Token Plan 套餐一旦产生额度抵扣（即已使用），已使用的部分不支持退款。

### Token Plan 是否支持学生代金券购买？

不支持。学生代金券仅适用于活动界面指定的产品，不能用于购买 Token Plan。

### 购买 Token Plan 后是否需要额外购买算力或 Plus 资源包？

不需要。订阅 Token Plan 后，直接在控制台订阅页面获取专属 API Key，即可使用套餐包含的模型和工具权益。
