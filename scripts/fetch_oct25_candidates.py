import json, urllib.request, re, html, time
from urllib.parse import urlparse

candidates = [
    {
        "id": "cand_1",
        "date": "2026-10-24 16:21",
        "reporter": "服部達典（MURA）",
        "raw_url": "https://www.instagram.com/meina_clo?dirf=MTBZ2x6eXlyeh1OA==",
        "username": "meina_clo",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-25 at 20.34.35.png"
    },
    {
        "id": "cand_2_dup",
        "date": "2026-10-24 16:45",
        "reporter": "井峯明香奈（shAdow）",
        "raw_url": "https://www.threads.com/@naomi_futoukoukids_mama?igshid=NTc4MTIwNjQ2YQ==",
        "username": "naomi_futoukoukids_mama",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-25 at 20.34.35.png",
        "is_dup": True,
        "dup_target": "blk_101"
    },
    {
        "id": "cand_3_dup",
        "date": "2026-10-24 16:47",
        "reporter": "井峯明香奈（shAdow）",
        "raw_url": "https://www.threads.com/@hiroshi_yamauchi_55?igshid=NTc4MTIwNjQ2YQ==",
        "username": "hiroshi_yamauchi_55",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-25 at 20.34.35.png",
        "is_dup": True,
        "dup_target": "blk_189"
    },
    {
        "id": "cand_4",
        "date": "2026-10-24 16:48",
        "reporter": "井峯明香奈（shAdow）",
        "raw_url": "https://www.threads.com/@hirachi_ceo?igshid=NTc4MTIwNjQ2YQ==",
        "username": "hirachi_ceo",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-25 at 20.34.35.png"
    },
    {
        "id": "cand_5",
        "date": "2026-10-24 16:49",
        "reporter": "井峯明香奈（shAdow）",
        "raw_url": "https://www.threads.com/@river_cangoxina?igshid=NTc4MTIwNjQ2YQ==",
        "username": "river_cangoxina",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-25 at 20.34.35.png"
    },
    {
        "id": "cand_6",
        "date": "2026-10-24 21:35",
        "reporter": "坂本有莉菜（Mimola）",
        "raw_url": "https://www.instagram.com/riku_nurse.mama?srtk=MWNKOTBuYjM2MGdjbA==",
        "username": "riku_nurse.mama",
        "platform": "Instagram",
        "reason": "聞いたことある〜から根掘り葉掘り聞いてきます。自分の人生たのし〜なのでおせっかい不用です。",
        "image": "Screenshot 2026-10-25 at 20.34.35.png"
    },
    {
        "id": "cand_7",
        "date": "2026-10-24 23:17",
        "reporter": "岸部千夏（Couleur）",
        "raw_url": "https://www.threads.com/@life_dorm.azusa",
        "username": "life_dorm.azusa",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-25 at 20.34.35.png"
    },
    {
        "id": "cand_8",
        "date": "2026-10-25 06:34",
        "reporter": "長野さとみ（Ablaze）",
        "raw_url": "https://www.instagram.com/camila812583?cplk=ZWJvYzcldXI5dXN6",
        "username": "camila812583",
        "platform": "Instagram",
        "reason": "会長の偽アカです",
        "image": "Screenshot 2026-10-25 at 20.34.29.png"
    },
    {
        "id": "cand_9",
        "date": "2026-10-25 08:34",
        "reporter": "服部達典（MURA）",
        "raw_url": "https://www.instagram.com/yunyun.kazamaura?psln=MWRIdjBiaWl5bxluYg==",
        "username": "yunyun.kazamaura",
        "platform": "Instagram",
        "reason": "ネットワークに集中したいとのことです。",
        "image": "Screenshot 2026-10-25 at 20.34.29.png"
    },
    {
        "id": "cand_10",
        "date": "2026-10-25 16:34",
        "reporter": "いわやともみ（Blooming）",
        "raw_url": "https://www.instagram.com/rinrin_neko?cplk=MXFjYmUzczVtNHo2Mg==",
        "username": "rinrin_neko",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-25 at 20.34.29.png"
    },
    {
        "id": "cand_11",
        "date": "2026-10-25 16:34",
        "reporter": "小西みゆき（Mimola）",
        "raw_url": "https://lite.tiktok.com/t/ZS9ydKNtKv7xS-8wliv/",
        "username": "ZS9ydKNtKv7xS-8wliv",
        "platform": "TikTok",
        "reason": "会長のなりすましです",
        "image": "Screenshot 2026-10-25 at 20.34.29.png"
    },
    {
        "id": "cand_12",
        "date": "2026-10-25 19:41",
        "reporter": "中嶋初美（glowell）",
        "raw_url": "https://www.threads.com/@kodomo_mirai_ouentai",
        "username": "kodomo_mirai_ouentai",
        "platform": "Threads",
        "reason": "腹が立ちました。コメントは、恐らくお仲間の方かと思いますが、投稿主はブロックで良いかと思います！",
        "image": "Screenshot 2026-10-25 at 20.34.29.png",
        "existing_match": "blk_085"
    },
    {
        "id": "cand_13",
        "date": "2026-10-25 20:26",
        "reporter": "畠山尚美",
        "raw_url": "https://www.threads.com/@momikaemasa?igshid=NTc4MTIwNjQ2YQ==",
        "username": "momikaemasa",
        "platform": "Threads",
        "reason": "何度もネオファミリーの話しは聞いてる\nネクストエイドが1番とやってるそう。\nネオに入る気全くなく時間の無駄です",
        "image": "Screenshot 2026-10-25 at 20.34.29.png"
    }
]

def fetch_url_info(u):
    if not u or not u.startswith("http"):
        return None, None
    for ua in ["facebookexternalhit/1.1", "Twitterbot/1.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"]:
        try:
            req = urllib.request.Request(u, headers={
                "User-Agent": ua,
                "Accept-Language": "ja,en-US;q=0.9,en;q=0.8"
            })
            with urllib.request.urlopen(req, timeout=6) as r:
                final_url = r.geturl()
                body = r.read(98304).decode("utf-8", errors="ignore")
                og = re.search(r'property=["\']og:title["\']\s+content=["\'](.*?)["\']', body, re.I) or \
                     re.search(r'content=["\'](.*?)["\']\s+property=["\']og:title["\']', body, re.I) or \
                     re.search(r'name=["\']twitter:title["\']\s+content=["\'](.*?)["\']', body, re.I)
                t = re.search(r'<title[^>]*>(.*?)</title>', body, re.S | re.I)
                raw = og.group(1) if og else (t.group(1) if t else None)
                if raw:
                    raw = html.unescape(raw).strip()
                    raw = re.sub(r'\s*[\|｜•·-]\s*(?:Instagram|Threads|TikTok).*$', '', raw, flags=re.I).strip()
                return raw, final_url
        except Exception:
            pass
    return None, None

for c in candidates:
    u = c["raw_url"]
    t, f_url = fetch_url_info(u)
    if not t and c["platform"] in ["Instagram", "Threads"]:
        # Try alternate platform (Threads <-> Instagram)
        alt = f"https://www.threads.net/@{c['username']}" if c["platform"] == "Instagram" else f"https://www.instagram.com/{c['username']}/"
        alt_t, _ = fetch_url_info(alt)
        if alt_t:
            t = alt_t
    c["fetched_title"] = t
    c["final_url"] = f_url
    print(f"[{c['id']}] {c['username']} -> {t} (URL: {f_url})")

with open("scripts/candidate_titles_oct25.json", "w", encoding="utf-8") as f:
    json.dump(candidates, f, ensure_ascii=False, indent=2)
