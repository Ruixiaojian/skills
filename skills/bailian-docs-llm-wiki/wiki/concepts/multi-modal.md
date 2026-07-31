# 多模态

多模态（Multimodal）指模型能够同时理解、生成或关联多种类型数据（如文本、图像、音频、视频、3D 等）的能力。在百炼平台中，多模态不是单一模型的标签，而是一类跨模态协同能力的统称，体现为模型对异构输入的联合建模能力，以及在统一接口下支持图文混合、音画联动、图生文、文生图、视频理解等端到端任务。

## 在百炼平台的不同场景中，这个概念如何使用

多模态能力在百炼平台中以**模型能力维度**和**API 协议维度**双重落地：

- **模型层面**：  
  - `qwen-vl`、`qwen3-vl-plus`、`qwen3.7-plus` 等 Qwen 系列模型原生支持**视觉语言理解**（VLU），可接收 `messages` 中混入图像 URL 或 base64 编码图像，并结合文本进行推理、问答、OCR、描述生成等；  
  - `qwen-image-*` 系列（如 `qwen-image-3.0-pro`）聚焦**视觉生成**（VLG），支持文生图、图生图、多图参考编辑，其 `input.messages` 可同时包含文本提示与图像对象；  
  - `qwen-audio-*` 模型支持语音识别（ASR）、语音合成（TTS）及音视频理解，实现“听—说—读—写”闭环；  
  - Tripo 3D 和 Vidu 视频模型虽不直接暴露多模态接口，但通过 `prompt + image` 或 `prompt + video` 等组合输入，本质属于**跨模态条件生成**，是多模态在生成侧的延伸。

- **API 协议层面**：  
  - 所有支持多模态的模型统一接入 `/api/v1/services/aigc/multimodal-generation/generation`（图像/图文生成）或 `/api/v1/services/aigc/text-generation/generation`（图文理解），而非传统纯文本路径；  
  - 输入结构采用标准化 `messages` 数组（兼容 OpenAI 格式），每条消息 `content` 可为字符串（文本）或对象数组（含 `type: "image_url"` / `"text"` 字段），例如：
    ```json
    {
      "messages": [
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "这张图里有什么？请用中文分点描述"},
            {"type": "image_url", "image_url": {"url": "https://xxx.jpg"}}
          ]
        }
      ]
    }
    ```
  - 图像、视频、3D 等非文本输入需为公网可访问 URL（推荐）或 base64 编码（部分模型支持），平台自动解析并转换为内部 token 表征。

## 关键参数和配置

- **必填模型标识**：`model` 必须指定明确支持多模态的模型 ID，例如 `"qwen-vl"`、`"qwen3-vl-plus"`、`"qwen-image-3.0-pro"`；使用 `qwen-plus` 等纯文本模型传入图像将返回错误。
- **输入格式**：  
  - 文本+图像混合：使用 `messages` 数组，`content` 为混合类型列表（非字符串）；  
  - 纯图像生成：部分模型（如 `qwen-image-*`）也支持 `input.prompt` 字符串，但推荐统一用 `messages` 保持扩展性；  
  - 图像尺寸与分辨率：单图像素上限约 1600 万（如 `4096×4096`），超限将被自动缩放或报错；视频输入最长支持 2 小时（`qwen3.7-plus`）。
- **输出控制**：  
  - `response_format`：若需结构化输出（如 JSON 描述），需显式设置 `{ "type": "json_object" }`（仅部分多模态模型支持）；  
  - `max_tokens`：建议显式设置，因图像 token 开销大（按 `h×w/(32×32)+2` 估算），避免意外超限；  
  - `stream`：目前多模态理解类接口（如 `qwen-vl`）暂不支持流式响应，生成类接口（如 `qwen-image-3.0-pro`）支持同步流式返回图片 URL。
- **地域与认证**：所有多模态 API 均需 `Authorization: Bearer <API_KEY>`，且部分模型（如 Tripo 3D、Fun-Music）强制限定华北2（北京）地域，调用前需确认 WorkspaceId 与 Endpoint 匹配。

## 面向开发者，简洁实用

- ✅ **优先用 `messages` 而非 `prompt`**：即使只输文本，也用 `[{ "role": "user", "content": "..." }]` 格式，为后续加图留兼容接口；  
- ✅ **图像传 URL，不传本地文件**：确保图片公网可访问（HTTPS），避免 base64 导致请求体过大；  
- ✅ **查模型能力表再选型**：`qwen-vl` 专用于理解，`qwen-image-*` 专用于生成，二者不可互换；  
- ✅ **注意 token 预估**：一张 2048×2048 图 ≈ 4098 tokens，叠加长文本易超 context window（如 `qwen3.7-plus` 为 1M tokens，但实际可用需预留输出空间）；  
- ✅ **错误排查重点**：`400 Bad Request` 多因 `content` 类型不合法（如图像未包装为对象）、`model` 不支持多模态或 URL 无法访问；`429 Too Many Requests` 说明触发多模态专属 RPM/TPM 限流（通常比纯文本更严格）。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [model experience](../guides/model-experience.md)
- [use cases](../guides/use-cases.md)


