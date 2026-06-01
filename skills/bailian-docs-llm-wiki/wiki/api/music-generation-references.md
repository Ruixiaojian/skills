# music generation references

百炼平台提供音乐生成能力，当前支持 Fun-Music 模型，可通过文本提示词或歌词输入自动生成歌曲。本文汇总音乐生成相关 API 的模型信息、核心参数、调用方式及使用限制，供开发者快速查阅。

## 支持的模型

| 模型名称 | 模型标识 | 状态 | 部署区域 |
|---------|---------|------|---------|
| Fun-Music | `fun-music-v1` | 邀测（需在模型广场申请开通） | 中国内地（北京地域） |

根据 [音乐生成Fun-Music API参考](../../raw/model-api-reference/music-generation-references/fun-music-api.md)，该模型支持两种输出模式：**非[流式输出](../concepts/streaming.md)**和**[流式输出](../concepts/streaming.md)**（基于 SSE）。

## 服务端点与认证

- **端点**：`POST https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation`
- **协议**：HTTPS
- **认证**：请求头 `Authorization: Bearer {api-key}`
- **[流式输出](../concepts/streaming.md)**：设置请求头 `X-DashScope-SSE: enable`

使用前需先获取 API Key。

## 关键参数

### 输入参数（input 对象）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `lyrics` | string | 条件必选 | 歌词内容，与 `prompt` 二选一。同时传入时仅 `lyrics` 生效 |
| `prompt` | string | 条件必选 | 提示词，模型据此自动创作歌词并生成歌曲，与 `lyrics` 二选一 |
| `gender` | string | 否 | 演唱声音性别，可选 `male` / `female`，默认 `female` |
| `format` | string | 否 | 音频编码格式，可选 `mp3`（默认）/ `wav` |
| `enable_aigc_watermark` | boolean | 否 | AIGC 水印开关，默认 `false`。开启后在音频末尾追加摩尔斯电码信号 |

### 字符限制

如 [音乐生成Fun-Music API参考](../../raw/model-api-reference/music-generation-references/fun-music-api.md) 所述，不同模式下的输入长度限制有所差异：

| 参数 | 非流式模式 | 流式模式 |
|------|-----------|---------|
| `lyrics` | 中文 5~350 字符，英文 5~2000 字符 | 中文 300~350 字，英文 200~250 词 |
| `prompt` | 1~2000 字符 | 5~1000 个中文汉字或英文单词 |

> **注意**：流式模式下 `lyrics` 的最小长度要求（300 字 / 200 词）远高于非流式模式（5 字符），使用流式输出时需确保歌词内容足够长。

## 使用方式

**非流式调用示例：**

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "fun-music-v1",
    "input": {
        "prompt": "夏日清新民谣，木吉他与口琴伴奏，轻快节奏，适合旅行Vlog背景音乐",
        "gender": "female"
    }
}'
```

**流式调用示例：**

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "fun-music-v1",
    "input": {
        "prompt": "节奏感强的电子舞曲，合成器音效，充满能量，适合健身运动场景",
        "gender": "male"
    }
}'
```

## 返回结构

返回对象的核心字段：

| 字段路径 | 类型 | 说明 |
|---------|------|------|
| `output.audio.url` | string | 完整音频文件的 OSS URL，有效期 **24 小时** |
| `output.audio.data` | string | 流式模式下的 Base64 音频数据片段；非流式为空字符串 |
| `output.audio.id` | string | 音频文件 ID |
| `output.audio.expires_at` | integer | URL 过期时间戳（Unix timestamp） |
| `output.extra_info.lyrics` | string | 生成的歌词内容 |
| `output.extra_info.channels` | integer | 声道数（如 2 为立体声） |
| `output.extra_info.sample_rate` | string | 采样率（如 "48000"） |
| `output.finish_reason` | string | `null` 生成中；`stop` 生成结束 |
| `usage.duration` | integer | 音乐时长（秒），用于计费 |

流式模式下，中间消息通过 `data` 字段返回 Base64 音频片段，最终消息包含完整的 `url`、`extra_info` 和 `usage` 信息。

## 限制与注意事项

- **邀测阶段**：根据 [音乐生成Fun-Music API参考](../../raw/model-api-reference/music-generation-references/fun-music-api.md)，Fun-Music 模型目前处于邀测状态，需在模型广场申请开通后方可使用。
- **区域限制**：仅在中国内地（北京地域）部署范围下可用。
- **参数优先级**：当 `lyrics` 和 `prompt` 同时传入时，仅 `lyrics` 生效，`prompt` 被忽略。
- **URL 有效期**：返回的音频 OSS URL 有效期为 24 小时，需及时下载或转存。
- **水印影响**：开启 `enable_aigc_watermark` 会在音频末尾追加摩尔斯电码信号，导致音频时长增加。

## 来源文档

- [音乐生成Fun-Music API参考](../../raw/model-api-reference/music-generation-references/fun-music-api.md)

