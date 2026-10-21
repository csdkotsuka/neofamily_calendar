import json, re
from urllib.parse import urlparse
from fetch_all_profiles import fetch_url_title

with open("js/blocklist-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("scripts/fetched_profiles.json", "r", encoding="utf-8") as f:
    fetched = json.load(f)

INVALID_TITLES = {
    "instagram", "threads", "threads • log in", "threads • ログイン",
    "ログイン • instagram", "facebook", "page not found",
    "このページを見るには、ログインまたは登録してください",
    "log in or sign up to view", "コンテンツは現在利用できません",
    "ページが見つかりません"
}

def is_valid_title(t):
    if not t:
        return False
    tl = t.strip().lower()
    if tl in INVALID_TITLES:
        return False
    if "threads • ログイン" in tl or "threads • log in" in tl or "ログイン • instagram" in tl:
        return False
    if "このページを見るには" in tl or "log in or sign up" in tl:
        return False
    return True

def clean_title_str(t):
    t = t.strip()
    # Clean "Threadsの○○ (@handle)" -> "○○"
    m = re.match(r'^Threadsの(.+?)\s*(?:\(@[A-Za-z0-9._]+\))?$', t)
    if m:
        t = m.group(1).strip()
    # Clean trailing "(@handle)" if still present
    t = re.sub(r'\s*\(@[A-Za-z0-9._]+\)\s*$', '', t).strip()
    return t

fixed_url_count = 0
updated_name_count = 0

for item in data:
    iid = item["id"]
    u = item.get("url", "")

    # 1. Split concatenated second https:// URL
    m_two = re.match(r'^(https?:\/\/.+?)(https?:\/\/.+)$', u)
    if m_two:
        u1 = m_two.group(1).rstrip("/")
        u2 = m_two.group(2)
        item["url"] = u1
        if not item.get("secondary_url"):
            item["secondary_url"] = u2
        u = u1
        fixed_url_count += 1

    # 2. Split glued date string like Twodaysagoat9:12AM
    m_dt = re.match(r'^(https?:\/\/.+?)(Twodaysago.*|Yesterday.*|Today.*)$', u, re.I)
    if m_dt:
        item["url"] = m_dt.group(1)
        u = item["url"]
        fixed_url_count += 1

    # 3. Split glued Japanese text (including ASCII prefix like "MLM" before Japanese text after a slash)
    m_mlm = re.match(r'^(https?:\/\/(?:www\.)?instagram\.com\/[A-Za-z0-9._]+\/)(MLM[^\x00-\x7F].*)$', u)
    if m_mlm:
        item["url"] = m_mlm.group(1)
        extra = m_mlm.group(2).strip()
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

    # Re-fetch for the cleaned URL if needed
    res = fetched.get(iid, {})
    title = res.get("title")
    if not is_valid_title(title):
        title = None
        if fixed_url_count > 0 and iid in ("blk_113", "blk_118", "blk_202", "blk_210", "blk_240", "blk_302", "blk_329", "blk_336", "blk_451", "blk_484", "blk_513", "blk_691"):
            for try_u in [item.get("url", ""), item.get("secondary_url", "")]:
                if not try_u: continue
                t_new, _ = fetch_url_title(try_u)
                if is_valid_title(t_new):
                    title = t_new
                    break

    if is_valid_title(title):
        clean_t = clean_title_str(title)
        if clean_t:
            item["name"] = clean_t
            updated_name_count += 1

            # Check if reason was just the profile name itself (from screenshot OCR)
            r = (item.get("reason") or "").strip()
            if r:
                norm_r = re.sub(r'[\s\u3000／/｜|・]', '', r).lower()
                norm_t = re.sub(r'[\s\u3000／/｜|・]', '', clean_t).lower()
                if norm_r == norm_t or (len(norm_r) > 4 and norm_r in norm_t):
                    item["reason"] = ""
    else:
        # Check if URL is broken / account not found
        st = res.get("status", "")
        if st in ("404", "not_found_or_private") and not item.get("url_warning"):
            item["url_warning"] = "リンク切れ/非公開"

with open("js/blocklist-data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("js/blocklist-data.js", "w", encoding="utf-8") as f:
    f.write("/**\n * NEO FAMILY Calendar - Blocklist Data (v5 Enriched Profile Names)\n")
    f.write(" * Total items: " + str(len(data)) + "\n */\n")
    f.write("var INITIAL_BLOCKLIST = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n")

print(f"Done! Fixed {fixed_url_count} glued URLs, updated {updated_name_count}/{len(data)} items with real profile display names.")
