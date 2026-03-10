# OpenClaw 安装教程

> 快速上手指南：如何在你的电脑上安装并运行 OpenClaw

---

## 环境要求

| 项目 | 要求 |
|------|------|
| 操作系统 | macOS、Linux、Windows (WSL2 推荐) |
| Node.js | 22.x 或更高版本 |
| 内存 | 推荐 4GB+ |
| 网络 | 需要访问 GitHub 和 npm |

---

## 安装方法

### 方法一：官方安装脚本（推荐）

这是最简单的方式，一行命令完成安装。

#### macOS / Linux / WSL2

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

#### Windows (PowerShell)

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

---

### 方法二：npm 全局安装

如果你已经安装了 Node.js 22+，可以手动安装：

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

> ⚠️ 如果遇到 sharp 构建错误，运行：
> ```bash
> SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest
> ```

---

### 方法三：本地 CLI 安装（无需 root）

适合不想污染全局 npm 环境的用户：

```bash
curl -fsSL https://openclaw.ai/install-cli.sh | bash
```

这会将 OpenClaw 安装到 `~/.openclaw` 目录下。

---

## 安装后配置

### 1. 运行引导向导

```bash
openclaw onboard --install-daemon
```

向导会帮你配置：
- API Key（LLM 提供商）
- 网关设置
- 消息通道（可选）

### 2. 检查状态

```bash
openclaw gateway status
```

### 3. 打开控制台

```bash
openclaw dashboard
```

这会在浏览器中打开 http://127.0.0.1:18789/

---

## 常用命令

| 命令 | 说明 |
|------|------|
| `openclaw status` | 查看网关状态 |
| `openclaw doctor` | 诊断配置问题 |
| `openclaw dashboard` | 打开网页控制台 |
| `openclaw gateway start` | 启动网关服务 |
| `openclaw gateway stop` | 停止网关服务 |
| `openclaw message send` | 发送测试消息 |

---

## 常见问题

### Q: 安装后提示 `openclaw: command not found`

这是 PATH 问题。重新加载 shell 配置：

```bash
# macOS / Linux
source ~/.zshrc  # 或 ~/.bashrc

# 然后验证
which openclaw
```

或者手动添加 PATH 到 `~/.zshrc`：

```bash
export PATH="$(npm prefix -g)/bin:$PATH"
```

### Q: Windows 下找不到命令

需要将 npm 全局 bin 目录添加到 PATH：

```powershell
# 查看 npm 全局路径
npm config get prefix

# 将输出的路径添加到系统 PATH
```

### Q: sharp 库构建失败

```bash
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest
```

---

## 进阶：配置消息通道

OpenClaw 支持多种消息渠道：

| 渠道 | 配置难度 | 说明 |
|------|----------|------|
| Telegram | ⭐ | 需要 Bot Token |
| Discord | ⭐ | 需要 Bot Token |
| WhatsApp | ⭐⭐ | 需要手机扫码 |
| Feishu (飞书) | ⭐⭐ | 需要企业应用 |
| Signal | ⭐⭐ | 需要手机扫码 |

详细配置请参考：https://docs.openclaw.ai/channels

---

## 更新 OpenClaw

```bash
openclaw update run
```

或者重新运行安装脚本：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

---

## 卸载

如果需要卸载：

```bash
# 停止服务
openclaw gateway stop

# 卸载 npm 包
npm uninstall -g openclaw

# 删除数据（可选）
rm -rf ~/.openclaw
```

---

## 更多资源

- 官方文档：https://docs.openclaw.ai
- GitHub：https://github.com/openclaw/openclaw
- Discord 社区：https://discord.com/invite/clawd
- ClawHub（插件市场）：https://clawhub.com

---

*更新于 2026-03-10*
