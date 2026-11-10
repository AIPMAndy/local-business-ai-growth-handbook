#!/usr/bin/env python3
"""Build dependency-free static site from data/content.json; supports subpath GitHub Pages."""
from __future__ import annotations
from html import escape as E
from pathlib import Path
import json, shutil, sys, re
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_site'
D=json.loads((ROOT/'data/content.json').read_text(encoding='utf-8'))
REPO='https://github.com/AIPMAndy/local-business-ai-growth-handbook'
SITE='https://aipmandy.github.io/local-business-ai-growth-handbook/'
SERVICE='https://metaver.vip/services'
HOME='https://metaver.vip/'
CORP='https://www.a6no1.cn/'
phases=['定位','经营','需求','发现','内容','AI生产','生产','转化','成交','复购','数据','规模化','风险']
def h(s):return E(str(s),quote=True)
def link(path,depth=0):return ('../'*depth)+path

def label(s):return f'<span class="eyebrow">{h(s)}</span>'
def badge(s):return f'<span class="tag">{h(s)}</span>'
def brand_card(compact=False):
    text='企业 AI + IP 获客｜把专业经验变成咨询与成交' if not compact else '让真实的本地生意，被更多需要的人找到。'
    return f'''<aside class="ad-panel" aria-label="广告：作者的商业服务"><div><div class="ad-kicker">广告 · 作者商业服务</div><h3>星觉科技 · 企业 AI + IP 获客</h3><p>{h(text)}。免费手册教通用方法；如需定制诊断与落地协助，可进一步沟通。</p><div class="ad-links"><a href="{SERVICE}" target="_blank" rel="noopener noreferrer">查看企业获客服务 ↗</a><a href="{CORP}" target="_blank" rel="noopener noreferrer">星觉科技官网 ↗</a><a href="{HOME}" target="_blank" rel="noopener noreferrer">AI 酋长 Andy 官网 ↗</a><button type="button" class="copy" data-copy="AIPMAndy">复制作者微信 AIPMAndy</button></div></div></aside>'''
def nav(depth=0,active=''):
    entries=[('index.html','首页'),('plan.html','30天计划'),('tools.html','测算工具'),('prompts.html','AI 提示词'),('scripts.html','口播脚本'),('cases.html','行业案例'),('sources.html','官方来源')]
    items=''.join(f'<a class="{"active" if active==u else ""}" href="{link(u,depth)}">{h(t)}</a>' for u,t in entries)
    return f'<header class="top"><div class="container nav-inner"><a href="{link("index.html",depth)}" class="logo"><span class="logo-emblem">A</span><span>LOCAL <strong>GROWTH</strong><small>AI · PLAYBOOK</small></span></a><nav aria-label="主导航">{items}</nav><a class="top-cta" href="{SERVICE}" target="_blank" rel="noopener noreferrer">企业服务 ↗</a></div></header>'
def foot(depth=0):
    return f'''<footer class="footer"><div class="container footer-grid"><div><strong>AI 酋长 Andy</strong><p>本地生意 AI 获客保姆级攻略 · 免费开源<br>先修好生意链路，再用 AI 提效。</p><small>© 2026 AI 酋长 Andy · MIT · 版本 {h(D['version'])} · 更新 {h(D['updated'])}</small></div><div class="footlinks"><a href="{link('privacy.html',depth)}">隐私与数据边界</a><a href="{link('sources.html',depth)}">官方来源</a><a href="{REPO}" target="_blank" rel="noopener noreferrer">GitHub 仓库</a><a href="{HOME}" target="_blank" rel="noopener noreferrer">作者官网</a></div><div><span class="foot-ad">广告 · 作者商业服务</span><p><a href="{SERVICE}" target="_blank" rel="noopener noreferrer">企业 AI+IP 获客咨询</a></p><p><a href="{CORP}" target="_blank" rel="noopener noreferrer">星觉科技</a></p><p>微信：<button class="text-button copy" data-copy="AIPMAndy">AIPMAndy（复制）</button></p></div></div></footer>'''
def page(title,desc,content,filename,depth=0,active='',js=True):
    path=filename
    canonical=SITE+path
    head=f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#fafbfe"><meta name="description" content="{h(desc)}"><meta property="og:title" content="{h(title)}"><meta property="og:description" content="{h(desc)}"><meta property="og:type" content="website"><meta property="og:image" content="{SITE}assets/social-preview.svg"><link rel="canonical" href="{h(canonical)}"><link rel="icon" type="image/svg+xml" href="{link('assets/favicon.svg',depth)}"><link rel="stylesheet" href="{link('assets/style.css',depth)}"><title>{h(title)} · 本地生意 AI 获客保姆级攻略</title><script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@type':'WebPage','name':title,'description':desc,'author':{'@type':'Person','name':'AI 酋长 Andy'},'isPartOf':{'@type':'CreativeWork','name':'本地生意 AI 获客保姆级攻略'}},ensure_ascii=False)}</script></head>'''
    script=f'<script defer src="{link("assets/app.js",depth)}"></script>' if js else ''
    return head+f'<body>{nav(depth,active)}<main>{content}</main>{foot(depth)}<div id="toast" role="status" aria-live="polite"></div>{script}</body></html>'
def card(ch,depth=0):
    return f'''<a class="chapter-card" data-search="{h((ch['title']+' '+ch['phase']+' '+ch['goal']).lower())}" href="{link('chapters/'+ch['id']+'.html',depth)}"><div class="chapter-top">{badge(ch['phase'])}<span class="num">{ch['id']}</span></div><h3>{h(ch['title'])}</h3><p>{h(ch['goal'])}</p><div class="card-cta">打开保姆级步骤 <span>↗</span></div></a>'''
def titleblock(kicker,title,subtitle):return f'<div class="section-title">{label(kicker)}<h1>{h(title)}</h1><p class="lead">{h(subtitle)}</p></div>'

def homepage():
    hero=f'''<section class="hero"><div class="container hero-grid"><div><div class="status-line"><span class="dot"></span>免费开源 · 2026 年版 · 从 0 到真实咨询</div><h1>附近有客户，<br><em>为什么找不到你？</em></h1><p class="hero-lead">不是教你“每天发十条视频”，而是把一家实体店从<strong>被发现、被信任、被咨询、被预约、到店、成交到复购</strong>整条链路打通。AI 负责提效，结果靠真实记录验证。</p><div class="hero-actions"><a class="btn primary" href="plan.html">从第 1 天开始 <span>→</span></a><a class="btn secondary" href="tools.html">测算一笔客值 <span>↗</span></a></div><div class="hero-sub"><span>26 章步骤</span><span>30 天执行</span><span>24 条口播</span><span>18 套提示词</span></div></div><div class="hero-art" role="img" aria-label="从本地发现到成交复购的增长路径"><div class="art-grid"></div><span class="art-label">LOCAL BUSINESS / AI GROWTH</span><div class="funnel-flow"><div><span class="flow-icon">◎</span><b>被附近客户找到</b><small>地图与平台</small></div><span class="flow-arrow">↓</span><div><span class="flow-icon">✦</span><b>看到专业与信任</b><small>真实内容与口碑</small></div><span class="flow-arrow">↓</span><div><span class="flow-icon">◇</span><b>咨询 · 到店 · 成交</b><small>透明服务与数据</small></div></div><div class="art-metric">不承诺流量。<strong>只验证真实生意。</strong></div></div></div></section>'''
    funnel=''.join(f'<div class="step-flow"><span>{str(i+1).zfill(2)}</span><strong>{t}</strong><small>{s}</small></div>' for i,(t,s) in enumerate([('发现','地图与本地搜索'),('信任','口碑与专业内容'),('咨询','明确问题与范围'),('到店','预约与交付'),('成交','净贡献与体验'),('复购','持续服务关系')]))
    route=''.join(f'<a class="route-item" href="chapters/{idx}.html"><span>{n}</span><strong>{t}</strong><small>{s}</small><span class="route-arrow">↗</span></a>' for n,idx,t,s in [('01','03','先做诊断','知道问题在哪里'),('02','06','让附近人找到','高德/百度/点评'),('03','14','AI做30个选题','客户原话出发'),('04','19','承接有效咨询','不只要点赞'),('05','23','算清楚真实回报','订单和利润说话')])
    topics=''.join(card(ch) for ch in D['chapters'])
    return hero+f'''<section class="section container"><div class="section-header">{label('FIRST PRINCIPLES')}<h2>每一步都要回到真实生意。</h2><p>没有成交链路，单纯增加浏览量只是在制造忙碌。</p></div><div class="funnel-strip">{funnel}</div></section><section class="section soft-bg"><div class="container split"><div>{label('QUICK START')}<h2>新手直接走这 5 步。</h2><p class="muted">每一步都有可交付的凭证。你做完了才算通过，而不是“看懂了就算会”。</p>{brand_card(True)}</div><div class="route-list">{route}</div></div></section><section class="section container" id="chapters"><div class="section-header">{label('THE FIELD MANUAL')}<h2>26 章，从开店到复购。</h2><p>教程不是灵感清单，而是可以逐项验收的操作手册。</p></div><div class="filter-line"><input id="chapterSearch" type="search" placeholder="搜索：地图、抖音、复购、毛利、AI…" aria-label="搜索章节"><span id="resultCount" aria-live="polite">26 章</span></div><div class="chapter-grid" id="chapterGrid">{topics}</div></section><section class="section soft-bg"><div class="container"><div class="section-header">{label('GET STARTED')}<h2>工具、案例、模板直接拿走。</h2></div><div class="feature-grid"><a href="plan.html"><span>↗</span><h3>30天执行清单</h3><p>每天只做一件重要事，自动记录勾选进度。</p></a><a href="tools.html"><span>↗</span><h3>获客贡献测算器</h3><p>输入你自己的真实数据，算净贡献而非空喊收入。</p></a><a href="prompts.html"><span>↗</span><h3>18套可复制提示词</h3><p>定位、地图、拍摄、回复、风控直接复制使用。</p></a><a href="scripts.html"><span>↗</span><h3>24条口播脚本</h3><p>从真实问题出发，替换为你自己可证明的素材。</p></a><a href="cases.html"><span>↗</span><h3>6个行业场景</h3><p>匿名经验和模拟教学分级。</p></a></div></div></section><section class="section container"><div class="section-header">{label('A NOTE ON PRIVACY')}<h2>家庭生意，只讲方法，不晒隐私。</h2><p>项目包含一个匿名汽车服务业场景，不披露具体门店、城市、个人信息、客户资料、合同、收入或可反向识别的细节。</p></div>{brand_card()}</section>'''

def chapter(ch):
    num=int(ch['id']); before=D['chapters'][num-2] if num>1 else None;after=D['chapters'][num] if num<len(D['chapters']) else None
    steps=''.join(f'<article class="action-card"><div class="action-number">{s["n"]:02}</div><div><h3>{h(s["action"])}</h3><p>完成标准：{h(s["check"])}</p></div></article>' for s in ch['steps'])
    prs=''.join(f'<li><a href="../prompts.html">复制提示词模板 {i+1}</a></li>' for i in range(0,1))
    pn=(f'<a href="{before["id"]}.html">← {h(before["title"])}</a>' if before else '<a href="../index.html#chapters">← 返回章节列表</a>')
    nn=(f'<a href="{after["id"]}.html">{h(after["title"])} →</a>' if after else '<a href="../plan.html">去做30天计划 →</a>')
    return f'''<div class="container page-pad"><div class="breadcrumb"><a href="../index.html">首页</a> / <a href="../index.html#chapters">课程</a> / 第{ch['id']}章</div><section class="article-hero">{label(ch['phase']+' · 保姆级实操')}<h1>{h(ch['title'])}</h1><p>{h(ch['goal'])}</p><div class="article-tags">{badge('4步内实操')}{badge('真实凭证验收')}{badge('免费开源')}</div></section><div class="article-layout"><article><div class="section-sub"><h2>照着做，一步一步来</h2><p>每完成一步，请保存截图、表格或客户实际反馈。以下动作可能需要你到官方商家后台操作，本网站不会索取账号密码。</p></div><div class="action-list">{steps}</div><div class="note warn"><strong>容易踩的坑</strong><p>{h(ch['warning'])}</p></div><div class="note success"><strong>本章交付物</strong><p>{h(ch['proof'])}</p><button class="btn tiny outline toggle-done" data-key="chapter-{ch['id']}">标记本章完成 ✓</button></div><div class="chapter-nav">{pn}{nn}</div></article><aside class="article-aside"><div class="aside-box"><small>CHAPTER {ch['id']}/26</small><h3>先完成，再继续</h3><p>阅读不算完成。把证据留在你自己控制的本地表格里。</p><a href="../plan.html">查看30天计划 ↗</a><a href="../prompts.html">AI 提示词库 ↗</a><a href="../tools.html">测算工具 ↗</a></div>{brand_card(True)}</aside></div></div>'''

def planpage():
    weeks=['摸清生意','修好可发现性','做出真实内容','承接咨询与复购','完成复盘']
    chunks=[]
    for j in range(0,30,7):
        sub=D['plan'][j:j+7]
        rows=''.join(f'''<label class="day-row"><input type="checkbox" data-day="{x['day']}"><span class="day-num">DAY {x['day']:02}</span><span class="day-body"><strong>{h(x['task'])}</strong><small>{h(x['action'])}</small><em>完成凭证：{h(x['proof'])}</em></span></label>''' for x in sub)
        chunks.append(f'<section class="week-block"><div class="week-heading"><h2>第{j//7+1}周 · {h(weeks[j//7])}</h2><small>{j+1}—{min(j+7,30)}天</small></div>{rows}</section>')
    return f'''<div class="container page-pad">{titleblock('30 DAYS / ONE ACTION EACH','30天，从0做到第一轮复盘。','每天一件事。每一步留凭证。打勾数据只保存在当前浏览器，可导出备份。')}<div class="progress-widget"><div><span class="eyebrow">YOUR PROGRESS</span><strong id="doneCount">0 / 30</strong></div><div class="progress-track"><i id="progressBar"></i></div><div class="progress-actions"><button type="button" class="btn tiny outline" id="exportProgress">导出进度 JSON</button><label class="btn tiny outline file-label">导入进度 JSON<input type="file" id="importProgress" accept=".json,application/json" hidden></label><button type="button" class="btn tiny texty" id="resetProgress">清空勾选</button></div></div><div class="plan-list">{''.join(chunks)}</div>{brand_card()}</div>'''

def tools():
    form='''<div class="calc-grid"><label>每笔真实实收（元）<input type="number" id="revenue" min="0" step="0.01" value="400"></label><label>单笔变动成本（元）<input type="number" id="variable" min="0" step="0.01" value="120"></label><label>每条线索获客成本（元）<input type="number" id="cpl" min="0" step="0.01" value="25"></label><label>本月合格咨询（条）<input type="number" id="leads" min="0" step="1" value="30"></label><label>到店数（次）<input type="number" id="visits" min="0" step="1" value="15"></label><label>实际成交（单）<input type="number" id="orders" min="0" step="1" value="6"></label><label>其他固定新增营销费（元）<input type="number" id="fixed" min="0" step="0.01" value="0"></label><label>新增营销人力工时（小时）<input type="number" id="hours" min="0" step="0.1" value="6"></label><label>每小时新增人力成本（元）<input type="number" id="hourly" min="0" step="0.01" value="35"></label></div><p class="calc-disclaimer">默认数字均为<strong>教学假设</strong>，不是行业平均和任何真实门店的成绩。请替换为自己的记录。测算未含房租等既有固定成本，也不代表会计净利润。</p><div id="calcErrors" aria-live="polite"></div><div class="metrics" aria-live="polite"><div><small>单笔贡献毛利</small><strong id="unitContribution">—</strong></div><div><small>获客线索 → 成交率</small><strong id="conv">—</strong></div><div><small>本期新增净贡献</small><strong id="net">—</strong></div><div><small>每单新增获客总成本</small><strong id="cac">—</strong></div></div><p id="calcInsight" class="hint"></p><button type="button" class="btn secondary" id="exportCalc">导出测算说明 TXT ↗</button>'''
    checks=[('能在高德找到店','amap'),('能在百度地图找到店','baidu'),('地址/营业时间正确','hours'),('有可信的门头与服务图片','images'),('价格边界可读','pricing'),('真实客户问题至少10条','questions'),('有至少3条可证明内容','content'),('主页3步内能咨询','entry'),('有线索来源台账','tracking'),('有权限/隐私检查','privacy')]
    checklist=''.join(f'<label class="audit-row"><input type="checkbox" data-audit="{k}"><span>{h(t)}</span></label>' for t,k in checks)
    return f'''<div class="container page-pad">{titleblock('MEASURE, NOT GUESS','先测算，再花钱。','不看单条爆款带来多少“可能收入”；只用你输入的订单数据算边际贡献。')}<section class="tool-card"><div class="section-header compact"><h2>获客与利润测算器</h2><p>计算公式公开可复核：净贡献 = 订单 × (实收 - 变动成本) - 线索 × 单条获客成本 - 额外推广费 - 新增人力成本。</p></div>{form}</section><section class="tool-card"><div class="section-header compact"><h2>门店 10 项体检</h2><p>完成后建议优先修复最影响真实咨询的断点，而非盲目增加内容数量。</p></div><div class="audit-grid">{checklist}</div><div class="audit-score">已通过 <strong id="auditCount">0 / 10</strong></div></section>{brand_card()}</div>'''

def promptpage():
    cards=''.join(f'''<article class="prompt-card"><div class="prompt-head"><span class="eyebrow">PROMPT {h(x['id'])}</span><button type="button" class="btn tiny outline copy" data-copy-target="prompt-{h(x['id'])}">复制提示词</button></div><h2>{h(x['title'])}</h2><pre id="prompt-{h(x['id'])}">{h(x['body'])}</pre></article>''' for x in D['prompts'])
    return f'<div class="container page-pad">{titleblock("18 COPY-READY PROMPTS","直接复制，不用重新学提示词。","给 AI 的必须是真实、经过脱敏的事实。所有输出都需要人工审核。") }<div class="prompt-grid">{cards}</div>{brand_card()}</div>'

def scriptpage():
    items=[]
    for x in D['scripts']:
        text=f"{x['hook']}\n\n{x['body']}\n\n{x['ending']}"
        items.append(f'''<article class="prompt-card"><div class="prompt-head">{badge(x['industry'])}<button type="button" class="btn tiny outline copy" data-copy-target="script-{x['id']}">复制脚本</button></div><h2>{h(x['title'])}</h2><pre id="script-{x['id']}">{h(text)}</pre><p class="script-evidence">发布前必须补的真实证据：{h(x['evidence'])}</p></article>''')
    return f'<div class="container page-pad">{titleblock("24 SHORT VIDEO STARTERS","24条能直接改写的同城口播。","覆盖通用门店、汽车服务、餐饮、美业、家电维修、零售和运动服务。全部是公开教学范例，不是发生过的真实客户故事。") }<div class="note warn"><strong>先补事实，再发视频</strong><p>每条脚本的【方括号】都必须换成实际可证明的资料；没有证据则删去。不能把教学样稿说成真实经营案例。</p></div><div class="prompt-grid">{"".join(items)}</div>{brand_card()}</div>'

def casespage():
    cas=[]
    for j,x in enumerate(D['cases'],1):
        acts=''.join(f'<li>{h(t)}</li>' for t in x['action'])
        cas.append(f'''<article class="case-card"><div class="case-head">{badge(x['tag'])}<span>CASE {j:02}</span></div><h2>{h(x['title'])}</h2><p class="case-type">{h(x['type'])}</p><p>{h(x['context'])}</p><div class="case-section"><strong>客户卡在哪里</strong><p>{h(x['problem'])}</p></div><div class="case-section"><strong>建议的逐步动作</strong><ol>{acts}</ol></div><div class="case-section"><strong>怎么判断有效</strong><p>{h(x['measure'])}</p></div><div class="case-status">证据状态：{h(x['status'])}</div></article>''')
    return f'<div class="container page-pad">{titleblock("CASE LIBRARY / EVIDENCE FIRST","案例可以匿名，数据不能乱编。","一个匿名家庭行业场景 + 五个明确标注的教学模拟。这里只讲方法，没有声称任何一家店已靠教程取得商业成绩。") }<div class="case-grid">{"".join(cas)}</div>{brand_card()}</div>'

def sourcepage():
    cards=''.join(f'<article class="source-card"><h2>{h(x["name"])}</h2><p>{h(x["supports"])}</p><a href="{h(x["url"])}" target="_blank" rel="noopener noreferrer">官方页面 ↗</a></article>' for x in D['sources'])
    return f'<div class="container page-pad">{titleblock("PRIMARY SOURCES","只给可核查的官方入口。","已核对公开官方页面或应用商店官方说明；具体资质、收费和后台字段以平台当前规则为准。") }<div class="sources-grid">{cards}</div><div class="note warn"><strong>权威边界</strong><p>教程中的 ROI 模型、内容方法、30 天计划是作者提出的实践框架，并非平台官方承诺。任何平台的算法、入驻门槛和收费都可能变化；广告内容必须可辨识且真实。</p></div></div>'

def privacy():
    return f'''<div class="container page-pad">{titleblock('PRIVACY BY DESIGN','这份教程不需要知道你是谁。','保姆级项目提供方法、模板和计算器；不会收集你的客户名单或经营后台。')}<div class="prose"><h2>公开案例做了哪些处理？</h2><p>有一个“家人从事汽车服务”的匿名化场景，仅保留行业层面的运营问题，不暴露店名、地址、所在城市、亲属身份、时间线、客户数量、车牌、客户数据、营收或可反向识别的经营特征。其他五个案例均为模拟教学。</p><h2>哪些东西绝不能上传公开仓库？</h2><p>客户姓名和手机号、聊天原文、家庭住址、身份证和营业执照扫描件、车牌、精确定位信息、店铺后台截图、合同和未公开的经营账目。示例 CSV 只包含合成样例与空白项。</p><h2>工具如何处理数据？</h2><p>进度勾选与店铺体检状态只保存在当前浏览器的 localStorage，不传至服务器。获客测算器仅在浏览器内计算；导出文件由你自行保管。若开启浏览器的跨设备同步或使用公共电脑，请自行控制隐私风险。</p><h2>如何合规使用 AI？</h2><p>上传任何文本前先脱敏。所有图片应确认肖像权与素材授权。不得编造评价、成交额、专业资质或维修结论。公开服务宣传遵守广告规则，平台入驻需要的敏感证件仅提交至核实过的官方后台。</p><h2>作者的广告如何区分？</h2><p>本项目的星觉科技服务链接均标记为“广告 · 作者商业服务”，与免费教程正文区分。免费开源内容无需购买服务即可使用。</p></div>{brand_card()}</div>'''

def build():
    if OUT.exists():shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    for p in ['assets/style.css','assets/app.js','assets/favicon.svg','assets/social-preview.svg']:
        t=OUT/p;t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/p,t)
    pages={
        'index.html':page('免费教程首页','附近的客户如何找到你的实体店？26章、30天、AI提示词、行业案例、线索与利润测算。',homepage(),'index.html',active='index.html'),
        'plan.html':page('30天执行计划','每天一件事，完成本地生意 AI 获客最小闭环。',planpage(),'plan.html',active='plan.html'),
        'tools.html':page('获客利润与门店诊断工具','本地生意真实订单净贡献计算器与10项门店体检。',tools(),'tools.html',active='tools.html'),
        'scripts.html':page('24条同城门店口播脚本','24条按行业分类的实体店视频口播示例，含真实证据要求。',scriptpage(),'scripts.html',active='scripts.html'),
        'prompts.html':page('18套AI提示词','本地商家可复制提示词：地图、短视频、咨询、复购、匿名化。',promptpage(),'prompts.html',active='prompts.html'),
        'cases.html':page('六类本地生意教学案例','汽车维修、餐饮、美业、家电维修、洗衣护理、健身的匿名/模拟场景。',casespage(),'cases.html',active='cases.html'),
        'sources.html':page('官方资料来源','高德地图、百度地图、大众点评、抖音来客与互联网广告管理官方参考。',sourcepage(),'sources.html',active='sources.html'),
        'privacy.html':page('隐私与数据保护','如何使用匿名化案例与脱敏资料做本地生意 AI 获客。',privacy(),'privacy.html')}
    for ch in D['chapters']:
        name='chapters/'+ch['id']+'.html'
        pages[name]=page(ch['title'],ch['goal'],chapter(ch),name,depth=1)
    for filename,html in pages.items():
        p=OUT/filename;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(html,encoding='utf-8')
    # Machine-readable content is bundled for transparent reuse; no private client data.
    shutil.copy2(ROOT/'data/content.json',OUT/'content.json')
    from xml.sax.saxutils import escape as X
    urls=''.join(f'<url><loc>{X(SITE+name)}</loc><lastmod>{D["updated"]}</lastmod></url>' for name in pages)
    (OUT/'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>',encoding='utf-8')
    (OUT/'.nojekyll').write_text('',encoding='utf-8')
    (OUT/'404.html').write_text(pages['index.html'],encoding='utf-8')
    print(f'Built {len(pages)} content pages +404; output={OUT}')
if __name__=='__main__':build()
