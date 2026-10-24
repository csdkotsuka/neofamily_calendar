import json, urllib.request, re, html, time
from urllib.parse import urlparse

candidates = [
    {
        "cand_id": "c1",
        "date": "2026-10-22 12:55",
        "reporter": "小野八音（yaShine）",
        "reason": "",
        "url": "https://www.instagram.com/kanrieiyoushi_metas?obrf=MXd0NXk3Y214Nzk1OQ==",
        "secondary_url": "",
        "platform": "Instagram",
        "image": "Screenshot 2026-10-24 at 15.12.15.png"
    },
    {
        "cand_id": "c2",
        "date": "2026-10-22 15:52",
        "reporter": "後藤広代（Lumiere.）",
        "reason": "",
        "url": "https://www.threads.com/share/BBsMFS1cFy/",
        "secondary_url": "https://www.threads.com/@kk_kasuga",
        "platform": "Threads",
        "image": "Screenshot 2026-10-24 at 15.12.15.png"
    },
    {
        "cand_id": "c3",
        "date": "2026-10-22 15:53",
        "reporter": "後藤広代（Lumiere.）",
        "reason": "",
        "url": "https://www.threads.com/share/BAa9M0zjs6/",
        "secondary_url": "https://www.threads.com/@yu.chuzai.mama",
        "platform": "Threads",
        "image": "Screenshot 2026-10-24 at 15.12.15.png"
    },
    {
        "cand_id": "c4",
        "date": "2026-10-22 16:26",
        "reporter": "小西みゆき（Mimola）",
        "reason": "自分でコミュニティ作ってるので大丈夫だそうです",
        "url": "https://www.instagram.com/baby_growth_japan?cplk=MnVqMWRmYjFydzlw",
        "secondary_url": "",
        "platform": "Instagram",
        "image": "Screenshot 2026-10-24 at 15.12.08.png"
    },
    {
        "cand_id": "c5",
        "date": "2026-10-22 17:17",
        "reporter": "服部達典（MURA）",
        "reason": "",
        "url": "https://www.instagram.com/herb_nemokoro?cplk=ZzImaWpucHFqMHEx",
        "secondary_url": "",
        "platform": "Instagram",
        "image": "Screenshot 2026-10-24 at 15.12.08.png"
    },
    {
        "cand_id": "c6",
        "date": "2026-10-22 17:24",
        "reporter": "井峯明香奈（shAdow）",
        "reason": "",
        "url": "https://www.threads.com/@1123.love.1123?igshid=NTc4MTIwNjQ2YQ==",
        "secondary_url": "",
        "platform": "Threads",
        "image": "Screenshot 2026-10-24 at 15.12.08.png"
    },
    {
        "cand_id": "c7",
        "date": "2026-10-22 17:49",
        "reporter": "後藤広代（Lumiere.）",
        "reason": "",
        "url": "https://www.threads.com/@kento12ap",
        "secondary_url": "",
        "platform": "Threads",
        "image": "Screenshot 2026-10-24 at 15.12.08.png"
    },
    {
        "cand_id": "c8",
        "date": "2026-10-22 18:52",
        "reporter": "菅野美穂（Couleur理事長）",
        "reason": "",
        "url": "https://www.threads.com/@chi_e_biyou",
        "secondary_url": "",
        "platform": "Threads",
        "image": "Screenshot 2026-10-24 at 15.12.08.png"
    },
    {
        "cand_id": "c10",
        "date": "2026-10-22 21:56",
        "reporter": "小西みゆき（Mimola）",
        "reason": "",
        "url": "https://www.instagram.com/caco.kosodate",
        "secondary_url": "",
        "platform": "Instagram",
        "image": "Screenshot 2026-10-24 at 15.12.08.png"
    },
    {
        "cand_id": "c11",
        "date": "2026-10-22 21:57",
        "reporter": "小西みゆき（Mimola）",
        "reason": "DM送ったら非公開になりました",
        "url": "https://www.instagram.com/m.baby_mama.23",
        "secondary_url": "",
        "platform": "Instagram",
        "image": "Screenshot 2026-10-24 at 15.12.08.png"
    },
    {
        "cand_id": "c12_a",
        "date": "2026-10-23 05:08",
        "reporter": "服部達典（MURA）",
        "reason": "",
        "url": "https://www.instagram.com/kosodatemama0524?rpxt=YmxrZ2RpcDMxbjc1",
        "secondary_url": "",
        "platform": "Instagram",
        "image": "Screenshot 2026-10-24 at 15.12.02.png"
    },
    {
        "cand_id": "c12_b",
        "date": "2026-10-23 05:08",
        "reporter": "服部達典（MURA）",
        "reason": "",
        "url": "https://www.instagram.com/cherilu_yn?mdxt=bGlqMDhmbjJ0czRu",
        "secondary_url": "",
        "platform": "Instagram",
        "image": "Screenshot 2026-10-24 at 15.12.02.png"
    },
    {
        "cand_id": "c12_d",
        "date": "2026-10-23 05:08",
        "reporter": "服部達典（MURA）",
        "reason": "",
        "url": "https://www.instagram.com/romy.yade?exln=ajdhcnYxYmx5Nmsx",
        "secondary_url": "",
        "platform": "Instagram",
        "image": "Screenshot 2026-10-24 at 15.12.02.png"
    },
    {
        "cand_id": "c14",
        "date": "2026-10-23 08:49",
        "reporter": "齊藤唯（Mimola）",
        "reason": "",
        "url": "https://www.threads.com/@magier_2023?igshid=NTc4MTIwNjQ2YQ==",
        "secondary_url": "",
        "platform": "Threads",
        "image": "Screenshot 2026-10-24 at 15.12.02.png"
    },
    {
        "cand_id": "c15",
        "date": "2026-10-23 09:28",
        "reporter": "森崎江里（RAYTUS / 愛知県）",
        "reason": "誰かのやりとり、スクショで晒されてます💦 コメントのやつも報告とブロックお願いします",
        "url": "https://www.threads.com/@rina.s0527",
        "secondary_url": "",
        "platform": "Threads",
        "image": "Screenshot 2026-10-24 at 15.12.02.png"
    },
    {
        "cand_id": "c19",
        "date": "2026-10-23 15:09",
        "reporter": "畑ゆかり（yuima-ru理事長）",
        "reason": "ぶった斬り会長・・・名指しでした",
        "url": "https://www.threads.com/@matsunaga__haruna?igshid=NTc4MTIwNjQ2YQ==",
        "secondary_url": "",
        "platform": "Threads",
        "image": "Screenshot 2026-10-24 at 15.11.56.png"
    },
    {
        "cand_id": "c20",
        "date": "2026-10-23 17:43",
        "reporter": "井峯明香奈（shAdow）",
        "reason": "",
        "url": "https://www.threads.com/@yokoyama_ibaraki?igshid=NTc4MTIwNjQ2YQ==",
        "secondary_url": "",
        "platform": "Threads",
        "image": "Screenshot 2026-10-24 at 15.11.56.png"
    },
    {
        "cand_id": "c21",
        "date": "2026-10-23 19:54",
        "reporter": "城間千聖（enLIGHT）",
        "reason": "",
        "url": "https://www.instagram.com/artmake_momoka?exln=b29zenR2cjUyYXB1bHs=",
        "secondary_url": "",
        "platform": "Instagram",
        "image": "Screenshot 2026-10-24 at 15.11.56.png"
    },
    {
        "cand_id": "c22",
        "date": "2026-10-23 20:42",
        "reporter": "岩﨑七菜子（tEaM_S.）",
        "reason": "ファーストして興味あるフリして、なんの断りもなくブロック＆zoom来ずでした",
        "url": "https://www.threads.com/@holitaku_pickleball",
        "secondary_url": "",
        "platform": "Threads",
        "image": "Screenshot 2026-10-24 at 15.11.56.png"
    },
    {
        "cand_id": "c23",
        "date": "2026-10-23 22:37",
        "reporter": "ロジャーズ優衣（enchant+）",
        "reason": "",
        "url": "https://www.threads.com/@poochan5676?igshid=NTc4MTIwNjQ2YQ==",
        "secondary_url": "",
        "platform": "Threads",
        "image": "Screenshot 2026-10-24 at 15.11.56.png"
    },
    {
        "cand_id": "c24",
        "date": "2026-10-23 22:57",
        "reporter": "ロジャーズ優衣（enchant+）",
        "reason": "",
        "url": "https://www.instagram.com/ayumi.reborn?xtok=MXRkZzUwaWIwam5leA==",
        "secondary_url": "",
        "platform": "Instagram",
        "image": "Screenshot 2026-10-24 at 15.11.48.png"
    },
    {
        "cand_id": "c25",
        "date": "2026-10-23 23:34",
        "reporter": "小野八音（yaShine）",
        "reason": "何度もお声かけいただき ZOOMもしてお断りしました、とのことです！",
        "url": "https://www.instagram.com/tomo.ninkatsueiyou?srtk=MWxtYjJ4aWM3bXlodg==",
        "secondary_url": "",
        "platform": "Instagram",
        "image": "Screenshot 2026-10-24 at 15.11.48.png"
    },
    {
        "cand_id": "c26",
        "date": "2026-10-24 01:14",
        "reporter": "桝田和裕（AMATERAS）",
        "reason": "",
        "url": "https://www.threads.com/@nobu491004?igshid=NTc4MTIwNjQ2YQ==",
        "secondary_url": "",
        "platform": "Threads",
        "image": "Screenshot 2026-10-24 at 15.11.48.png"
    },
    {
        "cand_id": "c27",
        "date": "2026-10-24 01:14",
        "reporter": "南藍（tidy.shin代表）",
        "reason": "言っていることに信ぴょう性がなく、マウント取ってくる。",
        "url": "https://www.threads.com/@mochi_creative123?igshid=NTc4MTIwNjQ2YQ==",
        "secondary_url": "",
        "platform": "Threads",
        "image": "Screenshot 2026-10-24 at 15.11.48.png"
    },
    {
        "cand_id": "c28",
        "date": "2026-10-24 10:11",
        "reporter": "城間千聖（enLIGHT）",
        "reason": "何度もお声かけしているようです。Zoom面談をした上でお断りしたそう。",
        "url": "https://www.instagram.com/sato_aoi_photo?psln=MWp5bGtncmZpYTE4OA==",
        "secondary_url": "",
        "platform": "Instagram",
        "image": "Screenshot 2026-10-24 at 15.11.48.png"
    },
    {
        "cand_id": "c29",
        "date": "2026-10-24 10:11",
        "reporter": "ロジャーズ優衣（enchant+）",
        "reason": "向こうからメッセージをいただきましたが、NEOに会うのは3回目だったそうです🙏",
        "url": "https://www.threads.com/@nijirosinkyu?igshid=NTc4MTIwNjQ2YQ==",
        "secondary_url": "https://www.instagram.com/nijirosinkyu?vrfl=MWg3M2oyM25uN2xtYg==",
        "platform": "Threads / Instagram",
        "image": "Screenshot 2026-10-24 at 15.11.48.png"
    },
    {
        "cand_id": "c30",
        "date": "2026-10-24 13:11",
        "reporter": "服部達典（MURA）",
        "reason": "",
        "url": "https://www.instagram.com/mayu_coach.mama?psln=MThpd2lycW5jamo5Mw==",
        "secondary_url": "",
        "platform": "Instagram",
        "image": "Screenshot 2026-10-24 at 15.11.48.png"
    }
]

GENERIC_TITLES = {
    "instagram", "threads", "threads • log in", "facebook",
    "このページを見るには、ログインまたは登録してください",
    "log in or sign up to view", "ログイン • instagram",
    "page not found", "ページが見つかりません", "コンテンツは現在利用できません"
}

def extract_clean_title(raw_title):
    if not raw_title:
        return None
    t = html.unescape(raw_title).strip()
    t = re.sub(r'\s+', ' ', t)
    if t.lower() in GENERIC_TITLES:
        return None
    if "このページを見るには" in t or "ログインまたは登録" in t or "Log in or sign up" in t:
        return None
    m = re.match(r'^(.*?)\s*\(@([A-Za-z0-9._]+)\)\s*[•·|-]\s*(?:Instagram|Threads).*$', t, re.I)
    if m:
        disp = m.group(1).strip()
        handle = m.group(2).strip()
        return disp if disp else f"@{handle}"
    m2 = re.match(r'^@?([A-Za-z0-9._]+)\s*[•·|-]\s*(?:Instagram|Threads).*$', t, re.I)
    if m2:
        return None
    t = re.sub(r'\s*[\|｜•·-]\s*Facebook.*$', '', t, flags=re.I).strip()
    t = re.sub(r'\s*[\|｜•·-]\s*TikTok.*$', '', t, flags=re.I).strip()
    if t.lower() in GENERIC_TITLES:
        return None
    return t

def fetch_url_info(u):
    if not u or not u.startswith("http"):
        return None, None
    for ua in ["facebookexternalhit/1.1", "Twitterbot/1.0"]:
        try:
            req = urllib.request.Request(u, headers={
                "User-Agent": ua,
                "Accept-Language": "ja,en-US;q=0.9,en;q=0.8"
            })
            with urllib.request.urlopen(req, timeout=8) as r:
                final_url = r.geturl()
                body = r.read(98304).decode("utf-8", errors="ignore")
                og = re.search(r'property=["\']og:title["\']\s+content=["\'](.*?)["\']', body, re.I) or \
                     re.search(r'content=["\'](.*?)["\']\s+property=["\']og:title["\']', body, re.I) or \
                     re.search(r'name=["\']twitter:title["\']\s+content=["\'](.*?)["\']', body, re.I)
                t = re.search(r'<title[^>]*>(.*?)</title>', body, re.S | re.I)
                raw = og.group(1) if og else (t.group(1) if t else None)
                cleaned = extract_clean_title(raw)
                return cleaned, final_url
        except Exception as e:
            pass
    return None, None

results = []
for c in candidates:
    print(f"Fetching {c['cand_id']}: {c['url']}")
    t, f_url = fetch_url_info(c["url"])
    if not t and c.get("secondary_url"):
        t, f_url2 = fetch_url_info(c["secondary_url"])
    # If still not found, try alternative platform
    if not t:
        p = urlparse(c["url"])
        path = p.path.strip("/")
        if "instagram.com" in p.netloc and path:
            h = path.split("/")[0]
            alt = f"https://www.threads.net/@{h}"
            alt_t, _ = fetch_url_info(alt)
            if alt_t:
                t = alt_t
        elif "threads." in p.netloc and path.startswith("@"):
            h = path[1:].split("/")[0]
            alt = f"https://www.instagram.com/{h}/"
            alt_t, _ = fetch_url_info(alt)
            if alt_t:
                t = alt_t
    c["fetched_title"] = t
    print(f"   -> Result: {t}")
    results.append(c)

with open("scripts/candidate_titles.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\nDone fetching candidate titles!")
