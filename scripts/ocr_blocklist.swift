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
guard let allFiles = try? fm.contentsOfDirectory(atPath: dir) else {
    print("Cannot read dir")
    exit(1)
}

let files = allFiles.filter { $0.hasSuffix(".png") }.sorted()
var results: [ImageResult] = []

print("Starting OCR for \(files.count) images...")

for (idx, file) in files.enumerated() {
    let path = "\(dir)/\(file)"
    guard let image = NSImage(contentsOfFile: path),
          let tiffData = image.tiffRepresentation,
          let ciImage = CIImage(data: tiffData) else {
        continue
    }
    
    var lines: [RecognizedLine] = []
    let request = VNRecognizeTextRequest { request, error in
        guard let observations = request.results as? [VNRecognizedTextObservation] else { return }
        for obs in observations {
            if let topCandidate = obs.topCandidates(1).first {
                let box = obs.boundingBox
                // Vision origin is bottom-left, so 1.0 - box.origin.y makes top=0
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
    
    // Sort lines by Y (top to bottom), then X (left to right)
    lines.sort { 
        if abs($0.y - $1.y) < 0.015 {
            return $0.x < $1.x
        }
        return $0.y < $1.y
    }
    
    results.append(ImageResult(file: file, lines: lines))
    if (idx + 1) % 20 == 0 || idx == files.count - 1 {
        print("Processed \(idx + 1)/\(files.count) images")
    }
}

let encoder = JSONEncoder()
encoder.outputFormatting = .prettyPrinted
if let data = try? encoder.encode(results) {
    try? data.write(to: URL(fileURLWithPath: "scripts/ocr_results.json"))
    print("Saved OCR results to scripts/ocr_results.json")
}
