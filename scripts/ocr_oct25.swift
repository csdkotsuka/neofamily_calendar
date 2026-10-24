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

let dir = "prvided data"
let files = [
    "S__14254161.jpg",
    "S__14254162.jpg",
    "S__14254163.jpg",
    "S__14254164.jpg",
    "S__14254165.jpg",
    "S__14254166.jpg"
]

var results: [ImageResult] = []

for file in files {
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
    try? data.write(to: URL(fileURLWithPath: "scripts/ocr_oct25_results.json"))
    print("Saved OCR results to scripts/ocr_oct25_results.json")
}
