#!/usr/bin/env python3
"""
Generate realistic watermark prototypes for YouTube.
Using Kaicho's real cutout photo, high-res vector-like shapes, and downscaling with Lanczos.
"""

import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# Paths
PHOTO_PATH = "assets/youtube/kaicho_photo_cutout.png"
FONT_BOLD = "/System/Library/Fonts/ヒラギノ角ゴシック W9.ttc"
FONT_HEAVY = "/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc"

def get_kaicho_head(size=(460, 460)):
    """Extract and enhance Kaicho's face from the cutout."""
    img = Image.open(PHOTO_PATH).convert("RGBA")
    # Head and shoulders bounding box in 608x870:
    # Top of hair is y=0, chin is around 320, chest is around 480.
    # Center X is around 360.
    box = (130, 0, 590, 480)
    head = img.crop(box)
    
    # Slight contrast & saturation boost for watermark pop
    enh_c = ImageEnhance.Contrast(head)
    head = enh_c.enhance(1.08)
    enh_s = ImageEnhance.Color(head)
    head = enh_s.enhance(1.05)
    
    return head

def add_sticker_border(image, border_width=12, border_color=(255, 255, 255, 255)):
    """Generate a clean white sticker border around transparent RGBA image."""
    alpha = image.split()[3]
    # Dilate alpha
    dilated = alpha.filter(ImageFilter.MaxFilter(border_width * 2 + 1))
    
    # Create border image
    border = Image.new("RGBA", image.size, border_color)
    border.putalpha(dilated)
    
    # Composite original over border
    result = Image.new("RGBA", image.size, (0, 0, 0, 0))
    result.paste(border, (0, 0))
    result.paste(image, (0, 0), image)
    return result

def add_drop_shadow(image, offset=(0, 8), blur_radius=12, shadow_color=(0, 0, 0, 140)):
    """Add a soft drop shadow."""
    alpha = image.split()[3]
    shadow_alpha = alpha.filter(ImageFilter.GaussianBlur(blur_radius))
    
    shadow = Image.new("RGBA", image.size, (shadow_color[0], shadow_color[1], shadow_color[2], 0))
    shadow.putalpha(shadow_alpha.point(lambda p: int(p * (shadow_color[3] / 255.0))))
    
    canvas = Image.new("RGBA", image.size, (0, 0, 0, 0))
    canvas.paste(shadow, offset, shadow)
    canvas.paste(image, (0, 0), image)
    return canvas

def draw_sunburst(draw, center, radius, ray_count=24, color1=(255, 215, 0), color2=(255, 185, 0)):
    """Draw circular sunburst rays."""
    cx, cy = center
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color1)
    
    angle_step = (2 * math.pi) / ray_count
    for i in range(0, ray_count, 2):
        a1 = i * angle_step
        a2 = (i + 1) * angle_step
        p1 = (cx, cy)
        p2 = (cx + radius * 1.5 * math.cos(a1), cy + radius * 1.5 * math.sin(a1))
        p3 = (cx + radius * 1.5 * math.cos(a2), cy + radius * 1.5 * math.sin(a2))
        draw.polygon([p1, p2, p3], fill=color2)

def draw_subscribe_button(draw, center_x, center_y, width, height, text="登録する", font_size=42, pill_color=(230, 33, 23), border_color=(255, 255, 255)):
    """Draw high-impact YouTube-style pill button with Play icon and text."""
    x1 = center_x - width // 2
    y1 = center_y - height // 2
    x2 = center_x + width // 2
    y2 = center_y + height // 2
    
    # Outer white/gold border
    if border_color:
        bw = 6
        draw.rounded_rectangle([x1 - bw, y1 - bw, x2 + bw, y2 + bw], radius=(height + bw * 2) // 2, fill=border_color)
    
    # Main red pill
    draw.rounded_rectangle([x1, y1, x2, y2], radius=height // 2, fill=pill_color)
    
    # White Play icon & text
    font = ImageFont.truetype(FONT_BOLD, font_size)
    
    # Draw white play triangle
    icon_w = int(height * 0.45)
    icon_h = int(height * 0.45)
    
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    total_w = icon_w + 12 + tw
    start_x = center_x - total_w // 2
    
    # Triangle
    tri_x = start_x
    tri_y = center_y - icon_h // 2
    draw.polygon([
        (tri_x, tri_y),
        (tri_x + icon_w, center_y),
        (tri_x, tri_y + icon_h)
    ], fill=(255, 255, 255, 255))
    
    # Text
    text_x = start_x + icon_w + 14
    text_y = center_y - th // 2 - 4
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))

def create_option_a_sunburst():
    """Option A: Vibrant Sunburst Circular Badge with real Kaicho face."""
    canvas_size = 600
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    
    # Sunburst mask layer
    burst_img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    burst_draw = ImageDraw.Draw(burst_img)
    center = (300, 300)
    radius = 270
    draw_sunburst(burst_draw, center, radius, ray_count=28, color1=(255, 218, 40), color2=(255, 175, 15))
    
    # Circular mask for sunburst
    mask = Image.new("L", (canvas_size, canvas_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], fill=255)
    
    # Golden border on circle
    burst_draw.ellipse([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], outline=(255, 255, 255), width=10)
    
    canvas.paste(burst_img, (0, 0), mask)
    
    # Kaicho photo
    head = get_kaicho_head()
    # Scale head to fit circle nicely: face prominent, bust at bottom
    head_w = 460
    head_h = int(head.size[1] * (head_w / head.size[0]))
    head_scaled = head.resize((head_w, head_h), Image.Resampling.LANCZOS)
    
    # Add sticker white outline to Kaicho so he pops from sunburst
    head_sticker = add_sticker_border(head_scaled, border_width=8, border_color=(255, 255, 255, 255))
    
    # Paste Kaicho so his head is nicely positioned
    # Head centered at x=300, top around y=45
    kx = (canvas_size - head_sticker.size[0]) // 2
    ky = 45
    canvas.paste(head_sticker, (kx, ky), head_sticker)
    
    # Mask bottom outside circle if any
    # Re-apply circular clip or let it overlap bottom slightly? Watermark looks best with button at bottom
    draw = ImageDraw.Draw(canvas)
    
    # Circular outer gold ring
    draw.ellipse([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], outline=(255, 255, 255), width=8)
    draw.ellipse([center[0] - radius - 4, center[1] - radius - 4, center[0] + radius + 4, center[1] + radius + 4], outline=(230, 160, 20), width=4)
    
    # Draw "登録する" button at bottom
    draw_subscribe_button(draw, center_x=300, center_y=490, width=400, height=100, text="登録する", font_size=52, pill_color=(235, 25, 25), border_color=(255, 255, 255))
    
    return canvas

def create_option_b_sticker():
    """Option B: Die-cut sticker (transparent BG, real Kaicho with thick white sticker border + subscribe button)."""
    canvas_size = 600
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    
    head = get_kaicho_head()
    # Scale head to fill nicely
    target_w = 500
    target_h = int(head.size[1] * (target_w / head.size[0]))
    head_scaled = head.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Create temp canvas for Kaicho + button
    temp = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    kx = (canvas_size - head_scaled.size[0]) // 2
    ky = 25
    temp.paste(head_scaled, (kx, ky), head_scaled)
    
    # Add button
    t_draw = ImageDraw.Draw(temp)
    draw_subscribe_button(t_draw, center_x=300, center_y=495, width=420, height=106, text="登録する", font_size=54, pill_color=(230, 30, 25), border_color=None)
    
    # Now create sticker outline around both Kaicho and the button!
    sticker = add_sticker_border(temp, border_width=14, border_color=(255, 255, 255, 255))
    # Add drop shadow
    final = add_drop_shadow(sticker, offset=(0, 8), blur_radius=10, shadow_color=(0, 0, 0, 130))
    return final

def create_option_c_kaicho_badge():
    """Option C: Circular Badge with 'ぶった斬り会長' + '登録' Red Pill."""
    canvas_size = 600
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    
    center = (300, 300)
    radius = 275
    
    # Background radial gradient
    bg = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(bg)
    draw_sunburst(bg_draw, center, radius, ray_count=24, color1=(255, 222, 60), color2=(255, 175, 15))
    
    mask = Image.new("L", (canvas_size, canvas_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], fill=255)
    
    canvas.paste(bg, (0, 0), mask)
    
    # Kaicho face
    head = get_kaicho_head()
    head_w = 460
    head_h = int(head.size[1] * (head_w / head.size[0]))
    head_scaled = head.resize((head_w, head_h), Image.Resampling.LANCZOS)
    head_sticker = add_sticker_border(head_scaled, border_width=8, border_color=(255, 255, 255, 255))
    
    kx = (canvas_size - head_sticker.size[0]) // 2
    ky = 50
    canvas.paste(head_sticker, (kx, ky), head_sticker)
    
    draw = ImageDraw.Draw(canvas)
    # White border around circle
    draw.ellipse([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], outline=(255, 255, 255), width=10)
    
    # Pill with "ぶった斬り会長 ♡ 登録"
    draw_subscribe_button(draw, center_x=300, center_y=490, width=470, height=96, text="ぶった斬り会長 登録", font_size=42, pill_color=(228, 28, 28), border_color=(255, 255, 255))
    
    return canvas

def create_option_d_youtube_pill():
    """Option D: Clean Official YouTube Red Button with Kaicho Head avatar."""
    canvas_size = 600
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    
    # Large rounded card
    draw = ImageDraw.Draw(canvas)
    
    # Outer white pill / rounded rectangle
    margin = 30
    rect = [margin, 40, canvas_size - margin, canvas_size - 40]
    
    # Dark modern background with subtle gradient
    draw.rounded_rectangle(rect, radius=60, fill=(20, 24, 33, 240), outline=(255, 255, 255, 255), width=8)
    
    # Kaicho circular avatar in center
    avatar_radius = 160
    avatar_center = (300, 240)
    
    # Face inside circle
    head = get_kaicho_head()
    # Crop square around face
    face_box = (150, 0, 570, 420)
    face_crop = img = Image.open(PHOTO_PATH).crop(face_box)
    face_crop = face_crop.resize((avatar_radius * 2, avatar_radius * 2), Image.Resampling.LANCZOS)
    
    avatar_mask = Image.new("L", (avatar_radius * 2, avatar_radius * 2), 0)
    am_draw = ImageDraw.Draw(avatar_mask)
    am_draw.ellipse([0, 0, avatar_radius * 2, avatar_radius * 2], fill=255)
    
    canvas.paste(face_crop, (avatar_center[0] - avatar_radius, avatar_center[1] - avatar_radius), avatar_mask)
    
    # Gold border on avatar
    draw.ellipse([avatar_center[0] - avatar_radius, avatar_center[1] - avatar_radius, avatar_center[0] + avatar_radius, avatar_center[1] + avatar_radius], outline=(255, 215, 0), width=8)
    
    # YouTube red subscribe button at bottom
    draw_subscribe_button(draw, center_x=300, center_y=475, width=460, height=96, text="チャンネル登録", font_size=46, pill_color=(235, 25, 25), border_color=(255, 255, 255))
    
    return canvas

def main():
    options = {
        "scratch/real_watermark_opt_a_sunburst.png": create_option_a_sunburst(),
        "scratch/real_watermark_opt_b_sticker.png": create_option_b_sticker(),
        "scratch/real_watermark_opt_c_kaicho.png": create_option_c_kaicho_badge(),
        "scratch/real_watermark_opt_d_official.png": create_option_d_youtube_pill(),
    }
    
    for path, img in options.items():
        # Save 600x600 high-res
        img.save(path)
        print(f"Saved high-res {path}")
        
        # Save 150x150 downscaled version
        small_path = path.replace(".png", "_150.png")
        small_img = img.resize((150, 150), Image.Resampling.LANCZOS)
        small_img.save(small_path)
        print(f"Saved 150x150 {small_path}")

if __name__ == "__main__":
    main()
