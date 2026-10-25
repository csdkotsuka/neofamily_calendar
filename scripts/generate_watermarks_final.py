#!/usr/bin/env python3
"""
Refine YouTube watermarks with Kaicho's real face, high precision masks,
and perfect antialiasing at both 150x150 and 500x500.
"""

import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

PHOTO_PATH = "assets/youtube/kaicho_photo_cutout.png"
FONT_BOLD = "/System/Library/Fonts/ヒラギノ角ゴシック W9.ttc"
FONT_HEAVY = "/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc"

def get_enhanced_head():
    img = Image.open(PHOTO_PATH).convert("RGBA")
    # Kaicho's face and upper chest: x: 130 to 590, y: 0 to 490
    box = (130, 0, 590, 490)
    head = img.crop(box)
    
    # Mild contrast and color boost for video overlay visibility
    head = ImageEnhance.Contrast(head).enhance(1.08)
    head = ImageEnhance.Color(head).enhance(1.06)
    head = ImageEnhance.Brightness(head).enhance(1.02)
    return head

def add_outline(image, width=12, color=(255, 255, 255, 255)):
    alpha = image.split()[3]
    dilated = alpha.filter(ImageFilter.MaxFilter(width * 2 + 1))
    outline = Image.new("RGBA", image.size, color)
    outline.putalpha(dilated)
    
    res = Image.new("RGBA", image.size, (0, 0, 0, 0))
    res.paste(outline, (0, 0))
    res.paste(image, (0, 0), image)
    return res

def add_shadow(image, offset=(0, 6), blur=10, opacity=120):
    alpha = image.split()[3]
    shadow_alpha = alpha.filter(ImageFilter.GaussianBlur(blur))
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    shadow.putalpha(shadow_alpha.point(lambda p: int(p * (opacity / 255.0))))
    
    canvas = Image.new("RGBA", image.size, (0, 0, 0, 0))
    canvas.paste(shadow, offset, shadow)
    canvas.paste(image, (0, 0), image)
    return canvas

def draw_sunburst(draw, center, radius, ray_count=28, c1=(255, 222, 50), c2=(255, 175, 15)):
    cx, cy = center
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=c1)
    step = (2 * math.pi) / ray_count
    for i in range(0, ray_count, 2):
        a1 = i * step
        a2 = (i + 1) * step
        p1 = (cx, cy)
        p2 = (cx + radius * 1.5 * math.cos(a1), cy + radius * 1.5 * math.sin(a1))
        p3 = (cx + radius * 1.5 * math.cos(a2), cy + radius * 1.5 * math.sin(a2))
        draw.polygon([p1, p2, p3], fill=c2)

def draw_pill_button(draw, cx, cy, w, h, text="登録する", font_size=52, bg_color=(235, 25, 25), stroke_color=(255, 255, 255), stroke_w=6, show_icon=True):
    x1, y1 = cx - w // 2, cy - h // 2
    x2, y2 = cx + w // 2, cy + h // 2
    
    # Outer border
    if stroke_color and stroke_w > 0:
        draw.rounded_rectangle([x1 - stroke_w, y1 - stroke_w, x2 + stroke_w, y2 + stroke_w],
                               radius=(h + stroke_w * 2) // 2, fill=stroke_color)
    
    # Main pill
    draw.rounded_rectangle([x1, y1, x2, y2], radius=h // 2, fill=bg_color)
    
    # Play icon + Text
    font = ImageFont.truetype(FONT_BOLD, font_size)
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    if show_icon:
        tri_w = int(h * 0.40)
        tri_h = int(h * 0.40)
        gap = 14
        total_w = tri_w + gap + tw
        start_x = cx - total_w // 2
        
        # Play triangle
        draw.polygon([
            (start_x, cy - tri_h // 2),
            (start_x + tri_w, cy),
            (start_x, cy + tri_h // 2)
        ], fill=(255, 255, 255, 255))
        
        tx = start_x + tri_w + gap
    else:
        tx = cx - tw // 2
        
    ty = cy - th // 2 - 4
    draw.text((tx, ty), text, font=font, fill=(255, 255, 255, 255))

def build_sunburst_stamp(size=600):
    """
    Circular gold sunburst badge with real Kaicho face cleanly framed
    and '登録する' pill button seamlessly anchored at the bottom.
    """
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    center = (size // 2, size // 2)
    radius = int(size * 0.45) # 270
    
    # 1. Circular sunburst background
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(bg)
    draw_sunburst(bg_draw, center, radius, ray_count=28)
    
    # 2. Kaicho face & upper chest
    head = get_enhanced_head()
    hw = int(size * 0.88) # large prominent face
    hh = int(head.size[1] * (hw / head.size[0]))
    head_scaled = head.resize((hw, hh), Image.Resampling.LANCZOS)
    
    # White sticker stroke around Kaicho
    head_outline = add_outline(head_scaled, width=10, color=(255, 255, 255, 255))
    
    kx = (size - head_outline.size[0]) // 2
    ky = int(size * 0.05) # top margin
    bg.paste(head_outline, (kx, ky), head_outline)
    
    # 3. Clip background + Kaicho to perfect circle
    circle_mask = Image.new("L", (size, size), 0)
    cm_draw = ImageDraw.Draw(circle_mask)
    cm_draw.ellipse([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], fill=255)
    
    canvas.paste(bg, (0, 0), circle_mask)
    
    # 4. Outer gold & white border rings
    draw = ImageDraw.Draw(canvas)
    draw.ellipse([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius],
                 outline=(255, 255, 255, 255), width=10)
    draw.ellipse([center[0] - radius - 5, center[1] - radius - 5, center[0] + radius + 5, center[1] + radius + 5],
                 outline=(225, 160, 20, 255), width=5)
    
    # 5. Bottom button: anchored cleanly across bottom rim
    btn_h = int(size * 0.18) # 108
    btn_y = center[1] + radius - btn_h // 2 + 6 # hugs the bottom curve
    btn_w = int(size * 0.74) # 444
    draw_pill_button(draw, center[0], btn_y, btn_w, btn_h, text="登録する", font_size=56,
                     bg_color=(235, 25, 25), stroke_color=(255, 255, 255), stroke_w=7)
    
    return add_shadow(canvas, offset=(0, 6), blur=8, opacity=110)

def build_sticker_stamp(size=600):
    """
    Transparent die-cut sticker style with real Kaicho bust + subscribe button.
    """
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    
    head = get_enhanced_head()
    hw = int(size * 0.86)
    hh = int(head.size[1] * (hw / head.size[0]))
    head_scaled = head.resize((hw, hh), Image.Resampling.LANCZOS)
    
    temp = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    kx = (size - head_scaled.size[0]) // 2
    ky = int(size * 0.04)
    temp.paste(head_scaled, (kx, ky), head_scaled)
    
    t_draw = ImageDraw.Draw(temp)
    btn_h = int(size * 0.18)
    btn_y = int(size * 0.83)
    btn_w = int(size * 0.74)
    draw_pill_button(t_draw, size // 2, btn_y, btn_w, btn_h, text="登録する", font_size=56,
                     bg_color=(230, 25, 25), stroke_color=(255, 255, 255), stroke_w=6)
    
    # Outer white sticker border around both Kaicho and button
    sticker = add_outline(temp, width=16, color=(255, 255, 255, 255))
    final = add_shadow(sticker, offset=(0, 8), blur=12, opacity=130)
    return final

def build_shorts_banner_stamp(w=800, h=160):
    """
    Horizontal banner stamp for Shorts video footer (800x160).
    Real Kaicho photo circle + 'ぶった斬り会長' title + Red Subscribe button.
    """
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    # Dark rounded pill container
    margin = 8
    draw.rounded_rectangle([margin, margin, w - margin, h - margin], radius=(h - margin*2) // 2,
                           fill=(18, 24, 38, 245), outline=(255, 215, 0, 255), width=4)
    
    # Left avatar circle
    avatar_r = (h - margin*2 - 12) // 2
    avatar_cx = margin + 6 + avatar_r
    avatar_cy = h // 2
    
    # Kaicho circular avatar with sunburst
    av_size = avatar_r * 2
    av_img = Image.new("RGBA", (av_size, av_size), (0, 0, 0, 0))
    av_draw = ImageDraw.Draw(av_img)
    draw_sunburst(av_draw, (avatar_r, avatar_r), avatar_r, ray_count=20)
    
    head = get_enhanced_head()
    head_scaled = head.resize((int(av_size * 1.15), int(av_size * 1.15)), Image.Resampling.LANCZOS)
    av_img.paste(head_scaled, ((av_size - head_scaled.size[0]) // 2, 2), head_scaled)
    
    # Mask to circle
    av_mask = Image.new("L", (av_size, av_size), 0)
    ImageDraw.Draw(av_mask).ellipse([0, 0, av_size, av_size], fill=255)
    
    canvas.paste(av_img, (avatar_cx - avatar_r, avatar_cy - avatar_r), av_mask)
    draw.ellipse([avatar_cx - avatar_r, avatar_cy - avatar_r, avatar_cx + avatar_r, avatar_cy + avatar_r],
                 outline=(255, 255, 255), width=4)
    
    # Right red subscribe button (compact so left text has plenty of room)
    btn_w = 116
    btn_h = h - margin*2 - 24
    btn_cx = w - margin - 12 - btn_w // 2
    draw_pill_button(draw, btn_cx, avatar_cy, btn_w, btn_h, text="登録", font_size=32,
                     bg_color=(235, 25, 25), stroke_color=(255, 255, 255), stroke_w=3, show_icon=False)
    
    # Center text
    font_title = ImageFont.truetype(FONT_BOLD, 38)
    font_sub = ImageFont.truetype(FONT_HEAVY, 18)
    
    tx = avatar_cx + avatar_r + 20
    draw.text((tx, avatar_cy - 30), "ぶった斬り会長", font=font_title, fill=(255, 245, 100), stroke_width=4, stroke_fill=(0, 0, 0))
    draw.text((tx, avatar_cy + 14), "【NEO FAMILY】チャンネル登録＆高評価してね♥", font=font_sub, fill=(255, 255, 255))
    
    return add_shadow(canvas, offset=(0, 4), blur=6, opacity=120)

def main():
    print("Generating watermark designs with Kaicho's real face...")
    
    # 1. Sunburst badge (clean, clipped)
    sunburst = build_sunburst_stamp(600)
    sunburst.save("scratch/wm_sunburst_600.png")
    sunburst_150 = sunburst.resize((150, 150), Image.Resampling.LANCZOS)
    sunburst_150.save("scratch/wm_sunburst_150.png")
    
    # 2. Die-cut sticker (transparent BG)
    sticker = build_sticker_stamp(600)
    sticker.save("scratch/wm_sticker_600.png")
    sticker_150 = sticker.resize((150, 150), Image.Resampling.LANCZOS)
    sticker_150.save("scratch/wm_sticker_150.png")
    
    # 3. Horizontal Shorts banner stamp
    banner_stamp = build_shorts_banner_stamp(800, 160)
    banner_stamp.save("scratch/wm_shorts_banner_stamp.png")
    
    # Update primary assets
    # Standard 150x150 YouTube Watermark
    sunburst_150.save("assets/youtube/youtube_watermark_standard.png")
    print("Updated assets/youtube/youtube_watermark_standard.png (150x150)")
    
    # Transparent die-cut sticker variant (150x150)
    sticker_150.save("assets/youtube/youtube_watermark_sticker.png")
    print("Saved assets/youtube/youtube_watermark_sticker.png (150x150)")
    
    # Shorts Watermark (500x500 high-res)
    shorts_wm = sunburst.resize((500, 500), Image.Resampling.LANCZOS)
    shorts_wm.save("assets/youtube/youtube_shorts_watermark.png")
    print("Updated assets/youtube/youtube_shorts_watermark.png (500x500)")
    
    shorts_wm_sticker = sticker.resize((500, 500), Image.Resampling.LANCZOS)
    shorts_wm_sticker.save("assets/youtube/youtube_shorts_watermark_sticker.png")
    print("Saved assets/youtube/youtube_shorts_watermark_sticker.png (500x500)")
    
    # Shorts Banner Stamp (800x160)
    banner_stamp.save("assets/youtube/youtube_shorts_banner_stamp.png")
    print("Updated assets/youtube/youtube_shorts_banner_stamp.png (800x160)")

if __name__ == "__main__":
    main()
