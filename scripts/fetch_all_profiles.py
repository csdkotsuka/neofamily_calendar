import json, urllib.request, re, html, time
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

with open("js/blocklist-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Fetching profile titles for {len(data)} items...")

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
    # Match Instagram / Threads format: "Display Name (@handle) • Instagram..."
    m = re.match(r'^(.*?)\s*\(@([A-Za-z0-9._]+)\)\s*[•·|-]\s*(?:Instagram|Threads).*$', t, re.I)
    if m:
        disp = m.group(1).strip()
        handle = m.group(2).strip()
        return disp if disp else f"@{handle}"
    # Also check "• Instagram" or "• Threads" without (@handle) when display name is empty
    m2 = re.match(r'^@?([A-Za-z0-9._]+)\s*[•·|-]\s*(?:Instagram|Threads).*$', t, re.I)
    if m2:
        return None
    # Facebook format
    t = re.sub(r'\s*[\|｜•·-]\s*Facebook.*$', '', t, flags=re.I).strip()
    t = re.sub(r'\s*[\|｜•·-]\s*TikTok.*$', '', t, flags=re.I).strip()
    if t.lower() in GENERIC_TITLES:
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
                if raw_og in ("Instagram", "Threads • Log in", "Threads"):
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
    
    # Extract handle to try cross-platform (IG <-> Threads) if primary fails
    for u in list(urls_to_try):
        try:
            p = urlparse(u)
            path = p.path.strip("/")
            if "threads.net" in p.netloc and path.startswith("@"):
                h = path[1:].split("/")[0]
                ig_u = f"https://www.instagram.com/{h}/"
                if ig_u not in urls_to_try:
                    urls_to_try.append(ig_u)
            elif "instagram.com" in p.netloc and path and "/" not in path:
                th_u = f"https://www.threads.net/@{path}"
                if th_u not in urls_to_try:
                    urls_to_try.append(th_u)
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

with open("scripts/fetched_profiles.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

found_count = sum(1 for v in results.values() if v["title"])
print(f"Finished! Found display names for {found_count}/{len(data)} items.")
