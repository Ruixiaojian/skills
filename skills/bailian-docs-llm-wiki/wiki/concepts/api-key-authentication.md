# API Key 认证与安全

API Key 是调用阿里云百炼平台大模型和应用服务的唯一鉴权凭证，用于标识调用者身份并控制访问权限。安全地管理和使用 API Key 是保障生产环境稳定运行的基础。

## 基本概念

API Key 的格式为 `sk-xxxxx`，创建后永久有效（无过期时间），手动删除后即失效。单个 API Key 只能归属**一个地域**内的**一个业务空间**和**一个用户**，不可转移。同一业务空间内的 API Key 权限相同，无需为不同模型类型（文生文、文生图、语音合成等）创建不同的 API Key。

> **注意**：Coding Plan 使用专属 API Key（格式：`sk-sp-xxxxx`），与百炼通用 API Key 不同。

## 获取与创建

### 权限要求

需使用主账号，或具备`管理员`或`API-Key`页面权限的子账号操作。

### 数量限制

| 地域 | 上限 |
|------|------|
| 华北2（北京）、新加坡、德国（法兰克福） | 每个主账号每个地域最多 50 个 |
| 美国（弗吉尼亚） | 每个归属账号最多 20 个 |

### 权限配置

- **全部**：授予调用所有模型与应用的权限。
- **自定义**：可配置 IP 访问白名单（最多 20 个 IPv4/IPv6 地址或网段）。

> 目前仅华北2（北京）地域支持 IP 白名单等精细权限控制。

## 安全存储：配置环境变量

为避免在代码中硬编码 API Key 导致泄漏风险，**必须**将其配置为环境变量。环境变量名称统一为 `DASHSCOPE_API_KEY`。

```bash
# Linux / macOS 永久生效
echo 'export DASHSCOPE_API_KEY="sk-xxx"' >> ~/.bashrc
source ~/.bashrc
```

```cmd
# Windows CMD 永久生效
setx DASHSCOPE_API_KEY "sk-xxx"
```

### 环境变量不生效的常见原因

- 仅设置了临时环境变量，对已启动的 IDE 或应用不生效
- 设置永久环境变量后未重启 IDE 或命令行工具
- 使用 `sudo` 执行脚本时未继承环境变量（可用 `sudo -E` 解决）
- 应用通过 systemd 等服务管理器启动，需在其配置文件中单独添加

## 调用时使用

API Key 通过 HTTP 请求头 `Authorization: Bearer` 传递：

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
```

各地域对应独立的 Base URL 和 API Key，**不可跨地域混用**：

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

## 临时 API Key

在浏览器、移动 App 等不可信环境中，应使用临时 API Key 代替永久 API Key 以防止泄露。

### 生成方式

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 关键参数

| 参数 | 说明 |
|------|------|
| `expire_in_seconds` | 有效期，范围 [1, 1800] 秒，默认 60 秒 |

### 响应示例

```json
{
  "token": "st-****",
  "expires_at": 1744080369
}
```

### 限制

- 临时 API Key（`st-` 前缀）继承生成它的永久 API Key 的全部权限
- 到期后自动失效，无法手动删除
- 不同地域需使用对应的 Endpoint 生成

## 权限与生命周期管理

### API Key 权限边界

- API Key 的可调用模型和限流与归属业务空间的权限一致
- 不受用户控制台页面权限管理的影响
- 子业务空间的 API Key 仅能调用该空间授权的模型

### 状态变更规则

| 操作 | 结果 |
|------|------|
| 主动删除 | 失效，不可恢复 |
| RAM 账号移出业务空间 | 失效（重新加入后恢复） |
| RAM 控制台删除账号 | 失效，不可恢复 |

> 自 2026 年 3 月 25 日起，华北2（北京）地域所有新创建的 API Key 均归属主账号。

## 安全最佳实践

1. **永远不要在客户端代码中硬编码** API Key，使用环境变量或密钥管理服务。
2. **前端/移动端场景**使用临时 API Key，有效期设置为满足业务需求的最短时间。
3. **生产环境按空间隔离**：为 dev/test/prod 创建独立业务空间，使用各自的 API Key。
4. **启用 IP 白名单**（北京地域）：限制 API Key 只能从特定 IP 地址调用。
5. **定期轮换**：虽然 API Key 无过期时间，仍建议定期删除旧 Key 并创建新 Key。
6. **如需停止服务**：在控制台删除已创建的 API Key 即可阻止所有调用。

## 关联主题页

- [preparations](../api/preparations.md)
- [more about models](../api/more-about-models.md)
- [more](../api/more.md)
- [application permission management](../guides/application-permission-management.md)
- [get started with models](../guides/get-started-with-models.md)
- [security and compliance](../guides/security-and-compliance.md)
- [support](../guides/support.md)


