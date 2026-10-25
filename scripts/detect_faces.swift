import Foundation
import Vision
import AppKit

let dir = "images/caravan"
let files = [
    "S__14254161.jpg",
    "S__14254162.jpg",
    "S__14254163.jpg",
    "S__14254164.jpg",
    "S__14254165.jpg",
    "S__14254166.jpg"
]

for file in files {
    let path = "\(dir)/\(file)"
    guard let image = NSImage(contentsOfFile: path),
          let tiffData = image.tiffRepresentation,
          let ciImage = CIImage(data: tiffData) else {
        continue
    }
    
    let size = image.size
    let request = VNDetectFaceRectanglesRequest { req, err in
        guard let observations = req.results as? [VNFaceObservation] else { return }
        print("File \(file): detected \(observations.count) faces (image size: \(Int(size.width))x\(Int(size.height)))")
        for (i, obs) in observations.enumerated() {
            let box = obs.boundingBox
            let x = box.origin.x * size.width
            let y = (1.0 - box.origin.y - box.height) * size.height
            let w = box.width * size.width
            let h = box.height * size.height
            print("  Face \(i): x=\(Int(x)), y=\(Int(y)), w=\(Int(w)), h=\(Int(h))")
        }
    }
    
    let handler = VNImageRequestHandler(ciImage: ciImage, options: [:])
    try? handler.perform([request])
}
