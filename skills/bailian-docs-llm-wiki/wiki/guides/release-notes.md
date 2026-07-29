# release notes

百炼平台的 Release Notes 汇总了近期模型能力更新与平台功能演进，涵盖新模型上线、已有模型迭代、API 能力增强及基础设施升级。所有变更均面向开发者设计，聚焦可编程性、稳定性与生产就绪性。详细变更请参考 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 和 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。

## 支持的模型/功能

- **新增模型（2026年7月重点）**：  
  - `qwen3.7-flash` 与 `qwen3.7-flash-2026-07-15`：Qwen3.7原生视觉语言Flash模型，强化多模态Agent执行能力，支持Search Agent、CI Agent等端到端任务；  
  - `qwen-image-3.0-pro`：图片生成模型，支持4.5k token输入、10px小字渲染、12国语言+20+字体原生渲染，适用于报纸/分镜/试卷等复杂版面；  
  - `kimi/kimi-k3`：2.8万亿参数旗舰模型，原生视觉理解，100万token上下文，全球首个开源3万亿级模型；  
  - `qwen3.7-text-embedding`：多语言文本向量模型，支持256~2560维自定义维度，在MTEB多语言检索任务上较v4提升20%；  
  - `qwen-audio-3.0-tts-plus` / `qwen-audio-3.0-tts-flash`：分别面向专业音质与实时交互场景，均支持更多方言/小语种、free-style指令控制及复杂声学环境鲁棒性优化；  
  - `qwen-audio-3.0-realtime-plus` / `qwen-audio-3.0-realtime-flash`：实时双工语音对话模型，登顶Artificial Analysis Speech-to-Speech评测榜首，“Plus”侧重高质量回复，“Flash”侧重首包延时≤200ms；  
  - `pixverse/pixverse-upscale` / `pixverse/pixverse-motioncontrol` / `pixverse/pixverse-lipsync`：视频生成三件套，分别提供超分至4K、动作迁移、精准对口型能力；  
  - `vidu/viduq3-*` 系列（如 `viduq3-pro-fast_img2video`, `viduq3-drama_reference2video`, `viduq3-ad_reference2video`）：覆盖图生视频、剧集/广告专用模型，支持16秒长视频、直出音效与营销级切镜；  
  - `glm-5.2-fast-preview`：GLM-5.2高速预览版，1M上下文，TPS达标准版1.5~2倍，适用于流式代码生成与Agent多轮调用。

- **平台级功能新增**：  
  - 新增 **智能体托管运行时 API**（2026-06-29），平台统一托管会话状态与工具执行生命周期；  
  - 新增 **知识检索服务** 与 **知识问答服务**（2026-06-23），支持多知识库联合检索与混合排序；  
  - 新增 **Skill 能力包**（2026-06-10），智能体可声明式接入官方或自定义技能；  
  - 新增 **数据连接模块**（2026-06-10），支持MySQL/语雀/OSS等数据源直连；  
  - 新增 **Responses API 异步调用模式**（2026-06-01），通过 `background=true` 提交长耗时任务并轮询结果；  
  - 新增 **模型导入 API**（2026-06-03）与 **国际站模型导入功能**（2026-06-05），支持从OSS导入LoRA微调模型；  
  - 新增 **临时 API Key 生成能力**（2026-06-03），适用于不可信环境下的安全鉴权。

> **注意**：文档中 `kimi/kimi-k2.7-code-highspeed` 描述为“与普通版是同一个模型”，但 `kimi/kimi-k2.7-code` 在同文档中被标注为独立模型ID；实际调用时请以控制台或API返回的模型元数据为准，避免硬编码别名。该矛盾已在 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 中体现。

## 关键参数

- **上下文长度**：`kimi/kimi-k3`、`glm-5.2`、`xiaomi/mimo-v2.5-pro`、`deepseek-v4-pro` 等主流旗舰模型均支持 **100万token** 上下文；`qwen3.7-max-2026-06-08` 及后续版本已启用视觉模态，但纯文本上下文仍维持1M；  
- **向量维度**：`qwen3.7-text-embedding` 支持 **256~2560维** 用户自定义输出维度；  
- **语音合成延迟**：`qwen-audio-3.0-tts-flash` 首包延时 ≤ **200ms**；`qwen-audio-3.0-realtime-flash` 端到端响应时延经并行推理优化后处于低水平；  
- **视频生成时长**：`vidu/viduq3-pro-fast_img2video` 支持 **16秒** 视频生成（较ViduQ2-Pro-fast扩展6秒）；`pixverse/pixverse-v6-r2v` 支持 **15秒长视频** 直出；  
- **OCR精度**：`qwen3.5-ocr` 在国内国际身份证、驾驶证等卡证关键信息抽取任务上效果显著提升；  
- **模型压缩**：2026年5月上线的[模型压缩模块](../../raw/model-user-guide/release-notes/model-release-notes.md)支持量化转低精度版本，降低部署成本。

## 使用方式

- **模型调用**：所有新模型均通过标准 DashScope API 接入，使用 `model` 字段指定模型ID（如 `"model": "qwen3.7-flash"`），无需额外配置；  
- **异步任务**：对长耗时请求（如视频生成、大文件RAG），推荐使用 Responses API 的 `background=true` 参数，并轮询 `/v1/tasks/{task_id}` 获取结果；  
- **知识库集成**：启用知识检索服务需先创建知识库，再通过 `/v1/knowledge_retrieval` 接口提交查询，支持 `top_k` 与 `filter` 参数；  
- **Skill 调用**：在智能体工作流中通过 `skills: ["web_search", "calculator"]` 声明所需能力，平台自动路由至对应服务；  
- **临时凭证**：敏感环境调用应使用 `/v1/auth/token` 接口生成临时API Key，有效期可设为1~3600秒，避免永久密钥泄露；  
- **模型导入**：LoRA微调模型需上传至OSS，调用 `POST /v1/models/import` 提交导入任务，成功后返回可部署的模型ID。

## 限制和注意事项

- **模型下线**：2026年7月起执行分批下线策略，`部分老旧模型下线通知`（7月10日）与 `部分老旧长尾模型下线通知`（7月9日）已明确淘汰范围，详见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-release-notes.md)；  
- **地域限制**：新增美国、德国、日本地域部署（2026-06-12），但部分模型（如 `qwen-image-3.0-pro`）暂未全地域开放，调用前需确认目标Region可用性；  
- **输入约束**：`qwen-image-3.0-pro` 支持最大4.5k token输入，但图像分辨率建议≤1024×1024以保障生成质量；`vidu/viduq3-*` 系列参考生视频模型要求输入图片数为0–14张（非全部型号均支持上限14张，具体见各模型文档）；  
- **音频处理**：`fun-asr-flash-2026-06-15` 支持5分钟以内音频转写，超时将截断；`qwen3.5-livetranslate-flash-realtime` 支持60种语言听、29种语言说，但实时翻译需保持稳定网络连接；  
- **计费变更**：`qwen-turbo` 资源包已于2026-06-28启动退市，存量资源包到期后不可续购；`GLM-5.2 Fast mode` 于7月14日降价，调用时需显式指定 `mode: "fast"` 才享受新资费；  
- **SDK兼容性**：多模态交互开发套件已提供 Android/iOS Lite SDK、Linux C++ SDK、RTOS C SDK 及 Java SDK，但各SDK功能覆盖不完全（如Lite SDK不支持音色复刻），选型时请核对 [多模态交互开发套件](../../raw/model-user-guide/release-notes/model-release-notes.md) 文档。

## 来源文档

- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


