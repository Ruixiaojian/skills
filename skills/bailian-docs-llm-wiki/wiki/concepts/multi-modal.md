# 多模态能力

多模态能力指百炼平台模型对文本、图像、视频、音频等多种数据类型进行联合理解、生成与推理的能力，支持跨模态信息融合与协同处理，是构建智能体、内容创作、工业质检等复杂AI应用的核心基础。

## 在百炼平台的不同场景中，这个概念如何使用

多模态能力并非单一模型特性，而是贯穿多个能力域的底层技术范式，在以下典型场景中体现为具体能力组合：

- **视觉理解与推理**：`qwen3.7-plus`、`qwen3.5-omni-plus` 等全模态大模型可同时接收文本指令 + 多张图像/视频片段，执行OCR识别、图表解析、视频事件定位、结构化输出（如JSON）及Function Calling（例如调用天气API后结合截图分析出行建议）。单请求最多支持2048张图片或64段视频，输入按统一Token规则计费（图像Token ≈ h×w/(32×32)+2）。

- **音视频端到端处理**：`qwen3.5-omni-plus-realtime` 支持语音输入→文本理解→工具调用→语音合成全流程，无需拆解ASR/TTS模块；S2S模型可直接处理带背景音的语音流，并在响应中保留语调、节奏等声学特征。

- **生成类多模态协同**：  
  - 图像生成中，`wan2.7-image-pro` 接收文本+参考图+风格图三重输入，实现精准可控的图文混合生成；  
  - 视频生成中，`wan2.7-t2v-2026-06-12` 支持“[prompt](../guides/prompt.md) + 自定义音频文件注入”，实现音画同步生成；  
  - 3D生成中，`Tripo/Tripo-H3.1` 允许文生3D、单图生3D或多图（前/左/后/右）联合重建，输入模态决定几何重建精度与纹理生成策略。

- **跨模态检索与重排序**：`qwen3-rerank` 可对图文混合结果集（如含标题、缩略图、描述的搜索项）进行联合语义重排序；`text-embedding-v4` 虽为文本模型，但其向量空间经多模态对齐训练，可与图像Embedding模型（如`qwen-vl-embed`）共用相似度计算，支撑跨模态检索。

> ⚠️ 注意：并非所有模型均具备完整多模态能力。例如 `qwen-long`（10M上下文）专注长文本处理，**不支持图像/视频输入**；`qwen3.7-max` **不支持结构化输出与Function Calling**，即使输入含多模态数据，也仅作单向理解，无法触发工具链。选型时请以[model experience](model-experience.md)中各模型的能力矩阵为准。

## 关键参数和配置

多模态能力的启用与控制依赖以下关键参数（均置于`parameters`对象内，部分需配合特定请求头）：

| 参数 | 类型 | 说明 | 典型值/约束 | 适用模型示例 |
|------|------|------|-------------|--------------|
| `max_image_count` / `max_video_count` | integer | 单请求最大媒体数量 | `qwen3.7-plus`: 2048 / 64；`qwen3.5-omni-plus`: 256 / 512 | 全模态理解模型 |
| `enable_thinking` | boolean | 启用分步推理模式（Chain-of-Thought），提升复杂多模态任务准确率 | `true` / `false`（默认`false`） | `qwen3.7-plus`, `qwen3.6-flash` |
| `tool_choice` | string / object | 控制工具调用策略（自动/指定/禁用），影响多模态意图识别后的动作决策 | `"auto"`, `"required"`, `{"type": "function", "function": {"name": "get_weather"}}` | 支持Function Calling的全模态模型 |
| `X-DashScope-Async` | request header | **强制异步调用标识**，所有耗时多模态生成任务（视频/3D）必须设置为`"enable"` | `"enable"`（必填） | `happyhorse-1.1-t2v`, `Tripo/Tripo-H3.1` |
| `audio` | boolean | 视频生成中是否启用音频轨道合成 | `true`（默认）/ `false` | `wan2.7-t2v-2026-06-12`, `happyhorse-1.1-t2v` |
| `texture_quality` / `geometry_quality` | string | 3D生成中贴图精细度与网格面数控制，直接影响多图输入的重建保真度 | `"standard"` / `"detailed"`；`"standard"` / `"ultra"` | `Tripo/Tripo-H3.1` |

> ✅ 实用提示：  
> - 多模态输入必须通过`input`字段统一组织（非`messages`），格式为`{"messages": [...]}`（文本为主）或`{"media": [...], "prompt": "..."}`（媒体为主）；  
> - 混合输入时，**图像/视频URL必须为公网可访问的HTTPS链接**，且需提前校验可用性（3D生成要求JPEG/PNG，分辨率20–6000像素）；  
> - 所有异步多模态任务（视频/3D）的`task_id`有效期严格为24小时，结果URL（如`pbr_model_url`）仅保留2小时，请及时下载。

## 面向开发者，简洁实用

- **快速验证**：用`curl`测试`qwen3.7-plus`的图文理解能力：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "qwen3.7-plus",
          "input": {
            "messages": [
              {
                "role": "user",
                "content": [
                  {"type": "text", "text": "这张图里有哪些商品？价格分别是多少？"},
                  {"type": "image_url", "image_url": {"url": "https://example.com/product.jpg"}}
                ]
              }
            ]
          },
          "parameters": {"max_output_tokens": 1024}
        }'
  ```

- **避坑指南**：  
  - ❌ 不要对`qwen-long`传入图片——会返回`400 Bad Request`；  
  - ❌ 不要省略`X-DashScope-Async: enable`调用视频/3D接口——会报错`current user api does not support synchronous calls`；  
  - ✅ 优先使用业务空间专属域名（如`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），多模态请求延迟降低30%+；  
  - ✅ 生产环境务必显式设置`max_output_tokens`，避免长输出导致超时或计费激增。

多模态能力的本质是“统一接口、混合输入、协同输出”。开发者只需关注业务需求的数据组合（文+图？音+视？文+图+3D？），平台将自动调度最适配的模型与计算资源——你负责定义“做什么”，我们负责实现“怎么做”。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [qwen api reference](../api/qwen-api-reference.md)


