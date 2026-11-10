import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'_site'
DATA=json.loads((ROOT/'data/content.json').read_text(encoding='utf-8'))

class Collector(HTMLParser):
    def __init__(self):super().__init__();self.refs=[];self.ids=[];self.headings=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag in ('a','link','script','img'):
            key='href' if tag in ('a','link') else 'src'
            if d.get(key):self.refs.append(d[key])
        if 'id' in d:self.ids.append(d['id'])
        if tag=='h1':self.headings.append('h1')

class ProjectChecks(unittest.TestCase):
    def test_expected_content(self):
        self.assertEqual(len(DATA['chapters']),26)
        self.assertEqual(len(DATA['plan']),30)
        self.assertEqual(len(DATA['prompts']),18)
        self.assertEqual(len(DATA['cases']),6)
        self.assertEqual(len(DATA['sources']),7)
        self.assertEqual(len(DATA['scripts']),24)
        self.assertEqual([x['id'] for x in DATA['chapters']],[f'{i:02}' for i in range(1,27)])
        self.assertEqual([x['day'] for x in DATA['plan']],list(range(1,31)))
        for c in DATA['chapters']:
            self.assertEqual(len(c['steps']),4,c['title'])
            self.assertGreater(len(c['proof']),3)
            self.assertGreater(len(c['warning']),5)
            for st in c['steps']:self.assertIn('action',st)

    def test_all_html_paths_and_internal_links(self):
        self.assertTrue(SITE.exists(),'run python scripts/build.py first')
        html_files=list(SITE.rglob('*.html'))
        self.assertEqual(len(html_files),35,'34 content pages and 404')
        for p in html_files:
            html=p.read_text(encoding='utf-8')
            col=Collector();col.feed(html)
            self.assertIn('<meta name="viewport"',html,str(p))
            self.assertIn('AIPMAndy',html,str(p))
            self.assertIn('广告 · 作者商业服务',html,str(p))
            self.assertIn('canonical',html,str(p))
            self.assertEqual(len(col.headings),1,str(p))
            for href in col.refs:
                if href.startswith(('http:','https:','mailto:','tel:','data:','#')):continue
                local=(p.parent/href.split('#')[0].split('?')[0]).resolve()
                self.assertTrue(local.is_relative_to(SITE.resolve()),f'path escaped site: {p.name} {href}')
                self.assertTrue(local.exists(),f'broken internal link in {p}: {href}')

    def test_no_private_identifiers_in_public_case(self):
        content=json.dumps(DATA['cases'][0],ensure_ascii=False)
        # Use generic patterns, not private real-life identifiers, in open-source tests.
        self.assertNotRegex(content,r'\b(?:19|20)\d{2}年')
        self.assertNotRegex(content,r'\b1[3-9]\d{9}\b')
        self.assertNotRegex(content,r'[A-Z]{1,2}[A-Z0-9]{5,7}')
        for token in ['车牌号：', '顾客姓名：', '具体住址：', '真实店名：', '经营收入：']:
            self.assertNotIn(token,content)
        self.assertIn('合成',DATA['cases'][1]['type'])
        for c in DATA['cases']:
            self.assertTrue('模拟' in c['status'] or '不披露' in c['status'])

    def test_sources_are_official_and_cited(self):
        for x in DATA['sources']:
            self.assertTrue(x['url'].startswith('https://'))
            self.assertTrue(urlparse(x['url']).hostname)
        main=(SITE/'index.html').read_text(encoding='utf-8')
        for u in ['https://metaver.vip/','https://metaver.vip/services','https://www.a6no1.cn/']:
            self.assertIn(u,main)
        self.assertIn('AIPMAndy',main)

    def test_templates_are_present(self):
        templates=list((ROOT/'templates').glob('*.csv'))
        self.assertEqual(len(templates),12)
        for t in templates:self.assertGreater(t.stat().st_size,20)

    def test_security_guardrails(self):
        code=(ROOT/'assets/app.js').read_text(encoding='utf-8')
        for unsafe in ['fetch(', 'XMLHttpRequest', 'sendBeacon(', 'eval(', 'document.cookie']:
            self.assertNotIn(unsafe,code)
        self.assertIn('广告 · 作者商业服务',(SITE/'index.html').read_text(encoding='utf-8'))
        self.assertIn('localStorage',code)
        self.assertIn('本期新增净贡献',(SITE/'tools.html').read_text(encoding='utf-8'))

if __name__=='__main__':unittest.main()
