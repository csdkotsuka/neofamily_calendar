import Foundation
import AppKit
import CoreGraphics
import CoreImage

// ========================================================
// YouTube Branding Asset Generator for ぶった斬り会長 / NEO FAMILY
// ========================================================

let outDir = "assets/youtube"
try? FileManager.default.createDirectory(atPath: outDir, withIntermediateDirectories: true, attributes: nil)

func savePNG(image: NSImage, to path: String) {
    guard let tiff = image.tiffRepresentation,
          let bitmap = NSBitmapImageRep(data: tiff),
          let pngData = bitmap.representation(using: .png, properties: [:]) else {
        print("Failed to convert image to PNG: \(path)")
        return
    }
    do {
        try pngData.write(to: URL(fileURLWithPath: path))
        print("✅ Saved: \(path) (\(Int(image.size.width))x\(Int(image.size.height)))")
    } catch {
        print("Error saving \(path): \(error)")
    }
}

// --------------------------------------------------------
// 1. イラスト風フィルター（実写写真をポップ・イラスト調に変換）
// --------------------------------------------------------
func makeIllustFromPhoto(path: String) -> NSImage? {
    guard let ciInput = CIImage(contentsOf: URL(fileURLWithPath: path)) else { return nil }
    
    // 1. コントラスト & 彩度アップ（ビビッド＆明るく）
    let colorFilter = CIFilter(name: "CIColorControls")!
    colorFilter.setValue(ciInput, forKey: kCIInputImageKey)
    colorFilter.setValue(1.4, forKey: kCIInputSaturationKey)
    colorFilter.setValue(1.15, forKey: kCIInputContrastKey)
    colorFilter.setValue(0.06, forKey: kCIInputBrightnessKey)
    let vibrant = colorFilter.outputImage!
    
    // 2. コミック調フィルター
    let comicFilter = CIFilter(name: "CIComicEffect")!
    comicFilter.setValue(vibrant, forKey: kCIInputImageKey)
    let comic = comicFilter.outputImage!
    
    // 3. ソフトライトでブレンド（線の強さと温かみのある肌色を両立）
    let blendFilter = CIFilter(name: "CISoftLightBlendMode")!
    blendFilter.setValue(comic, forKey: kCIInputImageKey)
    blendFilter.setValue(vibrant, forKey: kCIInputBackgroundImageKey)
    guard let output = blendFilter.outputImage else { return nil }
    
    let rep = NSCIImageRep(ciImage: output)
    let nsImage = NSImage(size: rep.size)
    nsImage.addRepresentation(rep)
    return nsImage
}

// --------------------------------------------------------
// 2. チャンネルアイコン A: 実写チラシ加工イラスト版 (800x800)
// --------------------------------------------------------
func generateIconPhotoIllust() {
    let size = NSSize(width: 800, height: 800)
    let image = NSImage(size: size)
    image.lockFocus()
    guard let ctx = NSGraphicsContext.current?.cgContext else { image.unlockFocus(); return }
    
    // 背景: ポップなグラデーション（ピンク〜オレンジ〜イエロー）
    let colorSpace = CGColorSpaceCreateDeviceRGB()
    let bgColors = [
        NSColor(red: 0.98, green: 0.25, blue: 0.50, alpha: 1.0).cgColor, // Rose Pink
        NSColor(red: 1.00, green: 0.55, blue: 0.35, alpha: 1.0).cgColor, // Coral Orange
        NSColor(red: 1.00, green: 0.85, blue: 0.40, alpha: 1.0).cgColor  // Warm Gold
    ] as CFArray
    let bgGradient = CGGradient(colorsSpace: colorSpace, colors: bgColors, locations: [0.0, 0.6, 1.0])!
    ctx.drawLinearGradient(bgGradient, start: CGPoint(x: 0, y: 800), end: CGPoint(x: 800, y: 0), options: [])
    
    // ポップなキラキラ・星の背景装飾
    ctx.saveGState()
    for (cx, cy, r, alpha) in [(120.0, 680.0, 45.0, 0.25), (680.0, 700.0, 35.0, 0.2), (100.0, 200.0, 30.0, 0.2), (720.0, 250.0, 50.0, 0.25), (400.0, 740.0, 25.0, 0.15)] {
        ctx.setFillColor(NSColor.white.withAlphaComponent(CGFloat(alpha)).cgColor)
        ctx.fillEllipse(in: CGRect(x: cx - r, y: cy - r, width: r * 2, height: r * 2))
    }
    ctx.restoreGState()
    
    // 円形の白いマージン枠（ステッカー風）
    let circleRect = CGRect(x: 40, y: 70, width: 720, height: 720)
    ctx.saveGState()
    ctx.setShadow(offset: CGSize(width: 0, height: -10), blur: 25, color: NSColor.black.withAlphaComponent(0.3).cgColor)
    ctx.setFillColor(NSColor.white.cgColor)
    ctx.fillEllipse(in: circleRect)
    ctx.restoreGState()
    
    // 内側の円にクリップして会長イラスト写真を配置
    ctx.saveGState()
    let innerCircle = circleRect.insetBy(dx: 14, dy: 14)
    ctx.addEllipse(in: innerCircle)
    ctx.clip()
    
    // 会長イラスト写真をロードして描画
    if let illust = makeIllustFromPhoto(path: "images/kaicho_face.jpg") {
        illust.draw(in: CGRect(x: 54, y: 84, width: 692, height: 692), from: .zero, operation: .sourceOver, fraction: 1.0)
    }
    ctx.restoreGState()
    
    // 下部バッジ: 「ぶった斬り会長」ポップラベル
    ctx.saveGState()
    let badgeRect = CGRect(x: 150, y: 35, width: 500, height: 95)
    ctx.setShadow(offset: CGSize(width: 0, height: -6), blur: 15, color: NSColor.black.withAlphaComponent(0.35).cgColor)
    ctx.setFillColor(NSColor(red: 0.08, green: 0.10, blue: 0.15, alpha: 0.95).cgColor)
    let badgePath = NSBezierPath(roundedRect: badgeRect, xRadius: 47.5, yRadius: 47.5)
    badgePath.fill()
    
    ctx.setStrokeColor(NSColor(red: 1.00, green: 0.85, blue: 0.30, alpha: 1.0).cgColor)
    badgePath.lineWidth = 4
    badgePath.stroke()
    ctx.restoreGState()
    
    // テキスト: ぶった斬り会長
    let font = NSFont.systemFont(ofSize: 46, weight: .black)
    let attrs: [NSAttributedString.Key: Any] = [
        .font: font,
        .foregroundColor: NSColor.white
    ]
    let titleStr = "ぶった斬り会長"
    let titleSize = titleStr.size(withAttributes: attrs)
    let textPoint = CGPoint(x: 150 + (500 - titleSize.width) / 2, y: 35 + (95 - titleSize.height) / 2 + 2)
    titleStr.draw(at: textPoint, withAttributes: attrs)
    
    image.unlockFocus()
    savePNG(image: image, to: "\(outDir)/youtube_icon_photo_illust.png")
}

// --------------------------------------------------------
// 3. チャンネルアイコン B: アニメ調イラスト版 (800x800)
// --------------------------------------------------------
func generateIconAnime() {
    let size = NSSize(width: 800, height: 800)
    let image = NSImage(size: size)
    image.lockFocus()
    guard let ctx = NSGraphicsContext.current?.cgContext else { image.unlockFocus(); return }
    
    // AI生成アイコン画像をベースに丸抜き・ステッカー加工
    let rawPath = "\(outDir)/ai_icon_raw.jpg"
    if let rawImg = NSImage(contentsOfFile: rawPath) {
        // 背景グラデーション
        let colorSpace = CGColorSpaceCreateDeviceRGB()
        let bgColors = [
            NSColor(red: 0.98, green: 0.22, blue: 0.45, alpha: 1.0).cgColor,
            NSColor(red: 0.99, green: 0.65, blue: 0.35, alpha: 1.0).cgColor
        ] as CFArray
        let bgGradient = CGGradient(colorsSpace: colorSpace, colors: bgColors, locations: [0.0, 1.0])!
        ctx.drawLinearGradient(bgGradient, start: CGPoint(x: 0, y: 800), end: CGPoint(x: 800, y: 0), options: [])
        
        // 白ステッカー枠
        let circleRect = CGRect(x: 35, y: 65, width: 730, height: 730)
        ctx.saveGState()
        ctx.setShadow(offset: CGSize(width: 0, height: -12), blur: 30, color: NSColor.black.withAlphaComponent(0.35).cgColor)
        ctx.setFillColor(NSColor.white.cgColor)
        ctx.fillEllipse(in: circleRect)
        ctx.restoreGState()
        
        // 内側クリップ
        ctx.saveGState()
        let innerCircle = circleRect.insetBy(dx: 12, dy: 12)
        ctx.addEllipse(in: innerCircle)
        ctx.clip()
        
        rawImg.draw(in: CGRect(x: 47, y: 77, width: 706, height: 706), from: .zero, operation: .sourceOver, fraction: 1.0)
        ctx.restoreGState()
        
        // 下部ピルバッジ
        ctx.saveGState()
        let badgeRect = CGRect(x: 140, y: 35, width: 520, height: 95)
        ctx.setShadow(offset: CGSize(width: 0, height: -6), blur: 15, color: NSColor.black.withAlphaComponent(0.35).cgColor)
        ctx.setFillColor(NSColor(red: 0.08, green: 0.10, blue: 0.16, alpha: 0.95).cgColor)
        let badgePath = NSBezierPath(roundedRect: badgeRect, xRadius: 47.5, yRadius: 47.5)
        badgePath.fill()
        
        ctx.setStrokeColor(NSColor(red: 1.00, green: 0.82, blue: 0.25, alpha: 1.0).cgColor)
        badgePath.lineWidth = 4
        badgePath.stroke()
        ctx.restoreGState()
        
        let font = NSFont.systemFont(ofSize: 45, weight: .black)
        let attrs: [NSAttributedString.Key: Any] = [
            .font: font,
            .foregroundColor: NSColor.white
        ]
        let titleStr = "ぶった斬り会長"
        let titleSize = titleStr.size(withAttributes: attrs)
        let textPoint = CGPoint(x: 140 + (520 - titleSize.width) / 2, y: 35 + (95 - titleSize.height) / 2 + 2)
        titleStr.draw(at: textPoint, withAttributes: attrs)
    }
    
    image.unlockFocus()
    savePNG(image: image, to: "\(outDir)/youtube_icon_anime.png")
}

// --------------------------------------------------------
// 4. チャンネルバナー (2560 x 1440) - セーフエリア完全準拠
// --------------------------------------------------------
func generateBanner(isAnime: Bool) {
    let size = NSSize(width: 2560, height: 1440)
    let image = NSImage(size: size)
    image.lockFocus()
    guard let ctx = NSGraphicsContext.current?.cgContext else { image.unlockFocus(); return }
    
    // 全体背景: エネルギッシュ＆キュートなグラデーション（ダークローズ〜パープル〜ウォームコーラル）
    let colorSpace = CGColorSpaceCreateDeviceRGB()
    let bgColors = [
        NSColor(red: 0.12, green: 0.08, blue: 0.20, alpha: 1.0).cgColor, // Deep Purple-Navy
        NSColor(red: 0.75, green: 0.12, blue: 0.35, alpha: 1.0).cgColor, // Vivid Rose Red
        NSColor(red: 0.98, green: 0.45, blue: 0.25, alpha: 1.0).cgColor, // Coral Peach
        NSColor(red: 1.00, green: 0.80, blue: 0.35, alpha: 1.0).cgColor  // Golden Sun
    ] as CFArray
    let bgGradient = CGGradient(colorsSpace: colorSpace, colors: bgColors, locations: [0.0, 0.45, 0.80, 1.0])!
    ctx.drawLinearGradient(bgGradient, start: CGPoint(x: 0, y: 1440), end: CGPoint(x: 2560, y: 0), options: [])
    
    // 背景パターン: ポップなドット・スター・ライトサークル
    ctx.saveGState()
    for i in 0..<120 {
        let rx = CGFloat((i * 137) % 2560)
        let ry = CGFloat((i * 97) % 1440)
        let r = CGFloat(4 + (i % 12))
        let alpha = CGFloat(0.08 + Double(i % 10) * 0.02)
        ctx.setFillColor(NSColor.white.withAlphaComponent(alpha).cgColor)
        ctx.fillEllipse(in: CGRect(x: rx, y: ry, width: r * 2, height: r * 2))
    }
    ctx.restoreGState()
    
    // セーフゾーン（YouTube推奨安全領域）: 中央 1546 x 423
    // X: 507 〜 2053, Y: 508 〜 931
    let safeX: CGFloat = 507
    let safeY: CGFloat = 508.5
    let safeW: CGFloat = 1546
    let safeH: CGFloat = 423
    
    // セーフエリア背景のハイライトプレート（半透明のガラス風ダークパネル）
    ctx.saveGState()
    let plateRect = CGRect(x: safeX - 20, y: safeY - 10, width: safeW + 40, height: safeH + 20)
    ctx.setFillColor(NSColor(red: 0.05, green: 0.06, blue: 0.12, alpha: 0.55).cgColor)
    let platePath = NSBezierPath(roundedRect: plateRect, xRadius: 36, yRadius: 36)
    platePath.fill()
    ctx.setStrokeColor(NSColor.white.withAlphaComponent(0.20).cgColor)
    platePath.lineWidth = 2
    platePath.stroke()
    ctx.restoreGState()
    
    // --- 右側: 会長イラスト / キャラクタービジュアル ---
    if isAnime {
        if let rawKV = NSImage(contentsOfFile: "\(outDir)/ai_banner_kv_raw.jpg") {
            ctx.saveGState()
            // 丸型ステッカー風フレームで配置
            let charRect = CGRect(x: safeX + safeW - 460, y: safeY + 12, width: 420, height: 400)
            ctx.setShadow(offset: CGSize(width: 0, height: 10), blur: 30, color: NSColor.black.withAlphaComponent(0.4).cgColor)
            ctx.setFillColor(NSColor.white.cgColor)
            let borderPath = NSBezierPath(roundedRect: charRect, xRadius: 32, yRadius: 32)
            borderPath.fill()
            
            let innerRect = charRect.insetBy(dx: 8, dy: 8)
            let innerPath = NSBezierPath(roundedRect: innerRect, xRadius: 26, yRadius: 26)
            innerPath.addClip()
            rawKV.draw(in: innerRect, from: .zero, operation: .sourceOver, fraction: 1.0)
            ctx.restoreGState()
        }
    } else {
        if let rawUpper = NSImage(contentsOfFile: "\(outDir)/kaicho_upperbody_raw.jpg") {
            ctx.saveGState()
            let charRect = CGRect(x: safeX + safeW - 440, y: safeY + 10, width: 400, height: 400)
            ctx.setShadow(offset: CGSize(width: 0, height: 10), blur: 30, color: NSColor.black.withAlphaComponent(0.4).cgColor)
            ctx.setFillColor(NSColor.white.cgColor)
            let borderPath = NSBezierPath(roundedRect: charRect, xRadius: 32, yRadius: 32)
            borderPath.fill()
            
            let innerRect = charRect.insetBy(dx: 8, dy: 8)
            let innerPath = NSBezierPath(roundedRect: innerRect, xRadius: 26, yRadius: 26)
            innerPath.addClip()
            
            // コミック風フィルターを適用
            if let illust = makeIllustFromPhoto(path: "\(outDir)/kaicho_upperbody_raw.jpg") {
                illust.draw(in: innerRect, from: .zero, operation: .sourceOver, fraction: 1.0)
            } else {
                rawUpper.draw(in: innerRect, from: .zero, operation: .sourceOver, fraction: 1.0)
            }
            ctx.restoreGState()
        }
    }
    
    // --- 左側: タイトル & キャッチコピー (セーフゾーン内) ---
    let textLeft: CGFloat = safeX + 50
    
    // 1. バッジ: [NEO FAMILY OFFICIAL CHANNEL]
    ctx.saveGState()
    let tagRect = CGRect(x: textLeft, y: safeY + safeH - 85, width: 330, height: 46)
    ctx.setFillColor(NSColor(red: 0.98, green: 0.22, blue: 0.45, alpha: 1.0).cgColor)
    let tagPath = NSBezierPath(roundedRect: tagRect, xRadius: 23, yRadius: 23)
    tagPath.fill()
    ctx.restoreGState()
    
    let tagFont = NSFont.systemFont(ofSize: 20, weight: .heavy)
    let tagAttrs: [NSAttributedString.Key: Any] = [
        .font: tagFont,
        .foregroundColor: NSColor.white
    ]
    "★ NEO FAMILY OFFICIAL ★".draw(at: CGPoint(x: textLeft + 22, y: safeY + safeH - 77), withAttributes: tagAttrs)
    
    // 2. メインタイトル: 「ぶった斬り会長」 (超特大・迫力フォント・ゴールド/ホワイトシャドウ)
    let titleStr = "ぶった斬り会長"
    let titleFont = NSFont.systemFont(ofSize: 104, weight: .black)
    
    // ドロップシャドウ
    ctx.saveGState()
    ctx.setShadow(offset: CGSize(width: 5, height: -8), blur: 18, color: NSColor.black.withAlphaComponent(0.6).cgColor)
    let titleShadowAttrs: [NSAttributedString.Key: Any] = [
        .font: titleFont,
        .foregroundColor: NSColor(red: 1.00, green: 0.88, blue: 0.35, alpha: 1.0) // Gold
    ]
    titleStr.draw(at: CGPoint(x: textLeft, y: safeY + safeH - 215), withAttributes: titleShadowAttrs)
    ctx.restoreGState()
    
    let titleAttrs: [NSAttributedString.Key: Any] = [
        .font: titleFont,
        .foregroundColor: NSColor.white
    ]
    titleStr.draw(at: CGPoint(x: textLeft, y: safeY + safeH - 215), withAttributes: titleAttrs)
    
    // 3. サブタイトル / キャッチコピー: 「夢をカタチに、心身と経済の豊かさを。」
    let subStr = "夢をカタチに、心身と経済の豊かさを。"
    let subFont = NSFont.systemFont(ofSize: 32, weight: .heavy)
    let subAttrs: [NSAttributedString.Key: Any] = [
        .font: subFont,
        .foregroundColor: NSColor(red: 1.00, green: 0.92, blue: 0.65, alpha: 1.0)
    ]
    subStr.draw(at: CGPoint(x: textLeft + 4, y: safeY + safeH - 275), withAttributes: subAttrs)
    
    // 4. Shorts ピルバッジ: 「⚡️ 毎日YouTube Shorts 切り抜き配信中！ 🔥」
    ctx.saveGState()
    let pillRect = CGRect(x: textLeft, y: safeY + 45, width: 620, height: 60)
    ctx.setFillColor(NSColor.white.cgColor)
    let pillPath = NSBezierPath(roundedRect: pillRect, xRadius: 30, yRadius: 30)
    pillPath.fill()
    ctx.setShadow(offset: CGSize(width: 0, height: -4), blur: 12, color: NSColor.black.withAlphaComponent(0.25).cgColor)
    ctx.restoreGState()
    
    let pillFont = NSFont.systemFont(ofSize: 25, weight: .black)
    let pillAttrs: [NSAttributedString.Key: Any] = [
        .font: pillFont,
        .foregroundColor: NSColor(red: 0.88, green: 0.10, blue: 0.30, alpha: 1.0)
    ]
    "🔥 毎日Shorts切り抜き動画を配信中！ 🔥".draw(at: CGPoint(x: textLeft + 35, y: safeY + 58), withAttributes: pillAttrs)
    
    image.unlockFocus()
    let outFileName = isAnime ? "youtube_banner_anime.png" : "youtube_banner_photo_illust.png"
    savePNG(image: image, to: "\(outDir)/\(outFileName)")
}

// --------------------------------------------------------
// 5. 動画の透かし (YouTube Studio 150x150 透過PNG)
// --------------------------------------------------------
func generateWatermarkStandard() {
    let size = NSSize(width: 150, height: 150)
    let image = NSImage(size: size)
    image.lockFocus()
    guard let ctx = NSGraphicsContext.current?.cgContext else { image.unlockFocus(); return }
    
    // 透過背景上に赤角丸正方形
    let rect = CGRect(x: 4, y: 4, width: 142, height: 142)
    ctx.saveGState()
    ctx.setShadow(offset: CGSize(width: 0, height: -3), blur: 8, color: NSColor.black.withAlphaComponent(0.35).cgColor)
    ctx.setFillColor(NSColor(red: 0.95, green: 0.15, blue: 0.25, alpha: 0.96).cgColor)
    let path = NSBezierPath(roundedRect: rect, xRadius: 28, yRadius: 28)
    path.fill()
    
    ctx.setStrokeColor(NSColor.white.cgColor)
    path.lineWidth = 3
    path.stroke()
    ctx.restoreGState()
    
    // YouTube再生アイコン風の白三角
    ctx.saveGState()
    ctx.setFillColor(NSColor.white.cgColor)
    let triPath = CGMutablePath()
    triPath.move(to: CGPoint(x: 64, y: 104))
    triPath.addLine(to: CGPoint(x: 92, y: 88))
    triPath.addLine(to: CGPoint(x: 64, y: 72))
    triPath.closeSubpath()
    ctx.addPath(triPath)
    ctx.fillPath()
    ctx.restoreGState()
    
    // テキスト: 登録 (または チャンネル登録)
    let font = NSFont.systemFont(ofSize: 26, weight: .black)
    let attrs: [NSAttributedString.Key: Any] = [
        .font: font,
        .foregroundColor: NSColor.white
    ]
    let str = "登録"
    let strSize = str.size(withAttributes: attrs)
    str.draw(at: CGPoint(x: (150 - strSize.width) / 2, y: 22), withAttributes: attrs)
    
    image.unlockFocus()
    savePNG(image: image, to: "\(outDir)/youtube_watermark_standard.png")
}

// --------------------------------------------------------
// 6. ショート動画用スタンプ / 透かし (500x500 高解像度 透過PNG)
// --------------------------------------------------------
func generateShortsWatermarkCute() {
    let size = NSSize(width: 500, height: 500)
    let image = NSImage(size: size)
    image.lockFocus()
    guard let ctx = NSGraphicsContext.current?.cgContext else { image.unlockFocus(); return }
    
    // 円形ステッカー風スタンプ（透過PNG）
    let center = CGPoint(x: 250, y: 250)
    let radius: CGFloat = 220
    let circleRect = CGRect(x: center.x - radius, y: center.y - radius, width: radius * 2, height: radius * 2)
    
    // 背景: 半透明（90%）のビビッドピンク〜オレンジグラデーション
    ctx.saveGState()
    ctx.addEllipse(in: circleRect)
    ctx.clip()
    
    let colorSpace = CGColorSpaceCreateDeviceRGB()
    let colors = [
        NSColor(red: 0.98, green: 0.20, blue: 0.45, alpha: 0.92).cgColor,
        NSColor(red: 1.00, green: 0.50, blue: 0.30, alpha: 0.92).cgColor
    ] as CFArray
    let gradient = CGGradient(colorsSpace: colorSpace, colors: colors, locations: [0.0, 1.0])!
    ctx.drawLinearGradient(gradient, start: CGPoint(x: 50, y: 450), end: CGPoint(x: 450, y: 50), options: [])
    ctx.restoreGState()
    
    // 太い白フチ
    ctx.saveGState()
    ctx.setStrokeColor(NSColor.white.cgColor)
    ctx.setLineWidth(14)
    ctx.strokeEllipse(in: circleRect.insetBy(dx: 7, dy: 7))
    ctx.restoreGState()
    
    // 上部文字: NEO FAMILY
    let topFont = NSFont.systemFont(ofSize: 32, weight: .heavy)
    let topAttrs: [NSAttributedString.Key: Any] = [
        .font: topFont,
        .foregroundColor: NSColor(red: 1.00, green: 0.90, blue: 0.40, alpha: 1.0)
    ]
    let topStr = "★ NEO FAMILY ★"
    let topSize = topStr.size(withAttributes: topAttrs)
    topStr.draw(at: CGPoint(x: (500 - topSize.width) / 2, y: 345), withAttributes: topAttrs)
    
    // メイン文字: ぶった斬り会長
    let mainFont = NSFont.systemFont(ofSize: 56, weight: .black)
    let mainAttrs: [NSAttributedString.Key: Any] = [
        .font: mainFont,
        .foregroundColor: NSColor.white
    ]
    let mainStr = "ぶった斬り"
    let mainSize = mainStr.size(withAttributes: mainAttrs)
    mainStr.draw(at: CGPoint(x: (500 - mainSize.width) / 2, y: 250), withAttributes: mainAttrs)
    
    let subStr = "会長"
    let subFont = NSFont.systemFont(ofSize: 68, weight: .black)
    let subAttrs: [NSAttributedString.Key: Any] = [
        .font: subFont,
        .foregroundColor: NSColor(red: 1.00, green: 0.95, blue: 0.30, alpha: 1.0)
    ]
    let subSize = subStr.size(withAttributes: subAttrs)
    subStr.draw(at: CGPoint(x: (500 - subSize.width) / 2, y: 160), withAttributes: subAttrs)
    
    // 下部文字: チャンネル登録♡
    ctx.saveGState()
    let pillRect = CGRect(x: 90, y: 75, width: 320, height: 60)
    ctx.setFillColor(NSColor.white.cgColor)
    let pillPath = NSBezierPath(roundedRect: pillRect, xRadius: 30, yRadius: 30)
    pillPath.fill()
    ctx.restoreGState()
    
    let pillFont = NSFont.systemFont(ofSize: 28, weight: .black)
    let pillAttrs: [NSAttributedString.Key: Any] = [
        .font: pillFont,
        .foregroundColor: NSColor(red: 0.90, green: 0.15, blue: 0.35, alpha: 1.0)
    ]
    let pillStr = "チャンネル登録♡"
    let pillSize = pillStr.size(withAttributes: pillAttrs)
    pillStr.draw(at: CGPoint(x: (500 - pillSize.width) / 2, y: 88), withAttributes: pillAttrs)
    
    image.unlockFocus()
    savePNG(image: image, to: "\(outDir)/youtube_shorts_watermark.png")
}

// --------------------------------------------------------
// 7. ショート動画用 横帯スタンプ (1080 x 220 透過PNG)
// --------------------------------------------------------
func generateShortsBannerStamp() {
    let size = NSSize(width: 1080, height: 220)
    let image = NSImage(size: size)
    image.lockFocus()
    guard let ctx = NSGraphicsContext.current?.cgContext else { image.unlockFocus(); return }
    
    // 半透明のグラデーション帯
    let barRect = CGRect(x: 30, y: 20, width: 1020, height: 180)
    ctx.saveGState()
    ctx.setShadow(offset: CGSize(width: 0, height: -5), blur: 15, color: NSColor.black.withAlphaComponent(0.35).cgColor)
    ctx.setFillColor(NSColor(red: 0.08, green: 0.09, blue: 0.15, alpha: 0.88).cgColor)
    let barPath = NSBezierPath(roundedRect: barRect, xRadius: 36, yRadius: 36)
    barPath.fill()
    
    ctx.setStrokeColor(NSColor(red: 1.00, green: 0.85, blue: 0.35, alpha: 0.9).cgColor)
    barPath.lineWidth = 3
    barPath.stroke()
    ctx.restoreGState()
    
    // 左側: 「ぶった斬り会長」ロゴ
    let logoFont = NSFont.systemFont(ofSize: 52, weight: .black)
    let logoAttrs: [NSAttributedString.Key: Any] = [
        .font: logoFont,
        .foregroundColor: NSColor.white
    ]
    "ぶった斬り会長".draw(at: CGPoint(x: 80, y: 105), withAttributes: logoAttrs)
    
    let subFont = NSFont.systemFont(ofSize: 26, weight: .bold)
    let subAttrs: [NSAttributedString.Key: Any] = [
        .font: subFont,
        .foregroundColor: NSColor(red: 1.00, green: 0.85, blue: 0.35, alpha: 1.0)
    ]
    "NEO FAMILY 公式切り抜き".draw(at: CGPoint(x: 82, y: 55), withAttributes: subAttrs)
    
    // 右側: [チャンネル登録] ポップボタン
    ctx.saveGState()
    let btnRect = CGRect(x: 720, y: 50, width: 290, height: 110)
    ctx.setFillColor(NSColor(red: 0.98, green: 0.20, blue: 0.40, alpha: 1.0).cgColor)
    let btnPath = NSBezierPath(roundedRect: btnRect, xRadius: 30, yRadius: 30)
    btnPath.fill()
    ctx.restoreGState()
    
    let btnFont = NSFont.systemFont(ofSize: 34, weight: .black)
    let btnAttrs: [NSAttributedString.Key: Any] = [
        .font: btnFont,
        .foregroundColor: NSColor.white
    ]
    let btnStr = "登録する♡"
    let btnSize = btnStr.size(withAttributes: btnAttrs)
    btnStr.draw(at: CGPoint(x: 720 + (290 - btnSize.width) / 2, y: 50 + (110 - btnSize.height) / 2 + 2), withAttributes: btnAttrs)
    
    image.unlockFocus()
    savePNG(image: image, to: "\(outDir)/youtube_shorts_banner_stamp.png")
}

// --------------------------------------------------------
// 実行
// --------------------------------------------------------
print("🚀 Generating YouTube Branding Assets...")
generateIconPhotoIllust()
generateIconAnime()
generateBanner(isAnime: false)
generateBanner(isAnime: true)
generateWatermarkStandard()
generateShortsWatermarkCute()
generateShortsBannerStamp()
print("🎉 All assets generated successfully in \(outDir)/")
