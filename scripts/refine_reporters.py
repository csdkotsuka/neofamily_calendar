import json, re

with open("js/blocklist-data.json") as f:
    data = json.load(f)

# True NEO team names
OFFICIAL_TEAMS = [
    "RAYTUS", "yuima-ru", "yuima", "ensemble", "MAARUKU", "MAARUKU.NEO",
    "Couleur", "enchant+", "enchant", "Meguria", "シャンブルカーサ", "シャンブル",
    "shAdow", "MURA", "AMATERAS", "CHOICE", "Ablaze", "Lumiere.", "Lumiere",
    "Blooming", "Mimola", "碧春", "tEaM_S.", "tEaM", "秘書課", "事務局", "理事長", "代表"
]

def is_true_official_reporter(text):
    if not text: return False
    t = text.replace("／", "/").replace("＼", "/").replace("\\", "/")
    # Must contain one of the official team names
    for team in OFFICIAL_TEAMS:
        if team.lower() in t.lower():
            # Exclude if it looks like an external business/address e.g. "滋賀彦根"
            if "彦根" in t or "サロン" in t or "セラピスト" in t or "http" in t:
                return False
            return True
    return False

for item in data:
    rep = item.get("reporter", "")
    
    # If reporter is not a true official team member (e.g. "BofZG3uWH" or "善明みなみ（滋賀彦根 / 多賀町）")
    if not is_true_official_reporter(rep):
        # Case A: Facebook share ID leaked as reporter
        if re.match(r'^[A-Za-z0-9_\-]{6,}$', rep.strip()):
            if "facebook.com/share/1" in item["url"]:
                item["url"] = f"https://www.facebook.com/share/1{rep.strip()}/"
                item["url_warning"] = ""
            item["reporter"] = "本多栞（RAYTUS / 秘書課）"
        # Case B: Target person profile leaked as reporter
        elif "善明みなみ" in rep:
            item["reporter"] = "本多栞（RAYTUS / 秘書課）"
            # prepend to reason
            item["reason"] = f"【ラクにキレイを叶える専門サロン】 hamien／ラク痩せ＆小顔セラピスト 善明みなみ/滋賀彦根／多賀町 {item['reason']}".strip()
        else:
            # Fallback to general admin/secretary
            item["reporter"] = "本多栞（RAYTUS / 秘書課）"

    # Also clean up URL query leftovers in reason e.g. " ？ igsh=..."
    if item.get("reason"):
        r = item["reason"]
        # If url has no query, but query is at the end of reason
        q_match = re.search(r'\s*([?？]\s*(?:igsh|utm_|igshid|stkn|psin|id=)[A-Za-z0-9_\-%=&\s]+)$', r)
        if q_match:
            query_part = q_match.group(1).replace("？", "?").replace(" ", "")
            if "?" not in item["url"]:
                item["url"] = item["url"] + query_part
            r = r[:q_match.start()].strip()
            
        # Clean double spaces
        r = re.sub(r'\s+', ' ', r).strip()
        item["reason"] = r

    # If Facebook profile.php has id in reason
    if "facebook.com/profile.php" in item["url"] and "?" not in item["url"]:
        id_m = re.search(r'id=(\d+)', item.get("reason", ""))
        if id_m:
            item["url"] = f"https://www.facebook.com/profile.php?id={id_m.group(1)}"
            item["reason"] = re.sub(r'[?？]?\s*id=\d+#?', '', item["reason"]).strip()

with open("js/blocklist-data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("js/blocklist-data.js", "w", encoding="utf-8") as f:
    f.write("/**\n * NEO FAMILY Calendar - Blocklist Data (v3 Verified Cleaned)\n")
    f.write(" * Total items: " + str(len(data)) + "\n */\n")
    f.write("const INITIAL_BLOCKLIST = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n")

print("Reporters and URLs refined successfully!")
