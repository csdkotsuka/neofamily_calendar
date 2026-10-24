import Foundation
import Vision
import AppKit

struct RecognizedLine: Codable {
    let text: String
    let y: Double
    let x: Double
    let height: Double
}

struct ImageResult: Codable {
    let file: String
    let lines: [RecognizedLine]
}

let fm = FileManager.default
let dir = "prvided data/BlockList"

let newFiles = [
    "Screenshot 2026-10-24 at 15.11.48.png",
    "Screenshot 2026-10-24 at 15.11.56.png",
    "Screenshot 2026-10-24 at 15.12.02.png",
    "Screenshot 2026-10-24 at 15.12.08.png",
    "Screenshot 2026-10-24 at 15.12.15.png",
    "Screenshot 2026-10-24 at 15.12.21.png"
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
                    height: box.height
                ))
            }
        }
    }
    request.recognitionLanguages = ["ja-JP", "en-US"]
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = true
    
    let handler = VNImageRequestHandler(ciImage: ciImage, options: [:])
    try? handler.perform([request])
    
    lines.sort { 
        if abs($0.y - $1.y) < 0.012 {
            return $0.x < $1.x
        }
        return $0.y < $1.y
    }
    
    results.append(ImageResult(file: file, lines: lines))
    print("Processed \(file): \(lines.count) lines")
}

let encoder = JSONEncoder()
encoder.outputFormatting = .prettyPrinted
if let data = try? encoder.encode(results) {
    try? data.write(to: URL(fileURLWithPath: "scripts/ocr_oct24_results.json"))
    print("Saved OCR results to scripts/ocr_oct24_results.json")
}
