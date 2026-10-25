import Foundation
import AppKit

func cropFace(file: String, cx: CGFloat, cy: CGFloat, size: CGFloat, outFile: String) {
    guard let img = NSImage(contentsOfFile: file) else { return }
    guard let rep = img.representations.first as? NSBitmapImageRep else { return }
    
    // Pixel dimensions
    let pw = CGFloat(rep.pixelsWide)
    let ph = CGFloat(rep.pixelsHigh)
    
    // Scale factor from image.size to pixels
    let sx = pw / img.size.width
    let sy = ph / img.size.height
    
    let cropSize = size * sx
    let cropX = max(0, min(pw - cropSize, (cx * sx) - cropSize / 2))
    let cropY = max(0, min(ph - cropSize, (cy * sy) - cropSize / 2))
    
    let cropRect = CGRect(x: cropX, y: cropY, width: cropSize, height: cropSize)
    
    guard let cgImage = rep.cgImage?.cropping(to: cropRect) else { return }
    
    let newRep = NSBitmapImageRep(cgImage: cgImage)
    let pngData = newRep.representation(using: .jpeg, properties: [:])
    try? pngData?.write(to: URL(fileURLWithPath: outFile))
    print("Saved \(outFile) (\(Int(cropSize))x\(Int(cropSize)))")
}

// S__14254162.jpg: Face at x=679, y=301, w=220, h=220. Center is x=789, y=411. Let size be 340 (including hair and neck).
cropFace(file: "images/caravan/S__14254162.jpg", cx: 789, cy: 411, size: 380, outFile: "images/kaicho_face_nagano.jpg")

// S__14254166.jpg: Face at x=745, y=205, w=204, h=204. Center is x=847, y=307. Size 360.
cropFace(file: "images/caravan/S__14254166.jpg", cx: 847, cy: 307, size: 360, outFile: "images/kaicho_face_hamamatsu.jpg")

// S__14254161.jpg: Face at x=225, y=195, w=153, h=153. Center is x=301, y=271. Size 300.
cropFace(file: "images/caravan/S__14254161.jpg", cx: 301, cy: 271, size: 300, outFile: "images/kaicho_face_kamaishi.jpg")
