import json, re, urllib.request, html
from urllib.parse import urlparse

with open("js/blocklist-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("scripts/fetched_profiles.json", "r", encoding="utf-8") as f:
    fetched = json.load(f)

from fetch_all_profiles import fetch_url_title

fixed_urls = 0
for item in data:
    u = item.get("url", "")
    # 1. Check if two URLs are concatenated inside u
    second_http = re.search(r'(https?:\/\/.+?)(https?:\/\/.+)', u)
    if second_http:
        u1 = second_http.group(1).strip()
        u2 = second_http.group(2).strip()
        item["url"] = u1
        if not item.get("secondary_url"):
            item["secondary_url"] = u2
        u = u1
        fixed_urls += 1

    # 2. Check if "Twodaysago..." or "Yesterday..." is glued to the end of u
    m_date = re.search(r'(https?:\/\/[^\s]+?)(Twodaysago.*|Yesterday.*|Today.*)$', u, re.I)
    if m_date:
        item["url"] = m_date.group(1)
        u = item["url"]
        fixed_urls += 1

    # 3. Check if non-ASCII (Japanese text) is glued to the end of u
    m_jp = re.match(r'^([A-Za-z0-9\-._~:/?#\[\]@!$&\'()*+,;%=]+)(.+)$', u)
    if m_jp:
        clean_u = m_jp.group(1)
        extra_text = m_jp.group(2).strip()
        item["url"] = clean_u
        if extra_text and extra_text not in (item.get("reason") or ""):
            item["reason"] = (extra_text + " " + (item.get("reason") or "")).strip()
        u = clean_u
        fixed_urls += 1

    # Same for secondary_url
    u2 = item.get("secondary_url", "")
    if u2:
        m_jp2 = re.match(r'^([A-Za-z0-9\-._~:/?#\[\]@!$&\'()*+,;%=]+)(.+)$', u2)
        if m_jp2:
            item["secondary_url"] = m_jp2.group(1)
            extra2 = m_jp2.group(2).strip()
            if extra2 and extra2 not in (item.get("reason") or ""):
                item["reason"] = (extra2 + " " + (item.get("reason") or "")).strip()
            fixed_urls += 1

print(f"Fixed {fixed_urls} concatenated/glued URLs.")

# Re-fetch for any item that didn't have a title yet
newly_found = 0
for item in data:
    iid = item["id"]
    if fetched.get(iid, {}).get("title"):
        continue
    urls_to_try = [item.get("url", ""), item.get("secondary_url", "")]
    for u in list(urls_to_try):
        if not u: continue
        p = urlparse(u)
        path = p.path.strip("/")
        if "threads.net" in p.netloc and path.startswith("@"):
            h = path[1:].split("/")[0]
            urls_to_try.append(f"https://www.threads.net/@{h}")
            urls_to_try.append(f"https://www.instagram.com/{h}/")
        elif "instagram.com" in p.netloc and path:
            h = path.split("/")[0]
            if h not in ("p", "reel", "share", "stories"):
                urls_to_try.append(f"https://www.instagram.com/{h}/")
                urls_to_try.append(f"https://www.threads.net/@{h}")
    for u in urls_to_try:
        if not u: continue
        title, st = fetch_url_title(u)
        if title:
            fetched[iid] = {"title": title, "status": "ok"}
            newly_found += 1
            print(f"  Newly resolved {iid}: {title} (from {u})")
            break

with open("scripts/fetched_profiles.json", "w", encoding="utf-8") as f:
    json.dump(fetched, f, ensure_ascii=False, indent=2)

with open("js/blocklist-data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Newly found {newly_found} profile titles!")
