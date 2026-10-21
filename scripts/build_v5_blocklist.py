import json, urllib.request, re, html
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

with open("js/blocklist-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Loaded {len(data)} clean items from HEAD.")

# Step 1: Fix ONLY genuinely concatenated second https:// URLs or non-ASCII Japanese text glued to URLs
fixed_url_count = 0
for item in data:
    u = item.get("url", "")
    # 1a. Two https:// URLs glued together
    m_two = re.match(r'^(https?:\/\/.+?)(https?:\/\/.+)$', u)
    if m_two:
        u1 = m_two.group(1).rstrip("/")
        u2 = m_two.group(2)
        if "mika_ombremor" in u1 and "mika_ombremoi" in u2:
            u1 = u1.replace("mika_ombremor", "mika_ombremoi")
        item["url"] = u1
        if not item.get("secondary_url"):
            item["secondary_url"] = u2
        u = u1
        fixed_url_count += 1

    # 1b. Glued date string like Twodaysagoat9:12AM
    m_dt = re.match(r'^(https?:\/\/.+?)(Twodaysago.*|Yesterday.*|Today.*)$', u, re.I)
    if m_dt:
        item["url"] = m_dt.group(1)
        u = item["url"]
        fixed_url_count += 1

    # 1c. Glued Japanese text (including "MLMに誘ってきます！")
    m_mlm = re.match(r'^(https?:\/\/(?:www\.)?instagram\.com\/[A-Za-z0-9._]+\/)(MLM[^\x00-\x7F].*)$', u)
    if m_mlm:
        item["url"] = m_mlm.group(1)
        extra = m_mlm.group(2).strip()
        if extra not in (item.get("reason") or ""):
            item["reason"] = (extra + " " + (item.get("reason") or "")).strip()
        u = item["url"]
        fixed_url_count += 1

    m_non_ascii = re.match(r'^([\x00-\x7F]+?)([^\x00-\x7F].*)$', u)
    if m_non_ascii:
        item["url"] = m_non_ascii.group(1)
        extra = m_non_ascii.group(2).strip()
        if extra not in (item.get("reason") or ""):
            item["reason"] = (extra + " " + (item.get("reason") or "")).strip()
        u = item["url"]
        fixed_url_count += 1

print(f"Step 1 complete: Fixed {fixed_url_count} glued URLs.")

GENERIC_TITLES = {
    "instagram", "threads", "threads • log in", "threads • ログイン",
    "ログイン • instagram", "facebook", "page not found",
    "このページを見るには、ログインまたは登録してください",
    "log in or sign up to view", "コンテンツは現在利用できません",
    "ページが見つかりません"
}

def extract_clean_title(raw_title):
    if not raw_title:
        return None
    t = html.unescape(raw_title).strip()
    t = re.sub(r'\s+', ' ', t)
    tl = t.lower()
    if tl in GENERIC_TITLES:
        return None
    if any(p in tl for p in ["threads • ログイン", "threads • log in", "ログイン • instagram", "このページを見るには", "log in or sign up", "page not found"]):
        return None
    # Match "Threadsの○○ (@handle)"
    m_th = re.match(r'^Threadsの(.+?)\s*(?:\(@[A-Za-z0-9._]+\))?$', t)
    if m_th:
        return m_th.group(1).strip()
    # Match Instagram / Threads format: "Display Name (@handle) • Instagram..."
    m = re.match(r'^(.*?)\s*\(@([A-Za-z0-9._]+)\)\s*[•·|-]\s*(?:Instagram|Threads).*$', t, re.I)
    if m:
        disp = m.group(1).strip()
        return disp if disp else None
    # Check "• Instagram" or "• Threads" without (@handle)
    m2 = re.match(r'^@?([A-Za-z0-9._]+)\s*[•·|-]\s*(?:Instagram|Threads).*$', t, re.I)
    if m2:
        return None
    # Facebook / TikTok format
    t = re.sub(r'\s*[\|｜•·-]\s*(?:Facebook|TikTok|Instagram|Threads).*$', '', t, flags=re.I).strip()
    t = re.sub(r'\s*\(@[A-Za-z0-9._]+\)\s*$', '', t).strip()
    if t.lower() in GENERIC_TITLES or not t:
        return None
    return t

def fetch_url_title(u):
    if not u or not u.startswith("http"):
        return None, "invalid"
    for ua in ["facebookexternalhit/1.1", "Twitterbot/1.0"]:
        try:
            req = urllib.request.Request(u, headers={
                "User-Agent": ua,
                "Accept-Language": "ja,en-US;q=0.9,en;q=0.8"
            })
            with urllib.request.urlopen(req, timeout=7) as r:
                body = r.read(98304).decode("utf-8", errors="ignore")
                og = re.search(r'property=["\']og:title["\']\s+content=["\'](.*?)["\']', body, re.I) or \
                     re.search(r'content=["\'](.*?)["\']\s+property=["\']og:title["\']', body, re.I) or \
                     re.search(r'name=["\']twitter:title["\']\s+content=["\'](.*?)["\']', body, re.I)
                if og:
                    cleaned = extract_clean_title(og.group(1))
                    if cleaned:
                        return cleaned, "ok"
                t = re.search(r'<title[^>]*>(.*?)</title>', body, re.S | re.I)
                if t:
                    cleaned = extract_clean_title(t.group(1))
                    if cleaned:
                        return cleaned, "ok"
                raw_og = html.unescape(og.group(1)).strip() if og else (html.unescape(t.group(1)).strip() if t else "")
                if any(x in raw_og.lower() for x in ["instagram", "threads • log in", "threads • ログイン"]):
                    return None, "not_found_or_private"
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None, "404"
        except Exception:
            pass
    return None, "unresolved"

def process_item(item):
    urls_to_try = []
    u1 = item.get("url", "")
    u2 = item.get("secondary_url", "")
    if u1: urls_to_try.append(u1)
    if u2: urls_to_try.append(u2)
    
    for u in list(urls_to_try):
        try:
            p = urlparse(u)
            path = p.path.strip("/")
            if "threads.net" in p.netloc and path.startswith("@"):
                h = path[1:].split("/")[0]
                for cand in [f"https://www.threads.net/@{h}", f"https://www.instagram.com/{h}/"]:
                    if cand not in urls_to_try:
                        urls_to_try.append(cand)
            elif "instagram.com" in p.netloc and path:
                h = path.split("/")[0]
                if h not in ("p", "reel", "share", "stories", "explore"):
                    for cand in [f"https://www.instagram.com/{h}/", f"https://www.threads.net/@{h}"]:
                        if cand not in urls_to_try:
                            urls_to_try.append(cand)
        except Exception:
            pass

    statuses = []
    for u in urls_to_try:
        title, st = fetch_url_title(u)
        statuses.append(st)
        if title:
            return item["id"], title, "ok"
    return item["id"], None, statuses[0] if statuses else "none"

results = {}
done = 0
with ThreadPoolExecutor(max_workers=25) as ex:
    futures = {ex.submit(process_item, item): item["id"] for item in data}
    for fut in as_completed(futures):
        iid, title, status = fut.result()
        results[iid] = {"title": title, "status": status}
        done += 1
        if done % 100 == 0 or done == len(data):
            print(f"  Progress: {done}/{len(data)}")

updated_names = 0
for item in data:
    iid = item["id"]
    res = results.get(iid, {})
    title = res.get("title")
    if title:
        item["name"] = title
        updated_names += 1
        # If reason was just the profile name itself, clear duplicate from reason
        r = (item.get("reason") or "").strip()
        if r:
            norm_r = re.sub(r'[\s\u3000／/｜|・]', '', r).lower()
            norm_t = re.sub(r'[\s\u3000／/｜|・]', '', title).lower()
            if norm_r == norm_t or (len(norm_r) > 4 and norm_r in norm_t):
                item["reason"] = ""
    else:
        st = res.get("status", "")
        if st in ("404", "not_found_or_private") and not item.get("url_warning"):
            item["url_warning"] = "リンク切れ/非公開"

with open("js/blocklist-data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("js/blocklist-data.js", "w", encoding="utf-8") as f:
    f.write("/**\n * NEO FAMILY Calendar - Blocklist Data (v5 Enriched Profile Names)\n")
    f.write(" * Total items: " + str(len(data)) + "\n */\n")
    f.write("var INITIAL_BLOCKLIST = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n")

print(f"All done! Updated {updated_names}/{len(data)} items with real profile display names.")
