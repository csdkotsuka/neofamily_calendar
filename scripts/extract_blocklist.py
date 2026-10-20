import json
import re
from datetime import datetime
from urllib.parse import urlparse

with open("scripts/ocr_results.json") as f:
    images_data = json.load(f)

images_data.sort(key=lambda x: x["file"])

def is_noise(t):
    t = t.strip()
    if not t or t in ["Notes", "Ca", "戻る", "編集", "完了", "共有", "投稿", "コメント"]:
        return True
    # Reaction counters like '20：', '1C：', '10…', '30：', '20', '1④', '1③…'
    if re.match(r'^[0-9①-⑳C\s：:…\.\,\_\@\(\)]+$', t):
        return True
    if re.match(r'^[0-9]+(?:\.[0-9]+)?$', t):
        return True
    return False

date_regex = re.compile(
    r'(?:'
    r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d+)(?:\s+(\d{1,2}:\d{2}\s*(?:AM|PM)?))?'
    r'|Yesterday(?:\s+at\s+(\d{1,2}:\d{2}\s*(?:AM|PM)?))?'
    r'|Today(?:\s+at\s+(\d{1,2}:\d{2}\s*(?:AM|PM)?))?'
    r'|(\d{4})年(\d{1,2})月(\d{1,2})日'
    r'|(\d{1,2})月(\d{1,2})日'
    r')', re.IGNORECASE
)

reporter_keywords = ["RAYTUS", "yuima", "ensemble", "MAARUKU", "Couleur", "enchant", "Meguria", "シャンブル", "tEaM", "秘書", "理事長", "リーダー", "スタッフ", "代表", "理事"]

def is_reporter(t):
    if ("/" in t or "／" in t) and any(k.lower() in t.lower() for k in reporter_keywords):
        return True
    return False

def clean_url(u):
    u = u.strip()
    # Normalize unicode
    u = u.replace("？", "?").replace("＆", "&").replace("＝", "=").replace("％", "%").replace("／", "/")
    u = u.replace(" ", "")
    # Typos in protocol or domain
    u = re.sub(r'^(nttps|nltps|htps|hfps|httos|https)[:：]\/*', 'https://', u, flags=re.IGNORECASE)
    u = re.sub(r'^(nttp|htip|http)[:：]\/*', 'http://', u, flags=re.IGNORECASE)
    u = re.sub(r'threaas\.com', 'threads.net', u, flags=re.IGNORECASE)
    u = re.sub(r'threads\.com', 'threads.net', u, flags=re.IGNORECASE)
    # Remove trailing junk punctuation
    u = re.sub(r'[」」\)\'\"\.#]+$', '', u)
    if not u.startswith("http"):
        if u.startswith("www."):
            u = "https://" + u
    return u

def extract_platform(url):
    u_low = url.lower()
    if "instagram.com" in u_low:
        return "Instagram"
    elif "threads.net" in u_low or "threads.com" in u_low:
        return "Threads"
    elif "facebook.com" in u_low:
        return "Facebook"
    elif "x.com" in u_low or "twitter.com" in u_low:
        return "X (Twitter)"
    elif "tiktok.com" in u_low:
        return "TikTok"
    else:
        return "Web"

def extract_account_from_url(url):
    u = clean_url(url)
    try:
        parsed = urlparse(u)
        path = parsed.path.strip("/")
        if "instagram.com" in parsed.netloc:
            parts = path.split("/")
            if parts and parts[0] not in ["p", "reel", "stories", "share"]:
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
            if path and path not in ["profile.php"]:
                return path.split("/")[0]
    except:
        pass
    return None

def normalize_date_str(raw_date):
    if not raw_date:
        return ""
    d_clean = raw_date.strip()
    # Replace Yesterday (assumes current context is Oct 20, 2026)
    if "yesterday" in d_clean.lower():
        time_part = re.search(r'(\d{1,2}:\d{2}\s*(?:AM|PM)?)', d_clean, re.I)
        t_str = f" {time_part.group(1)}" if time_part else ""
        return f"2026-10-19{t_str}"
    
    # Month name like Jun 5 11:25 AM
    months = {"jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06", 
              "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"}
    m = re.match(r'([A-Za-z]{3})[a-z]*\.?\s+(\d+)(?:\s+(\d{1,2}:\d{2}\s*(?:AM|PM)?))?', d_clean, re.I)
    if m:
        mon_str = m.group(1).lower()
        if mon_str in months:
            mm = months[mon_str]
            dd = f"{int(m.group(2)):02d}"
            time_str = f" {m.group(3)}" if m.group(3) else ""
            return f"2026-{mm}-{dd}{time_str}"
    
    return d_clean

# Parse each image into post blocks
all_raw_posts = []

for img_idx, img in enumerate(images_data):
    lines = [l["text"].strip() for l in img["lines"] if not is_noise(l["text"])]
    if not lines:
        continue
    
    # Group into posts
    # A new post boundary is marked by:
    # (a) Date line OR (b) Reporter line
    curr_post = {"date": None, "reporter": None, "lines": [], "image": img["file"]}
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if line is a date
        date_match = date_regex.search(line)
        rep_match = is_reporter(line)
        
        if (date_match or rep_match) and curr_post["lines"]:
            # Commit current post if it has substantive content (URL or text)
            all_raw_posts.append(curr_post)
            # Start new post, inheriting recent date/reporter if needed
            new_date = line if date_match else None
            new_rep = line if rep_match else None
            curr_post = {"date": new_date, "reporter": new_rep, "lines": [], "image": img["file"]}
        else:
            if date_match and not curr_post["date"]:
                curr_post["date"] = line
            elif rep_match and not curr_post["reporter"]:
                curr_post["reporter"] = line
            else:
                curr_post["lines"].append(line)
        i += 1
        
    if curr_post["lines"] or curr_post["date"] or curr_post["reporter"]:
        all_raw_posts.append(curr_post)

print(f"Total raw post blocks collected: {len(all_raw_posts)}")

# Now process raw posts: join split URLs, extract URLs, extract names and reasons
extracted_records = []

for post in all_raw_posts:
    raw_lines = post["lines"]
    post_date = normalize_date_str(post["date"])
    reporter = post["reporter"] or ""
    
    # Reassemble URLs that were split across multiple lines
    cleaned_lines = []
    idx = 0
    while idx < len(raw_lines):
        line = raw_lines[idx]
        # Check if line is URL continuation
        if idx > 0 and (line.startswith("igsh=") or line.startswith("utm_") or line.startswith("igshid=") or line.startswith("id=") or line.startswith("stkn=") or line.startswith("psIn=")):
            cleaned_lines[-1] = cleaned_lines[-1] + line
        elif idx > 0 and cleaned_lines[-1].endswith(("?", "？", "=", "＝", "&", "＆", "/")):
            cleaned_lines[-1] = cleaned_lines[-1] + line
        else:
            cleaned_lines.append(line)
        idx += 1
        
    urls = []
    text_lines = []
    
    for l in cleaned_lines:
        u_match = re.search(r'(?:https?:\/\/|www\.|nttps:\/\/|hftps:\/\/)[^\s]+', l, re.I)
        if u_match or "instagram.com" in l.lower() or "threads" in l.lower() or "facebook.com" in l.lower():
            # Extract URL part
            u_str = u_match.group(0) if u_match else l
            u_clean = clean_url(u_str)
            urls.append(u_clean)
            # If there was text before/after URL in same line
            rest = l.replace(u_str, "").strip()
            if rest and not is_noise(rest):
                text_lines.append(rest)
        else:
            if not is_noise(l) and not is_reporter(l):
                text_lines.append(l)
                
    if not urls and not text_lines:
        continue
        
    # Name extraction heuristic:
    # If text lines exist, first short line without comment indicators is often the name
    name_candidates = []
    reason_lines = []
    
    for t in text_lines:
        # Check if t is comment/reason
        is_reason = False
        if any(w in t for w in ["お断り", "勧誘", "モラハラ", "悪口", "退会", "ドタキャン", "声かけない", "ブロック", "話を聞いた", "必要ない", "営業", "zoom", "Zoom", "リスケ", "警戒", "着信", "DM", "連絡", "不信感", "事実でない", "おせっかい", "お金がない", "入る気ない"]):
            is_reason = True
        elif len(t) > 35:
            is_reason = True
            
        if is_reason:
            reason_lines.append(t)
        else:
            name_candidates.append(t)
            
    name = " / ".join(name_candidates).strip()
    reason = " ".join(reason_lines).strip()
    
    extracted_records.append({
        "date": post_date,
        "raw_date": post["date"] or "",
        "reporter": reporter,
        "urls": urls,
        "name": name,
        "reason": reason,
        "image": post["image"]
    })

print(f"Total extracted records before deduplication: {len(extracted_records)}")
