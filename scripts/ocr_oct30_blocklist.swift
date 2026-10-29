import Foundation
import Vision
import AppKit

struct RecognizedLine: Codable {
    let text: String
    let y: Double
    let x: Double
    let height: Double
    let width: Double
}

struct ImageResult: Codable {
    let file: String
    let lines: [RecognizedLine]
}

let fm = FileManager.default
let dir = "prvided data/BlockList"

let newFiles = [
    "Screenshot 2026-10-30 at 8.02.48.png",
    "Screenshot 2026-10-30 at 8.02.53.png",
    "Screenshot 2026-10-30 at 8.02.59.png",
    "Screenshot 2026-10-30 at 8.03.03.png",
    "Screenshot 2026-10-30 at 8.03.09.png",
    "Screenshot 2026-10-30 at 8.03.14.png",
    "Screenshot 2026-10-30 at 8.03.21.png",
    "Screenshot 2026-10-30 at 8.03.48.png",
    "Screenshot 2026-10-30 at 8.03.53.png",
    "Screenshot 2026-10-30 at 8.04.10.png"
]

var results: [ImageResult] = []

print("Starting OCR for \(newFiles.count) images...")

for (idx, file) in newFiles.enumerated() {
    let path = "\(dir)/\(file)"
    guard let image = NSImage(contentsOfFile: path),
          let tiffData = image.tiffRepresentation,
          let ciImage = CIImage(data: tiffData) else {
        print("Failed to load \(file)")
        continue
    }
    
    var lines: [RecognizedLine] = []
    let request = VNRecognizeTextRequest { request, error in
        guard let observations = request.results as? [VNRecognizedTextObservation] else { return }
        for obs in observations {
            if let topCandidate = obs.topCandidates(1).first {
                let box = obs.boundingBox
                lines.append(RecognizedLine(
                    text: topCandidate.string,
                    y: 1.0 - (box.origin.y + box.height),
                    x: box.origin.x,
                    height: box.height,
                    width: box.width
                ))
            }
        }
    }
    request.recognitionLanguages = ["ja-JP", "en-US"]
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = true
    
    let handler = VNImageRequestHandler(ciImage: ciImage, options: [:])
    try? handler.perform([request])
    
    // Sort lines primarily top to bottom
    lines.sort { abs($0.y - $1.y) < 0.008 ? $0.x < $1.x : $0.y < $1.y }
    
    results.append(ImageResult(file: file, lines: lines))
    print("Done [\(idx+1)/\(newFiles.count)]: \(file) (\(lines.count) lines)")
}

let encoder = JSONEncoder()
encoder.outputFormatting = .prettyPrinted
if let data = try? encoder.encode(results) {
    let outUrl = URL(fileURLWithPath: "scripts/ocr_oct30_blocklist_results.json")
    try? data.write(to: outUrl)
    print("Saved results to scripts/ocr_oct30_blocklist_results.json")
}
