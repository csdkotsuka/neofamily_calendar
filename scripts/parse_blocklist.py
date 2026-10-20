import json
import re
from urllib.parse import urlparse, parse_qs

with open("scripts/ocr_results.json") as f:
    images_data = json.load(f)

# Sort images by filename so they are in chronological order
images_data.sort(key=lambda x: x["file"])

def is_noise_line(text):
    t = text.strip()
    if not t:
        return True
    if t in ["Notes", "Ca", "戻る", "編集", "完了", "共有"]:
        return True
    # Reaction counters like '20：', '1C：', '10…', '30：', '20'
    if re.match(r'^\d+[C0-9\s：:…\.\,\_]*$', t):
        return True
    return False

def clean_url(url_candidate):
    # OCR cleanups
    u = url_candidate.strip()
    u = u.replace("？", "?").replace("＆", "&").replace("＝", "=")
    u = u.replace(" ", "")
    # Common OCR typo for https
    u = re.sub(r'^(nttps|nltps|htps|hfps|httos|https)\b', 'https', u, flags=re.IGNORECASE)
    u = re.sub(r'^(nttp|htip|http)\b', 'http', u, flags=re.IGNORECASE)
    
    # If doesn't start with http, check if it's www.
    if re.match(r'^www\.', u, re.IGNORECASE):
        u = "https://" + u
    return u

def extract_posts_from_image(img_entry):
    lines = [l for l in img_entry["lines"] if not is_noise_line(l["text"])]
    
    # Identify posts. In LINE Note:
    # A post usually starts with or contains:
    # - A reporter line: e.g. "本多栞/RAYTUS/秘書課", "中川美雪/yuima-ru", "川野弥生/enchant+"
    # - A date line: e.g. "Jun 5 11:25 AM", "Yesterday at 12:41 PM", "Aug 12 12:10 AM"
    posts = []
    
    # Let's collect raw text blocks
    # Group lines into logical chunks
    return lines

print("Testing parser...")
