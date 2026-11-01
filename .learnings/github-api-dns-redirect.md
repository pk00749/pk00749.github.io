## 2026-10-29: GitHub API 被 DNS/hosts 重定向导致 301

**现象**: 调用 `https://api.github.com/repos/...` 返回 HTTP 301，Location 指向 `https://github.com/repos/...`，所有请求（含 rate_limit）都被重定向。

**原因**: 本机 `/etc/hosts` 把 `api.github.com` 和 `github.com` 指向同一个 IP（140.82.121.3，即 github.com 的 web IP），api.github.com 的正确 API IP 是 140.82.113.x/114.x/116.x 等。curl 默认不做跨 host 的 --resolve 覆盖，所以被 gitHub web 层重定向。

**解决**: 用 `curl --resolve api.github.com:443:140.82.113.6 ...` 指定真实 API IP。

**其他方案**（本次也踩到）:
- `git clone`/`git fetch` 走 github.com 也非常慢（curl 28 Operation too slow），浅克隆 9 页文件都拉不下来。GitHub API 单文件 PUT 上传更快更稳。
- 本地 workspace git 仓库的 `origin/master` 是 GitHub Pages 站点分支（带 `_posts/`），`origin/main` 是 workspace 自身分支。**推 `_posts/` 应走 GitHub API PUT 到 master 分支**，而不是本地 git commit。

**教训**: 000533 公告推送任务的 GitHub API 调用必须带 `--resolve` 参数（或改用 curl 而非 python urllib，urllib 同样会跟随重定向导致 PUT 失败）。
