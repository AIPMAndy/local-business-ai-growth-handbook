# 本地生意 AI 获客保姆级攻略（2026）

<!-- andy-pdf-edition:start -->
## 精美 PDF 电子书

[**免费下载《本地生意 AI 获客攻略》**](pdf/local-business-ai-growth-handbook-guide.pdf) · [直接下载 PDF](https://github.com/AIPMAndy/local-business-ai-growth-handbook/raw/refs/heads/main/pdf/local-business-ai-growth-handbook-guide.pdf)

**71 页 · A5 手机阅读版 · 可点击目录 · 0.82 MB**  
整理日期：2026-11-13。包含完整实操正文、案例、模板与原始来源；平台规则与价格沿用原资料的核查日期。

**作者与服务（广告）**：AI 酋长 Andy · 个人微信 **AIPMAndy** · [个人官网](https://metaver.vip/) · [公司官网](https://www.a6no1.cn/)。免费教程可直接使用，咨询与合作自愿选择。
<!-- andy-pdf-edition:end -->

> **一家实体店真正需要的不是 AI 帮你发 100 条视频，而是让附近的人找到你、相信你、咨询你、到店、成交，再回来。**

**作者：AI 酋长 Andy** · [个人官网](https://metaver.vip/) · [星觉科技](https://www.a6no1.cn/) · [企业 AI + IP 获客](https://metaver.vip/services) · 业务微信：`AIPMAndy`

## 免费教程与业务联系

**🌐 [立即使用在线教程](https://aipmandy.github.io/local-business-ai-growth-handbook/)** ｜ **[GitHub 开源仓库](https://github.com/AIPMAndy/local-business-ai-growth-handbook)**

> **企业官网（星觉科技）：[https://www.a6no1.cn/](https://www.a6no1.cn/)**  
> **业务微信：`AIPMAndy`**（微信搜索添加，备注“本地生意”）
>
> **广告 · 作者商业服务：** 免费教程可直接使用。需要实体店 AI 获客诊断、内容方案或企业合作，可通过以上渠道联系。

![本地生意AI获客保姆级攻略](assets/social-preview.svg)

## 你能直接拿走什么

| 模块 | 内容 | 验收 |
|---|---|---|
| 完整课程 | **26章、104条实际操作动作**，每章都给完成凭证、常见错误 | 浏览器打开独立章节页 |
| 短视频素材 | **24条按行业分类的口播脚本**，附发布前必须补的真实证据 | `scripts.html`中逐条复制改写 |
| 30天计划 | **30天，每天一个动作**，分周推进 | 完成勾选，可导入/导出 |
| AI工具箱 | **18套可复制提示词**，覆盖定位、地图、选题、话术、匿名化和红队审核 | 复制至自己使用的AI工具 |
| 本地获客测算 | 单笔贡献毛利、咨询成交率、净贡献、每单新增获客成本 | 以自有数据复核，示例为假设 |
| 门店体检 | 10项发现/信任/承接/隐私检查 | 浏览器本地保存 |
| 6类案例 | 汽车服务的**家人行业匿名场景**+餐饮、美业、家电维修、洗衣护理、健身教学模拟 | 真实与模拟明确分级 |
| 模板 | **12个CSV**：成本、顾客原话、竞品、选题、线索、数据周报、30天计划等 | Excel/Numbers/WPS可打开 |
| 响应式网站 | 首页、工具、案例、来源、隐私、26个独立章节，共34个正文页面 | 电脑和手机可读，零外部 JS 依赖 |
| 官方来源 | 高德、百度地图、点评、抖音来客、广告规范 | `sources.html` 与 `docs/SOURCES.md` |
| 质量与发布 | Python、Node测试 + GitHub Actions/Pages 配置 | 本地测试与线上验收分开 |

## 五分钟开始

1. 下载项目 ZIP，解压后打开 `_site/index.html`。如遇 `file://` 本地存储限制，运行 `python3 -m http.server 8080 -d _site`，打开 `http://localhost:8080`。
2. 打开 `_site/plan.html`，从 Day 1 开始。**不是看完教程，而是完成每一天的凭证。**
3. 把 `_site/tools.html` 的示例数字替换为自己真实订单记录；无数据就承认“没有数据”。
4. 从 `_site/prompts.html` 复制提示词，用匿名客户问题生成第一批选题，人工核验再发布。
5. 每周只问一个问题：**合格咨询、到店和贡献毛利有没有变好？**

## 建议的运营顺序

**第一周** 选出最值得推广的一项服务，算单笔贡献，核验门店地图和顾客问题。**第二周** 修高德/百度/点评可发现性，补上主页咨询路径。**第三周** 用顾客原话和真实证据做内容，小步发布。**第四周** 把咨询、预约、到店、成交与复购记录连接起来，做一轮对照测试与复盘。详细动作见 [30天清单](templates/12-30day-plan.csv)。

## 本地运行和验收

项目只需 Python 3.10+，不需要数据库、Node 构建依赖、付费 API 或账号密码。

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests -v
node --check assets/app.js      # 可选，但建议安装 Node 18+
node tests/test_calc.js         # 可选：验证浏览器测算器公式
python3 -m http.server 8080 -d _site
```

网站**没有自动发布内容、群发消息、爬取客户信息、调用大模型或连接第三方平台**。AI 提示词需要使用者自己复制到其选择的工具，审稿、授权、发布与客户沟通由商家负责。

## 项目目录

```text
local-business-ai-growth-handbook/
├── README.md / START-HERE.md / PUBLISH.md / LICENSE
├── index.html?                     # 生成到 _site/index.html
├── data/content.json              # 26章、30天、18提示词、6案例的唯一内容源
├── assets/style.css               # 苹果风响应式设计
├── assets/app.js                  # 本地进度、筛选、测算、复制
├── assets/social-preview.svg      # 开源宣传图
├── scripts/build.py               # 无第三方依赖的静态站构建
├── tests/                        # 数据、链接、隐私与计算测试
├── templates/                    # 12份CSV空白模板
├── docs/                         # 官方资料、发布门禁、执行指南
├── examples/                     # 匿名汽车服务示例
├── .github/workflows/pages.yml   # 验证通过后自动发布 GitHub Pages
└── _site/                         # 本地生成网站，可离线阅读
```

## 广告与服务入口（明确披露）

> **广告 · 作者商业服务**
>
> 通用方法完全免费开放；如果你希望围绕自己门店做方案、搭建内容生产和线索承接，可以了解 [星觉科技企业 AI+IP 获客服务](https://metaver.vip/services)，访问 [星觉科技官网](https://www.a6no1.cn/) 或 [AI 酋长 Andy 官网](https://metaver.vip/)。业务微信：**`AIPMAndy`**（请备注“本地生意”）。

网站的首屏路线区、课程侧栏、首页末尾、页脚均有清晰标注的商业入口；**购买服务不是使用免费课程的前提**。

## 真实案例与隐私边界

- **家庭生意**：只使用匿名的“家人长期从事实体汽车服务”这一行业场景。绝不公开具体位置、店名、亲属身份、客户规模、客户资料、车牌、营业数据、合同价格或故事中可反向定位的细节。
- **其他案例**：全部标注“合成教学场景”，不得被转载为实际成交效果。
- **表格中的数字**：空白为主；网站测算器默认值只是教学假设，不是商家成绩或行业基准。
- **使用数据**：网页中的进度勾选和门店体检状态只保存在浏览器 localStorage；测算在浏览器本地进行。没有服务器、账号体系或远程数据收集。
- **传播**：真实顾客肖像、声音、聊天、车牌、住址等须取得必要授权或脱敏，严禁编造评价和收入证明。

## 官方资料与平台边界

**地图基础信息**：高德商家开放平台、百度地图商户中心；**点评和生活服务**：大众点评商家入驻、抖音来客应用官方说明。不同城市、行业和类目的入驻资质、收费、权益可能不同，平台的当前官方要求优先于本教程。官方网址和适用范围在 [`docs/SOURCES.md`](docs/SOURCES.md)。

平台算法不承诺自然曝光；关注数、播放量、咨询和成交不是同一个概念。增收、降本、效果均须以真实订单和新增贡献核实；不提供买评、刷榜、批量骚扰或绕过平台风控的操作方案。

## 发布

看 [`PUBLISH.md`](PUBLISH.md)，也可在安装 GitHub CLI 且确认无同名远程仓库时运行 `bash scripts/publish.sh`。推广素材在 [`docs/PROMOTION.md`](docs/PROMOTION.md)。 ：本地验证 → 创建 Public 仓库 → 推送源码 → GitHub Pages 选 GitHub Actions → 等待部署 → 实际打开手机和桌面网页核验。**不能把“代码准备好”或“Actions通过”说成“线上已验收”。**

## 授权

原创代码与原创文字采用 MIT License；链接的第三方官方页面、他人标识、第三方素材不因此取得再授权。引用请注明原作者，分享服务案例请遵守隐私与广告规则。
