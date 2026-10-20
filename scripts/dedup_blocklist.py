import json
import re
from urllib.parse import urlparse, urlunparse

with open("scripts/ocr_results.json") as f:
    images_data = json.load(f)

# Import the extraction logic
exec(open("scripts/extract_blocklist.py").read())

def get_canonical_url(u):
    if not u:
        return ""
    try:
        # Strip trailing ? or / or params
        parsed = urlparse(u)
        path = parsed.path.rstrip("/")
        # Ignore tracking params for dedup
        netloc = parsed.netloc.lower().replace("www.", "")
        if "threads" in netloc:
            netloc = "threads.net"
        return f"{netloc}{path}".lower()
    except:
        return u.lower()

# Expand records that contain multiple unrelated URLs, or group if same person
expanded_records = []
for r in extracted_records:
    urls = r["urls"]
    if not urls:
        # Record with no URL but has name/reason
        if r["name"] or r["reason"]:
            expanded_records.append({
                "date": r["date"],
                "reporter": r["reporter"],
                "name": r["name"],
                "url": "",
                "secondary_url": "",
                "platform": "その他",
                "reason": r["reason"],
                "image": r["image"]
            })
    elif len(urls) == 1:
        u = urls[0]
        expanded_records.append({
            "date": r["date"],
            "reporter": r["reporter"],
            "name": r["name"],
            "url": u,
            "secondary_url": "",
            "platform": extract_platform(u),
            "reason": r["reason"],
            "image": r["image"]
        })
    else:
        # Multiple URLs: check if they are same handle (e.g., ig + threads)
        handles = [extract_account_from_url(u) for u in urls]
        # If handles are similar or count is 2 (e.g. IG and Threads)
        clean_handles = [h.strip("@").lower() for h in handles if h and h != "facebookユーザー"]
        if len(set(clean_handles)) == 1 and len(clean_handles) == len(urls):
            # Same person with multiple social accounts!
            expanded_records.append({
                "date": r["date"],
                "reporter": r["reporter"],
                "name": r["name"],
                "url": urls[0],
                "secondary_url": urls[1] if len(urls) > 1 else "",
                "platform": f"{extract_platform(urls[0])} / {extract_platform(urls[1])}",
                "reason": r["reason"],
                "image": r["image"]
            })
        else:
            # Different people listed in one post
            for u in urls:
                acc = extract_account_from_url(u)
                expanded_records.append({
                    "date": r["date"],
                    "reporter": r["reporter"],
                    "name": acc or r["name"],
                    "url": u,
                    "secondary_url": "",
                    "platform": extract_platform(u),
                    "reason": r["reason"],
                    "image": r["image"]
                })

print(f"Total expanded items: {len(expanded_records)}")

# Deduplication
dedup_map = {}

for item in expanded_records:
    canon = get_canonical_url(item["url"])
    if canon and canon not in ["facebook.com/share", "facebook.com/profile.php", "instagram.com", "threads.net"]:
        key = ("url", canon)
    else:
        # Fallback key: date + reporter + (name or url)
        key = ("fallback", item["date"], item["reporter"], item["name"] or item["url"])
        
    if key not in dedup_map:
        dedup_map[key] = item
    else:
        # Merge: keep the richer information
        existing = dedup_map[key]
        if not existing["name"] and item["name"]:
            existing["name"] = item["name"]
        elif item["name"] and len(item["name"]) > len(existing["name"]):
            existing["name"] = item["name"]
            
        if not existing["reason"] and item["reason"]:
            existing["reason"] = item["reason"]
        elif item["reason"] and len(item["reason"]) > len(existing["reason"]):
            existing["reason"] = item["reason"]
            
        if not existing["date"] and item["date"]:
            existing["date"] = item["date"]
            
        if not existing["reporter"] and item["reporter"]:
            existing["reporter"] = item["reporter"]

unique_records = list(dedup_map.values())
print(f"Unique deduped records: {len(unique_records)}")

# Refine name if missing
for r in unique_records:
    if not r["name"] or r["name"].strip() == "":
        acc = extract_account_from_url(r["url"])
        if acc:
            r["name"] = acc
        else:
            r["name"] = "（名称未記載）"

# Display sample of 10 items
for item in unique_records[:10]:
    print(f"[{item['date']}] {item['name']} | {item['platform']} | {item['url']} | 理由: {item['reason'][:30]}...")

