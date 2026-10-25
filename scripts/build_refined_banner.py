# -*- coding: utf-8 -*-
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_ultimate_banner():
    W, H = 2560, 1440
    
    # Fonts
    font_title = ImageFont.truetype('/System/Library/Fonts/ヒラギノ角ゴシック W9.ttc', 112)
    font_subtitle = ImageFont.truetype('/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc', 38)
    font_catch = ImageFont.truetype('/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc', 26)
    font_badge = ImageFont.truetype('/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc', 22)
    font_pill = ImageFont.truetype('/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc', 21)
    
    font_tv_brand = ImageFont.truetype('/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc', 30)
    font_tv_en = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 18)
    font_tv_bottom = ImageFont.truetype('/System/Library/Fonts/ヒラギノ角ゴシック W7.ttc', 24)
    
    # 1. Base Canvas with Rich Midnight Royal Navy Gradient
    base = Image.new('RGBA', (W, H), (8, 14, 34, 255))
    draw_base = ImageDraw.Draw(base)
    
    for y in range(H):
        dist = abs(y - 720) / 720.0
        # Deep royal navy at center (16, 32, 78), Midnight black-navy at top & bottom (5, 9, 22)
        r = int(16 - 11 * (dist ** 1.2))
        g = int(32 - 23 * (dist ** 1.2))
        b = int(78 - 56 * (dist ** 1.2))
        draw_base.line([(0, y), (W, y)], fill=(r, g, b, 255))
        
    # 2. Dynamic Gold & Amber Sunburst
    sunburst = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_sun = ImageDraw.Draw(sunburst)
    cx, cy = 1790, 720
    radius = 2900
    ray_count = 36
    angle_step = 2 * math.pi / ray_count
    
    for i in range(0, ray_count, 2):
        a1 = i * angle_step
        a2 = (i + 1) * angle_step
        x1 = cx + radius * math.cos(a1)
        y1 = cy + radius * math.sin(a1)
        x2 = cx + radius * math.cos(a2)
        y2 = cy + radius * math.sin(a2)
        
        # Warm golden amber rays
        draw_sun.polygon([(cx, cy), (x1, y1), (x2, y2)], fill=(255, 212, 70, 44))
        
    # Radial mask for sunburst: soft natural fade
    radial_mask = Image.new('L', (W, H), 0)
    draw_rm = ImageDraw.Draw(radial_mask)
    for r in range(1900, 0, -25):
        alpha = int(255 * (1.0 - (r / 1900.0) ** 1.4))
        draw_rm.ellipse([cx - r, cy - r, cx + r, cy + r], fill=min(255, alpha))
        
    base.paste(sunburst, (0, 0), radial_mask)
    
    # 3. TV Area Cinema Styling (Top & Bottom Accents)
    tv_accents = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_tv = ImageDraw.Draw(tv_accents)
    
    # Helper to draw vector 4-point star
    def draw_star(draw_obj, center_x, center_y, outer_r, inner_r, fill_color):
        points = []
        for p in range(8):
            r = outer_r if (p % 2 == 0) else inner_r
            ang = p * math.pi / 4.0 - math.pi / 2.0
            points.append((center_x + r * math.cos(ang), center_y + r * math.sin(ang)))
        draw_obj.polygon(points, fill=fill_color)

    # A. Top Brand Header
    top_title = "NEO FAMILY  公式  YouTube チャンネル"
    bbox_top = font_tv_brand.getbbox(top_title)
    tw_top = bbox_top[2] - bbox_top[0]
    tx_top = (W - tw_top) // 2
    ty_top = 265
    
    # Stars beside top title
    draw_star(draw_tv, tx_top - 40, ty_top + 16, 14, 4, (255, 225, 100, 240))
    draw_star(draw_tv, tx_top + tw_top + 40, ty_top + 16, 14, 4, (255, 225, 100, 240))
    
    # Flanking gold lines
    line_y = ty_top + 16
    line_len = 260
    for lx in range(line_len):
        l_alpha = int(210 * (lx / line_len))
        draw_tv.line([(tx_top - 65 - line_len + lx, line_y), (tx_top - 65 - line_len + lx, line_y)], fill=(255, 215, 90, l_alpha), width=2)
        l_alpha_r = int(210 * (1.0 - lx / line_len))
        draw_tv.line([(tx_top + tw_top + 65 + lx, line_y), (tx_top + tw_top + 65 + lx, line_y)], fill=(255, 215, 90, l_alpha_r), width=2)
        
    draw_tv.text((tx_top, ty_top), top_title, font=font_tv_brand, fill=(255, 235, 135, 220))
    
    top_sub = "OFFICIAL SHORTS & HIGHLIGHTS"
    bbox_sub = font_tv_en.getbbox(top_sub)
    tw_sub = bbox_sub[2] - bbox_sub[0]
    draw_tv.text(((W - tw_sub) // 2, ty_top + 46), top_sub, font=font_tv_en, fill=(215, 195, 140, 160))
    
    # B. Bottom Tagline
    bot_title = "DREAM TO REALITY   ★   100 BILLION MINDSET   ★   BE HAPPY TOGETHER"
    bbox_bot = font_tv_bottom.getbbox(bot_title)
    tw_bot = bbox_bot[2] - bbox_bot[0]
    tx_bot = (W - tw_bot) // 2
    ty_bot = 1145
    
    line_y_b = ty_bot + 13
    for lx in range(line_len):
        l_alpha = int(190 * (lx / line_len))
        draw_tv.line([(tx_bot - 45 - line_len + lx, line_y_b), (tx_bot - 45 - line_len + lx, line_y_b)], fill=(255, 215, 90, l_alpha), width=2)
        l_alpha_r = int(190 * (1.0 - lx / line_len))
        draw_tv.line([(tx_bot + tw_bot + 45 + lx, line_y_b), (tx_bot + tw_bot + 45 + lx, line_y_b)], fill=(255, 215, 90, l_alpha_r), width=2)
        
    draw_tv.text((tx_bot, ty_bot), bot_title, font=font_tv_bottom, fill=(255, 225, 120, 190))
    
    # Sparkle stars in TV area
    random.seed(123)
    for _ in range(50):
        sx = random.randint(80, W - 80)
        sy = random.randint(60, H - 60)
        if 480 < sx < 1650 and 500 < sy < 940:
            continue
        sz = random.randint(8, 24)
        star_alpha = random.randint(110, 220)
        draw_star(draw_tv, sx, sy, sz, sz * 0.28, (255, 240, 170, star_alpha))
        
    base = Image.alpha_composite(base, tv_accents)
    
    # 4. Soft Vignette Glow behind text
    text_glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_tg = ImageDraw.Draw(text_glow)
    draw_tg.ellipse([450, 470, 1720, 970], fill=(4, 8, 20, 195))
    text_glow = text_glow.filter(ImageFilter.GaussianBlur(65))
    base = Image.alpha_composite(base, text_glow)
    
    # 5. Kaicho Photo - Exactly within Safe Area (509 .. 932)
    kaicho_raw = Image.open('assets/youtube/kaicho_photo_cutout.png')
    bbox = kaicho_raw.getbbox()
    kaicho_crop = kaicho_raw.crop(bbox) # 539 x 719
    
    # Safe Area Height is 423 (from Y=509 to Y=932)
    # Set photo height to 414: top at Y=516 (7px below safe top), bottom at Y=930 (2px above safe bottom)
    target_photo_h = 414
    target_photo_w = int(target_photo_h * (kaicho_crop.width / kaicho_crop.height)) # 310px
    kaicho_resized = kaicho_crop.resize((target_photo_w, target_photo_h), Image.Resampling.LANCZOS)
    
    # Position: X: 1640 .. 1950 (Leaves ~100px safe margin to right edge of safe area at 2053)
    photo_x = 1640
    photo_y = 516
    
    # White sticker outline
    alpha = kaicho_resized.split()[3]
    outline_img = Image.new('RGBA', (target_photo_w + 30, target_photo_h + 30), (0, 0, 0, 0))
    outline_img.paste(Image.new('RGBA', (target_photo_w, target_photo_h), (255, 255, 255, 255)), (15, 15), alpha)
    outline_mask = outline_img.split()[3].filter(ImageFilter.MaxFilter(11))
    
    # Drop shadow
    shadow_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    shadow_stamp = Image.new('RGBA', outline_img.size, (0, 0, 0, 200))
    shadow_img.paste(shadow_stamp, (photo_x - 15, photo_y - 4), outline_mask)
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(18))
    base = Image.alpha_composite(base, shadow_img)
    
    # Sticker outline
    white_sticker = Image.new('RGBA', outline_img.size, (255, 255, 255, 255))
    base.paste(white_sticker, (photo_x - 15, photo_y - 15), outline_mask)
    
    # Paste Photo
    base.paste(kaicho_resized, (photo_x, photo_y), kaicho_resized)
    
    # 6. Main Text & Badge Elements
    text_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_txt = ImageDraw.Draw(text_layer)
    
    tx = 535 # 28px inside safe area left edge (507)
    
    # A. Badge: ★ ぶった斬り会長公認 ★
    badge_y = 534
    badge_w = 340
    badge_h = 42
    badge_r = 21
    draw_txt.rounded_rectangle([tx, badge_y, tx + badge_w, badge_y + badge_h], radius=badge_r, fill=(215, 20, 50, 250), outline=(255, 220, 60, 255), width=3)
    badge_str = "★ ぶった斬り会長公認 ★"
    b_bbox = font_badge.getbbox(badge_str)
    bw = b_bbox[2] - b_bbox[0]
    draw_txt.text((tx + (badge_w - bw) // 2, badge_y + 8), badge_str, font=font_badge, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))
    
    # B. Main Title: ぶった斬り会長
    title_str = "ぶった斬り会長"
    title_y = 588
    
    # Drop shadow
    title_shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_ts = ImageDraw.Draw(title_shadow)
    draw_ts.text((tx + 2, title_y + 10), title_str, font=font_title, fill=(0, 0, 0, 200), stroke_width=26, stroke_fill=(0, 0, 0, 200))
    title_shadow = title_shadow.filter(ImageFilter.GaussianBlur(8))
    base = Image.alpha_composite(base, title_shadow)
    
    # Multi-stroke title
    def draw_text_with_outline(draw_ctx, text, pos, font, fill_color, stroke_layers):
        for sw, sc in stroke_layers:
            draw_ctx.text(pos, text, font=font, fill=sc, stroke_width=sw, stroke_fill=sc)
        draw_ctx.text(pos, text, font=font, fill=fill_color)
        
    draw_text_with_outline(
        draw_txt,
        title_str,
        (tx - 4, title_y),
        font_title,
        fill_color=(255, 240, 50, 255),
        stroke_layers=[
            (26, (255, 255, 255, 255)),
            (14, (190, 28, 15, 255))
        ]
    )
    
    # C. Subtitle: 【公認】夢をカタチにする切り抜きShorts
    sub_str = "【公認】夢をカタチにする切り抜きShorts"
    sub_y = 730
    draw_text_with_outline(
        draw_txt,
        sub_str,
        (tx, sub_y),
        font_subtitle,
        fill_color=(255, 255, 255, 255),
        stroke_layers=[
            (10, (10, 30, 80, 255)),
            (5, (0, 0, 0, 255))
        ]
    )
    
    # D. Catchphrase: 100億企業を創ったリアル思考 × 心身と経済の豊かさを仲間と共に
    catch_str = "100億企業を創ったリアル思考 × 心身と経済の豊かさを仲間と共に"
    catch_y = 786
    draw_text_with_outline(
        draw_txt,
        catch_str,
        (tx, catch_y),
        font_catch,
        fill_color=(255, 244, 195, 255),
        stroke_layers=[
            (5, (0, 0, 0, 255))
        ]
    )
    
    # E. Pill Button with Vector YouTube Play Icon!
    pill_y = 838
    pill_w = 460
    pill_h = 44
    pill_r = 22
    draw_txt.rounded_rectangle([tx, pill_y, tx + pill_w, pill_y + pill_h], radius=pill_r, fill=(245, 60, 20, 245), outline=(255, 255, 255, 255), width=2)
    
    # Draw vector play icon: white rounded rect + red triangle
    icon_x = tx + 18
    icon_y = pill_y + 10
    icon_w = 32
    icon_h = 24
    draw_txt.rounded_rectangle([icon_x, icon_y, icon_x + icon_w, icon_y + icon_h], radius=6, fill=(255, 255, 255, 255))
    # Red play triangle
    tri_x = icon_x + 12
    tri_y = icon_y + 6
    draw_txt.polygon([(tri_x, tri_y), (tri_x + 11, tri_y + 6), (tri_x, tri_y + 12)], fill=(245, 60, 20, 255))
    
    pill_text = "Shorts毎日配信中！チャンネル登録してね♡"
    draw_txt.text((icon_x + icon_w + 12, pill_y + 11), pill_text, font=font_pill, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))
    
    base = Image.alpha_composite(base, text_layer)
    
    # 7. Final Output Image (2560 x 1440)
    final_rgb = base.convert('RGB')
    final_rgb.save('assets/youtube/youtube_banner_photo_illust.jpg', quality=95)
    base.save('assets/youtube/youtube_banner_photo_illust.png')
    print("Saved youtube_banner_photo_illust.jpg & .png")
    
    # 8. Mocks & Previews
    # A. Studio Mockup (with overlay lines)
    mock = final_rgb.copy()
    dim = Image.new('RGBA', (W, H), (0, 0, 0, 115))
    draw_dim = ImageDraw.Draw(dim)
    draw_dim.rectangle([0, 509, W, 932], fill=(0, 0, 0, 0)) # clear desktop
    mock_with_dim = Image.alpha_composite(mock.convert('RGBA'), dim)
    draw_m = ImageDraw.Draw(mock_with_dim)
    
    font_guide = ImageFont.truetype('/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc', 30)
    
    # TV area (outer border)
    draw_m.rectangle([4, 4, W - 4, H - 4], outline=(0, 160, 255, 255), width=4)
    draw_m.text((30, 30), "テレビで表示可能 (2560 x 1440)", font=font_guide, fill=(0, 220, 255, 255))
    
    # Desktop area (0 .. 2560, 509 .. 932)
    draw_m.rectangle([0, 509, W, 932], outline=(0, 160, 255, 255), width=4)
    draw_m.text((30, 520), "パソコンで表示可能 (2560 x 423)", font=font_guide, fill=(0, 220, 255, 255))
    
    # Safe area (507 .. 2053, 509 .. 932)
    draw_m.rectangle([507, 509, 2053, 932], outline=(0, 230, 255, 255), width=4)
    draw_m.text((520, 520), "すべてのデバイスで表示可能 (1546 x 423)", font=font_guide, fill=(0, 255, 255, 255))
    
    mock_with_dim.convert('RGB').save('scratch/youtube_banner_studio_preview.jpg', quality=92)
    
    # B. Mobile / All Devices (1546 x 423)
    mobile_crop = final_rgb.crop((507, 509, 2053, 932))
    mobile_crop.save('scratch/preview_mobile_safe_area.jpg', quality=95)
    
    # C. Desktop (2560 x 423)
    desktop_crop = final_rgb.crop((0, 509, 2560, 932))
    desktop_crop.save('scratch/preview_desktop.jpg', quality=95)
    
    print("Saved all preview images in scratch/")

if __name__ == '__main__':
    create_ultimate_banner()
