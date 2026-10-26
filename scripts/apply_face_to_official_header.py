#!/usr/bin/env python3
"""
apply_face_to_official_header.py

Replaces the character face in 会長YouTube_ヘッダー.png with the official
caricature face from the latest YouTube banner (sunglasses, fade haircut,
confident triumphant grin), preserving the katana blade, body pose,
crimson background, and matching the 8px white sticker outline.
"""

import os
import shutil
import unicodedata
from PIL import Image, ImageFilter
import numpy as np

WORKSPACE_DIR = "/Users/kotsuka/Documents/systemDev/neo_family_calendar"
ASSETS_DIR = os.path.join(WORKSPACE_DIR, "assets")

def find_user_header():
    for f in os.listdir(ASSETS_DIR):
        norm = unicodedata.normalize('NFC', f)
        if '会長YouTube_ヘッダー' in norm and f.endswith('.png') and '元画像' not in norm and '修正版' not in norm:
            return os.path.join(ASSETS_DIR, f)
    raise FileNotFoundError("会長YouTube_ヘッダー.png not found in assets/")

def main():
    header_path = find_user_header()
    print(f"📖 Found source header: {header_path}")
    
    # Backup original if not already backed up
    backup_path = os.path.join(ASSETS_DIR, "会長YouTube_ヘッダー_元画像.png")
    if not os.path.exists(backup_path):
        shutil.copy2(header_path, backup_path)
        print(f"💾 Backed up original to: {backup_path}")
    
    # Always load from the pristine backup
    orig = Image.open(backup_path).convert('RGBA')
    
    # 1. Load the exact character used in youtube_banner_sukatto.png
    slash_path = os.path.join(ASSETS_DIR, "youtube_v2", "samurai_slash_caricature_crop.png")
    slash_im = Image.open(slash_path).convert('RGBA')
    
    target_h = 412
    target_w = int(target_h * (slash_im.width / float(slash_im.height)))
    stk_res = slash_im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Apply sticker border (same 8px border as in banner and header)
    border_width = 8
    pad = border_width + 4
    canvas_stk = Image.new('RGBA', (target_w + pad * 2, target_h + pad * 2), (0, 0, 0, 0))
    canvas_stk.paste(stk_res, (pad, pad), stk_res)
    alpha = canvas_stk.split()[3]
    thick_alpha = alpha.filter(ImageFilter.MaxFilter(border_width * 2 + 1))
    border_img = Image.new('RGBA', canvas_stk.size, (255, 255, 255, 255))
    border_img.putalpha(thick_alpha)
    stk_im = Image.alpha_composite(border_img, canvas_stk)
    offset = pad
    
    # 2. Extract the face directly from the sticker character
    # In stk_res, sunglasses center is (204.6, 156.0)
    # In stk_im, sunglasses center is (204.6 + offset, 156.0 + offset)
    sg_stk_x = 204.6 + offset
    sg_stk_y = 156.0 + offset
    
    c_x1 = int(sg_stk_x - 105)
    c_x2 = int(sg_stk_x + 105)
    c_y1 = int(sg_stk_y - 125)
    c_y2 = int(sg_stk_y + 95)
    
    head = stk_im.crop((c_x1, c_y1, c_x2, c_y2))
    
    # Soft vertical feathering on the bottom 14 pixels of neck to blend with kimono collar
    arr_head = np.array(head)
    fade_len = 14
    for i in range(fade_len):
        factor = i / float(fade_len)
        row_idx = arr_head.shape[0] - fade_len + i
        arr_head[row_idx, :, 3] = (arr_head[row_idx, :, 3] * factor).astype(np.uint8)
    head_feathered = Image.fromarray(arr_head)
    
    # 3. Position and fit the face onto orig:
    # Target sunglasses in orig: (716.2, 618.9)
    sg_in_crop_x = sg_stk_x - c_x1
    sg_in_crop_y = sg_stk_y - c_y1
    paste_x = int(716.2 - sg_in_crop_x)
    paste_y = int(618.9 - sg_in_crop_y)
    
    res = orig.copy()
    res.paste(head_feathered, (paste_x, paste_y), head_feathered)
    
    # 4. Save to files
    out_png = header_path
    out_jpg = os.path.splitext(header_path)[0] + ".jpg"
    copy_png = os.path.join(ASSETS_DIR, "会長YouTube_ヘッダー_修正版.png")
    copy_jpg = os.path.join(ASSETS_DIR, "会長YouTube_ヘッダー_修正版.jpg")
    
    res.save(out_png, "PNG")
    res.convert("RGB").save(out_jpg, "JPEG", quality=95, optimize=True)
    shutil.copy2(out_png, copy_png)
    shutil.copy2(out_jpg, copy_jpg)
    print(f"✅ Updated main file: {out_png}")
    print(f"✅ Generated JPEG: {out_jpg}")
    print(f"✅ Generated copy: {copy_png}")
    
    acc1_banner_dir = os.path.join(ASSETS_DIR, "youtube_accounts", "01_ぶった斬り会長_公式切り抜き", "01_バナー")
    if os.path.exists(acc1_banner_dir):
        shutil.copy2(out_png, os.path.join(acc1_banner_dir, "会長YouTube_ヘッダー_公式修正版.png"))
        shutil.copy2(out_jpg, os.path.join(acc1_banner_dir, "会長YouTube_ヘッダー_公式修正版.jpg"))
        print(f"📁 Synchronized to: {acc1_banner_dir}")
        
    print("🎉 All updates completed successfully!")

if __name__ == "__main__":
    main()
