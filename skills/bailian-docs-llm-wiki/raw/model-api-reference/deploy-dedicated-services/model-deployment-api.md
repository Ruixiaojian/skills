# 模型部署API参考

本文档以通义千问模型的部署为例进行说明，使用 API（HTTP）调用方式帮助您使用阿里云百炼提供的模型部署功能。

## 前提条件

-   您已经阅读了[模型部署简介](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)和[使用 API 进行模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-quick-start)的相关内容，掌握了模型部署 API 的使用方法，并熟悉了在阿里云百炼平台上进行模型部署的基本步骤。
    
-   已配置百炼的 API-KEY， 请参考[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    

## 获取可以部署的模型列表

### **地址**

```
GET https://dashscope.aliyuncs.com/api/v1/deployments/models
```

### **请求示例**

通过下面的命令可以查询支持部署的模型，推荐使用`version=v1.0`获取包含部署方案和模板信息的完整响应。

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments/models?page_no=1&page_size=100&version=v1.0&model_source=base" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

查询用户微调模型：

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments/models?page_no=1&page_size=100&version=v1.0&model_source=custom" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

### **请求参数**

**参数**

**类型**

**传参方式**

**必选**

**说明**

page\_no

Number

query

否

页码，默认值为1。

page\_size

Number

query

否

页大小，默认为50，最大值为100，最小值为1。

model\_source

String

query

否

模型来源。`base`表示系统模型（默认），`custom`表示用户微调模型。

version

String

query

否

API 版本，推荐使用`v1.0`。使用`v1.0`时，响应中将包含完整的部署方案和模板信息。

### **响应示例**

命令执行完成后，获得以下结果：

```
{
    "request_id": "f7da015c-ea90-4d96-af89-2f8d7604026a",
    "output": {
        "page_no": 1,
        "page_size": 100,
        "total": 5,
        "models": [
            {
                "model_name": "qwen3-8b",
                "plans": [
                    {
                        "plan": "mu",
                        "templates": [
                            {
                                "template_id": "MU1",
                                "template_name": "单机部署-标准推理型",
                                "template_type": "COUPLED",
                                "template_version": "v1",
                                "template_desc": "适用于标准推理场景",
                                "roles": {
                                    "unified": {
                                        "model_unit_spec": "MU1",
                                        "capacity_unit_per_instance": 4
                                    }
                                }
                            },
                            {
                                "template_id": "MU1-PD",
                                "template_name": "PD分离部署-标准推理型",
                                "template_type": "SEPERATED",
                                "template_version": "v1",
                                "template_desc": "适用于PD分离推理场景",
                                "roles": {
                                    "prefill": {
                                        "model_unit_spec": "MU1",
                                        "capacity_unit_per_instance": 4
                                    },
                                    "decode": {
                                        "model_unit_spec": "MU1",
                                        "capacity_unit_per_instance": 4
                                    }
                                }
                            }
                        ]
                    },
                    {
                        "plan": "lora"
                    }
                ]
            }
        ]
    }
}
```

### **响应参数**

**参数**

**类型**

**说明**

models

Array

可部署模型列表。

models\[\].model\_name

String

模型名称。

models\[\].plans

Array

该模型支持的部署方案列表。使用`version=v1.0`时返回。

models\[\].plans\[\].plan

String

部署方案类型：`mu`（模型单元）、`cu`（算力单元）、`ptu`（预置吞吐量）、`lora`（LoRA共享部署）。

models\[\].plans\[\].templates

Array

部署模板列表（`plan=mu`时返回）。

page\_no

Number

查询页码。

page\_size

Number

查询页大小。

total

Long

满足查询条件的所有模型个数。

### **模板字段说明（templates）**

**参数**

**类型**

**说明**

template\_id

String

模板 ID，在[创建模型部署任务](#13f7a7d05829h)时作为`template_id`参数传入。

template\_name

String

模板显示名称。

template\_type

String

模板类型：`COUPLED`（非 PD 分离，使用`capacity`参数）、`SEPERATED`（PD 分离，使用`prefill_capacity`和`decode_capacity`参数）。

template\_version

String

模板版本。

template\_desc

String

模板描述。

roles

Object

节点角色配置。COUPLED 模式包含`unified`节点，SEPERATED 模式包含`prefill`和`decode`节点。

### **roles 节点字段说明**

**参数**

**类型**

**说明**

model\_unit\_spec

String

模型单元规格。

capacity\_unit\_per\_instance

Number

单实例容量单元数，即 base\_capacity。创建部署时`capacity`必须是该值的整数倍。

## 创建模型部署任务

### **地址**

```
POST https://dashscope.aliyuncs.com/api/v1/deployments
```

### **请求示例**

#### 按预置吞吐（PTU）计费

**说明**

执行以下部署命令后，即便您还没有调用模型，模型部署服务仍将在部署成功后开始计费。建议您先确认服务计费规则，再执行部署命令。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5681566771/p1069175.png)

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "name": "my_qwen_flash",
    "model_name": "qwen-flash-2025-07-28",
    "plan": "ptu",
    "ptu_capacity": {
        "input_tpm": 10000,
	"output_tpm": 1000
    }
}'
```

#### 按模型单元的使用时长计费

**说明**

-   执行以下部署命令后，即便您还没有调用模型，模型部署服务仍将在部署成功后开始计费。建议您先确认服务计费规则，再执行部署命令。
    
-   模型单元-后付费方式的算力资源先买到先得。如购买不成功会全额退款。
    

#### ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1816324671/p1028065.png)

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "name": "my_qwen_plus",  
    "model_name": "qwen-plus-2025-12-01",
    "plan": "mu",
    "deploy_spec": "MU1",
    "enable_thinking": true,
    "capacity": 4,
    "max_context_length": 10000,
    "rpm_limit": 500,
    "tpm_limit": 1000
}'
```

模型单元部署模式还支持以下更多设置：

**配置内容**

**配置详情**

配置模型推理模式

部分模型在以**模型单元**方式部署时，可配置推理模式、最长上下文等。

-   Instruct - 模型部署后以**非思考模式**进行推理。
    
-   Thinking - 模型部署后以思考模式进行推理。
    

最长上下文

部分模型的**模型单元**部署模式支持该设置。最长上下文长度基于模型类型。

服务限流

部分模型的**模型单元**部署模式支持该设置，可限制模型调用的 RPM、TPM。

如何在 API 设置上述内容，请参考：[使用 API 创建模型部署任务](https://help.aliyun.com/zh/model-studio/model-deployment-api#0dda8fc0587ho)。

#### 按模型 Token 使用量计费

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1816324671/p1028063.png)

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{        
    "model_name": "qwen3-8b-ft-202511132025-0260",
    "plan": "lora",
    "capacity": 1,
    "name": "qwen3-8b-ft"
}'
```

> capacity 参数设置无效，但必须填写。如需希望扩缩容，请前往百炼模型部署[控制台](https://bailian.console.aliyun.com/tab=model?tab=model#/efm/model_deploy)填写表单申请。

#### **按算力单元的使用时长收费（仅适用于图片生成、视频生成）**

**说明**

执行以下部署命令后，即便您还没有调用模型，模型部署服务仍将在部署成功后开始计费。建议您先确认服务计费规则，再执行部署命令。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1816324671/p1028070.png)

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{        
    "model_name": "animate-anyone-detect",
    "capacity": 2,
    "plan": "cu",
    "name": "my_animate"
}'
```

### **请求参数**

**参数**

**类型**

**传参方式**

**必选**

**说明**

model\_name

String

body

是

待部署的模型名称，对应[我的模型](https://bailian.console.aliyun.com/?tab=model#/efm/model_center)中的模型 ID。

plan

String

body

是

部署方案，支持以下计费模式：

**计费方式**

**plan 设置**

按模型单元计费

`"plan": "mu"`

按算力单元计费

`"plan": "cu"`

预置吞吐量

`"plan": "ptu"`

LoRA 共享部署（按 Token 用量计费）

`"plan": "lora"`

调优后的模型支持的部署方式可以在[我的模型](https://bailian.console.aliyun.com/?tab=model#/efm/model_center)中快速查询到。

**说明**

CosyVoice 系列调优模型当前仅支持`"plan": "mu"`。

name

String

body

是

模型的控制台显示名称

capacity

Integer

body

否

仅`"plan": "mu"`时必填，部署使用的资源单元数量，需为`base_capacity`的整数倍。不同`deploy_spec`的取值约束不同，例如`MU2`必须为 8 的倍数，`MU5`可填 1。样例：`"capacity": 1`。

billing\_method

String

body

否

仅`"plan": "mu"`时必填，计费方式。当前支持`"POST_PAY"`（后付费）。样例：`"billing_method": "POST_PAY"`。

deploy\_spec

String

body

否

仅`"plan": "mu"`时，可填写该设置。

具体支持情况请参考：[模型单元部署的功能支持情况](#2fc096b2fdw9z)。

当设置`"plan": "mu"`时，该参数**必须填写**。样例：`"deploy_spec": "MU1"`。

**说明**

CosyVoice 等部分调优模型不接受 `MU1` / `MU2` 等友好名缩写，必须使用具体规格的真实 ID（形如 `dps-20260521172224-1vabse`）。可通过[获取可以部署的模型列表](#dc35528058t0d)接口返回的 `deploy_specs` 字段获取。

enable\_thinking

Boolean

body

否

部分模型支持，可设置为`true`或`false`。

max\_context\_length

Number

body

否

部分模型支持。样例：`"max_context_length": 131072`。

rpm\_limit

Number

body

否

部分模型支持， requests per minute，每分钟请求数。

tpm\_limit

Number

body

否

部分模型支持， token per minute，每分钟 Token 使用量。

ptu\_capacity

Object

body

否

仅`"plan": "ptu"`时，可填写该设置。

具体支持情况请参考：[PTU部署的功能支持情况](#2fc096b2fdw9z)。

如果不填写该参数，将默认按照 `10,000 input_tpm` 和 `1,000 output_tpm` 进行设置。

当设置`"plan": "ptu"`时，该参数才生效。

样例：`"ptu_capacity": { "input_tpm": 10000, "output_tpm": 1000 }`。

ptu\_capacity.input\_tpm

Number

body

否

所有模型支持，input token pre-minute，部署的模型每分钟支持的最大输入 Token 量。

ptu\_capacity.output\_tpm

Number

body

否

所有模型支持，output token pre-minute，部署的模型每分钟支持的最大输出 Token 量。

ptu\_capacity.thinking\_output\_tpm

Number

body

否

部分模型支持，thinking output token pre-minute，部署的模型每分钟支持的预置思考最大输出 Token 量。

suffix

String

body

否

模型部署后，将生成新的模型名称，**suffix** 用于指定新模型名称的后缀，最大长度为8个字符且需全局唯一。每个模型在首次部署时，可以不指定后缀。如果需要对同一模型进行多次部署，则必须设置后缀以便于区分。

参考输出参数 **deployed\_model**。

### **支持的模型**

点击这里查看**支持情况**与计费

#### 按使用时长计费（预置吞吐）

`**费用 = 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM)**`

后付费按小时计算：使用时长单位为小时，单价取下表"持续 1 小时"列；预付费按天计算：使用时长单位为天，单价取下表"持续 1 天"列。

-   预付费订单支付后实时生效，有效期 N 天至第 N 天 23:59 结束。若在 22:00 后下单，到期日将自动顺延1天。
    
-   预付费订单到期后，将延后2小时停止服务，停止后资源保留14小时后释放。
    
-   预付费订单无法提前终止服务。
    
-   后付费时，如果账户欠费，部署的资源将保留并继续计费 24 小时，之后自动释放资源。
    

当模型输入超过最长输入 Token 或 超出购买的 TPM 量时，相关调用将自动切换为当前模型的按量付费模式。此时，推理性能可能下降，[限流](https://help.aliyun.com/zh/model-studio/rate-limit)将受业务空间中当前快照模型的公共流量的管控，[费用](https://help.aliyun.com/zh/model-studio/model-pricing)按模型调用（按量付费）标准计收。

-   此时，调用 API 返回 Header 将包含：`x-dashscope-ptu-overflow:true`。
    
-   TPM 统计请前往：[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)。
    

缩容场景（降配）的具体降费退费规则请参考：[降配退款规则说明](https://help.aliyun.com/zh/user-center/description-of-downgrade-refund-rules)。

##### 千问

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM/小时**

**后付费输出**

**Per 1K TPM/小时**

**预付费输入**

**Per 10K TPM/天**

**预付费输出**

**Per 1K TPM/天**

千问3.7-Max-2026-05-20

qwen3.7-max-2026-05-20

128,000

¥28.8

¥8.64

¥345.6

¥103.68

千问3.6-Flash-2026-04-16

qwen3.6-flash-2026-04-16

128,000

¥2.88

¥1.73

¥34.56

¥20.74

千问3.6-Plus-2026-04-02

qwen3.6-plus-2026-04-02

128,000

¥4.8

¥2.88

¥57.6

¥34.56

千问3.5-Plus-2026-04-20

qwen3.5-plus-2026-04-20

128,000

¥1.92

¥1.15

¥23.04

¥13.82

千问3-Max-2025-09-23

qwen3-max-2025-09-23

128,000

¥7.68

¥3.08

¥92.16

¥36.96

千问-Flash-2025-07-28

qwen-flash-2025-07-28

128,000

¥0.36

¥0.36

¥4.32

¥4.32

千问-Plus-2025-12-01

qwen-plus-2025-12-01

128,000

¥1.92

非思考：¥0.48

思考：¥1.92

¥23.04

非思考：¥5.76

思考：¥23.04

##### DeepSeek

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM/小时**

**后付费输出**

**Per 1K TPM/小时**

**预付费输入**

**Per 10K TPM/天**

**预付费输出**

**Per 1K TPM/天**

DeepSeek-v4-Pro

deepseek-v4-pro

64,000

¥43.2

¥8.64

¥518.4

¥103.68

DeepSeek-v3.2

deepseek-v3.2

64,000

¥7.2

¥1.08

¥86.4

¥12.96

DeepSeek-v3

deepseek-v3

64,000

¥7.2

¥2.88

¥86.4

¥34.56

##### 千问VL

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM/小时**

**后付费输出**

**Per 1K TPM/小时**

**预付费输入**

**Per 10K TPM/天**

**预付费输出**

**Per 1K TPM/天**

千问3-VL-Plus-2025-09-23

qwen3-vl-plus-2025-09-23

128,000

¥2.4

¥2.4

¥28.8

¥28.8

##### 更多模型

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM/小时**

**后付费输出**

**Per 1K TPM/小时**

**预付费输入**

**Per 10K TPM/天**

**预付费输出**

**Per 1K TPM/天**

GLM-5.1

glm-5.1

64,000

¥21.6

¥8.64

¥259.2

¥103.68

#### 按使用时长计费（模型单元）

`**费用 = 使用时长（小时）× 模型单元数量 × 模型单元单价**`

"模型单元单价"在后付费场景下取下表"小时单价"列；预付费按月计费时，公式改为 **包月数 × 模型单元数量 × 月单价**。

-   预付费购买的首月，如在首月内提前退订，日单价（≈ 月单价 / 30）将按 **1.2** 倍计费（不满一天按一天计费）
    

**说明**

模型单元-后付费方式的算力资源先买到先得。如购买不成功会全额退款。

##### 文本生成

###### 千问

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**包月单价（元）**

千问3.6-35B-A3B

qwen3.6-35b-a3b

MU8

¥47

¥22,400

MU9

¥51

¥24,600

千问3.6-27B

qwen3.6-27b

MU9

¥51

¥24,600

千问3.6-Plus-2026-04-02

qwen3.6-plus-2026-04-02

MU1

¥54

PD分离模式：¥864

¥26,118

PD分离模式：¥417,888

千问3.5-397B-A17B

qwen3.5-397b-a17b

MU3

¥137

PD分离模式：¥2,192

¥65,969

PD分离模式：¥1,055,504

MU6

¥25

¥12,089

千问3.5-122B-A10B

qwen3.5-122b-a10b

MU1

¥54

¥26,118

MU2

¥80

¥38,000

MU6

¥25

¥12,089

MU9

¥51

¥24,600

千问3.5-35B-A3B

qwen3.5-35b-a3b

MU1

¥54

¥26,118

MU2

¥80

¥38,000

MU8

¥47

¥22,400

MU9

¥51

¥24,600

千问3.5-27B

qwen3.5-27b

MU1

¥54

¥26,118

MU9

¥51

¥24,600

千问3.5-9B

qwen3.5-9b

MU1

¥54

¥26,118

MU8

¥47

¥22,400

MU9

¥51

¥24,600

千问3.5-Plus-2026-02-15

qwen3.5-plus-2026-02-15

MU1

¥54

PD分离模式：¥864

¥26,118

PD分离模式：¥417,888

MU3

¥137

PD分离模式：¥2,192

¥65,969

PD分离模式：¥1,055,504

千问3-235B-A22B-Instruct-2507

qwen3-235b-a22b-instruct-2507

MU1

¥54

¥26,118

MU2

¥80

¥38,000

千问3-Next-80B-A3B-Instruct

qwen3-next-80b-a3b-instruct

MU1

¥54

¥26,118

千问3-32B

qwen3-32b

MU1

¥54

¥26,118

MU6

¥25

¥12,089

千问3-30B-A3B

qwen3-30b-a3b

MU9

¥51

¥24,600

千问3-30B-A3B-Instruct-2507

qwen3-30b-a3b-instruct-2507

MU1

¥54

¥26,118

MU2

¥80

¥38,000

千问3-8B

qwen3-8b

MU1

¥54

¥26,118

MU2

¥80

¥38,000

MU5

¥21

¥10,139

千问3-4B

qwen3-4b

MU1

¥54

¥26,118

MU5

¥21

¥10,139

千问3-1.7B

qwen3-1.7b

MU1

¥54

¥26,118

MU5

¥21

¥10,139

千问3-Embedding-0.6B

qwen3-embedding-0.6b

MU5

¥21

¥10,139

MU6

¥25

¥12,089

千问3-MoE-Rerank-0.6B

qwen3-moe-rerank-0.6b

MU5

¥21

¥10,139

千问3-Rerank-0.6B

qwen3-rerank-0.6b

MU5

¥21

¥10,139

MU6

¥25

¥12,089

千问3-Max-2025-09-23

qwen3-max-2025-09-23

MU2

¥80

¥38,000

MU3

¥137

¥65,969

千问3-Rerank

qwen3-rerank

MU5

¥21

¥10,139

千问2.5-开源版-72B

qwen2.5-72b-instruct

MU1

¥54

¥26,118

千问2.5-开源版-32B

qwen2.5-32b-instruct

MU1

¥54

¥26,118

千问2.5-开源版-14B

qwen2.5-14b-instruct

MU1

¥54

¥26,118

千问2.5-开源版-7B

qwen2.5-7b-instruct

MU1

¥54

¥26,118

MU5

¥21

¥10,139

千问2.5-开源版-3B

qwen2.5-3b-instruct

MU5

¥21

¥10,139

千问-Flash-2025-07-28

qwen-flash-2025-07-28

MU1

¥54

¥26,118

千问-Plus-2025-07-28

qwen-plus-2025-07-28

MU1

¥54

PD分离模式：¥864

¥26,118

PD分离模式：¥417,888

千问-Plus-2025-12-01

qwen-plus-2025-12-01

MU1

¥54

¥26,118

###### GLM

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**包月单价（元）**

GLM-5

glm-5

MU3

¥137

PD分离模式：¥2,192

¥65,969

PD分离模式：¥1,055,504

GLM-4.7

glm-4.7

MU6

¥25

PD分离模式：¥800

¥12,089

PD分离模式：¥386,848

###### DeepSeek

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**包月单价（元）**

DeepSeek-v4-Flash

deepseek-v4-flash

MU1

¥54

¥26,118

DeepSeek-v3.2

deepseek-v3.2

MU2

¥80

PD分离模式：¥1,280

¥38,000

PD分离模式：¥608,000

###### 更多模型

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**包月单价（元）**

MiniMax-M2.5

MiniMax-M2.5

MU1

¥54

PD分离模式：¥864

¥26,118

PD分离模式：¥417,888

Kimi-K2.5

kimi-k2.5

MU2

¥80

¥38,000

模型类型：

-   Instruct - 模型部署后以**非思考模式**进行推理。
    
-   Thinking - 模型部署后以思考模式进行推理。
    

模型部署类型：

-   PD 分离模式 - **降低首 Token 延迟、提高吞吐。**
    
    该部署模式部署的模型在进行模型推理时，将首 Token 计算（Prefill）和后续 Token 计算（Decode）两个计算阶段，拆到不同的计算节点执行。
    

##### 多模态

###### 千问VL

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**包月单价（元）**

千问3-VL-235B-A22B-Instruct

qwen3-vl-235b-a22b-instruct

MU1

¥54

¥26,118

千问3-VL-235B-A22B-Thinking

qwen3-vl-235b-a22b-thinking

MU1

¥54

¥26,118

千问3-VL-32B-Instruct

qwen3-vl-32b-instruct

MU2

¥80

¥38,000

千问3-VL-8B-Instruct

qwen3-vl-8b-instruct

MU1

¥54

¥26,118

千问3-VL-4B-Instruct

qwen3-vl-4b-instruct

MU1

¥54

¥26,118

千问3-VL-2B-Instruct

qwen3-vl-2b-instruct

MU5

¥21

¥10,139

千问3-VL-Embedding-2B

qwen3-vl-embedding-2b

MU5

¥21

¥10,139

千问3-VL-Flash-2025-10-15

qwen3-vl-flash-2025-10-15

MU1

¥54

¥26,118

千问3-VL-Plus-2025-09-23

qwen3-vl-plus-2025-09-23

MU1

¥54

¥26,118

千问VL-Max-2025-08-13

qwen-vl-max-2025-08-13

MU6

¥25

¥12,089

千问VL-OCR-2025-11-20

qwen-vl-ocr-2025-11-20

MU6

¥25

¥12,089

###### 千问 Omni

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**包月单价（元）**

千问3.5-Omni-Flash

qwen3.5-omni-flash

MU8

¥47

¥22,400

MU9

¥51

¥24,600

千问3.5-Omni-Plus

qwen3.5-omni-plus

MU9

¥51

¥24,600

模型类型：

-   Instruct - 模型部署后以**非思考模式**进行推理。
    
-   Thinking - 模型部署后以思考模式进行推理。
    
-   Instruct/Thinking - 可在模型部署时**选择是否开启思考模式**。
    

##### 语音合成

**CosyVoice**

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**包月单价（元）**

cosyvoice-v3-flash

cosyvoice-v3-flash

MU5

¥20

¥9,500

#### 按模型 Token 使用量

`**费用 = 模型输入 Token 数 × 模型输入单价 + 模型输出 Token 数 × 模型输出单价（最小计费单位：1 token）**`

-   仅当对下列基础模型完成 SFT 高效训练并得到自定义模型后，才支持按模型 Token 使用量计费。
    

##### 千问

**基础模型**

**模型代码**

**输入**

**元/千Token**

**输出**

**元/千Token**

千问3-32B

qwen3-32b

¥0.002

非思考模式：¥0.008

思考模式：¥0.02

千问3-14B

qwen3-14b

¥0.001

非思考模式：¥0.004

思考模式：¥0.01

千问3-8B

qwen3-8b

¥0.0005

非思考模式：¥0.002

思考模式：¥0.005

千问2.5-开源版-72B

qwen2.5-72b-instruct

¥0.004

¥0.012

千问2.5-开源版-32B

qwen2.5-32b-instruct

¥0.002

¥0.006

千问2.5-开源版-14B

qwen2.5-14b-instruct

¥0.001

¥0.003

千问2.5-开源版-7B

qwen2.5-7b-instruct

¥0.0005

¥0.001

##### 千问VL

**基础模型**

**模型代码**

**输入**

**元/千Token**

**输出**

**元/千Token**

千问3-VL-8B-Instruct

qwen3-vl-8b-instruct

¥0.0005

¥0.002

千问2.5-VL-72B

qwen2.5-vl-72b-instruct

¥0.016

¥0.048

千问2.5-VL-32B

qwen2.5-vl-32b-instruct

¥0.008

¥0.024

千问2.5-VL-7B

qwen2.5-vl-7b-instruct

¥0.002

¥0.005

#### **图片、视频生成模型（预置）-按实例时长计费**

`**费用 = 资源占用时长（小时）× 实例数量 × 实例单价（不满 1 小时按 1 小时计费）**`

"实例单价"在后付费场景下取下表"后付费单价（元/实例/小时）"列；预付费按月计费时，公式改为 **包月数 × 实例数量 × 预付费单价（元/月）**。

##### 图片生成

**模型服务**

**模型类型**

**独占实例资源规格**

**后付费单价（元/实例/小时）**

**预付费单价**

**（元/月）**

万相-文本生成图像-0521

预置模型

轻量版

¥20/实例/小时

¥10,000/月

##### 视频生成

**模型服务**

**模型类型**

**独占实例资源规格**

**后付费单价（元/实例/小时）**

**预付费单价**

**（元/月）**

悦动人像EMO-detect

预置模型

轻量版

¥20/实例/小时

¥10,000/月

悦动人像EMO

舞动人像AnimateAnyone-detect

舞动人像AnimateAnyone

### **响应示例**

命令执行完成后，返回如下结果：

```
{
  "request_id": "f2ae64f7-83cc-410c-bc0b-840443f7eb86",
  "output": {
    "deployed_model": "emo-35b3f106-sample01",
    "gmt_create": "2025-06-17T11:00:38.68",
    "gmt_modified": "2025-06-17T11:00:38.68",
    "status": "PENDING",
    "model_name": "emo",
    "base_model": "emo",
    "base_capacity": 1,
    "capacity": 1,
    "ready_capacity": 0,
    "workspace_id": "llm-v71tlv3d***",
    "charge_type": "post_paid",
    "creator": "175805416***",
    "modifier": "175805416***"
  }
}
```

### **响应参数**

**参数**

**类型**

**说明**

request\_id

String

本次请求的ID。

output

Object

本次部署任务的详细信息。

deployed\_model

String

新模型的唯一标识。在发起模型调用请求时需要在SDK参数传入。

gmt\_create

String

创建部署任务的时间。

gmt\_modified

String

修改部署任务的时间。

status

String

部署任务的状态。

-   PENDING：正在创建部署任务。
    
-   UPDATING：正在更新部署任务。
    
-   RUNNING：部署任务正在运行，此时已部署的模型可以正常处理请求。
    
-   STOPPED：部署任务已经停止，此时的部署任务不会被计费。
    
-   DELETING：正在删除部署任务。
    
-   FAILED：部署任务创建或更新失败。
    

model\_name

String

部署任务使用的模型名称。

base\_model

String

部署任务使用的模型对应的基础模型ID。

base\_capacity

Number

基础模型运行所需的最小资源单元数量。

capacity

Number

部署任务使用的资源单元数量。

ready\_capacity

Number

已就绪并可立即处理请求的资源单元数量。受限于资源初始化速度或硬件状态。

workspace\_id

String

部署任务所属的业务空间ID。

charge\_type

String

部署任务的扣费方法。

> `post_paid`：后付费。

creator

String

该部署任务创建人UID。

modifier

String

对该部署任务进行最后一次操作的账号UID。

plan

String

部署任务的计费模式。（部分模式不显示该参数）

仅**模型单元**部署方式响应

model\_unit\_spec

String

模型单元规格。

enable\_thinking

Boolean

是否开启思考模式，部分模型支持。

max\_context\_length

Number

最大上下文长度限制。

rpm\_limit

String

Requests per minute，每分钟请求数。

tpm\_limit

Number

Token per minute，每分钟 Token 使用量。

仅预置吞吐量（ptu）部署方式响应

ptu\_capacity

Object

当设置`"plan": "ptu"`时，该参数才生效。

样例：`"ptu_capacity": { "input_tpm": 10000, "output_tpm": 1000 }`。

ptu\_capacity.input\_tpm

Number

所有模型支持，input token pre-minute，部署的模型每分钟支持的最大输入 Token 量。

ptu\_capacity.output\_tpm

Number

所有模型支持，output token pre-minute，部署的模型每分钟支持的最大输出 Token 量。

ptu\_capacity.thinking\_output\_tpm

Number

部分模型支持，thinking output token pre-minute，部署的模型每分钟支持的预置思考最大输出 Token 量。

## 修改部署的模型设置

**说明**

仅模型单元部署方式的[部分模型](#2fc096b2fdw9z)支持修改设置 rpm 和 tpm。

### **地址**

```
PUT https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}/update
```

### **请求示例**

通过以下命令可以查询指定专属服务的详细信息：

```
curl -X PUT "https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}/update" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "rpm_limit": 1000,
    "tpm_limit": 200
}'
```

### **请求参数**

**参数**

**类型**

**传参方式**

**必选**

**说明**

deployed\_model

String

path

是

新模型的唯一标识。

rpm\_limit

Number

body

至少填写一个参数

Requests per minute，每分钟请求数。

tpm\_limit

Number

body

Token per minute，每分钟 Token 使用量。

### **响应示例**

命令执行完成后，返回如下结果：

```
{
    "request_id": "1d121fd9-876c-40ad-bc40-a9e68ef3b986",
    "output":
    {
        "deployed_model": "qwen-plus-2025-12-01-b6d61c71",
        "gmt_create": "2026-01-07T13:52:44",
        "gmt_modified": "2026-01-07T14:01:41",
        "status": "PENDING",
        "model_name": "qwen-plus-2025-12-01",
        "base_model": "qwen-plus-2025-12-01",
        "base_capacity": 4,
        "capacity": 4,
        "ready_capacity": 0,
        "workspace_id": "llm-8v53e*******",
        "charge_type": "post_paid",
        "creator": "16542902******",
        "modifier": "16542902********",
        "plan": "mu",
        "model_unit_spec": "MU1",
        "enable_thinking": true,
        "max_context_length": 1,
        "rpm_limit": 1000,
        "tpm_limit": 200
    }
}
```

### **响应参数**

请参考[创建模型部署任务](#13f7a7d05829h)的响应参数。

## 查询模型部署任务

### **地址**

```
GET https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}
```

### **请求示例**

通过以下命令可以查询指定专属服务的详细信息：

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments/qwen-plus-202305099980-fac9-sample" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

### **请求参数**

**参数**

**类型**

**传参方式**

**必选**

**说明**

deployed\_model

String

path

是

新模型的唯一标识。

### **响应示例**

命令执行完成后，返回如下结果：

```
{
  "request_id": "66a855f0-a6fe-4b05-9786-fb30c7c6782d",
  "output": {
    "deployed_model": "emo-35b3f106-sample01",
    "gmt_create": "2025-06-17T11:00:38",
    "gmt_modified": "2025-06-17T11:06:13",
    "status": "RUNNING",
    "model_name": "emo",
    "base_model": "emo",
    "base_capacity": 1,
    "capacity": 1,
    "ready_capacity": 1,
    "workspace_id": "llm-v71tlv3***",
    "charge_type": "post_paid",
    "creator": "175805416***",
    "modifier": "175805416***"
  }
}
```

### **响应参数**

请参考[创建模型部署任务](#13f7a7d05829h)的响应参数。

## 列举模型部署任务

### **地址**

```
GET https://dashscope.aliyuncs.com/api/v1/deployments
```

### **请求示例**

通过以下命令可以获取专属服务列表：

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments?page_no=1&page_size=100" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

### **请求参数**

**参数**

**类型**

**传参方式**

**必选**

**说明**

page\_no

Number

query

否

页码，默认值为1。

page\_size

Number

query

否

页大小，默认为50，最大值为200，最小值为1。

### **响应示例**

命令执行完成后，返回以下结果：

```
{
  "request_id": "7efdd3a7-a90d-96c6-b477-70055d59edf7",
  "output": {
    "page_no": 1,
    "page_size": 10,
    "total": 1,
    "deployments": [
      {
        "deployed_model": "emo-35b3f106-sample01",
        "gmt_create": "2025-06-17T11:00:38",
        "gmt_modified": "2025-06-17T11:06:13",
        "status": "RUNNING",
        "model_name": "emo",
        "base_model": "emo",
        "base_capacity": 1,
        "capacity": 1,
        "ready_capacity": 1,
        "workspace_id": "llm-v71tlv3d***",
        "charge_type": "post_paid",
        "creator": "175805416***",
        "modifier": "175805416***"
      }
    ]
  }
}
```

### **响应参数**

请参考[创建模型部署任务](#13f7a7d05829h)的响应参数。

## 更新模型部署任务

通过更新操作调整专属服务使用的资源单元数量。

### **地址**

```
PUT https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}/scale
```

### **请求示例**

通过以下命令可以将指定的服务进行扩缩容：

```
curl --request PUT "https://dashscope.aliyuncs.com/api/v1/deployments/emo-35b3f106-sample01/scale" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json' \
    --data '{    
                "capacity":2
            }'
```

### **请求参数**

**参数**

**类型**

**传参方式**

**必选**

**说明**

deployed\_model

String

path

是

新模型的唯一标识。

capacity

Number

body

条件必选

仅`"plan": "mu"`时，可填写该设置。

具体支持情况请参考：[模型单元部署的功能支持情况](#2fc096b2fdw9z)。

更新之后，模型所使用的资源单元。**必须**是`[base_capacity](#4d68826158yix)`的整数倍。

ptu\_capacity

Object

body

条件必选

仅`"plan": "ptu"`时，可填写该设置。

具体支持情况请参考：[PTU部署的功能支持情况](#2fc096b2fdw9z)。

当设置`"plan": "ptu"`时，该参数才生效。

样例：`"ptu_capacity": { "input_tpm": 10000, "output_tpm": 1000 }`。

ptu\_capacity.input\_tpm

Number

body

所有模型支持，input token pre-minute，部署的模型每分钟支持的最大输入 Token 量。

ptu\_capacity.output\_tpm

Number

body

所有模型支持，output token pre-minute，部署的模型每分钟支持的最大输出 Token 量。

ptu\_capacity.thinking\_output\_tpm

Number

body

部分模型支持，thinking output token pre-minute，部署的模型每分钟支持的预置思考最大输出 Token 量。

### **响应示例**

命令执行完成后，返回以下结果：

```
{
  "request_id": "6c6b7676-3fea-423b-bc26-c9e2337e1142",
  "output": {
    "deployed_model": "emo-35b3f106-sample01",
    "gmt_create": "2025-06-17T11:00:38",
    "gmt_modified": "2025-06-17T11:42:02.311",
    "status": "UPDATING",
    "model_name": "emo",
    "base_model": "emo",
    "base_capacity": 1,
    "capacity": 2,
    "ready_capacity": 1,
    "workspace_id": "llm-v71tlv3dezezp2en",
    "charge_type": "post_paid",
    "creator": "17580541***",
    "modifier": "17580541***"
  }
}
```

### **响应参数**

请参考[创建模型部署任务](#13f7a7d05829h)的响应参数。

## 删除模型部署任务

### **地址**

```
DELETE https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}
```

### **请求示例**

通过以下命令可以删除指定的部署任务。

```
curl --request DELETE "https://dashscope.aliyuncs.com/api/v1/deployments/emo-35b3f106-sample01" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

### **请求参数**

**参数**

**类型**

**传参方式**

**必选**

**说明**

deployed\_model

String

path

是

新模型的唯一标识。

### **响应示例**

命令执行完成后，返回以下结果：

```
{
  "request_id": "5378b78b-8564-481f-a3e0-580e551df22c",
  "output": {
    "deployed_model": "emo-35b3f106-sample01",
    "gmt_create": "2025-06-17T11:00:38",
    "gmt_modified": "2025-06-17T11:42:02",
    "status": "DELETING",
    "model_name": "emo",
    "base_model": "emo",
    "base_capacity": 1,
    "capacity": 2,
    "ready_capacity": 1,
    "workspace_id": "llm-v71tlv3***",
    "charge_type": "post_paid",
    "creator": "175805416***",
    "modifier": "175805416***"
  }
}
```

### **响应参数**

请参考[创建模型部署任务](#13f7a7d05829h)的响应参数。

## 异常响应

### **响应示例**

```
{
    "request_id": "ca218d57-b91b-46b2-bd35-c41c6287bcf4",
    "message": "Model: qwen-plus-20230703-cx7f not found!",
    "code": "NotFound"
}
```

### **响应参数**

**字段**

**类型**

**描述**

request\_id

String

本次请求的系统唯一码。

code

String

错误码。

message

String

错误信息。

当请求出错时，可能返回以下错误：

**错误码**

**错误信息**

**错误原因**

**NotFound**

Model: xxx not found!

-   创建部署任务时指定了不存在的模型。
    
-   查询/更新/删除部署任务时指定了不存在的模型。
    

**Conflict**

Deployed model xxx already exists, please specify a suffix.

创建部署任务时使用了已使用过的suffix。

**InvalidParameter**

Invalid capacity (xx), capacity must be larger than or equal to 0 and multiples of 1 and less than 1000!

创建/更新部署任务时指定了无效的算力单元数量。
