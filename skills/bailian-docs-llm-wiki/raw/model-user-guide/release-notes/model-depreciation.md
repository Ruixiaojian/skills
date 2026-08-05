# 模型下线机制说明

为优化资源利用和确保用户使用最新、最优模型，阿里云百炼平台将根据模型迭代升级情况不定期下线历史模型。本文将为您介绍模型下线机制。

## **通知机制**

### **通知时间**

-   **快照**模型（模型名称带有具体的日期标识，例如qwen-max-2025-01-25，常见于千问系列模型）将在正式**下线前30天**发布下线通知。
    
-   **主线**模型（系列模型的核心版本）将在正式**下线前3个月**发布下线通知。
    

### **通知方式**

通过短信、邮件、站内信、官网公告等方式。

> 短信、邮件、站内信仅面向近3个月有待下线模型调用记录的用户。

## 下线影响

-   **自下线通知发布之日起**，将逐步缩减待下线模型的QPM（每分钟调用次数）和TPM（每分钟消耗Token数）。对于申请过扩容的模型，会先恢复至[默认限流](https://help.aliyun.com/zh/model-studio/rate-limit)数据后再进行缩减。在此过程中，模型API接口、控制台上的相关功能均保持正常使用。
    
-   **自模型正式下线之日起**：
    
    -   **模型推理**：停止支持模型推理服务，已创建的调用该模型的应用和服务将无法返回结果。
        
    -   **模型调优及模型部署**：不再支持基于下线模型进行新的调优和部署操作（部分模型的调优与部署功能可能在模型下线后仍可正常使用，具体请以下线通知为准）。已经训练和部署的模型不受影响。
        
    -   **控制台功能及官方文档**：模型相关的控制台功能（模型广场、模型体验等）、官方文档将同步下线。
        

## 操作建议

1.  前往[模型观测](https://bailian.console.aliyun.com/#/model-telemetry)页面，检查您的账号是否正在使用待下线的模型。
    
2.  如果再使用，建议您先测试替代模型的业务效果，再切换至替代模型。
    

## 下线模型列表

### **2026年10月10日将下线**

详细说明，请参见官网公告[【大模型服务平台百炼】部分老旧模型下线通知](https://www.aliyun.com/notice/118434)。

**类别**

**模型名称**

**下线时间**

**替代模型**

图像生成与编辑

aitryon

2026年10月10日00:00:00

qwen-image-2.0

aitryon-parsing-v1

aitryon-plus

aitryon-refiner

animate-anyone-detect-gen2

emo-detect-v1

emoji-detect-v1

facechain-generation

image-out-painting

liveportrait

liveportrait-detect

qwen-image

qwen-image-edit

qwen-image-edit-max

qwen-image-edit-max-2026-01-16

qwen-image-edit-plus

qwen-image-edit-plus-2025-10-30

qwen-image-edit-plus-2025-12-15

qwen-image-max

qwen-image-max-2025-12-30

qwen-image-plus

qwen-image-plus-2026-01-09

wordart-semantic

wordart-texture

wanx-background-generation-v2

wan2.7-image

视频生成

animate-anyone-gen2

wan2.7-r2v

animate-anyone-template-gen2

emo-v1

emoji-v1

千问Plus

qwen-plus-0112

qwen3.7-plus

qwen-plus-1220

qwen-plus-2025-07-28

qwen-plus-2025-09-11

qwen-plus-2025-12-01-us

qwen3.7-plus-us

qwen-plus-us

千问Flash

qwen-flash-2025-07-28-us

qwen3.6-flash-us

qwen-flash-us

千问Long

qwen-long-2025-01-25

qwen3.7-plus

qwen-long-latest

千问Math

qwen-math-plus

qwen3.7-plus

qwen-math-plus-0816

qwen-math-plus-0919

qwen-math-plus-latest

千问VL OCR

qwen-vl-ocr

qwen3.7-plus

qwen-vl-ocr-1028

qwen-vl-ocr-2025-04-13

qwen-vl-ocr-2025-08-28

qwen-vl-ocr-latest

千问VL

qwen3-vl-plus-2025-09-23

qwen3.7-plus

qwen3-vl-plus-2025-12-19

qwen3-vl-flash-2025-10-15-us

qwen3.6-flash-us

qwen3-vl-flash-2026-01-22-us

qwen3-vl-flash-us

千问Omni

qwen-omni-turbo

qwen3.5-omni-plus

qwen-omni-turbo-2025-01-19

qwen-omni-turbo-2025-03-26

qwen-omni-turbo-latest

qwen2.5-omni-7b

qwen3-omni-30b-a3b-captioner

qwen3-omni-flash-2025-09-15

qwen3-omni-flash-2025-12-01

qwen-omni-turbo-realtime

qwen3.5-omni-plus-realtime

qwen-omni-turbo-realtime-2025-05-08

qwen-omni-turbo-realtime-latest

qwen3-omni-flash-realtime

qwen3-omni-flash-realtime-2025-12-01

千问翻译

qwen-mt-turbo

qwen-mt-flash

qwen-mt-lite-us

qwen3.6-flash-us

语音合成

cosyvoice-clone-v1

voice-enrollment

cosyvoice-v1

cosyvoice-v3.5-plus

cosyvoice-v3

千问TTS

qwen3-tts-flash-2025-09-18

cosyvoice-v3.5-plus

qwen3-tts-flash-2025-11-27

qwen3-tts-instruct-flash

qwen3-tts-instruct-flash-2026-01-26

qwen3-tts-vc-2026-01-22

qwen3-tts-vd-2026-01-26

qwen3-tts-flash-realtime-2025-09-18

qwen3.5-omni-plus-realtime

qwen3-tts-flash-realtime-2025-11-27

qwen3-tts-instruct-flash-realtime

qwen3-tts-instruct-flash-realtime-2026-01-22

qwen3-tts-vc-realtime-2025-11-27

qwen3-tts-vc-realtime-2026-01-15

qwen3-tts-vd-realtime-2025-12-16

qwen3-tts-vd-realtime-2026-01-15

语音识别

fun-asr-2025-08-25

fun-asr

fun-asr-2025-11-07

fun-asr-mtl

fun-asr-mtl-2025-08-25

sensevoice-v1

qwen3-asr-flash-2025-09-08

qwen3-asr-flash-2026-02-10

qwen3-asr-flash-filetrans-2025-11-17

fun-asr-mtl-realtime

fun-asr-realtime

fun-asr-realtime-2025-09-15

fun-asr-realtime-2025-11-07

qwen3-asr-flash-realtime-2025-10-27

qwen3-asr-flash-realtime-2026-02-10

语音翻译

qwen3-livetranslate-flash-realtime

qwen3.5-livetranslate-flash-realtime

qwen3-livetranslate-flash-realtime-2025-09-22

第三方模型

glm-4.5

glm-5.2

glm-4.5-air

其他

codeqwen1.5-7b-chat

qwen3.7-plus

nlp-rag-rewrite-one

farui-plus

法睿应用

### **2026年10月10日将下线**

详细说明，请参见官网公告[【大模型服务平台百炼】部分主线模型下线通知](https://www.aliyun.com/notice/118344)。

**类别**

**模型名称**

**下线时间**

**替代模型**

千问Max

qwen3.6-max-preview

2026年10月10日00:00:00

qwen3.7-max

qwen3-max-preview

qwen3-max

千问VL

qwen3-vl-flash

qwen3.6-flash

千问Coder

qwen3-coder-plus

qwen3.7-plus

### **2026年10月10日将下线**

详细说明，请参见官网公告[【大模型服务平台百炼】部分语音系列历史主线模型下线通知](https://www.aliyun.com/notice/118331)。

**类别**

**模型名称**

**下线时间**

**替代模型**

语音合成

qwen-tts

2026年10月10日00:00:00

cosyvoice-v3-flash

qwen-tts-realtime

声音复刻

qwen-voice-enrollment

voice-enrollment

音色设计

qwen-voice-design

cosyvoice-v3.5-flash

语音翻译

gummy-chat-v1

无直接替代模型

gummy-realtime-v1

语音识别

paraformer-realtime-v1

paraformer-realtime-v2

paraformer-realtime-8k-v1

paraformer-realtime-8k-v2

paraformer-v1

paraformer-v2

paraformer-8k-v1

paraformer-8k-v2

paraformer-mtl-v1

paraformer-v2

### **2026年10月10日将下线**

详细说明，请参见官网公告[【大模型服务平台百炼】部分历史主线模型下线通知](https://www.aliyun.com/notice/118177)。

**类别**

**模型名称**

**下线时间**

**替代模型**

千问Turbo

qwen-turbo

2026年10月10日00:00:00

Qwen3.7/3.6 系列最新模型

qwen-turbo-realtime

千问VL

qwen-vl-max

qwen-vl-plus

QwQ

qwq-plus

QVQ

qvq-max

qvq-plus

千问Math

qwen-math-turbo

千问Coder

qwen-coder-turbo

qwen-coder-plus

### **2026年10月10日将下线**

详细说明，请参见官网公告[【大模型服务平台百炼】部分历史快照模型下线通知](https://www.aliyun.com/notice/118345)。

**类别**

**模型名称**

**下线时间**

**替代模型**

千问Max

qwen3-max-2026-01-23

2026年10月10日00:00:00

qwen3.7-max

qwen3-max-2025-09-23

千问VL

qwen3-vl-8b-instruct

qwen3.6-flash

qwen3-vl-8b-thinking

qwen3-vl-flash-2026-01-22

qwen3-vl-flash-2025-10-15

qwen3-vl-30b-a3b-instruct

qwen3.7-plus

qwen3-vl-30b-a3b-thinking

qwen3-vl-32b-instruct

qwen3-vl-32b-thinking

qwen3-vl-235b-a22b-thinking

千问Coder

qwen3-coder-next

qwen3.7-plus

qwen3-coder-30b-a3b-instruct

qwen3-coder-plus-2025-09-23

qwen3-coder-plus-2025-07-22

qwen3-coder-480b-a35b-instruct

千问3开源版

qwen3-8b

qwen3.6-flash

qwen3-14b

qwen3-30b-a3b

qwen3.7-plus

qwen3-30b-a3b-instruct-2507

qwen3-30b-a3b-thinking-2507

qwen3-32b

qwen3-235b-a22b

qwen3-vl-235b-a22b-instruct

qwen3-235b-a22b-instruct-2507

qwen3-235b-a22b-thinking-2507

qwen3-next-80b-a3b-instruct

qwen3-next-80b-a3b-thinking

第三方模型

deepseek-r1-distill-qwen-7b

qwen3.7-plus

deepseek-r1-distill-qwen-14b

deepseek-r1-distill-qwen-32b

deepseek-v3

deepseek-v3.1

deepseek-v3.2

deepseek-v3.2-exp

deepseek-r1

deepseek-r1-0528

MiniMax-M2.1

glm-4.7

glm-4.6

Moonshot-Kimi-K2-Instruct

kimi-k2-thinking

### **2026年10月10日将下线**

详细说明，请参见官网公告[【大模型服务平台百炼】部分语音系列历史快照模型下线通知](https://www.aliyun.com/notice/118332)。

**类别**

**模型名称**

**下线时间**

**替代模型**

语音合成

qwen-tts-latest

2026年10月10日00:00:00

cosyvoice-v3-flash

qwen-tts-2025-05-22

qwen-tts-2025-04-10

qwen-tts-realtime-latest

qwen-tts-realtime-2025-07-15

### **2026年5月30日已下线**

详细说明，请参见官网公告[GTE-RERANK模型下线通知](https://www.aliyun.com/notice/118217)。

**类别**

**模型名称**

**下线时间**

**替代模型**

重排序

gte-rerank

2026年5月30日00:00:00

qwen3-rerank

### **2026年5月13日已下线**

详细说明，请参见官网公告[部分历史快照模型下线通知](https://www.aliyun.com/notice/118178)。

**类别**

**模型名称**

**下线时间**

**替代模型**

千问Max快照

qwen-max-latest

2026年5月13日00:00:00

Qwen3.6系列最新模型

qwen-max-2025-01-25

qwen-max-0919

qwen-max-0428

千问Turbo快照

qwen-turbo-latest

qwen-turbo-2025-07-15

qwen-turbo-2025-04-28

qwen-turbo-2025-02-11

qwen-turbo-2024-11-01

qwen-turbo-1101

千问VL-Max快照

qwen-vl-max-latest

qwen-vl-max-2025-08-13

qwen-vl-max-2025-04-08

qwen-vl-max-2025-04-02

qwen-vl-max-2025-01-25

qwen-vl-max-1230

qwen-vl-max-1119

千问VL-Plus快照

qwen-vl-plus-latest

qwen-vl-plus-2025-08-15

qwen-vl-plus-2025-07-10

qwen-vl-plus-2025-05-07

qwen-vl-plus-2025-01-25

qwen-vl-plus-0102

QwQ-Plus快照

qwq-plus-latest

qwq-plus-2025-03-05

QVQ-Max快照

qvq-max-latest

qvq-max-2025-05-15

qvq-max-2025-03-25

QVQ-Plus快照

qvq-plus-latest

qvq-plus-2025-05-15

千问Math-Turbo快照

qwen-math-turbo-latest

qwen-math-turbo-0919

千问Coder-Turbo快照

qwen-coder-turbo-latest

qwen-coder-turbo-0919

千问Coder-Plus快照

qwen-coder-plus-latest

qwen-coder-plus-2024-11-06

开源系列快照

qwq-32b

qwq-32b-preview

qvq-72b-preview

qwen2.5-vl-32b-instruct

qwen2.5-vl-72b-instruct

qwen2.5-vl-7b-instruct

qwen2.5-vl-3b-instruct

qwen2.5-7b-instruct-1m

qwen2.5-14b-instruct-1m

qwen2.5-72b-instruct

qwen2.5-32b-instruct

qwen2.5-14b-instruct

qwen2.5-math-72b-instruct

qwen2.5-math-7b-instruct

qwen2.5-coder-1.5b-instruct

qwen2.5-coder-0.5b-instruct

qwen2.5-coder-14b-instruct

qwen2.5-coder-32b-instruct

qwen2.5-coder-3b-instruct

qwen2.5-coder-7b-instruct

qwen2.5-math-1.5b-instruct

qwen2.5-3b-instruct

qwen2.5-1.5b-instruct

qwen2.5-0.5b-instruct

qwen2.5-7b-instruct

qwen3-0.6b

qwen3-1.7b

qwen3-4b

### **2026年3月30日已下线**

**类别**

**模型名称**

**下线时间**

**替代模型**

千问Audio

qwen-audio-asr

2026年3月30日00:00:00

qwen3-asr-flash

qwen-audio-asr-latest

qwen-audio-chat

qwen3-omni-flash

qwen2-audio-instruct

千问2-开源版

qwen2-57b-a14b-instruct

qwen3-235b-a22b

qwen2-72b-instruct

qwen2-7b-instruct

qwen2-1.5b-instruct

qwen2-0.5b-instruct

千问1.5

qwen1.5-110b-chat

qwen3-235b-a22b

qwen1.5-72b-chat

qwen1.5-32b-chat

qwen1.5-14b-chat

qwen1.5-7b-chat

qwen1.5-1.8b-chat

qwen1.5-0.5b-chat

千问Math

qwen2.5-math-1.5b-instruct

qwen-math-plus

千问Coder

qwen2.5-coder-3b-instruct

qwen-coder-plus

qwen2.5-coder-1.5b-instruct

qwen2.5-coder-0.5b-instruct

千问VL

qwen2-vl-72b-instruct

qwen3.5-flash

qwen2-vl-7b-instruct

qwen2-vl-2b-instruct

qwen-vl-v1

qwen-vl-chat-v1

第三方模型

baichuan2-turbo

qwen-flash

abab6.5s-chat

abab6.5g-chat

abab6.5t-chat

NLU

opennlu-v1

qwen3.5-flash

图像生成

stable-diffusion-v1.5

qwen-image-plus、z-image-turbo、wan2.6-t2i

stable-diffusion-xl

stable-diffusion-3.5-large

stable-diffusion-3.5-large-turbo

flux-dev

flux-merged

flux-schnell

Llama 4

llama-4-scout-17b-16e-instruct

qwen3.5-flash

llama-4-maverick-17b-128e-instruct

### **2026年1月30日已下线**

详细说明，请参见官网公告[大模型服务平台百炼部分历史快照模型下线通知](https://www.aliyun.com/notice/117814)。

**类别**

**模型名称**

**下线时间**

**替代模型**

千问Max

qwen-max-2024-04-03

2026年1月30日00:00:00

qwen-max-2025-01-25

千问Plus

qwen-plus-2024-11-27

qwen-plus-2025-12-01

qwen-plus-2024-11-25

qwen-plus-2024-09-19

qwen-plus-2024-08-06

qwen-plus-2024-07-23

千问Turbo

qwen-turbo-2024-09-19

qwen-flash-2025-07-28

qwen-turbo-2024-06-24

千问VL

qwen-vl-max-2024-10-30

qwen3-vl-plus-2025-12-19

qwen-vl-max-2024-08-09

qwen-vl-plus-2024-08-09

qwen3-vl-flash-2025-10-15

千问Audio

qwen-audio-turbo-2024-12-04

qwen3-asr-flash

qwen-audio-turbo-2024-08-07

qwen-audio-asr-2024-12-04

### **2025年7月30日已下线**

详细说明，请参见官网公告[【大模型服务平台百炼】历史模型下线通知](https://www.aliyun.com/notice/117351)。

**类别**

**模型名称**

**下线时间**

**替代模型**

千问VL快照版

qwen-vl-plus-2023-12-01

2025年7月30日00:00:00

qwen-vl-plus

零一万物

yi-large

qwen-max、qwen-plus、qwen-flash等

yi-medium

yi-large-rag

yi-large-turbo

Dolly

dolly-12b-v2

### **2025年7月2日已下线**

详细说明，请参见官网公告[大模型服务平台阿里云百炼部分历史模型下线通知](https://www.aliyun.com/notice/117140?spm=5176.29512420.J_JASdJ65l9Zg8lf6Fc9UC_.1.671f19d51H9SI9)。

**类别**

**模型名称**

**下线时间**

**替代模型**

Llama-仅文本输入

llama3.3-70b-instruct

2025年7月2日00:00:00

qwen-max、qwen-plus、qwen-flash等

llama3.2-3b-instruct

llama3.2-1b-instruct

llama3.1-405b-instruct

llama3.1-70b-instruct

llama3.1-8b-instruct

llama3-70b-instruct

llama3-8b-instruct

llama2-13b-chat-v2

llama2-7b-chat-v2

Llama-文本和图像输入

llama3.2-90b-vision-instruct

llama3.2-11b-vision

百川-开源版

baichuan2-13b-chat-v1

baichuan2-7b-chat-v1

baichuan-7b-v1

ChatGLM

chatglm3-6b

chatglm-6b-v2

姜子牙

ziya-llama-13b-v1

BELLE

belle-llama-13b-2m-v1

元语

chatyuan-large-v2

BiLLa

billa-7b-sft-v1

动漫人物生成

wanx-style-cosplay-v1

无直接替代模型

图配文

wanx-ast

创意文字生成-WordArt锦书

wordart-surnames

AnyText图文融合

wanx-anytext-v1

### **2025年5月8日已下线**

详细说明，请参见官网公告[大模型服务平台阿里云百炼部分历史快照模型下线通知](https://www.aliyun.com/notice/117139?spm=5176.29512420.J_JASdJ65l9Zg8lf6Fc9UC_.4.657b19d5uj1jXt)。

**类别**

**模型名称**

**下线时间**

替代模型

文本生成-千问

qwen-max-2024-01-07

> 又称qwen-max-0107

2025年5月8日00:00:00

qwen-max

qwen-plus-2024-06-24

> 又称qwen-plus-0624

qwen-plus

qwen-plus-2024-02-06

> 又称qwen-plus-0206

qwen-turbo-2024-02-06

> 又称qwen-turbo-0206

qwen-turbo

qwen-vl-max-2024-02-01

> 又称qwen-vl-max-0201

qwen-vl-max

文本生成-千问-开源版

qwen-72b-chat

qwen2.5-72b-instruct

qwen-14b-chat

qwen2.5-14b-instruct

qwen-7b-chat

qwen2.5-7b-instruct

qwen-1.8b-chat

qwen2.5-1.5b-instruct

qwen-1.8b-longcontext-chat

qwen2.5-1.5b-instruct

qwen2-math-72b-instruct

qwen2.5-math-72b-instruct

qwen2-math-7b-instruct

qwen2.5-math-7b-instruct

qwen2-math-1.5b-instruct

qwen2.5-math-1.5b-instruct

幻影人像Motionshop视频生成模型

motionshop-video-detect

可使用animate-anyone-gen2的“按视频背景生成”功能，达到近似效果

motionshop-gen3d

motionshop-synthesis

### **2024年4月22日已下线**

**类别**

**模型名称**

**下线时间**

替代模型

文本生成-千问

qwen-max-1201

2024年4月22日00:00:00

qwen-max
