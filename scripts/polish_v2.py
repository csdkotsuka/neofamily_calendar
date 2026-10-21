import json, re

# Execute finalize script
exec(open("scripts/finalize_blocklist_v2.py").read())

# Date normalizer
def format_date(d_str):
    if not d_str: return ""
    d = d_str.strip()
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

for item in final_items:
    item["date"] = format_date(item["date"])
    
    # 1. Fix Facebook share URLs where share ID leaked into reason or name
    if "facebook.com/share/1" in item["url"] and len(item["url"]) <= 28:
        # Check reason
        m = re.search(r'([A-Za-z0-9_\-]{6,}\/?)', item.get("reason", ""))
        if m:
            share_id = m.group(1).strip("/")
            item["url"] = f"https://www.facebook.com/share/1{share_id}/"
            item["reason"] = item["reason"].replace(m.group(0), "").strip()
            item["url_warning"] = ""
            
    # 2. Fix salon / title names in reason that should be in name
    if "【" in item.get("reason", "") and ("サロン" in item["reason"] or "セラピスト" in item["reason"] or "善明みなみ" in item["reason"]):
        # Move it to name
        title_text = re.sub(r'[\s\/／]+$', '', item["reason"]).strip()
        item["name"] = title_text
        item["reason"] = ""

    # 3. Clean up trailing / leading slashes and whitespace
    item["name"] = re.sub(r'[\s\/／]+$', '', item["name"]).strip()
    item["name"] = re.sub(r'^[\s\/／]+', '', item["name"]).strip()
    if not item["name"]:
        item["name"] = f"@{item['account_id']}" if item.get("account_id") else "（名称未記載）"

    # 4. Clean reason
    if item.get("reason"):
        item["reason"] = item["reason"].strip()
        # If reason is just punctuation
        if re.match(r'^[、。\.\s\-・]+$', item["reason"]):
            item["reason"] = ""

    # 5. Check broken link condition
    # e.g., missing account name in instagram/threads, or generic facebook share without id
    u = item["url"]
    if "facebook.com/share/1" in u and len(u) <= 28:
        item["url_warning"] = "⚠️ 共有ID欠落（リンク切れの可能性）"
    elif u.rstrip("/").endswith("instagram.com") or u.rstrip("/").endswith("threads.net"):
        item["url_warning"] = "⚠️ アカウントURL不完全"
    elif "facebook.com/profile.php" in u and "id=" not in u:
        item["url_warning"] = "⚠️ プロフィールID欠落"

# Save dataset
with open("js/blocklist-data.json", "w", encoding="utf-8") as f:
    json.dump(final_items, f, ensure_ascii=False, indent=2)

with open("js/blocklist-data.js", "w", encoding="utf-8") as f:
    f.write("/**\n * NEO FAMILY Calendar - Blocklist Data (Verified & Cleaned v2)\n")
    f.write(" * Total items: " + str(len(final_items)) + "\n */\n")
    f.write("const INITIAL_BLOCKLIST = " + json.dumps(final_items, ensure_ascii=False, indent=2) + ";\n")

print(f"\nSaved {len(final_items)} cleaned items to js/blocklist-data.json and js/blocklist-data.js")
