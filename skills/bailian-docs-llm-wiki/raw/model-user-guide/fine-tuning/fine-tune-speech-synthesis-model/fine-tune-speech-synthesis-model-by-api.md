# CosyVoice模型调优

本文档介绍如何对阿里云百炼提供的 CosyVoice 语音合成模型进行 SFT（`efficient_sft`）调优。**当前调优任务仅支持通过 API（HTTP）方式发起，控制台暂不支持。**

## **适用范围**

-   **支持微调的方式**：SFT 高效微调（`efficient_sft`），暂不支持 CPT、DPO 等其他训练方式。
    
-   **支持微调的模型**：`cosyvoice-v3-flash`。
    
-   **支持的服务部署范围与地域**：CosyVoice 模型调优仅对服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)的情况可用，且仅支持**华北2（北京）**地域。
    

**说明**

**以下场景不属于本 API 的能力范围，请使用对应的独立功能**：声音复刻、声音设计等生成专属音色的需求，请使用阿里云百炼平台对应的 [声音复刻](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide)/ [声音设计](https://help.aliyun.com/zh/model-studio/voice-design-user-guide) 功能，不要通过本调优 API 实现。

## **前提条件**

-   已经完整阅读了[模型调优简介](https://help.aliyun.com/zh/model-studio/model-training-overview)，了解模型调优的基本概念、流程及数据格式要求。
    
-   已开通服务并获得 API-KEY，请参考[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    
-   [阿里云子账号](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)）需被授予必要的调用、训练和部署[权限](https://help.aliyun.com/zh/model-studio/use-workspace#895b613347th4)。
    

## **操作流程**

通过 API 调优 CosyVoice 模型的完整流程如下：

1.  **准备调优数据集**：按指定目录结构准备训练音频（`.wav`）与样本文件（`data.jsonl`），打包为 `.zip`。
    
2.  **上传调优文件**：将 `.zip` 上传到百炼，获取文件 ID（`file_id`）。
    
3.  **创建调优任务**：基于 `file_id` 启动训练，获取任务 ID（`job_id`）与调优后模型 ID（`finetuned_output`）。
    
4.  **查询任务状态与日志**：等待训练完成（状态变为 `SUCCEEDED`），如需排查可拉取训练日志。
    
5.  **部署并调用调优后的模型**：将调优成功的模型 ID 部署为可调用的服务，然后像调用基础模型一样使用它。
    

**一次跑通的量级参考**：以下为一次实操样本数据，便于你在开工前对耗时与费用建立预期，**实际数值随数据量、超参与队列等待时间不同而变化**。

**项目**

**实测值**

训练样本量

99 条音频（数据集压缩包约 37 MB）

超参取值

`lm_max_epoch=4 / lm_step=1 / lm_num=2 / lm_batch_size=1000`；`fm_max_epoch=4 / fm_step=2 / fm_num=2 / fm_batch_size=2000`

训练总耗时

约 37 分钟（从 `PENDING` 进入 `SUCCEEDED`）

消耗 Token 数

约 99,406 Tokens

费用估算

约 19.88 元（按 0.2 元 / 千 Tokens 计）

## **准备调优数据集**

### **音频规格要求**

为保证调优效果，训练音频需满足以下规格要求：

**规格项**

**要求**

音频格式

`.wav`

采样率

不低于 16 kHz。

单条音频时长

推荐 2 秒 ~ 30 秒；最低不少于 1 秒。

语种

按训练目标音色的目标语种准备，无固定限制。

文本语种

`data.jsonl` 中 `text` 字段的语种必须与对应音频的语种保持一致。

### **目录结构**

将训练样本组织为以下目录结构，并将整个目录打包为 `.zip` 压缩包后上传：

```
user_data/
├── data.jsonl           # 训练样本列表（必需）
└── train/               # 训练音频目录（所有训练 wav 放在这里）
    ├── 100001.wav
    ├── 100002.wav
    └── ...
```

### **data.jsonl 格式**

`data.jsonl` 文件每行一个训练样本：

```
{"wav_fn": "train/100001.wav", "text": "你好。"}
{"wav_fn": "train/100002.wav", "text": "我明白了。"}
```

**字段说明**

**字段**

**必填**

**说明**

`wav_fn`

是

音频文件名，系统自动拼接为 `{data_dir}/train/{wav_fn}`。

`text`

是

对应的文本。当前版本必填，ASR 自动补齐功能未开放。

**文本写法建议**：

-   **无需归一化**：数字、英文 / 中文混排、标点符号等无需做特殊归一化处理，按音频中的自然念法书写即可。
    
-   **去除特殊符号**：建议提前去除文本中不发音的特殊符号（如 emoji、装饰符号、控制字符等），仅保留与音频实际发音对应的内容。
    

### **数据量建议**

CosyVoice 模型调优对数据量的建议如下：

-   **推荐数据量**：训练音频总时长在 **1~10 小时** 之间即可获得较好效果，超过 10 小时收益不明显。
    
-   **样本条数**：建议训练音频不少于 **150 条**，以保证调优效果稳定；算法侧与平台侧对 `data.jsonl` 内的样本条数均无明确上限，可按总时长目标自由组织。
    

**说明**

训练数据总时长直接影响 Token 消耗与训练时长，请在准备数据前结合预算评估，详见[计费说明](#cv-billing-title)。

## **上传调优文件**

将打包好的 `train_data.zip` 通过 multipart/form-data 上传到阿里云百炼平台。关键字段：`files`（本地 zip 路径）、`purpose`（固定填 `fine-tune`）、`descriptions`（可选）。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/files' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--form 'files=@"train_data.zip"' \
--form 'purpose="fine-tune"' \
--form 'descriptions="训练语音包"'
```

> Windows CMD 请将 `${DASHSCOPE_API_KEY}` 替换为 `%DASHSCOPE_API_KEY%`，PowerShell 请替换为 `$env:DASHSCOPE_API_KEY`。

**说明**

请保存响应中的 `file_id`，这是上传数据集的唯一标识，下一步创建调优任务时需要使用。完整请求/响应字段说明请参见 [上传文件](https://help.aliyun.com/zh/model-studio/model-customization-file-management-service#d031ae7105c1g)。

## **创建调优任务**

使用上一步获取的 `file_id` 启动训练任务。

> Windows CMD 请将 `${DASHSCOPE_API_KEY}` 替换为 `%DASHSCOPE_API_KEY%`，PowerShell 请替换为 `$env:DASHSCOPE_API_KEY`。

**请求示例**

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json' \
--data '{
    "model": "cosyvoice-v3-flash",
    "training_file_ids": [
        "<替换为训练数据集的file_id>"
    ],
    "hyper_parameters": {
        "lm_max_epoch": 4,
        "lm_step": 1,
        "lm_num": 2,
        "fm_max_epoch": 4,
        "fm_step": 2,
        "fm_num": 2,
        "lm_batch_size": 1000,
        "fm_batch_size": 2000
    },
    "training_type": "efficient_sft"
}'
```

关键请求字段：`model` 固定为 `cosyvoice-v3-flash`，`training_type` 固定为 `efficient_sft`，`training_file_ids` 仅支持挂载一个训练文件 ID，`hyper_parameters` 内 8 个 LM / FM 子字段全部必填。每个字段的取值范围、类型、传参方式请参见 [模型调优 API 参考](https://help.aliyun.com/zh/model-studio/model-training-api-reference)。

### **如何设置超参数**

CosyVoice 调优涉及两个子网络：**LM**（Language Model，将文本转为离散语音 token 的自回归语言模型）与 **FM**（Flow Matching，将语音 token 还原为 Mel 谱的流匹配模型）。两者的训练超参分别以 `lm_*` 与 `fm_*` 前缀区分。

超参数决定训练轮次与 Checkpoint 保存策略，会直接影响调优耗时、Token 消耗与最终模型效果。

> **建议先用以下推荐值跑通一次完整流程，根据效果再决定是否调整：**

-   **LM 网络**：`lm_max_epoch=60`，`lm_step=5`，`lm_num=3`，`lm_batch_size=1000`。
    
-   **FM 网络**：`fm_max_epoch=100`，`fm_step=10`，`fm_num=3`，`fm_batch_size=2000`。
    

其中 `*_max_epoch` 为训练总轮次，`*_step` 为保存 Checkpoint 的步长，`*_num` 为最多保留的 Checkpoint 个数，`*_batch_size` 为训练批次大小。各字段的完整取值范围请参见 [模型调优 API 参考](https://help.aliyun.com/zh/model-studio/model-training-api-reference)。

**说明**

提高训练轮次会增加 Token 消耗与训练时长。调整前请先评估业务预算与数据量级（参见上方 [数据集大小建议](#cv-dataset-size-title)）。

### **模型产出（Checkpoint）说明**

单次调优任务可能产出多个 Checkpoint（候选模型），具体数量与排序由超参数中的 `lm_num`、`fm_num` 与 `*_step` 共同决定。

1.  **选模型**：分别从 LM、FM 的最大轮次往回数，每隔 `*_step` 选一个，共选 `*_num` 个。
    
2.  **组合**：LM 与 FM 的选择做全排列，候选 Checkpoint 数量 = `lm_num × fm_num`。
    
3.  **排序**：按 `LM 轮次 × FM 轮次` 从大到小排序（乘积越大代表双端训练越充分，越靠前）。
    
4.  **截断**：在上一步**降序排序**结果上从前往后截取，最多保留 **10** 个；候选不足 10 个时全部输出。
    
5.  **命名**：`checkpoint-{LM 轮次 4 位补零}{FM 轮次 4 位补零}`，例如 LM 4 / FM 4 输出为 `checkpoint-00040004`。
    

**示例**：以参数 `lm_max_epoch=4, lm_step=1, lm_num=2, fm_max_epoch=4, fm_step=2, fm_num=2` 为例：

-   LM 选出：4、3（从 4 开始，每次减 `lm_step=1`，共 `lm_num=2` 个）。
    
-   FM 选出：4、2（从 4 开始，每次减 `fm_step=2`，共 `fm_num=2` 个）。
    
-   全排列得到 4 个候选，按乘积降序输出：
    

**排序**

**LM / FM 轮次**

**乘积**

**Checkpoint 名称**

1

LM 4 / FM 4

16

`checkpoint-00040004`

2

LM 3 / FM 4

12

`checkpoint-00030004`

3

LM 4 / FM 2

8

`checkpoint-00040002`

4

LM 3 / FM 2

6

`checkpoint-00030002`

**说明**

响应中的 `finetuned_output` 始终对应排序最靠前（即乘积最大）的 Checkpoint。

### **响应结果**

请求成功后，请保存响应中的两个关键字段：`output.job_id`（任务 ID，用于后续查询状态、获取日志、取消或删除任务）与 `output.finetuned_output`（调优完成后的模型 ID，用于后续调用）。任务创建后 `status` 初始为 `PENDING`，将随训练进度变化。响应字段的完整说明请参见 [模型调优 API 参考](https://help.aliyun.com/zh/model-studio/model-training-api-reference)。

## **查询任务状态与日志**

创建调优任务后，整个训练过程会持续较长时间。可使用以下两个接口跟踪进度：通过**查询任务详情**掌握当前所处阶段，通过**获取训练日志**排查异常或确认训练进展。

### **查询任务详情**

使用创建任务时返回的 `job_id` 查询任务状态。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json'
```

响应中 `output.status` 字段表示当前阶段：`PENDING`（待开始）→ `QUEUING`（排队中，平台同一时刻仅运行一个训练任务）→ `RUNNING`（训练进行中）→ `SUCCEEDED`（训练成功）。异常终止状态包括 `FAILED`（训练失败）、`CANCELING`（取消中）与 `CANCELED`（已取消）。状态字段的完整定义请参见[模型调优 API 参考](https://help.aliyun.com/zh/model-studio/model-training-api-reference)。

### **获取训练日志**

当任务长时间停留在某一状态、或进入 `FAILED` 状态时，可拉取训练日志辅助排查。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>/logs?offset=0&line=1000' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json'
```

> 通过 `offset` 控制起始位置，`line` 控制最多返回的行数（示例每次拉取 1000 行）。响应字段说明请参见[模型调优 API 参考](https://help.aliyun.com/zh/model-studio/model-training-api-reference)。

## **模型部署&调用**

当任务状态进入 `SUCCEEDED` 时，从查询接口响应中记录下 `finetuned_output` 字段的值——这是**调优后模型的唯一 ID**，对应[模型产出](#cv-create-ckpt-title)中排序最靠前的 Checkpoint。需要先将该模型 ID 部署为可调用的服务，才能在业务中使用。

### **模型部署**

CosyVoice 调优模型仅支持**按模型单元的使用时长**（`"plan": "mu"`）计费方式部署。当前提供以下两种部署方式，**推荐使用控制台部署**：

**部署规格**：CosyVoice 调优模型当前仅支持 **MU5** 规格（MU，Model Unit，是百炼平台的算力部署最小单位）。

API 请求中的 `capacity` 字段表示**部署副本数**，对应控制台部署页面的**部署副本数**选项，与副本数一一对应（`"capacity": 1` 部署 1 个副本，`"capacity": N` 部署 N 个副本，可填 ≥ 1 的整数）。副本越多，可承载的并发吞吐越高，费用也按副本数线性增长。

`capacity` 字段的完整取值约束请参见[模型部署-API详情](https://help.aliyun.com/zh/model-studio/model-deployment-api)；MU5 的小时单价 / 包月单价请参见[模型部署简介](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)。

-   **方式一：在阿里云百炼控制台部署（推荐）**
    
    前往[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/efm/model_center)的**我的模型**页面，按界面提示选择部署方式、模型规格与部署单元数，提交后即可在页面查看部署状态和部署成功后的模型实例 ID。控制台部署的详细操作请参见[模型部署简介](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)。
    
-   **方式二：通过 API 部署**
    
    将调优任务成功后的模型 ID（响应中的 `finetuned_output` 字段值）作为 `model_name`，调用部署接口。下方示例使用规格 MU5（对应 `deploy_spec="dps-20260521172224-1vabse"`，`capacity` 为 1 的整数倍）：
    
    ```
    curl --location 'https://dashscope.aliyuncs.com/api/v1/deployments' \
    --header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
    --header 'Content-Type: application/json' \
    --data '{
        "model_name": "<替换为调优任务返回的 finetuned_output 字段值>",
        "plan": "mu",
        "deploy_spec": "dps-20260521172224-1vabse",
        "capacity": 1,
        "billing_method": "POST_PAY"
    }'
    ```
    
    部署请求提交成功后，响应中 `output.deployed_model` 即为部署实例 ID，**后续调用模型时需将其作为** `**model**` **参数传入**。可用部署规格的获取方式与各字段的取值约束请参见[模型部署-API详情](https://help.aliyun.com/zh/model-studio/model-deployment-api)。
    
    部署任务创建后将经历 `PENDING` → `DEPLOYING` → `RUNNING` 多个阶段，可通过以下接口查询当前部署状态：
    
    ```
    curl --location 'https://dashscope.aliyuncs.com/api/v1/deployments/<替换为 deployed_model 字段值>' \
    --header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
    --header 'Content-Type: application/json'
    ```
    
    当响应中 `status` 字段值为 `RUNNING` 时，表示该模型已可供调用。更多模型部署相关的操作（如扩缩容、下线等）请参见[模型部署-API详情](https://help.aliyun.com/zh/model-studio/model-deployment-api)。
    

### **模型调用**

当模型部署状态为 `RUNNING` 时，调优后的模型即可投入业务调用。调用方式（含 endpoint、请求体字段、典型响应与音频取回方式）与其他 CosyVoice 模型一致，完整说明请参见用户指南 [语音合成](https://help.aliyun.com/zh/model-studio/tts-model/)。相比原模型，**仅需调整以下两个请求参数**：

-   `model`：设置为部署任务成功后的实例 ID，即部署响应中 `output.deployed_model` 字段的值。
    
-   `voice`：必须固定为 `"default"`。
    

**重要**

调优后的模型只承载训练数据所对应的**专属音色**。调用时 `voice` 参数必须固定为 `"default"`（即代表该专属音色）；若传入预置音色名或音色复刻 ID，请求将失败。

完整调用示例如下，根据业务场景选择**非实时（HTTP）**或**实时（WebSocket）**方式：

## **非实时（HTTP）**

单次合成完整文本，响应中包含合成音频的 URL，有效期为 24 小时。

```
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "<替换为部署响应中的 deployed_model 字段值>",
    "input": {
      "text": "我家的后面有一个很大的花园。",
      "voice": "default",
      "format": "wav",
      "sample_rate": 24000
    }
}'
```

## **实时（Python WebSocket）**

通过 DashScope Python SDK 建立 WebSocket 流式合成连接，依赖 `dashscope` 包。

```
# coding=utf-8
import os
import dashscope
from dashscope.audio.tts_v2 import *

dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')
dashscope.base_websocket_api_url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference'

# 模型 ID 替换为部署响应中的 deployed_model 字段值；voice 必须固定为 "default"
model = "<替换为部署响应中的 deployed_model 字段值>"
voice = "default"

# 实例化 SpeechSynthesizer，并传入模型（model）与音色（voice）
synthesizer = SpeechSynthesizer(model=model, voice=voice)
# 发送待合成文本，获取二进制音频
audio = synthesizer.call("我家的后面有一个很大的花园。")
# 打印 requestId 与首包延迟
print('[Metric] requestId 为：{}，首包延迟为：{} 毫秒'.format(
    synthesizer.get_last_request_id(),
    synthesizer.get_first_package_delay()))

# 将音频保存至本地
with open('output.mp3', 'wb') as f:
    f.write(audio)
```

## **API 参考**

[模型调优 API 参考](https://help.aliyun.com/zh/model-studio/model-training-api-reference)。

## **计费说明**

CosyVoice 模型调优涉及两部分费用：**训练费用**（按训练消耗的 Token 数）与**部署费用**（调优后模型部署，按模型单元的使用时长）。

### **训练费用**

按训练消耗的 Token 数计费，单价为 **0.2 元 / 千 Tokens**。

单次调优任务消耗的 Token 数可按下式估算：

消耗 Tokens\=(lm\_max\_epoch+fm\_max\_epoch)×25×训练集总时长(秒)

其中 `lm_max_epoch` 与 `fm_max_epoch` 为[超参数](#cv-create-hp-title)中设置的 LM 与 FM 训练轮次；训练集总时长为[调优数据集](#cv-dataset-title)中全部音频文件的总秒数。

**说明**

提高 `lm_max_epoch` 或 `fm_max_epoch`、扩大训练集均会线性增加 Token 消耗。请在提交任务前结合预算评估。

### **部署费用**

调优后的模型部署后按**使用时长**计费，CosyVoice 调优模型当前仅支持 **MU5** 规格，计费规则、单价与计费起止时刻请参见[模型部署简介](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)。
