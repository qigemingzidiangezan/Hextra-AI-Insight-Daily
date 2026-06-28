"""AI Daily News Generator - GitHub Actions edition
Triggered daily via .github/workflows/daily-build.yml
Secrets are passed via environment variables:
  GEMINI_API_KEY - Google Gemini API key
  GH_TOKEN - GitHub Personal Access Token with repo scope
"""
import os, json, re, base64, urllib.request, ssl, sys
from xml.etree import ElementTree as ET
from datetime import datetime, timezone, timedelta

# Read secrets from env
GEMINI_KEY = os.environ.get('GEMINI_API_KEY', '')
GH_TOKEN = os.environ.get('GH_TOKEN', '')
REPO_OWNER = os.environ.get('REPO_OWNER', 'qigemingzidiangezan')
REPO_NAME = os.environ.get('REPO_NAME', 'Hextra-AI-Insight-Daily')
SITE_URL = os.environ.get('SITE_URL', f'https://{REPO_OWNER}.github.io/{REPO_NAME}/')
GITHUB_API = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"

if not GEMINI_KEY:
    print("[ERROR] GEMINI_API_KEY not set")
    sys.exit(1)
if not GH_TOKEN:
    print("[ERROR] GH_TOKEN not set")
    sys.exit(1)

def fetch_url(url, method='GET', data=None, headers_extra=None, timeout=30):
    req = urllib.request.Request(url, method=method)
    if data:
        req.data = data.encode('utf-8') if isinstance(data, str) else data
    if headers_extra:
        for k, v in headers_extra.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f"  Fetch error: {e}")
        return None, None

# Step 1: Fetch RSS feeds
RSS_FEEDS = [
    ('TechCrunch AI', 'https://techcrunch.com/category/artificial-intelligence/feed/'),
    ('The Verge AI', 'https://www.theverge.com/rss/ai-artificial-intelligence/index.xml'),
]

items = []
for name, url in RSS_FEEDS:
    print(f"[FETCH] {name}...")
    status, xml = fetch_url(url)
    if not xml:
        continue
    try:
        root = ET.fromstring(xml)
        elements = root.findall('.//item') + root.findall('.//{http://www.w3.org/2005/Atom}entry')
        for item_elem in elements[:8]:
            title = ''
            link = ''
            desc = ''
            pub_date = ''
            for child in item_elem.iter():
                tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                if tag == 'title':
                    title = (child.text or '').strip()
                elif tag == 'link':
                    link = child.attrib.get('href', '') or (child.text or '').strip()
                elif tag in ('description', 'content', 'summary', 'encoded'):
                    text = (child.text or '').strip()[:500]
                    desc = re.sub(r'<[^>]*>', '', text)
                elif tag in ('pubDate', 'published', 'updated'):
                    pub_date = (child.text or '').strip()
            if title and len(title) > 5 and title not in ('TechCrunch', 'The Verge'):
                items.append({'title': title, 'link': link, 'desc': desc, 'date': pub_date, 'source': name})
        print(f"  Parsed {len([i for i in items if i['source'] == name])} items from {name}")
    except Exception as e:
        print(f"  Parse error: {e}")

if not items:
    print("[ERROR] No news items found from any source")
    sys.exit(1)

print(f"  Total: {len(items)} news items")

# Step 2: Build prompt
news_text = '\n\n---\n\n'.join([
    f"新闻{i+1}: {it['title']}\n来源: {it['source']}\n日期: {it.get('date','N/A')}\n链接: {it.get('link','N/A')}\n描述: {it.get('desc','')[:400]}"
    for i, it in enumerate(items[:12])
])

system_instruction = "你是一个专业的AI科技新闻编辑，擅长撰写简洁专业的中文AI日报。"

prompt = f"""{news_text}

---

请根据以上AI科技新闻，生成一份中文AI日报（Markdown格式），使用以下结构：

## **AI内容摘要**
用一段话总结今日AI领域最重要的动态。

## **AI产品与功能更新**
将重要的AI产品发布、更新、收购等新闻整理成编号列表。每条包含：公司/产品名称用**加粗**、关键信息、emoji表情装饰，末尾附上原文链接。

## **AI前沿研究**
如果有AI论文或研究方面的新闻，单独列出。

## **开源TOP项目**
如果有热门开源AI项目的新闻，单独列出。

要求：用中文撰写，简洁专业，突出重点，每条新闻后须附原文链接。"""

print(f"[AI] Calling Gemini (prompt: {len(prompt)} chars)...")

# Step 3: Call Gemini
gemini_payload = json.dumps({
    "contents": [{"parts": [{"text": prompt}]}],
    "systemInstruction": {"parts": [{"text": system_instruction}]},
    "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.7}
}).encode('utf-8')

status3, gemini_resp = fetch_url(
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}",
    method='POST',
    data=gemini_payload,
    headers_extra={'Content-Type': 'application/json'},
    timeout=90
)

if not gemini_resp:
    print("[ERROR] Gemini API no response")
    sys.exit(1)

gemini_data = json.loads(gemini_resp)
ai_text = gemini_data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')

if not ai_text:
    print(f"[ERROR] Gemini returned empty: {gemini_resp[:300]}")
    sys.exit(1)

print(f"[AI] Generated {len(ai_text)} chars")

# Step 4: Build Hugo markdown
cst = timezone(timedelta(hours=8))
today = datetime.now(cst).strftime('%Y-%m-%d')
year, month, day = today.split('-')
month_dir = f"{year}-{month}"
title_date = f"{year}/{int(month)}/{int(day)}"
link_title = f"{month}-{day} AI日报"

plain_desc = re.sub(r'[#*>`\[\]()!\-|]', '', ai_text)
plain_desc = re.sub(r'\n+', ' ', plain_desc).strip()[:150].replace('"', "'")

header = (
    f'>  `AI 日报` | `早八更新` | `全网数据聚合` | `前沿科学探索` | '
    f'`开源创新力量` | `AI与人类未来` | '
    f'[访问网页版]({SITE_URL})\n\n'
)

hugo_content = f"""---
linkTitle: "{link_title}"
title: "AI资讯日报 {title_date}"
date: {today} 08:00:00
comments: true
description: "{plain_desc}..."
---

{header}
{ai_text}

---

## **收听语音版AI日报**

| 小宇宙 | 抖音 |
| --- | --- |
| [AI情报站](https://www.xiaoyuzhoufm.com/) | [自媒体账号](https://www.douyin.com/) |
"""

file_path = f"content/cn/{month_dir}/{today}.md"
print(f"[COMMIT] {file_path}")

# Step 5: Check existing file SHA
existing_sha = None
s, resp = fetch_url(
    f"{GITHUB_API}/contents/{file_path}?ref=main",
    headers_extra={
        'Authorization': f'Bearer {GH_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'AI-Daily-Bot',
    }
)
if s == 200 and resp:
    try:
        existing_sha = json.loads(resp).get('sha')
        print(f"  Updating existing file")
    except:
        pass

# Step 6: Commit
commit_payload = {
    "message": f"{'Update' if existing_sha else 'Create'} AI daily for {today}",
    "content": base64.b64encode(hugo_content.encode('utf-8')).decode('ascii'),
    "branch": "main",
}
if existing_sha:
    commit_payload["sha"] = existing_sha

s4, resp4 = fetch_url(
    f"{GITHUB_API}/contents/{file_path}",
    method='PUT',
    data=json.dumps(commit_payload),
    headers_extra={
        'Authorization': f'Bearer {GH_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
        'User-Agent': 'AI-Daily-Bot',
    }
)

if s4 in (200, 201):
    print(f"[OK] AI daily published!")
    print(f"  View: https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/main/{file_path}")
else:
    print(f"[ERROR] Commit failed (HTTP {s4}): {resp4[:300] if resp4 else 'no response'}")
    sys.exit(1)

# Step 7: Ensure month _index.md exists
idx_path = f"content/cn/{month_dir}/_index.md"
s5, _ = fetch_url(
    f"{GITHUB_API}/contents/{idx_path}?ref=main",
    headers_extra={
        'Authorization': f'Bearer {GH_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'AI-Daily-Bot',
    }
)
if s5 != 200:
    idx_content = f"""---
title: {year}-{month}
weight: {int(year) * 10000 + int(month)}
breadcrumbs: false
sidebar:
  open: false
---
"""
    fetch_url(
        f"{GITHUB_API}/contents/{idx_path}",
        method='PUT',
        data=json.dumps({
            "message": f"Create month index for {month_dir}",
            "content": base64.b64encode(idx_content.encode('utf-8')).decode('ascii'),
            "branch": "main",
        }),
        headers_extra={
            'Authorization': f'Bearer {GH_TOKEN}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json',
            'User-Agent': 'AI-Daily-Bot',
        }
    )
    print(f"  Created month index")

print(f"[DONE] Pipeline complete!")
