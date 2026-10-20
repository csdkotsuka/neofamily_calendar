import json
import re
from urllib.parse import urlparse

with open("scripts/ocr_results.json") as f:
    images_data = json.load(f)

images_data.sort(key=lambda x: x["file"])

def is_noise(t, x):
    t = t.strip()
    if not t or t in ["Notes", "Ca", "戻る", "編集", "完了", "共有", "投稿", "コメント", "ノート"]:
        return True
    if x > 0.75: # reactions on the right side
        return True
    if re.match(r'^[0-9①-⑳C\s：:…\.\,\_\@\(\)]+$', t):
        return True
    if re.match(r'^[0-9]+(?:\.[0-9]+)?$', t):
        return True
    return False

date_regex = re.compile(
    r'^(?:'
    r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d+(?:\s+\d{1,2}:\d{2}\s*(?:AM|PM)?)?'
    r'|Yesterday(?:\s+at\s+\d{1,2}:\d{2}\s*(?:AM|PM)?)?'
    r'|Today(?:\s+at\s+\d{1,2}:\d{2}\s*(?:AM|PM)?)?'
    r'|\d{4}年\d{1,2}月\d{1,2}日(?:\s+\d{1,2}:\d{2})?'
    r'|\d{1,2}月\d{1,2}日(?:\s+\d{1,2}:\d{2})?'
    r')$', re.IGNORECASE
)

reporter_keywords = ["RAYTUS", "yuima", "ensemble", "MAARUKU", "Couleur", "enchant", "Meguria", "シャンブル", "tEaM", "秘書", "理事長", "リーダー", "スタッフ", "代表", "理事", "事務局"]

def is_reporter(t):
    if ("/" in t or "／" in t) and any(k.lower() in t.lower() for k in reporter_keywords):
        # Don't treat URLs or dates as reporters
        if "http" not in t.lower() and not re.search(r'\d{4}\/\d', t):
            return True
    return False

def clean_url_str(u):
    u = u.strip()
    u = u.replace("？", "?").replace("＆", "&").replace("＝", "=").replace("％", "%").replace("／", "/")
    u = u.replace(" ", "")
    u = re.sub(r'^(nttps|nltps|htps|hfps|httos|https)[:：]\/*', 'https://', u, flags=re.IGNORECASE)
    u = re.sub(r'^(nttp|htip|http)[:：]\/*', 'http://', u, flags=re.IGNORECASE)
    u = re.sub(r'threaas\.com', 'threads.net', u, flags=re.IGNORECASE)
    u = re.sub(r'threads\.com', 'threads.net', u, flags=re.IGNORECASE)
    u = re.sub(r'[」」\)\'\"\.#]+$', '', u)
    if not u.startswith("http"):
        if u.startswith("www."):
            u = "https://" + u
    return u

def is_url_line(t):
    t_clean = t.replace(" ", "").lower()
    if any(p in t_clean for p in ["http://", "https://", "nttps://", "htps://", "instagram.com", "threads.net", "threads.com", "facebook.com", "tiktok.com", "x.com", "twitter.com"]):
        return True
    return False

def is_url_continuation(t):
    t_clean = t.replace(" ", "").lower()
    if any(t_clean.startswith(prefix) for prefix in [
        "igsh=", "utm_", "igshid=", "id=", "stkn=", "psin=", "xnw==", "mibextid=", 
        "share/", "profile.php", "bofz", "1ee1", "1krj", "1sq7", "1kbw"
    ]):
        return True
    if len(t_clean) < 50 and re.match(r'^[a-z0-9\=\_\%\-\&\?]+$', t_clean, re.I):
        return True
    return False

def get_platform(url):
    u_low = url.lower()
    if "instagram.com" in u_low:
        return "Instagram"
    elif "threads.net" in u_low or "threads.com" in u_low:
        return "Threads"
    elif "facebook.com" in u_low:
        return "Facebook"
    elif "x.com" in u_low or "twitter.com" in u_low:
        return "X"
    elif "tiktok.com" in u_low:
        return "TikTok"
    return "Web"

def extract_account_id(url):
    u = clean_url_str(url)
    try:
        parsed = urlparse(u)
        path = parsed.path.strip("/")
        if "instagram.com" in parsed.netloc:
            parts = path.split("/")
            if parts and parts[0] not in ["p", "reel", "stories", "share", "explore"]:
                return parts[0]
        elif "threads" in parsed.netloc:
            parts = path.split("/")
            for p in parts:
                if p.startswith("@"):
                    return p.lstrip("@")
            if parts and parts[0] not in ["share"]:
                return parts[0].lstrip("@")
        elif "facebook.com" in parsed.netloc:
            if "share/" in path:
                return None
            if path and path not in ["profile.php", "groups", "pages"]:
                return path.split("/")[0]
    except:
        pass
    return None

def normalize_date(raw):
    if not raw:
        return ""
    d = raw.strip()
    if "yesterday" in d.lower():
        tm = re.search(r'(\d{1,2}:\d{2}\s*(?:AM|PM)?)', d, re.I)
        return f"2026-10-19 {tm.group(1)}" if tm else "2026-10-19"
    if "today" in d.lower():
        tm = re.search(r'(\d{1,2}:\d{2}\s*(?:AM|PM)?)', d, re.I)
        return f"2026-10-20 {tm.group(1)}" if tm else "2026-10-20"
        
    months = {"jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06", 
              "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"}
    m = re.match(r'([A-Za-z]{3})[a-z]*\.?\s+(\d+)(?:\s+(\d{1,2}:\d{2}\s*(?:AM|PM)?))?', d, re.I)
    if m:
        mon = months.get(m.group(1).lower(), "01")
        day = f"{int(m.group(2)):02d}"
        tm = f" {m.group(3)}" if m.group(3) else ""
        return f"2026-{mon}-{day}{tm}"
    return d

# Group lines per image into posts
posts = []

for img in images_data:
    sorted_lines = sorted(img["lines"], key=lambda l: l["y"])
    valid_lines = [l["text"].strip() for l in sorted_lines if not is_noise(l["text"], l["x"])]
    if not valid_lines:
        continue
        
    curr_post = {"date": "", "reporter": "", "content_lines": [], "image": img["file"]}
    
    for line in valid_lines:
        if date_regex.match(line):
            if curr_post["content_lines"]:
                posts.append(curr_post)
                curr_post = {"date": line, "reporter": "", "content_lines": [], "image": img["file"]}
            else:
                curr_post["date"] = line
        elif is_reporter(line):
            if not curr_post["reporter"]:
                curr_post["reporter"] = line
            else:
                # If we already had a reporter and content, this is a new post without date header
                if curr_post["content_lines"]:
                    posts.append(curr_post)
                    curr_post = {"date": curr_post["date"], "reporter": line, "content_lines": [], "image": img["file"]}
                else:
                    curr_post["reporter"] = line
        else:
            curr_post["content_lines"].append(line)
            
    if curr_post["content_lines"]:
        posts.append(curr_post)

print(f"Total post chunks parsed across images: {len(posts)}")

# Now parse content lines in each post
processed_entries = []

for p in posts:
    lines = p["content_lines"]
    post_date = normalize_date(p["date"])
    reporter = p["reporter"]
    
    # Merge URL lines
    merged_lines = []
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        if idx > 0 and (is_url_continuation(line) or (merged_lines and is_url_line(merged_lines[-1]) and not is_url_line(line) and ("=" in line or line.startswith("/") or line.startswith("#") or line.startswith("?")))):
            merged_lines[-1] = merged_lines[-1] + "" + line
        else:
            merged_lines.append(line)
        idx += 1
        
    # Classify lines into URLs, Names, and Reasons
    urls = []
    text_pieces = []
    
    for l in merged_lines:
        if is_url_line(l):
            # Extract URL part
            u_match = re.search(r'(?:https?:\/\/|www\.|nttps:\/\/|hftps:\/\/)[^\s]+', l, re.I)
            if u_match:
                urls.append(clean_url_str(u_match.group(0)))
                rest = l.replace(u_match.group(0), "").strip()
                if rest and not is_noise(rest, 0):
                    text_pieces.append(rest)
            else:
                urls.append(clean_url_str(l))
        else:
            text_pieces.append(l)
            
    # Separate names vs reasons
    name_parts = []
    reason_parts = []
    
    reason_keywords = [
        "お断り", "勧誘", "モラハラ", "悪口", "退会", "ドタキャン", "声かけない", "ブロック", 
        "話を聞いた", "必要ない", "営業", "zoom", "Zoom", "リスケ", "警戒", "着信", "DM", 
        "連絡", "不信感", "事実でない", "おせっかい", "お金がない", "入る気ない", "煽る", 
        "マウント", "文面", "メッセージ", "失業手当", "無職", "変わった人", "ネガティブ", 
        "クレーム", "トラブル", "迷惑", "辞退", "注意", "注意喚起", "危険", "怪しい"
    ]
    
    for t in text_pieces:
        # Ignore label tags like (threads), (インスタ)
        if t in ["（threads）", "（インスタ）", "(threads)", "(インスタ)", "（Threads）", "（Instagram）"]:
            continue
            
        if any(rk in t for rk in reason_keywords) or len(t) > 30 or t.endswith(("。", "！", "!", "ました", "ください", "ません")):
            reason_parts.append(t)
        else:
            name_parts.append(t)
            
    name = " / ".join(name_parts).strip()
    reason = " ".join(reason_parts).strip()
    
    # If no URLs, still keep if there is name or reason
    if not urls:
        if name or reason:
            processed_entries.append({
                "date": post_date,
                "reporter": reporter,
                "name": name,
                "url": "",
                "secondary_url": "",
                "platform": "その他",
                "reason": reason,
                "account_id": "",
                "image": p["image"]
            })
    elif len(urls) == 1:
        u = urls[0]
        acc = extract_account_id(u)
        processed_entries.append({
            "date": post_date,
            "reporter": reporter,
            "name": name or (f"@{acc}" if acc else ""),
            "url": u,
            "secondary_url": "",
            "platform": get_platform(u),
            "reason": reason,
            "account_id": acc or "",
            "image": p["image"]
        })
    else:
        # Check if 2 URLs belong to same person (e.g. Threads & Instagram)
        accs = [extract_account_id(u) for u in urls]
        non_none_accs = [a.lower() for a in accs if a]
        if len(urls) == 2 and (len(set(non_none_accs)) <= 1 or not non_none_accs):
            # Same person with 2 social links!
            main_acc = non_none_accs[0] if non_none_accs else ""
            processed_entries.append({
                "date": post_date,
                "reporter": reporter,
                "name": name or (f"@{main_acc}" if main_acc else ""),
                "url": urls[0],
                "secondary_url": urls[1],
                "platform": f"{get_platform(urls[0])} / {get_platform(urls[1])}",
                "reason": reason,
                "account_id": main_acc,
                "image": p["image"]
            })
        else:
            # Multiple separate URLs
            for u in urls:
                acc = extract_account_id(u)
                processed_entries.append({
                    "date": post_date,
                    "reporter": reporter,
                    "name": (f"@{acc}" if acc else "") or name,
                    "url": u,
                    "secondary_url": "",
                    "platform": get_platform(u),
                    "reason": reason,
                    "account_id": acc or "",
                    "image": p["image"]
                })

print(f"Total processed entries before deduplication: {len(processed_entries)}")

# Canonical URL helper
def get_canonical(u):
    if not u:
        return ""
    try:
        parsed = urlparse(u)
        netloc = parsed.netloc.lower().replace("www.", "")
        if "threads" in netloc:
            netloc = "threads.net"
        path = parsed.path.rstrip("/")
        # If facebook share, keep full path
        return f"{netloc}{path}".lower()
    except:
        return u.lower()

# Deduplicate
dedup_dict = {}

for entry in processed_entries:
    canon = get_canonical(entry["url"])
    if canon and canon not in ["instagram.com", "threads.net", "facebook.com", "facebook.com/share", "facebook.com/profile.php"]:
        key = ("url", canon)
    else:
        # Key by date + reporter + name/reason
        key = ("fallback", entry["date"], entry["reporter"], entry["name"] or entry["reason"][:20])
        
    if key not in dedup_dict:
        dedup_dict[key] = entry
    else:
        # Merge richer information
        curr = dedup_dict[key]
        if not curr["name"] and entry["name"]:
            curr["name"] = entry["name"]
        elif entry["name"] and len(entry["name"]) > len(curr["name"]):
            curr["name"] = entry["name"]
            
        if not curr["reason"] and entry["reason"]:
            curr["reason"] = entry["reason"]
        elif entry["reason"] and len(entry["reason"]) > len(curr["reason"]):
            curr["reason"] = entry["reason"]
            
        if not curr["secondary_url"] and entry["secondary_url"]:
            curr["secondary_url"] = entry["secondary_url"]
            curr["platform"] = f"{curr['platform']} / {get_platform(entry['secondary_url'])}"
            
        if not curr["date"] and entry["date"]:
            curr["date"] = entry["date"]
            
        if not curr["reporter"] and entry["reporter"]:
            curr["reporter"] = entry["reporter"]

final_list = list(dedup_dict.values())

# Give unique IDs and polish names
for idx, item in enumerate(final_list, 1):
    item["id"] = f"blk_{idx:03d}"
    if not item["name"] or item["name"].strip() == "":
        if item["account_id"]:
            item["name"] = f"@{item['account_id']}"
        elif item["url"]:
            item["name"] = item["platform"] + "アカウント"
        else:
            item["name"] = "（名称未記載）"
            
    # Polish reporter
    if not item["reporter"] or item["reporter"].strip() == "":
        item["reporter"] = "管理部/秘書課"

print(f"\nFinal deduplicated blocklist items: {len(final_list)}")

# Save to JSON
with open("js/blocklist-data.json", "w", encoding="utf-8") as f:
    json.dump(final_list, f, ensure_ascii=False, indent=2)

# Also save as a JS module/variable for direct client loading
with open("js/blocklist-data.js", "w", encoding="utf-8") as f:
    f.write("/**\n * NEO FAMILY Calendar - Blocklist Data (Auto-extracted from LINE Note Screenshots)\n")
    f.write(" * Total items: " + str(len(final_list)) + "\n */\n")
    f.write("const INITIAL_BLOCKLIST = " + json.dumps(final_list, ensure_ascii=False, indent=2) + ";\n")

print("Saved to js/blocklist-data.json and js/blocklist-data.js successfully!")
