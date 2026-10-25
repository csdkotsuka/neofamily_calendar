import Foundation
import CoreGraphics
import CoreText
import AppKit

// MARK: - Helper Functions
func createCGContext(width: Int, height: Int) -> CGContext? {
    let colorSpace = CGColorSpaceCreateDeviceRGB()
    let bitmapInfo = CGImageAlphaInfo.premultipliedLast.rawValue
    return CGContext(data: nil, width: width, height: height, bitsPerComponent: 8, bytesPerRow: width * 4, space: colorSpace, bitmapInfo: bitmapInfo)
}

func loadCGImage(from path: String) -> CGImage? {
    guard let img = NSImage(contentsOfFile: path),
          let rep = img.representations.first as? NSBitmapImageRep,
          let cg = rep.cgImage else {
        return nil
    }
    return cg
}

func saveCGImageAsPNG(_ image: CGImage, to path: String) {
    let rep = NSBitmapImageRep(cgImage: image)
    guard let data = rep.representation(using: .png, properties: [:]) else { return }
    try? data.write(to: URL(fileURLWithPath: path))
    print("Saved PNG: \(path)")
}

func saveCGImageAsJPEG(_ image: CGImage, to path: String, quality: Double = 0.92) {
    let rep = NSBitmapImageRep(cgImage: image)
    guard let data = rep.representation(using: .jpeg, properties: [.compressionFactor: quality]) else { return }
    try? data.write(to: URL(fileURLWithPath: path))
    print("Saved JPEG: \(path)")
}

// Draw radial sunburst rays
func drawSunburst(context: CGContext, center: CGPoint, radius: CGFloat, rayCount: Int, color1: NSColor, color2: NSColor) {
    context.saveGState()
    context.setFillColor(color1.cgColor)
    context.fill(context.boundingBoxOfClipPath)
    
    let angleStep = (CGFloat.pi * 2.0) / CGFloat(rayCount)
    context.setFillColor(color2.cgColor)
    
    for i in 0..<rayCount {
        if i % 2 == 0 {
            let startAngle = CGFloat(i) * angleStep
            let endAngle = CGFloat(i + 1) * angleStep
            
            let path = CGMutablePath()
            path.move(to: center)
            path.addArc(center: center, radius: radius, startAngle: startAngle, endAngle: endAngle, clockwise: false)
            path.closeSubpath()
            
            context.addPath(path)
            context.fillPath()
        }
    }
    context.restoreGState()
}

// Draw pop stars
func drawStar(context: CGContext, center: CGPoint, points: Int = 4, outerRadius: CGFloat, innerRadius: CGFloat, fillColor: CGColor, strokeColor: CGColor? = nil, strokeWidth: CGFloat = 0) {
    let path = CGMutablePath()
    let angleStep = CGFloat.pi / CGFloat(points)
    
    for i in 0..<(points * 2) {
        let radius = (i % 2 == 0) ? outerRadius : innerRadius
        let angle = CGFloat(i) * angleStep - CGFloat.pi / 2.0
        let x = center.x + radius * cos(angle)
        let y = center.y + radius * sin(angle)
        if i == 0 {
            path.move(to: CGPoint(x: x, y: y))
        } else {
            path.addLine(to: CGPoint(x: x, y: y))
        }
    }
    path.closeSubpath()
    
    context.setFillColor(fillColor)
    context.addPath(path)
    context.fillPath()
    
    if let stroke = strokeColor, strokeWidth > 0 {
        context.setStrokeColor(stroke)
        context.setLineWidth(strokeWidth)
        context.addPath(path)
        context.strokePath()
    }
}

// Draw text with multiple outlines
func drawOutlinedText(context: CGContext, text: String, point: CGPoint, fontName: String, fontSize: CGFloat, fillColor: CGColor, strokeColor: CGColor, strokeWidth: CGFloat, outerStrokeColor: CGColor? = nil, outerStrokeWidth: CGFloat = 0) {
    let font = CTFontCreateWithName(fontName as CFString, fontSize, nil)
    
    // Outer stroke if present
    if let outerColor = outerStrokeColor, outerStrokeWidth > 0 {
        let outerAttributes: [NSAttributedString.Key: Any] = [
            NSAttributedString.Key(kCTFontAttributeName as String): font,
            NSAttributedString.Key(kCTStrokeColorAttributeName as String): outerColor,
            NSAttributedString.Key(kCTStrokeWidthAttributeName as String): (outerStrokeWidth / fontSize) * 100.0,
            NSAttributedString.Key(kCTForegroundColorAttributeName as String): outerColor
        ]
        let attrString = NSAttributedString(string: text, attributes: outerAttributes)
        let line = CTLineCreateWithAttributedString(attrString)
        context.textPosition = point
        CTLineDraw(line, context)
    }
    
    // Middle/Standard stroke
    if strokeWidth > 0 {
        let strokeAttributes: [NSAttributedString.Key: Any] = [
            NSAttributedString.Key(kCTFontAttributeName as String): font,
            NSAttributedString.Key(kCTStrokeColorAttributeName as String): strokeColor,
            NSAttributedString.Key(kCTStrokeWidthAttributeName as String): (strokeWidth / fontSize) * 100.0,
            NSAttributedString.Key(kCTForegroundColorAttributeName as String): strokeColor
        ]
        let attrString = NSAttributedString(string: text, attributes: strokeAttributes)
        let line = CTLineCreateWithAttributedString(attrString)
        context.textPosition = point
        CTLineDraw(line, context)
    }
    
    // Fill text
    let fillAttributes: [NSAttributedString.Key: Any] = [
        NSAttributedString.Key(kCTFontAttributeName as String): font,
        NSAttributedString.Key(kCTForegroundColorAttributeName as String): fillColor
    ]
    let attrString = NSAttributedString(string: text, attributes: fillAttributes)
    let line = CTLineCreateWithAttributedString(attrString)
    context.textPosition = point
    CTLineDraw(line, context)
}

// =================================================================
// 1. YouTube Banner Anime Illustration (2560 x 1440)
// =================================================================
print("--- Generating YouTube Banner (Anime Illustration) ---")
if let ctx = createCGContext(width: 2560, height: 1440),
   let bgImage = loadCGImage(from: "assets/youtube/ai_banner_male_raw.jpg") {
    
    ctx.draw(bgImage, in: CGRect(x: 0, y: 0, width: 2560, height: 1440))
    
    // Gradient dark overlay on left for text readability
    let colorSpace = CGColorSpaceCreateDeviceRGB()
    let gradColors = [
        NSColor(red: 0.05, green: 0.08, blue: 0.18, alpha: 0.90).cgColor,
        NSColor(red: 0.05, green: 0.08, blue: 0.18, alpha: 0.45).cgColor,
        NSColor(red: 0.05, green: 0.08, blue: 0.18, alpha: 0.0).cgColor
    ] as CFArray
    let gradLocations: [CGFloat] = [0.0, 0.45, 0.75]
    if let gradient = CGGradient(colorsSpace: colorSpace, colors: gradColors, locations: gradLocations) {
        ctx.drawLinearGradient(gradient, start: CGPoint(x: 480, y: 720), end: CGPoint(x: 1650, y: 720), options: [])
    }
    
    // Badge Tag: ★ NEO FAMILY 公式 ★
    let badgeRect = CGRect(x: 540, y: 835, width: 330, height: 42)
    ctx.setFillColor(NSColor(red: 0.88, green: 0.12, blue: 0.28, alpha: 0.95).cgColor)
    let badgePath = CGPath(roundedRect: badgeRect, cornerWidth: 21, cornerHeight: 21, transform: nil)
    ctx.addPath(badgePath)
    ctx.fillPath()
    
    ctx.setStrokeColor(NSColor(red: 1.0, green: 0.85, blue: 0.2, alpha: 1.0).cgColor)
    ctx.setLineWidth(3.0)
    ctx.addPath(badgePath)
    ctx.strokePath()
    
    drawOutlinedText(
        context: ctx,
        text: "★ NEO FAMILY 公式 ★",
        point: CGPoint(x: 575, y: 846),
        fontName: "HiraginoSans-W8",
        fontSize: 22,
        fillColor: NSColor.white.cgColor,
        strokeColor: NSColor.black.cgColor,
        strokeWidth: 2
    )
    
    // Main Title: ぶった斬り会長
    drawOutlinedText(
        context: ctx,
        text: "ぶった斬り会長",
        point: CGPoint(x: 535, y: 715),
        fontName: "HiraginoSans-W9",
        fontSize: 105,
        fillColor: NSColor(red: 1.0, green: 0.92, blue: 0.25, alpha: 1.0).cgColor,
        strokeColor: NSColor(red: 0.75, green: 0.15, blue: 0.05, alpha: 1.0).cgColor,
        strokeWidth: 14,
        outerStrokeColor: NSColor.white.cgColor,
        outerStrokeWidth: 28
    )
    
    // Subtitle
    drawOutlinedText(
        context: ctx,
        text: "【公式】夢をカタチにする切り抜きShorts 🔥",
        point: CGPoint(x: 540, y: 645),
        fontName: "HiraginoSans-W8",
        fontSize: 34,
        fillColor: NSColor.white.cgColor,
        strokeColor: NSColor.black.cgColor,
        strokeWidth: 6,
        outerStrokeColor: NSColor(red: 0.1, green: 0.2, blue: 0.45, alpha: 1.0).cgColor,
        outerStrokeWidth: 12
    )
    
    // Concept line
    drawOutlinedText(
        context: ctx,
        text: "100億企業を創ったリアル思考 ✕ 心身と経済の豊かさを仲間と共に",
        point: CGPoint(x: 540, y: 585),
        fontName: "HiraginoSans-W7",
        fontSize: 24,
        fillColor: NSColor(red: 1.0, green: 0.95, blue: 0.8, alpha: 1.0).cgColor,
        strokeColor: NSColor.black.cgColor,
        strokeWidth: 4
    )
    
    // Pill: チャンネル登録コール
    let pillRect = CGRect(x: 540, y: 520, width: 440, height: 42)
    ctx.setFillColor(NSColor(red: 0.95, green: 0.3, blue: 0.05, alpha: 0.9).cgColor)
    let pillPath = CGPath(roundedRect: pillRect, cornerWidth: 21, cornerHeight: 21, transform: nil)
    ctx.addPath(pillPath)
    ctx.fillPath()
    
    drawOutlinedText(
        context: ctx,
        text: "🔔 毎日Shorts配信中！チャンネル登録してね♡",
        point: CGPoint(x: 560, y: 532),
        fontName: "HiraginoSans-W8",
        fontSize: 18,
        fillColor: NSColor.white.cgColor,
        strokeColor: NSColor.black.cgColor,
        strokeWidth: 2
    )
    
    if let outImage = ctx.makeImage() {
        saveCGImageAsPNG(outImage, to: "assets/youtube/youtube_banner_anime.png")
        saveCGImageAsJPEG(outImage, to: "assets/youtube/youtube_banner_anime.jpg", quality: 0.92)
    }
}

// =================================================================
// 2. YouTube Banner Photo Pop-Art (2560 x 1440) - Clean Sunburst Background!
// =================================================================
print("--- Generating YouTube Banner (Photo Pop-Art with Dedicated Sunburst) ---")
if let ctx = createCGContext(width: 2560, height: 1440),
   let kaichoPhoto = loadCGImage(from: "assets/youtube/kaicho_photo_cutout.png") {
    
    // Royal Navy background
    let colorSpace = CGColorSpaceCreateDeviceRGB()
    let bgColors = [
        NSColor(red: 0.05, green: 0.09, blue: 0.25, alpha: 1.0).cgColor,
        NSColor(red: 0.08, green: 0.16, blue: 0.42, alpha: 1.0).cgColor,
        NSColor(red: 0.12, green: 0.24, blue: 0.58, alpha: 1.0).cgColor
    ] as CFArray
    if let bgGrad = CGGradient(colorsSpace: colorSpace, colors: bgColors, locations: [0.0, 0.5, 1.0]) {
        ctx.drawLinearGradient(bgGrad, start: CGPoint(x: 0, y: 1440), end: CGPoint(x: 2560, y: 0), options: [])
    }
    
    // Full-bleed vibrant sunburst centered near the center-right (X: 1750, Y: 720)
    let sunburstCenter = CGPoint(x: 1750, y: 720)
    let c1 = NSColor(red: 1.0, green: 0.85, blue: 0.18, alpha: 0.38)
    let c2 = NSColor(red: 1.0, green: 0.95, blue: 0.45, alpha: 0.82)
    drawSunburst(context: ctx, center: sunburstCenter, radius: 2400, rayCount: 36, color1: c1, color2: c2)
    
    // Sparkles across banner
    for _ in 0..<45 {
        let sx = CGFloat.random(in: 400...2500)
        let sy = CGFloat.random(in: 250...1250)
        let starSize = CGFloat.random(in: 12...34)
        drawStar(context: ctx, center: CGPoint(x: sx, y: sy), points: 4, outerRadius: starSize, innerRadius: starSize * 0.3, fillColor: NSColor(red: 1.0, green: 0.96, blue: 0.60, alpha: 0.88).cgColor)
    }
    
    // Smooth soft radial dark glow behind typography (very gentle, perfectly transparent at edges)
    let textGlowColors = [
        NSColor(red: 0.04, green: 0.08, blue: 0.22, alpha: 0.62).cgColor,
        NSColor(red: 0.04, green: 0.08, blue: 0.22, alpha: 0.35).cgColor,
        NSColor(red: 0.04, green: 0.08, blue: 0.22, alpha: 0.0).cgColor
    ] as CFArray
    if let textGlow = CGGradient(colorsSpace: colorSpace, colors: textGlowColors, locations: [0.0, 0.60, 1.0]) {
        ctx.saveGState()
        ctx.translateBy(x: 1140, y: 700)
        ctx.scaleBy(x: 1.7, y: 1.0)
        ctx.drawRadialGradient(textGlow, startCenter: .zero, startRadius: 0, endCenter: .zero, endRadius: 420, options: [])
        ctx.restoreGState()
    }
    
    // Draw Kaicho photo - perfectly within Safe Area right side (X: 1520 .. 2037)
    let photoH: CGFloat = 740
    let photoW: CGFloat = photoH * (CGFloat(kaichoPhoto.width) / CGFloat(kaichoPhoto.height))
    let photoRect = CGRect(x: 1520, y: 350, width: photoW, height: photoH)
    
    ctx.saveGState()
    ctx.setShadow(offset: CGSize(width: 0, height: -10), blur: 30, color: NSColor(white: 0, alpha: 0.55).cgColor)
    ctx.draw(kaichoPhoto, in: photoRect)
    ctx.restoreGState()
    
    ctx.saveGState()
    ctx.setShadow(offset: .zero, blur: 24, color: NSColor.white.cgColor)
    ctx.draw(kaichoPhoto, in: photoRect)
    ctx.restoreGState()
    
    ctx.draw(kaichoPhoto, in: photoRect)
    
    // Typography shifted right to X: 720
    let textStartX: CGFloat = 720
    
    // Badge: ★ ぶった斬り会長公認 ★
    let badgeRect = CGRect(x: textStartX, y: 840, width: 350, height: 44)
    ctx.setFillColor(NSColor(red: 0.88, green: 0.12, blue: 0.28, alpha: 0.95).cgColor)
    let badgePath = CGPath(roundedRect: badgeRect, cornerWidth: 22, cornerHeight: 22, transform: nil)
    ctx.addPath(badgePath)
    ctx.fillPath()
    
    ctx.setStrokeColor(NSColor(red: 1.0, green: 0.85, blue: 0.2, alpha: 1.0).cgColor)
    ctx.setLineWidth(3.0)
    ctx.addPath(badgePath)
    ctx.strokePath()
    
    drawOutlinedText(
        context: ctx,
        text: "★ ぶった斬り会長公認 ★",
        point: CGPoint(x: textStartX + 32, y: 851),
        fontName: "HiraginoSans-W8",
        fontSize: 22,
        fillColor: NSColor.white.cgColor,
        strokeColor: NSColor.black.cgColor,
        strokeWidth: 2
    )
    
    // Main Title: ぶった斬り会長
    drawOutlinedText(
        context: ctx,
        text: "ぶった斬り会長",
        point: CGPoint(x: textStartX - 5, y: 720),
        fontName: "HiraginoSans-W9",
        fontSize: 105,
        fillColor: NSColor(red: 1.0, green: 0.92, blue: 0.25, alpha: 1.0).cgColor,
        strokeColor: NSColor(red: 0.75, green: 0.15, blue: 0.05, alpha: 1.0).cgColor,
        strokeWidth: 14,
        outerStrokeColor: NSColor.white.cgColor,
        outerStrokeWidth: 28
    )
    
    // Subtitle
    drawOutlinedText(
        context: ctx,
        text: "【公認】夢をカタチにする切り抜きShorts 🔥",
        point: CGPoint(x: textStartX, y: 650),
        fontName: "HiraginoSans-W8",
        fontSize: 34,
        fillColor: NSColor.white.cgColor,
        strokeColor: NSColor.black.cgColor,
        strokeWidth: 6,
        outerStrokeColor: NSColor(red: 0.1, green: 0.2, blue: 0.45, alpha: 1.0).cgColor,
        outerStrokeWidth: 12
    )
    
    // Catchphrase
    drawOutlinedText(
        context: ctx,
        text: "100億企業を創ったリアル思考 ✕ 心身と経済の豊かさを仲間と共に",
        point: CGPoint(x: textStartX, y: 590),
        fontName: "HiraginoSans-W7",
        fontSize: 24,
        fillColor: NSColor(red: 1.0, green: 0.95, blue: 0.8, alpha: 1.0).cgColor,
        strokeColor: NSColor.black.cgColor,
        strokeWidth: 4
    )
    
    // Pill: 🔔 Short動画配信！チャンネル登録してね♡
    let pillRect = CGRect(x: textStartX, y: 525, width: 440, height: 42)
    ctx.setFillColor(NSColor(red: 0.95, green: 0.3, blue: 0.05, alpha: 0.9).cgColor)
    let pillPath = CGPath(roundedRect: pillRect, cornerWidth: 21, cornerHeight: 21, transform: nil)
    ctx.addPath(pillPath)
    ctx.fillPath()
    
    drawOutlinedText(
        context: ctx,
        text: "🔔 Short動画配信中！チャンネル登録してね♡",
        point: CGPoint(x: textStartX + 20, y: 537),
        fontName: "HiraginoSans-W8",
        fontSize: 18,
        fillColor: NSColor.white.cgColor,
        strokeColor: NSColor.black.cgColor,
        strokeWidth: 2
    )
    
    if let outImage = ctx.makeImage() {
        saveCGImageAsPNG(outImage, to: "assets/youtube/youtube_banner_photo_illust.png")
        saveCGImageAsJPEG(outImage, to: "assets/youtube/youtube_banner_photo_illust.jpg", quality: 0.92)
    }
}

// =================================================================
// 3. YouTube Icon Anime Illustration (800 x 800) - Clean & Perfect!
// =================================================================
print("--- Generating YouTube Icon (Anime Illustration) ---")
if let ctx = createCGContext(width: 800, height: 800),
   let iconRaw = loadCGImage(from: "assets/youtube/ai_icon_male_raw.jpg") {
    
    // Pure clean avatar without intrusive guide lines
    ctx.draw(iconRaw, in: CGRect(x: 0, y: 0, width: 800, height: 800))
    
    if let outImage = ctx.makeImage() {
        saveCGImageAsPNG(outImage, to: "assets/youtube/youtube_icon_anime.png")
        saveCGImageAsJPEG(outImage, to: "assets/youtube/youtube_icon_anime.jpg", quality: 0.92)
    }
}

// =================================================================
// 4. YouTube Icon Photo Cutout Pop-Art (800 x 800) - Clean Sunburst Background!
// =================================================================
print("--- Generating YouTube Icon (Photo Pop-Art) ---")
if let ctx = createCGContext(width: 800, height: 800),
   let kaichoPhoto = loadCGImage(from: "assets/youtube/kaicho_photo_cutout.png") {
    
    // Background Sunburst
    let c1 = NSColor(red: 1.0, green: 0.80, blue: 0.15, alpha: 1.0)
    let c2 = NSColor(red: 1.0, green: 0.94, blue: 0.40, alpha: 1.0)
    drawSunburst(context: ctx, center: CGPoint(x: 400, y: 400), radius: 600, rayCount: 24, color1: c1, color2: c2)
    
    // Sparkles
    for _ in 0..<12 {
        let sx = CGFloat.random(in: 60...740)
        let sy = CGFloat.random(in: 60...740)
        drawStar(context: ctx, center: CGPoint(x: sx, y: sy), points: 4, outerRadius: 20, innerRadius: 6, fillColor: NSColor.white.cgColor, strokeColor: NSColor(red: 0.9, green: 0.6, blue: 0.1, alpha: 1.0).cgColor, strokeWidth: 1.5)
    }
    
    // Draw Kaicho photo cutout centered and prominent
    // Aspect ratio 608 x 870
    let photoH: CGFloat = 660
    let photoW: CGFloat = photoH * (CGFloat(kaichoPhoto.width) / CGFloat(kaichoPhoto.height))
    let photoRect = CGRect(x: (800 - photoW) / 2.0, y: 80, width: photoW, height: photoH)
    
    // White sticker outline & drop shadow
    ctx.saveGState()
    ctx.setShadow(offset: CGSize(width: 0, height: -6), blur: 18, color: NSColor(white: 0, alpha: 0.4).cgColor)
    ctx.draw(kaichoPhoto, in: photoRect)
    ctx.restoreGState()
    
    ctx.saveGState()
    ctx.setShadow(offset: .zero, blur: 14, color: NSColor.white.cgColor)
    ctx.draw(kaichoPhoto, in: photoRect)
    ctx.restoreGState()
    
    ctx.draw(kaichoPhoto, in: photoRect)
    
    // Bottom badge: ぶった斬り会長
    let badgeRect = CGRect(x: 160, y: 35, width: 480, height: 75)
    ctx.saveGState()
    ctx.setShadow(offset: CGSize(width: 0, height: -4), blur: 12, color: NSColor(white: 0, alpha: 0.4).cgColor)
    ctx.setFillColor(NSColor(red: 0.88, green: 0.12, blue: 0.25, alpha: 0.98).cgColor)
    let badgePath = CGPath(roundedRect: badgeRect, cornerWidth: 37.5, cornerHeight: 37.5, transform: nil)
    ctx.addPath(badgePath)
    ctx.fillPath()
    ctx.restoreGState()
    
    ctx.setStrokeColor(NSColor(red: 1.0, green: 0.88, blue: 0.2, alpha: 1.0).cgColor)
    ctx.setLineWidth(4.0)
    ctx.addPath(badgePath)
    ctx.strokePath()
    
    drawOutlinedText(
        context: ctx,
        text: "ぶった斬り会長",
        point: CGPoint(x: 235, y: 53),
        fontName: "HiraginoSans-W9",
        fontSize: 44,
        fillColor: NSColor.white.cgColor,
        strokeColor: NSColor.black.cgColor,
        strokeWidth: 4
    )
    
    if let outImage = ctx.makeImage() {
        saveCGImageAsPNG(outImage, to: "assets/youtube/youtube_icon_photo_illust.png")
        saveCGImageAsJPEG(outImage, to: "assets/youtube/youtube_icon_photo_illust.jpg", quality: 0.92)
    }
}

// =================================================================
// 5. Shorts Horizontal Banner Stamp (1080 x 220) - Perfectly Spaced!
// =================================================================
print("--- Generating Shorts Banner Stamp (1080 x 220) ---")
if let ctx = createCGContext(width: 1080, height: 220),
   let iconRaw = loadCGImage(from: "assets/youtube/ai_icon_male_raw.jpg") {
    
    let barRect = CGRect(x: 20, y: 20, width: 1040, height: 180)
    ctx.saveGState()
    ctx.setShadow(offset: CGSize(width: 0, height: -4), blur: 16, color: NSColor(white: 0, alpha: 0.35).cgColor)
    ctx.setFillColor(NSColor(red: 0.08, green: 0.12, blue: 0.24, alpha: 0.94).cgColor)
    let barPath = CGPath(roundedRect: barRect, cornerWidth: 90, cornerHeight: 90, transform: nil)
    ctx.addPath(barPath)
    ctx.fillPath()
    ctx.restoreGState()
    
    // Gold border
    ctx.setStrokeColor(NSColor(red: 1.0, green: 0.85, blue: 0.2, alpha: 1.0).cgColor)
    ctx.setLineWidth(4.0)
    ctx.addPath(barPath)
    ctx.strokePath()
    
    // Circular Kaicho icon on the left
    let iconRect = CGRect(x: 35, y: 30, width: 160, height: 160)
    ctx.saveGState()
    ctx.addEllipse(in: iconRect)
    ctx.clip()
    ctx.draw(iconRaw, in: iconRect)
    ctx.restoreGState()
    
    ctx.setStrokeColor(NSColor.white.cgColor)
    ctx.setLineWidth(4.0)
    ctx.strokeEllipse(in: iconRect)
    
    // Main text
    drawOutlinedText(
        context: ctx,
        text: "ぶった斬り会長",
        point: CGPoint(x: 225, y: 110),
        fontName: "HiraginoSans-W9",
        fontSize: 54,
        fillColor: NSColor(red: 1.0, green: 0.92, blue: 0.25, alpha: 1.0).cgColor,
        strokeColor: NSColor.black.cgColor,
        strokeWidth: 6,
        outerStrokeColor: NSColor.white.cgColor,
        outerStrokeWidth: 12
    )
    
    // Sub text - perfectly fits before the subscribe button!
    drawOutlinedText(
        context: ctx,
        text: "【NEO FAMILY】チャンネル登録＆高評価してね❤️",
        point: CGPoint(x: 228, y: 58),
        fontName: "HiraginoSans-W8",
        fontSize: 24,
        fillColor: NSColor.white.cgColor,
        strokeColor: NSColor.black.cgColor,
        strokeWidth: 4
    )
    
    // Subscribe button pill on right
    let btnRect = CGRect(x: 880, y: 65, width: 150, height: 90)
    ctx.setFillColor(NSColor(red: 0.88, green: 0.12, blue: 0.25, alpha: 1.0).cgColor)
    let btnPath = CGPath(roundedRect: btnRect, cornerWidth: 45, cornerHeight: 45, transform: nil)
    ctx.addPath(btnPath)
    ctx.fillPath()
    
    drawOutlinedText(
        context: ctx,
        text: "登録",
        point: CGPoint(x: 915, y: 92),
        fontName: "HiraginoSans-W9",
        fontSize: 38,
        fillColor: NSColor.white.cgColor,
        strokeColor: NSColor.black.cgColor,
        strokeWidth: 2
    )
    
    if let outImage = ctx.makeImage() {
        saveCGImageAsPNG(outImage, to: "assets/youtube/youtube_shorts_banner_stamp.png")
    }
}

print("=== ALL ASSETS REGENERATED WITH PERFECTION ===")
