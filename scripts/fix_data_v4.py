import json, re
from urllib.parse import urlparse

with open("js/blocklist-data.json") as f:
    data = json.load(f)

print(f"Loaded {len(data)} items.")

# 1. Domain typos repair (facepook, facehook, etc.)
for item in data:
    u = item.get("url", "")
    # Fix facepook, facehook, etc.
    if "facepook.com" in u.lower() or "facehook.com" in u.lower():
        u = re.sub(r'face[ph]ook\.com', 'facebook.com', u, flags=re.I)
        item["url"] = u
        item["platform"] = "Facebook"
        
    # Fix share/I -> share/1
    if "facebook.com/share/I" in item["url"]:
        item["url"] = item["url"].replace("/share/I", "/share/1")

    # 2. Re-attach URL parameters and continuations leaking into reason
    r = item.get("reason", "")
    if r:
        # Check if reason starts with or contains URL parameters
        # e.g. "？ mibextid=wwXlfr 一回お話し聞いていて..."
        # or "?igsh=... " or "share/1..."
        
        # Match parameter at start: e.g. "^[?？&＆]?\s*(mibextid|igsh|igshid|utm_|stkn|psin|obrf|dirf|dllrf|rpxt|srtk|exin|cpik|xtok|id=)[=\sA-Za-z0-9_\-%]+"
        p_match = re.match(r'^[?？&＆]?\s*((?:mibextid|igsh|igshid|utm_source|utm_medium|stkn|psin|obrf|dirf|dllrf|rpxt|srtk|exin|cpik|xtok|id)[=＝][A-Za-z0-9_\-%=]+)(.*)', r, re.I)
        if p_match:
            param_str = p_match.group(1).replace("＝", "=")
            rest_reason = p_match.group(2).strip()
            # Append to URL
            sep = "&" if "?" in item["url"] else "?"
            item["url"] = item["url"] + sep + param_str
            item["reason"] = rest_reason
            r = rest_reason
            
        # Also check anywhere inside reason if there's a standalone URL continuation
        # e.g. "? mibextid=wwXlfr"
        m2 = re.search(r'[?？]\s*((?:mibextid|igsh|igshid|stkn|psin|id=)[A-Za-z0-9_\-%=]+)', r)
        if m2:
            param_str = m2.group(1)
            sep = "&" if "?" in item["url"] else "?"
            if param_str.split("=")[0] not in item["url"]:
                item["url"] = item["url"] + sep + param_str
            r = r.replace(m2.group(0), "").strip()
            item["reason"] = r

        # Clean trailing/leading question marks or junks in reason
        item["reason"] = re.sub(r'^[?？\s]+', '', item["reason"]).strip()

    # 3. Simplify warning messages for compact UI
    w = item.get("url_warning", "")
    if w:
        if "プロトコル" in w or "nttps" in w or "threaas" in w:
            item["url_warning"] = "修復済"
        elif "共有ID欠落" in w or "ID欠落" in w:
            item["url_warning"] = "ID欠落"
        elif "不完全" in w or "欠損" in w:
            item["url_warning"] = "URL不完全"
        elif "形式異常" in w:
            item["url_warning"] = "形式注意"
        else:
            item["url_warning"] = "注意"

# 4. Sort strictly chronologically (古い順にソート)
def parse_date_for_sort(d_str):
    if not d_str:
        return "9999-99-99 99:99"
    # Format e.g. "2026-06-05 11:25 AM" or "2026-10-19"
    parts = d_str.strip().split()
    date_part = parts[0]
    time_part = "00:00"
    if len(parts) >= 2:
        # e.g. 11:25 AM
        t_raw = " ".join(parts[1:])
        m = re.match(r'(\d{1,2}):(\d{2})(?:\s*(AM|PM))?', t_raw, re.I)
        if m:
            h = int(m.group(1))
            minute = int(m.group(2))
            ampm = m.group(3)
            if ampm:
                if ampm.upper() == "PM" and h < 12: h += 12
                if ampm.upper() == "AM" and h == 12: h = 0
            time_part = f"{h:02d}:{minute:02d}"
    return f"{date_part} {time_part}"

data.sort(key=lambda x: parse_date_for_sort(x.get("date", "")))

# 5. Renumber chronologically from blk_001
for idx, item in enumerate(data, 1):
    item["id"] = f"blk_{idx:03d}"

print(f"Renumbered {len(data)} items chronologically.")
print("Sample first 5 items (oldest):")
for item in data[:5]:
    print(f"[{item['id']}] Date: {item['date']} | Name: {item['name']} | URL: {item['url']}")
    print(f"  Reason: {item['reason']}")

print("\nSample last 5 items (newest):")
for item in data[-5:]:
    print(f"[{item['id']}] Date: {item['date']} | Name: {item['name']} | URL: {item['url']}")

# Save
with open("js/blocklist-data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("js/blocklist-data.js", "w", encoding="utf-8") as f:
    f.write("/**\n * NEO FAMILY Calendar - Blocklist Data (v4 Chronological)\n")
    f.write(" * Total items: " + str(len(data)) + "\n */\n")
    f.write("const INITIAL_BLOCKLIST = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n")

print("Saved clean chronological dataset to js/blocklist-data.json and js/blocklist-data.js!")
