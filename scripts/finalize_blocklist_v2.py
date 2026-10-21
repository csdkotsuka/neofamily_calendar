import json
import re
from urllib.parse import urlparse

# Import earlier logic
exec(open("scripts/rebuild_blocklist_v2.py").read())

def get_canonical_key(u):
    if not u: return ""
    try:
        parsed = urlparse(u)
        netloc = parsed.netloc.lower().replace("www.", "")
        if "threads" in netloc: netloc = "threads.net"
        path = parsed.path.rstrip("/")
        return f"{netloc}{path}".lower()
    except:
        return u.lower()

# Expand records
expanded_items = []

for r in cleaned_records:
    urls = r["urls"]
    if not urls:
        continue # Strictly no URL = exclude
        
    if len(urls) == 1:
        u_info = urls[0]
        acc = extract_account_id(u_info["url"])
        expanded_items.append({
            "date": r["date"],
            "reporter_name": r["reporter_name"],
            "reporter_dept": r["reporter_dept"],
            "reporter": r["reporter_display"],
            "name": r["name"],
            "account_id": acc or "",
            "url": u_info["url"],
            "secondary_url": "",
            "platform": u_info["platform"],
            "url_warning": u_info["warning"] or "",
            "reason": r["reason"],
            "image": r["image"]
        })
    else:
        # Check if same person (e.g. IG + Threads)
        accs = [extract_account_id(u["url"]) for u in urls]
        clean_accs = [a.lower() for a in accs if a]
        if len(urls) == 2 and (len(set(clean_accs)) <= 1 or not clean_accs):
            # Same person with 2 social accounts!
            main_acc = clean_accs[0] if clean_accs else ""
            warns = [u["warning"] for u in urls if u["warning"]]
            expanded_items.append({
                "date": r["date"],
                "reporter_name": r["reporter_name"],
                "reporter_dept": r["reporter_dept"],
                "reporter": r["reporter_display"],
                "name": r["name"],
                "account_id": main_acc,
                "url": urls[0]["url"],
                "secondary_url": urls[1]["url"],
                "platform": f"{urls[0]['platform']} / {urls[1]['platform']}",
                "url_warning": " / ".join(warns),
                "reason": r["reason"],
                "image": r["image"]
            })
        else:
            # Multiple separate target accounts
            for u in urls:
                acc = extract_account_id(u["url"])
                expanded_items.append({
                    "date": r["date"],
                    "reporter_name": r["reporter_name"],
                    "reporter_dept": r["reporter_dept"],
                    "reporter": r["reporter_display"],
                    "name": r["name"] if len(urls) == 1 else "",
                    "account_id": acc or "",
                    "url": u["url"],
                    "secondary_url": "",
                    "platform": u["platform"],
                    "url_warning": u["warning"] or "",
                    "reason": r["reason"],
                    "image": r["image"]
                })

print(f"Total expanded items: {len(expanded_items)}")

# Deduplicate by canonical URL
dedup_dict = {}

for item in expanded_items:
    canon = get_canonical_key(item["url"])
    # If generic facebook or empty
    if not canon or canon in ["facebook.com/share", "facebook.com/share/1", "facebook.com/profile.php", "instagram.com", "threads.net"]:
        key = ("fallback", item["date"], item["reporter"], item["name"] or item["url"])
    else:
        key = ("url", canon)
        
    if key not in dedup_dict:
        dedup_dict[key] = item
    else:
        existing = dedup_dict[key]
        # Keep richer name
        if not existing["name"] and item["name"]:
            existing["name"] = item["name"]
        elif item["name"] and len(item["name"]) > len(existing["name"]):
            existing["name"] = item["name"]
            
        # Keep richer reason
        if not existing["reason"] and item["reason"]:
            existing["reason"] = item["reason"]
        elif item["reason"] and len(item["reason"]) > len(existing["reason"]):
            existing["reason"] = item["reason"]
            
        # Keep secondary url if missing
        if not existing["secondary_url"] and item["secondary_url"]:
            existing["secondary_url"] = item["secondary_url"]
            existing["platform"] = f"{existing['platform']} / {get_platform_name(item['secondary_url'])}"
            
        # Merge warning
        if item["url_warning"] and item["url_warning"] not in existing["url_warning"]:
            existing["url_warning"] = (existing["url_warning"] + " " + item["url_warning"]).strip()

final_items = list(dedup_dict.values())
print(f"Final deduplicated count: {len(final_items)}")

# Polish final names and reasons
for idx, item in enumerate(final_items, 1):
    item["id"] = f"blk_{idx:03d}"
    
    # If name is still empty, fallback to account ID or "（名称未記載）"
    if not item["name"] or item["name"].strip() == "":
        if item["account_id"]:
            item["name"] = f"@{item['account_id']}"
        else:
            item["name"] = "（名称未記載）"
            
    # Double check if any reason leaked into name
    if is_reason_text(item["name"]):
        # Move it to reason!
        if item["reason"]:
            item["reason"] = item["name"] + " " + item["reason"]
        else:
            item["reason"] = item["name"]
        item["name"] = f"@{item['account_id']}" if item["account_id"] else "（名称未記載）"

    # Specific broken link heuristics
    if "facebook.com/share/1" in item["url"] and len(item["url"]) <= 28:
        item["url_warning"] = "⚠️ 共有リンクID欠落の可能性あり"
    if item["url"].rstrip("/").endswith("instagram.com") or item["url"].rstrip("/").endswith("threads.net"):
        item["url_warning"] = "⚠️ アカウントURL不完全（ユーザー名なし）"

print("\n--- SAMPLE 15 FINAL ENTRIES ---")
for item in final_items[:15]:
    print(f"[{item['id']}] 氏名: {item['name']}")
    print(f"  URL: {item['url']}")
    if item['secondary_url']: print(f"  URL2: {item['secondary_url']}")
    print(f"  報告者: {item['reporter']}")
    if item['url_warning']: print(f"  ⚠️ 警告: {item['url_warning']}")
    print(f"  理由: {item['reason'][:50] if item['reason'] else '-'}")
    print("-" * 50)
