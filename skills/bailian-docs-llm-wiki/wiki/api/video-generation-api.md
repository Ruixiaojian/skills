# video generation api

百炼平台的视频生成 API 提供统一的异步调用接口，支持多种模型和多类视频生成任务，包括文生视频、图生视频、参考生视频、视频编辑、数字人等。所有视频生成任务均采用"创建任务 → 轮询获取结果"的异步模式，任务耗时通常为 1-5 分钟。

## 支持的模型与功能

### 通用视频生成模型

| 模型系列 | 支持的任务类型 | 说明 |
|---------|-------------|------|
| **万相 2.7**（推荐） | 文生视频、图生视频（首帧/首尾帧/续写）、参考生视频、视频编辑 | 最新版协议，支持多模态输入（文本/图像/音频/视频），支持多镜头叙事 |
| **万相 2.1-2.6** | 文生视频、图生视频、首尾帧生视频、参考生视频、视频编辑 | 旧版协议，部分功能仅限特定版本 |
| **HappyHorse 1.0** | 文生视频、图生视频（首帧）、参考生视频、视频编辑 | 支持多地域部署（北京/新加坡/弗吉尼亚/法兰克福） |
| **爱诗 PixVerse** | 文生视频、图生视频（首帧/首尾帧）、参考生视频 | 需在控制台单独开通，支持 C1/V6/V5.6 多个版本 |
| **可灵 Kling** | 文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑 | 需在控制台单独开通，支持智能分镜 |
| **Vidu** | 文生视频、图生视频（首帧/首尾帧）、参考生视频 | 需在控制台单独开通，支持 Q2/Q3 Pro/Turbo |

### 数字人与特效模型

| 模型 | 功能 | 说明 |
|------|------|------|
| **wan2.2-s2v**（数字人） | 图片+音频 → 说话/唱歌视频 | 支持全身/半身/肖像，需先调用检测接口 |
| **wan2.2-animate-move**（图生动作） | 人物图片+参考视频 → 动作视频 | 标准/专业两种模式 |
| **wan2.2-animate-mix**（视频换人） | 人物图片+参考视频 → 换人视频 | 保留原视频场景和光照 |
| **AnimateAnyone**（舞动人像） | 人物图片+动作模板 → 舞蹈视频 | 需依次调用检测、模板生成、视频生成三个接口 |
| **EMO**（悦动人像） | 肖像+音频 → 唱演视频 | 适合人物特写，口型自然 |
| **LivePortrait**（灵动人像） | 肖像+音频 → 播报视频 | 快速轻量 |
| **VideoRetalk**（声动人像） | 视频+音频 → 口型替换视频 | 仅支持 API 调用 |
| **video-style-transform** | 视频风格重绘 | 8 种预设风格 |

详细模型参数参见 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/text-to-video-api-reference.md) 和 [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-video-generation-api-reference.md)。

## 调用方式

### 统一接入端点

大多数视频生成模型共享同一个接口路径：

| 地域 | Endpoint |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` |
| 新加坡 | `https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` |

> **注意**：部分模型（如图生动作、视频换人、数字人、AnimateAnyone、EMO 等）使用不同的路径 `/api/v1/services/aigc/image2video/video-synthesis`，请以各模型文档为准。

### 异步调用流程

**步骤 1：创建任务**

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.7-t2v-2026-04-25",
    "input": {
        "prompt": "一只小猫在月光下奔跑"
    },
    "parameters": {
        "resolution": "720P",
        "ratio": "16:9",
        "duration": 5
    }
}'
```

**步骤 2：轮询结果**

```bash
curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 必需请求头

| Header | 值 | 说明 |
|--------|---|------|
| `Content-Type` | `application/json` | 固定值 |
| `Authorization` | `Bearer sk-xxxx` | 百炼 API Key |
| `X-DashScope-Async` | `enable` | **必须设置**，否则报错 |

## 关键参数

### 通用请求体结构

```json
{
    "model": "模型名称",
    "input": {
        "prompt": "文本描述",
        "media": [
            {"type": "first_frame|last_frame|video|reference_image|driving_audio|image_url", "url": "..."}
        ]
    },
    "parameters": {
        "resolution": "720P",
        "duration": 5,
        "ratio": "16:9",
        "prompt_extend": true,
        "watermark": true
    }
}
```

### 常用参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| `resolution` | string | 视频分辨率：`480P`、`540P`、`720P` |
| `duration` | integer | 视频时长（秒），常见值：5、10、15 |
| `ratio` / `aspect_ratio` | string | 画面比例，如 `16:9`、`9:16`、`1:1` |
| `prompt_extend` | boolean | 是否开启智能提示词扩写 |
| `watermark` | boolean | 是否添加水印 |
| `size` | string | 部分模型使用像素尺寸，如 `1280*720` |

> **注意**：不同模型对参数的命名和支持范围不完全一致。例如万相 2.7 使用 `ratio`，可灵使用 `aspect_ratio`；爱诗 PixVerse 使用 `size` 而非 `resolution`。请以各模型的 API 文档为准。

### media 类型说明

| type 值 | 用途 | 适用场景 |
|---------|------|---------|
| `first_frame` | 首帧图像 | 图生视频 |
| `last_frame` | 尾帧图像 | 首尾帧生视频 |
| `video` | 输入视频 | 视频编辑、视频续写 |
| `reference_image` | 参考图像 | 参考生视频 |
| `reference_video` | 参考视频 | 参考生视频（万相2.7） |
| `driving_audio` | 驱动音频 | 音频驱动视频生成 |
| `image_url` | 图像（PixVerse） | 爱诗模型的通用图像输入 |

## 限制和注意事项

### 地域限制

- **模型、Endpoint URL 和 API Key 必须属于同一地域**，跨地域调用将失败
- 部分第三方模型（PixVerse、Kling、Vidu）仅支持北京地域
- 数字人、AnimateAnyone、EMO、LivePortrait、Emoji、VideoRetalk 仅适用于北京地域

### 任务限制

- `task_id` 有效期为 **24 小时**，过期返回 `UNKNOWN` 状态
- **请勿重复创建任务**，创建成功后轮询获取即可
- 并发限制因模型而异，部分模型（如 EMO、AnimateAnyone）同一时刻仅支持 1 个任务运行

### 输入限制

- [prompt](../guides/prompt.md) 长度：通常不超过 5000 个非中文字符或 2500 个中文字符
- 图像输入支持 URL 和 Base64 编码（部分模型）
- 视频编辑模型耗时可能更长（约 5-10 分钟），详见 [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-wanx-vace-api-reference.md)

### 版本迁移建议

> **注意**：万相 2.7 为最新推荐版本。原 wan2.6 及早期模型的图生视频接口使用旧版协议（`img_url` 字段），新版协议统一使用 `media` 数组。如需了解旧版接口，参见 [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-image-to-video-api-reference.md)。

### 费用

- 各模型按生成视频时长或张数计费，具体单价参见各模型文档中的"资费与限流"部分
- 多数模型提供免费额度供试用

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-video-edit-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/text-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/image-to-video-general-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-animate-move-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-s2v-overview.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-animate-mix-api.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/animateanyone-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/emo-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/liveportrait-quick-start.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/emoji-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/videoretalk.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/video-style-transform-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-reference-to-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-video-generation-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-keyframe-to-video-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-image-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)

