import json, re

with open("scripts/ocr_results.json", "r", encoding="utf-8") as f:
    ocr_data = json.load(f)

ocr_data.sort(key=lambda x: x["file"])

# Filter only pure UI chrome (status bar "Notes", reaction counts on far right x > 0.78)
def is_ui_chrome(text, x, y):
    t = text.strip()
    if not t:
        return True
    if y < 0.055 and t in ("Notes", "ノート", "完了", "編集", "<", "＜"):
        return True
    if x > 0.78 and re.match(r'^[0-9①-⑳C\s：:…\.\,\_\@\(\)☺️👍❤️✨🙏]+$', t):
        return True
    return False

md_lines = [
    "# LINE Note ブロックリスト スクリーンショット純粋文字起こし（全97枚）",
    "",
    "提供いただいた全97枚のスクリーンショット（`prvided data/BlockList`）を、画像の上から下へ（Y座標順）そのまま忠実に文字起こしした原文データです。",
    ""
]

js_records = []

for idx, img in enumerate(ocr_data, 1):
    fname = img["file"]
    # Sort strictly top-to-bottom (only sort left-to-right if on the exact same line within 0.004)
    lines = sorted(img["lines"], key=lambda l: (round(l["y"] / 0.004), l["x"]))
    clean_lines = []
    for l in lines:
        if is_ui_chrome(l["text"], l["x"], l["y"]):
            continue
        clean_lines.append(l["text"].strip())
    
    md_lines.append(f"## [{idx:02d}/97] `{fname}`")
    md_lines.append("```text")
    for cl in clean_lines:
        md_lines.append(cl)
    md_lines.append("```")
    md_lines.append("")
    
    js_records.append({
        "index": idx,
        "file": fname,
        "text": "\n".join(clean_lines)
    })

md_content = "\n".join(md_lines)
with open("blocklist_raw_transcription.md", "w", encoding="utf-8") as f:
    f.write(md_content)

with open("js/ocr-transcription-data.js", "w", encoding="utf-8") as f:
    f.write("/**\n * Pure verbatim OCR transcription of all 97 LINE Note screenshots\n */\n")
    f.write("var RAW_OCR_TRANSCRIPTIONS = " + json.dumps(js_records, ensure_ascii=False, indent=2) + ";\n")

print(f"Generated raw transcription for {len(js_records)} screenshots ({len(md_content)} chars).")
