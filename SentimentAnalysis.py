from textblob import TextBlob
import csv
import os

def analyze_sentiment():
    print("Sentiment Analysis Test")
    keywords = ["windows", "microsoft", "windows 11", "copilot"]
    negative_log_file = "negative_sentiments.csv"

    # write negative comments into a diff file.
    with open(negative_log_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        file.seek(0)
        if file.tell() == 0:
            writer.writerow(["Sentence", "Polarity"])

    # check if the comment contains the keywords.
    def process_sentence(sentence):
        if not any(keyword.lower() in sentence.lower() for keyword in keywords):
            print(f"Input is irrelevant: {sentence}")
            return
        blob = TextBlob(sentence)
        sentiment = blob.sentiment
        print("\nSentiment Analysis Result:")
        print(f"Sentence: {sentence}")
        print(f"Polarity: {sentiment.polarity:.2f}")
        
        if sentiment.polarity > 0:
            print("Overall Sentiment: Positive\n")
        elif sentiment.polarity < 0:
            print("Overall Sentiment: Negative\n")
            with open(negative_log_file, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([sentence, f"{sentiment.polarity:.2f}"])
        else:
            print("Overall Sentiment: Neutral\n")

    # upload comments as a file instead
    file_input = input("Upload comments as a file? (y/n)").strip().lower()
    if file_input == "y":
        file_path = input("Enter the file path: ").strip()
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                print("\nProcessing file...")
                for line in f:
                    line = line.strip()
                    if line:
                        process_sentence(line)
        else:
            print("File not found. Proceeding with manual input.")

    while True:
        user_input = input("Enter a sentence (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            print("Quitting")
            break
        process_sentence(user_input)

if __name__ == "__main__":
    analyze_sentiment()