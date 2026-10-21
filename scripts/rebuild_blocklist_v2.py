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
    if x > 0.75: # reaction counters on right
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

reporter_keywords = ["RAYTUS", "yuima", "ensemble", "MAARUKU", "Couleur", "enchant", "Meguria", "シャンブル", "tEaM", "秘書", "理事長", "リーダー", "スタッフ", "代表", "理事", "事務局", "Mimola", "Blooming", "Lumiere"]

def is_reporter_line(t):
    t_clean = t.replace("／", "/").replace("＼", "/").replace("\\", "/")
    if "/" in t_clean and any(k.lower() in t_clean.lower() for k in reporter_keywords):
        if "http" not in t.lower() and not re.search(r'\d{4}\/\d', t):
            return True
    return False

def parse_reporter_details(t):
    if not t:
        return {"name": "管理部", "dept": "秘書課", "display": "管理部（秘書課）"}
    t_clean = t.replace("／", "/").replace("＼", "/").replace("\\", "/")
    parts = [p.strip() for p in t_clean.split("/") if p.strip()]
    if not parts:
        return {"name": "管理部", "dept": "", "display": "管理部"}
        
    name = parts[0]
    if name == "本多菜": name = "本多栞"
    if name.startswith("本多"): name = "本多栞"
    
    dept_parts = parts[1:]
    dept = " / ".join(dept_parts) if dept_parts else ""
    display = f"{name}（{dept}）" if dept else name
    return {"name": name, "dept": dept, "display": display}

def clean_and_normalize_url(u):
    raw = u.strip()
    warning = None
    
    # Check for known typos in scheme / domain
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

    # Unicode normalization
    raw = raw.replace("？", "?").replace("＆", "&").replace("＝", "=").replace("％", "%").replace("／", "/")
    raw = raw.replace(" ", "")
    
    # Strip trailing punctuation
    raw = re.sub(r'[」」\)\'\"\.#]+$', '', raw)
    
    if not raw.startswith("http"):
        if raw.startswith("www."):
            raw = "https://" + raw

    # Validate completeness
    try:
        parsed = urlparse(raw)
        path = parsed.path.strip("/")
        if "instagram.com" in parsed.netloc:
            if not path or path in ["p", "reel", "stories", "share", "explore"]:
                warning = "⚠️ URL不完全（アカウント名欠損）"
        elif "threads" in parsed.netloc:
            if not path or path in ["share"]:
                warning = "⚠️ URL不完全（アカウント名欠損）"
        elif "facebook.com" in parsed.netloc:
            if path == "share/1" or path == "share":
                warning = "⚠️ URL不完全（共有ID欠落）"
    except Exception:
        warning = "⚠️ URL形式異常"

    return raw, warning

def get_platform_name(url):
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
    try:
        parsed = urlparse(url)
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

def is_reason_text(t):
    # Clearly a reason/comment, NOT a person name
    reason_words = [
        "お断り", "勧誘", "モラハラ", "悪口", "退会", "ドタキャン", "声かけない", "ブロック", 
        "話を聞いた", "必要ない", "営業", "zoom", "Zoom", "リスケ", "警戒", "着信", "DM", 
        "連絡", "不信感", "事実でない", "おせっかい", "お金がない", "入る気ない", "煽る", 
        "マウント", "文面", "メッセージ", "失業手当", "無職", "変わった人", "ネガティブ", 
        "クレーム", "トラブル", "迷惑", "辞退", "注意", "注意喚起", "危険", "怪しい", 
        "通報", "嫌がらせ", "コメント", "愚痴", "晒され", "魅力を感じ", "盛り上がって",
        "自己紹介", "親のお金", "大ファン", "泣いて喜んで", "退会してました", "同感です",
        "被害者", "目を覚まし", "ぶったぎり", "とても失礼", "掲載の方", "私の店"
    ]
    if any(w in t for w in reason_words):
        return True
    if len(t) > 25:
        return True
    if t.endswith(("。", "！", "!", "ました", "ください", "ません", "でした", "です", "ます", "とのこと", "そうです", "人です", "ペ", "い）")):
        return True
    return False

def is_clean_person_name(t):
    # Filter out label tags
    if t in ["（threads）", "（インスタ）", "(threads)", "(インスタ)", "（Threads）", "（Instagram）", "【インスタ】", "【threads】"]:
        return False
    if is_reason_text(t):
        return False
    # If contains title brackets like 【ラクにキレイを叶える専門サロン】 or name with title
    if "【" in t and "】" in t:
        return True
    # Typical name or business name
    if len(t) <= 25 and not any(ch in t for ch in ["http", ".com", ".net", "www", "/", "\\"]):
        return True
    return False

# Group lines per image into posts
posts = []

for img in images_data:
    sorted_lines = sorted(img["lines"], key=lambda l: l["y"])
    valid_lines = [l["text"].strip() for l in sorted_lines if not is_noise(l["text"], l["x"])]
    if not valid_lines:
        continue
        
    curr_post = {"date": "", "reporter": "", "lines": [], "image": img["file"]}
    
    for line in valid_lines:
        if date_regex.match(line):
            if curr_post["lines"]:
                posts.append(curr_post)
                curr_post = {"date": line, "reporter": "", "lines": [], "image": img["file"]}
            else:
                curr_post["date"] = line
        elif is_reporter_line(line):
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

print(f"Total raw posts collected: {len(posts)}")

# Reconstruct URLs and clean up posts
cleaned_records = []

for p in posts:
    lines = p["lines"]
    
    # Connect broken URL lines
    merged_lines = []
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        
        # Check if line is Facebook share broken across lines
        if merged_lines and "facebook.com/share/1" in merged_lines[-1] and not merged_lines[-1].endswith("/"):
            # Check if this line is the rest of Facebook share ID (e.g. BofZG3uWH/)
            m = re.match(r'^([A-Za-z0-9_\-]{6,}\/?)(.*)', line)
            if m:
                merged_lines[-1] = merged_lines[-1] + m.group(1)
                rest = m.group(2).strip()
                if rest:
                    merged_lines.append(rest)
                idx += 1
                continue
                
        # Check if line is URL continuation
        is_url_cont = False
        t_clean = line.replace(" ", "").lower()
        if any(t_clean.startswith(prefix) for prefix in ["igsh=", "utm_", "igshid=", "id=", "stkn=", "psin=", "xnw==", "mibextid="]):
            is_url_cont = True
        elif merged_lines and any(u in merged_lines[-1].lower() for u in ["http://", "https://", "nttps://", "instagram.com", "threads", "facebook.com"]):
            if merged_lines[-1].endswith(("?", "？", "=", "＝", "&", "＆", "/", "#")) or is_url_cont:
                is_url_cont = True
            elif len(t_clean) < 40 and re.match(r'^[a-z0-9\=\_\%\-\&\?]+$', t_clean, re.I):
                is_url_cont = True

        if is_url_cont and merged_lines:
            merged_lines[-1] = merged_lines[-1] + line.replace(" ", "")
        else:
            merged_lines.append(line)
        idx += 1

    # Extract URLs and text
    raw_urls = []
    text_chunks = []
    
    for l in merged_lines:
        u_match = re.search(r'(?:https?:\/\/|www\.|nttps:\/\/|hftps:\/\/)[^\s]+', l, re.I)
        if u_match:
            u_str = u_match.group(0)
            raw_urls.append(u_str)
            rest = l.replace(u_str, "").strip()
            if rest and not is_noise(rest, 0):
                text_chunks.append(rest)
        elif any(domain in l.lower() for domain in ["instagram.com", "threads.net", "threads.com", "facebook.com"]):
            raw_urls.append(l)
        else:
            text_chunks.append(l)

    # CRITICAL: If NO URL, IGNORE this post (per user instruction: URLがない人は登録する意味がない)
    if not raw_urls:
        continue

    # Process and normalize URLs
    processed_urls = []
    for u in raw_urls:
        c_url, warn = clean_and_normalize_url(u)
        processed_urls.append({"url": c_url, "warning": warn, "platform": get_platform_name(c_url)})

    # Reporter parsing
    rep_info = parse_reporter_details(p["reporter"])

    # Separate Names vs Reasons
    name_candidates = []
    reason_candidates = []

    for t in text_chunks:
        if is_clean_person_name(t):
            name_candidates.append(t)
        else:
            if t not in ["（threads）", "（インスタ）", "(threads)", "(インスタ)", "【インスタ】", "【threads】"]:
                reason_candidates.append(t)

    target_name = " / ".join(name_candidates).strip()
    reason_memo = " ".join(reason_candidates).strip()

    cleaned_records.append({
        "date": p["date"] or "",
        "reporter_name": rep_info["name"],
        "reporter_dept": rep_info["dept"],
        "reporter_display": rep_info["display"],
        "urls": processed_urls,
        "name": target_name,
        "reason": reason_memo,
        "image": p["image"]
    })

print(f"Posts with valid URLs extracted: {len(cleaned_records)}")
