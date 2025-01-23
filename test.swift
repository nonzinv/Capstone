import Foundation
import NaturalLanguage

class SentimentAnalyzer {
    let keywords = ["windows", "microsoft", "windows 11", "copilot"]
    let negativeLogFile = "negative_sentiments.csv"

    init() {
        createOrInitializeCSV()
    }

    func createOrInitializeCSV() {
        let fileManager = FileManager.default
        if !fileManager.fileExists(atPath: negativeLogFile) {
            let header = "Sentence,Polarity\n"
            do {
                try header.write(toFile: negativeLogFile, atomically: true, encoding: .utf8)
            } catch {
                print("Error initializing CSV file: \(error)")
            }
        }
    }

    func processSentence(_ sentence: String) {
        guard keywords.contains(where: { sentence.lowercased().contains($0.lowercased()) }) else {
            print("Input is irrelevant: \(sentence)")
            return
        }

        let polarity = analyzePolarity(for: sentence)
        print("\nSentiment Analysis Result:")
        print("Sentence: \(sentence)")
        print("Polarity: \(String(format: "%.2f", polarity))")

        if polarity > 0 {
            print("Overall Sentiment: Positive\n")
        } else if polarity < 0 {
            print("Overall Sentiment: Negative\n")
            logNegativeSentiment(sentence: sentence, polarity: polarity)
        } else {
            print("Overall Sentiment: Neutral\n")
        }
    }

    func analyzePolarity(for sentence: String) -> Double {
        let sentimentPredictor = NLTagger(tagSchemes: [.sentimentScore])
        sentimentPredictor.string = sentence
        let (sentiment, _) = sentimentPredictor.tag(at: sentence.startIndex, unit: .paragraph, scheme: .sentimentScore)
        return Double(sentiment?.rawValue ?? "0.0") ?? 0.0
    }

    func logNegativeSentiment(sentence: String, polarity: Double) {
        let entry = "\(sentence),\(String(format: "%.2f", polarity))\n"
        do {
            if let fileHandle = FileHandle(forWritingAtPath: negativeLogFile) {
                fileHandle.seekToEndOfFile()
                if let data = entry.data(using: .utf8) {
                    fileHandle.write(data)
                }
                fileHandle.closeFile()
            }
        } catch {
            print("Error logging negative sentiment: \(error)")
        }
    }

    func processFile(atPath path: String) {
        do {
            let fileContent = try String(contentsOfFile: path, encoding: .utf8)
            let lines = fileContent.split(separator: "\n")
            for line in lines {
                processSentence(String(line))
            }
        } catch {
            print("Error reading file: \(error)")
        }
    }

    func startInteractiveSession() {
        while true {
            print("Enter a sentence (or type 'exit' to quit):", terminator: " ")
            if let userInput = readLine() {
                if userInput.lowercased() == "exit" {
                    print("Quitting")
                    break
                }
                processSentence(userInput)
            }
        }
    }
}

// Main
let analyzer = SentimentAnalyzer()
print("Do you want to upload a file with comments? (yes/no):", terminator: " ")
if let fileInput = readLine()?.lowercased(), fileInput == "yes" {
    print("Enter the file path:", terminator: " ")
    if let filePath = readLine() {
        analyzer.processFile(atPath: filePath)
    }
} else {
    analyzer.startInteractiveSession()
}
