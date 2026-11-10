# 将本地项目发布为 GitHub 开源仓库 + GitHub Pages

**本发行包未确认远程仓库已创建，也未声称 Pages 已上线。**

## 1. 先验证源码

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests -v
node --check assets/app.js
node tests/test_calc.js
```

## 2. 创建新公开仓库并推送（本机已安装 Git 与 GitHub CLI）

从解压目录执行：

```bash
cd local-business-ai-growth-handbook
git init -b main
git add .
git commit -m "feat: launch local business AI growth handbook"
gh auth status
gh repo create AIPMAndy/local-business-ai-growth-handbook --public --source=. --remote=origin --push
```

如果仓库已经存在，不要再次运行 `gh repo create`；先 `gh repo view AIPMAndy/local-business-ai-growth-handbook` 核对权限与现有内容后再提交。若当前默认分支不是 `main`，需根据实际情况调整 Actions 触发分支。

## 3. 启用 Pages

仓库 → Settings → Pages → Build and deployment → Source：**GitHub Actions**。

推送 `main` 后 `.github/workflows/pages.yml` 先运行 Python/Node 测试，通过后发布 `_site`。检查 Actions 最终结果，不通过必须修复。

## 4. 线上检查，不通过不能宣称发布完成

- 打开 `https://github.com/AIPMAndy/local-business-ai-growth-handbook`，确认 `visibility = public` 且 README 与文件齐全。
- 打开 `https://aipmandy.github.io/local-business-ai-growth-handbook/`，确认能加载首页（HTTP 200），且页面不是 404。
- 抽查：`/plan.html`、`/tools.html`、`/prompts.html`、`/chapters/06.html`、`/chapters/19.html`、`/privacy.html`。
- 在真机与桌面浏览器测试章节搜索、完成勾选/重新打开后持久化、进度 JSON 导出/导入、微信复制、利润计算、广告链接与官方资料链接。
- 对外发布后再把 README 开头的**“尚未确认上线”**改为有日期和证据的已完成状态。

## 5. 常见问题

- **手机打不开**：先确认 Pages source 是 GitHub Actions、工作流全部通过，并在设置页复制平台实际给出的地址。
- **CSS 丢失**：检查网站是不是在 `/local-business-ai-growth-handbook/` 子路径，以及 assets 链接相对层级。
- **Actions权限失败**：检查仓库 Actions/Pages 权限与仓库可见性；不是重新跑无效操作即可解决。
- **进度没保存**：有的浏览器会限制本地 file URL 的存储，改用本地 HTTP 服务或线上 Pages。
