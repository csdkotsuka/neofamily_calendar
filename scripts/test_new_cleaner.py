import json, re
from urllib.parse import urlparse

with open("scripts/ocr_results.json") as f:
    images_data = json.load(f)

images_data.sort(key=lambda x: x["file"])

def is_noise(t, x):
    t = t.strip()
    if not t or t in ["Notes", "Ca", "戻る", "編集", "完了", "共有", "投稿", "コメント", "ノート"]:
        return True
    if x > 0.75:
        return True
    if re.match(r'^[0-9①-⑳C\s：:…\.\,\_\@\(\)]+$', t):
        return True
    return False

# Reporter parsing helper
def parse_reporter(t):
    t = t.strip()
    # Normalize slashes
    t = t.replace("／", "/").replace("＼", "/").replace("\\", "/")
    parts = [p.strip() for p in t.split("/") if p.strip()]
    if not parts:
        return {"name": "管理部", "dept": "", "display": "管理部"}
    
    # Common OCR fix
    name = parts[0]
    if name == "本多菜": name = "本多栞"
    
    dept_parts = parts[1:]
    dept = " / ".join(dept_parts) if dept_parts else ""
    
    display = f"{name}（{dept}）" if dept else name
    return {"name": name, "dept": dept, "display": display}

print("Reporter test:")
print(parse_reporter("本多栞/RAYTUS/秘書課"))
print(parse_reporter("畑ゆかり/yuima-ru理事長"))
print(parse_reporter("藤井詩穂/shAdow"))
print(parse_reporter("片岡哉江かなえ/シャンブルカーサ"))
