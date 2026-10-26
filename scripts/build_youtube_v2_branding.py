# -*- coding: utf-8 -*-
"""
High-Precision YouTube Branding Asset Generator (V2 - Official Caricature Slash Situation Edition)
- Character: 'ぶった斬り会長' caricature in a dynamic mid-swing katana slash situation ('ぶった斬るシチュエーション').
  (Fade hairstyle, gradient aviator sunglasses, charismatic smug grin 'ドヤ顔', katana slash wave).
- Layout:
  - Round NEO FAMILY logo removed from banner.
  - Text shifted to the left (X: 535) with generous whitespace.
- Wording:
  - Daily update promises removed as requested ('厳選Shorts随時配信中', 'Shortsでお届け').
- Pill Icons:
  - Fixed font-missing glyph / tofu bug (boxes with X) by drawing clean, crisp vector icons (heart, flame, star, play).
- Icon & Watermarks:
  - Fully updated and synchronized across all folders.
"""

import math
import random
import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_V2 = "assets/youtube_v2"
OUTPUT_ACCOUNTS = "assets/youtube_accounts"
os.makedirs(OUTPUT_V2, exist_ok=True)

# System Fonts (macOS)
FONT_W9 = '/System/Library/Fonts/ヒラギノ角ゴシック W9.ttc'
FONT_W8 = '/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc'
FONT_W7 = '/System/Library/Fonts/ヒラギノ角ゴシック W7.ttc'
FONT_W6 = '/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc'
FONT_ARIAL_BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'

SLASH_CARICATURE_PATH = 'assets/youtube_v2/samurai_slash_caricature_crop.png'

# -------------------------------------------------------------
# Precision Alignment & Helper Functions
# -------------------------------------------------------------

def draw_pill_with_vector_icon(draw, box, fill_color, border_color, icon_type, text, font, text_color):
    """Draw a pill button with a custom vector icon (NO emoji to prevent tofu / glyph corruption)."""
    x1, y1, x2, y2 = box
    h = y2 - y1
    w = x2 - x1
    radius = h // 2
    
    draw.rounded_rectangle(box, radius=radius, fill=fill_color, outline=border_color, width=2)
    
    t_bbox = font.getbbox(text)
    tw = t_bbox[2] - t_bbox[0]
    th = t_bbox[3] - t_bbox[1]
    
    icon_sz = 16
    gap = 8
    total_content_w = icon_sz + gap + tw
    start_x = x1 + (w - total_content_w) / 2.0
    cy = y1 + h / 2.0
    
    ix = start_x
    if icon_type == 'heart':
        pts = [
            (ix + icon_sz*0.5, cy + icon_sz*0.45),
            (ix, cy - icon_sz*0.1),
            (ix + icon_sz*0.2, cy - icon_sz*0.45),
            (ix + icon_sz*0.5, cy - icon_sz*0.2),
            (ix + icon_sz*0.8, cy - icon_sz*0.45),
            (ix + icon_sz, cy - icon_sz*0.1)
        ]
        draw.polygon(pts, fill=(255, 255, 255, 255))
    elif icon_type == 'flame':
        pts = []
        for p in range(8):
            r = icon_sz*0.5 if (p % 2 == 0) else icon_sz*0.22
            ang = p * math.pi / 4.0 - math.pi / 2.0
            pts.append((ix + icon_sz*0.5 + r * math.cos(ang), cy + r * math.sin(ang)))
        draw.polygon(pts, fill=(255, 255, 255, 255))
    elif icon_type == 'star':
        pts = []
        for p in range(8):
            r = icon_sz*0.5 if (p % 2 == 0) else icon_sz*0.2
            ang = p * math.pi / 4.0 - math.pi / 2.0
            pts.append((ix + icon_sz*0.5 + r * math.cos(ang), cy + r * math.sin(ang)))
        draw.polygon(pts, fill=(255, 255, 255, 255))
    elif icon_type == 'play':
        tri_w = icon_sz * 0.8
        tri_h = icon_sz * 0.9
        pts = [
            (ix + 1, cy - tri_h / 2.0),
            (ix + 1 + tri_w, cy),
            (ix + 1, cy + tri_h / 2.0)
        ]
        draw.polygon(pts, fill=(255, 255, 255, 255))
        
    tx = start_x + icon_sz + gap - t_bbox[0]
    ty = cy - th / 2.0 - t_bbox[1]
    draw.text((tx, ty), text, font=font, fill=text_color)

def draw_centered_text(draw_ctx, text, font, box, fill, stroke_width=0, stroke_fill=None):
    bbox = font.getbbox(text, stroke_width=stroke_width)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    bx1, by1, bx2, by2 = box
    box_w = bx2 - bx1
    box_h = by2 - by1
    draw_x = bx1 + (box_w - w) / 2.0 - bbox[0]
    draw_y = by1 + (box_h - h) / 2.0 - bbox[1]
    if stroke_width > 0 and stroke_fill:
        draw_ctx.text((draw_x, draw_y), text, font=font, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)
    else:
        draw_ctx.text((draw_x, draw_y), text, font=font, fill=fill)
    return draw_x, draw_y

def draw_text_with_outline(draw_ctx, text, pos, font, fill_color, stroke_layers):
    for sw, sc in stroke_layers:
        draw_ctx.text(pos, text, font=font, fill=sc, stroke_width=sw, stroke_fill=sc)
    draw_ctx.text(pos, text, font=font, fill=fill_color)

def draw_star(draw_obj, center_x, center_y, outer_r, inner_r, fill_color):
    points = []
    for p in range(8):
        r = outer_r if (p % 2 == 0) else inner_r
        ang = p * math.pi / 4.0 - math.pi / 2.0
        points.append((center_x + r * math.cos(ang), center_y + r * math.sin(ang)))
    draw_obj.polygon(points, fill=fill_color)

def make_sticker(im_rgba, border_width=10, border_color=(255, 255, 255, 255)):
    alpha = im_rgba.split()[3]
    padded_w = im_rgba.width + border_width * 2 + 10
    padded_h = im_rgba.height + border_width * 2 + 10
    pad_img = Image.new('RGBA', (padded_w, padded_h), (0, 0, 0, 0))
    pad_img.paste(Image.new('RGBA', im_rgba.size, (255, 255, 255, 255)), (border_width + 5, border_width + 5), alpha)
    mask = pad_img.split()[3].filter(ImageFilter.MaxFilter(border_width * 2 + 1))
    sticker = Image.new('RGBA', (padded_w, padded_h), (0, 0, 0, 0))
    sticker.paste(Image.new('RGBA', (padded_w, padded_h), border_color), (0, 0), mask)
    sticker.paste(im_rgba, (border_width + 5, border_width + 5), im_rgba)
    return sticker, border_width + 5

# -------------------------------------------------------------
# 1. Banners (2560 x 1440) - Katana Slash Situation
# -------------------------------------------------------------

def build_banner_sukatto():
    W, H = 2560, 1440
    
    font_title = ImageFont.truetype(FONT_W9, 84)
    font_subtitle = ImageFont.truetype(FONT_W8, 30)
    font_catch = ImageFont.truetype(FONT_W8, 22)
    font_badge = ImageFont.truetype(FONT_W8, 20)
    font_pill = ImageFont.truetype(FONT_W8, 19)
    
    font_tv_brand = ImageFont.truetype(FONT_W8, 28)
    font_tv_en = ImageFont.truetype(FONT_ARIAL_BOLD, 17)
    font_tv_bottom = ImageFont.truetype(FONT_W7, 24)
    
    # 1. Base Gradient Canvas
    base = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    draw_base = ImageDraw.Draw(base)
    
    for y in range(H):
        dist_c = abs(y - 720) / 720.0
        r = int(245 - 35 * (dist_c ** 1.3))
        g = int(75 + 30 * (1.0 - dist_c) - 25 * dist_c)
        b = int(105 + 20 * (1.0 - dist_c) - 50 * dist_c)
        draw_base.line([(0, y), (W, y)], fill=(r, max(0, g), max(0, b), 255))
        
    radial_glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_rg = ImageDraw.Draw(radial_glow)
    gcx, gcy = 1750, 720
    for r in range(1600, 0, -20):
        factor = (1.0 - (r / 1600.0) ** 1.3)
        alpha = int(180 * factor)
        draw_rg.ellipse([gcx - r, gcy - r, gcx + r, gcy + r], fill=(255, 215, 120, min(255, alpha)))
    base = Image.alpha_composite(base, radial_glow)
    
    # TV Area Accents (Wording updated: NO daily promise)
    tv_accents = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_tv = ImageDraw.Draw(tv_accents)
    
    top_title = "NEO FAMILY  OFFICIAL  YOUTUBE  CHANNEL"
    bbox_top = font_tv_brand.getbbox(top_title)
    tw_top = bbox_top[2] - bbox_top[0]
    tx_top = (W - tw_top) // 2
    ty_top = 265
    
    draw_star(draw_tv, tx_top - 40, ty_top + 15, 14, 4, (255, 245, 180, 240))
    draw_star(draw_tv, tx_top + tw_top + 40, ty_top + 15, 14, 4, (255, 245, 180, 240))
    draw_tv.text((tx_top, ty_top), top_title, font=font_tv_brand, fill=(255, 250, 220, 240))
    
    top_sub = "WOMEN & FAMILY EMPOWERMENT  ★  OFFICIAL SHORTS"
    bbox_sub = font_tv_en.getbbox(top_sub)
    tw_sub = bbox_sub[2] - bbox_sub[0]
    draw_tv.text(((W - tw_sub) // 2, ty_top + 45), top_sub, font=font_tv_en, fill=(255, 235, 200, 190))
    
    bot_title = "ココロが軽くなる、今日が変わる。モヤモヤを一刀両断する共創コミュニティ"
    bbox_bot = font_tv_bottom.getbbox(bot_title)
    tw_bot = bbox_bot[2] - bbox_bot[0]
    draw_tv.text(((W - tw_bot) // 2, 1145), bot_title, font=font_tv_bottom, fill=(255, 245, 225, 210))
    
    random.seed(456)
    for _ in range(60):
        sx = random.randint(80, W - 80)
        sy = random.randint(60, H - 60)
        if 480 < sx < 2080 and 490 < sy < 950:
            continue
        sz = random.randint(6, 20)
        draw_star(draw_tv, sx, sy, sz, sz * 0.3, (255, 255, 220, random.randint(100, 210)))
        
    base = Image.alpha_composite(base, tv_accents)
    
    # 2. Right Side: Katana Slash Situation Illustration
    slash_im = Image.open(SLASH_CARICATURE_PATH).convert('RGBA')
    target_h = 412
    target_w = int(target_h * (slash_im.width / float(slash_im.height))) # ~436px
    stk_res = slash_im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    stk_im, offset = make_sticker(stk_res, border_width=10, border_color=(255, 255, 255, 255))
    
    kx = 1570
    ky = 516
    
    s_shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    shadow_stamp = Image.new('RGBA', stk_im.size, (50, 10, 20, 140))
    s_shadow.paste(shadow_stamp, (kx - offset + 6, ky - offset + 8), stk_im.split()[3])
    s_shadow = s_shadow.filter(ImageFilter.GaussianBlur(16))
    base = Image.alpha_composite(base, s_shadow)
    base.paste(stk_im, (kx - offset, ky - offset), stk_im)
    
    # 3. Left Side: Typography (Shifted right & down, line spacing expanded, no pills)
    text_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_txt = ImageDraw.Draw(text_layer)
    
    tx = 580 # Shifted slightly right (inside safe area 507..2053)
    
    # Top Badges
    badge_y = 570
    b1_box = (tx, badge_y, tx + 260, badge_y + 40)
    draw_txt.rounded_rectangle(b1_box, radius=20, fill=(225, 29, 72, 245), outline=(255, 235, 140, 255), width=2)
    draw_centered_text(draw_txt, "★ ぶった斬り会長公認 ★", font_badge, b1_box, (255, 255, 255))
    
    tx_b2 = tx + 260 + 16
    b2_box = (tx_b2, badge_y, tx_b2 + 270, badge_y + 40)
    draw_txt.rounded_rectangle(b2_box, radius=20, fill=(245, 158, 11, 245), outline=(255, 255, 255, 230), width=2)
    draw_centered_text(draw_txt, "✨ 厳選Shorts随時配信中 ✨", font_badge, b2_box, (255, 255, 255))
    
    # Main Title (Shifted down, generous spacing)
    title_str = "主婦のスカッと切り抜き"
    title_y = 638
    
    t_shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_tsh = ImageDraw.Draw(t_shadow)
    draw_tsh.text((tx + 4, title_y + 8), title_str, font=font_title, fill=(80, 5, 20, 160), stroke_width=20, stroke_fill=(80, 5, 20, 160))
    t_shadow = t_shadow.filter(ImageFilter.GaussianBlur(8))
    base = Image.alpha_composite(base, t_shadow)
    
    draw_text_with_outline(
        draw_txt,
        title_str,
        (tx, title_y),
        font_title,
        fill_color=(255, 245, 80, 255),
        stroke_layers=[
            (20, (255, 255, 255, 255)),
            (10, (225, 29, 72, 255))
        ]
    )
    
    # Subtitle (Expanded line margin)
    sub_str = "日常のモヤモヤ・人間関係・夫婦の悩みをズバッと解消！"
    sub_y = 762
    draw_text_with_outline(
        draw_txt,
        sub_str,
        (tx, sub_y),
        font_subtitle,
        fill_color=(255, 255, 255, 255),
        stroke_layers=[
            (8, (120, 10, 40, 255)),
            (4, (0, 0, 0, 220))
        ]
    )
    
    # Catchphrase (Expanded line margin, NO daily promise)
    catch_str = "240万再生の共感ストーリー × 心が軽くなる魂の言葉をShortsでお届け♥"
    catch_y = 826
    draw_text_with_outline(
        draw_txt,
        catch_str,
        (tx, catch_y),
        font_catch,
        fill_color=(255, 245, 205, 255),
        stroke_layers=[
            (5, (100, 10, 30, 240))
        ]
    )
    
    base = Image.alpha_composite(base, text_layer)
    
    out_png = os.path.join(OUTPUT_V2, "youtube_banner_sukatto.png")
    out_jpg = os.path.join(OUTPUT_V2, "youtube_banner_sukatto.jpg")
    base.save(out_png, "PNG")
    base.convert("RGB").save(out_jpg, "JPEG", quality=92, optimize=True)
    print(f"✅ Generated: {out_jpg}")


def build_banner_community():
    """Alternative pattern: Community & Terakoya variation"""
    W, H = 2560, 1440
    
    font_title = ImageFont.truetype(FONT_W9, 76)
    font_subtitle = ImageFont.truetype(FONT_W8, 30)
    font_catch = ImageFont.truetype(FONT_W8, 22)
    font_badge = ImageFont.truetype(FONT_W8, 20)
    font_pill = ImageFont.truetype(FONT_W8, 19)
    
    font_tv_brand = ImageFont.truetype(FONT_W8, 28)
    font_tv_en = ImageFont.truetype(FONT_ARIAL_BOLD, 17)
    font_tv_bottom = ImageFont.truetype(FONT_W7, 24)
    
    base = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    draw_base = ImageDraw.Draw(base)
    
    for y in range(H):
        dist_c = abs(y - 720) / 720.0
        r = int(240 - 45 * dist_c)
        g = int(90 + 35 * (1.0 - dist_c) - 20 * dist_c)
        b = int(120 + 25 * (1.0 - dist_c) - 40 * dist_c)
        draw_base.line([(0, y), (W, y)], fill=(r, max(0, g), max(0, b), 255))
        
    # Right: Katana Slash Character
    slash_im = Image.open(SLASH_CARICATURE_PATH).convert('RGBA')
    target_h = 412
    target_w = int(target_h * (slash_im.width / float(slash_im.height)))
    stk_res = slash_im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    stk_im, offset = make_sticker(stk_res, border_width=10, border_color=(255, 255, 255, 255))
    
    kx = 1580
    ky = 516
    s_shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    shadow_stamp = Image.new('RGBA', stk_im.size, (40, 10, 20, 140))
    s_shadow.paste(shadow_stamp, (kx - offset + 6, ky - offset + 8), stk_im.split()[3])
    s_shadow = s_shadow.filter(ImageFilter.GaussianBlur(16))
    base = Image.alpha_composite(base, s_shadow)
    base.paste(stk_im, (kx - offset, ky - offset), stk_im)
    
    # Left: Typography (Shifted right & down, line spacing expanded, no pills)
    text_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_txt = ImageDraw.Draw(text_layer)
    tx = 570
    
    badge_y = 570
    b1_box = (tx, badge_y, tx + 310, badge_y + 40)
    draw_txt.rounded_rectangle(b1_box, radius=20, fill=(16, 149, 120, 245), outline=(255, 255, 255, 230), width=2)
    draw_centered_text(draw_txt, "★ NEO FAMILY 公式切り抜き ★", font_badge, b1_box, (255, 255, 255))
    
    tx_b2 = tx + 310 + 16
    b2_box = (tx_b2, badge_y, tx_b2 + 280, badge_y + 40)
    draw_txt.rounded_rectangle(b2_box, radius=20, fill=(225, 29, 72, 245), outline=(255, 235, 140, 255), width=2)
    draw_centered_text(draw_txt, "✨ 夢をカタチにするShorts ✨", font_badge, b2_box, (255, 255, 255))
    
    title_str = "NEO FAMILY 公式切り抜き"
    title_y = 638
    t_shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_tsh = ImageDraw.Draw(t_shadow)
    draw_tsh.text((tx + 4, title_y + 8), title_str, font=font_title, fill=(60, 10, 20, 160), stroke_width=22, stroke_fill=(60, 10, 20, 160))
    t_shadow = t_shadow.filter(ImageFilter.GaussianBlur(8))
    base = Image.alpha_composite(base, t_shadow)
    
    draw_text_with_outline(
        draw_txt,
        title_str,
        (tx, title_y),
        font_title,
        fill_color=(255, 248, 120, 255),
        stroke_layers=[
            (22, (255, 255, 255, 255)),
            (12, (225, 29, 72, 255))
        ]
    )
    
    sub_str = "仲間と創る新時代ライフスタイル＆夢実現ストーリー"
    sub_y = 762
    draw_text_with_outline(
        draw_txt,
        sub_str,
        (tx, sub_y),
        font_subtitle,
        fill_color=(255, 255, 255, 255),
        stroke_layers=[
            (8, (100, 15, 30, 255)),
            (4, (0, 0, 0, 220))
        ]
    )
    
    catch_str = "子育て・健康・美容・起業！普通の人たちが次々と夢を叶えるリアルストーリー"
    catch_y = 826
    draw_text_with_outline(
        draw_txt,
        catch_str,
        (tx, catch_y),
        font_catch,
        fill_color=(255, 245, 210, 255),
        stroke_layers=[
            (5, (80, 10, 25, 240))
        ]
    )
    
    base = Image.alpha_composite(base, text_layer)
    
    out_png = os.path.join(OUTPUT_V2, "youtube_banner_community.png")
    out_jpg = os.path.join(OUTPUT_V2, "youtube_banner_community.jpg")
    base.save(out_png, "PNG")
    base.convert("RGB").save(out_jpg, "JPEG", quality=92, optimize=True)
    print(f"✅ Generated: {out_jpg}")


# -------------------------------------------------------------
# 2. Channel Icons (800 x 800) - Slash Caricature Character
# -------------------------------------------------------------

def build_icon_sukatto():
    S = 800
    base = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    
    cx, cy = S // 2, S // 2
    r_max = S // 2 - 12
    for r in range(r_max, 0, -2):
        t = r / float(r_max)
        red = int(245 - 20 * (1.0 - t))
        green = int(55 + 85 * (1.0 - t))
        blue = int(85 + 50 * (1.0 - t))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(red, green, blue, 255))
        
    draw.ellipse([cx - r_max, cy - r_max, cx + r_max, cy + r_max], outline=(255, 215, 80, 255), width=10)
    draw.ellipse([cx - r_max + 10, cy - r_max + 10, cx + r_max - 10, cy + r_max - 10], outline=(255, 255, 255, 230), width=4)
    
    slash_im = Image.open(SLASH_CARICATURE_PATH).convert('RGBA')
    target_w = 540
    target_h = int(target_w * (slash_im.height / float(slash_im.width)))
    stk_scaled = slash_im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    stk_im, offset = make_sticker(stk_scaled, border_width=12, border_color=(255, 255, 255, 255))
    
    kx = (S - stk_im.width) // 2
    ky = 75
    
    k_shadow = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    shadow_stamp = Image.new('RGBA', stk_im.size, (50, 10, 20, 140))
    k_shadow.paste(shadow_stamp, (kx + 4, ky + 6), stk_im.split()[3])
    k_shadow = k_shadow.filter(ImageFilter.GaussianBlur(14))
    base = Image.alpha_composite(base, k_shadow)
    base.paste(stk_im, (kx, ky), stk_im)
    
    # Bottom Ribbon: "主婦のスカッと切り抜き"
    draw = ImageDraw.Draw(base)
    ribbon_w = 640
    ribbon_h = 96
    rx = (S - ribbon_w) // 2
    ry = 582
    r_box = (rx, ry, rx + ribbon_w, ry + ribbon_h)
    
    draw.rounded_rectangle([rx + 3, ry + 6, rx + ribbon_w + 3, ry + ribbon_h + 6], radius=30, fill=(50, 10, 20, 140))
    draw.rounded_rectangle(r_box, radius=30, fill=(225, 29, 72, 255), outline=(255, 235, 120, 255), width=5)
    
    font_bold = ImageFont.truetype(FONT_W9, 56)
    draw_centered_text(draw, "主婦のスカッと切り抜き", font_bold, r_box, (255, 255, 255), stroke_width=3, stroke_fill=(120, 10, 30))
    
    # Sub-Pill: "★ ぶった斬り会長 ★"
    sub_w = 340
    sub_h = 42
    sx = (S - sub_w) // 2
    sy = ry + ribbon_h - 12
    s_box = (sx, sy, sx + sub_w, sy + sub_h)
    draw.rounded_rectangle([sx + 2, sy + 3, sx + sub_w + 2, sy + sub_h + 3], radius=21, fill=(50, 10, 20, 120))
    draw.rounded_rectangle(s_box, radius=21, fill=(245, 158, 11, 255), outline=(255, 255, 255, 255), width=2)
    font_sub = ImageFont.truetype(FONT_W8, 22)
    draw_centered_text(draw, "★ ぶった斬り会長 ★", font_sub, s_box, (255, 255, 255))
    
    out_png = os.path.join(OUTPUT_V2, "youtube_icon_sukatto.png")
    out_jpg = os.path.join(OUTPUT_V2, "youtube_icon_sukatto.jpg")
    base.save(out_png, "PNG")
    rgb_base = Image.new('RGB', (S, S), (255, 255, 255))
    rgb_base.paste(base, (0, 0), base)
    rgb_base.save(out_jpg, "JPEG", quality=95, optimize=True)
    print(f"✅ Generated: {out_jpg}")


def build_icon_community():
    """Alternative pattern: Community edition icon"""
    S = 800
    base = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    
    cx, cy = S // 2, S // 2
    r_max = S // 2 - 12
    for r in range(r_max, 0, -2):
        t = r / float(r_max)
        red = int(240 - 25 * (1.0 - t))
        green = int(70 + 70 * (1.0 - t))
        blue = int(100 + 40 * (1.0 - t))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(red, green, blue, 255))
        
    draw.ellipse([cx - r_max, cy - r_max, cx + r_max, cy + r_max], outline=(255, 215, 80, 255), width=10)
    draw.ellipse([cx - r_max + 10, cy - r_max + 10, cx + r_max - 10, cy + r_max - 10], outline=(255, 255, 255, 230), width=4)
    
    slash_im = Image.open(SLASH_CARICATURE_PATH).convert('RGBA')
    target_w = 540
    target_h = int(target_w * (slash_im.height / float(slash_im.width)))
    stk_scaled = slash_im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    stk_im, offset = make_sticker(stk_scaled, border_width=12, border_color=(255, 255, 255, 255))
    
    kx = (S - stk_im.width) // 2
    ky = 75
    k_shadow = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    shadow_stamp = Image.new('RGBA', stk_im.size, (40, 10, 20, 140))
    k_shadow.paste(shadow_stamp, (kx + 4, ky + 6), stk_im.split()[3])
    k_shadow = k_shadow.filter(ImageFilter.GaussianBlur(14))
    base = Image.alpha_composite(base, k_shadow)
    base.paste(stk_im, (kx, ky), stk_im)
    
    draw = ImageDraw.Draw(base)
    ribbon_w = 640
    ribbon_h = 96
    rx = (S - ribbon_w) // 2
    ry = 582
    r_box = (rx, ry, rx + ribbon_w, ry + ribbon_h)
    
    draw.rounded_rectangle([rx + 3, ry + 6, rx + ribbon_w + 3, ry + ribbon_h + 6], radius=30, fill=(40, 10, 20, 140))
    draw.rounded_rectangle(r_box, radius=30, fill=(16, 149, 120, 255), outline=(255, 235, 120, 255), width=5)
    
    font_bold = ImageFont.truetype(FONT_W9, 56)
    draw_centered_text(draw, "公式切り抜きCH", font_bold, r_box, (255, 255, 255), stroke_width=3, stroke_fill=(10, 70, 50))
    
    sub_w = 340
    sub_h = 42
    sx = (S - sub_w) // 2
    sy = ry + ribbon_h - 12
    s_box = (sx, sy, sx + sub_w, sy + sub_h)
    draw.rounded_rectangle([sx + 2, sy + 3, sx + sub_w + 2, sy + sub_h + 3], radius=21, fill=(40, 10, 20, 120))
    draw.rounded_rectangle(s_box, radius=21, fill=(245, 158, 11, 255), outline=(255, 255, 255, 255), width=2)
    font_sub = ImageFont.truetype(FONT_W8, 22)
    draw_centered_text(draw, "★ NEO FAMILY ★", font_sub, s_box, (255, 255, 255))
    
    out_png = os.path.join(OUTPUT_V2, "youtube_icon_community.png")
    out_jpg = os.path.join(OUTPUT_V2, "youtube_icon_community.jpg")
    base.save(out_png, "PNG")
    rgb_base = Image.new('RGB', (S, S), (255, 255, 255))
    rgb_base.paste(base, (0, 0), base)
    rgb_base.save(out_jpg, "JPEG", quality=95, optimize=True)
    print(f"✅ Generated: {out_jpg}")


# -------------------------------------------------------------
# 3. Watermarks & Shorts Stamps
# -------------------------------------------------------------

def build_watermarks():
    S = 150
    im150 = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d150 = ImageDraw.Draw(im150)
    
    cx, cy = 75, 75
    for r in range(71, 0, -2):
        t = r / 71.0
        d150.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(int(245 - 20*t), int(45 + 75*(1-t)), int(75 + 40*(1-t)), 255))
    d150.ellipse([3, 3, 147, 147], outline=(255, 215, 80, 255), width=4)
    d150.ellipse([7, 7, 143, 143], outline=(255, 255, 255, 230), width=2)
    
    slash_im = Image.open(SLASH_CARICATURE_PATH).convert('RGBA')
    # Focus on head area of slash caricature: (300, 180, 750, 580)
    head_crop = slash_im.crop((300, 180, 750, 580))
    head_sz = 86
    head_res = head_crop.resize((head_sz, int(head_sz * head_crop.height / float(head_crop.width))), Image.Resampling.LANCZOS)
    
    hx = (S - head_res.width) // 2
    hy = 10
    im150.paste(head_res, (hx, hy), head_res)
    
    # Bottom pill: Vector play icon + text (NO emoji bug!)
    pw, ph = 130, 36
    px = (S - pw) // 2
    py = 98
    pbox = (px, py, px + pw, py + ph)
    font150_sub = ImageFont.truetype(FONT_W8, 16)
    draw_pill_with_vector_icon(d150, pbox, (225, 29, 72, 255), (255, 255, 255, 255), 'play', "登録する", font150_sub, (255, 255, 255))
    
    p150 = os.path.join(OUTPUT_V2, "youtube_watermark_standard.png")
    im150.save(p150, "PNG")
    print(f"✅ Generated: {p150}")
    
    # 2. Die-cut Sticker Watermark (150x150)
    im_stk = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d_stk = ImageDraw.Draw(im_stk)
    d_stk.ellipse([6, 6, 144, 144], fill=(255, 255, 255, 255), outline=(225, 29, 72, 255), width=5)
    im_stk.paste(head_res, (hx, hy + 4), head_res)
    
    stk_box = (14, 102, 136, 136)
    d_stk.rounded_rectangle(stk_box, radius=14, fill=(225, 29, 72, 255), outline=(255, 220, 90, 255), width=2)
    f_reg = ImageFont.truetype(FONT_W8, 14)
    draw_centered_text(d_stk, "チャンネル登録", f_reg, stk_box, (255, 255, 255))
    
    p_stk = os.path.join(OUTPUT_V2, "youtube_watermark_sticker.png")
    im_stk.save(p_stk, "PNG")
    print(f"✅ Generated: {p_stk}")
    
    # 3. High-res Shorts Watermark (500x500)
    W500 = 500
    im500 = Image.new('RGBA', (W500, W500), (0, 0, 0, 0))
    d500 = ImageDraw.Draw(im500)
    
    cx5, cy5 = 250, 250
    d500.ellipse([34, 44, 466, 476], fill=(50, 10, 20, 70))
    im500 = im500.filter(ImageFilter.GaussianBlur(10))
    d500 = ImageDraw.Draw(im500)
    
    for r in range(215, 0, -3):
        t = r / 215.0
        d500.ellipse([cx5 - r, cy5 - r, cx5 + r, cy5 + r], fill=(int(245 - 25*t), int(50 + 70*(1-t)), int(80 + 50*(1-t)), 255))
    d500.ellipse([35, 35, 465, 465], outline=(255, 220, 90, 255), width=10)
    d500.ellipse([45, 45, 455, 455], outline=(255, 255, 255, 230), width=4)
    
    stk5 = slash_im.resize((360, int(360 * slash_im.height / float(slash_im.width))), Image.Resampling.LANCZOS)
    stk5_im, _ = make_sticker(stk5, border_width=8)
    im500.paste(stk5_im, (cx5 - stk5_im.width // 2, 45), stk5_im)
    
    rw, rh = 400, 94
    rx = (W500 - rw) // 2
    ry = 345
    rib5_box = (rx, ry, rx + rw, ry + rh)
    d500.rounded_rectangle([rx + 2, ry + 4, rx + rw + 2, ry + rh + 4], radius=32, fill=(40, 10, 20, 140))
    f500_title = ImageFont.truetype(FONT_W9, 44)
    draw_pill_with_vector_icon(d500, rib5_box, (225, 29, 72, 255), (255, 255, 255, 255), 'play', "登録してね♥", f500_title, (255, 255, 255))
    
    p500 = os.path.join(OUTPUT_V2, "youtube_shorts_watermark.png")
    im500.save(p500, "PNG")
    print(f"✅ Generated: {p500}")
    
    # 4. Shorts Lower Third Banner Stamp (800x160)
    BW, BH = 800, 160
    im_bar = Image.new('RGBA', (BW, BH), (0, 0, 0, 0))
    d_bar = ImageDraw.Draw(im_bar)
    
    fbar_main = ImageFont.truetype(FONT_W9, 36)
    fbar_sub = ImageFont.truetype(FONT_W8, 22)
    fbar_cta = ImageFont.truetype(FONT_W8, 24)
    
    d_bar.rounded_rectangle([14, 18, BW - 14, BH - 8], radius=24, fill=(40, 10, 20, 120))
    im_bar = im_bar.filter(ImageFilter.GaussianBlur(6))
    d_bar = ImageDraw.Draw(im_bar)
    
    d_bar.rounded_rectangle([10, 10, BW - 10, BH - 14], radius=24, fill=(255, 255, 255, 250), outline=(225, 29, 72, 255), width=4)
    
    stk_bar = slash_im.resize((120, int(120 * slash_im.height / float(slash_im.width))), Image.Resampling.LANCZOS)
    im_bar.paste(stk_bar, (20, 16), stk_bar)
    
    d_bar.text((156, 32), "主婦のスカッと切り抜き", font=fbar_main, fill=(225, 29, 72, 255))
    d_bar.text((158, 84), "ぶった斬り会長公認 ★ 厳選Shorts配信中", font=fbar_sub, fill=(100, 116, 139, 255))
    
    cw, ch = 240, 58
    cx_cta = BW - cw - 30
    cy_cta = (BH - 24 - ch) // 2 + 10
    cta_box = (cx_cta, cy_cta, cx_cta + cw, cy_cta + ch)
    draw_pill_with_vector_icon(d_bar, cta_box, (225, 29, 72, 255), (255, 225, 120, 255), 'play', "チャンネル登録", fbar_cta, (255, 255, 255))
    
    p_bar = os.path.join(OUTPUT_V2, "youtube_shorts_banner_stamp.png")
    im_bar.save(p_bar, "PNG")
    print(f"✅ Generated: {p_bar}")


# -------------------------------------------------------------
# 4. Synchronize into Category Folders & Account Folders
# -------------------------------------------------------------

def sync_folders():
    cat_map = {
        '01_バナー': [
            'youtube_banner_sukatto.jpg', 'youtube_banner_sukatto.png',
            'youtube_banner_community.jpg', 'youtube_banner_community.png'
        ],
        '02_写真_アイコン': [
            'youtube_icon_sukatto.jpg', 'youtube_icon_sukatto.png',
            'youtube_icon_community.jpg', 'youtube_icon_community.png'
        ],
        '03_透かし_ウォーターマーク': [
            'youtube_watermark_standard.png',
            'youtube_watermark_sticker.png',
            'youtube_shorts_watermark.png',
            'youtube_shorts_banner_stamp.png'
        ]
    }
    for sub, flist in cat_map.items():
        sub_dir = os.path.join(OUTPUT_V2, sub)
        os.makedirs(sub_dir, exist_ok=True)
        for fn in flist:
            src = os.path.join(OUTPUT_V2, fn)
            dst = os.path.join(sub_dir, fn)
            if os.path.exists(src):
                shutil.copy2(src, dst)
                
    acc2 = os.path.join(OUTPUT_ACCOUNTS, "02_主婦のスカッと切り抜き_NEOFAMILY")
    for fn in ['youtube_banner_sukatto.jpg', 'youtube_banner_sukatto.png']:
        shutil.copy2(os.path.join(OUTPUT_V2, fn), f"{acc2}/01_バナー/{fn}")
    for fn in ['youtube_icon_sukatto.jpg', 'youtube_icon_sukatto.png']:
        shutil.copy2(os.path.join(OUTPUT_V2, fn), f"{acc2}/02_写真_アイコン/{fn}")
    for fn in ['youtube_watermark_standard.png', 'youtube_watermark_sticker.png', 'youtube_shorts_watermark.png', 'youtube_shorts_banner_stamp.png']:
        shutil.copy2(os.path.join(OUTPUT_V2, fn), f"{acc2}/03_透かし/{fn}")
        
    acc3 = os.path.join(OUTPUT_ACCOUNTS, "03_NEOFAMILY公式_夢実現切り抜き")
    for fn in ['youtube_banner_community.jpg', 'youtube_banner_community.png']:
        shutil.copy2(os.path.join(OUTPUT_V2, fn), f"{acc3}/01_バナー/{fn}")
    for fn in ['youtube_icon_community.jpg', 'youtube_icon_community.png']:
        shutil.copy2(os.path.join(OUTPUT_V2, fn), f"{acc3}/02_写真_アイコン/{fn}")
    for fn in ['youtube_watermark_standard.png', 'youtube_watermark_sticker.png', 'youtube_shorts_watermark.png', 'youtube_shorts_banner_stamp.png']:
        shutil.copy2(os.path.join(OUTPUT_V2, fn), f"{acc3}/03_透かし/{fn}")
        
    # Update text snippets to remove daily promises
    txt_dir = f"{acc2}/04_設定テキスト"
    os.makedirs(txt_dir, exist_ok=True)
    with open(f"{txt_dir}/チャンネル名とハンドル.txt", "w", encoding="utf-8") as f:
        f.write("""■ チャンネル名候補（いずれかを選択）
【第一推奨・共感特化】
主婦のスカッと切り抜き【NEO FAMILY公式】

【案2・お悩み解消重視】
主婦のスカッと相談室【ぶった斬り会長＆NEO FAMILY】

【案3・コミュニティ共創総合】
NEO FAMILY【公式切り抜き】夢を叶える寺子屋チャンネル

----------------------------------------
■ ハンドル（@ハンドル）候補
@sukatto_neofamily （第一推奨）
@buttagiri_sukatto
@neofamily_kirinuki
""")
    with open(f"{txt_dir}/概要欄_説明文.txt", "w", encoding="utf-8") as f:
        f.write("""「誰にも言えなかった日々のモヤモヤ、ここで全部スカッと解消！」

SNS総フォロワー24万人超・ぶった斬り会長と、
全国で夢を叶える女性・ママたちの共創コミュニティ【NEO FAMILY】がお届けする公式切り抜きShortsチャンネルです✨

夫婦関係・子育て・人間関係・お金の悩みから、
一歩踏み出して自分らしく生きるためのヒントまで、
思わず「わかる！」と頷く共感ストーリーと心が軽くなる魂の言葉を厳選Shorts動画でお届けします🌸

━━━━━━━━━━━━━━━━━━━━━
🎬 当チャンネルでお届けする内容
━━━━━━━━━━━━━━━━━━━━━
・日常のモヤモヤを吹き飛ばす「主婦のスカッと話」
・ぶった斬り会長による、愛とユーモアあふれる本音の悩み相談
・家事・育児・お仕事の合間に1分で元気になれるショート動画
・普通のママや女性たちが特技を活かして輝いていくリアルストーリー

━━━━━━━━━━━━━━━━━━━━━
✨ 配信情報
━━━━━━━━━━━━━━━━━━━━━
・厳選したスカッと切り抜きShortsを随時配信中！
・通知（ベルマーク🔔）をオンにして、最新動画をチェックしてくださいね。

▼ 公式イベントカレンダー & ポータル
https://neofamily-calendar.kotsuka-folio.workers.dev/

#主婦のスカッと話 #ぶった斬り会長 #NEOFAMILY #切り抜き #Shorts #子育て #夫婦関係 #人間関係 #人生好転
""")

    print("✨ All folders synchronized perfectly!")

if __name__ == '__main__':
    print("🚀 Rebuilding YouTube branding with Katana Slash Situation & Vector Pills...")
    build_banner_sukatto()
    build_banner_community()
    build_icon_sukatto()
    build_icon_community()
    build_watermarks()
    sync_folders()
    print("🎉 All tasks completed with high precision!")
