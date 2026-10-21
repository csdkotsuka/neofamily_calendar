import json, re
from urllib.parse import urlparse

with open("scripts/ocr_results.json") as f:
    images_data = json.load(f)

images_data.sort(key=lambda x: x["file"])

def is_noise(t, x):
    t = t.strip()
    if not t or t in ["Notes", "Ca", "戻る", "編集", "完了", "共有", "投稿", "コメント", "ノート"]:
        return True
    if x > 0.75: # reactions on the right
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

# Any pattern with Name / Team, or Name Team (e.g. "北御門祥子 ／ Ablaze", "本多栞/RAYTUS/秘書課", "とくながあけみ RAYTUS")
team_keywords = [
    "RAYTUS", "yuima", "ensemble", "MAARUKU", "Couleur", "enchant", 
    "Meguria", "シャンブル", "tEaM", "秘書", "理事長", "リーダー", 
    "スタッフ", "代表", "理事", "事務局", "Mimola", "Blooming", 
    "Lumiere", "Ablaze", "ablaze", "CHOICE", "MURA", "AMATERAS", 
    "shAdow", "碧春", "Couleur理事長", "yuima-ru理事長"
]

def is_reporter_text(t):
    t_clean = t.replace("／", "/").replace("＼", "/").replace("\\", "/")
    # Has slash and team keyword or looks like reporter
    if "/" in t_clean:
        if any(k.lower() in t_clean.lower() for k in team_keywords):
            if "http" not in t.lower() and not re.search(r'\d{4}\/\d', t):
                return True
        # If 2 parts, both relatively short, and not a URL
        parts = t_clean.split("/")
        if len(parts) >= 2 and all(len(p.strip()) <= 15 for p in parts) and "http" not in t.lower():
            return True
            
    # Also check space-separated known teams (e.g. "とくながあけみ RAYTUS")
    for k in team_keywords:
        if k in t and len(t) <= 25 and not any(ch in t for ch in ["http", ".com", ".net", "www"]):
            return True
    return False

def parse_reporter_display(t):
    if not t:
        return "管理部（秘書課）"
    t_clean = t.replace("／", "/").replace("＼", "/").replace("\\", "/")
    
    # Handle space separation e.g. "北御門祥子 Ablaze" or "北御門祥子 ／ Ablaze"
    t_clean = re.sub(r'\s+[\/]\s+', '/', t_clean)
    
    parts = [p.strip() for p in t_clean.split("/") if p.strip()]
    if len(parts) == 1:
        # Check space split
        sp = t_clean.split()
        if len(sp) >= 2:
            parts = sp
            
    if not parts:
        return "管理部（秘書課）"
        
    name = parts[0]
    if name == "本多菜": name = "本多栞"
    if name.startswith("本多"): name = "本多栞"
    
    dept_parts = parts[1:]
    dept = " / ".join(dept_parts) if dept_parts else ""
    return f"{name}（{dept}）" if dept else name

def format_date_str(d_clean):
    if not d_clean: return ""
    d = d_clean.strip()
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

def separate_url_and_japanese_text(line):
    # Splits e.g. "https://www.threads.net/@pastel_aco?igshid=...お声がけたくさんされてるみたいですが..."
    # into URL and comment text
    # Match URL part up to first non-URL character (like Japanese, quotes, spaces)
    # URL valid chars: A-Za-z0-9-._~:/?#[]@!$&'()*+,;%=
    m = re.search(r'((?:https?:\/\/|www\.|nttps:\/\/|hftps:\/\/)[A-Za-z0-9\-._~:/?#\[\]@!$&\'()*+,;%=]+)(.*)', line)
    if m:
        u = m.group(1)
        rest = m.group(2).strip()
        return u, rest
    return line, ""

def clean_url(u):
    raw = u.strip()
    warning = ""
    
    # Fix typos
    if raw.lower().startswith("nttps://"):
        warning = "プロトコル誤記修復 (nttps→https)"
        raw = "https://" + raw[8:]
    elif raw.lower().startswith("htps://"):
        warning = "プロトコル誤記修復 (htps→https)"
        raw = "https://" + raw[7:]
    elif raw.lower().startswith("http://") and any(d in raw.lower() for d in ["instagram.com", "threads.net", "facebook.com"]):
        raw = "https://" + raw[7:]
        
    if "threaas.com" in raw.lower():
        warning = "ドメイン誤記修復 (threaas→threads.net)"
        raw = re.sub(r'threaas\.com', 'threads.net', raw, flags=re.I)
    elif "threads.com" in raw.lower():
        raw = re.sub(r'threads\.com', 'threads.net', raw, flags=re.I)

    raw = raw.replace("？", "?").replace("＆", "&").replace("＝", "=").replace("％", "%").replace("／", "/")
    raw = raw.replace(" ", "")
    raw = re.sub(r'[」」\)\'\"\.#]+$', '', raw)
    
    if not raw.startswith("http"):
        if raw.startswith("www."):
            raw = "https://" + raw

    # Validate
    try:
        parsed = urlparse(raw)
        path = parsed.path.strip("/")
        if "instagram.com" in parsed.netloc:
            if not path or path in ["p", "reel", "stories", "share", "explore"]:
                warning = "⚠️ アカウントURL不完全"
        elif "threads" in parsed.netloc:
            if not path or path in ["share"]:
                warning = "⚠️ アカウントURL不完全"
        elif "facebook.com" in parsed.netloc:
            if path == "share/1" or path == "share":
                warning = "⚠️ 共有ID欠落（リンク切れの可能性）"
    except Exception:
        warning = "⚠️ URL形式異常"

    return raw, warning

def extract_account_handle(url):
    try:
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        if "instagram.com" in parsed.netloc:
            parts = path.split("/")
            if parts and parts[0] not in ["p", "reel", "stories", "share", "explore"]:
                return f"@{parts[0]}"
        elif "threads" in parsed.netloc:
            parts = path.split("/")
            for p in parts:
                if p.startswith("@"):
                    return p
            if parts and parts[0] not in ["share"]:
                return f"@{parts[0]}"
        elif "facebook.com" in parsed.netloc:
            if "share/" in path:
                return "Facebookユーザー"
            if path and path not in ["profile.php", "groups", "pages"]:
                return f"FB: {path.split('/')[0]}"
            return "Facebookユーザー"
    except:
        pass
    return "（名称未記載）"

def get_platform_label(url):
    u = url.lower()
    if "instagram.com" in u: return "Instagram"
    if "threads.net" in u: return "Threads"
    if "facebook.com" in u: return "Facebook"
    if "x.com" in u or "twitter.com" in u: return "X"
    if "tiktok.com" in u: return "TikTok"
    return "Web"

# Parse raw posts from OCR results
posts = []

for img in images_data:
    sorted_lines = sorted(img["lines"], key=lambda l: l["y"])
    valid_lines = [l["text"].strip() for l in sorted_lines if not is_noise(l["text"], l["x"])]
    if not valid_lines: continue
    
    curr_post = {"date": "", "reporter": "", "lines": [], "image": img["file"]}
    
    for line in valid_lines:
        if date_regex.match(line):
            if curr_post["lines"]:
                posts.append(curr_post)
                curr_post = {"date": line, "reporter": "", "lines": [], "image": img["file"]}
            else:
                curr_post["date"] = line
        elif is_reporter_text(line):
            if not curr_post["reporter"]:
                curr_post["reporter"] = line
            else:
                if curr_post["lines"]:
                    posts.append(curr_post)
                    curr_post = {"date": curr_post["date"], "reporter": line, "lines": [], "image": img["file"]}
                else:
                    curr_post["reporter"] = line
        else:
            curr_post["lines"].append(line)
            
    if curr_post["lines"]:
        posts.append(curr_post)

print(f"Collected {len(posts)} raw posts.")

# Process each post
reconstructed_items = []

for p in posts:
    lines = p["lines"]
    
    # 1. Connect multiline URLs & split text attached to URLs
    merged_lines = []
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        
        # Check if line has URL followed by Japanese text
        url_part, text_rest = separate_url_and_japanese_text(line)
        
        # Check if URL was broken across lines (e.g. facebook share or query params)
        if merged_lines and any(d in merged_lines[-1].lower() for d in ["instagram.com", "threads", "facebook.com"]):
            t_clean = line.replace(" ", "")
            is_cont = False
            if any(t_clean.lower().startswith(prefix) for prefix in ["igsh=", "utm_", "igshid=", "id=", "stkn=", "psin=", "xnw==", "mibextid="]):
                is_cont = True
            elif merged_lines[-1].endswith(("?", "？", "=", "＝", "&", "＆", "/", "#")):
                is_cont = True
            elif "facebook.com/share/1" in merged_lines[-1] and re.match(r'^[A-Za-z0-9_\-]{6,}\/?$', t_clean):
                is_cont = True
                
            if is_cont:
                merged_lines[-1] = merged_lines[-1] + url_part.replace(" ", "")
                if text_rest:
                    merged_lines.append(text_rest)
                idx += 1
                continue
                
        merged_lines.append(url_part)
        if text_rest:
            merged_lines.append(text_rest)
        idx += 1

    # Extract URLs vs text comments
    raw_urls = []
    raw_texts = []
    discovered_reporter = p["reporter"]
    
    for l in merged_lines:
        if is_reporter_text(l):
            # This line is actually a reporter!
            discovered_reporter = l
            continue
            
        u_match = re.search(r'(?:https?:\/\/|www\.|nttps:\/\/|hftps:\/\/)[^\s]+', l, re.I)
        if u_match:
            raw_urls.append(u_match.group(0))
        elif any(d in l.lower() for d in ["instagram.com", "threads.net", "threads.com", "facebook.com"]):
            raw_urls.append(l)
        else:
            # Check labels like (threads), (インスタ)
            if l not in ["（threads）", "（インスタ）", "(threads)", "(インスタ)", "【インスタ】", "【threads】"]:
                raw_texts.append(l)

    # CRITICAL: Exclude posts without any URL
    if not raw_urls:
        continue

    # Clean URLs
    cleaned_urls = []
    for ru in raw_urls:
        cu, warn = clean_url(ru)
        cleaned_urls.append((cu, warn))

    # All text in the post is directly preserved as reason/note (ユーザー指示: 要約なしでそのまま記載)
    reason_note = " ".join(raw_texts).strip()
    
    # Clean reporter display
    reporter_str = parse_reporter_display(discovered_reporter)
    date_str = format_date_str(p["date"])
    
    # Store item
    if len(cleaned_urls) == 1:
        u, w = cleaned_urls[0]
        handle = extract_account_handle(u)
        reconstructed_items.append({
            "date": date_str,
            "reporter": reporter_str,
            "name": handle,
            "url": u,
            "secondary_url": "",
            "platform": get_platform_label(u),
            "url_warning": w,
            "reason": reason_note,
            "image": p["image"]
        })
    elif len(cleaned_urls) == 2 and (get_platform_label(cleaned_urls[0][0]) != get_platform_label(cleaned_urls[1][0])):
        # Same person with 2 platforms (e.g. Threads & Instagram)
        u1, w1 = cleaned_urls[0]
        u2, w2 = cleaned_urls[1]
        handle = extract_account_handle(u1)
        if handle == "（名称未記載）":
            handle = extract_account_handle(u2)
        warns = [w for w in [w1, w2] if w]
        reconstructed_items.append({
            "date": date_str,
            "reporter": reporter_str,
            "name": handle,
            "url": u1,
            "secondary_url": u2,
            "platform": f"{get_platform_label(u1)} / {get_platform_label(u2)}",
            "url_warning": " / ".join(warns),
            "reason": reason_note,
            "image": p["image"]
        })
    else:
        # Multiple accounts in one post
        for u, w in cleaned_urls:
            handle = extract_account_handle(u)
            reconstructed_items.append({
                "date": date_str,
                "reporter": reporter_str,
                "name": handle,
                "url": u,
                "secondary_url": "",
                "platform": get_platform_label(u),
                "url_warning": w,
                "reason": reason_note,
                "image": p["image"]
            })

print(f"Total reconstructed items before deduplication: {len(reconstructed_items)}")

# Deduplication by canonical URL
def get_canon(u):
    try:
        p = urlparse(u)
        netloc = p.netloc.lower().replace("www.", "")
        path = p.path.rstrip("/")
        return f"{netloc}{path}".lower()
    except:
        return u.lower()

dedup_map = {}
for item in reconstructed_items:
    canon = get_canon(item["url"])
    if not canon or canon in ["facebook.com/share", "facebook.com/share/1", "facebook.com/profile.php", "instagram.com", "threads.net"]:
        key = ("fallback", item["date"], item["reporter"], item["url"])
    else:
        key = ("url", canon)

    if key not in dedup_map:
        dedup_map[key] = item
    else:
        existing = dedup_map[key]
        # Merge longer reason
        if len(item["reason"]) > len(existing["reason"]):
            existing["reason"] = item["reason"]
        # Merge secondary URL if exists
        if not existing["secondary_url"] and item["secondary_url"]:
            existing["secondary_url"] = item["secondary_url"]
            existing["platform"] = f"{existing['platform']} / {get_platform_label(item['secondary_url'])}"
        if not existing["date"] and item["date"]:
            existing["date"] = item["date"]
        if item["url_warning"] and item["url_warning"] not in existing["url_warning"]:
            existing["url_warning"] = (existing["url_warning"] + " " + item["url_warning"]).strip()

final_dataset = list(dedup_map.values())
print(f"Final clean deduped items: {len(final_dataset)}")

for idx, item in enumerate(final_dataset, 1):
    item["id"] = f"blk_{idx:03d}"

# Check slashed names
bad_names = [d for d in final_dataset if "/" in d["name"] or "／" in d["name"]]
print(f"Remaining slashed names: {len(bad_names)}")

# Sample check
print("\n--- SAMPLE 10 ITEMS ---")
for item in final_dataset[:10]:
    print(f"[{item['id']}] 氏名: {item['name']} | 報告者: {item['reporter']}")
    print(f"  URL: {item['url']}")
    print(f"  理由: {item['reason'][:60] if item['reason'] else '-'}")
    print("-" * 50)

# Save
with open("js/blocklist-data.json", "w", encoding="utf-8") as f:
    json.dump(final_dataset, f, ensure_ascii=False, indent=2)

with open("js/blocklist-data.js", "w", encoding="utf-8") as f:
    f.write("/**\n * NEO FAMILY Calendar - Blocklist Data (v3 Verified Cleaned)\n")
    f.write(" * Total items: " + str(len(final_dataset)) + "\n */\n")
    f.write("const INITIAL_BLOCKLIST = " + json.dumps(final_dataset, ensure_ascii=False, indent=2) + ";\n")

print("Saved to js/blocklist-data.json and js/blocklist-data.js successfully!")
