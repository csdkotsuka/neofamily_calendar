import json, urllib.request, re, html, time
from urllib.parse import urlparse

# Load existing blocklist
with open("js/blocklist-data.json", "r", encoding="utf-8") as f:
    existing = json.load(f)

def extract_account_key(url):
    if not url:
        return None
    base = url.split("?")[0].rstrip("/")
    m_share = re.search(r'threads\.(?:net|com)/share/([a-zA-Z0-9_\-]+)', base)
    if m_share:
        return ("share", m_share.group(1))
    m_threads = re.search(r'threads\.(?:net|com)/@([a-zA-Z0-9_.\-]+)', base)
    if m_threads:
        return ("threads", m_threads.group(1).lower())
    m_ig = re.search(r'instagram\.com/([a-zA-Z0-9_.\-]+)', base)
    if m_ig:
        name = m_ig.group(1).lower()
        if name not in ["p", "reel", "stories", "explore"]:
            return ("ig", name)
    return ("raw", base.lower())

existing_index = {}
for item in existing:
    k1 = extract_account_key(item.get("url", ""))
    k2 = extract_account_key(item.get("secondary_url", ""))
    if k1:
        existing_index.setdefault(k1, []).append(item)
    if k2:
        existing_index.setdefault(k2, []).append(item)

# Candidate list
candidates = [
    {
        "cand_id": "c1",
        "date": "2026-10-22 12:55",
        "reporter": "小野八音（yaShine）",
        "reason": "",
        "url": "https://www.instagram.com/kanrieiyoushi_metas?obrf=MXd0NXk3Y214Nzk1OQ==",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.12.15.png"
    },
    {
        "cand_id": "c2",
        "date": "2026-10-22 15:52",
        "reporter": "後藤広代（Lumiere.）",
        "reason": "",
        "url": "https://www.threads.com/share/BBsMFS1cFy/",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.12.15.png"
    },
    {
        "cand_id": "c3",
        "date": "2026-10-22 15:53",
        "reporter": "後藤広代（Lumiere.）",
        "reason": "",
        "url": "https://www.threads.com/share/BAa9M0zjs6/",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.12.15.png"
    },
    {
        "cand_id": "c4",
        "date": "2026-10-22 16:26",
        "reporter": "小西みゆき（Mimola）",
        "reason": "自分でコミュニティ作ってるので大丈夫だそうです",
        "url": "https://www.instagram.com/baby_growth_japan?cplk=MnVqMWRmYjFydzlw",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.12.08.png"
    },
    {
        "cand_id": "c5",
        "date": "2026-10-22 17:17",
        "reporter": "服部達典（MURA）",
        "reason": "",
        "url": "https://www.instagram.com/herb_nemokoro?cplk=ZzImaWpucHFqMHEx",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.12.08.png"
    },
    {
        "cand_id": "c6",
        "date": "2026-10-22 17:24",
        "reporter": "井峯明香奈（shAdow）",
        "reason": "",
        "url": "https://www.threads.com/@1123.love.1123?igshid=NTc4MTIwNjQ2YQ==",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.12.08.png"
    },
    {
        "cand_id": "c7",
        "date": "2026-10-22 17:49",
        "reporter": "後藤広代（Lumiere.）",
        "reason": "",
        "url": "https://www.threads.com/@kento12ap",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.12.08.png"
    },
    {
        "cand_id": "c8",
        "date": "2026-10-22 18:52",
        "reporter": "菅野美穂（Couleur理事長）",
        "reason": "",
        "url": "https://www.threads.com/@chi_e_biyou",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.12.08.png"
    },
    {
        "cand_id": "c9",
        "date": "2026-10-22 21:25",
        "reporter": "北御門祥子（Ablaze）",
        "reason": "",
        "url": "https://www.threads.com/share/BAt2rEETHn/",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.12.08.png"
    },
    {
        "cand_id": "c10",
        "date": "2026-10-22 21:56",
        "reporter": "小西みゆき（Mimola）",
        "reason": "",
        "url": "https://www.instagram.com/caco.kosodate",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.12.08.png"
    },
    {
        "cand_id": "c11",
        "date": "2026-10-22 21:57",
        "reporter": "小西みゆき（Mimola）",
        "reason": "DM送ったら非公開になりました",
        "url": "https://www.instagram.com/m.baby_mama.23",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.12.08.png"
    },
    {
        "cand_id": "c12_a",
        "date": "2026-10-23 05:08",
        "reporter": "服部達典（MURA）",
        "reason": "",
        "url": "https://www.instagram.com/kosodatemama0524?rpxt=YmxrZ2RpcDMxbjc1",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.12.02.png"
    },
    {
        "cand_id": "c12_b",
        "date": "2026-10-23 05:08",
        "reporter": "服部達典（MURA）",
        "reason": "",
        "url": "https://www.instagram.com/cherilu_yn?mdxt=bGlqMDhmbjJ0czRu",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.12.02.png"
    },
    {
        "cand_id": "c12_c",
        "date": "2026-10-23 05:08",
        "reporter": "服部達典（MURA）",
        "reason": "",
        "url": "https://www.instagram.com/herb_nemokoro?rpxt=ZzImaWpucHFqMHEx",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.12.02.png"
    },
    {
        "cand_id": "c12_d",
        "date": "2026-10-23 05:08",
        "reporter": "服部達典（MURA）",
        "reason": "",
        "url": "https://www.instagram.com/romy.yade?exln=ajdhcnYxYmx5Nmsx",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.12.02.png"
    },
    {
        "cand_id": "c14",
        "date": "2026-10-23 08:49",
        "reporter": "齊藤唯（Mimola）",
        "reason": "",
        "url": "https://www.threads.com/@magier_2023?igshid=NTc4MTIwNjQ2YQ==",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.12.02.png"
    },
    {
        "cand_id": "c15",
        "date": "2026-10-23 09:28",
        "reporter": "森崎江里（RAYTUS / 愛知県）",
        "reason": "誰かのやりとり、スクショで晒されてます💦 コメントのやつも報告とブロックお願いします",
        "url": "https://www.threads.com/@rina.s0527",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.12.02.png"
    },
    {
        "cand_id": "c16",
        "date": "2026-10-23 09:46",
        "reporter": "相良沙織（Meguria理事長）",
        "reason": "@森崎江里／愛知県/RAYTUS さんのいう方のリンクはこちら 通報もよろしくお願い申し上げます。",
        "url": "https://www.threads.com/@rina.s0527",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.12.02.png"
    },
    {
        "cand_id": "c17",
        "date": "2026-10-23 11:19",
        "reporter": "坂本有莉菜（Mimola）",
        "reason": "",
        "url": "https://www.threads.com/@tomopooh1113?igshid=NTc4MTIwNjQ2YQ==",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.12.02.png"
    },
    {
        "cand_id": "c18",
        "date": "2026-10-23 14:27",
        "reporter": "井峯明香奈（shAdow）",
        "reason": "",
        "url": "https://www.threads.com/@shimosonet?igshid=NTc4MTIwNjQ2YQ==",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.11.56.png"
    },
    {
        "cand_id": "c19",
        "date": "2026-10-23 15:09",
        "reporter": "畑ゆかり（yuima-ru理事長）",
        "reason": "ぶった斬り会長・・・名指しでした",
        "url": "https://www.threads.com/@matsunaga__haruna?igshid=NTc4MTIwNjQ2YQ==",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.11.56.png"
    },
    {
        "cand_id": "c20",
        "date": "2026-10-23 17:43",
        "reporter": "井峯明香奈（shAdow）",
        "reason": "",
        "url": "https://www.threads.com/@yokoyama_ibaraki?igshid=NTc4MTIwNjQ2YQ==",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.11.56.png"
    },
    {
        "cand_id": "c21",
        "date": "2026-10-23 19:54",
        "reporter": "城間千聖（enLIGHT）",
        "reason": "",
        "url": "https://www.instagram.com/artmake_momoka?exln=b29zenR2cjUyYXB1bHs=",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.11.56.png"
    },
    {
        "cand_id": "c22",
        "date": "2026-10-23 20:42",
        "reporter": "岩﨑七菜子（tEaM_S.）",
        "reason": "ファーストして興味あるフリして、なんの断りもなくブロック＆zoom来ずでした",
        "url": "https://www.threads.com/@holitaku_pickleball",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.11.56.png"
    },
    {
        "cand_id": "c23",
        "date": "2026-10-23 22:37",
        "reporter": "ロジャーズ優衣（enchant+）",
        "reason": "",
        "url": "https://www.threads.com/@poochan5676?igshid=NTc4MTIwNjQ2YQ==",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.11.56.png"
    },
    {
        "cand_id": "c24",
        "date": "2026-10-23 22:57",
        "reporter": "ロジャーズ優衣（enchant+）",
        "reason": "",
        "url": "https://www.instagram.com/ayumi.reborn?xtok=MXRkZzUwaWIwam5leA==",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.11.48.png"
    },
    {
        "cand_id": "c25",
        "date": "2026-10-23 23:34",
        "reporter": "小野八音（yaShine）",
        "reason": "何度もお声かけいただき ZOOMもしてお断りしました、とのことです！",
        "url": "https://www.instagram.com/tomo.ninkatsueiyou?srtk=MWxtYjJ4aWM3bXlodg==",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.11.48.png"
    },
    {
        "cand_id": "c26",
        "date": "2026-10-24 01:14",
        "reporter": "桝田和裕（AMATERAS）",
        "reason": "",
        "url": "https://www.threads.com/@nobu491004?igshid=NTc4MTIwNjQ2YQ==",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.11.48.png"
    },
    {
        "cand_id": "c27",
        "date": "2026-10-24 01:14",
        "reporter": "南藍（tidy.shin代表）",
        "reason": "言っていることに信ぴょう性がなく、マウント取ってくる。",
        "url": "https://www.threads.com/@mochi_creative123?igshid=NTc4MTIwNjQ2YQ==",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.11.48.png"
    },
    {
        "cand_id": "c28",
        "date": "2026-10-24 10:11",
        "reporter": "城間千聖（enLIGHT）",
        "reason": "何度もお声かけしているようです。Zoom面談をした上でお断りしたそう。",
        "url": "https://www.instagram.com/sato_aoi_photo?psln=MWp5bGtncmZpYTE4OA==",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.11.48.png"
    },
    {
        "cand_id": "c29",
        "date": "2026-10-24 10:11",
        "reporter": "ロジャーズ優衣（enchant+）",
        "reason": "向こうからメッセージをいただきましたが、NEOに会うのは3回目だったそうです🙏",
        "url": "https://www.threads.com/@nijirosinkyu?igshid=NTc4MTIwNjQ2YQ==",
        "secondary_url": "https://www.instagram.com/nijirosinkyu?vrfl=MWg3M2oyM25uN2xtYg==",
        "image": "Screenshot 2026-10-24 at 15.11.48.png"
    },
    {
        "cand_id": "c30",
        "date": "2026-10-24 13:11",
        "reporter": "服部達典（MURA）",
        "reason": "",
        "url": "https://www.instagram.com/mayu_coach.mama?psln=MThpd2lycW5jamo5Mw==",
        "secondary_url": "",
        "image": "Screenshot 2026-10-24 at 15.11.48.png"
    }
]

print("=== CHECKING DUPLICATES WITH EXISTING BLOCKLIST ===")
for c in candidates:
    k = extract_account_key(c["url"])
    k_sec = extract_account_key(c["secondary_url"])
    match = existing_index.get(k) or (existing_index.get(k_sec) if k_sec else None)
    if match:
        print(f"DUPLICATE FOUND with existing: {c['cand_id']} ({c['url']}) -> Matches {len(match)} existing items:")
        for m in match:
            print(f"   - {m['id']} (serial: {m.get('serialNo')}, date: {m.get('date')}, name: {m.get('name')}, reporter: {m.get('reporter')})")

print("\n=== CHECKING INTRA-CANDIDATE DUPLICATES ===")
seen = {}
for c in candidates:
    k = extract_account_key(c["url"])
    if k in seen:
        print(f"INTRA DUPLICATE: {c['cand_id']} duplicates {seen[k]['cand_id']} on key {k}")
    else:
        seen[k] = c
