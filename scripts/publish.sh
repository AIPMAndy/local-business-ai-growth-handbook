#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
TARGET="AIPMAndy/local-business-ai-growth-handbook"
for tool in git gh python3 node; do
  command -v "$tool" >/dev/null || { echo "缺少 $tool；请先安装再发布。" >&2; exit 1; }
done
python3 scripts/build.py
python3 -m unittest discover -s tests -v
node --check assets/app.js
node tests/test_calc.js
gh auth status
# Safe default: never overwrite an existing repository or switch its remote.
if gh repo view "$TARGET" >/dev/null 2>&1; then
  echo "检测到远程仓库 $TARGET 已存在。为防止覆盖，此脚本停止；请手动核对 origin 和分支。" >&2
  exit 2
fi
if [ -d .git ]; then
  echo '检测到目录已是 Git 仓库。请核对现有 remote 后手动发布，避免误推。' >&2
  exit 3
fi
git init -b main
git add .
git commit -m "feat: publish local business AI growth handbook"
gh repo create "$TARGET" --public --source=. --remote=origin --push
echo '源码已推送。请在 GitHub Settings → Pages 选择 GitHub Actions，然后等待 verify/deploy 完成并做线上验收。'
