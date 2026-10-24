import json, re

with open("scripts/candidate_titles.json") as f:
    items = json.load(f)

# Exclude c9, c12_c, c16, c17, c18
excluded = {"c9", "c12_c", "c16", "c17", "c18"}
valid_items = [item for item in items if item["cand_id"] not in excluded]

print(f"Valid new items count: {len(valid_items)}")

with open("js/blocklist-data.json") as f:
    existing = json.load(f)

# Check all handles and urls against existing
existing_urls = set()
for e in existing:
    u1 = e.get("url", "")
    u2 = e.get("secondary_url", "")
    if u1: existing_urls.add(u1.split("?")[0].rstrip("/").lower())
    if u2: existing_urls.add(u2.split("?")[0].rstrip("/").lower())

for idx, item in enumerate(valid_items):
    u1_base = item["url"].split("?")[0].rstrip("/").lower()
    u2_base = item["secondary_url"].split("?")[0].rstrip("/").lower() if item.get("secondary_url") else None
    
    if u1_base in existing_urls:
        print(f"WARNING: u1 {u1_base} in existing!")
    if u2_base and u2_base in existing_urls:
        print(f"WARNING: u2 {u2_base} in existing!")
        
    print(f"[{idx+1:02d}] {item['date']} | {item['reporter']} | {item['fetched_title']} | {item['url']}")
