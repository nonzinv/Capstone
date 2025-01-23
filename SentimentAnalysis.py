from textblob import TextBlob
import csv

def analyze_sentiment():
    print("Sentiment Analysis Test")
    keywords = ["windows", "microsoft", "windows 11", "copilot"]
    negative_log_file = "negative_sentiments.csv"
    with open(negative_log_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        file.seek(0)
        if file.tell() == 0:
            writer.writerow(["Sentence", "Polarity"])
    while True:
        user_input = input("Enter a sentence (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            print("Quitting")
            break
        if not any(keyword.lower() in user_input.lower() for keyword in keywords):
            print(f"Input is irrelevant.")
            continue
        blob = TextBlob(user_input)
        sentiment = blob.sentiment
        print("\nSentiment Analysis Result:")
        print(f"Polarity: {sentiment.polarity:.2f}")
        if sentiment.polarity > 0:
            print("Overall Sentiment: Positive\n")
        elif sentiment.polarity < 0:
            print("Overall Sentiment: Negative\n")
            with open(negative_log_file, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([user_input, f"{sentiment.polarity:.2f}"])
        else:
            print("Overall Sentiment: Neutral\n")

if __name__ == "__main__":
    analyze_sentiment()